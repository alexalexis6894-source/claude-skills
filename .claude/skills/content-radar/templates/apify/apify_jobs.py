#!/usr/bin/env python3
"""Пачка прогонов Apify по файлу заданий. Запускается локально, токен берётся из переменной окружения APIFY_TOKEN
(получить: https://console.apify.com/settings/integrations, в Git и в чат не класть).

  export APIFY_TOKEN=...     # или: APIFY_TOKEN=... python3 apify_jobs.py ...
  python3 apify_jobs.py radar/<slug>/apify/jobs-main.json --max-usd 2 --threads 8

Файл заданий:
{
  "out": "raw",                               # папка результатов; относительный путь считается от папки проекта
                                              # (родитель папки apify/, где лежит этот файл), для ig-заданий "ig"
  "jobs": [
    {"name": "ig-posts", "actor": "apify~instagram-post-scraper", "max_usd": 0.9,
     "trim": "none" | "tiktok",                  # tiktok – оставить только нужные поля
     "input": {...}}
  ]
}

Правила экономии: у каждого прогона свой потолок maxTotalChargeUsd, сумма потолков не может
быть больше общего потолка запуска (--max-usd). Готовый файл результата повторно не собирается,
поэтому прерванный сбор можно просто запустить ещё раз. Платные ИИ-описания и транскрипции запрещены.
Результат: <out>/<name>.json.gz и строка в <out>/../apify/spend.jsonl с фактической ценой.
"""
import argparse, gzip, json, os, pathlib, sys, time, urllib.error, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

print = __import__("functools").partial(print, flush=True)
API = "https://api.apify.com/v2"
TOKEN = os.environ.get("APIFY_TOKEN", "").strip()
FORBIDDEN = {"aiVideoDescription": (True,), "aiVideoSummary": (True,),
             "downloadSubtitlesOptions": ("TRANSCRIBE_ALL_VIDEOS", "DOWNLOAD_AND_TRANSCRIBE_VIDEOS_WITHOUT_SUBTITLES")}


def call(method, path, payload=None, query=None, tries=5, timeout=180):
    q = dict(query or {}, token=TOKEN)
    url = f"{API}{path}?{urllib.parse.urlencode(q)}"
    data = json.dumps(payload).encode() if payload is not None else None
    for attempt in range(1, tries + 1):
        req = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:400]
            if e.code < 500 and e.code != 429 or attempt == tries:
                raise RuntimeError(f"HTTP {e.code} {path}: {body}")
        except (urllib.error.URLError, ConnectionError, TimeoutError, OSError) as e:
            if attempt == tries:
                raise RuntimeError(f"сеть {path}: {e}")
        time.sleep(4 * attempt)


def trim_tiktok(it):
    ch = it.get("channel") or {}
    v = it.get("video") or {}
    subs = [{"lang": s.get("language_code") or s.get("lang"), "url": s.get("url"), "auto": s.get("is_auto_generated")}
            for s in (it.get("subtitleInformation") or []) if s.get("url")]
    return {
        "id": str(it.get("id") or ""), "text": it.get("title"), "views": it.get("views"), "likes": it.get("likes"),
        "comments": it.get("comments"), "shares": it.get("shares"), "saves": it.get("bookmarks"),
        "hashtags": it.get("hashtags"), "ts": it.get("uploadedAt"), "date": (it.get("uploadedAtFormatted") or "")[:10],
        "author": ch.get("username"), "author_name": ch.get("name"), "followers": ch.get("followers"),
        "verified": ch.get("verified"), "author_videos": ch.get("videos"), "region": ch.get("region") or it.get("region"),
        "sec": round(v["duration"]) if isinstance(v.get("duration"), (int, float)) else None,
        "cover": v.get("cover"), "song": (it.get("song") or {}).get("title"), "url": it.get("postPage"),
        "kw": it.get("searchKeyword") or it.get("keyword"), "subs": subs or None, "lang": it.get("textLanguage"),
    }


def guard(inp):
    for k, bad in FORBIDDEN.items():
        if k in inp and inp[k] in bad:
            sys.exit(f"Платная опция {k}={inp[k]!r} запрещена: смысл берём из подписи бесплатно.")


def run_job(job, out, ledger):
    dest = out / f"{job['name']}.json.gz"
    if dest.exists():
        print(f"[{job['name']}] уже собран, пропуск")
        return 0.0
    guard(job["input"])
    q = {"maxTotalChargeUsd": job["max_usd"]}
    if "max_items" in job:
        q["maxItems"] = job["max_items"]
    try:
        run = call("POST", f"/acts/{job['actor']}/runs", job["input"], q)["data"]
    except RuntimeError as e:
        print(f"[{job['name']}] не запустился: {e}")
        return None
    rid = run["id"]
    deadline = time.time() + job.get("timeout_min", 40) * 60
    while run["status"] in ("READY", "RUNNING") and time.time() < deadline:
        time.sleep(10)
        run = call("GET", f"/actor-runs/{rid}")["data"]
    if run["status"] in ("READY", "RUNNING"):
        call("POST", f"/actor-runs/{rid}/abort")
        run = call("GET", f"/actor-runs/{rid}")["data"]
    items, off = [], 0
    while True:
        chunk = call("GET", f"/datasets/{run['defaultDatasetId']}/items", query={"clean": 1, "offset": off, "limit": 1000})
        items += chunk
        if len(chunk) < 1000:
            break
        off += 1000
    if job.get("trim") == "tiktok":
        items = [trim_tiktok(x) for x in items if x.get("id")]
    usd = round(float(run.get("usageTotalUsd") or 0), 5)
    with gzip.open(dest, "wt", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False)
    rec = {"name": job["name"], "actor": job["actor"], "status": run["status"], "items": len(items), "usd": usd,
           "run_id": rid, "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    with open(ledger, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"[{job['name']}] {run['status']}: {len(items)} записей, ${usd}")
    return usd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jobs")
    ap.add_argument("--max-usd", type=float, required=True)
    ap.add_argument("--threads", type=int, default=8)
    a = ap.parse_args()
    if not TOKEN:
        sys.exit("Нет APIFY_TOKEN. Получите токен на https://console.apify.com/settings/integrations и задайте: export APIFY_TOKEN=...")
    cfg = json.loads(pathlib.Path(a.jobs).read_text(encoding="utf-8"))
    out = pathlib.Path(cfg["out"])
    if not out.is_absolute():
        out = pathlib.Path(a.jobs).resolve().parent.parent / out
    out.mkdir(parents=True, exist_ok=True)
    ledger = out.parent / "apify" / "spend.jsonl"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    todo = [j for j in cfg["jobs"] if not (out / f"{j['name']}.json.gz").exists()]
    cap = round(sum(j["max_usd"] for j in todo), 4)
    print(f"Заданий {len(cfg['jobs'])}, к запуску {len(todo)}, сумма потолков ${cap}, потолок запуска ${a.max_usd}")
    if cap > a.max_usd + 1e-9:
        sys.exit("Сумма потолков прогонов больше потолка запуска: уменьшите задания или поднимите max_usd")
    me = call("GET", "/users/me/limits")["data"]
    print("Лимит месяца до запуска:", json.dumps(me.get("current", {}), ensure_ascii=False)[:300])
    used = me.get("current", {}).get("monthlyUsageUsd")
    hard_limit = me.get("limits", {}).get("maxMonthlyUsageUsd")
    if todo and isinstance(used, (int, float)) and isinstance(hard_limit, (int, float)) and used >= hard_limit:
        sys.exit(f"Месячный лимит Apify исчерпан: использовано ${used:.4f}, лимит ${hard_limit:.4f}. Прогоны не запускались.")
    with ThreadPoolExecutor(a.threads) as ex:
        results = list(ex.map(lambda j: run_job(j, out, ledger), todo))
    failed = sum(result is None for result in results)
    spent = sum(result for result in results if result is not None)
    print(f"Прогон стоил ${spent:.4f}")
    me = call("GET", "/users/me/limits")["data"]
    print("Лимит месяца после:", json.dumps(me.get("current", {}), ensure_ascii=False)[:300],
          "из", json.dumps(me.get("limits", {}).get("maxMonthlyUsageUsd")))
    if failed:
        sys.exit(f"Не запустилось {failed} из {len(todo)} заданий. Сбор не завершён; готовые результаты сохранены. Ошибочные задания не считать бесплатным успешным сбором.")


if __name__ == "__main__":
    main()

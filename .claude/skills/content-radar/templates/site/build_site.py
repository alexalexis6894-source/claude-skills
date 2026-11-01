#!/usr/bin/env python3
"""Карта тем TikTok: размеченные ролики -> статическая страница <корень>/<slug>/ (index.html, data.js, app.js, style.css).

  python3 build_site.py <папка проекта> [--root=site]    # например radar/example; страница ляжет в site/<slug>/

Корень выдачи (--root, по умолчанию site) считается от текущей папки. Можно задать и полный путь поля "out" в site.json.

В папке проекта лежат:
  site.json       – бренд, тексты, фильтры (образец: templates/example/site.json)
  labeled.json    – ролики после merge: поля сбора (id, text, author, views, likes, comments, shares, saves, date, sec, url, followers)
                    плюс разметка (theme, format, fit, conf, lang, title, description, hook, idea)
  ideas.json      – карточки вкладки «Что снимать»: id референса, theme, title, hook, plan, mechanic
  findings.html   – (необязательно) короткий блок выводов над идеями
  portrait.html   – (необязательно) вкладка «Портрет Instagram»: кто автор, что продаёт, из чего лента, что собирает реакцию
  queries.json    – (необязательно) поисковые слова, [{"q": "..."}] или ["..."]
  all.json        – (необязательно) все уникальные ролики сбора, для строки «получено / уникальных»
  apify/spend.jsonl – (необязательно) расход Apify по прогонам

Скрипт ничего не придумывает: все числа берёт из файлов. Шаблон страницы и приложение лежат рядом (index.html.tpl, app.js, style.css).
"""
import datetime, html, json, pathlib, shutil, statistics, sys, re

HERE = pathlib.Path(__file__).resolve().parent
KEEP = ["id", "text", "author", "views", "likes", "comments", "shares", "saves", "date", "sec", "url", "theme", "format",
        "fit", "conf", "lang", "title", "description", "hook", "idea", "local"]


def nb(n):
    return f"{n:,}".replace(",", " ")


def clean(s):
    return (s or "").replace("—", "-").replace("–", "-")


def row(r, short=False):
    out = {k: r.get(k) for k in KEEP}
    out["text"] = (r.get("text") or "")[:200 if short else 420]
    for k in ("title", "description", "hook", "idea"):
        out[k] = clean(out.get(k))
    if short:
        for k in ("idea", "hook", "description"):
            out.pop(k, None)
    if not out.get("local"):
        out.pop("local", None)
    return out


def opts(pairs, selected=None):
    return "".join(f'<option value="{html.escape(str(v))}"{" selected" if str(v) == str(selected) else ""}>{html.escape(t)}</option>' for v, t in pairs)


def method(cfg, meta, qlist, nthemes):
    e = html.escape
    qs = " · ".join(e(q) for q in qlist)
    spend = f"<h3>Сколько стоил сбор</h3><p>Apify: ${meta['usd_total']:.2f}.</p>" if meta.get("usd_total") else ""
    return f"""<h3>Источник и объём</h3><p>Срез от {cfg['day_ru']}. Поиск TikTok по {meta['queries']} словам. Получено {nb(meta['raw'])} записей, уникальных {nb(meta['unique'])}.
В карту вошли ролики, опубликованные с {meta['cut']}: {nb(meta['pool'])} по теме и {nb(meta['excluded'])} посторонних или без понятной темы (их можно открыть в таблице, включив «Включить неразобранные и посторонние»).</p>
<h3>Как разобран каждый ролик</h3><p>Тема, формат, язык и снимаемость размечены по подписи и хэштегам параллельными агентами по закрытому словарю из {nthemes} тем. {cfg['method_fit_note']}
Видео целиком агенты не смотрели: содержание сверх подписи не додумывалось, у роликов с пустой подписью разметка помечена как неуверенная.</p>
<h3>Как читать показатели</h3><ul><li>Один ролик относится к одной теме, суммы тем складываются без повторного счёта.</li>
<li>Медиана считается по роликам текущей выборки, с учётом выбранных фильтров. Порог просмотров меняет медиану: чем он выше, тем сильнее она описывает залетевшие ролики, а не нишу целиком.</li>
<li>Сумма просмотров включает повторные просмотры и пересекающиеся аудитории. Это не уникальный охват и не прогноз заявок.</li>
<li>Выдача поиска не является полной или случайной выборкой TikTok. Результат зависит от формулировок запросов.</li>
<li>Цифры TikTok нельзя напрямую переносить на Instagram и на другую страну. Ролики показывают темы и приёмы, которые стоит проверить своими съёмками.</li></ul>
{spend}<h3>Поисковые слова</h3><p>{qs}</p>"""


def main():
    argv = [a for a in sys.argv[1:] if not a.startswith("--")]
    root_arg = next((a[7:] for a in sys.argv[1:] if a.startswith("--root=")), "site")
    if not argv:
        sys.exit("Нужна папка проекта: build_site.py <папка проекта> [--root=site]")
    proj = pathlib.Path(argv[0]).resolve()
    cfg = json.loads((proj / "site.json").read_text(encoding="utf-8"))
    out = pathlib.Path(cfg.get("out") or pathlib.Path(root_arg) / cfg["slug"]).resolve()
    out.mkdir(parents=True, exist_ok=True)

    L = json.loads((proj / "labeled.json").read_text(encoding="utf-8"))
    merge = cfg.get("merge", {})
    noise = set(cfg.get("noise_themes", []))
    loc = cfg.get("local")
    rx = re.compile(loc["regex"], re.I) if loc else None
    for r in L:
        r["theme"] = merge.get(r["theme"], r["theme"])
        if rx:
            blob = " ".join([r.get("text") or ""] + [str(h) for h in (r.get("hashtags") or [])])
            r["local"] = loc["value"] if rx.search(blob) else ""
    rows = [row(r) for r in L if r["theme"] not in noise]
    archive = [row(r, True) for r in L if r["theme"] in noise]
    rows.sort(key=lambda r: -(r["views"] or 0))

    ideas = json.loads((proj / "ideas.json").read_text(encoding="utf-8")) if (proj / "ideas.json").exists() else []
    ids = {r["id"] for r in rows}
    for x in ideas:
        assert x["id"] in ids, f"идея ссылается на неизвестный ролик {x['id']}"
    # Стандарт content-radar: все ролики разобраны по темам и форматам, у каждого заголовок и описание. Без этого страницу не собираем.
    assert len({r["theme"] for r in rows}) >= 12, "тем меньше 12: словарь тем слишком грубый, разметку делать заново по vocab.json"
    assert len({r["format"] for r in rows}) >= 5, "форматов меньше 5: проверьте разметку формата"
    done = sum(1 for r in rows if (r.get("title") or "").strip() and (r.get("description") or "").strip())
    assert done >= .95 * len(rows), f"заголовок и описание есть только у {done} из {len(rows)} роликов"
    assert len(ideas) >= 10, "во вкладке «Что снимать» должно быть от 10 идей (ideas.json)"
    all_path = proj / "all.json"
    unique = len(json.loads(all_path.read_text(encoding="utf-8"))) if all_path.exists() else len(L)
    spend = []
    if (proj / "apify" / "spend.jsonl").exists():
        spend = [json.loads(l) for l in (proj / "apify" / "spend.jsonl").read_text().splitlines() if l.strip()]
    qlist = []
    if (proj / "queries.json").exists():
        q = json.loads((proj / "queries.json").read_text(encoding="utf-8"))
        qlist = [x["q"] if isinstance(x, dict) else x for x in q]
    day = datetime.date.fromisoformat(cfg["day"])
    cuts = {str(d): str(day - datetime.timedelta(days=d)) for d in (30, 90, 180)}
    dates = sorted(r["date"] for r in rows if r.get("date"))
    meta = {"key": cfg["key"], "fit_names": cfg["fit_names"], "fit_short": cfg["fit_short"],
            "lang_main": [v for v, _ in cfg["langs"] if v != "other"], "default_threshold": cfg["default_threshold"],
            "csv_name": cfg["slug"] + ".csv", "idea_hook_label": cfg["idea_hook_label"], "cuts": cuts,
            "raw": sum(x["items"] for x in spend) if spend else len(L), "unique": unique, "pool": len(rows),
            "excluded": len(archive), "queries": len(qlist), "cut": dates[0] if dates else "",
            "usd_total": round(sum(x["usd"] for x in spend), 2) if spend else 0}
    themes = {r["theme"] for r in rows}

    portrait = (proj / "portrait.html").read_text(encoding="utf-8") if (proj / "portrait.html").exists() else ""
    findings = (proj / "findings.html").read_text(encoding="utf-8") if (proj / "findings.html").exists() else ""
    data = {"rows": rows, "archive": archive, "ideas": ideas, "meta": meta, "portrait": portrait,
            "method": method(cfg, meta, qlist, len(themes))}
    (out / "data.js").write_text("const D=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")

    t = cfg["theme"]
    theme_css = (f":root{{--bg:{t['bg']};--accent:{t['accent']};--line:{t['line']};--light:{t['light']}}}"
                 f"header{{background:{t['header']}}}.brand{{border-bottom-color:{t['line']}}}.stat{{border-left-color:{t['line']}}}"
                 f"select,input[type=search],.quiet,.more{{border-color:{t['line']}}}")
    tpl = (HERE / "index.html.tpl").read_text(encoding="utf-8")
    nav_portrait = '<button data-tab="portrait">Портрет Instagram</button>' if portrait else ""
    sec_portrait = ('<section id="portrait" hidden><p class="eyebrow">03 / Отправная точка</p><h2>' + html.escape(cfg["portrait_title"]) +
                    '</h2><div id="portraitContent" class="portrait"></div></section>') if portrait else ""
    local_filter = ""
    if loc:
        local_filter = f'<label>{html.escape(loc["label"])}<select id="local">{opts([("", loc["all"]), (loc["value"], loc["name"])])}</select></label>\n'
    findings_html = f'<div class="findings">{findings}</div>' if findings else ""
    subs = {
        "TITLE": cfg["title"], "DESCRIPTION": cfg["description"], "THEME_CSS": theme_css, "BRAND_UPPER": cfg["brand_upper"],
        "META_LINE": cfg["meta_line"], "EYEBROW": cfg["eyebrow"], "H1": cfg["h1"], "LEAD": cfg["lead"], "NAV_IDEAS": cfg["nav_ideas"],
        "NAV_PORTRAIT": nav_portrait, "FIT_YES_OPT": cfg["fit_opts"][0], "FIT_PART_OPT": cfg["fit_opts"][1],
        "LANG_OPTS": opts(cfg["langs"]), "LOCAL_FILTER": local_filter, "PERIOD_OPTS": opts(cfg["periods"]),
        "THRESHOLD_OPTS": opts(cfg["thresholds"], cfg["default_threshold"]), "SEARCH_PLACEHOLDER": cfg["search_placeholder"],
        "COLLECTION_EXAMPLE": cfg["collection_example"], "IDEAS_TITLE": cfg["ideas_title"], "IDEAS_NOTE": cfg["ideas_note"],
        "FINDINGS": findings_html, "SEC_PORTRAIT": sec_portrait, "METHOD_NUM": "04" if portrait else "03",
        "FOOTER_BRAND": cfg["footer_brand"], "FOOTER_HTML": cfg.get("footer_html", ""),
    }
    page = tpl
    for k, v in subs.items():
        page = page.replace("{{" + k + "}}", v)
    assert "{{" not in page, re.findall(r"\{\{\w+\}\}", page)
    (out / "index.html").write_text(page, encoding="utf-8")
    for f in ("app.js", "style.css"):
        shutil.copy(HERE / f, out / f)
    print(f"rows {len(rows)}, archive {len(archive)}, ideas {len(ideas)}, themes {len(themes)}, data.js {(out / 'data.js').stat().st_size // 1024} КБ -> {out}")
    print(f"Приёмка: node {HERE / 'verify.mjs'} {cfg['slug']} --root={root_arg}  (нужен PASS по всем пунктам)")


if __name__ == "__main__":
    main()

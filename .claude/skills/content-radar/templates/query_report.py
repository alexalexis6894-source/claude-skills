#!/usr/bin/env python3
"""Отдача поисковых запросов: сколько залетевших роликов дал каждый и почём.

Считает по уже собранным radar/<slug>/raw/*.json.gz (их кладёт apify_jobs.py), денег не тратит. Нужен, чтобы при повторном
сборе по той же нише не платить за запросы, которые ничего не принесли.

    python3 query_report.py radar/<slug>            # порог 500 тыс. просмотров
    python3 query_report.py radar/<slug> 1000000    # свой порог
"""
import glob, gzip, json, pathlib, sys
from collections import defaultdict

if len(sys.argv) < 2:
    sys.exit("Нужна папка проекта: query_report.py radar/<slug> [порог просмотров]")
BASE = pathlib.Path(sys.argv[1]).resolve()
PRICE = 0.0003  # доллар за запись apidojo~tiktok-scraper; для другого актора поправьте
HIT = int(sys.argv[2]) if len(sys.argv) > 2 else 500_000


def load():
    per, views, pos_stat = defaultdict(set), {}, defaultdict(lambda: [0, 0])
    for f in sorted(glob.glob(str(BASE / "raw" / "*.json.gz"))):
        name = pathlib.Path(f).name
        if any(x in name for x in ("comments", "profiles", "ai-described", "_probe")):
            continue
        items = json.load(gzip.open(f, "rt", encoding="utf-8"))
        for pos, i in enumerate(items, 1):
            vid = str(i.get("id") or "")
            if not vid:
                continue
            v = i.get("views") or 0
            per[i.get("kw") or name.split(".")[0]].add(vid)
            views[vid] = v
            b = f"{(pos - 1) // 25 * 25 + 1}-{(pos - 1) // 25 * 25 + 25}"
            pos_stat[b][0] += 1
            pos_stat[b][1] += v >= HIT
    return per, views, pos_stat


def main():
    per, views, pos_stat = load()
    if not per:
        sys.exit("В raw/ нет выгрузок поиска (*.json.gz)")
    hits = {v for v, x in views.items() if x >= HIT}
    total_items = sum(len(s) for s in per.values())
    print(f"запросов {len(per)}, уникальных роликов {len(views)}, от {HIT//1000} тыс. {len(hits)}")
    print(f"оплачено записей примерно {total_items}, это около ${total_items * PRICE:.2f}\n")

    print("отдача запросов, от лучшего к худшему:")
    rows = sorted(((q, len(s), len(s & hits)) for q, s in per.items()), key=lambda r: -r[2])
    for q, n, hi in rows:
        price = f"${n * PRICE / hi:.4f}" if hi else "ничего не дал"
        print(f"  {hi:>3} из {n:>3} | {price:>13} за находку | {q[:52]}")

    print("\nглубина выдачи:")
    for k in sorted(pos_stat, key=lambda x: int(x.split("-")[0])):
        n, hi = pos_stat[k]
        print(f"  позиции {k:>7}: {hi:>4} из {n:>5} залетевших ({round(100*hi/n) if n else 0}%)")

    # Жадное покрытие: минимальный набор запросов, который даёт почти всех залетевших.
    print("\nминимальный набор запросов:")
    pool, covered, spent, n_q = dict(per), set(), 0.0, 0
    while pool:
        q, ids = max(pool.items(), key=lambda kv: len((kv[1] & hits) - covered))
        gain = len((ids & hits) - covered)
        if not gain:
            break
        covered |= ids & hits
        spent += len(ids) * PRICE
        n_q += 1
        del pool[q]
        if n_q % 5 == 0 or len(covered) == len(hits):
            print(f"  {n_q:>2} запросов: покрыто {len(covered):>4} из {len(hits)} "
                  f"({round(100*len(covered)/len(hits)):>3}%), потрачено ~${spent:.2f}")
    print("\nфактические пересечения запросов, за них платили дважды:")
    overlaps = []
    qs = list(per)
    for i, a in enumerate(qs):
        for b in qs[i + 1:]:
            both = per[a] & per[b]
            if len(both) >= 10:
                overlaps.append((len(both), a, b))
    for n_, a, b in sorted(overlaps, reverse=True)[:6]:
        print(f"  {n_:>3} общих роликов (~${n_ * PRICE:.2f}) | «{a[:28]}» и «{b[:28]}»")
    if not overlaps:
        print("  заметных пересечений нет, формулировки подобраны удачно")
    else:
        print(f"  всего пересечений от 10 роликов: {len(overlaps)}, "
              f"суммарно ~${sum(n for n, _, _ in overlaps) * PRICE:.2f}")

    dead = list(pool)
    if dead:
        print(f"\n  ничего уникального не дали {len(dead)} запросов, в следующий раз не брать:")
        for q in dead[:8]:
            print(f"    {q[:60]}")


if __name__ == "__main__":
    main()

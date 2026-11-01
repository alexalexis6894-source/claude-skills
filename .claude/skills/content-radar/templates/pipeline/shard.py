#!/usr/bin/env python3
"""all.json -> shards/shard-NN.json по SIZE роликов для параллельной разметки.

  python3 shard.py <папка проекта> [MIN_VIEWS=1000] [SIZE=130] [REGEX_ИМЁН_ПРОГОНОВ_КОТОРЫЕ_БРАТЬ_ВСЕГДА]

Берём ролики с просмотрами не ниже MIN_VIEWS, плюс все, найденные прогонами, чьё имя подходит под регулярное выражение
(например русские и местные запросы: `-ru-|-loc-`). Сортировка по просмотрам, поэтому нулевой шард самый сильный."""
import json, pathlib, re, sys
root = pathlib.Path(sys.argv[1]).resolve()
MIN_VIEWS = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
SIZE = int(sys.argv[3]) if len(sys.argv) > 3 else 130
rx = re.compile(sys.argv[4]) if len(sys.argv) > 4 else None
allv = json.load(open(root / "all.json"))
keep = [v for v in allv if (v.get("views") or 0) >= MIN_VIEWS or (rx and any(rx.search(s) for s in v["src"]))]
keep.sort(key=lambda v: -(v.get("views") or 0))
(root / "shards").mkdir(exist_ok=True)
for old in (root / "shards").glob("shard-*.json"):
    old.unlink()
fields = ["id", "text", "hashtags", "views", "likes", "saves", "shares", "comments", "sec", "author", "followers", "kw", "lang"]
n = 0
for i in range(0, len(keep), SIZE):
    chunk = [{k: v.get(k) for k in fields} for v in keep[i:i + SIZE]]
    for c in chunk:
        c["text"] = (c["text"] or "")[:400]
    json.dump(chunk, open(root / "shards" / f"shard-{n:02d}.json", "w"), ensure_ascii=False)
    n += 1
print(f"отобрано {len(keep)} из {len(allv)}, шардов {n}")

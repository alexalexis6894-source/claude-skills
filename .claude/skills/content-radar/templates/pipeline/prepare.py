#!/usr/bin/env python3
"""raw/*.json.gz -> all.json (уникальные ролики; поле src – из каких прогонов пришёл, kws – по каким запросам).

  python3 prepare.py <папка проекта>"""
import gzip, json, glob, pathlib, statistics, re, sys
root = pathlib.Path(sys.argv[1]).resolve()
rows = {}
for f in sorted(glob.glob(str(root / "raw" / "*.json.gz"))):
    for it in json.load(gzip.open(f)):
        i = it.get("id")
        if not i:
            continue
        kw = it.get("kw")
        cur = rows.get(i)
        if cur is None:
            it["kws"] = [kw] if kw else []
            it["src"] = [pathlib.Path(f).stem]
            rows[i] = it
        else:
            if kw and kw not in cur["kws"]:
                cur["kws"].append(kw)
            cur["src"].append(pathlib.Path(f).stem)
allv = list(rows.values())
json.dump(allv, open(root / "all.json", "w"), ensure_ascii=False)
print("уникальных роликов", len(allv), "медиана просмотров", statistics.median([v.get("views") or 0 for v in allv]))

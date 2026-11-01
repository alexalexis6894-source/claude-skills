#!/usr/bin/env python3
"""labels/shard-NN.jsonl + all.json -> labeled.json. Сверяет порядок и id с шардами, значения осей со словарём vocab.json.

  python3 merge.py <папка проекта>

Обязательные поля разметки: id, theme, format, fit, conf, lang, title, description, hook, idea."""
import json, pathlib, glob, sys
root = pathlib.Path(sys.argv[1]).resolve()
V = json.load(open(root / "vocab.json"))["axes"]
allv = {v["id"]: v for v in json.load(open(root / "all.json"))}
out, bad, miss = [], [], []
for f in sorted(glob.glob(str(root / "shards" / "shard-*.json"))):
    n = pathlib.Path(f).stem.split("-")[1]
    src = [str(r["id"]) for r in json.load(open(f))]
    lf = root / "labels" / f"shard-{n}.jsonl"
    if not lf.exists():
        miss.append(n); continue
    got = [json.loads(l) for l in open(lf, encoding="utf-8") if l.strip()]
    if [str(g["id"]) for g in got] != src:
        print("РАСХОЖДЕНИЕ", n, len(got), len(src)); sys.exit(1)
    for g in got:
        for k, vals in V.items():
            if g.get(k) not in vals:
                bad.append((n, g["id"], k, g.get(k)))
        if not (g.get("title") or "").strip():
            bad.append((n, g["id"], "title", ""))
        row = dict(allv[str(g["id"])])
        row.update({k: g.get(k) for k in list(V) + ["title", "description", "hook", "idea"]})
        out.append(row)
print("размечено", len(out), "нарушений", len(bad), "нет файлов", miss)
for b in bad[:30]: print(b)
json.dump(out, open(root / "labeled.json", "w"), ensure_ascii=False)
sys.exit(1 if bad or miss else 0)

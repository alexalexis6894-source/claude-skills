#!/usr/bin/env python3
"""labeled.json -> findings.html: короткие выводы с числами из данных (блок над идеями во вкладке «Что снимать»).

  python3 findings.py <папка проекта> [минимум роликов в теме для вывода, по умолчанию 30]

Скрипт универсальный: ничего не знает о нише, считает по осям theme, format, lang и по полю local из site.json.
Формулировки это заготовка: прочитайте findings.html и допишите смысл под бренд (что в план берём, что нет и почему).
Темы с малой выборкой в выводы не попадают. Числа везде по всей собранной выборке без порога просмотров."""
import html, json, pathlib, re, statistics as st, sys

root = pathlib.Path(sys.argv[1]).resolve()
MIN_N = int(sys.argv[2]) if len(sys.argv) > 2 else 30
cfg = json.loads((root / "site.json").read_text(encoding="utf-8"))
noise = set(cfg.get("noise_themes", []))
merge = cfg.get("merge", {})
rows = [r for r in json.loads((root / "labeled.json").read_text(encoding="utf-8"))]
for r in rows:
    r["theme"] = merge.get(r["theme"], r["theme"])
rows = [r for r in rows if r["theme"] not in noise]
e = html.escape


def num(n):
    n = int(round(n))
    if n >= 1_000_000:
        return f"{n / 1e6:.1f}".replace(".", ",") + " млн"
    if n >= 10_000:
        return f"{round(n / 1000)} тыс."
    if n >= 1000:
        return f"{n / 1000:.1f}".replace(".", ",") + " тыс."
    return str(n)


def pct(x):
    return f"{x * 100:.1f}".replace(".", ",") + "%"


def rate(r, k):
    return (r.get(k) or 0) / r["views"] if r.get("views") else 0


def group(key, fn=lambda r: True):
    g = {}
    for r in rows:
        if fn(r):
            g.setdefault(r[key], []).append(r)
    return g


def stat(g):
    return {"n": len(g), "med": st.median([r["views"] or 0 for r in g]), "save": st.median([rate(r, "saves") for r in g])}


allst = stat(rows)
themes = {k: stat(g) for k, g in group("theme").items() if len(g) >= MIN_N}
yes = {k: stat(g) for k, g in group("theme", lambda r: r["fit"] == "yes").items() if len(g) >= max(10, MIN_N // 2)}
fmts = {k: stat(g) for k, g in group("format").items() if len(g) >= MIN_N and k != "Неясно"}
li = []
if themes:
    top = sorted(themes.items(), key=lambda kv: -kv[1]["save"])[:3]
    li.append("<li><b>Эти темы чаще всего сохраняют.</b> " + "; ".join(f"«{e(k)}» {pct(s['save'])}" for k, s in top) +
              f" (по всей выборке {pct(allst['save'])}). Сохранение означает «вернусь и повторю»: так ведёт себя полезный ролик.</li>")
if yes:
    top = sorted(yes.items(), key=lambda kv: -kv[1]["med"])[:3]
    li.append("<li><b>Охват у снимаемого своими силами дают:</b> " + "; ".join(f"«{e(k)}» (медиана {num(s['med'])}, роликов: {s['n']})" for k, s in top) +
              f". Медиана всей выборки {num(allst['med'])}.</li>")
if fmts:
    best = max(fmts.items(), key=lambda kv: kv[1]["med"])
    worst = min(fmts.items(), key=lambda kv: kv[1]["med"])
    li.append(f"<li><b>Среди форматов выше всех «{e(best[0])}»:</b> медиана {num(best[1]['med'])} при {best[1]['n']} роликах; ниже всех «{e(worst[0])}» – {num(worst[1]['med'])}.</li>")
ru = [r for r in rows if r.get("lang") == "ru"]
if ru:
    line = f"Русских роликов {len(ru)} из {len(rows)}, медиана русских {num(st.median([r['views'] or 0 for r in ru]))}"
    loc = cfg.get("local")
    if loc:
        rx = re.compile(loc["regex"], re.I)
        near = [r for r in rows if rx.search(" ".join([r.get("text") or ""] + [str(h) for h in (r.get("hashtags") or [])]))]
        if near:
            line += f"; с привязкой «{e(loc['name'])}» {len(near)}, их медиана {num(st.median([r['views'] or 0 for r in near]))}"
    li.append(f"<li><b>Язык и география.</b> {line}.</li>")
out = (f"<h3>Что показали данные</h3><ul>{''.join(li)}</ul><p class='small'>Числа по всей собранной выборке без порога просмотров "
       f"(роликов по темам: {len(rows)}). Фильтры страницы пересчитывают карту под выбранный порог. Это связи, а не причины.</p>")
out = out.replace("тыс..", "тыс.").replace("млн..", "млн.")
(root / "findings.html").write_text(out, encoding="utf-8")
print(re.sub(r"<[^>]+>", " ", out)[:1500])

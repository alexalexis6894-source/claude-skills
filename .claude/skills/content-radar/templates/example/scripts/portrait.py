#!/usr/bin/env python3
"""ig/ig-profile.json.gz + ig/ig-posts.json.gz + portrait.json -> portrait.html (вкладка «Портрет Instagram»).

  python3 portrait.py <папка проекта>

Выгрузки лежат в ig/ после запуска apify/jobs-ig.json (apify~instagram-profile-scraper и apify~instagram-post-scraper).
Таблицы и числа считаются из постов, текст пишете вы в portrait.json (образец рядом):
  note    – одна строка о срезе: дата, профиль, сколько постов прочитано, что не смотрели
  who     – абзац «Кто это» (HTML)
  sells   – абзац «Что продаёт» (HTML)
  rubrics – [["Название рубрики", "регулярное выражение по подписи"], ...]; пост попадает в первую подошедшую рубрику
  points  – список выводов «Что собирает реакцию» (HTML); числа берите из таблиц ниже
  extra   – необязательно: ещё один блок HTML в конце
Видео и сторис не смотрим: портрет строится по подписям и реакциям."""
import collections, gzip, html, json, pathlib, re, statistics, sys

root = pathlib.Path(sys.argv[1]).resolve()
P = json.load(gzip.open(root / "ig" / "ig-posts.json.gz", "rt", encoding="utf-8"))
pr = json.load(gzip.open(root / "ig" / "ig-profile.json.gz", "rt", encoding="utf-8"))
pr = pr[0] if isinstance(pr, list) else pr
C = json.loads((root / "portrait.json").read_text(encoding="utf-8"))
e = html.escape
P.sort(key=lambda p: p.get("timestamp") or "", reverse=True)
likes = [p.get("likesCount") or 0 for p in P]
med = int(statistics.median(likes)) if likes else 0
RUB = C.get("rubrics", [])


def rub(p):
    c = (p.get("caption") or "").lower()
    for name, rx in RUB:
        if re.search(rx, c):
            return name
    return "Без подписи или прочее"


by = collections.defaultdict(list)
for p in P:
    by[rub(p)].append(p.get("likesCount") or 0)
rub_rows = "".join(f"<tr><td>{e(k)}</td><td class='num'>{len(v)}</td><td class='num'>{int(statistics.median(v))}</td></tr>"
                   for k, v in sorted(by.items(), key=lambda kv: -len(kv[1])))
top = sorted(P, key=lambda p: -(p.get("likesCount") or 0))[:6]
tops = "".join(f"<tr><td class='num'>{p.get('likesCount') or 0}</td><td class='num'>{p.get('commentsCount') or 0}</td><td>{(p.get('timestamp') or '')[:10]}</td>"
               f"<td><a href='{e(p.get('url') or '')}' target='_blank' rel='noopener'>{e(((p.get('caption') or 'без подписи').split(chr(10))[0])[:90])}</a></td></tr>" for p in top)
videos = sum(1 for p in P if p.get("type") == "Video")
first = (P[-1].get("timestamp") or "")[:10] if P else ""
points = "".join(f"<li>{x}</li>" for x in C.get("points", []))
out = f"""
<p class="note">{C.get('note', '')}</p>
<h3>Кто это</h3>
<p>{C.get('who', '')} Подписчиков: {format(pr.get('followersCount', 0), ',').replace(',', ' ')}, постов: {pr.get('postsCount', 0)}.</p>
<h3>Что продаёт</h3>
<p>{C.get('sells', '')}</p>
<h3>Из чего состоит лента</h3>
<div class="tablewrap"><table><tr><th>Рубрика</th><th class="num">Постов</th><th class="num">Медиана лайков</th></tr>{rub_rows}</table></div>
<h3>Что собирает реакцию</h3>
<p>Лайков на пост: медиана {med}, максимум {max(likes) if likes else 0}. Видео {videos} из {len(P)}. Все посты опубликованы с {first}.</p>
<div class="tablewrap"><table><tr><th class="num">Лайки</th><th class="num">Комм.</th><th>Дата</th><th>Пост</th></tr>{tops}</table></div>
<ul>{points}</ul>
{C.get('extra', '')}
"""
(root / "portrait.html").write_text(out, encoding="utf-8")
print("portrait.html", len(out))

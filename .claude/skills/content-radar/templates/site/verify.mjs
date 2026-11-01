#!/usr/bin/env node
/* Приёмка страницы карты тем content-radar. Без PASS по всем пунктам страницу не сдают.

     node <скилл>/templates/site/verify.mjs <slug>                  # из корня проекта: страница site/<slug>/index.html, сервер поднимается сам
     node <скилл>/templates/site/verify.mjs <slug> --root=public    # если страница собрана не в site/, а в другой папке
     node <скилл>/templates/site/verify.mjs <slug> --base=https://вы.github.io/репо   # проверить опубликованный адрес
                                                                    # (base – корень сайта, страница лежит по <base>/<slug>/)

   Нужен Playwright: npm i playwright && npx playwright install chromium (в папке проекта или глобально).

   Что проверяется на 1280 и 390 px: темы идут одной таблицей (не карточками и не переходом на другую вкладку), у каждой строки
   сумма, медиана, число роликов и авторов, колонки ранжируют, строка раскрывается шторкой с форматами и роликами, лента запускается
   из шторки и закрывается на том же ролике, разрез «по форматам», фильтры пересчитывают таблицу, идеи и метод на месте,
   разметка полная (темы, форматы, заголовок и описание у роликов), нет U+2014 в тексте страницы, нет ошибок JS. */
import { createRequire } from 'node:module';
import { createServer } from 'node:http';
import { execSync } from 'node:child_process';
import { readFileSync, existsSync, statSync } from 'node:fs';
import { dirname, extname, join, resolve } from 'node:path';

const require = createRequire(import.meta.url);
function loadPlaywright() {
  const roots = [process.cwd() + '/', import.meta.url];
  const tries = [];
  for (const r of roots) { try { tries.push(createRequire(r).resolve('playwright')); } catch (_) { /* нет в этой папке */ } }
  try { tries.push(join(execSync('npm root -g', { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim(), 'playwright')); } catch (_) { /* npm недоступен */ }
  for (const t of tries) { try { return require(t); } catch (_) { /* следующий путь */ } }
  console.error('Не найден playwright. Установите: npm i playwright && npx playwright install chromium'); process.exit(2);
}
const { chromium } = loadPlaywright();
const CHROME = process.env.CHROMIUM_PATH && existsSync(process.env.CHROMIUM_PATH) ? process.env.CHROMIUM_PATH : undefined; // по умолчанию браузер Playwright

const args = process.argv.slice(2);
const slug = args.find(a => !a.startsWith('--'));
const baseArg = (args.find(a => a.startsWith('--base=')) || '').slice(7).replace(/\/$/, '');
const rootArg = (args.find(a => a.startsWith('--root=')) || '').slice(7) || 'site';
if (!slug) { console.error('Нужен slug: verify.mjs <slug> [--root=site] [--base=URL]'); process.exit(2); }

let server = null, base = baseArg;
if (!base) {
  const root = resolve(rootArg), mime = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.png': 'image/png', '.woff2': 'font/woff2', '.json': 'application/json' };
  server = createServer((q, r) => {
    let p = decodeURIComponent(q.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html';
    const f = join(root, p);
    if (!f.startsWith(root) || !existsSync(f) || !statSync(f).isFile()) { r.writeHead(404); r.end(); return; }
    r.writeHead(200, { 'content-type': mime[extname(f)] || 'application/octet-stream' }); r.end(readFileSync(f));
  });
  await new Promise(ok => server.listen(0, ok));
  base = `http://localhost:${server.address().port}`;
}
const url = `${base}/${slug}/index.html`;

const results = [];
const ok = (name, cond, detail = '') => { results.push({ name, pass: !!cond, detail }); };
const nums = a => a.map(v => (v == null ? -1 : v));
const sorted = (a, dir) => nums(a).every((v, i, x) => i === 0 || (dir < 0 ? x[i - 1] >= v : x[i - 1] <= v));

const browser = await chromium.launch(CHROME ? { executablePath: CHROME } : {});
for (const [vname, vp, mobile] of [['десктоп', { width: 1280, height: 900 }, false], ['телефон', { width: 390, height: 844 }, true]]) {
  const ctx = await browser.newContext({ viewport: vp, isMobile: mobile, hasTouch: mobile, deviceScaleFactor: mobile ? 2 : 1 });
  const p = await ctx.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  p.on('console', m => { if (m.type() === 'error' && !/tiktok|ERR_|Failed to load|net::/i.test(m.text())) errs.push(m.text()); });
  await p.route(/tiktok\.com/, r => r.abort());
  const T = s => `[${vname}] ${s}`;
  try {
    await p.goto(url, { waitUntil: 'load' });
    await p.waitForSelector('.grp', { timeout: 8000 });
  } catch (e) { ok(T('страница открылась и в ней есть таблица тем'), false, e.message); await ctx.close(); continue; }

  // 1. Вид: таблица, а не карточки и не вкладка со списком роликов
  ok(T('нет карточек тем и вкладки «Ролики»'), (await p.locator('#topicGrid, .topic-card, [data-tab="videos"]').count()) === 0);
  const n = await p.locator('.grp').count();
  ok(T('темы строками таблицы, не меньше 10'), n >= 10, `строк ${n}`);
  const cells = await p.$$eval('.grp-head', hs => hs.map(h => ({ c: h.querySelectorAll('.g-c').length, med: (h.querySelector('.g-c.med b') || {}).textContent })));
  ok(T('в каждой строке шесть показателей и медиана'), cells.every(x => x.c === 6 && x.med && x.med !== 'нет данных' && x.med !== '–'), JSON.stringify(cells.find(x => !(x.c === 6 && x.med && x.med !== 'нет данных' && x.med !== '–')) || ''));
  const tabs = await p.$$eval('nav [data-tab]', b => b.map(x => x.textContent.trim()));
  ok(T('вкладки: Темы и ролики, идеи, Как считали'), tabs[0] === 'Темы и ролики' && tabs.includes('Как считали') && tabs.length >= 3, tabs.join(' | '));

  // 2. Ранжирование
  if (!mobile) {
    ok(T('шапка с семью сортируемыми колонками'), (await p.locator('.tt-head [data-sort]').count()) === 7);
    await p.click('.tt-head [data-sort="median"]');
    let med = await p.evaluate(() => [...G.values()].map(g => g.median));
    ok(T('клик по «Медиана» ранжирует по убыванию'), sorted(med, -1));
    await p.click('.tt-head [data-sort="median"]');
    med = await p.evaluate(() => [...G.values()].map(g => g.median));
    ok(T('второй клик меняет направление'), sorted(med, 1));
    await p.click('.tt-head [data-sort="sum"]');
  } else {
    await p.selectOption('#topicSort', 'median');
    const med = await p.evaluate(() => [...G.values()].map(g => g.median));
    ok(T('выбор «По медиане» ранжирует таблицу'), sorted(med, -1));
    await p.selectOption('#topicSort', 'sum');
  }

  // 3. Шторка: форматы внутри, ролики внутри, лента из шторки
  await p.locator('.grp-head').first().click();
  await p.waitForSelector('.grp.open .video-card', { timeout: 5000 }).catch(() => {});
  ok(T('строка раскрывается на месте'), (await p.locator('.grp.open').count()) === 1);
  ok(T('внутри шторки мини-таблица форматов с медианами'), (await p.locator('.grp.open .sub-r[data-sub]').count()) >= 2);
  ok(T('внутри шторки карточки роликов'), (await p.locator('.grp.open .video-card').count()) >= 1);
  const card = await p.$eval('.grp.open .video-card', c => ({ h: c.querySelector('h3').textContent.trim(), d: c.querySelectorAll('p').length, play: !!c.querySelector('[data-play]'), a: !!c.querySelector('a[href*="tiktok.com"]') }));
  ok(T('у карточки заголовок, описание, «Смотреть отсюда» и ссылка в TikTok'), card.h && card.d >= 2 && card.play && card.a, JSON.stringify(card));
  const before = await p.locator('.grp.open .g-count').innerText();
  await p.locator('.grp.open .sub-r[data-sub]').nth(1).click();
  ok(T('клик по формату фильтрует ролики темы'), (await p.locator('.grp.open .g-count').innerText()) !== before || (await p.locator('.grp.open .sub-r.on[data-sub]:not([data-sub=""])').count()) === 1);
  await p.locator('.grp.open [data-playg]').first().click();
  await p.waitForSelector('#feed:not([hidden])', { timeout: 4000 }).catch(() => {});
  const feed = await p.evaluate(() => ({ shown: !document.querySelector('#feed').hidden, slides: document.querySelectorAll('#feedList .slide').length, src: (document.querySelector('#feedList iframe') || {}).src || '' }));
  ok(T('«Смотреть подряд» открывает ленту с плеером TikTok прямо из шторки'), feed.shown && feed.slides >= 1 && feed.src.includes('/player/v1/'), JSON.stringify(feed));
  await p.keyboard.press('Escape');
  await p.waitForTimeout(500);
  ok(T('закрытие ленты возвращает к той же теме и ролику'), (await p.locator('#feed').isHidden()) && (await p.locator('.grp.open').count()) === 1 && (await p.locator('.video-card.here').count()) === 1);

  // 4. Разрез по форматам и фильтры
  const themes = await p.evaluate(() => [...G.keys()].join('|'));
  await p.click('[data-axis="format"]');
  const formats = await p.evaluate(() => [...G.keys()].join('|'));
  ok(T('переключатель «По форматам» строит ту же таблицу по форматам'), formats !== themes && (await p.locator('.grp').count()) >= 4);
  await p.click('[data-axis="theme"]');
  const total = await p.evaluate(() => base().length);
  await p.selectOption('#threshold', { index: await p.$$eval('#threshold option', o => o.length - 1) });
  ok(T('порог просмотров пересчитывает таблицу и показатели'), (await p.evaluate(() => base().length)) < total);
  await p.click('#reset');
  const word = await p.evaluate(() => { const r = rows.find(x => x.title && x.title.split(/\s+/).some(w => w.length >= 6)); return r ? r.title.split(/\s+/).find(w => w.length >= 6).replace(/[^\p{L}]/gu, '') : ''; });
  await p.fill('#search', word); await p.waitForTimeout(450);
  const found = await p.evaluate(() => base().length);
  ok(T('поиск сужает выборку и пересчитывает таблицу'), found >= 1 && found <= total, `слово «${word}», роликов ${found} из ${total}`);
  await p.fill('#search', ''); await p.waitForTimeout(300);

  // 5. Остальные вкладки
  await p.click('nav [data-tab="ideas"]');
  const ideas = await p.$$eval('#ideaGrid .idea', a => a.map(x => !!x.querySelector('a[href*="tiktok.com"]')));
  ok(T('«Что снимать»: от 10 идей, у каждой референс'), ideas.length >= 10 && ideas.every(Boolean), `идей ${ideas.length}`);
  await p.click('nav [data-tab="method"]');
  ok(T('«Как считали» заполнена'), (await p.locator('#methodContent').innerText()).length > 300);
  if (mobile) ok(T('нет горизонтальной прокрутки'), await p.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1));
  ok(T('нет ошибок JS'), errs.length === 0, errs.slice(0, 2).join(' / '));

  // 6. Полнота разметки и чистота текста (один раз)
  if (!mobile) {
    const d = await p.evaluate(() => {
      const R = D.rows, has = (r, k) => r[k] && String(r[k]).trim();
      const yes = R.filter(r => r.fit === 'yes');
      return {
        rows: R.length, themes: new Set(R.map(r => r.theme)).size, formats: new Set(R.map(r => r.format)).size,
        td: R.filter(r => has(r, 'title') && has(r, 'description')).length / R.length,
        idea: yes.length ? yes.filter(r => has(r, 'idea')).length / yes.length : 1,
        ideasOk: D.ideas.every(x => R.some(r => r.id === x.id)), ideaN: D.ideas.length,
        dash: [document.documentElement.outerHTML.replace(/<script[\s\S]*?<\/script>/g, ''), D.method, D.portrait, JSON.stringify(D.ideas), R.map(r => [r.title, r.description, r.hook, r.idea].join(' ')).join(' ')].filter(s => s && s.includes('—')).length,
      };
    });
    ok('разметка: не меньше 12 тем и 5 форматов', d.themes >= 12 && d.formats >= 5, `тем ${d.themes}, форматов ${d.formats}`);
    ok('разметка: у 95% роликов есть заголовок и описание', d.td >= .95, `${Math.round(d.td * 100)}%`);
    ok('разметка: у 90% снимаемых есть «как снять у себя»', d.idea >= .9, `${Math.round(d.idea * 100)}%`);
    ok('идеи ссылаются на ролики из выборки', d.ideasOk && d.ideaN >= 10, `идей ${d.ideaN}`);
    ok('в тексте страницы нет длинного тире U+2014', d.dash === 0);
  }
  await ctx.close();
}
await browser.close();
if (server) server.close();

const bad = results.filter(r => !r.pass);
for (const r of results) console.log(`${r.pass ? '  PASS' : '  FAIL'}  ${r.name}${r.pass || !r.detail ? '' : '  ← ' + r.detail}`);
console.log(`\n${bad.length ? 'НЕ ПРОШЛА' : 'ПРИЁМКА ПРОЙДЕНА'}: ${results.length - bad.length} из ${results.length}  (${url})`);
process.exit(bad.length ? 1 : 0);

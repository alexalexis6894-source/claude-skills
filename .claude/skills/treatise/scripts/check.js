// Проверка страницы-трактата: ошибки консоли, горизонтальное переполнение, скриншоты глав.
// Запуск: NODE_PATH=$(npm root -g) node check.js <файл.html или URL> [папка для скриншотов]
// Нужен Playwright (npm i -g playwright && npx playwright install chromium).
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const target = process.argv[2];
const out = process.argv[3] || 'qa';
if (!target) { console.error('Укажите файл или URL страницы'); process.exit(2); }
const url = /^https?:|^file:/.test(target) ? target : 'file://' + path.resolve(target);
fs.mkdirSync(out, { recursive: true });

(async () => {
  const browser = await chromium.launch();
  let bad = 0;
  for (const [w, h] of [[1440, 900], [390, 844]]) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    const errors = [];
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('pageerror', e => errors.push(String(e)));
    await page.goto(url);
    await page.waitForTimeout(600);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    const scenes = await page.$$('.m-scene');
    for (let i = 0; i < scenes.length; i++) {          // каждую сцену прокручиваем в экран, чтобы она сыграла
      await scenes[i].scrollIntoViewIfNeeded();
      await page.waitForTimeout(2200);
      await scenes[i].screenshot({ path: path.join(out, `scene-${i + 1}-${w}.png`) });
    }
    await page.evaluate(() => scrollTo(0, 0));
    await page.screenshot({ path: path.join(out, `top-${w}.png`) });
    console.log(`${w}px: сцен ${scenes.length}, переполнение ${overflow}px, ошибок консоли ${errors.length}`);
    errors.forEach(e => console.log('  ' + e));
    if (overflow !== 0 || errors.length) bad++;
    await page.close();
  }
  await browser.close();
  process.exit(bad ? 1 : 0);
})();

# Реестр скиллов

Память скилла `skill-scout`: где искать, что уже проверено и что помогло. Разведчик читает
этот файл первым, а после каждой задачи ведущий дописывает вердикт.

Порог для внешних скиллов: репозиторий от 10 000 звёзд, обновлялся за полгода, есть `SKILL.md`,
лицензия позволяет копировать. Звёзды ниже сверены через GitHub в октябре 2026 года, перепроверять,
если запись старше 30 дней. «Не читан» значит, что источник прошёл порог по звёздам, но его
`SKILL.md` ещё никто не читал глазами, перед установкой обязательно прочитать.

## Скиллы этого набора (`.claude/skills/`)

Порог звёзд к ним не применяется.

| Скилл | Для чего |
|---|---|
| skill-scout | разведка скиллов перед сложной задачей |
| trio | план тремя агентами для больших задач |
| apple-design, awwwards-research, playground | интерфейсы, анимация, референсы, интерактивные песочницы |
| treatise | наглядная объяснялка сложной темы: страница со сценами и шторками |
| tekst-produkt | тексты продуктовых страниц и смет для заказчиков и людей из стройки |
| write-ru, editor-ru, humanizer-ru, minto-pyramid | русский текст: мысль, слова, правка |
| humanize, ai-check | английский текст без следов ИИ, проверка на «звучит как ИИ» |
| naming, brand-naming, brand-naming-strategies, brand-positioning | нейминг и позиционирование |
| management-consulting, market-research-reports, startup-financial-modeling, the-fool | разбор бизнеса |
| linkedin-* | посты, профиль, планы и аудит для LinkedIn |
| supabase, supabase-postgres-best-practices | базы данных |
| find-skills, i-have-adhd | поиск скиллов, формат ответов для читателя с СДВГ |

## Большие сборники (искать внутри по теме)

| Репозиторий | ★ | Что внутри | Статус |
|---|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | 181 049 | официальные: документы, дизайн, skill-creator, webapp-testing | официальный |
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | 37 947 | официальный каталог плагинов | официальный |
| [obra/superpowers](https://github.com/obra/superpowers) | 298 935 | методология разработки, работа субагентами, брейншторм | не читан |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 290 563 | инженерные скиллы (из него призма архитектора в trio) | частично в trio |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | 278 937 | скиллы, память, безопасность, research-first | не читан |
| [garrytan/gstack](https://github.com/garrytan/gstack) | 136 365 | роли CEO, дизайнер, инженер, QA (из него призма инженера в trio) | пригоден целиком, ставится по инструкции репозитория |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 106 478 | продакшн-инженерия, test-driven-development | не читан |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 77 074 | каталог | список |
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | 55 658 | каталог скиллов, агентов, хуков | список |
| [sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) | 47 583 | каталог на 2 400 скиллов | список |
| [wshobson/agents](https://github.com/wshobson/agents) | 40 663 | маркетплейс плагинов (из него startup-financial-modeling) | частично установлен |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 35 696 | каталог на 1 000+ скиллов | список |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | 32 396 | React, Next.js, веб-дизайн | не читан |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | 28 171 | 380 скиллов: инженерия, маркетинг, продукт, финансы | не читан |
| [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | 26 998 | продакт-менеджмент: job-stories, user-segmentation, customer-journey-map | читан выборочно, безопасен |

## По темам

| Тема | Репозиторий | ★ | Статус |
|---|---|---|---|
| Дизайн интерфейсов | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 135 704 | не читан |
| Дизайн, вкус | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | 95 927 | не читан |
| Слайды в вебе | [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides) | 30 639 | не читан |
| Схемы и диаграммы | [tt-a1i/archify](https://github.com/tt-a1i/archify) | 83 362 | не читан |
| Схемы и диаграммы | [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | 55 012 | читан, полезен для композиции схем |
| Схемы draw.io | [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill) | 10 129 | не читан |
| Тексты без следов ИИ | [blader/humanizer](https://github.com/blader/humanizer) | 56 785 | прочитан: чек-лист структурных паттернов, не установлен |
| Маркетинг, SEO, CRO | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | 54 666 | cold-email и social прочитаны, остальное не читано |
| Свежий ресерч по соцсетям | [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | 64 206 | метод пригоден; мастер настройки читает куки, скрипты не запускать |
| Академический ресерч | [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | 51 924 | не читан |
| Русский текст, письмо и редактура | [ilyautov/humanizer-ru](https://github.com/ilyautov/humanizer-ru) (449 ★, MIT), [IlyaChv/stop-slop-ru](https://github.com/IlyaChv/stop-slop-ru) (3 ★, MIT), [unicodef1wn/russian-writing-skills](https://github.com/unicodef1wn/russian-writing-skills) (MIT) | ниже порога | установлены по прямому выбору под русские тексты как `humanizer-ru`, `write-ru`, `editor-ru` |
| Структура мысли | [millwright-labs/minto-pyramid-skill](https://github.com/millwright-labs/minto-pyramid-skill) | ниже порога | установлен как `minto-pyramid` |
| Наука, медицина | [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 48 902 | частично установлен (market-research-reports) |
| Obsidian | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | 49 533 | не читан |
| Видео | [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) | 68 154 | не читан |
| Видео Remotion | [Vincentwei1021/video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) | 11 867 | не читан |
| Карта кода | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | 126 343 | не читан |
| Простота кода | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | 163 205 | не читан |
| Ревью кода | [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | 47 101 | не читан |
| Планы в файлах | [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) | 27 446 | не читан |
| Google Workspace | [googleworkspace/cli](https://github.com/googleworkspace/cli) | 31 485 | не читан |
| Проверка чужих скиллов | [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector) | 20 167 | сканер безопасности, не читан |
| Стандарт скиллов | [agentskills/agentskills](https://github.com/agentskills/agentskills) | 26 131 | спецификация |

## Пробелы (скиллов от 10 000 ★ не нашлось)

- Смета и ведомость объёмов работ по проектной документации (ГЭСН и подобные).
- Скилл для совместной правки таблицы (состояния сохранения, откат при ошибке) – брать принципы из frontend-design (anthropics) и frontend-ui-engineering (addyosmani).
- Pinterest и сбор референсов из закрытых соцсетей.
- Тренд-вотчинг: закрывается методом last30days плюс обычным веб-поиском.
- Выбор облака и оценка стоимости инференса.

## Не брать

- Скиллы для обхода антибот-защиты и скрытой автоматизации браузера.
- Харнессы и приложения целиком (dify, lobehub, ruflo и подобные): это не скиллы, а платформы.
- Скиллы, чей мастер настройки читает куки, токены или шлёт данные на чужие серверы.

## Вердикты

Формат: дата, задача, скилл, помог или нет, одной строкой. Новые записи дописывать в конец.

- Тексты без следов ИИ, blader/humanizer (56 785 ★, MIT): помог как чек-лист структурных паттернов («не X, а Y», одинокие строки-концовки, заход-разбег, тройки, пересказ известного) и фактический замок. Не установлен, выжимка живёт в проектных правилах письма.
- humanizer-ru (449 ★, MIT): установлен как редактор. Главный вывод: «удаляй, не дописывай» (просьба «добавь голос» ломает текст), фактический замок, сканер `scan.py` с чистотой «было/стало». Конфликт: скилл банит и «–»; если проект разрешает «–», правило проекта главнее.
- write-ru (stop-slop-ru, 3 ★, MIT): установлен как писатель с нуля. Помогли правило нуля, деятель и глагол, связки вместо рубленых фраз, ритм 15–25 слов. Россыпь цифр сам не ловит, это закрывается правилами проекта.
- cold-email и social (coreyhaines31/marketingskills, ~55 000 ★, MIT): помогли с заходом (хук, польза читателю, одна лёгкая просьба) и хуками для коротких видео. Не установлены, заточены под B2B-продажи на английском.
- pisma-infostyle (0 ★): схемы сопроводительного и холодного письма и правило честного пробела полезны, но тон даёт сухие тексты. Брать только схемы.
- Английский `humanize` не для русских текстов (цель обмануть детекторы, требует искусственной шероховатости). Русские тексты идут через `write-ru` и `humanizer-ru`.
- Тексты для людей из стройки: слепая проба пяти связок (судья в роли технадзора) показала, что слог чистят все, проваливается мысль. Итог: minto-pyramid (порядок мысли) → write-ru → editor-ru → слепой читатель, оформлено как `tekst-produkt`.
- Тренды и соцсети, last30days (64 206 ★, MIT): метод пригоден, скрипты не запускали. В паре с newsjacking из marketingskills закрыл роль тренд-вотчинга через обычный веб-поиск.
- LinkedIn, sergebulaev/linkedin-skills (4 771 ★, MIT, ниже порога, но крупнее под LinkedIn нет): linkedin-post-writer и linkedin-humanizer (аудит поднял посты с 79 до 94 из 100 и нашёл ошибки фактов), profile-optimizer и content-planner помогли. Публикацию через внешний сервис не подключали.
- the-fool (красная команда): стабильно полезен как последняя проверка стратегий и расчётов; независимый агент находил настоящие ошибки в допущениях и арифметике.
- Проверка проекта по проектной документации: invariants из quantity-surveyor (0 ★, MIT) пригодились как выжимка («не прочитано ≠ ноль», поставка и монтаж раздельно, уровни достоверности объёма). Работа с PDF: pdfplumber по координатам слов плюс линии ячеек дали таблицу в 1644 строки без потерь (anthropic pdf).
- Диаграммы и схемы, diagram-design (cathrynlavery, 55 012 ★): дал композицию схем; frontend-design (anthropics) задал порядок «план, проверка, сборка, самокритика» и отказ от шаблонных приёмов. Оба оказались сильнее общих «дизайн-вкусовых» скиллов в пробе.
- Продуктовая работа, phuryn/pm-skills (~27 000 ★): job-stories превратили сценарии «когда / хочу / чтобы» в имена тестов, user-segmentation отделил контексты от демографии, customer-journey-map дал скелет стадий и моментов истины. Не установлены.
- Инженерия, addyosmani test-driven-development: помог на денежных инвариантах, миграциях и гонках; ловил возврат прокрутки и перекрытие кнопок через тесты, а не на глаз.
- Структурированный разбор текста, regex-vs-llm-structured-text (affaan-m/ECC) и llm-evaluation (wshobson/agents): помогли разделить явные поля и сложную речь и собрать воспроизводимый базовый прогон.
- Браузерная приёмка, anthropics/webapp-testing и gstack qa / design-review: реальные нажатия и скриншоты выявляли дефекты, которых не видно по DOM (перекрытия, захват указателя, тесная раскладка при увеличенном тексте).
- Интерфейсы, свой apple-design: закрепился как основной для мобильных состояний, жестов, 44px, reduced motion и последовательного раскрытия. Он не разрешает менять действующий фирменный стиль проекта: смена дизайна без прямой просьбы запрещена.
- Объяснялки сложных тем, свой treatise + корень стиля проекта: помогли перенести фокус с пересказа школ на узнаваемую сцену; editor-ru дал независимую ревизию логики и категоричных утверждений; the-fool/evidence-audit проверил опору и границы вывода.
- Исследование референсов, awwwards-research: плоская редакция приёмов с источниками годится как вход для design-consultation; Pinterest и закрытые соцсети скиллами от 10 000 ★ не закрыты.

# Набор скиллов и рабочих правил для Claude Code и Codex

33 скилла и общие правила работы агента: анализ ниши TikTok с картой тем, русская редактура,
нейминг, разбор бизнеса, планирование тремя агентами, наглядные статьи, LinkedIn и другое.
Личных данных, клиентских материалов и ключей здесь нет: каждый подключает свои доступы.

## Установка одной фразой

Откройте Claude Code (терминал, приложение или claude.ai/code) и вставьте:

```text
Установи мне набор скиллов и рабочих правил из https://github.com/alexalexis6894-source/claude-skills.
Склонируй репозиторий во временную папку, прочитай README.md, CLAUDE.md и install.sh,
затем запусти `bash install.sh` (скиллы в ~/.claude/skills, правила в ~/.claude/CLAUDE.md,
мой прежний CLAUDE.md сохранится в .bak). Если у меня стоит Codex, установщик подключит и его.
После установки покажи список скиллов, кратко объясни, что каждый умеет, и спроси,
какую задачу я хочу решить первой. Если для анализа TikTok нужен APIFY_TOKEN,
дай прямую ссылку, где его взять, и куда его положить.
```

Обновление: та же фраза ещё раз, установщик заменит скиллы на свежие и обновит блок правил,
не трогая остальной текст вашего CLAUDE.md.

## Вариант для облака (claude.ai/code)

1. Нажмите **Use this template → Create a new repository** вверху этой страницы
   (или Fork). Получится ваша копия.
2. Откройте https://claude.ai/code и выберите свою копию как репозиторий сессии.
   Скиллы из `.claude/skills/` и правила из `CLAUDE.md` подхватятся сами, при старте
   облачной сессии хук ещё и поставит gstack (55 инженерных скиллов Гарри Тана).
3. Работайте прямо в этом репозитории: результаты (страницы, исследования) кладите в `site/`
   и `research/`.

## Вручную

```bash
git clone https://github.com/alexalexis6894-source/claude-skills.git
cd claude-skills
bash install.sh            # глобально для всех проектов
bash install.sh --project  # только в текущую папку проекта
bash install.sh --gstack   # плюс gstack
```

## Что внутри

| Задача | Скиллы |
|---|---|
| Анализ ниши и трендов TikTok, «что снимать» | `content-radar` |
| Сложная задача: подобрать инструменты и спланировать | `skill-scout`, `trio`, `the-fool` |
| Русские тексты без канцелярита и ИИ-штампов | `write-ru`, `editor-ru`, `humanizer-ru`, `minto-pyramid`, `tekst-produkt` |
| Английские тексты | `humanize`, `ai-check` |
| Наглядная статья-объяснение со сценами | `treatise`, `playground` |
| Нейминг и позиционирование | `naming`, `brand-naming`, `brand-naming-strategies`, `brand-positioning` |
| Разбор бизнеса, рынок, финмодель | `management-consulting`, `market-research-reports`, `startup-financial-modeling` |
| Дизайн и референсы | `apple-design`, `awwwards-research` |
| LinkedIn | `linkedin-marketing`, `linkedin-post-writer`, `linkedin-hook-extractor`, `linkedin-content-planner`, `linkedin-profile-optimizer`, `linkedin-humanizer`, `linkedin-interviewer` |
| Базы данных | `supabase`, `supabase-postgres-best-practices` |
| Прочее | `find-skills`, `i-have-adhd` |

Скилл вызывается сам по смыслу просьбы или явно: `/content-radar`, `/trio` и т. д.

## Анализ TikTok: что понадобится

- Аккаунт Apify и токен: https://console.apify.com/settings/integrations → **Personal API tokens**
  → скопировать. Положить в переменную окружения `APIFY_TOKEN` (в терминале `export APIFY_TOKEN=...`,
  в облаке claude.ai/code: название среды → Edit → Environment variables). В чат токен не присылать.
- Бесплатного кредита Apify ($5 в месяц) хватает примерно на два-три анализа ниши:
  типичный сбор стоит $1,5–2, потолок задаётся в каждом запуске.
- Результат: страница `site/<slug>/index.html` с таблицей всех тем ниши. Открыть локально
  (`python3 -m http.server` в папке `site`) или выложить на GitHub Pages / Netlify Drop.

## Правила работы (CLAUDE.md)

Установщик добавляет в ваш `~/.claude/CLAUDE.md` блок правил: агент сам доводит задачу до
проверенного результата, проверяет интерфейсы в браузере со скриншотами, при блокере даёт
готовое решение со ссылкой, большие задачи ведёт через `skill-scout` и параллельных субагентов,
отчёты делает веб-страницами, пишет по-русски без канцелярита. Блок между маркерами
`skills-kit:begin/end` можно править под себя.

## Лицензии

Собственные скиллы набора: MIT (см. `LICENSE`). Сторонние скиллы сохраняют свои лицензии,
источники и изменения перечислены в `THIRD_PARTY.md`.

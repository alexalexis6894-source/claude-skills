#!/bin/bash
# Ставит и обновляет gstack (github.com/garrytan/gstack) в облачной сессии: 55 скиллов
# Гарри Тана (/office-hours, /plan-ceo-review, /plan-eng-review, /review, /investigate…).
# Контейнер облака каждый раз новый, поэтому без хука gstack пропадал бы.
# Работает в фоне: скиллы появляются в сессии сами, как только setup закончит.
set -uo pipefail

[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0
# Браузер gstack (browse/dist/browse) запускает облачный Chromium по этой переменной
[ -n "${CLAUDE_ENV_FILE:-}" ] && echo 'export GSTACK_CHROMIUM_PATH=/opt/pw-browsers/chromium' >> "$CLAUDE_ENV_FILE"
echo '{"async": true, "asyncTimeout": 600000}'

GS="$HOME/.claude/skills/gstack"
LOG="$HOME/.claude/gstack-install.log"
mkdir -p "$HOME/.claude/skills"

{
  if [ -d "$GS/.git" ] && [ -d "$GS/bin" ]; then
    before=$(git -C "$GS" rev-parse HEAD)
    git -C "$GS" fetch -q --depth 1 origin && git -C "$GS" reset -q --hard FETCH_HEAD
    [ "$(git -C "$GS" rev-parse HEAD)" = "$before" ] && { echo "gstack актуален: $before"; exit 0; }
  else
    rm -rf "$GS"
    git clone -q --single-branch --depth 1 https://github.com/garrytan/gstack.git "$GS" || exit 0
  fi
  # Браузер gstack не качаем: в облаке уже есть Chromium (/opt/pw-browsers)
  cd "$GS" && ./setup --no-browser -q
  echo "gstack $(cat "$GS/VERSION" 2>/dev/null) установлен"
} >>"$LOG" 2>&1 || true
exit 0

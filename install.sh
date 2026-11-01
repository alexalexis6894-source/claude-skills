#!/usr/bin/env bash
# Ставит скиллы и рабочие правила из этого репозитория в Claude Code (и Codex) на этом компьютере.
#   ./install.sh            скиллы в ~/.claude/skills, правила в ~/.claude/CLAUDE.md
#   ./install.sh --project  то же в текущую папку проекта (./.claude/skills, ./CLAUDE.md)
#   ./install.sh --gstack   дополнительно поставить gstack (github.com/garrytan/gstack)
# Повторный запуск обновляет установленное. Чужие скиллы с другими именами не трогаются.
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
MODE=global; GSTACK=0
for a in "$@"; do case "$a" in --project) MODE=project;; --gstack) GSTACK=1;; esac; done

if [ "$MODE" = project ]; then DEST="$PWD/.claude"; RULES="$PWD/CLAUDE.md"; else DEST="$HOME/.claude"; RULES="$HOME/.claude/CLAUDE.md"; fi
mkdir -p "$DEST/skills"

n=0
for d in "$SRC"/.claude/skills/*/; do
  name=$(basename "$d")
  rm -rf "$DEST/skills/$name"
  cp -R "$d" "$DEST/skills/$name"
  n=$((n+1))
done
echo "Скиллы: $n шт. -> $DEST/skills"

# Правила: вставляем блок между маркерами, остальной текст файла сохраняем
BEGIN="<!-- skills-kit:begin -->"; END="<!-- skills-kit:end -->"
touch "$RULES"
[ -s "$RULES" ] && cp "$RULES" "$RULES.bak"
python3 - "$RULES" "$SRC/CLAUDE.md" "$BEGIN" "$END" <<'PY'
import sys, re, pathlib
dst, src, b, e = sys.argv[1:]
cur = pathlib.Path(dst).read_text(encoding="utf-8")
block = f"{b}\n{pathlib.Path(src).read_text(encoding='utf-8').strip()}\n{e}"
if b in cur and e in cur:
    cur = re.sub(re.escape(b) + r".*?" + re.escape(e), lambda m: block, cur, flags=re.S)
else:
    cur = (cur.rstrip() + "\n\n" if cur.strip() else "") + block + "\n"
pathlib.Path(dst).write_text(cur, encoding="utf-8")
PY
echo "Правила: $RULES (прежняя версия сохранена в .bak)"

# Codex читает ~/.codex/AGENTS.md и скиллы из ~/.codex/skills
if [ "$MODE" = global ] && command -v codex >/dev/null 2>&1; then
  mkdir -p "$HOME/.codex/skills"
  for d in "$SRC"/.claude/skills/*/; do name=$(basename "$d"); rm -rf "$HOME/.codex/skills/$name"; cp -R "$d" "$HOME/.codex/skills/$name"; done
  touch "$HOME/.codex/AGENTS.md"
  grep -q "skills-kit" "$HOME/.codex/AGENTS.md" || printf '\n<!-- skills-kit -->\nСледуй правилам из ~/.claude/CLAUDE.md (блок skills-kit).\n' >> "$HOME/.codex/AGENTS.md"
  echo "Codex: скиллы в ~/.codex/skills, ссылка на правила в ~/.codex/AGENTS.md"
fi

if [ "$GSTACK" = 1 ]; then
  GS="$HOME/.claude/skills/gstack"
  if [ -d "$GS/.git" ]; then git -C "$GS" pull -q; else git clone -q --depth 1 https://github.com/garrytan/gstack.git "$GS"; fi
  (cd "$GS" && ./setup) && echo "gstack установлен"
fi
echo "Готово. Перезапустите Claude Code, чтобы он увидел новые скиллы."

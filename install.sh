#!/usr/bin/env bash
# Ставит скиллы и рабочие правила из этого репозитория в Claude Code (и Codex) на этом компьютере.
#   ./install.sh            скиллы в ~/.claude/skills, правила в ~/.claude/CLAUDE.md (свой CLAUDE.md не перезаписывается)
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
  if [ -d "$DEST/skills/$name" ] && ! diff -rq "$d" "$DEST/skills/$name" >/dev/null 2>&1 && [ ! -f "$DEST/skills-kit/installed/$name" ]; then
    BK="$DEST/skills-backup-$(date +%Y%m%d-%H%M%S)"; mkdir -p "$BK"; mv "$DEST/skills/$name" "$BK/"
    echo "  ваш скилл $name с тем же именем сохранён в $BK/$name"
  fi
  rm -rf "$DEST/skills/$name"
  cp -R "$d" "$DEST/skills/$name"
  mkdir -p "$DEST/skills-kit/installed"; touch "$DEST/skills-kit/installed/$name"
  n=$((n+1))
done
echo "Скиллы: $n шт. -> $DEST/skills"

# Правила. Свой CLAUDE.md человека главнее и не перезаписывается:
#  - файла нет или он пустой: правила набора ставятся целиком;
#  - в файле только наш прежний блок: блок обновляется целиком;
#  - есть свой текст: файл не трогаем, эталон кладём в skills-kit/RULES.md,
#    а дописать только недостающее должен Claude по скиллу rules-merge (со сверкой субагентом).
BEGIN="<!-- skills-kit:begin -->"; END="<!-- skills-kit:end -->"
mkdir -p "$DEST/skills-kit"
cp "$SRC/CLAUDE.md" "$DEST/skills-kit/RULES.md"
touch "$RULES"
STATE=$(python3 - "$RULES" "$BEGIN" "$END" <<'PY2'
import sys, re, pathlib
t = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
b, e = sys.argv[2], sys.argv[3]
own = re.sub(re.escape(b) + r".*?" + re.escape(e), "", t, flags=re.S)
print("own" if own.strip() else ("ours" if b in t else "empty"))
PY2
)
if [ "$STATE" = own ]; then
  echo "Правила: у вас уже есть свой $RULES, он не изменён."
  echo "  Эталон правил набора: $DEST/skills-kit/RULES.md"
  echo "  NEEDS_MERGE: попросите Claude выполнить скилл rules-merge, он допишет только недостающее."
else
  [ -s "$RULES" ] && cp "$RULES" "$RULES.bak"
  { echo "$BEGIN"; cat "$SRC/CLAUDE.md"; echo "$END"; } > "$RULES"
  echo "Правила: своего CLAUDE.md не было, правила набора поставлены целиком в $RULES"
fi

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

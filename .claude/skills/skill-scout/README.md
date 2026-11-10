# Skill Scout

A skill for Claude Code (and Codex) that finds the best skills for your task before the work starts.

You describe a task. Skill Scout understands it, searches your own skills, plugins and popular
GitHub repositories (10,000+ stars), reads every candidate for safety, tries the contested ones
on a small slice of the task, and then the whole task runs through the winners.

## Install

Paste this into Claude Code:

```text
Install the skill-scout skill from
https://github.com/alexalexis6894-source/claude-skills/tree/main/.claude/skills/skill-scout
into ~/.claude/skills/skill-scout (SKILL.md, SKILL.ru.md and references/registry.md).
Read SKILL.md before installing and tell me what it does.
```

Or by hand:

```bash
git clone --depth 1 https://github.com/alexalexis6894-source/claude-skills.git
mkdir -p ~/.claude/skills
cp -R claude-skills/.claude/skills/skill-scout ~/.claude/skills/
```

For one project only, copy the folder into `<project>/.claude/skills/` instead.
In a cloud session (claude.ai/code) fork the repository and open the session on your fork:
skills from `.claude/skills/` are picked up automatically.

## Use

Type `/skill-scout` followed by the task, or just say "find skills for this task".
It also triggers by itself on complex work: a new feature, research, a design, a website, naming.

## How it works

1. **Task card.** The request, the expected result, the stages, search keywords.
2. **Scout.** One subagent reads the registry, your local skills and plugins, then searches GitHub.
3. **Threshold.** 10,000+ stars, updated within six months, a real `SKILL.md`, a permissive license.
4. **Safety.** Every candidate is read in full. Anything that asks for tokens, ships data out
   or installs through `curl | sh` is rejected.
5. **Trial.** Skills competing for one role each do the same small slice of the task in parallel.
6. **Work.** The lead picks 1 to 4 skills and the task runs only through them.
7. **Memory.** The verdict goes into `references/registry.md`, so the next scouting starts smarter.

## Files

- `SKILL.md`: the skill, in English.
- `SKILL.ru.md`: the Russian original.
- `references/registry.md`: a registry of vetted sources with star counts and verdicts (in Russian, the agent reads it fine).

MIT license. If it saved you time, a star on the repository helps other people find it.

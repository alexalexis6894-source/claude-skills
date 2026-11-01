# Third-party skills

The skills below are copies of open-source skills written by other people. Each keeps its
original license (a `LICENSE` file sits in the skill folder). All of them are MIT licensed.
The copies may lag behind the upstream repositories, so check the source for the latest version.

Licenses were checked against the upstream `LICENSE` files. "Local changes" lists what differs
from upstream apart from the added `LICENSE` file.

| Skill | Source | License | Local changes |
|---|---|---|---|
| `ai-check` | [harshaneel/humanize](https://github.com/harshaneel/humanize) (`plugins/humanize/skills/ai-check`) | MIT, Harshaneel Gokhale | None. `LICENSE` added. |
| `humanize` | [harshaneel/humanize](https://github.com/harshaneel/humanize) (`plugins/humanize/skills/humanize`) | MIT, Harshaneel Gokhale | `description` extended: proactive use for emails, slides and website copy, and a pointer to `humanizer-ru` and `write-ru` for Russian text. `LICENSE` added. |
| `humanizer-ru` | [ilyautov/humanizer-ru](https://github.com/ilyautov/humanizer-ru) (`skills/humanizer-ru`) | MIT, Ilya Utov | Source line and installation notes added at the top of `SKILL.md` (dash handling, venv setup for `scripts/scan.py`). Version 3.31.4, older than upstream. The `mcp` mode (`mcp_server.py`) is not included. |
| `write-ru` | [IlyaChv/stop-slop-ru](https://github.com/IlyaChv/stop-slop-ru) (`write-ru`) | MIT, Hardik Pandya (Stop Slop) and Ilya Chv | Source line and installation note added in `SKILL.md`. `evals/` and `README.md` not copied. The companion skill `stop-slop-ru` is not included, use `humanizer-ru` for checking someone else's text. |
| `editor-ru` | [unicodef1wn/russian-writing-skills](https://github.com/unicodef1wn/russian-writing-skills) (`editor-ru`) | MIT, Unicode (@unicodeunicode) | Source line added to `SKILL.md`. |
| `minto-pyramid` | [millwright-labs/minto-pyramid-skill](https://github.com/millwright-labs/minto-pyramid-skill) | MIT, Millwright Labs | Source line added to `SKILL.md`. `evals/` and `README.md` not copied. |
| `naming` | [glacierphonk/naming](https://github.com/glacierphonk/naming) | MIT, GlacierPhonk | None in `SKILL.md`. Repository files such as `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` and `open-source.md` are not copied, so the link to `open-source.md` inside `SKILL.md` is dead. |
| `brand-naming` | [arnabbagxd/Brand-building-skills](https://github.com/arnabbagxd/Brand-building-skills) (`skills/brand-naming`) | MIT | None. `LICENSE` added from the repository root. |
| `brand-positioning` | [arnabbagxd/Brand-building-skills](https://github.com/arnabbagxd/Brand-building-skills) (`skills/brand-positioning`) | MIT | None. `LICENSE` added from the repository root. |
| `brand-naming-strategies` | [mike-coulbourn/claude-vibes](https://github.com/mike-coulbourn/claude-vibes) (`plugins/vibes/skills/brand-naming-strategies`) | MIT, Mike Coulbourn | None. `LICENSE` added from the repository root. |
| `management-consulting` | [gcamilo/management-consulting](https://github.com/gcamilo/management-consulting) | MIT | `assets/` and `docs/` not copied. |
| `market-research-reports` | [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) (`skills/market-research-reports`) | MIT, K-Dense Inc. | `scripts/` (optional offline CLIs) not copied. `LICENSE` added from the repository root. |
| `startup-financial-modeling` | [wshobson/agents](https://github.com/wshobson/agents) (`plugins/startup-business-analyst/skills/startup-financial-modeling`) | MIT, Seth Hobson | None. `LICENSE` added from the repository root. |
| `the-fool` | [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) (`skills/the-fool`) | MIT | None. `LICENSE` added from the repository root. |
| `find-skills` | [vercel-labs/skills](https://github.com/vercel-labs/skills) (`skills/find-skills`) | MIT, Vercel, Inc. | None. Copy is an older upstream version. `LICENSE` added. |
| `supabase` | [supabase/agent-skills](https://github.com/supabase/agent-skills) (`skills/supabase`) | MIT, Supabase | None. Copy is an older upstream version (0.1.0); `references/` and `assets/` are not copied. `LICENSE` added. |
| `supabase-postgres-best-practices` | [supabase/agent-skills](https://github.com/supabase/agent-skills) (`skills/supabase-postgres-best-practices`) | MIT, Supabase | None. Copy is an older upstream version (1.1.1); `references/` is not copied. `LICENSE` added. |
| `linkedin-marketing` | [sergebulaev/linkedin-skills](https://github.com/sergebulaev/linkedin-skills) (root `SKILL.md` and `references/`) | MIT, Sergey Bulaev | Source line added. Publora tracking parameters removed from links. `lib/` (publishing layer) not copied. `references/voice-profile.md` replaced with an empty template to fill in. `references/precedence.md` (newer upstream file) not copied. |
| `linkedin-post-writer` | [sergebulaev/linkedin-skills](https://github.com/sergebulaev/linkedin-skills) (`skills/linkedin-post-writer`) | MIT, Sergey Bulaev | Source line added. Relative paths point to `../linkedin-marketing/references/`. |
| `linkedin-hook-extractor` | same | MIT, Sergey Bulaev | Source line added. Relative paths adjusted. |
| `linkedin-content-planner` | same | MIT, Sergey Bulaev | Source line added. Relative paths adjusted. |
| `linkedin-profile-optimizer` | same | MIT, Sergey Bulaev | Source line added. |
| `linkedin-humanizer` | same | MIT, Sergey Bulaev | Source line added. Relative paths adjusted. `scripts/` not copied. |
| `linkedin-interviewer` | same | MIT, Sergey Bulaev | Source line added. Relative paths adjusted. |

The `linkedin-*` skills share one license, kept in `linkedin-marketing/LICENSE`. Upstream also has
`linkedin-comment-drafter`, `linkedin-reply-handler`, `linkedin-repurposer`, `linkedin-thread-monitor`,
`linkedin-employee-advocacy` and `linkedin-engager-analytics`. They are not part of this kit, so mentions
of them inside the copied files point to skills you would need to install separately.

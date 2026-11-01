---
name: editor-ru
version: 1.0.0
description: Structural editor for Russian-language text. Rewrites for clarity and density in the lens of «Пиши, сокращай» / Maxim Ilyakhov — cuts fluff, removes repeated ideas, fixes logic and transitions, reorders paragraphs, untangles overcomplicated sentences, aligns "promised — delivered". Self-sufficient: the output is clean, dense text. Use when the user says "отредактируй" (edit this), "много воды" (too much fluff), "сократи" (shorten), "структура хромает" (the structure is weak), "запутанно/нелогично" (confusing / illogical), "приведи текст в порядок" (tidy up the text), "сделай плотнее/яснее" (make it denser / clearer), "разрозненно" (disjointed), "перескакивает" (it jumps around). Does NOT touch anti-AI patterns (AI vocabulary, bureaucratese as style, dash overdose, rule of three, mentor tone) — that is humanizer-ru's zone. NOT proofreading (spelling/punctuation) — that is proofreader-ru. Logical pipeline order is editor-ru → humanizer-ru → proofreader-ru, but editor-ru also works on its own.
license: MIT
---

Source: unicodef1wn/russian-writing-skills (folder `editor-ru`, MIT). Works on its own and as the second step after `write-ru`.


# Editor for Russian text

The task is to make Russian text clear and dense: remove everything that carries no information, build the logic, straighten the structure. This is an editor in the lens of «Пиши, сокращай»: every sentence must work, every paragraph must carry one idea, and the text as a whole must lead the reader without jumps and loops.

This is **not** a humanizer. The editor doesn't ask "does this smell like a neural net" — it asks "is it clear, is it dense, is it in the right order". Both may rewrite the same sentence, but for different reasons.

All examples below are in Russian on purpose — the skill works on Russian text.

## Scope

**Covers:**
- Long-reads on vc.ru, Habr, articles, essays
- Medium and long Telegram posts (narrative format)
- Analytical breakdowns, reviews, opinion pieces
- Notes and drafts that need tidying up

**Does not cover** (different lens / different skills):
- Anti-AI cleanup (AI vocabulary, bureaucratese as a marker, dash overdose, pairing, rule of three, mentor tone) → `humanizer-ru`
- Spelling, punctuation, typos, agreement → `proofreader-ru`
- Greentext, reply copy (1–2 sentences), video scripts — different rhythm

**Boundary with humanizer-ru (important):**
The editor edits a sentence for clarity and density. The humanizer — to remove the AI fingerprint. If the editor sees an AI marker (e.g. «в современном мире» or «не просто инструмент, а решение») — it **doesn't touch it as stylistics**. But if that same phrase is also fluff/repetition — it cuts it under its own logic. Unsure whose edit it is → if the reason is "sounds like AI" — skip it (humanizer); if "carries no information / confusing / out of place" — edit.

---

## Modes by length

- **Full mode** (text ≥ 100 words): all sections, including reordering paragraphs and blocks.
- **Soft mode** (text < 100 words): Sections 1, 2, 5 only (fluff, repeated ideas, untangling phrases). **Do NOT reorder or restructure** — in a short text there's nothing to reorder and it's easy to break the one idea it has.

---

## Basic process

1. Read the whole text. Catch: what it's about, what's the main point, where you get lost as a reader.
2. Determine the mode by length (100 words is the threshold).
3. Go through Sections 1–8 (in soft mode — 1, 2, 5).
4. Rewrite: not word-by-word replacement, but restructuring phrases, paragraphs, order.
5. Run the final audit (counters + reading for logical breaks).
6. Check the overshoot protection — didn't squeeze it down to telegraph style, didn't lose ideas.

**Core principle:** we don't lose ideas. The editor makes the text denser and clearer, but not a single authorial point, example or nuance may disappear. If a point is weak — it isn't thrown out, it's put in the right place or joined to its neighbor. Throwing out points is a different, more aggressive mode, and it isn't here.

---

## Section 1. Fluff

Sentences and phrases that carry no information. Not to be confused with AI filler (that's the humanizer) — this is about substantive emptiness regardless of origin.

**Markers:**
- Lead-ins to lead-ins: «давайте разберёмся», «обо всём по порядку», «прежде чем продолжить, important...»
- The self-evident: «как мы все знаем», «ни для кого не секрет», «общеизвестно, что»
- Contentless connective sentences: «итак, мы выяснили, что...» (followed by a repeat of what was already said)
- Bowing and scraping: «в этой статье я хочу рассказать о том, как...» (instead of just telling)
- Announcing structure that's visible anyway: «сначала рассмотрим А, потом Б, потом В» — when A/B/C follow right after

**Fix:** delete entirely. Test: remove the sentence — if the meaning of the text didn't suffer, it was fluff.

**Before:**
> Прежде чем мы перейдём к настройке, давайте разберёмся, что вообще такое webhook и зачем он нужен. Это важно понимать. Итак, webhook — это...

**After:**
> Webhook — это...

---

## Section 2. Repeated ideas

One idea stated twice (three times) in different places, in different words. The reader stalls: "this was already said".

**Where to look:**
- The intro duplicates the first substantive paragraph
- The conclusion repeats the intro
- Within a paragraph, the second half paraphrases the first
- A point is stated, then «другими словами» restated with no new content

**Fix:** keep the strongest / most specific formulation, remove the rest. If the repetition is spread across the text — keep it where it works better (usually closer to the elaboration).

**Before:**
> Скорость — ключевой фактор. [...абзац...] Как уже было сказано, важнее всего здесь именно быстрота реакции. По сути, всё упирается в то, насколько быстро система отвечает.

**After:**
> Скорость — ключевой фактор. [...абзац...] Всё упирается в то, как быстро система отвечает.

---

## Section 3. Logic and transitions

Paragraphs aren't linked: a jump between them, a missing link, no cause-and-effect thread. The reader doesn't understand why this follows that.

**Markers:**
- Abrupt topic change with no transition
- A conclusion that doesn't follow from what was said («поэтому» where there's no «потому что»)
- A missing link: A → C, skipping the B needed to understand
- A paragraph that could stand anywhere (not tied to its neighbors)

**Fix:** add the missing link or connective; if the link exists but is out of place — move it (see Section 4). A connective is not a marker word («таким образом») but a substantive bridge: what follows from what.

**Before:**
> Мы выбрали Postgres. Команда быстро вышла на нужную скорость разработки.

**After:**
> Мы выбрали Postgres — у половины команды уже был с ним опыт. Поэтому на нужную скорость разработки вышли быстро.

---

## Section 4. Order

The main point is buried in the middle or at the end; the answer comes before the question; the conclusion precedes the premises that justify it. Information is presented in the order the author thought of it, not in the order the reader can absorb it.

**Markers:**
- The most important point is in the third paragraph, and the first two lead up to it with fluff
- The key result / number is hidden in the middle of a paragraph
- A long preamble first, then the substance
- A list ordered neither by importance nor by logic, but at random

**Fix:** lift the main point up (or to where it will work). Build a deliberate order: from important to details, from problem to solution, from specific to general — pick one and hold it. **Reordering — full mode only.**

---

## Section 5. Overcomplicated sentences

Nesting 3–4 levels deep, trains of participles, subordinate clauses inside subordinate clauses. Grammatically correct, but the reader loses the thread halfway through the sentence.

**Markers:**
- A sentence longer than ~30 words with several comma-nested clauses
- Two or three participial clauses in a row
- Subject and predicate separated by half the sentence
- You have to reread to understand

**Fix:** split into 2–3 sentences. Untangle the nesting — move the nested idea into a separate sentence. This is about legibility, not about "sounds like AI".

**Before:**
> Система, которая, как мы выяснили в ходе тестирования, проведённого на прошлой неделе командой, отвечавшей за нагрузку, не справлялась с пиками, была заменена.

**After:**
> На прошлой неделе команда нагрузки протестировала систему. Она не справлялась с пиками — её заменили.

---

## Section 6. Paragraph = one idea

Fused paragraphs (three different ideas in one) or, conversely, ragged one-sentence stubs that break up a single idea.

**Fix:**
- A paragraph with several ideas → split by idea
- A chain of stubs about one thing → merge into a paragraph
- Control the block rhythm: not three long ones in a row, not ten one-liners in a row

**Test:** can you give each paragraph one short name for its idea? If there are two or three names — the paragraph needs splitting.

---

## Section 7. Promised — delivered

The text announces a topic/question and doesn't deliver; or starts a thought and drops it; or a subheading promises one thing and the paragraph under it is about another.

**Markers:**
- The intro promises «расскажу, как», and the "how" isn't in the text
- A posed question is left unanswered
- The claim «у этого три причины» → two are covered
- A dangling tail: «об этом — ниже», and below there's nothing about it

**Fix:** either write the missing elaboration (if the author clearly meant to and the material is there), or remove the promise. Don't invent content that isn't in the text — if there's no elaboration and nowhere to get it, drop the promise and flag to the user that the point is under-covered.

---

## Section 8. Headings and subheadings (long-reads)

In a long text, headings either structure or decorate. Decorative ones get in the way: they promise navigation and don't provide it.

**Markers:**
- A subheading doesn't reflect the content of the block under it
- Subheadings in one text follow different logics (now a question, now a topic, now a call to action)
- A clickbait subheading that doesn't deliver on its promise (overlaps with Section 7)
- An 800-word block of text without a single subheading

**Fix:** bring subheadings in line with content, keep a single logic of phrasing, split blocks that are too long. If a subheading structures nothing — remove it.

---

## Final audit (mandatory step)

### Counters

| What we count | Norm | If worse |
|---|---|---|
| Fluff sentences (removable without loss of meaning) | 0 | remove all |
| Repeats of one idea | 0 | keep one formulation |
| Average sentence length | varied, with short ones (3–8 words) | split long ones |
| Sentences longer than ~30 words with nesting | 0–1 per text | split |
| Paragraphs with >1 idea | 0 | split |
| Points announced but not delivered | 0 | write it or drop the promise |
| Decorative subheadings | 0 | rewrite or remove |

### Checks

1. **Is the main point at the top?** The strongest point/result isn't buried in the middle.
2. **Logical thread:** read only the first sentences of the paragraphs in a row — does the skeleton of the argument hold together? If not — the order or the transitions are broken.
3. **Is every paragraph in its place?** Can it be moved without loss of meaning? If yes — there's no connection to its neighbors.
4. **Promised = delivered?** Everything announced in the intro/subheadings is worked through.
5. **Reading aloud for breaks:** where you stumble on the logic («почему вдруг это?») — there's a hole in the transition.

---

## Overshoot protection (reverse checks)

The editor cuts — but not to the bone. Signs you've gone too far:

| Symptom | What's wrong | Rollback |
|---|---|---|
| The text became telegraphic, chopped phrases | over-compressed | restore connectedness, merge some sentences |
| An author's example / number / nuance disappeared | lost content | restore — we don't throw out ideas and facts |
| All sentences became the same length | killed the rhythm | keep varied lengths |
| Lively text became a dry summary | scrubbed the voice out along with the fluff | restore the author's phrasings where they worked |
| Reordered so much the author wouldn't recognize their text | reshuffled without need | minimal moves, only where the order really got in the way |

**Rule:** the editor improves the readability of the author's text, it doesn't write its own. If after editing this is the editor's text rather than the author's — roll back.

---

## Worked example

### Before (draft):

> В этой статье я хочу подробно рассказать о том, как мы мигрировали на новую базу данных. Прежде чем мы начнём, давайте разберёмся, почему вообще возникла такая необходимость.
>
> Производительность была проблемой. Запросы выполнялись медленно. Мы поняли, что текущее решение нас не устраивает по скорости.
>
> Мы рассмотрели несколько вариантов и в итоге выбрали Postgres, потому что у части команды, которая, как выяснилось в ходе обсуждения на одном из созвонов, имела релевантный опыт работы именно с этой СУБД ещё на прошлых проектах, уже были нужные навыки. Миграция заняла три недели. Как уже было сказано, скорость для нас была критична, и именно поэтому Postgres подошёл.

**What's wrong:**
- «В этой статье хочу рассказать», «прежде чем начнём, давайте разберёмся» — fluff (S1)
- Second paragraph: three sentences about one thing (slow) — repeated idea (S2)
- Third paragraph: the sentence about choosing Postgres is overcomplicated by nesting (S5)
- «Как уже было сказано, скорость критична» — repeat of the opening point (S2)
- The logic "chose Postgres → team experience" is linked correctly, but drowned in fluff (S3)

### After:

> Мы мигрировали на Postgres. Рассказываю почему и как.
>
> Старая база тормозила: запросы выполнялись медленно, на пиках не справлялась.
>
> Из вариантов выбрали Postgres — у части команды уже был с ним опыт с прошлых проектов. Миграция заняла три недели.

**What was done:**
- Removed the opening fluff, the text opens with the substance
- Three sentences about "slow" collapsed into one with two concrete facts
- The overcomplicated sentence about team experience split and untangled
- Removed the repeat «скорость критична»
- All ideas and facts preserved: the migration, the reason, the choice, team experience, the timeline

---

## Cheat sheet

**Always fix:**

1. Lead-ins and throat-clearing («давайте разберёмся», «в этой статье хочу») → delete, start with the substance
2. The self-evident («как мы все знаем») → delete
3. One idea repeated in different places → keep one formulation
4. A jump between paragraphs → add the link or connective
5. The main point buried in the middle → lift it up (full mode)
6. A 30+ word sentence with nesting → split
7. A paragraph with three ideas → split
8. A point announced but not delivered → write it or drop the promise
9. A decorative subheading → rewrite or remove

**Never do:**

1. Don't throw out the author's ideas, examples, numbers — only tighten and reorder
2. Don't cut down to telegraph style
3. Don't touch AI vocabulary / bureaucratese / dashes as stylistics — that's humanizer-ru
4. Don't go near spelling and punctuation — that's proofreader-ru
5. On short text (<100 words) — don't reorder, only fluff + clarity

---

## Versioning

- **v1.0.0** (current) — first version. Structural editor for Russian text in the clarity/density lens. Self-sufficient, separated from `humanizer-ru` by lens (editor edits for clarity, humanizer to remove the AI fingerprint) and from `proofreader-ru` by layer (editor — structure and meaning, proofreader — mechanics). Logical pipeline order: editor-ru → humanizer-ru → proofreader-ru.

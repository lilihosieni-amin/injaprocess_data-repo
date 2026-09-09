---
name: edit-fact
description: Apply a direct conversational edit to the quantitative facts store with NO voice/transcript — resolve the target entry, classify the instruction as an addition, a change or a retirement, write the delta or the patch, preview it, run the matching merge facts verb (the sole writer), and commit with source.type "chat". Mirrors edit-process for facts (design §13, v3.7 §5).
---

# edit-fact playbook

**Invocation:** the user, in chat, instructs a targeted edit of the quantitative facts store with
**no recording processed** — e.g. «پارمسان الان ۱۰۰ گرمه», «این دو تا قانون یکی هستن», «F-00042 رو
بازنشسته کن», «واحد جدید: حلب».

This reuses the **entire `merge facts` op set** built for the `quantify` pipeline (design §12/§13,
v3.7 §5) and the same `quantify` agent, in its **`targeted`** mode — for everything the bot has to
compose. A change whose value the owner named is written by this playbook itself, as a patch
`merge facts edit` applies. It **never writes `facts/*.json` directly** — every change goes through
`merge facts …` (the sole writer, guard-enforced), so INV-1 still holds. The only differences from a `quantify` pipeline run are the input (a chat instruction,
not the estate/transcripts) and the absence of Gate M / Gate A / Stage 1–2 (a targeted edit needs
none of the estate-wide resolution).

All paths are relative to `<data-repo>` (`DATA_ROOT`). Every engine CLI runs with
`DATA_ROOT=<data-repo>` set; every `validate` call additionally carries
`SCHEMA_DIR=<code-repo>/schemas`. The `quantify` agent's `schema_path`/`data_root` inputs need the
same two roots — see Step 3.

## Step 1 — Resolve the entry (read-only)

1. Resolve the target entry from the instruction, against `facts/.index.json`:
   - an id matching `^F-[0-9]{5}$`, matched directly;
   - else an exact `key` match;
   - else a Persian title/alias search (`title`, `aliases`) over the index.
   Restrict candidates to **open** entries (`retired: false`) unless the instruction names a
   retired id explicitly — a retired entry is edited only by naming its id directly (e.g. to
   correct its heir), never found by title search.
2. **Ambiguity → ask in Persian**, listing every candidate by id, kind, title and scope, and wait
   for the user to pick one — never guess (mirrors `edit-process` Step 1's "list candidate
   processes by name and id").
3. **No candidate, and the instruction reads as introducing a fact from scratch** (a new item,
   record, rule or note nothing in the store yet names — e.g. «واحد جدید: حلب») — there is nothing
   to load. Continue with no entry; Step 3 dispatches `quantify` without one, and its targeted-mode
   contract covers exactly this case ("a single new entry the instruction describes from
   scratch").
4. **No candidate, and the instruction reads as referring to something that should already
   exist** — ask the user in Persian rather than guessing; do not fabricate a from-scratch entry
   the instruction did not actually ask for.
5. **Exactly one candidate** (or one named directly) — read its **full envelope** from the matching
   store file, by the index row's `kind`: `item` → `facts/items.json`, `record` →
   `facts/records.json`, `measurement` → `facts/measurements.json`, `rule` → `facts/rules.json`,
   `note` → `facts/notes.json`. You will pass this envelope to `quantify` verbatim, or read the
   path you are about to patch out of it (INV-1: never invent or edit a field yourself).
6. **Several entries.** An instruction may name a set rather than one entry — «در شرح ۱۰ ثبت …»,
   «همهٔ قاعده‌های آشپزخانه که …». Resolve it to a **list** of entries, read each one's envelope,
   and run everything below **once per entry, each in its own run directory, in order**. An entry
   that fails does not stop the others; Step 6's report names every one of them, and says which
   failed and why. Step 4's one question, where the case needs one, is still **one** message for
   the whole set: preview every entry first, ask once, then write.

## Step 2 — Create the run directory and its initial `meta.json`

1. `{run_dir} = runs/facts/{dept}/{stamp}/`, `{stamp}` a UTC `YYYYMMDD-HHMMSS` — one fresh run
   directory per **entry** the instruction touches (never reused across instructions or entries,
   and never shared with a pipeline run's own `{run_dir}`).
2. **`{dept}` rule:** the first department in the resolved entry's (canonical) `scope.departments`,
   or `management` when `scope.departments` is empty (a universal entry) — mirroring QF-43's own
   bootstrap convention that a scope-free write is `management`'s. For a from-scratch instruction
   (Step 1.3, no entry loaded), use the department the user names in the instruction, or
   `management` if none is named or implied.
3. Write the initial `{run_dir}/meta.json`, mirroring the `quantify` playbook's own Stage 0 fresh-run
   shape but with `origin: "chat"` and the instruction recorded verbatim:
   ```json
   {
     "department": "<dept>",
     "origin": "chat",
     "actor": "<the Telegram user who invoked this run>",
     "started_at": "<ISO-8601 Z, now>",
     "finished_at": null,
     "recordings": [],
     "attachments": [],
     "workbooks": [],
     "delta": "",
     "merged": false,
     "ids_created": [],
     "instruction": "<the user's instruction, verbatim, in Persian>"
   }
   ```
   `recordings`/`attachments`/`workbooks` stay `[]` — edit-fact reads no estate, no attachments, no
   recordings.
4. Validate: `Bash: DATA_ROOT=<data-repo> SCHEMA_DIR=<code-repo>/schemas validate facts-run-meta {run_dir}/meta.json`.
   Fix the offending field (named in stderr) and re-validate on failure.

## Step 3 — Classify the instruction, then write the change

Three cases, decided from the instruction and the entry Step 1 loaded:

| the instruction … | vehicle | who writes it |
|---|---|---|
| **adds** — a new entry from scratch, a dated successor (QF-35), a fill of a `null`/absent leaf, a new source, account or alias | `{run_dir}/facts-delta.json` → `merge facts apply` | the `quantify` agent, targeted mode, delta form |
| **changes or removes what an existing entry says, and names the value** — a word, a sentence, a number, a member to drop, a department to add | `{run_dir}/facts-patch.json` → `merge facts edit` | **this playbook**, with no dispatch — the value is the owner's, there is nothing to compose |
| **changes what an existing entry says and the text has to be composed** — a statement to reword, a title to invent | `{run_dir}/facts-patch.json` → `merge facts edit` | the `quantify` agent, targeted mode, patch form |
| **retires or merges** | `merge facts retire [--heir]` | — |

A change to a field that already holds a value is an **`edit`**, never an `apply`: the write ladder
cannot rewrite a filled leaf, and an `apply` that tries only opens a disagreement — which is how the
owner's ten-statement correction was silently dropped once already.

### The patch — `{run_dir}/facts-patch.json`

```json
{"schema_version": 1,
 "ops": [{"op": "set",    "path": "statement",               "value": "برگهٔ روزانهٔ …"},
         {"op": "set",    "path": "data/outputs/vazn/value", "value": 285},
         {"op": "set",    "path": "scope/departments",       "value": ["cooking", "warehouse"]},
         {"op": "remove", "path": "data/applies_to/pitza__s0__j__r6"},
         {"op": "unset",  "path": "data/pack"},
         {"op": "append", "path": "aliases",                 "value": "برگه روزانه"}]}
```

A `path` is `/`-separated; a segment into a list names a member by its `key`, and an `accounts[]`
member by its `id`. `ops` apply in order, each seeing the one before it. `set` writes the value at
the path, replacing whatever is there — a scalar, an object, a list, a whole list member (whose
`key` it may not change). `remove` drops a list member and `unset` a dict key; either on a path
that does not exist is a **refusal**, not a no-op — nothing to remove means the instruction was
wrong. `append` adds to a list, and refuses a keyed member already present (that one is a `set`).
No path begins with `id`, `kind`, `key`, `status` or `updated_at`, and no op reaches under `source`
— provenance is never edited out.

**Writing a mechanical change yourself** (case 2) is one `set` per field the owner named, carrying
their exact value; a member they asked to drop is one `remove`; «هم‌چنین …» is an `append`. Read
the current value out of Step 1's envelope so the path is one that exists. The style card below is
still the law — the same lint runs at the verb's gate, whoever wrote the sentence.

### The dispatch (cases 1 and 3)

```
Task: quantify
  mode: targeted
  form: <delta for case 1, patch for case 3>
  instruction: <the user's instruction, verbatim>
  entry: <Step 1's loaded envelope — omit this key entirely for a from-scratch instruction>
  run_dir: {run_dir}
  facts_index: facts/.index.json
  schema_path: <code-repo>/schemas/facts-delta.schema.json — for the patch form, facts-patch.schema.json instead
  data_root: <data-repo>
```

Wait for it to complete. It writes the one file the form names — `{run_dir}/facts-delta.json` (one
entry touching the resolved entry: a revise-shaped update, a dated successor with `supersedes`, or a
from-scratch new entry) or `{run_dir}/facts-patch.json` (ops over the loaded entry only) — and a
one-paragraph Persian summary (counts per kind, every `unknown`/`disputed` field, every stub, every
supersession named by id). For a merge instruction, the **second** entry (the merge partner) is one
`facts_index` already lets the agent find on its own (QF-34's reuse map — it is *given* the index
precisely so it can locate a merge target, an existing unit, or any other reference the instruction
needs without `edit-fact` pre-resolving a second entry); which of the two is the heir and which is
superseded is named in the delta and/or the Persian summary — **keep this summary**, Step 4 and
Step 6 both read it.

## The style card (design §5.2)

A targeted edit writes prose into the store exactly as a pipeline unit does, and the same lint
refuses it — so the same card applies, whether the agent wrote the sentence or you did. A failing
sentence surfaces at `validate facts-delta` for an addition, and at `--preview` for a patch.

- **`title`** — a noun phrase naming the concept, at most 60 characters, Persian, no file, tab or
  cell name, no Latin except an item code.
- **`statement`** — one to three sentences in the register of a written procedure: what is measured
  or computed, in what unit, by whom, when. Never an A1 address, a column letter, a tab, file or
  `Table_*` name, formula text, a function name, a schema field name, the pipeline's own words
  («پاس», «اسکلت», «بخش از داده‌ها», «واحد کاری», «بچ», `original`, `bindings`, `FEEL`, `account`,
  `expr`), a quotation, «گفته شد» or «گوینده». «ستون», «تب» and «سلول» are allowed only in a
  record's own `statement` and in a field's `description`.
- The lint also covers `aliases[]`, `fields[].description`, `grain`, `method`, `exceptions`,
  `tracked[].reason` and any `issues[].description` the agent wrote, and it refuses any Latin token
  of four letters or more except `csv`, `Excel`, `sheet`, a unit symbol and an item code.

The instruction the owner typed is **not** the statement. «پارمسان الان ۱۰۰ گرمه» becomes «بستهٔ
پنیر پارمسان ۱۰۰ گرم است», not a quotation of what was said.

## Step 4 — Preview, and ask only where the owner has not already decided

For a patch (cases 2 and 3), run the verb in preview first. It writes nothing:

```
Bash: DATA_ROOT=<data-repo> merge facts edit --id F-… --patch {run_dir}/facts-patch.json --run {run_dir} --preview
```

It prints one block per op — the op, «فعلی» (the value as the store holds it now) and «پیشنهاد»
(what the op would write) — then `OK`, or the refusal lines and a non-zero exit. **Keep that
output**: it is INV-5's field-by-field view, built without reading the store file yourself, and
Step 6's report is made of it.

Then gate, in this order:

- **No question** for a mechanical change (case 2) or an addition (case 1). The instruction named
  the target and the exact value, and that **is** INV-5's approval (owner ruling, 2026-09-09). Go
  straight to Step 5.
- **One question**, the preview shown in full, for prose you composed (case 3), for any `remove`,
  and for a retirement or a merge. **One message for the whole instruction**, however many entries
  it touches — never one question per field, and never one per entry. Wait for an explicit
  «تأیید». **If declined, write nothing at all** — do not "prepare it anyway."

For composed prose or a removal, the preview goes to the owner as the command printed it — those
are their own values:

```
تغییرهای زیر انجام می‌شود:

{the preview output of every entry, exactly as printed}

تأیید می‌کنید؟
```

For a retirement, the one-liner as before:

```
{id} «{title}» بازنشسته می‌شود. تأیید می‌کنید؟
```

or, with a heir:

```
{retired-id} «{retired-title}» بازنشسته می‌شود؛ وارث آن {heir-id} «{heir-title}» خواهد بود. تأیید می‌کنید؟
```

**A preview that exits non-zero** is a wrong instruction or a badly composed sentence, and nothing
was written:

- case 3 — re-dispatch `quantify` **once**, the refusal appended to the instruction, then preview
  again; if it refuses a second time, report it and stop;
- case 2 — tell the owner in Persian what the gate refused, and stop. Do not repair the value
  yourself; the value was theirs.

## Step 5 — Write, one verb per run directory

1. For an addition, validate the delta first:
   `Bash: DATA_ROOT=<data-repo> SCHEMA_DIR=<code-repo>/schemas validate facts-delta {run_dir}/facts-delta.json`.
   On non-zero exit, re-dispatch `quantify` (mode `targeted`, same inputs) with the stderr error
   appended, then re-validate. **After 2 failed attempts, STOP and report the delta path to the
   user in Persian** instead of looping — mirroring `quantify`/`process-voice`'s own `classify`
   bound. A patch needs no separate validation call: `--preview` has already run every check the
   write runs.
2. Run **exactly the verb the classification calls for**:

   | Situation | Verb |
   |---|---|
   | A change or a removal in an entry that already exists (cases 2 and 3) | `Bash: DATA_ROOT=<data-repo> merge facts edit --id F-… --patch {run_dir}/facts-patch.json --run {run_dir}` |
   | A field fill, a new source/account/item, a from-scratch new entry, a dated successor (case 1) | `Bash: DATA_ROOT=<data-repo> merge facts apply --delta {run_dir}/facts-delta.json --run {run_dir}` |
   | Settling an already-recorded disputed account the owner named by id | `Bash: DATA_ROOT=<data-repo> merge facts resolve --id F-… --field <path> --account <id> --run {run_dir}` |
   | Retiring an entry, with or without a heir | `Bash: DATA_ROOT=<data-repo> merge facts retire --id F-… [--heir F-…] --run {run_dir}` |
   | Promoting a `note` to another kind | `Bash: DATA_ROOT=<data-repo> merge facts promote --id F-… --kind <kind> [--key <key>] --run {run_dir}` |

   **No `resolve` ever follows an `edit`.** The verb settles the disagreement on every path it sets
   by itself — the account matching the new value becomes the chosen one, the rest are rejected —
   and it records the entry as confirmed by the chat actor. There is nothing left to do in the
   panel afterwards.
3. **Each verb gets THIS run's directory, and it is theirs alone.** `apply`'s own
   `{run_dir}/facts-delta.json` is the applied delta itself (a dict); `edit`, `resolve`, `retire`
   and `promote` each *append* `{"verb": …, "args": …}` to `{run_dir}/facts-delta.json` as a
   growing **list** — pointed at a directory `apply` already wrote into, that append crashes, and
   pointed at a directory a *different* `apply` call already used, a second `apply` silently
   overwrites the first's provenance (QF-7). So:
   - **One entry, one verb** — the common case, every mechanical change included: use `{run_dir}`
     for it and stop.
   - **Several entries** (Step 1.6) — each entry gets its own stamped
     `runs/facts/{dept}/{stamp}/`, minted in turn, one verb in each.
   - **Two verbs for one entry** — a merge whose heir also needs `apply`-only content from the
     retired entry — run the first verb against `{run_dir}`, then **mint a second stamped**
     `{run_dir2} = runs/facts/{dept}/{stamp2}/` for the second, and say so plainly in the Step 6
     report (which command ran against which directory).
4. A non-zero exit from any of these is a **precondition failure with nothing written** for that
   call — report the stderr message in Persian and stop that entry; do not re-dispatch `quantify`
   for a verb-only failure (the patch already passed `--preview`, the delta already passed
   `validate`; a remaining failure needs a human decision). With several entries, the others still
   run.

## Step 6 — Commit and report

1. Commit with the allowlist — never `git add -A`:
   ```
   Bash: git -C <data-repo> add departments runs facts attachments && \
         git -C <data-repo> commit -m "edit-fact({id}): <one-line Persian/English summary of the change>"
   ```
2. If any `merge` command run in Step 5 printed lines prefixed `facts:` — the read-only lookup
   `merge remove`/`merge restructure` print when a tombstoned **process** is referenced by a fact
   (QF-8, "Reporting a tombstone", item 1) — relay them in the Persian report exactly as
   `process-voice` Stage 9 and `edit-process` Step 6 do; `edit-fact`'s own verbs do not print these,
   so this is normally a no-op here.
3. Reply in Persian with what changed. Per entry: the preview's own «فعلی» and «پیشنهاد» lines,
   the id, and the field or lifecycle change; for a destructive op, that the original was retired
   (not deleted) and its heir, if any. With several entries (Step 1.6), one line each, and the
   ones that failed named with the reason. Name every run directory a command in Step 5 actually
   used. Do not paste the full entry JSON back.
4. End the report with **«در پنل تأییدشده است»** whenever the entry came out confirmed. `merge
   facts edit` always confirms the entry it wrote as the chat actor's, and this run's other verbs
   do too — `meta.json` says `origin: "chat"`. The sentence is what tells the owner there is
   nothing left for them to accept in the panel.

## Usage examples

The spec's four (§13, verbatim):

- «پارمسان الان ۱۰۰ گرمه» — a dated change (QF-35): resolve the `pack.size`-bearing item, dispatch
  `quantify`, receive a successor entry with `supersedes` and a newer `valid_from` → case 1, no
  question → `merge facts apply`.
- «این دو تا قانون یکی هستن» — resolve the entry the instruction names most directly; `quantify`
  locates the other via `facts_index` and returns which is the heir → one question (the retire
  confirmation, with heir) → `merge facts retire --id … --heir … --run {run_dir}`.
- «F-00042 رو بازنشسته کن» — resolve `F-00042` directly (no ambiguity) → one question (the retire
  confirmation, no heir) → `merge facts retire --id F-00042 --run {run_dir}`.
- «واحد جدید: حلب» — Step 1.3, no entry to load → `quantify` writes a from-scratch entry (temp id
  `T-1`) → case 1, no question → `merge facts apply`.

And the two the patch verb was built for:

- «در شرح این ثبت به‌جای «سیاهه» بنویس «برگه»» — the owner names the target and the exact word:
  case 2. This playbook writes a one-op patch setting `statement` to the sentence with the word
  replaced → `--preview` → no question → `merge facts edit`, and the report ends with
  «در پنل تأییدشده است».
- «در شرح ۱۰ ثبت آشپزخانه «سیاهه» را «برگه» کن» — Step 1.6: ten entries, ten run directories, the
  same one-op patch in each, in order. An entry whose gate refuses is reported and the rest carry
  on.

## Invariants

- **`merge facts …` is the sole writer of `facts/**`** — never edit `facts/*.json` (or
  `facts/.index.json`, which `merge` rebuilds on every write) directly; guard-enforced (INV-1).
- **IDs only from `allocate-id`, invoked exclusively by `merge facts apply`.** The delta's new
  entries carry temp ids (`T-1`, …) only; copy the resolved entry's real `F-…` id verbatim where a
  delta or a `--id` references it; never write a real-looking id yourself. A patch never mints
  anything: it names paths in an entry that already exists.
- **INV-3** — no fabrication: you never invent a value. The `quantify` agent models only what the
  instruction and the loaded entry/index actually support, and you do not write `facts-delta.json`
  content yourself. The one thing you may write is a patch whose every value the owner named —
  their word, their number, their member — over paths that already exist in the loaded entry.
- **INV-5** — a filled field is never overwritten without the owner's approval, and **an
  instruction that names the target and the exact value is that approval** (owner ruling,
  2026-09-09): no question is asked for a mechanical change or an addition. What still needs an
  explicit «تأیید» is prose you composed, a removal, and a retirement or merge — one question, the
  preview shown in full (Step 4). The engine cannot tell the two apart; you are the gate.
- **INV-4** — never delete: a retirement is `retire` (`retired: true`, tombstone-equivalent), never
  a hard delete; a merge is `retire --heir`, never removal of the losing entry.
- **Run-directory hygiene (Step 5.3)** — one fresh directory per entry; `apply` never shares one
  with `edit`/`resolve`/`retire`/`promote` or with a different `apply` call; a second verb call an
  entry needs gets its own second stamped directory.
- **Provenance** — the resulting change is `source.type: "chat"` (set by the delta or the verb,
  never by you) and `meta.json`'s `origin: "chat"`; `merge facts edit` unions that source itself
  and records the entry as the chat actor's, which is why nothing is left pending in the panel;
  Claude commits it.

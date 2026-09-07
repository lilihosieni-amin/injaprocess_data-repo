---
name: edit-fact
description: Apply a direct conversational edit to the quantitative facts store with NO voice/transcript — resolve the target entry, dispatch the quantify agent in targeted mode, confirm destructive/overwrite ops, run the matching merge facts verb (the sole writer), and commit with source.type "chat". Mirrors edit-process for facts (design §13).
---

# edit-fact playbook

**Invocation:** the user, in chat, instructs a targeted edit of the quantitative facts store with
**no recording processed** — e.g. «پارمسان الان ۱۰۰ گرمه», «این دو تا قانون یکی هستن», «F-00042 رو
بازنشسته کن», «واحد جدید: حلب».

This reuses the **entire `merge facts` op set** built for the `quantify` pipeline (design §12/§13)
and the same `quantify` agent, in its **`targeted`** mode. It **never writes `facts/*.json`
directly** — every change goes through `merge facts …` (the sole writer, guard-enforced), so INV-1
still holds. The only differences from a `quantify` pipeline run are the input (a chat instruction,
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
   `note` → `facts/notes.json`. You will pass this envelope to `quantify` verbatim (INV-1: never
   invent or edit a field yourself before the agent sees it).

## Step 2 — Create the run directory and its initial `meta.json`

1. `{run_dir} = runs/facts/{dept}/{stamp}/`, `{stamp}` a UTC `YYYYMMDD-HHMMSS` — one fresh run
   directory per **instruction** (never reused across instructions, and never shared with a
   pipeline run's own `{run_dir}`).
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

## Step 3 — Dispatch `Task: quantify` (targeted mode)

```
Task: quantify
  mode: targeted
  instruction: <the user's instruction, verbatim>
  entry: <Step 1's loaded envelope — omit this key entirely for a from-scratch instruction>
  run_dir: {run_dir}
  facts_index: facts/.index.json
  schema_path: <code-repo>/schemas/facts-delta.schema.json
  data_root: <data-repo>
```

Wait for it to complete. It writes `{run_dir}/facts-delta.json` — one entry touching the resolved
entry (a revise-shaped update, a dated successor with `supersedes`, or a from-scratch new entry) —
and a one-paragraph Persian summary (counts per kind, every `unknown`/`disputed` field, every stub,
every supersession named by id). For a merge instruction, the **second** entry (the merge partner)
is one `facts_index` already lets the agent find on its own (QF-34's reuse map — it is *given* the
index precisely so it can locate a merge target, an existing unit, or any other reference the
instruction needs without `edit-fact` pre-resolving a second entry); which of the two is the heir
and which is superseded is named in the delta and/or the Persian summary — **keep this summary**,
Step 4 and Step 6 both read it.

## The style card (design §5.2)

A targeted edit writes prose into the store exactly as a pipeline unit does, and the same lint
refuses it — so the same card applies, and `validate facts-delta` is where a failing sentence
surfaces.

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

## Step 4 — Gate the destructive and overwrite cases

Before touching the store, classify what the delta (and the instruction) actually do, and gate in
this order. **A plain fill (a field that was `null`/absent), a plain addition (a new source,
account, item, or a wholly new entry), or a dated successor (QF-35 — a legitimate change carrying a
newer `valid_from`) needs no gate at all** — proceed straight to Step 5.

**A. Retiring or merging (destructive).** The instruction retires the resolved entry, or declares
two entries the same referent (a merge — one becomes the heir, the other is retired with
`superseded_by` pointing at it). One-line Persian confirmation, mirroring the tombstone/restructure
gate `edit-process` Step 3 gives its own destructive ops:

```
{id} «{title}» بازنشسته می‌شود. تأیید می‌کنید؟
```

or, with a heir:

```
{retired-id} «{retired-title}» بازنشسته می‌شود؛ وارث آن {heir-id} «{heir-title}» خواهد بود. تأیید می‌کنید؟
```

Wait for an explicit «تأیید». **If declined, write nothing at all** — do not "prepare it anyway."

**B. Overwriting a filled field.** The `quantify` write ladder (§11) never silently overwrites a
scalar field that already holds a value — a differing value becomes a disputed `accounts[]` entry
instead, unless it is a dated successor (case A above's sibling, already exempted). A fact has no
`pending` queue behind it the way a process edit does, so — exactly as `edit-process` gates
`set_process` (INV-5) — show the user each such field **before** it is written, current value
first:

```
فیلد: «{field path or Persian label}»
فعلی:    {current value, verbatim}
پیشنهاد: {proposed value}
```

Rules, identical to `edit-process`'s:
- **Field by field.** Never bundle several fields into one question. A field the user does not
  approve is **dropped from the delta** before Step 5 — the current value survives untouched.
- **Never infer approval from the instruction alone** — the user must see the exact current value.
- If the user approves, Step 5's `apply` still records the change as a dispute (that is what the
  write ladder does) — but since the user has just confirmed which value should win, Step 5
  immediately follows the `apply` with a `resolve` call settling that field's new account as
  `chosen`, so the entry does not sit disputed despite an explicit confirmation (see Step 5).
- Choosing among **already-recorded** competing accounts by id (e.g. «برای F-00040 حساب اول رو
  انتخاب کن») is not gated here — the accounts and their statements are already visible to the
  user; naming one directly is itself the confirmation, and Step 5 runs `resolve` on it alone.

## Step 5 — Validate, then run the matching `merge facts` verb

1. `Bash: DATA_ROOT=<data-repo> SCHEMA_DIR=<code-repo>/schemas validate facts-delta {run_dir}/facts-delta.json`.
   On non-zero exit, re-dispatch `quantify` (mode `targeted`, same inputs) with the stderr error
   appended, then re-validate. **After 2 failed attempts, STOP and report the delta path to the
   user in Persian** instead of looping — mirroring `quantify`/`process-voice`'s own `classify`
   bound.
2. Run **exactly the verb(s) the instruction and the gated delta call for**:

   | Situation | Verb |
   |---|---|
   | A field fill, a new source/account/item, a from-scratch new entry, a dated successor, an approved field-by-field overwrite (case B) | `Bash: DATA_ROOT=<data-repo> merge facts apply --delta {run_dir}/facts-delta.json --run {run_dir}` |
   | Settling a named/just-confirmed disputed account | `Bash: DATA_ROOT=<data-repo> merge facts resolve --id F-… --field <path> --account <id> --run {run_dir}` |
   | Retiring an entry, with or without a heir (case A) | `Bash: DATA_ROOT=<data-repo> merge facts retire --id F-… [--heir F-…] --run {run_dir}` |
   | Promoting a `note` to another kind | `Bash: DATA_ROOT=<data-repo> merge facts promote --id F-… --kind <kind> [--key <key>] --run {run_dir}` |

   For the apply-then-resolve pair a confirmed overwrite (case B) produces: after `apply` runs, the
   store — not `apply`'s stdout, which only prints `created`/`updated` ids — holds the account id
   you need. Re-read the touched entry from its store file (Step 1's kind→file table). **On a
   first-time dispute (no prior account on that field) the write ladder materialises TWO new open
   accounts on that field in this one `apply` call — the incumbent (the old value, restated) and
   the challenger (the value from this delta) — so "new since before the call" matches both and
   does not tell them apart.** Select the `accounts[]` member on that field by **value**: the one
   whose `value` equals the proposed value the user approved at gate 4.B (compare numbers as
   numbers, strings exactly) — that one is the challenger, and its `id` is the `--account` value for
   the `resolve` call. **Never compute an account id yourself** (it is a hash `merge` alone
   computes) — if no member's `value` matches the approved value, **STOP and report the mismatch to
   the user in Persian** rather than guessing which account to resolve.
3. **Each of these verbs gets THIS run's directory, and it is theirs alone.** `edit-fact` mints one
   run directory per instruction, and `apply` is never mixed with `resolve`/`retire`/`promote` in
   one directory: `apply`'s own `{run_dir}/facts-delta.json` is the applied delta itself (a dict);
   `resolve`/`retire`/`promote` each *append* `{"verb": …, "args": …}` to
   `{run_dir}/facts-delta.json` as a growing **list** — pointed at a directory `apply` already
   wrote into, that append crashes, and pointed at a directory a *different* `apply` call already
   used, a second `apply` silently overwrites the first's provenance (QF-7). So:
   - **If this instruction needs only one verb call** (every one of the four example instructions
     below does), use `{run_dir}` for it and stop.
   - **If it genuinely needs two** — the apply-then-resolve pair Step 4.B's confirmed overwrite
     produces, or a merge (case A) whose heir also needs `apply`-only content from the retired
     entry — run the first verb against `{run_dir}`, then **mint a second stamped**
     `{run_dir2} = runs/facts/{dept}/{stamp2}/` for the second verb, and say so plainly in the
     Step 6 report (which command ran against which directory).
4. A non-zero exit from any of these is a **precondition failure with nothing written** for that
   call — report the stderr message in Persian and stop; do not re-dispatch `quantify` for a
   verb-only failure (the delta already passed `validate`; a remaining failure needs a human
   decision).

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
3. Reply in Persian with what changed: the entry id(s) touched, the field(s) or lifecycle change,
   and — for a destructive op — that the original was retired (not deleted) and its heir, if any.
   Name every run directory a command in Step 5 actually used. Do not paste the full entry JSON
   back.

## Usage examples

The spec's four (§13, verbatim):

- «پارمسان الان ۱۰۰ گرمه» — a dated change (QF-35): resolve the `pack.size`-bearing item, dispatch
  `quantify`, receive a successor entry with `supersedes` and a newer `valid_from` → no gate (case
  C) → `merge facts apply`.
- «این دو تا قانون یکی هستن» — resolve the entry the instruction names most directly; `quantify`
  locates the other via `facts_index` and returns which is the heir → gate A (retire
  confirmation, with heir) → `merge facts retire --id … --heir … --run {run_dir}`.
- «F-00042 رو بازنشسته کن» — resolve `F-00042` directly (no ambiguity) → gate A (retire
  confirmation, no heir) → `merge facts retire --id F-00042 --run {run_dir}`.
- «واحد جدید: حلب» — Step 1.3, no entry to load → `quantify` writes a from-scratch entry (temp id
  `T-1`) → no gate (case C, a plain addition) → `merge facts apply`.

## Invariants

- **`merge facts …` is the sole writer of `facts/**`** — never edit `facts/*.json` (or
  `facts/.index.json`, which `merge` rebuilds on every write) directly; guard-enforced (INV-1).
- **IDs only from `allocate-id`, invoked exclusively by `merge facts apply`.** The delta's new
  entries carry temp ids (`T-1`, …) only; copy the resolved entry's real `F-…` id verbatim where a
  delta references it; never write a real-looking id yourself.
- **INV-3** — no fabrication: the `quantify` agent models only what the instruction and the loaded
  entry/index actually support; you dispatch it, you do not write `facts-delta.json` content
  yourself.
- **INV-5** — a filled field is never overwritten without the user seeing the current value and
  approving that field explicitly (Step 4.B). The engine cannot enforce this (it disputes instead
  of refusing); you are the gate that keeps a confirmed correction from surprising the user by
  sitting disputed.
- **INV-4** — never delete: a retirement is `retire` (`retired: true`, tombstone-equivalent), never
  a hard delete; a merge is `retire --heir`, never removal of the losing entry.
- **Run-directory hygiene (Step 5.3)** — one fresh directory per instruction; `apply` never shares
  one with `resolve`/`retire`/`promote` or with a different `apply` call; a second verb call this
  instruction needs gets its own second stamped directory.
- **Provenance** — the resulting change is `source.type: "chat"` (set by the delta/verb call, never
  by you) and `meta.json`'s `origin: "chat"`; Claude commits it.

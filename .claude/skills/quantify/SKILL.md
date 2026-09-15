---
name: quantify
description: Orchestrate the quantitative-facts pipeline v3 — workbook checkpoint, resolve the set, set-confirmation, transcribe, prepare, plan, run the units in bounded batches of four, review, assemble and validate, apply, commit and the report. Resumes from `facts-plan status`.
---

# quantify playbook (v3)

**Invocation:** `/quantify <department>`.

All paths are relative to `<data-repo>` (`DATA_ROOT`). Every engine CLI runs with
`DATA_ROOT=<data-repo>`; every `validate` call additionally carries `SCHEMA_DIR=<code-repo>/schemas`.
`{run_dir}` is `runs/facts/{department}/{stamp}/`, `{stamp}` a UTC `YYYYMMDD-HHMMSS`.

## What you are, and what you are not

You dispatch, you validate, you assemble, you apply, and you send one engine-written file
**verbatim**. You never write fact content and you never compose owner-facing prose out of data.

You read exactly three things: `facts-plan status` output, `{run_dir}/report.md`, and
validator output. You do **not** read `skeleton.json`, `plan.json`, a
unit's output, `assembly.json` or the delta. They are not for you, and the last run's whole failure
was a coordinator that read them and started authoring.

## Run every command bare

No `2>&1`, no `| head`, no `| tail`, no `>` redirect. The tool result already carries both streams,
and a pipe both truncates the errors you need and trips the repository's write guard.

And never through Python. `facts_plan`, `merge_facts` and `engine_common` are the engine's
internals; the seven CLIs the guard names are its whole interface. A `python -c`, a `-m`, a heredoc or a
script under the run directory that imports one of them is blocked by the repository's guard, and
the thing it was reaching for is either a CLI flag or a defect to report.

## Turn discipline

This playbook runs over a bot that executes **one model turn per user message**: the moment you end
your turn, it stops and waits.

**The only legitimate end-of-turn points are:** Gate M (conditional), Gate A, a **yield** between
batches, and the very end of the run.

Everywhere else you continue in the **same turn**. A returning `Task` or a returning CLI is never a
stopping point. **A message with no tool call ends the turn** — so between stages, either your
message carries the next call, or you have already made the mistake. Never send a
«⏳ … در حال …» status as its own message; a status line rides **inside** the message that carries
the next call.

## Owner vocabulary

«بخش از داده‌ها» for a unit. «فایل» for a workbook, named by its title. Never a unit id, never a
stage letter, never a department code, never a path, never a command, never an account id. The
report is written by the engine — send it as it is.

## Laptop precondition (design §6.1)

Before Stage U, when the run is in a terminal rather than on the bot:

```
Bash: test -f ~/.claude/.ponytail-active
```

This must **fail** (exit 1). If it succeeds, stop and say so: a coding-minimality persona is being
injected into every subagent and the units will under-decide. Also confirm
`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` is exported, or a unit longer than two minutes may be
backgrounded (ADR 0006).

---

## Stage 0 — Resume

```
Bash: DATA_ROOT=<data-repo> facts-plan status --run {run_dir} --new-turn
```

It writes `{run_dir}/turn.json` and prints a compact table — one line per unit as `unit · type ·
state · attempts`, followed by `· retry` and the refused labels when a decision is owed a retry —
plus the stage to enter, `plan_stale`, `elapsed_s` and `yield`.

**Resume ladder**, exactly as `status` reports it: no skeleton → Stage P (or earlier, by what is on
disk: transcripts, then dumps, then the plan); pending units, or a unit with a `retry` list → Stage
U; all units done and no delta → Stage R; a delta present and no `id-map.json` → Stage 5 (a retry of the apply is safe); an
`id-map.json` present and the run unfinished → Stage 6.

For a **fresh** run: create `{run_dir}` and write its initial `meta.json` (`facts-run-meta.schema.json`
— `department`, `origin: "pipeline"`, `actor`, `started_at`, `finished_at: null`, empty
`recordings`/`attachments`/`workbooks`/`units`, `delta: ""`, `merged: false`, `ids_created: []`),
then continue to Stage M.

If the previous turn died mid-stage, your **first message of the turn** says so in one sentence and
**carries the next tool call**:

```persian
کار قبلی نیمه‌تمام مانده بود؛ ۹ بخش از ۱۵ آماده است و از همان‌جا ادامه می‌دهم.
```

---

## Stage M — Workbook checkpoint (STOP, conditional)

```
Bash: DATA_ROOT=<data-repo> dump-workbook --init-manifest
```

It dumps every workbook, fills the mechanical columns, and writes a proposal into every **empty**
judgement column, naming that column in the row's unresolved list. A filled column is never
re-proposed. Its last line reports how many rows still hold an unresolved column.

**If none does, skip straight to "Resolve the set."** Otherwise dispatch, as the first action of
this turn:

```
Task: quantify
  mode: manifest
  run_dir: {run_dir}
  manifest_path: attachments/sheets/manifest.json
  dump_root: attachments/sheets/.dump/
  schema_path: <code-repo>/schemas/manifest-proposal.schema.json
```

Then `Bash: DATA_ROOT=<data-repo> SCHEMA_DIR=<code-repo>/schemas validate manifest-proposal {run_dir}/manifest-proposal.json`.
On a non-zero exit, re-dispatch once with the errors appended; after two attempts, stop and report
in Persian. Do **not** end your turn here — continue into the checkpoint.

### Gate M (STOP)

Present each row as the workbook's **title** and Persian choices, one workbook per numbered line,
each choice with its reason:

```persian
ردیف‌هایی که نیاز به تأیید دارند (۲ مورد):

۱. «کانتر ناهارخوران»
   دپارتمان: آشپزخانه (چون برگه‌ها مصرف و موجودی آشپزخانه را ثبت می‌کنند)
   شعبه: ناهارخوران (چون نام پوشه همین را می‌گوید)
   برگه‌های مرجع: ؟ (هیچ برگه‌ای بدون فرمول و با کد قلم پیدا نشد)

۲. «گزارش مرکزی»
   دپارتمان: مدیریت (چون مصرف اعلامی همهٔ شعبه‌ها را جمع می‌زند)
   شعبه: چاله‌باغ (چون نام پوشه همین را می‌گوید)
   برگه‌های مرجع: هیچ‌کدام (هیچ برگه‌ای شکل مرجع ندارد)

اصلاح می‌کنید یا تأیید؟
```

**End your turn and wait.** On a correction to a judgement column, re-dispatch, re-validate,
re-present, wait again. On a correction to a mechanical column, apply it yourself — no dispatch —
and re-present. On «تأیید»: write the manifest (fill each answered column, remove it from the row's
unresolved list, set `confirmed` when nothing is left), validate it
(`validate manifest attachments/sheets/manifest.json`), fix whatever stderr names, and continue in
the same turn.

A row the owner leaves unresolved is skipped by every later stage and named once in the report.

---

## Resolve the set

Gather, asking nothing yet: every manifest row whose departments include `{department}` or are
empty; `departments/{department}/attachments/*`; the cached `.text/*.txt` conversions; and the
candidate recordings — `meetings/transcripts/{department}-*.txt` together with any
`meetings/audio/{department}-*` that has no transcript. Mark a recording already consumed by an
earlier facts run or by a process run; neither marker excludes it.

---

## Gate A — Set checkpoint (STOP)

Present every input and its state, and close with the recordings question. Recordings are named by
their **date**, never by a file name:

```persian
ورودی‌های آمادهٔ اجرای اعداد آشپزخانه:

الف) فایل‌های Excel (۳ مورد):
  ۱. «پیتزا» — خوانده شد
  ۲. «گزارش مرکزی» — خوانده شد
  ۳. «مواد اولیه» — خوانده شد
ب) پیوست‌های آشپزخانه (۲ مورد):
  ۱. شرح شغل سرآشپز — شرح داده شده
  ۲. فرم کنترل انبار — شرح داده می‌شود
ج) جلسه‌های ضبط‌شدهٔ آشپزخانه:
  ۱. ۲۶ مرداد (رونویس تأییدشده — قبلاً در اجرای فرایند خوانده شده)
  ۲. ۱ شهریور (رونویس خام آماده است — بازبینی می‌شود)
  ۳. ۵ شهریور (بدون رونویس — رونویسی می‌شود)

کدام جلسه‌ها را وارد کنم؟ تاریخ‌ها را نام ببرید یا «هیچ‌کدام» بنویسید.
```

**End your turn and wait.** The workbook and attachment lists are not editable here; only the
recording selection is. A dispute about a workbook's department is a Gate M matter — re-enter it,
then return here.

---

## Stage 1 — Transcribe

Only the recordings the owner named; skipped entirely on «هیچ‌کدام». For each: if
`meetings/transcripts/raw/{basename}.txt` exists, read it and make no call; otherwise
`Bash: DATA_ROOT=<data-repo> transcribe {basename}`. Strip any preamble, run the per-file verbatim
sanity gate, and write the cleaned text to `meetings/transcripts/{basename}.txt`, leaving the raw
file as the audit trail. Then the yield check (below) and on to Stage 2 in the same turn.

---

## Stage 2 — Prepare

```
Bash: DATA_ROOT=<data-repo> dump-workbook --manifest
Bash: DATA_ROOT=<data-repo> extract-attachment {department}
Bash: DATA_ROOT=<data-repo> extract-attachment --path attachments/sheets
```

`--manifest` never fails on a row that still holds an unresolved column: it warns, skips that
workbook and dumps the rest. `extract-attachment` may exit **3** (advisory — some files skipped,
every convertible one converted): relay the skipped lines in Persian and continue. Exit **2** is a
real precondition failure and stops the run. Yield check, then Stage P in the same turn.

---

## Stage P — Plan

```
Bash: DATA_ROOT=<data-repo> facts-plan build {department} --run {run_dir} --recordings a,b,c
```

It reads the dumps, the chosen transcripts, the cached attachment text and the store's identity
slice, and writes the skeleton, the plan, one `input.md` per unit, and the estate's function
library. Each `input.md` ends with the **shape section**, rendered from the store's own schema:
the closed key list per kind with the required keys marked, every enum's values, and a worked
`new[]` example — a paper form among them. That section is the unit's contract, and a key it does
not name is set aside at the unit's gate, never used. It prints the unit count for the log —
**nothing owner-facing**. Do not open what it wrote.

Every attachment — a form photo, a pdf, a docx text — goes into an `attachment` unit of its own
(`u-att-1`, `u-att-2`, … in input order, packed to the size budget), never onto a transcript unit.

Exit 2 means a group could not be split under the size budget, that a candidate spans two
workbooks the manifest keeps apart — the second names both rows, and the remedy is a `twin_of` on
one of them — or that a chosen transcript range or an attachment was placed in no unit, naming the
file. Report any of them in Persian and stop. Yield check, then Stage U in the same turn.

A plan is immutable: `build` refuses to replace one whose units have already produced output, and
`--rebuild` is the only way to renumber them.

---

## Stage U — The units (bounded parallel, batches of at most 4)

Run the pending units in **bounded parallel batches of at most 4** `Task`s per message. Dispatch up
to 4 in **one message**, wait for the whole batch to return, validate each, then dispatch the next
batch of up to 4 — repeat until every unit is done or failed. **Never dispatch more than 4 in the
same message.** Bounded batching, and not full fan-out, is what keeps the run inside the bridge's
proven-safe envelope (ADR 0011) while recovering most of the wall-clock a serial sweep loses — the
agents spend their time on model wait, so four-way concurrency overlaps it.

Do the whole batched sweep **within one turn**, subject to the yield rule: dispatching a batch and
awaiting it is a tool call, not a turn end.

`status` runs the units in two phases: the workbook, attachment and item units first, then the
transcript units. A unit `status` prints as `waiting` is never dispatched; it turns `pending` on its
own once every earlier unit is done or failed, and its input is rewritten by the engine at that
moment — dispatch it as any other unit.

One `Task` per pending unit. Attachment units are dispatched like any unit, in the same batches:

```
Task: quantify
  mode: unit
  run_dir: {run_dir}
  unit: {unit id}
  attempt: {1 or 2}
  input_path: {run_dir}/units/{unit id}/input.md
  schema_path: <code-repo>/schemas/facts-unit.schema.json
  retry: {on attempt 2 only: the labels `status` printed after `retry`}
```

Every dispatch carries the sentence **«nothing runs in the background and no monitor exists; the
results arrive as tool results in this same turn»**. The progress line rides in the same message:

```persian
۸ از ۲۶ بخش از داده‌ها بررسی شد.
```

On return, validate each unit of the batch:

```
Bash: DATA_ROOT=<data-repo> SCHEMA_DIR=<code-repo>/schemas validate facts-unit {run_dir}/units/{unit id}/out.1.json --run {run_dir}
```

The unit is taken from the directory the file sits in, so an output must be written at
`{run_dir}/units/{unit id}/out.{attempt}.json` and nowhere else; a document naming another unit is
refused.

A line beginning `note:` is not a failure: the engine stores that entry with a mark the panel
shows, and nothing is retried for it. A refusal costs only its own decision — the unit's other
decisions land, and `status` prints the unit `done` with `· retry` and the refused labels.

**The retry rule — the cap is the engine's, not a choice.** Retry only refused decisions: a unit
whose `status` line carries `retry` is re-dispatched **once**, with `attempt: 2`, its previous
output path, those labels as `retry` and the validator's lines for them — and its answer is folded
over the first attempt by candidate. A unit still `pending` after a refused first attempt (its
output refused as a whole) is re-dispatched the same way with no `retry` list.
There is no third attempt to give: `validate facts-unit` refuses `out.3.json` outright («attempt
cap: two per run») and `facts-plan status` reports that unit `failed`, which is what `assemble`
reads. The run continues without it; its candidates are reported as unexamined, never as dropped.
A truncated or unparseable file costs no attempt — `status` deletes it.
Never ask the owner to lift the cap: a unit that fails twice is a defect in the input or in the
engine, and both are reported after the run, not worked around during it.

Between batches:

```
Bash: DATA_ROOT=<data-repo> facts-plan status --run {run_dir}
```

**The yield rule.** `status` prints `elapsed_s` and `yield`. `yield: true` is the **only** signal you
act on — never your own sense of how long this is taking. Check it after Stage 1, after Stage 2,
after Stage P, between batches, and before Stage R. On `yield: true`, send the progress line as the
**last message of the turn** and stop. **You never continue past a `yield: true`** — not for one
more batch, not to finish validating a unit already returned, not because the next call is cheap.
Stopping is the engine's instruction, and the next message resumes it losslessly:

```persian
۸ از ۲۶ بخش از داده‌ها بررسی شد؛ برای ادامه «ادامه بده» را بفرستید.
```

The owner's next message re-enters Stage 0 and the run continues from the first unfinished unit.
Ending a turn at a boundary is a normal, lossless outcome. If the run is on the bot and a budget
warning arrives in the conversation, treat it as a `yield: true` at the next boundary.

---

## Stage R — Review

```
Bash: DATA_ROOT=<data-repo> facts-plan digest --run {run_dir}
```

Then one dispatch:

```
Task: quantify
  mode: review
  run_dir: {run_dir}
  input_path: {run_dir}/review/input.md
  schema_path: <code-repo>/schemas/facts-unit.schema.json
```

Then `Bash: DATA_ROOT=<data-repo> SCHEMA_DIR=<code-repo>/schemas validate facts-unit {run_dir}/review/out.json --run {run_dir}`.
On failure, re-dispatch once with the validator's lines appended — they name the decision and the
member. On a second failure, continue to Stage V anyway: `assemble --review` applies every decision
that passes and holds back the rest **by decision**, and the report names each one. The review is
never dropped — owner ruling, 2026-09-09. `digest` shares `assemble`'s preparation: when it exits 2
naming a **unit**, no output of that unit is usable and an attempt is left — re-dispatch it
exactly as Stage U says and run `digest` again. Only when its line says the digest is over the
engine's ceiling is the run over: stop it and send

```persian
نتیجهٔ این اجرا بزرگ‌تر از آن است که یکجا بازبینی شود. این یک نقص فنی است و باید برطرف شود؛ هیچ‌چیز ثبت نشد.
```

---

## Stage V — Assemble and validate

```
Bash: DATA_ROOT=<data-repo> facts-plan assemble --run {run_dir} --review
Bash: DATA_ROOT=<data-repo> SCHEMA_DIR=<code-repo>/schemas validate facts-delta {run_dir}/facts-delta.json --store --run {run_dir}
```

The validate call performs the whole apply in memory, including the resulting store's schema, and
writes nothing — so what it refuses is exactly what `apply` will hold back, and nothing more.

**A per-entry error here is a defect, not your work — and it costs only that entry.** Every
per-entry rule — the store schema per kind and the content pass — is enforced at each unit's own
gate, so a delta assembled from validated units should not fail one (design addendum I1). If
`validate facts-delta` names a single entry anyway, do not stop: `apply` holds that entry back,
writes the rest, and the report names it. Hand-repair nothing. `note:` lines are marks, not errors.

`assemble` itself exits 2, naming the unit, when no attempt of that unit is usable (each was
refused as a whole) and an attempt is still left: re-dispatch that unit and run `assemble` again. On a residual error, the
message names the unit that produced it. If that unit is under two attempts, re-dispatch it with
the error, then **re-enter Stage R** (the assembly changed, so the review is stale: digest, review,
validate) and re-run Stage V. `assemble --review` exits 2 naming a stale review for the same
reason — re-enter Stage R. Never proceed without the review. If Stage V fails again on an error
that names no entry — the delta itself — stop **before** the apply and relay it in Persian.

---

## Stage 5 — Apply

Stage V passing is the approval — owner ruling, 2026-09-09: the checkpoint message was not
readable at the size a department produces, and an apply is reversible. Continue **in the same
turn**, asking nothing. The owner reads the result in the report (Stage 7) and answers any
dispute there; a run the owner rejects is undone with `merge facts revert --run {run_dir}`
(runbook 07 §6). `gate-b.md` stays on disk as the run's record of what it proposed and is never
sent.

```
Bash: DATA_ROOT=<data-repo> merge facts apply --delta {run_dir}/facts-delta.json --run {run_dir}
```

One delta, one run directory, once. Capture every `created`/`updated` id it prints.

`apply` judges the delta entry by entry. An entry that would break the store is held back — a
`precondition failed: held back:` line on stderr, and a row in `{run_dir}/held.json` — and every
other entry is written. **Exit 0 with held entries is a finished apply: the run continues to
Stage 6.** Do not re-dispatch for a held entry, do not relay the lines — the report names it.

Exit 2 is a **precondition failure with nothing written** — not one entry could be. Report it in
Persian and **stop the run**. Do not re-dispatch anything and do not hand-edit anything — ever:

```persian
ثبت انجام نشد: یکی از پیش‌شرط‌ها برقرار نبود و هیچ چیزی نوشته نشد. علت را بررسی می‌کنم و نتیجه را می‌گویم.
```

---

## Stage 6 — Finish and commit

Update `{run_dir}/meta.json` to its final shape — `finished_at`, `recordings`, `attachments`,
`workbooks`, `delta`, `merged: true`, `ids_created`, and `units` (one `{id, type, state, attempts}`
per unit, from `facts-plan status`) — and validate it:

```
Bash: DATA_ROOT=<data-repo> SCHEMA_DIR=<code-repo>/schemas validate facts-run-meta {run_dir}/meta.json
Bash: DATA_ROOT=<data-repo> facts-plan report --run {run_dir}
Bash: git -C <data-repo> add departments runs facts attachments && git -C <data-repo> commit -m "quantify({department}): {C} created, {U} updated"
```

Never `git add -A`. Continue to Stage 7 in the same turn.

---

## Stage 7 — Report

Read `{run_dir}/report.md` and **send it verbatim**. Its first lines name any lost source — a file,
a meeting or photos no unit could carry into the store — in the owner's own names; after them it
carries the open disputes lettered, the unanswered units grouped per item, the dropped candidates in the owner's own words, any workbook
skipped or part left unfinished, and what the review changed and what of it was set aside. It does
not carry the engine's findings inside the files (owner ruling, 2026-09-09): those are drawn on the
entry in the panel, and the run keeps its own count of them.

When the owner answers a lettered dispute, **you** run the resolve — never print a command:

```
Bash: DATA_ROOT=<data-repo> merge facts resolve --id F-… --field <path> --account <id> --run {fix_run}
```

`{fix_run}` is a **fresh** stamped run directory, never `{run_dir}` (already claimed by the apply).
Every resolve in this report may share one `{fix_run}`. Confirm by the field's Persian label, never
by id or path. The run ends with the report — owner ruling, 2026-09-09: the store-wide audit is an
operator's tool (runbook 07 §5) and is not run here.

---

## Stage ordering

| Stage | Name | Tool / CLI | Pauses? |
|---|---|---|---|
| 0 | Resume | `facts-plan status --new-turn` | — |
| M | Workbook checkpoint | `dump-workbook --init-manifest`, `Task: quantify` (manifest) | **STOP** if a row is unresolved |
| — | Resolve the set | Read / Glob | — |
| **A** | **Set checkpoint** | message | **STOP** |
| 1 | Transcribe | `transcribe` × chosen | — |
| 2 | Prepare | `dump-workbook --manifest`, `extract-attachment` × 2 | — |
| **P** | **Plan** | `facts-plan build` | — |
| **U** | **Units** | `Task: quantify` (unit) × ≤4 per message, `validate facts-unit` each | **STOP** at a yield |
| **R** | **Review** | `facts-plan digest`, `Task: quantify` (review), `validate facts-unit` | — |
| **V** | **Assemble + validate** | `facts-plan assemble`, `validate facts-delta --store --run` | — |
| 5 | Apply | `merge facts apply` | — |
| 6 | Finish + commit | Write `meta.json`, `facts-plan report`, `git -C` | — |
| 7 | Report | send `report.md` verbatim | — |

## Key invariants

- `merge facts` is the only writer of `facts/**` (INV-1, guard-enforced). Neither this playbook nor
  the agent ever writes there.
- The coordinator writes no fact content and composes no owner-facing prose from data. `report.md`
  goes out verbatim.
- Batches of at most four `Task`s per message; every unit validated on return; at most two attempts
  per unit per run — refused by the engine, never lifted.
- The review is never dropped: what passes is applied, what fails is held back by decision and
  named in the report; a stale review is redone.
- The only yield signal is `facts-plan status`'s own `yield: true`, and it ends the turn.
- The engine is driven through its CLIs only; no Python touches its internals.
- A refusal costs one decision or one entry, never a unit or a file: a unit retries only its refused
  decisions, and `apply` holds back only the entries that would break the store and writes the rest.
- One `apply` per run, into one run directory. A second apply into a used directory is refused.
  Stage 7's resolves open their own fresh directory.
- Every engine command is run bare.
- `meta.json` with `finished_at: null` always signals a resumable run; all timestamps are ISO-8601
  with a `Z`.

---
name: process-voice
description: Orchestrate the full voice→IDEF pipeline — transcribe, classify, human checkpoint, extract, merge, summarize, commit, and the end-of-run conflict report. Resumes from {run_dir}/meta.json.
---

# process-voice playbook

**Invocation:** `/process-voice <department>` (default: the whole department set) **or** `/process-voice <t1> <t2> …` (an explicit list of transcript/audio basenames; the department is inferred from filenames). One path — a set of one is the smallest case; there is **no** per-voice or batch mode. The date part of a basename is Shamsi.

All file paths are relative to `<data-repo>` (the value of `DATA_ROOT`).
Every engine CLI must be called with `DATA_ROOT=<data-repo>` set in the environment.

## Turn discipline (critical — read first)

This playbook runs over a Telegram bot that executes **one model turn per user message**:
the moment you end your turn, the bot stops and waits for the user to send another message.
A multi-stage run must therefore **not yield mid-pipeline**, or it will look "stuck" to the
user even though nothing is wrong.

**The ONLY legitimate end-of-turn points in a run are:**
1. **Gate A** (set-confirmation checkpoint, before Stage 1) — pause for the user to confirm the set,
2. **Gate B** (segmentation/restructure checkpoint, after Stage 3) — pause for the user to approve
   the proposed process set + restructure ops,
3. the **Stage 9 report → Stage 10** hand-off and, within **Stage 10** (consolidation review), the
   numbered report (**10c**) and each applied item's show-result (**10d step 6**) — human-gated
   STOP points like Gate B, one item at a time, and
4. the **very end of the run**, after the last Stage 10 item (or Stage 10b's empty-list silence).

Gate A and Gate B are the two mid-run pauses; Stage 10's per-item gates are the post-run pauses;
everywhere else you continue in the **same turn**.

Everywhere else you MUST continue in the **same turn**. A returning `Task`/subagent (classify,
each extract batch, summarize, each `consolidate` review/apply dispatch) or a returning engine CLI
(transcribe, merge) is **never** a stopping point — the instant it returns, proceed directly to the
next stage (or the next extract) without ending your turn. In Stage 10 the STOP points are the user
gates (10c, 10d step 6), **not** the `consolidate` dispatch returning. Dispatching a subagent and then stopping is one failure this rule prevents. Just as bad —
and **the most common failure in practice** — is *announcing* a stage in prose and then stopping
**before** you dispatch (e.g. sending «…در حال استخراج…» and ending the turn). **A message that
contains no tool call ends the turn.** So between stages, either your message carries the next
`Task`/CLI call, or you have already made the mistake.

**Status lines — never send one on its own.** Because a prose-only message *is* the end of your
turn, do **not** send a "⏳ … در حال …" status as its own message before a stage — that standalone
message is the single most common reason a run stalls mid-pipeline. If you want to reassure the
user, the status line must ride **inside the same message that carries that stage's `Task`/CLI
call** (a short text block, then the tool calls, in one message). When unsure, send **no** status
and just dispatch — the bot already shows a live progress indicator, so silence is safe while a
lone status message is not.

---

## Stage 0 — Resolve state / resume

`{run_dir}` is `runs/{department}/{stamp}/`, where `{stamp}` is a UTC `YYYYMMDD-HHMMSS`. A run is
scoped to **one department**.

1. Resolve the department: for the department form it is the argument; for the explicit-list form,
   infer it from the transcript basenames (`{department}-…`). Then look for the most recent
   `runs/{department}/*/meta.json`.
2. **Resume an interrupted run** — `meta.json` exists with `finished_at: null`:
   - `segments.json` **absent** → the set was resolved but not yet confirmed: **re-enter at Gate A**
     (re-resolve the set and re-present it).
   - `segments.json` **present**, `processes[]` empty → classified but not yet approved:
     **re-enter at Gate B** (re-read `segments.json` and re-present it).
   - `processes[]` non-empty → merges started: resume at Stage 6 for any un-merged artifact, then
     Stages 7–9. Do NOT re-run completed stages (idempotency).
3. **Fresh run** — no in-progress `meta.json`: create a new `{run_dir} = runs/{department}/{stamp}/`
   and continue to "Resolve the set".
4. **Re-run** — the user explicitly asks to re-process a finished set: create a new
   `runs/{department}/{stamp}/` with the current timestamp (the timestamp *is* the attempt key —
   there is no `attempt-NN`; each run gets its own stamped dir). Continue to "Resolve the set".

> `{run_dir}` holds all run artefacts (meta.json, segments.json, candidates/, deltas/,
> restructure/). Transcripts at `meetings/transcripts/{basename}.txt` are shared across runs and are
> never run-relative.

---

## Resolve the set

- **Department form:** the set = every recording the department has —
  `meetings/transcripts/{department}-*.txt` **∪** any `meetings/audio/{department}-*` without a
  matching transcript. Glob both.
- **Explicit-list form:** the set = exactly the named basenames. The user's selection is
  **authoritative** — never silently widen it, never refuse it for being incomplete. Note which
  department recordings are being **left out** (glob the department, subtract the named set) to
  disclose at Gate A.

Order the set by Shamsi date in the filename (later sessions supersede earlier ones downstream).

**Context budget.** If the resolved set is so large it would exceed the largest-context Opus budget,
**stop and name the set, its size, and the limit**, asking the user to narrow it or raise the
context. Never compress, distil, or fall back to one-transcript-at-a-time (spec §4.1).

---

## Gate A — set-confirmation checkpoint (STOP)

Before transcribing anything, disclose the resolved set and pause.

1. Init `{run_dir}` (create the directory) and write an initial `{run_dir}/meta.json` with
   `finished_at: null` and `processes: []` (Stage 2 shape) so Stage-0 resume can re-enter here.
2. Send a Persian checkpoint listing **the set** (every basename, transcript or audio) and, for the
   explicit-list form, **which department recordings are left out**. Example:

   ```
   مجموعهٔ ضبط‌های دپارتمان dining برای این اجرا:
     ۱. dining-1405-04-11
     ۲. dining-1405-04-14
     ۳. dining-1405-04-15 (فاقد رونویس — رونویسی می‌شود)
   (فرم فهرست صریح) موارد کنار گذاشته‌شده: dining-1405-04-20
   تأیید می‌کنید یا مجموعه اصلاح شود؟
   ```

3. **End your turn and wait.** This is Gate A. On the user's reply:
   - **Edit** (add/drop a recording, switch department↔list): **re-resolve the set** ("Resolve the
     set"), re-present Gate A, wait again.
   - **Confirmation** («تأیید» / «بله» / «ok»): proceed to Stage 1 in the next turn.

---

## Stage 1 — Transcribe-missing reconcile (FR-P1, FR-P2)

Runs **after** Gate A, only for the confirmed set. Idempotent. For **each** confirmed recording
that lacks a transcript at `meetings/transcripts/{basename}.txt`:

1. Run the transcription CLI (idempotent — skips Vertex AI if the transcript already exists):
   ```
   Bash: DATA_ROOT=<data-repo> transcribe {basename}
   ```
2. On a **fresh transcription** (the transcript file did not exist before):
   - Read stdout. Strip any Gemini preamble, postamble, or section headings injected by the model.
   - **Per-file verbatim sanity gate:** if the text appears summarized or rewritten (rather than
     verbatim speech), flag it to the user and STOP. When stopping, tell the user (in Persian) their
     options: «(الف) پردازش را دوباره اجرا کنید تا رونویسی از نو انجام شود؛ یا (ب) یک رونویسِ
     اصلاح‌شده را به‌صورت دستی در `meetings/transcripts/{basename}.txt` قرار دهید و دوباره اجرا کنید
     — در این حالت خط لوله به‌دلیل ایدمپوتنسی از Vertex عبور می‌کند و همان فایل شما را استفاده
     می‌کند.»
   - Write the cleaned text to `meetings/transcripts/{basename}.txt`.
3. Confirm every recording in the set now has a transcript before continuing. (Recordings that
   already had a transcript are untouched.) This whole reconcile runs **in one turn** (each
   `transcribe` is a CLI call, not a turn end) — proceed to Stage 2 in the same turn.

---

## Stage 2 — Init / finalise run record

Gate A already wrote an initial `{run_dir}/meta.json`. Now record the confirmed set (write
`finished_at` explicitly as `null` — Stage-0 resume depends on it):

```json
{
  "department": "<department>",
  "transcripts": ["<basename>", "..."],
  "started_at": "<ISO-8601 Z timestamp>",
  "finished_at": null,
  "attempt": 1,
  "processes": []
}
```

- `department`: the run's department code (`^[a-z]+$`).
- `transcripts`: every confirmed transcript basename in the set.
- `started_at` / `finished_at`: ISO-8601 with `Z` suffix (e.g. `2026-07-15T09:14:00Z`).
- `attempt`: `1` (each run gets its own stamped `{run_dir}`; the timestamp is the attempt key).
- `processes`: empty; populated after merge in Stage 6.

**Validate:** `Bash: validate run-meta {run_dir}/meta.json`. On non-zero exit, fix the offending
field (named in stderr) and re-validate before continuing.

---

## Stage 3 — classify over the set

Dispatch `classify` as the **first thing you do this turn** (no prose-only message first — that
ends the turn; any status line rides in the **same** message as the `Task` call):

```
Task: classify
  transcript_paths: [<every confirmed transcript path in the set>]
  department: {department}
  run_dir: {run_dir}
```

Wait for it to complete. It reads **all** transcripts and writes `{run_dir}/segments.json`, labelling
each desired process `new`/`update`/`unchanged`/`merge`/`split`/`attach`/`tombstone` with
attributed `evidence[]` + `supersedes[]`, plus the top-level `tombstone`/`attach_subprocess`/
`contradictions` op arrays. **Keep its completion message** — the contradictions/lineage summary it
returns feeds Gate B.

**Validate it:** `Bash: validate segments {run_dir}/segments.json`. On non-zero exit, re-dispatch
`classify` with the stderr error appended, then re-validate. After 2 failed attempts, stop and
report to the user instead of looping.

**Do NOT end your turn here.** classify returning is not a stopping point — continue immediately, in
the **same turn**, into Gate B (read `segments.json`, send the checkpoint).

---

## Gate B — segmentation / restructure checkpoint (STOP) (FR-P4)

1. Read `{run_dir}/segments.json`.
2. Present **the department's proposed process set in shift order**, each item labelled by its op
   (`new`/`update`/`unchanged`/`merge`/`split`/`attach`/`tombstone`), with, per spec §4.10:
   - the committed id(s) it **supersedes** (from `supersedes`);
   - **attributed evidence** spanning sessions — for each item, one indented line per session
     mention: `     مستند به: «…» ({transcript})` drawn from that segment's `evidence[]`;
   - a **lineage line** for `merge`/`split`/`attach`/`tombstone` (which committed ids are
     merged/split/re-parented/retired), from the classify return summary + the `tombstone` /
     `attach_subprocess` arrays;
   - **contradictions** the agent flagged — both accounts, each attributed (from the
     `contradictions` array);
   - carried from Gate A (explicit-list form): which recordings were **left out**.
3. Compose the checkpoint in Persian and send it.

**Example (reproduce this structure):**

```
فرایندهای پیشنهادی برای دپارتمان dining (به ترتیب شیفت):
الف) جدید:
  ۱. فرایند سفارش‌گیری سالن
     مستند به: «مشتری سر کیوسک سفارشش را می‌زند…» (dining-1405-04-11)
ب) به‌روزرسانی:
  — «فرایند پخت» ← cooking-002 (بازبینی برچسب یک گره)
     مستند به: «زمان سرخ‌کردن را از هفت به پنج دقیقه بردیم» (dining-1405-04-15)
ج) ادغام:
  — «فرایند تسویه» ← dining-003 + dining-007 (این دو در واقع یک فرایندند)
د) تفکیک:
  — dining-005 ← «آماده‌سازی سالن» + «تمیزکاری پایان‌شب» (یک فرایند در واقع دو تاست)
هـ) الحاق زیرفرایند: dining-009 زیر باکس n4 از فرایند dining-002
و) حذف (سنگ‌قبر): dining-011 (این کار دیگر انجام نمی‌شود)
⚠ تعارض: «فرایند انبار» — دو روایت متفاوت ثبت شد (dining-04-11 و dining-04-14).
موارد کنار گذاشته‌شده: dining-1405-04-20
تأیید می‌کنید یا اصلاحی لازم است؟
```

4. **End your turn and wait.** This is Gate B — the second and last mid-run pause. `{run_dir}/meta.json`
   has `finished_at: null` and `processes: []`; nothing has been written to `departments/**`. On the
   next turn read `{run_dir}/meta.json` to resume (Stage-0 routes here when `segments.json` exists and
   `processes[]` is empty). If the classify return message is no longer in context, re-dispatch
   `classify` (idempotent) to regenerate the summary before composing this checkpoint.

**Handling the user's reply:**

- **Correction** (missed/extra process, wrong op, wrong `supersedes`, contradiction resolved a
  particular way, an item should be merge not update, etc.): re-dispatch **only** `classify` with the
  corrected instructions (nothing in `departments/**` has been written yet), re-validate
  `segments.json`, re-present Gate B, wait again.
- **Confirmation** («تأیید» / «بله» / «ok»): proceed to Stage 5a.

---

## Stages 5–9 — Build the confirmed set (FR-P8)

A run is scoped to **one department**, so there is no per-department fan-out: run Stages 5a–8 once
for `{department}`, then Stage 9. (Segments the set surfaced in a **neighbour** department are rare;
if any exist, handle them by running their own department pipeline separately — do not silently
widen this run.)

---

### Stage 5a — prepare attachments

Before extracting, convert each touched department's attachment documents to cached text so the
`extract` and `summarize` agents can read them. This runs **in the same turn** as the extract
sweep (it carries a `Bash` call, so it does not end the turn — see Turn discipline).

For this run's department:

```
Bash: DATA_ROOT=<data-repo> extract-attachment {department}
```

- Capture stdout: each line is a cached `.txt` path relative to `<data-repo>`. Collect them into
  a per-department list `attachment_texts` (an empty list if the command printed nothing).
- If the command exits non-zero, it still printed the paths it *could* convert on stdout — use
  those. Note any `skipped …` lines from stderr and, at the end of the run, mention them to the
  user in Persian (e.g. «پیوستِ {نام فایل} خوانده نشد و نادیده گرفته شد.»). A failed attachment
  must **never** block extraction — attachments are a supplement.

`attachment_texts` is passed into every `extract` task (Stage 5) and the `summarize` task
(Stage 7) for that department.

---

### Stage 5 — extract (bounded parallel — batches of at most 4)

Extract the segments classified as `new`, `update`, `merge`, or `split` in **bounded parallel
batches of at most 4**. Dispatch **up to 4** `extract` `Task`s **in one message**, **wait for the
whole batch to return**, then dispatch the next batch of up to 4 — repeat until every
`new`/`update`/`merge`/`split` segment has been extracted. **Never dispatch more than 4 `extract`
tasks in the same message.** Bounded batching (not full N-way fan-out) keeps the run within the SDK
bridge's proven-safe envelope (control-bot patches 0004/env; ADR 0011) while recovering most of the
wall-clock lost to serial extract — most of each agent's runtime is model/network wait, so 4-way
concurrency shortens the sweep substantially on the 2-CPU host.

Do the whole batched sweep **within one turn**: dispatching a batch and awaiting its results is a
tool call, not a turn end, so proceed from one batch to the next (and then on to Stage 6) without
ending your turn. Do **not** send a «⏳ در حال استخراج…» prose-only message (a message with no tool
call ends the turn and stalls the run); if you want a status line, it must ride in the **same
message** as an `extract` `Task` batch.

Dispatch one `extract` `Task` per **desired process** that needs an artifact — i.e. every segment
whose `status` is `new`, `update`, `merge`, or `split` (each heir of a merge/split is its own
`restructure` dispatch). Pass the segment's attributed `evidence` and the full set:

- **new segment** (`supersedes: []`):
  ```
  Task: extract
    department: {department}
    process_name: {process_name}           # from this segment
    evidence: {evidence}                   # this segment's evidence[] from segments.json
    transcript_paths: [<every transcript in the set>]
    mode: new
    seq: {seq}                             # zero-padded run ordinal, e.g. 01
    run_dir: {run_dir}
    attachment_texts: {attachment_texts}   # from Stage 5a (may be empty)
  ```
  The agent writes `{run_dir}/candidates/{seq}.json`.

- **update segment** (`supersedes: [X]`, one-to-one):
  ```
  Task: extract
    department: {department}
    process_name: {process_name}
    evidence: {evidence}
    transcript_paths: [<every transcript in the set>]
    mode: update
    existing_id: {X}
    existing_process_paths: [departments/{department}/processes/{X}.json]
    run_dir: {run_dir}
    attachment_texts: {attachment_texts}
  ```
  The agent writes `{run_dir}/deltas/{X}.json`.

- **merge / split heir** (`restructure`): dispatch one `extract` per **heir** (a merge yields one
  heir; a split yields 2+). Pass every superseded `process.json` so the agent has the originals'
  ids:
  ```
  Task: extract
    department: {department}
    process_name: {heir process_name}
    evidence: {evidence}
    transcript_paths: [<every transcript in the set>]
    mode: restructure
    existing_process_paths: [departments/{department}/processes/{S}.json, ...]   # all superseded ids
    seq: {seq}
    run_dir: {run_dir}
    attachment_texts: {attachment_texts}
  ```
  The agent writes each heir to `{run_dir}/candidates/{seq}.json` (a full candidate + its
  `subprocess_links`). Collect, per restructure, the heir candidate paths and each heir's
  `supersedes` (from `segments.json`) — Stage 6 assembles them into a restructure **plan**.

**`unchanged` (`supersedes: [X]`, identical), `tombstone`, and `attach_subprocess` segments are NOT
extracted** — they carry no graph artifact. `unchanged` is recorded in `meta.json` in Stage 8;
`tombstone`/`attach` are executed directly by their own `merge` verbs in Stage 6.

After the **last** extract batch returns, proceed to Stage 6 in the **same turn**.

---

### Stage 6 — merge (deterministic)

Process every artifact using the `merge` engine CLI — the **sole writer** of
`departments/**/processes/*.json` (hook-enforced). Run the verb matching each segment's op.

**For each `new` candidate:**
```
Bash: DATA_ROOT=<data-repo> merge new \
  --candidate {run_dir}/candidates/{seq}.json \
  --department {department} \
  --run {run_dir}
```
Capture the printed `<id>`. Record `{id, status: "new"}` for meta.json.

**For each `update` delta:**
```
Bash: DATA_ROOT=<data-repo> merge update \
  --process {existing_id} \
  --delta {run_dir}/deltas/{existing_id}.json \
  --run {run_dir}
```
Record `{existing_id, status: "update"}` for meta.json. (`merge update` now also applies the delta's
`revise_nodes` and `remove_edges`, and re-layouts after edge removal — no extra flags needed.)

**For each `merge`/`split` restructure:** assemble the plan file `{run_dir}/restructure/{seq}.json`
in the shape `{department, heirs: [{candidate, supersedes:[pid], subprocess_links:[…]}]}` — one
`heirs[]` entry per heir extracted in Stage 5, `candidate` being the **inline candidate object**
(the JSON contents of that heir's `{run_dir}/candidates/{seq}.json` file, not its path — the
`restructure.schema` requires the object), `subprocess_links` from the heir's artifact, and
`supersedes` = this heir's members from `segments.json` **minus** any id that appears in the
heir's `subprocess_links.child` (a member id is in `supersedes` **or** `subprocess_links.child`,
never both — else the engine would tombstone a still-live child). Then:
```
Bash: DATA_ROOT=<data-repo> merge restructure \
  --plan {run_dir}/restructure/{seq}.json \
  --run {run_dir}
```
Capture the printed heir ids and superseded (tombstoned) ids. Record each heir as
`{id, status: "merge"|"split", superseded:[…], heir_of:[…]}` for meta.json.

**For each `attach_subprocess` entry** (from `segments.json`):
```
Bash: DATA_ROOT=<data-repo> merge attach-subprocess \
  --parent-process {parent_process} --node {parent_node} --child {child} \
  --run {run_dir}
```
Record `{id: {child}, status: "attach"}` for meta.json.

**For each `tombstone` id** (from `segments.json`):
```
Bash: DATA_ROOT=<data-repo> merge remove \
  --process {id} --run {run_dir}
```
Record `{id, status: "tombstone"}` for meta.json.

**What merge does when a candidate/delta contains sub-processes:**
For each entry in `subprocesses` (candidate) or `add_subprocesses` (delta), `merge` performs these 7 steps automatically:
1. Resolves the parent activity's real node ID from the newly-merged or existing `process.json`.
2. Allocates the child process ID via `allocate-id` CLI (INV-1 — never by an LLM).
3. Writes `departments/{department}/processes/{child-id}.json` with `parent: {process: "<parent-id>", node: "<parent-node-id>"}` and `source.type: "auto"`.
4. Sets the parent node's `subprocess` field to the child process ID.
5. Syncs the parent box's `icom` to equal the child's `idef0` (child wins on conflict).
6. Lays out the child process (serpentine layout).
7. Prints `subprocess <child-id> node <parent-node-id>` to stdout.

**Capture the printed child IDs:** parse every `subprocess <child-id> node <parent-node-id>` line from merge stdout. Collect these pairs for use in Stage 8.

**Layout:** `merge` also computes/updates node positions (serpentine layout) for new nodes; manually positioned nodes (`layout: manual`) are never moved. Never set node positions yourself — the layout is deterministic engine work, not LLM work.

---

### Stage 7 — summarize over the set

Dispatch a `summarize` task for `{department}` — as the **first action of the turn**, no standalone
status message before it (that ends the turn); any status line rides in the **same message** as the
`Task` call:
```
Task: summarize
  department: {department}
  transcript_paths: [<every transcript in the set>]
  data_root: <data-repo>
  attachment_texts: {attachment_texts}   # from Stage 5a (may be empty)
```
Wait for completion. It reads the whole set and writes/updates `departments/{department}/overview.json`.

**Validate it:** `Bash: validate overview departments/{department}/overview.json`. On non-zero exit, re-dispatch `summarize` with the stderr error so it corrects the file, then re-validate (max 2 attempts, then report to the user).

---

### Stage 8 — Finish run + commit

1. Update `{run_dir}/meta.json`:
   - Set `finished_at` to the current ISO-8601 Z timestamp.
   - Populate `processes[]` with every entry from Stages 5–6:
     - new: `{id: "<dept>-NNN", status: "new"}`
     - update: `{id: "<existing_id>", status: "update"}`
     - unchanged: `{id: "<existing_id>", status: "unchanged"}`
     - merge/split heirs: `{id: "<heir-id>", status: "merge"|"split", superseded: […], heir_of: […]}`
     - attach: `{id: "<child-id>", status: "attach"}`
     - tombstone: `{id: "<id>", status: "tombstone"}`
     - auto-created sub-processes (from merge stdout): `{id: "<child-id>", status: "new", auto_subprocess_of: "<parent-id>"}`
   - Re-validate: `Bash: validate run-meta {run_dir}/meta.json` (fix and re-validate on failure) so a
     malformed record is never committed.

2. Commit the run artefacts:
   ```
   Bash: git -C <data-repo> add departments runs && \
         git -C <data-repo> commit -m "pipeline({department}): {N} processes from {K} transcripts"
   ```
   `{N}` = count of new + updated + restructured (merge/split/attach/tombstone) processes (not
   unchanged); `{K}` = size of the set.

---

### Stage 9 — Conflict report + auto-subprocess summary (FR-M4)

After the run is committed:

1. **Auto-subprocess report (report only — no approval pause):** For every auto-created child collected in Stage 6, output a Persian line in Telegram:
   ```
   زیرفرایند {child-id} به‌صورت خودکار زیرِ باکس {parent-node} از فرایند {parent-id} ساخته شد.
   ```
   Children are ordinary processes: UI-editable, classify-matchable on future voices (`update`/`unchanged` with their `existing_id`), and user-removable (orphan, not cascade — INV-4). No approval is required.

2. For each `process.json` written or updated in this run, read its `pending[]` array.
3. If any process has pending conflicts, present the full list in Telegram. If there are no auto-subprocess entries and no conflicts, report completion directly (see item 5).

**Conflict report format (Persian):**

```
گزارش تعارض‌های این اجرا:

فرایند: {id} — {process_name}
  فیلد: {field_name}
  مقدار فعلی: {current_value}
  مقدار پیشنهادی: {proposed_value}
  منبع: {transcript}

برای قبول: merge accept --process {id} --index {n}
برای رد: merge reject --process {id} --index {n}
یا از طریق پنل UI اقدام کنید. مقدار اصلی تا تأیید شما تغییر نمی‌کند.
```

4. If the user resolves inline, run:
   ```
   Bash: DATA_ROOT=<data-repo> merge accept --process {id} --index {n}
   ```
   or:
   ```
   Bash: DATA_ROOT=<data-repo> merge reject --process {id} --index {n}
   ```
   The original value is **never auto-changed**. If the user defers to the UI inbox, leave the `pending[]` entries in place.

5. **Restructure lineage report (report only — no pause).** For every `merge`/`split`/`attach`/
   `tombstone` recorded in Stage 8, output a Persian line naming the heir(s) and the superseded/
   retired/re-parented committed ids, e.g. «فرایندهای dining-003 و dining-007 در dining-014 ادغام
   شدند (نسخه‌های قبلی سنگ‌قبر شدند).» Tombstones stay on disk, are excluded from future matching,
   and are shown labelled in the UI.

6. If there are no conflicts (`pending[]` is empty for all written processes), report completion:
   ```
   پایان موفق اجرا. مجموعهٔ {K} رونویسِ دپارتمان {department} پردازش و ثبت شد.
   ```

---

### Stage 10 — consolidation review (STOP, human-gated) (design 2026-07-19)

Runs after the run is committed (Stage 8) and the conflict report (Stage 9). It is a
**STOP gate** like Gate B: you present suggestions and wait for the user, one item at a
time.

**10a — Review.** Dispatch — as the first action of the turn:
```
Task: consolidate
  mode: review
  department: {department}
  transcript_paths: [<every transcript in the set>]
  attachment_texts: {attachment_texts}   # from Stage 5a (may be empty)
  run_dir: {run_dir}
  data_root: <data-repo>
```
Wait. Then **validate:** `Bash: validate consolidation {run_dir}/consolidation.json`
(on non-zero exit, re-dispatch `consolidate` with the stderr error, max 2 attempts).

**10b — If `suggestions` is empty:** if the `consolidate` return **also** has no «کم‌اهمیت‌تر»
notes, tell the user no consolidation is needed («بازبینی انجام شد؛ هیچ ادغام یا زیرفرایندی
لازم نیست.») and the run is done — STOP, do not invent work. If the return **does** carry
«کم‌اهمیت‌تر» notes, present them (the heading in 10c) and ask whether to pursue any; then STOP.

**10c — Present the numbered report (STOP).** Build the message **from
`{run_dir}/consolidation.json`** (the detailed source), **not** from the agent's short
return summary. Produce one Persian message with this structure — keep the confident items
**fully detailed**, do not summarise them away:

- a one-line intro (all active processes reviewed together; tombstoned/superseded ones
  ignored);
- «N پیشنهاد مطمئن:» then **every** `pending` suggestion as `۱، ۲، ۳…`, each rendering its
  **full `problem` text and full `action` text verbatim** (never shorten or paraphrase them)
  plus the ids involved (`processes` / `child`+`parent_process`+`parent_node`), and for a
  `merge` the `recommended_shape` as your suggested shape;
- if the `consolidate` return carried «موارد کم‌اهمیت‌تر» notes, a «— موارد کم‌اهمیت‌تر —»
  heading with **one brief line per case** (these stay short), labelled with Persian letters
  **الف، ب، پ، ت…** (never digits) — so the less-important list is visually distinct from the
  numbered (۱، ۲، ۳…) main list;
- the output path `{run_dir}/consolidation.json` and a note that **no process file has
  changed yet**;
- the closing question: which item to apply (and, for a merge, **flat** or
  **mother+subprocess** — state your recommendation).

Then Wait. If the user asks to pursue a «کم‌اهمیت‌تر» item, re-dispatch `consolidate`
(`mode: review`); it re-evaluates and either emits that case as a full suggestion to apply
via 10d, or explains why it still cannot be cited.

**10d — Apply one approved item (repeat until the user is done).** For the chosen item:

1. **Staleness guard.** Re-read every process id the item references. If any is now
   tombstoned/missing (an earlier applied item changed it), re-dispatch `consolidate`
   (`mode: review`) to regenerate `consolidation.json`, re-present, and restart 10d.
2. **Record the choice.** For a merge, set the item's `chosen_shape` in
   `consolidation.json` (Write). Set `status: "approved"`.
3. **Run the structural verb:**
   - **merge:** build the heir with the **hardened `extract` path** — never an ad-hoc `Agent`
     dispatch (that stalls the SDK bridge, ADRs 0002–0007). Dispatch **one**
     `Task: extract  mode: restructure  existing_process_paths: [<each member's process.json>]  evidence: [<union of the members' evidence from consolidation.json>]  transcript_paths: [<every transcript in the set>]  attachment_texts: {attachment_texts}  chosen_shape: <flat|mother_subprocess>  seq: 01  run_dir: {run_dir}  data_root: <data-repo>`.
     It writes a heir candidate to `{run_dir}/candidates/01.json`. **Assemble** the restructure
     plan `{department, heirs: [{candidate: <that candidate>, supersedes: <members>, subprocess_links: <from the candidate>}]}` —
     `supersedes` = **all** members for `flat`, or the **non-child** members for
     `mother_subprocess` (a member id is in `supersedes` **or** `subprocess_links.child`, never
     both). Write it to `{run_dir}/restructure.consolidation.json`,
     `Bash: validate restructure {run_dir}/restructure.consolidation.json`, then
     `Bash: DATA_ROOT=<data-repo> merge restructure --plan {run_dir}/restructure.consolidation.json --run {run_dir}`.
     Capture the printed `heir <id>` and `tombstoned <id>` lines.
   - **attach:** `Bash: DATA_ROOT=<data-repo> merge attach-subprocess --parent-process {parent_process} --node {parent_node} --child {child} --run {run_dir}`.
4. **Soundness pass (§4.7).** Dispatch `Task: consolidate  mode: apply  item: <the item, plus the new `heir <id>` captured in step 3 for a merge (or the `parent_process`+`child` for an attach)>  …` — so it verifies the **heir**, not the now-tombstoned member ids in `item.processes`. For the seam check: for each returned delta, Write it, `Bash: validate delta <path>`, then `Bash: DATA_ROOT=<data-repo> merge update --process <pid> --delta <path> --run {run_dir}`. Append the returned repair records to the item's `repairs[]` in `consolidation.json`.
5. **Mark applied + commit.** Set the item's `status: "applied"` in `consolidation.json`.
   `Bash: git -C <data-repo> add departments runs && git -C <data-repo> commit -m "consolidate({department}): item {n} — {merge|attach}"`. (Stage only `departments`/`runs` — never `git add -A`, which would sweep in unrelated `.claude`/config edits.)
6. **Show the result.** Present the finished process(es) to the user in Persian — the
   heir/parent id and its node flow (labels in order) — so they see the completed
   outcome. Then return to 10c for the next item, or finish if the user is done.

---

## Summary of stage ordering

| Stage | Name | Tool/CLI | Pauses? |
|-------|------|----------|---------|
| 0 | Resolve state / resume | Read meta.json | — |
| — | Resolve the set (dept glob or explicit list) | Glob | — |
| **A** | **Set-confirmation checkpoint** | Telegram message | **STOP** |
| 1 | Transcribe-missing reconcile (idempotent; per-file verbatim gate) | `Bash: transcribe` × missing | — |
| 2 | Init / finalise run record | Write meta.json | — |
| 3 | classify over the set | `Task: classify` | — |
| **B** | **Segmentation / restructure checkpoint** | Telegram message | **STOP** |
| 5a | prepare attachments | `Bash: extract-attachment` | — |
| 5 | extract per desired process (**batches of ≤4**) | `Task: extract` × N (≤4/msg) | — |
| 6 | merge (`new`/`update`/`restructure`/`attach-subprocess`/`remove`) | `Bash: merge …` | — |
| 7 | summarize over the set | `Task: summarize` | — |
| 8 | Finish + commit | Write meta.json, `git -C` | — |
| 9 | Conflict + restructure-lineage report | `Bash: merge accept/reject` | — |
| 10 | consolidation review (STOP) | `Task: consolidate` + `merge restructure`/`attach-subprocess`/`update` | user approves each item |

**Key invariants:**
- `merge` is the ONLY writer of `departments/**/processes/*.json` (hook-enforced); `restructure`,
  `attach-subprocess`, `remove` are engine verbs — never hand-edit process files.
- The run reads **all** transcripts in full (spec §4.1); no distillation, no per-voice/batch mode,
  no conservative-subset mode. A set of one is the smallest case.
- **Gate A and Gate B are the only mid-run pauses**, and **Stage 10's per-item gates** (10c report,
  10d step 6 show-result) are the post-run pauses. Everywhere else, continue in the same turn — a
  returning `Task`/CLI (including each `consolidate` dispatch) is never a stopping point. Never send a
  prose-only message between stages (a message with no tool call ends the turn — the #1 stall);
  status text rides with the next call.
- Stage-0 resume re-enters at **Gate A** (`segments.json` absent) or **Gate B** (`segments.json`
  present, `processes[]` empty).
- **Extract runs in bounded parallel** — dispatch at most 4 `extract` `Task`s per message, await the
  batch, then the next; never more than 4 in one message (ADR 0011 — full N-way fan-out is dropped by
  the SDK bridge; batches of 4 are proven safe under patches 0004/env).
- Tombstoned processes stay on disk, are excluded from classify matching, and are shown labelled in
  the UI (INV-4 — never deleted here; only user-initiated UI delete removes one).
- `{run_dir}/meta.json` with `finished_at: null` always signals a resumable in-progress run. All
  timestamps are ISO-8601 with `Z` suffix.

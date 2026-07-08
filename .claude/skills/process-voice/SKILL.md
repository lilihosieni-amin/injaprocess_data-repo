---
name: process-voice
description: Orchestrate the full voice→IDEF pipeline — transcribe, classify, human checkpoint, extract, merge, summarize, commit, and the end-of-run conflict report. Resumes from {run_dir}/meta.json.
---

# process-voice playbook

**Invocation:** `/process-voice <voice>` where `<voice>` is the audio basename (e.g. `dining-2026-05-06`).

All file paths are relative to `<data-repo>` (the value of `DATA_ROOT`).
Every engine CLI must be called with `DATA_ROOT=<data-repo>` set in the environment.

---

## Stage 0 — Resolve state / resume

1. Check whether `runs/{voice}/meta.json` exists.
2. If it exists AND `finished_at` is `null`, the previous run was interrupted — set `{run_dir}` to `runs/{voice}` and resume it: inspect `processes[]` to determine how far it got (empty + `{run_dir}/segments.json` present → resume at Stage 4; non-empty → resume at Stage 6 for any unmerged segment, then Stages 7–9). Do NOT re-run stages that already completed (idempotency).
3. If `runs/{voice}/meta.json` does not exist, this is a fresh run — set `{run_dir}` to `runs/{voice}` and continue to Stage 1.
4. If `runs/{voice}/meta.json` exists with a non-null `finished_at` (or the user explicitly requests re-processing), this is a re-run — set `{run_dir}` to `runs/{voice}/attempt-NN/` where `NN` is zero-padded and is the lowest integer ≥ 2 whose directory does not yet exist. Continue to Stage 1.

> `{run_dir}` is the single run-scoped directory used for all artefacts in this run (meta.json, segments.json, candidates/, deltas/). The transcript at `meetings/transcripts/{voice}.txt` is shared across attempts and is never run-relative.

---

## Stage 1 — Locate + transcribe (FR-P1, FR-P2)

1. Glob `meetings/audio/{voice}.*`. If no file matches, list the three closest filenames and ask the user conversationally which one to use. Stop until they reply.
2. Run the transcription CLI (idempotent — skips Vertex AI if `meetings/transcripts/{voice}.txt` already exists):
   ```
   Bash: DATA_ROOT=<data-repo> transcribe {voice}
   ```
3. On a **fresh transcription** (the transcript file did not exist before):
   - Read stdout. Strip any Gemini preamble, postamble, or section headings injected by the model.
   - If the text appears summarized or rewritten (rather than verbatim speech), flag it to the user and STOP. Do not proceed. When stopping, tell the user (in Persian) their options: «(الف) پردازش را دوباره اجرا کنید تا رونویسی از نو انجام شود؛ یا (ب) یک رونویسِ اصلاح‌شده را به‌صورت دستی در `meetings/transcripts/{voice}.txt` قرار دهید و دوباره اجرا کنید — در این حالت خط لوله به‌دلیل ایدمپوتنسی از Vertex عبور می‌کند و همان فایل شما را استفاده می‌کند.»
   - Write the cleaned text to `meetings/transcripts/{voice}.txt`.
4. Confirm the transcript exists before continuing.

---

## Stage 2 — Init run record

1. `{run_dir}` was determined in Stage 0; create the directory now if it does not exist.
2. Write `{run_dir}/meta.json` with exactly the shape below
   (always write `finished_at` explicitly — even as `null` — because Stage 0 resume depends on reading this field):
   ```json
   {
     "voice": "<voice>",
     "departments": ["<tag>"],
     "started_at": "<ISO-8601 Z timestamp>",
     "finished_at": null,
     "attempt": 1,
     "processes": []
   }
   ```
   - `departments`: the upload tag(s) extracted from the voice filename or provided by the user.
   - `started_at` / `finished_at`: ISO-8601 with `Z` suffix (e.g. `2026-05-06T09:14:00Z`).
   - `attempt`: the integer taken from Stage 0's `{run_dir}` — `1` for the base run `runs/{voice}/`, or `NN` when `{run_dir}` is `runs/{voice}/attempt-NN/`. (The example above shows the base-run value `1`.)
   - `processes`: start empty; populated after merge in Stage 6.
3. **Validate the record:** `Bash: validate run-meta {run_dir}/meta.json`. If it exits non-zero, fix the meta object you just wrote (the stderr message names the offending field) and re-validate before continuing.

---

## Stage 3 — classify

Dispatch the `classify` agent via the `Task` tool:

```
Task: classify
  transcript_path: meetings/transcripts/{voice}.txt
  voice: {voice}
  tagged_departments: [<tagged departments>]
```

Wait for the task to complete. It writes `{run_dir}/segments.json`.
The segments file categorises every identified process as one of: `new`, `update`, or `unchanged`.

**Validate it:** `Bash: validate segments {run_dir}/segments.json`. If it exits non-zero, re-dispatch the `classify` agent with the stderr error appended to its prompt so it corrects the output, then re-validate. After 2 failed attempts, stop and report the error to the user instead of looping.

---

## Stage 4 — Human checkpoint (FR-P4)

1. Read `{run_dir}/segments.json`.
2. Group segments into three categories:
   - **الف) جدید** — processes classified as `new` (no existing ID).
   - **ب) به‌روزرسانی** — processes classified as `update`, formatted as `«{process_name}» → {existing_id}`.
   - **ج) بدون تغییر** — processes classified as `unchanged`, formatted as `{process_name} → {existing_id}`.
3. Collect any flagged sub-process candidates and any org-overview note from the `classify` agent's Stage-3 return message (delivered to the orchestrator at the end of Stage 3). These fields are NOT in `segments.json` (which is `additionalProperties: false` and carries no sub-process field) — they are only in the classify agent's completion message. If Stage 4 is re-entered on a later turn (via Stage 0 resume) and the classify return message is no longer in context, re-dispatch the `classify` agent to regenerate its summary before composing the checkpoint (classify is idempotent and cheap; it will re-produce the same segments and notes).
4. Note any departments mentioned in the transcript that differ from the upload tag (this information comes from `segments.json`).
5. Compose the checkpoint message in Persian and send it to the user in Telegram.

**Example checkpoint message (reproduce this format exactly):**

```
فرایندهای شناسایی‌شده از صدای dining-2026-05-06:
الف) جدید:
  ۱. فرایند انبارداری (warehouse)
  ۲. فرایند سفارش‌گیری سالن (dining)
ب) به‌روزرسانی:
  — «فرایند پخت» → cooking-002
ج) بدون تغییر:
  — کنترل موجودی → warehouse-003
⚠ این صدا با برچسب «dining» بود ولی به warehouse و cooking هم مربوط شد.
تأیید می‌کنید یا اصلاحی لازم است؟
```

6. **End your turn and wait.** Do NOT proceed to Stage 5 in the same turn.
   The session is paused here. `{run_dir}/meta.json` has `finished_at: null` and `processes: []`.
   When the user replies in the next turn, read `{run_dir}/meta.json` to resume (Stage 0 re-entry will route here).

**Handling the user's reply:**

- **Correction** (missed process, wrong split/merge, move `unchanged`→`update`, incorrect ID):
  - Re-dispatch only the `classify` agent with the corrected instructions.
  - Do NOT touch any department process file — nothing has been written yet.
  - For a single-segment override (e.g. user corrects one extract), re-dispatch only that one `extract` task.
  - Re-present the checkpoint message with the updated segments. End your turn and wait again.
- **Unchanged→update override** (user says an `unchanged` item actually has new detail): reclassify ONLY that segment as `update` (edit `segments.json` accordingly, or re-dispatch `classify` with that instruction), re-present the checkpoint, and on confirmation include that segment in Stage 5 extraction. Do not re-run the whole pipeline.
- **Confirmation** (user says "تأیید" / "بله" / "ok" / equivalent):
  - Proceed to Stage 5.

---

## Stages 5–9 — Per-department fan-out (FR-P8)

Collect the full set of departments touched by the confirmed segments.
For each department, run the following sub-pipeline independently (Stages 5–8).
Stage 9 (conflict report) runs once after all departments complete.

---

### Stage 5 — extract (parallel)

For each segment classified as `new` or `update`, dispatch an `extract` task via the `Task` tool.
Run ALL dispatches in parallel (do not wait for each before starting the next).

- **new segment:**
  ```
  Task: extract
    voice: {voice}
    transcript_path: meetings/transcripts/{voice}.txt
    mode: new
    seq: {seq}           # sequential integer within this run, zero-padded e.g. 01
    department: {dept}
    run_dir: {run_dir}
  ```
  The agent writes `{run_dir}/candidates/{seq}.json`.

- **update segment:**
  ```
  Task: extract
    voice: {voice}
    transcript_path: meetings/transcripts/{voice}.txt
    mode: update
    existing_id: {existing_id}
    existing_process_path: departments/{dept}/processes/{existing_id}.json
    department: {dept}
    run_dir: {run_dir}
  ```
  The agent writes `{run_dir}/deltas/{existing_id}.json`.

**unchanged segments are NOT extracted.** Their `process.json` files remain untouched.
They will be recorded in `meta.json.processes` as `{id, status: "unchanged"}` in Stage 8.

Wait for all parallel extract tasks to finish before proceeding to Stage 6.

---

### Stage 6 — merge (deterministic, per department)

Process each candidate/delta using the `merge` engine CLI.
Never write `departments/**/processes/*.json` any other way — this is hook-enforced.

**For each `new` candidate:**
```
Bash: DATA_ROOT=<data-repo> merge new \
  --candidate {run_dir}/candidates/{seq}.json \
  --department {dept} \
  --run {run_dir}
```
Capture the printed `<id>` (e.g. `warehouse-004`). Record `{id, status: "new"}` for meta.json.

**For each `update` delta:**
```
Bash: DATA_ROOT=<data-repo> merge update \
  --process {existing_id} \
  --delta {run_dir}/deltas/{existing_id}.json \
  --run {run_dir}
```
Record `{existing_id, status: "update"}` for meta.json.

**What merge does when a candidate/delta contains sub-processes:**
For each entry in `subprocesses` (candidate) or `add_subprocesses` (delta), `merge` performs these 7 steps automatically:
1. Resolves the parent activity's real node ID from the newly-merged or existing `process.json`.
2. Allocates the child process ID via `allocate-id` CLI (INV-1 — never by an LLM).
3. Writes `departments/{dept}/processes/{child-id}.json` with `parent: {process: "<parent-id>", node: "<parent-node-id>"}` and `source.type: "auto"`.
4. Sets the parent node's `subprocess` field to the child process ID.
5. Syncs the parent box's `icom` to equal the child's `idef0` (child wins on conflict).
6. Lays out the child process (serpentine layout).
7. Prints `subprocess <child-id> node <parent-node-id>` to stdout.

**Capture the printed child IDs:** parse every `subprocess <child-id> node <parent-node-id>` line from merge stdout. Collect these pairs for use in Stage 8.

**Layout:** `merge` also computes/updates node positions (serpentine layout) for new nodes; manually positioned nodes (`layout: manual`) are never moved. Never set node positions yourself — the layout is deterministic engine work, not LLM work.

---

### Stage 7 — summarize (per department)

For each department touched in Stage 6, dispatch a `summarize` task:
```
Task: summarize
  department: {dept}
  data_root: <data-repo>
```
Wait for completion. It writes/updates `departments/{dept}/overview.json`.

**Validate it:** `Bash: validate overview departments/{dept}/overview.json`. On non-zero exit, re-dispatch `summarize` for that department with the stderr error so it corrects the file, then re-validate (max 2 attempts, then report to the user).

---

### Stage 8 — Finish run + commit (per department)

1. Update `{run_dir}/meta.json`:
   - Set `finished_at` to the current ISO-8601 Z timestamp.
   - Populate `processes[]` with all entries from Stages 5–6:
     - new merges: `{id: "<dept>-NNN", status: "new"}`
     - update merges: `{id: "<existing_id>", status: "update"}`
     - unchanged segments: `{id: "<existing_id>", status: "unchanged"}`
     - auto-created sub-processes (captured from merge stdout in Stage 6): `{id: "<child-id>", status: "new", auto_subprocess_of: "<parent-id>"}`
   - After updating, re-validate: `Bash: validate run-meta {run_dir}/meta.json` (fix and re-validate on failure) so a malformed record is never committed.

2. Commit the run artefacts:
   ```
   Bash: git -C <data-repo> add -A && \
         git -C <data-repo> commit -m "pipeline({dept}): {N} processes from {voice}"
   ```
   Where `{N}` is the count of new + updated processes (not unchanged) for that department.

   For multiple departments, either commit once per department or include all in one commit message listing each department:
   ```
   pipeline(warehouse+cooking): 3 processes from dining-2026-05-06
   ```

---

### Stage 9 — Conflict report + auto-subprocess summary (FR-M4)

After all departments have been committed:

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
  منبع: {voice}

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

5. If there are no conflicts (`pending[]` is empty for all written processes), report completion:
   ```
   پایان موفق اجرا. فرایندهای {voice} پردازش و ثبت شدند.
   ```

---

## Summary of stage ordering

| Stage | Name | Tool/CLI | Per-dept? |
|-------|------|----------|-----------|
| 0 | Resolve state / resume | Read meta.json | — |
| 1 | Locate + transcribe | `Bash: transcribe` | — |
| 2 | Init run record | Write meta.json | — |
| 3 | classify | `Task: classify` | — |
| 4 | Human checkpoint | Telegram message | — |
| 5 | extract (parallel) | `Task: extract` × N | yes |
| 6 | merge | `Bash: merge new/update` | yes |
| 7 | summarize | `Task: summarize` | yes |
| 8 | Finish + commit | Write meta.json, `git -C` | yes |
| 9 | Conflict report | `Bash: merge accept/reject` | — (once) |

**Key invariants:**
- `merge` is the ONLY writer of `departments/**/processes/*.json` (ARD hook-enforced).
- `unchanged` processes are never re-extracted or re-merged; only recorded in meta.json.
- The checkpoint turn ends the session turn — extract never runs in the same turn as classify.
- `{run_dir}/meta.json` with `finished_at: null` always signals a resumable in-progress run.
- All timestamps are ISO-8601 with `Z` suffix.

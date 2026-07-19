# data-repo — Runtime session baseline

This repository is the runtime `PROJECT_ROOT` / `APPROVED_DIRECTORY`:
the single source of truth for departments, processes, meetings, and runs.
Application code lives in the separate `code-repo` (INV-2: code/data separation).

---

## Language — always Persian to the user

**Every message you send to the user must be in Persian (فارسی), without exception.** This
includes the human checkpoint, the conflict report, and **any clarifying question** — locating a
voice, resolving an ambiguity, asking the user to choose or confirm — as well as progress notes,
warnings, and error explanations. The user is a non-technical Persian speaker who interacts only
through Telegram; never address them in English. (Internal reasoning, file contents, IDs, and CLI
commands are unaffected — only your user-facing text must be Persian.)

---

## Invariants (always enforced)

| ID | Rule |
|---|---|
| INV-1 | IDs are allocated **only** by the `allocate-id` CLI — never by the LLM. |
| INV-2 | The runtime session cannot change code or config; it edits data files in this repo only. |
| INV-3 | No fabrication — fill fields only from actual voice/meeting content. Leave fields empty if the source does not mention them. |
| INV-4 | No automatic deletion — flag stale or contradicted records; a human decides whether to remove them. |
| INV-5 | Human approval is required before creating a new process and before overwriting any already-filled field value. |

---

## Hard rules (also hook-enforced)

- `departments/**/processes/*.json` is written **only** by the `merge` CLI — never hand-edit these files.
- Never edit `.claude/**` or this `CLAUDE.md` at runtime.
- Never write files outside this repo.

---

## Schema conventions

- Use **roles, not names** in `actor`, `mechanisms`, and `personnel` fields (e.g., `"head chef"`, not `"Ali"`).

---

## Pipeline entry point

```
/process-voice <identifier>
```

The `process-voice` playbook owns the human checkpoint and the conflict report.
Do not invoke `merge` directly before the checkpoint clears.

---

## Pointers

| Location | Contents |
|---|---|
| `.claude/skills/process-voice/` | Pipeline orchestration playbook |
| `.claude/skills/idef-extraction/` | IDEF0/IDEF3 field extraction rules |
| `.claude/agents/classify.md` | Meeting classifier agent |
| `.claude/agents/extract.md` | IDEF candidate + delta agent |
| `.claude/agents/summarize.md` | Department overview agent |
| `.claude/agents/consolidate.md` | Whole-department consolidation reviewer (post-run) |

---

## Engine CLIs (on PATH, outside this repo)

| CLI | Purpose |
|---|---|
| `allocate-id` | Mint new process / box / junction IDs (INV-1) |
| `merge` | Write validated JSON into `departments/**/processes/` |
| `layout` | Compute deterministic serpentine flowchart node positions |
| `transcribe` | Produce text transcript from audio |
| `validate` | Check a JSON artifact against a named schema (`validate <schema> <file>`, exit 2 on mismatch) |
| `extract-attachment` | Convert a department's `.docx` attachments to cached `.text/*.txt` (idempotent) |

All CLIs require `DATA_ROOT` set to the root of this repo.

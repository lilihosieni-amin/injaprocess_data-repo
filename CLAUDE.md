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
through Telegram; never address them in English. Internal reasoning and file contents are
unaffected — only your user-facing text must be Persian.

**No internal artefact ever appears in a message to the user.** File paths, field paths
(`data/expr`), account ids (`a1f0c3d9`), run directories, department codes (`cooking`) and CLI
commands are yours, not theirs: the user has the panel and Telegram, and no access to this
repository. In particular, **never print a command for the user to run** — offer lettered or
numbered choices, wait for their answer, and run the command yourself. Name a thing the way the
panel names it: its Persian title («آشپزخانه», «مصرف اعلامی»), or the entry id the panel's own
«شناسه» column shows (`F-00040`, `cooking-001`).

Exactly three things stay in English: an attachment's own file name, an entry id the panel
displays, and the words **csv**, **Excel** and **sheet** — write those as they are. Never
translate them to «صفحات گسترده»; the user does not recognise it.

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
- `departments/**/order.json` is written **only** by the `order` CLI — never hand-edit it. It holds
  the department's human-curated process order; read it when you need to know the sequence, but the
  `merge` CLI keeps it in sync by itself, so there is nothing for you to do. Never run `order set`
  or `order move` either — those two verbs *choose* the order, which is the user's job in the UI;
  the hook blocks them.
- `facts/**` is written **only** by the `merge facts` CLI — the agent writes only
  `runs/facts/{dept}/{stamp}/facts-delta.json` and `runs/facts/{dept}/{stamp}/facts-patch.json`.
- Never edit `.claude/**` or this `CLAUDE.md` at runtime.
- Never write files outside this repo.

---

## Schema conventions

- Use **roles, not names** in `actor`, `mechanisms`, `personnel`, `speaker_role`, `filled_by`,
  `approved_by`, `by`, and `signatures[].role` fields (e.g., `"head chef"`, not `"Ali"`).

---

## Facts conventions

- Facts are **definitions, not observations**: what a column means, its unit, who fills it in,
  when, and how it is computed — never a number that changes every night (QF-1).
- The store is **global**, one file per kind; department is a scope tag, not a partition, and
  `merge facts` is the only writer (QF-2).
- Write rules **never overwrite**: a later run's different value does not replace the existing
  one — it opens a disagreement as an account on the field, for a human to resolve (QF-17).
- **No Persian keys** — every fact, record column, and keyed structure carries an ASCII `key`;
  Persian lives only in `title`, `statement`, `description`, and the other prose fields (QF-32).

---

## Pipeline entry point

```
/process-voice <identifier>
/quantify [department]
/edit-fact <instruction>
```

The `process-voice` playbook owns the human checkpoint and the conflict report.
Do not invoke `merge` directly before the checkpoint clears.

`/quantify` runs a facts pass over the estate — dumped workbooks, the
manifest, and any recordings the user names — and owns the manifest and facts
checkpoints. `/edit-fact` applies one chat-driven correction to a single fact
(e.g. «پارمسان الان ۱۰۰ گرمه»). Neither writes `facts/**` directly; both
dispatch the `quantify` agent and invoke `merge facts`.

---

## Pointers

| Location | Contents |
|---|---|
| `.claude/skills/process-voice/` | Pipeline orchestration playbook |
| `.claude/skills/idef-extraction/` | IDEF0/IDEF3 field extraction rules |
| `.claude/skills/edit-process/` | Chat-driven direct edits (no voice) → the `merge` verbs; merge/split heirs are built by `extract` (Mode C) |
| `.claude/skills/quantify/` | Facts pipeline orchestration playbook v3 — the planner packs the estate into units, the units run four at a time, one reviewer reads the assembled result |
| `.claude/skills/edit-fact/` | Chat-driven direct edit to one fact (no recording) → `merge facts edit` for a change, `apply` for an addition, `retire` for a retirement; mirrors `edit-process` |
| `.claude/agents/classify.md` | Meeting classifier agent |
| `.claude/agents/extract.md` | IDEF candidate + delta agent — **and the sole builder of restructure/merge heirs** (Mode C), for the pipeline, `consolidate`, and `edit-process` |
| `.claude/agents/summarize.md` | Department overview agent |
| `.claude/agents/consolidate.md` | Whole-department consolidation **reviewer + soundness** (post-run) — proposes merges/attaches and verifies the applied result; the heir itself is built by `extract` |
| `.claude/agents/quantify.md` | Quantitative-facts agent (modes `unit`, `review`, `manifest`, `targeted`) — decides one prepared unit; reads two files and writes one; never reads a dump, a transcript or the store |

---

## Engine CLIs (on PATH, outside this repo)

| CLI | Purpose |
|---|---|
| `allocate-id` | Mint new process / box / junction IDs (INV-1) |
| `merge` | Write validated JSON into `departments/**/processes/` |
| `order` | Read a department's curated process order: `order show <dept>`, `order sync <dept>`, `order check <dept>`. The curating verbs `set` and `move` are **hook-blocked** — the user reorders in the UI (§4.6) |
| `layout` | Compute deterministic serpentine flowchart node positions |
| `transcribe` | Produce text transcript from audio |
| `validate` | Check a JSON artifact against a named schema (`validate <schema> <file>`, exit 2 on mismatch) |
| `extract-attachment` | Convert a department's `.docx` attachments to cached `.text/*.txt` (idempotent) |
| `facts-plan` | Plan and assemble a facts run: `facts-plan build <dept> --run R --recordings a,b`, `status --run R [--new-turn]`, `digest --run R`, `assemble --run R [--review]`, `report --run R` |

All CLIs require `DATA_ROOT` set to the root of this repo.

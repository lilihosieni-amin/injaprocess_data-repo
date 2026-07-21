---
name: edit-process
description: Apply a direct conversational edit to committed process work with NO voice/transcript — read the target process.json, build the matching engine artifact, confirm destructive ops, run the matching merge verb (the sole writer), and commit with source.type "chat". Reuses the pipeline's engine op set (§4.12).
---

# edit-process playbook

**Invocation:** the user, in chat, instructs a targeted edit of committed work with **no recording
processed** — e.g. «برچسب گره X را در فرایند Y عوض کن», «بعد از مرحلهٔ Z یک مرحله اضافه کن», «آن یال
را حذف کن», «این دو فرایند را ادغام کن», «این فرایند را حذف کن».

This reuses the **entire engine op set** built for the pipeline. It **never writes `process.json`
directly** — every change goes through `merge` (the sole writer, hook-enforced), so INV-1/INV-3/INV-4
all still hold. The only differences from a pipeline run are the input (a chat instruction, not
transcripts) and the absence of the read-all/segment phase (a targeted edit needs neither).

All paths are relative to `<data-repo>` (`DATA_ROOT`). Every engine CLI runs with
`DATA_ROOT=<data-repo>` set.

## Step 1 — Identify the target and read it (read-only)

1. Resolve the target process id(s) from the instruction (ask the user in Persian if ambiguous —
   e.g. list candidate processes by name and id).
2. **Read** each target `departments/{dept}/processes/{id}.json` (read-only) to obtain its **real
   node ids**. You will copy those ids verbatim into the artifact; never invent an id (INV-1). Do
   not match against **tombstoned** processes (`tombstoned: true` / non-empty `superseded_by`).

## Step 2 — Build the matching engine artifact

Choose the artifact by the kind of edit (see the `idef-extraction` skill §5/§8 for exact shapes):

- **Field / label change** → a `delta` with `revise_nodes: [{id, set:{…}}]` (overwrite) — or
  `enrich_nodes` if the field is empty.
- **Insert a step** → a `delta` with `add_nodes` (temp keys `n1`, …) + `add_edges`, and — for **edge
  hygiene** — `remove_edges` for the edge the new node makes redundant.
- **Remove an edge** → a `delta` with `remove_edges: [{from, to}]` (real ids).
- **Drop a node** → a `delta` with `flag_removed: [{id}]` (the engine sets `removed:true`; never
  deletes — INV-4).
- **Merge / split** → a `merge restructure` plan — but **do not build the heir candidate
  inline**. Dispatch **`Task: extract  mode: restructure`** with the members'
  `existing_process_paths`, the department's `transcript_paths`, `attachment_texts`, and (for a
  merge) the user's `chosen_shape` (`flat`|`mother_subprocess`); it builds a fresh,
  **timeline-ordered, coverage-complete** heir candidate (`extract.md` Mode C — the same hardened
  builder the pipeline uses, so a chat merge is ordered and duplicate-free too, and it never
  improvises an `Agent` dispatch that stalls the SDK bridge). Then assemble the plan
  `{department, heirs:[{candidate:<from extract>, supersedes:[…], subprocess_links:[…]}]}` (a
  member id is in `supersedes` **or** `subprocess_links.child`, never both) and run
  `merge restructure`.
- **Re-parent an existing process under a node** → `merge attach-subprocess`.
- **Delete / retire a process** → `merge remove` (tombstone, never a hard delete).

Write any `delta`/`candidate`/`plan` artifact to a scratch path under `runs/chat/{stamp}/`.

## Step 3 — Confirm proportionally (the analogue of Gate B)

- A **simple, non-destructive** edit (a field change, adding a node/edge) executes **directly** — no
  confirmation pause.
- A **destructive/structural** edit (delete/tombstone, merge, split, attach) shows a **one-line
  Persian confirmation first** and waits for the user's «تأیید». This is the proportional analogue
  of Gate B — destructive-op confirmation, scaled to a single edit.

## Step 4 — Run the matching `merge` verb (the sole writer)

Run exactly the verb matching the artifact, with `--run runs/chat/{stamp}`:

```
Bash: DATA_ROOT=<data-repo> merge update --process {id} --delta {delta} --run runs/chat/{stamp}
Bash: DATA_ROOT=<data-repo> merge restructure --plan {plan} --run runs/chat/{stamp}
Bash: DATA_ROOT=<data-repo> merge attach-subprocess --parent-process {P} --node {N} --child {C} --run runs/chat/{stamp}
Bash: DATA_ROOT=<data-repo> merge remove --process {id} --run runs/chat/{stamp}
```

`merge` applies the change, re-layouts, and **preserves all ids and prior manual edits**. The run
carries `source.type: "chat"` provenance (the engine sets `source`/`touched_by`; the agent never
sets provenance — INV-1).

## Step 5 — Commit to git

Every mutation to committed data ends in a commit — nothing is left uncommitted. Commit with a clear
message keyed to the edit:

```
Bash: git -C <data-repo> add departments runs && \
      git -C <data-repo> commit -m "chat-edit({id}): <one-line Persian/English summary of the change>"
```

The deploy `git-push` cron pushes it, exactly like a pipeline commit. Confirm the working tree is
clean afterward (`git -C <data-repo> status --porcelain` prints nothing).

## Step 6 — Report

Reply in Persian with what changed (the process id, the node/edge/label affected, and — for a
destructive op — that the original was tombstoned/flagged, not deleted). Do not paste the full
`process.json`.

## Invariants

- **`merge` is the sole writer** — never edit `process.json` directly (hook-enforced).
- **INV-1** — ids are engine-minted; copy committed ids verbatim, use temp keys for new nodes, never
  set `source`/`superseded_by`/`position`/`layout`.
- **INV-3** — no fabrication: model only what the user actually instructed.
- **INV-4** — never delete/lose: node drops are `flag_removed`; process removals are `merge remove`
  (tombstone). The only hard delete is user-initiated in the UI.
- **Provenance** — the resulting change is `source.type: "chat"`; Claude commits it.

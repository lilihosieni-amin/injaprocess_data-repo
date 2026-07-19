---
name: idef-extraction
description: IDEF0/IDEF3 extraction knowledge — the candidate/delta output contract, the no-fabrication rule (INV-3), and roles-not-names (ARD §4.4). Preloaded by the extract agent.
---

# IDEF Extraction Knowledge

This skill is **preloaded into the `extract` agent**. It defines:

1. The IDEF0/IDEF3 modelling concepts the agent must apply,
2. The exact JSON output contract (`candidate.json` for new processes; `delta.json` for updates),
3. Inviolable rules: no fabrication (INV-3), temporary keys only (INV-1), roles not names (ARD §4.4).

All `label`, `description`, `summary`, `actor`, and ICOM string values the agent writes **must be in Persian**, matching the language of the source voice/document.

---

## 1. IDEF0 / ICOM

IDEF0 models a process as a **function box** that transforms inputs into outputs, governed by controls, using mechanisms.

| ICOM letter | JSON key | Persian term | Meaning |
|---|---|---|---|
| I | `inputs` | ورودی / مصرف‌شونده | What is consumed or transformed by the activity. A raw ingredient, a document, a request. |
| C | `controls` | قید / قاعده | Rules, standards, recipes, or regulations that govern **how** the activity runs without being consumed. |
| O | `outputs` | خروجی | What the activity produces or delivers. |
| M | `mechanisms` | منبع / نقش انجام‌دهنده | The role, system, or resource that **performs** the activity — e.g. «کارپرداز»، «سیستم انبارداری». |

**Critical rule — roles not names (ARD §4.4):** `mechanisms` items and each activity's `actor` field **must be a role or system label**, never a personal name or individual employee. Write «گارسون» not «علی رضایی». Write «سرآشپز» not «خانم محمدی».

The process-level `idef0` object and each activity node's `icom` object both use these four arrays exactly:

```json
{
  "inputs": [],
  "controls": [],
  "outputs": [],
  "mechanisms": []
}
```

Any or all arrays may be empty when the transcript does not supply the information.

---

## 2. IDEF3 — Activities, Edges, and Junctions

IDEF3 describes the **sequence** (flow) of activities, including branching and merging logic.

### Activities (boxes)

An activity is a named step in the process — a unit of work performed by a role. Each activity has:
- A `label` — a self-sufficient Persian title (see "What goes in the flow" below; length is not a constraint)
- A `description` (Persian) carrying only supporting detail ABOUT the step — never an action
- An `actor` (Persian role name)
- Its own `icom` object (the ICOM at this step's level)
- A `subprocess` pointer (`null` in the candidate; merge sets it after allocating the child ID — see §7)

### What goes in the flow — nodes, titles, and descriptions

The flowchart must be fully readable from node titles alone. A reader must never need to
open a node's detail view to understand a step, and must never need to read a description
to discover that an action exists. Content is lost two ways, both forbidden: **compression**
(shrinking a real action into a short, vague label) and **demotion** (writing a real action
into the description instead of the flow).

**The node test — "does someone DO this?"** For every piece of extracted content, ask: is
there an actor (a person, role, or unit) performing an action, and does something change
state / move the process forward?
- YES → it is a STEP: emit it as its own activity node in the flow.
- NO → it is supporting DESCRIPTION on an existing node.

MUST be a node: any action performed by a person or role; any decision or check that
branches the flow (model it as a junction — see "Control-flow completeness" below); any
handoff between people, roles, or units; any action whose omission would leave a gap in the
sequence.

MUST NOT be a node (it is description): HOW an action is carried out (technique/tools/
systems); constraints, timings, thresholds, quality standards; exceptions and edge cases
attached to an existing step; background and rationale. The `description` field is for
detail ABOUT the steps — it is NOT a container for content that did not fit the flow. If
you are about to write an actor plus a verb-of-doing into a description, stop: that is a
node you failed to create.

**Titles are self-sufficient; length is not a constraint.** The `label` must state the
essential substance of the step. Never compress a step into a vague category label. A
longer label, up to a full Persian sentence, is acceptable; never drop substantive content
to make a title shorter. Completeness beats brevity.

**One action per node (the splitting rule).** If a faithful account of a step contains two
different actions a person performs, split them into two sequential nodes — do not put them
in one box. The test: if the title needs «و» ("and") to join two things a person actually
DOES, it is two nodes. Splitting is the preferred outcome because it guarantees nothing is
dropped.
  - WRONG (compressed, drops half): «ثبت سفارش دستی توسط سرپرست»
  - WRONG (complete but two actions in one box): «ثبت سفارش دستی توسط سرپرست و هماهنگی با صندوق جهت ثبت سفارش»
  - CORRECT (two nodes, complete): «ثبت سفارش دستی توسط سرپرست» → «هماهنگی با صندوق جهت ثبت سفارش»

**Default to a node when unsure; never silently drop.** If you cannot tell whether
something is a step or a description, make it a step — an over-detailed flow is fixed by
the reviewer in seconds, but an action buried in prose or behind a vague label is invisible
and will be missed. If material does not fit the current node, that is a signal to create
another node, never to shorten, generalize, or demote it.

**One node per task.** Represent each distinct task with **exactly one** activity node in a
flow. If the process **revisits** a step later (a re-check, a return, a second pass), model
it as a **loop-back edge to the existing node** (see the junction/loop-back rule below) —
never a second copy of the node. A recurring step is an *edge*, not a duplicated node. (Do
not collapse genuinely distinct steps that merely sound alike — §6.)

**Self-check before emitting.** Re-read every title and description: every description
sentence that passes the node test ("someone does this") must be promoted into the flow as
its own node in its correct chronological position, and every title must be readable in
isolation with no detail view open.

### Entry and exit (start/end discipline)

Every graph must have exactly **one entry activity** and every path must reach a **meaningful end**.

- **Entry test:** the entry node is the activity that runs FIRST in a normal execution of this process (its trigger). A contingency (overflow, error handling), an upstream step performed by another department, or a one-time setup step can NEVER be the entry. If more than one activity ends up with no incoming edge, you have missed a preceding step or included out-of-scope material — fix the graph; do not leave multiple implicit starts.
- **Exit test:** every path from the entry must terminate at a node with no outgoing edge that represents a real outcome of the process (e.g. «مشتری نشانده‌شده سر میز», not merely the act of making a phone call). No activity may dangle mid-flow without a successor unless it is a genuine end.

### Directed Edges

Edges express temporal precedence: activity A must finish (or begin) before activity B. Each edge has:
- `from` — key or ID of the source node
- `to` — key or ID of the destination node
- `label` (optional) — governed by the edge-label contract below

**Edge-label contract (mandatory):** a label may contain ONLY one of:
1. **A branch condition** — the Persian condition under which this path is taken (e.g. «در صورت وجود کمبود», «پیش از ساعت ۶»). Required on EVERY edge leaving an XOR/OR split.
2. **A concrete artifact** — the object/document that passes along this edge (e.g. «فرم اصلاحیه», «استند شماره‌دار»), only when naming it adds information.

A label must NEVER restate or paraphrase the source or target node's own label or action — «پس از انتخاب تاریخ» on the edge leaving «باز کردن فرم و انتخاب تاریخ» is wrong. If B simply follows A with no condition and no meaningful artifact, omit `label` entirely: **an unlabeled edge is the correct default for plain sequence.**

### Junctions

Junctions model branching and merging of the flow. A junction node has:
- `junctionType` — one of `AND`, `OR`, `XOR`
- `direction` — one of `split` (fan-out from one incoming edge to many outgoing) or `join` (fan-in from many incoming edges to one outgoing)

| junctionType | split meaning | join meaning |
|---|---|---|
| `AND` | All outgoing paths are activated simultaneously (parallel execution). | All incoming paths must complete before proceeding. |
| `OR` | One or more outgoing paths are activated (inclusive or). | Waits for whichever paths were activated. |
| `XOR` | Exactly one outgoing path is activated (exclusive choice). | The first (and only) arriving path triggers continuation. |

**Control-flow completeness (mandatory):** whenever the transcript expresses a decision, condition, exception, error, rejection, or rework — cues like «اگر…», «در صورتی که…», «اگر نشد/نبود», «تأیید یا رد», «خطا», «شکایت», «اصلاح/تغییر سفارش» — you MUST model it as an explicit junction with one labeled outgoing edge per spoken outcome. Never as prose inside a `description`, and never as a plain activity with a single conditional edge.

- Exclusive choice → `XOR` split; put the decision question/criterion in the preceding activity's `description`.
- Branches must cover every spoken outcome. An inspection/verification/approval step MUST have both its pass branch and its spoken fail branch; route the fail branch to its correction activity, and if the voice says the work is re-checked, add the loop-back edge to the re-check step.
- Junction topology must be well-formed: a `split` has exactly 1 incoming and 2+ outgoing edges; a `join` has 2+ incoming and exactly 1 outgoing. An AND split whose paths continue must rejoin at an AND join.

Dropping a spoken branch is an omission defect under §6 — exactly as forbidden as fabrication.

---

## 3. Temporary Keys (INV-1)

The `extract` agent **must never emit a final ID** in `candidate.json` or `delta.json`. Final IDs (seen in `process.json` after the `merge` CLI runs) are two-level and are **allocated only by the `allocate-id` CLI** after merge, never by an LLM:
- process ID → `{dept}-{NNN}` (e.g. `cooking-001`)
- box/activity ID → `{process-id}-n{NNN}` (e.g. `cooking-001-n010`)
- junction ID → `{process-id}-j{N}` (e.g. `cooking-001-j1`)

**Naming convention for temp keys:**

| Node type | Key pattern | Examples |
|---|---|---|
| `activity` | `n` + integer | `n1`, `n2`, `n3`, … |
| `junction` | `j` + integer | `j1`, `j2`, `j3`, … |

Edges in `candidate.json` reference these temp keys in their `from` and `to` fields.

In `delta.json`, `add_nodes` entries use the same temp key convention (`n1`, `j1`, …). `add_edges` may reference temp keys (for newly added nodes) or existing real IDs already present in `process.json` (for connections to existing nodes). `enrich_nodes` and `flag_removed` always reference real existing IDs.

**Never** write a key or ID value that matches the final-ID pattern. The structural check will reject any such string in the output.

---

## 4. Candidate Contract (new process)

When the transcript describes a **brand-new process** (no existing `process.json`), output a single JSON object conforming to the candidate contract below (the `merge` CLI validates this shape when it consumes the file). All top-level fields are **required**.

### Top-level structure

```json
{
  "department": "<lowercase department slug, e.g. dining>",
  "process_name": "<Persian process name>",
  "summary": "<Persian one-paragraph summary of the whole process>",
  "idef0": {
    "inputs": [],
    "controls": [],
    "outputs": [],
    "mechanisms": []
  },
  "kpis": [],
  "nodes": [],
  "edges": []
}
```

### Activity node (required fields)

Every activity node in `nodes` **must** have all seven fields (and **only** these — do NOT emit `position` or `layout` fields; those are added by the merge/layout engine, never by the extract agent):

```json
{
  "key": "n1",
  "type": "activity",
  "label": "<Persian label>",
  "description": "<Persian description>",
  "actor": "<Persian role>",
  "icom": {
    "inputs": [],
    "controls": [],
    "outputs": [],
    "mechanisms": []
  },
  "subprocess": null
}
```

| Field | Rule |
|---|---|
| `key` | Temp key: `n1`, `n2`, … (unique within this candidate) |
| `type` | Must be the string `"activity"` |
| `label` | Persian, self-sufficient title; length is not a constraint (§2 "What goes in the flow") |
| `description` | Persian, supporting detail ABOUT the step — never an action (§2 "What goes in the flow") |
| `actor` | Persian role/system (never a personal name) |
| `icom` | Object with four arrays: `inputs`, `controls`, `outputs`, `mechanisms` (each may be empty) |
| `subprocess` | `null` in the candidate — merge sets it (see §7) |

### Junction node (required fields)

Every junction node in `nodes` **must** have all four fields:

```json
{
  "key": "j1",
  "type": "junction",
  "junctionType": "AND",
  "direction": "split"
}
```

| Field | Allowed values |
|---|---|
| `key` | Temp key: `j1`, `j2`, … |
| `type` | Must be `"junction"` |
| `junctionType` | `AND` \| `OR` \| `XOR` |
| `direction` | `split` \| `join` |

### KPI object

```json
{
  "name": "<Persian KPI name>",
  "definition": "<Persian definition>",
  "target": "<target value as string>",
  "unit": "<unit>"
}
```

Only `name` is required. Omit `definition`, `target`, `unit` (or leave them as empty strings) if not mentioned in the transcript.

### Edge object

```json
{
  "from": "n1",
  "to": "n2",
  "label": "<optional Persian label>"
}
```

`from` and `to` are required. `label` is optional and governed by the §2 edge-label contract — omit it for plain sequence.

#### Sub-processes (subprocesses)

**OPTIONAL** top-level `subprocesses` array. Emit it only when one or more activity boxes qualify as a self-contained, separately-nameable procedure (see §7). Each item has the following shape:

```json
{
  "parent_key": "n4",
  "process": {
    "department": "<lowercase department slug>",
    "process_name": "<Persian process name>",
    "summary": "<Persian summary>",
    "idef0": { "inputs": [], "controls": [], "outputs": [], "mechanisms": [] },
    "kpis": [],
    "nodes": [],
    "edges": []
  }
}
```

| Field | Rule |
|---|---|
| `parent_key` | The temp activity key in **this** candidate (e.g. `n4`) whose box qualifies. This is the activity whose work will be decomposed. |
| `process` | A full candidate body with its **own** temp node keys (`n1`, `n2`, … starting fresh). Must NOT itself contain a `subprocesses` field — nesting is single-level only (schema-enforced). |

**Critical:** The parent activity node's own `subprocess` field **stays `null`** in the candidate. The `merge` CLI resolves the real IDs and sets `subprocess` on the parent node after allocation (INV-1). The extract agent **never** mints a process or subprocess ID — temp node keys only.

Minimal example (candidate with one subprocess entry):

```json
{
  "department": "cooking",
  "process_name": "فرایند پخت غذا",
  "summary": "...",
  "idef0": { "inputs": [], "controls": [], "outputs": [], "mechanisms": [] },
  "kpis": [],
  "nodes": [
    {
      "key": "n1", "type": "activity",
      "label": "آماده‌سازی مواد", "description": "...",
      "actor": "آشپز", "icom": { "inputs": [], "controls": [], "outputs": [], "mechanisms": [] },
      "subprocess": null
    },
    {
      "key": "n4", "type": "activity",
      "label": "پخت اصلی", "description": "...",
      "actor": "سرآشپز", "icom": { "inputs": [], "controls": [], "outputs": [], "mechanisms": [] },
      "subprocess": null
    }
  ],
  "edges": [{ "from": "n1", "to": "n4" }],
  "subprocesses": [
    {
      "parent_key": "n4",
      "process": {
        "department": "cooking",
        "process_name": "فرایند پخت اصلی — جزئیات",
        "summary": "...",
        "idef0": { "inputs": [], "controls": [], "outputs": [], "mechanisms": [] },
        "kpis": [],
        "nodes": [
          { "key": "n1", "type": "activity", "label": "گرم‌کردن تنور", "description": "...", "actor": "سرآشپز", "icom": { "inputs": [], "controls": [], "outputs": [], "mechanisms": [] }, "subprocess": null },
          { "key": "n2", "type": "activity", "label": "قرار دادن غذا", "description": "...", "actor": "سرآشپز", "icom": { "inputs": [], "controls": [], "outputs": [], "mechanisms": [] }, "subprocess": null }
        ],
        "edges": [{ "from": "n1", "to": "n2" }]
      }
    }
  ]
}
```

---

## 5. Delta Contract (update to existing process)

When the transcript set updates an **existing process** (a `process.json` already exists), output a single JSON object conforming to the delta contract below (validated by `merge` on consumption). All six top-level arrays are **required** (they may be empty).

```json
{
  "add_nodes": [],
  "add_edges": [],
  "enrich_nodes": [],
  "revise_nodes": [],
  "remove_edges": [],
  "flag_removed": []
}
```

### `add_nodes`

New nodes to insert. Uses the same activity/junction shapes as candidate `nodes` (with temp keys `n1`, `j1`, …). All required fields identical to §4. When `merge` applies the delta, it converts every temp key in `add_nodes` into a real allocated ID by calling the `allocate-id` CLI (INV-1); the extract agent never does this.

### `add_edges`

New edges to add. `from`/`to` may be temp keys (new nodes) or real existing IDs from `process.json`.

For example, if you are adding a new node `n1` and connecting it to an already-existing node whose real ID you read from `process.json`, the edge would look like:

```json
{ "from": "n1", "to": "<real-id-from-process-json>" }
```

The temp key (`n1`) is author-chosen. The real ID comes verbatim from `process.json` — the agent reads it, it does not invent it.

### `enrich_nodes`

Updates to **existing** nodes. Each entry has:
- `id` — the real existing node ID (read from `process.json`, never invented)
- `set` — an object containing **only the fields being enriched** (partial update)

```json
{
  "id": "<real-id-from-process-json>",
  "set": {
    "description": "<updated Persian description>",
    "icom": {
      "inputs": ["<new item>"],
      "controls": [],
      "outputs": [],
      "mechanisms": []
    }
  }
}
```

The `set` object may contain any subset of node fields. Do not repeat fields that are unchanged.

### `revise_nodes` (overwrite committed fields — supersession)

`enrich_nodes` fills **empty** fields (or raises a `pending` conflict); it cannot overwrite a value the process already has. When a **later session supersedes** an earlier account (spec §4.3), use `revise_nodes` to overwrite specific committed fields. Each entry:

```json
{
  "id": "<real-id-from-process-json>",
  "set": { "label": "<new Persian label>", "description": "<new Persian description>" }
}
```

- `id` — a real existing node id read verbatim from `process.json` (never invented).
- `set` — only the fields being overwritten (any subset of the node's fields; the §2 node/title rules still govern `label`/`description`).

Every revision is shown at Gate B **before** it is written, so overwrite is safe. Use `enrich_nodes` for fill-empty; use `revise_nodes` only to change an already-filled value.

### `remove_edges` (edge hygiene)

A delta can add edges but cannot otherwise remove one, so inserting a node between `1` and `2` leaves a stale `1→2` edge beside `1→new→2`. Emit the now-redundant edge here:

```json
{ "from": "<real-id>", "to": "<real-id>" }
```

- Both endpoints are **real existing node ids** read from `process.json`.
- **Edge-hygiene rule:** whenever you attach a node onto an existing path, or re-route flow, emit the edge it makes redundant in `remove_edges` — the engine never guesses which edge to drop. `merge update` hard-deletes these edges (edges are structure, not the content INV-4 protects) and re-layouts afterward.

### `flag_removed`

Existing node IDs that the transcript set implies are no longer part of the process. The `merge` CLI will set `removed: true` on these nodes — it **never deletes** them (INV-4). The extract agent must not delete nodes; it only flags.

```json
{ "id": "<real-id-from-process-json>" }
```

### `add_subprocesses` (Sub-processes in a delta)

**OPTIONAL** `add_subprocesses` array. Emit it when a box in an **existing** process qualifies as a self-contained, separately-nameable procedure (see §7). Each item:

```json
{
  "parent": "<real node id OR a temp key from add_nodes>",
  "process": {
    "department": "<lowercase department slug>",
    "process_name": "<Persian process name>",
    "summary": "<Persian summary>",
    "idef0": { "inputs": [], "controls": [], "outputs": [], "mechanisms": [] },
    "kpis": [],
    "nodes": [],
    "edges": []
  }
}
```

| Field | Rule |
|---|---|
| `parent` | A **real** existing node ID read from `process.json` (e.g. `cooking-001-n010`), OR a temp key from `add_nodes` if the parent is a newly added node in this delta. Never invent a real ID. |
| `process` | A full candidate body with its own temp node keys. Must NOT contain `subprocesses` — single level only. |

The extract agent **never** mints a process or subprocess ID — temp node keys only (INV-1). The `merge` CLI resolves real IDs and sets `subprocess` on the parent node.

---

## 6. No Fabrication (INV-3)

Fill every field **only from actual content present in the transcript or document**. Do not invent data to complete a template.

- If the transcript does not mention inputs for an activity, emit `"inputs": []`.
- If no KPIs are mentioned, emit `"kpis": []`.
- If the actor's role is unclear, emit `"actor": ""`.
- Short outputs are acceptable **only when the source itself is silent**. Do not pad to look complete.

**ناقص‌بودن اشکالی ندارد؛ جعل اطلاعات ممنوع است.**

(Incompleteness is fine; fabrication of information is forbidden.)

**The rule cuts both ways.** Omitting content that WAS spoken is equally a defect: every step, decision, exception branch, timing («تا قبل از ۵:۵۴»), quantity («۵ تا ۶ سینی»), named tool/form/system (گوگل فرمز، بی‌سیم، فرم اصلاحیه), and service standard («کمتر از دو دقیقه») present in the transcript excerpt must appear in the graph or its fields. Before finishing, re-scan the excerpt once and confirm nothing spoken was dropped. Leave a field empty only when the source genuinely does not supply it.

This rule applies to every string field: `label`, `description`, `summary`, `actor`, all ICOM array items, KPI fields. If it was not explicitly said or clearly implied in the transcript, do not write it.

---

## 7. Sub-processes (self-contained, separately-nameable procedures)

### When to create a child process

Emit a child process in `subprocesses` (candidate) or `add_subprocesses` (delta) **only
when a group of steps is a self-contained, separately-nameable procedure — one the domain
expert would refer to as a distinct thing in its own right** (e.g. «فرایند تسویه پایان
شیفت»). **Step count is never the reason to nest.** A box is not promoted to a sub-process
because it "has many sub-steps".

If a group of steps is NOT such a nameable procedure, do NOT nest it and do NOT summarise
it in prose: emit each step as a flat sibling activity node in the main flow, under the
"What goes in the flow" rules in §2. Producing a longer, flatter top-level flow is the
intended outcome — visible flow beats hidden hierarchy.

### How to create a child process

1. In the `subprocesses` / `add_subprocesses` array, add an entry with:
   - `parent_key` / `parent`: the temp key (or real ID) of the qualifying activity.
   - `process`: a full candidate body capturing those steps as activity nodes with their
     own temp keys (`n1`, `n2`, …), each obeying the §2 node/title rules.
2. Keep `subprocess: null` on the parent activity node itself — **merge** allocates the
   child ID and sets this field (INV-1).
3. **No recursion:** if one of the child process's own nodes is itself a self-contained
   nameable procedure, do **not** nest further — leave it as a flat node in the child flow.
4. Report the parent node key and child process name in your completion message so the
   orchestrator knows to capture the printed child ID from merge stdout.

### No duplication across a process and its subprocess

A real task appears **exactly once** across a process and its subprocess(es). When you
promote a box to a subprocess, its constituent steps belong to the **child only** — the
parent keeps **just the container box** (the higher-level activity whose `subprocess`
points at the child). Do **not** also emit those same steps as flat activity nodes in the
parent flow. If you find the decomposed steps sitting in both the parent flow and the
child, remove them from the parent — the box is their single parent-level representative.

**Allowed (do not treat as duplication):** the container box and the child's first node sit
at **different levels of abstraction** and are *expected to differ* — the box names the area
of work, the child's first node is a concrete first step. Example: a parent box
«مدیریت نوبت در زمان شلوغی» whose child subprocess begins «هدایت مشتری به اتاق انتظار».
These are **not** duplicates; never force them to match, and never collapse the box into
the child.

**Guardrail (§6, INV-3):** collapse only *accidental* duplicate copies of the same single
occurrence. A step the process genuinely performs at two **distinct** points, or a
loop-back re-check, is **kept** — as one node plus the appropriate edges. Never drop
distinct spoken work merely because two labels sound alike.

### What merge does with a submitted child (informational — for understanding context)

When `merge` processes a candidate or delta that contains a `subprocesses` / `add_subprocesses` entry, it:
1. Resolves the parent activity's real node ID.
2. Allocates the child process ID via `allocate-id` CLI.
3. Writes `departments/{dept}/processes/{child-id}.json` with `parent: {process: "<parent-id>", node: "<parent-node-id>"}` and `source.type: "auto"`.
4. Sets the parent node's `subprocess` field to the child process ID.
5. Syncs the parent box's `icom` to equal the child's `idef0` (child wins on conflict).
6. Lays out the child process (serpentine layout).
7. Prints `subprocess <child-id> node <parent-node-id>` to stdout — the orchestrator captures these lines.

**The extract agent never mints a process or subprocess ID. Temp node keys only (INV-1).**

---

## 8. Restructure — heir candidates & `subprocess_links` (merge / split)

When the mapping between committed and desired processes is **not one-to-one** (2+ committed → 1
desired = merge; 1 committed → 2+ desired = split), the change is a **restructure**, not an update
(spec §4.5). The `extract` agent emits each **heir** as a **full candidate body** (§4 shape — fresh
temp keys `n1`, `j1`, …), plus, when the heir owns hierarchy links, a `subprocess_links` array:

```json
{
  "subprocess_links": [
    { "parent_key": "n3", "child": "<committed child process id>" }
  ]
}
```

| Field | Rule |
|---|---|
| `parent_key` | The heir's own temp activity key whose box owns the sub-process link. |
| `child` | The **committed** child process id (read verbatim from disk) that must re-parent under this heir. |

The orchestrator assembles the run's restructure **plan** — `{department, heirs:[{candidate,
supersedes:[pid], subprocess_links:[…]}]}` — and runs `merge restructure`. The agent supplies only
each heir's `candidate` + `subprocess_links`; the **engine** mints every real id, tombstones each
superseded original (`superseded_by` + tombstoned flag), and redirects hierarchy pointers
deterministically. **Hierarchy-closed set:** every process whose links are affected must be in the
plan, or the engine refuses and names the missing one — so declare every affected link here.
`attach-subprocess` (re-parent an existing process, unchanged, under a node) and `remove`
(tombstone with no heir) are separate `merge` verbs the orchestrator runs directly from
`segments.json`'s op arrays; the extract agent does not build artifacts for them. **The agent never
mints an id (INV-1); it copies committed ids verbatim and uses temp keys for new nodes.**

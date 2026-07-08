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
- A short `label` (Persian, 2–6 words)
- A longer `description` (Persian, one or two sentences)
- An `actor` (Persian role name)
- Its own `icom` object (the ICOM at this step's level)
- A `subprocess` pointer (`null` in the candidate; merge sets it after allocating the child ID — see §7)

### Directed Edges

Edges express temporal precedence: activity A must finish (or begin) before activity B. Each edge has:
- `from` — key or ID of the source node
- `to` — key or ID of the destination node
- `label` (optional) — a short Persian description of what flows along this edge

### Junctions

Junctions model branching and merging of the flow. A junction node has:
- `junctionType` — one of `AND`, `OR`, `XOR`
- `direction` — one of `split` (fan-out from one incoming edge to many outgoing) or `join` (fan-in from many incoming edges to one outgoing)

| junctionType | split meaning | join meaning |
|---|---|---|
| `AND` | All outgoing paths are activated simultaneously (parallel execution). | All incoming paths must complete before proceeding. |
| `OR` | One or more outgoing paths are activated (inclusive or). | Waits for whichever paths were activated. |
| `XOR` | Exactly one outgoing path is activated (exclusive choice). | The first (and only) arriving path triggers continuation. |

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
| `label` | Persian, 2–6 words |
| `description` | Persian, describes what happens in this step |
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

`from` and `to` are required. `label` is optional.

#### Sub-processes (subprocesses)

**OPTIONAL** top-level `subprocesses` array. Emit it only when one or more activity boxes qualify (see §7 threshold rule). Each item has the following shape:

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

When the transcript updates an **existing process** (a `process.json` already exists), output a single JSON object conforming to the delta contract below (validated by `merge` on consumption). All four top-level arrays are **required** (they may be empty).

```json
{
  "add_nodes": [],
  "add_edges": [],
  "enrich_nodes": [],
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

### `flag_removed`

Existing node IDs that the voice implies are no longer part of the process. The `merge` CLI will set `removed: true` on these nodes — it **never deletes** them (INV-4). The extract agent must not delete nodes; it only flags.

```json
{ "id": "<real-id-from-process-json>" }
```

### `add_subprocesses` (Sub-processes in a delta)

**OPTIONAL** `add_subprocesses` array. Emit it when a box in an **existing** process qualifies (see §7 threshold rule). Each item:

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
- Short, incomplete outputs are always acceptable. Do not pad to look complete.

**ناقص‌بودن اشکالی ندارد؛ جعل اطلاعات ممنوع است.**

(Incompleteness is fine; fabrication of information is forbidden.)

This rule applies to every string field: `label`, `description`, `summary`, `actor`, all ICOM array items, KPI fields. If it was not explicitly said or clearly implied in the transcript, do not write it.

---

## 7. Sub-processes (auto-create at threshold)

### Threshold

Emit a child process in `subprocesses` (candidate) or `add_subprocesses` (delta) **only** when an activity box is genuinely described in the transcript with **4 or more distinct sequential sub-steps**. If the box is described with fewer than 4 distinct sequential sub-steps, use **flag-only** behaviour instead (see below).

### At or above threshold (4+ sub-steps) — emit a child

1. In the `subprocesses` / `add_subprocesses` array, add an entry with:
   - `parent_key` / `parent`: the temp key (or real ID) of the qualifying activity.
   - `process`: a full candidate body capturing those sub-steps as activity nodes with their own temp keys (`n1`, `n2`, …).
2. Keep `subprocess: null` on the parent activity node itself — **merge** allocates the child ID and sets this field (INV-1).
3. **No recursion:** if one of the child process's own activity nodes would itself qualify (4+ sub-steps of its sub-steps), do **not** nest further — apply flag-only on that node instead.
4. Report the parent node key and child process name in your completion message so the orchestrator knows to capture the printed child ID from merge stdout.

### Below threshold — flag-only

1. Keep `subprocess: null` on the node.
2. Append a short Persian note to the node's `description`. Example: «این مرحله شامل چند زیرگام مجزاست و ممکن است در آینده به‌عنوان فرایند مستقل مستندسازی شود.»
3. **Report** the node key and a brief explanation in your completion message to the orchestrator.

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

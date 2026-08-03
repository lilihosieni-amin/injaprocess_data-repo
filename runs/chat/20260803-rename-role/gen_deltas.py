"""Generate one merge-update delta per process that names the logistics supervisor role
under an old variant. Writes deltas only; the merge CLI remains the sole writer of
departments/**/processes/*.json.
"""
import json
import glob
import os

ROOT = "/data"
OUT = os.path.join(ROOT, "runs/chat/20260803-rename-role/deltas")
TARGET = "سرپرست بخش لجستیک"

# Longest-first so that a longer phrase is never partially rewritten by a shorter rule.
RULES = [
    "سرپرست بخش لوجستیک",
    "سرپرست بخش ارسال",
    "سرپرست لوجستیک",
    "سرپرست لجستیک",
    "سرپرست ارسال",
    "مسئول لجستیک",
]

NODE_TEXT_FIELDS = ("label", "description", "actor")


def sub(value):
    """Replace every old variant in a string / list of strings / ICOM dict."""
    if isinstance(value, str):
        for old in RULES:
            if old != TARGET:
                value = value.replace(old, TARGET)
        return value
    if isinstance(value, list):
        out = []
        for item in value:
            new = sub(item)
            # collapse the duplicate strings the rename can create in ICOM lists
            if not isinstance(new, str) or new not in out:
                out.append(new)
        return out
    if isinstance(value, dict):
        return {k: sub(v) for k, v in value.items()}
    return value


os.makedirs(OUT, exist_ok=True)
plan = []

for path in sorted(glob.glob(os.path.join(ROOT, "departments/*/processes/*.json"))):
    doc = json.load(open(path))
    pid = doc["id"]

    if doc.get("tombstoned") or doc.get("superseded_by"):
        if any(r in json.dumps(doc, ensure_ascii=False) for r in RULES):
            plan.append((pid, "SKIPPED-TOMBSTONED", 0, False))
        continue

    revise = []
    for node in doc["nodes"]:
        if node["type"] != "activity":
            continue
        changed = {}
        for field in NODE_TEXT_FIELDS:
            new = sub(node.get(field, ""))
            if new != node.get(field, ""):
                changed[field] = new
        new_icom = sub(node["icom"])
        if new_icom != node["icom"]:
            changed["icom"] = new_icom
        if changed:
            revise.append({"id": node["id"], "set": changed})

    set_process = {}
    for field in ("name", "summary"):
        new = sub(doc[field])
        if new != doc[field]:
            set_process[field] = new
    new_idef0 = sub(doc["idef0"])
    if new_idef0 != doc["idef0"]:
        set_process["idef0"] = new_idef0
    new_kpis = sub(doc.get("kpis", []))
    if new_kpis != doc.get("kpis", []):
        set_process["kpis"] = new_kpis

    if not revise and not set_process:
        continue

    delta = {
        "add_nodes": [],
        "add_edges": [],
        "enrich_nodes": [],
        "revise_nodes": revise,
        "remove_edges": [],
        "flag_removed": [],
    }
    if set_process:
        delta["set_process"] = set_process

    json.dump(
        delta,
        open(os.path.join(OUT, pid + ".json"), "w"),
        ensure_ascii=False,
        indent=2,
    )
    plan.append((pid, "delta", len(revise), bool(set_process)))

for pid, kind, n, sp in plan:
    print(f"{pid}\t{kind}\tnodes={n}\tset_process={sp}")
print(f"\nTOTAL delta files: {sum(1 for p in plan if p[1] == 'delta')}")

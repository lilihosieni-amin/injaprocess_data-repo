#!/usr/bin/env python3
"""Build merge-CLI deltas that normalise cooking-department role vocabulary.

Reads process files (read-only) and writes ONLY delta artifacts under runs/.
Process files themselves are written exclusively by the `merge` CLI (INV-1).

Substitutions (applied in this order so the combined phrase is handled first):
    "سرپرست بخش (سرلاین)" -> "سرپرست لاین"
    "سرپرست بخش"          -> "سرپرست لاین"
    "سرلاین"              -> "سرپرست لاین"
    "سرآشپز"              -> "سرپرست آشپزخانه"
"""
import json
import pathlib
import sys

ROOT = pathlib.Path("/data")
PROC = ROOT / "departments" / "cooking" / "processes"
OUT = ROOT / "runs" / "chat" / "20260904-role-terms"

SUBS = [
    ("سرپرست بخش (سرلاین)", "سرپرست لاین"),
    ("سرپرست بخش", "سرپرست لاین"),
    ("سرلاین", "سرپرست لاین"),
    ("سرآشپز", "سرپرست آشپزخانه"),
]

FILES = ["cooking-023", "cooking-024", "cooking-026", "cooking-027",
         "cooking-029", "cooking-030", "cooking-032", "cooking-036"]


def sub(text):
    if not isinstance(text, str):
        return text
    for old, new in SUBS:
        text = text.replace(old, new)
    return text


def sub_list(items):
    """Substitute then de-duplicate, preserving original order."""
    seen, out = set(), []
    for it in items:
        v = sub(it)
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out


def sub_icom(icom):
    return {k: sub_list(icom.get(k, [])) for k in
            ("inputs", "controls", "outputs", "mechanisms")}


def main():
    summary = []
    for pid in FILES:
        path = PROC / f"{pid}.json"
        doc = json.loads(path.read_text(encoding="utf-8"))

        revise, skipped_removed = [], 0
        for n in doc["nodes"]:
            if n.get("type") != "activity":
                continue
            if n.get("removed"):
                blob = json.dumps(n, ensure_ascii=False)
                if any(o in blob for o, _ in SUBS):
                    skipped_removed += 1
                continue
            changed = {}
            for field in ("label", "description", "actor"):
                if field in n:
                    v = sub(n[field])
                    if v != n[field]:
                        changed[field] = v
            if "icom" in n and isinstance(n["icom"], dict):
                v = sub_icom(n["icom"])
                if v != n["icom"]:
                    changed["icom"] = v
            if changed:
                revise.append({"id": n["id"], "set": changed})

        set_process = {}
        for field in ("name", "summary"):
            v = sub(doc.get(field, ""))
            if v != doc.get(field, ""):
                set_process[field] = v
        idef0 = {k: sub_list(doc["idef0"].get(k, [])) for k in
                 ("inputs", "controls", "outputs", "mechanisms")}
        if idef0 != doc["idef0"]:
            set_process["idef0"] = idef0
        kpis = []
        for k in doc.get("kpis", []):
            kpis.append({kk: sub(vv) for kk, vv in k.items()})
        if kpis != doc.get("kpis", []):
            set_process["kpis"] = kpis

        if not revise and not set_process:
            summary.append(f"{pid}: no change")
            continue

        delta = {
            "add_nodes": [], "add_edges": [], "enrich_nodes": [],
            "revise_nodes": revise, "remove_edges": [], "flag_removed": [],
        }
        if set_process:
            delta["set_process"] = set_process

        dest = OUT / f"delta-{pid}.json"
        dest.write_text(json.dumps(delta, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
        summary.append(
            f"{pid}: nodes={len(revise)} "
            f"process_fields={sorted(set_process) or 'none'} "
            f"retired_nodes_left_untouched={skipped_removed}")

    print("\n".join(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())

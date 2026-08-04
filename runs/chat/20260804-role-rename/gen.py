import json, glob, os

ZW = "‌"
CD = "صندوق" + ZW + "دار"   # صندوق‌دار
PEYK = "پیک"                                          # پیک

RENAME = {
    "پیک موتوری": PEYK,          # پیک موتوری
    "صندوق": CD,                                      # صندوق
    "صندوقدار": CD,                    # صندوقدار
    "همکار بخش صندوق": CD,   # همکار بخش صندوق
    "همکار صندوق": CD,       # همکار صندوق
    "پرسنل صندوق": CD,       # پرسنل صندوق
    "کارکنان بخش صندوق": CD,  # کارکنان بخش صندوق
    "همکاران صندوق": CD,          # همکاران صندوق
}

OUT = "runs/chat/20260804-role-rename"


def dedupe(seq):
    seen, res = set(), []
    for x in seq:
        if x not in seen:
            seen.add(x)
            res.append(x)
    return res


files = sorted(glob.glob("departments/cashier/proces" + "ses/*.json") +
               glob.glob("departments/logistics/proces" + "ses/*.json"))

node_summary, idef_summary = [], []

for f in files:
    d = json.load(open(f))
    if d.get("tombstoned") or d.get("superseded_by"):
        continue
    revise = []
    n_actor = n_mech = 0
    for n in d.get("nodes", []):
        if n.get("type") != "activity":
            continue
        st = {}
        old_a = n.get("actor")
        new_a = RENAME.get(old_a, old_a)
        if new_a != old_a:
            st["actor"] = new_a
            n_actor += 1
        icom = n.get("icom", {})
        old_m = icom.get("mechanisms", [])
        new_m = dedupe([RENAME.get(m, m) for m in old_m])
        if new_m != old_m:
            st["icom"] = {
                "inputs": list(icom.get("inputs", [])),
                "controls": list(icom.get("controls", [])),
                "outputs": list(icom.get("outputs", [])),
                "mechanisms": new_m,
            }
            n_mech += sum(1 for m in old_m if m in RENAME)
        if st:
            revise.append({"id": n["id"], "set": st})

    # phase 2 (idef0) — reported only, not written
    im = d.get("idef0", {}).get("mechanisms", [])
    new_im = dedupe([RENAME.get(m, m) for m in im])
    if new_im != im:
        idef_summary.append((d["id"], im, new_im))

    if revise:
        delta = {"add_nodes": [], "add_edges": [], "enrich_nodes": [],
                 "revise_nodes": revise, "remove_edges": [], "flag_removed": []}
        p = os.path.join(OUT, d["id"] + ".delta.json")
        with open(p, "w") as fh:
            json.dump(delta, fh, ensure_ascii=False, indent=2)
        node_summary.append((d["id"], len(revise), n_actor, n_mech))

print("=== PHASE 1: node deltas written ===")
for pid, nodes, a, m in node_summary:
    print("%-16s nodes=%-3d actor=%-3d mech=%d" % (pid, nodes, a, m))
print("totals: processes=%d nodes=%d actor=%d mech=%d" % (
    len(node_summary), sum(x[1] for x in node_summary),
    sum(x[2] for x in node_summary), sum(x[3] for x in node_summary)))

print()
print("=== PHASE 2: idef0.mechanisms (needs INV-5 approval) ===")
for pid, old, new in idef_summary:
    ch = [(o, n) for o, n in zip(old, new) if o != n]
    dropped = len(old) - len(new)
    print("%-16s %s%s" % (pid, "  ".join("%s -> %s" % c for c in ch),
                          ("   [dedupe: -%d]" % dropped) if dropped else ""))
print("processes needing set_process: %d" % len(idef_summary))

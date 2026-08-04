import json, glob, os

ZW = "‌"
CD = "صندوق" + ZW + "دار"          # صندوق‌دار
CD_CC = CD + " کال" + ZW + "سنتر"        # صندوق‌دار کال‌سنتر
PEYK = "پیک"                                                  # پیک

# phase 1 map (already applied to nodes; idef0 still carries these)
RENAME = {
    "پیک موتوری": PEYK,
    "صندوق": CD,
    "صندوقدار": CD,
    "همکار بخش صندوق": CD,
    "همکار صندوق": CD,
    "پرسنل صندوق": CD,
    "کارکنان بخش صندوق": CD,
    "همکاران صندوق": CD,
}
# final approved item: parenthetical variants
RENAME2 = {
    CD + " (پرسنل بخش صندوق)": CD,
    "همکار صندوق (کال" + ZW + "سنتر)": CD_CC,
}
ALL = dict(RENAME)
ALL.update(RENAME2)

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

rows = []
for f in files:
    d = json.load(open(f))
    if d.get("tombstoned") or d.get("superseded_by"):
        continue

    # node-level: only the newly approved parenthetical variants remain
    revise = []
    for n in d.get("nodes", []):
        if n.get("type") != "activity":
            continue
        st = {}
        old_a = n.get("actor")
        new_a = RENAME2.get(old_a, old_a)
        if new_a != old_a:
            st["actor"] = new_a
        icom = n.get("icom", {})
        old_m = icom.get("mechanisms", [])
        new_m = dedupe([RENAME2.get(m, m) for m in old_m])
        if new_m != old_m:
            st["icom"] = {
                "inputs": list(icom.get("inputs", [])),
                "controls": list(icom.get("controls", [])),
                "outputs": list(icom.get("outputs", [])),
                "mechanisms": new_m,
            }
        if st:
            revise.append({"id": n["id"], "set": st})

    # process-level idef0.mechanisms
    idef0 = d.get("idef0", {})
    old_im = idef0.get("mechanisms", [])
    new_im = dedupe([ALL.get(m, m) for m in old_im])

    if not revise and new_im == old_im:
        continue

    delta = {"add_nodes": [], "add_edges": [], "enrich_nodes": [],
             "revise_nodes": revise, "remove_edges": [], "flag_removed": []}
    if new_im != old_im:
        delta["set_process"] = {"idef0": {
            "inputs": list(idef0.get("inputs", [])),
            "controls": list(idef0.get("controls", [])),
            "outputs": list(idef0.get("outputs", [])),
            "mechanisms": new_im,
        }}
    p = os.path.join(OUT, d["id"] + ".p2.json")
    with open(p, "w") as fh:
        json.dump(delta, fh, ensure_ascii=False, indent=2)
    rows.append((d["id"], len(revise), len(old_im) - len(new_im),
                 "set_process" in delta))

for pid, nrev, dd, sp in rows:
    print("%-16s revise_nodes=%-2d idef0=%s%s" % (
        pid, nrev, "yes" if sp else "no",
        ("  [dedupe -%d]" % dd) if dd else ""))
print("total deltas: %d" % len(rows))

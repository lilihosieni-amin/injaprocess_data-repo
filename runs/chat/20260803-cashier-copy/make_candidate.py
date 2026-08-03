"""Take the ORIGINAL merged candidate (the one that produced logistics-026 before any
subprocess attachment or node removal) and re-target it at the cashier department."""
import json

src = "/data/runs/chat/20260802-merge-21-31/candidate.json"
dst = "/data/runs/chat/20260803-cashier-copy/candidate.json"

c = json.load(open(src))
assert c["department"] == "logistics", c["department"]
c["department"] = "cashier"

json.dump(c, open(dst, "w"), ensure_ascii=False, indent=2)

acts = [n for n in c["nodes"] if n["type"] == "activity"]
print("department:", c["department"])
print("name:", c["process_name"])
print("activities:", len(acts), "junctions:", len(c["nodes"]) - len(acts), "edges:", len(c["edges"]))
print("last activity key/label:", acts[-1]["key"], "|", acts[-1]["label"])
print("has subprocess pointers:", any(n.get("subprocess") for n in c["nodes"]))

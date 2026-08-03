import json

for pid, dept in (("cashier-037", "cashier"), ("cashier-031", "cashier")):
    d = json.load(open(f"/data/departments/{dept}/processes/{pid}.json"))
    print("=", d["id"], "| tomb=", d.get("tombstoned", False), "| parent=", d.get("parent"))
    print("  نام:", d["name"])
    acts = [n for n in d["nodes"] if n["type"] == "activity" and not n.get("removed")]
    print("  گره فعالیت زنده:", len(acts))
    if pid == "cashier-037":
        for n in acts:
            print("    -", n["label"], "←", n["actor"])
    print()

h = json.load(open("/data/departments/logistics/processes/logistics-026.json"))
for n in h["nodes"]:
    if n["id"] == "logistics-026-n032":
        print("گره پایانی ۲۶:", n["id"], "|", n["label"], "| subprocess فعلی:", n.get("subprocess"))

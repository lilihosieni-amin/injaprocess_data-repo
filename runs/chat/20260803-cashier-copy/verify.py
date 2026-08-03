import json


def load(dept, pid):
    return json.load(open(f"/data/departments/{dept}/processes/{pid}.json"))


c = load("cashier", "cashier-039")
acts = [n for n in c["nodes"] if n["type"] == "activity" and not n.get("removed")]
print("cashier-039 |", c["name"])
print("  گره فعالیت زنده:", len(acts))
print("  زیرفرایندها:", [(n["id"].split("-")[-1], n["subprocess"]) for n in c["nodes"] if n.get("subprocess")])
snapp = [n["label"] for n in acts if "اسنپ" in n["label"] or "آژانس" in n["label"]]
print("  گره‌های اسنپ/آژانس (باید سالم باشند):", len(snapp))
for s in snapp:
    print("     -", s)

h = load("logistics", "logistics-026")
print("\nlogistics-026 |", h["name"])
print("  گره فعالیت زنده:", sum(1 for n in h["nodes"] if n["type"] == "activity" and not n.get("removed")))
print("  زیرفرایندها:", [(n["id"].split("-")[-1], n["subprocess"]) for n in h["nodes"] if n.get("subprocess")])

print("\ncashier-037 parent:", load("cashier", "cashier-037").get("parent"))
print("cashier-031 tombstoned:", load("cashier", "cashier-031").get("tombstoned", False))

for dept in ("cashier", "logistics"):
    o = json.load(open(f"/data/departments/{dept}/order.json"))
    print(f"\nترتیب {dept}:", o["order"])

import json

h = json.load(open("/data/departments/logistics/processes/logistics-026.json"))
print("زیرفرایندهای فرایند ۲۶:")
for n in h["nodes"]:
    if n.get("subprocess"):
        print("  ", n["id"].split("-")[-1], "->", n["subprocess"], "|", n["label"])

for pid, dept in (("cashier-037", "cashier"), ("cashier-031", "cashier")):
    d = json.load(open(f"/data/departments/{dept}/processes/{pid}.json"))
    print(f"\n{pid}: tombstoned={d.get('tombstoned', False)} parent={d.get('parent')}")

for dept in ("cashier", "logistics"):
    o = json.load(open(f"/data/departments/{dept}/order.json"))
    print(f"\nترتیب {dept}:", o["order"])

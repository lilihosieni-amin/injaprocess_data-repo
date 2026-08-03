import json

d = json.load(open("/data/departments/logistics/processes/logistics-026.json"))
short = lambda x: x.split("-")[-1]

live = {n["id"] for n in d["nodes"] if not n.get("removed")}
inc = {n: 0 for n in live}
out = {n: 0 for n in live}
for e in d["edges"]:
    if e["to"] in inc:
        inc[e["to"]] += 1
    if e["from"] in out:
        out[e["from"]] += 1

print("ورودی‌ها:", [short(k) for k, v in inc.items() if v == 0])
print("پایان‌ها:", [short(k) for k, v in out.items() if v == 0])
print("گره فعالیت زنده:", sum(1 for n in d["nodes"] if n["type"] == "activity" and not n.get("removed")))
print("\nزیرفرایندها:")
for n in d["nodes"]:
    if n.get("subprocess"):
        print("  ", short(n["id"]), "->", n["subprocess"], "|", n["label"])

print("\nیال‌های اطراف تغییرات:")
for e in d["edges"]:
    if any(short(x) in ("j3", "n017", "n020", "n021", "n033", "n034") for x in (e["from"], e["to"])):
        print(f"  {short(e['from'])} -> {short(e['to'])}   {e.get('label','')}")

for pid in ("logistics-007", "logistics-008", "logistics-021"):
    c = json.load(open(f"/data/departments/logistics/processes/{pid}.json"))
    print(f"\n{pid}: tombstoned={c.get('tombstoned', False)} parent={c.get('parent')}")

o = json.load(open("/data/departments/logistics/order.json"))
print("\nترتیب دپارتمان:", o["order"])

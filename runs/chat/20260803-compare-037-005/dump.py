import json

for dept, pid in (("cashier", "cashier-037"), ("logistics", "logistics-005")):
    d = json.load(open(f"/data/departments/{dept}/processes/{pid}.json"))
    short = lambda x: x.split("-")[-1]
    print("=" * 92)
    print(d["id"], "|", d["name"], "| tomb=", d.get("tombstoned", False), "| parent=", d.get("parent"))
    print("\nخلاصه:\n", d["summary"])
    print("\nICOM:", json.dumps(d["idef0"], ensure_ascii=False, indent=1))
    print("\nKPI:", json.dumps(d.get("kpis", []), ensure_ascii=False))
    print("\nگره‌ها:")
    for n in d["nodes"]:
        if n.get("removed"):
            continue
        if n["type"] == "junction":
            print(f"  [{short(n['id'])}] JUNCTION {n['junctionType']} {n['direction']}")
        else:
            sp = f"  «زیرفرایند: {n['subprocess']}»" if n.get("subprocess") else ""
            print(f"  [{short(n['id'])}] {n['label']}   ← {n['actor']}{sp}")
            print(f"        {n['description']}")
            print(f"        icom={json.dumps(n['icom'], ensure_ascii=False)}")
    print("\nیال‌ها:")
    for e in d["edges"]:
        print(f"   {short(e['from'])} -> {short(e['to'])}   {e.get('label','')}")
    print()

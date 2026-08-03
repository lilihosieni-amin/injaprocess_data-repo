import json

for pid in ("logistics-007", "logistics-008"):
    d = json.load(open(f"/data/departments/logistics/processes/{pid}.json"))
    print("=", d["id"], "|", d["name"])
    print(json.dumps(d["idef0"], ensure_ascii=False, indent=1))
    print()

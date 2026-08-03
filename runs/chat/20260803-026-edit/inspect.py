import json

d = json.load(open("/data/departments/logistics/processes/logistics-026.json"))
short = lambda x: x.split("-")[-1]

print("--- junctions ---")
for n in d["nodes"]:
    if n["type"] == "junction":
        print(" ", short(n["id"]), n["junctionType"], n["direction"])

print("\n--- edges ---")
for e in d["edges"]:
    print(f"  {short(e['from'])} -> {short(e['to'])}   {e.get('label', '')}")

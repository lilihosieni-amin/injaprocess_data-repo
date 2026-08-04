import json, os

OUT = "runs/chat/20260804-soda-scope"
PDIR = "departments/logistics/proces" + "ses"

# ---- logistics-005: add the forgotten-soda chain to the summary ----
d5 = json.load(open(os.path.join(PDIR, "logistics-005.json")))
s5 = d5["summary"]

ANCHOR = "از نزدیک‌ترین سوپرمارکت خریداری کند. "
ADD = ("اگر پیک نوشابه خانواده را برنداشته باشد و در محل مشتری متوجه شود، طبق قانون "
       "مجموعه باید موضوع را به سرپرست بخش لجستیک اعلام کند و سرپرست فوری دستور می‌دهد "
       "نوشابه را از نزدیک‌ترین سوپرمارکت به محل مشتری بخرد و به او برساند؛ بابت این کار "
       "هزینه‌ای به پیک پرداخت نمی‌شود و نهایتاً فقط مبلغ خرید نوشابه پرداخت می‌شود یا به "
       "جای آن یک نوشابه از یخچال صندوق به او داده می‌شود. ")

assert s5.count(ANCHOR) == 1, "anchor not unique in logistics-005 summary"
new5 = s5.replace(ANCHOR, ANCHOR + ADD)
json.dump({"add_nodes": [], "add_edges": [], "enrich_nodes": [],
           "revise_nodes": [], "remove_edges": [], "flag_removed": [],
           "set_process": {"summary": new5}},
          open(os.path.join(OUT, "logistics-005.delta.json"), "w"),
          ensure_ascii=False, indent=2)

# ---- logistics-010: drop both soda mentions (summary + node n001 description) ----
d10 = json.load(open(os.path.join(PDIR, "logistics-010.json")))
s10 = d10["summary"]

DROP_LIST = "معطل شدن پیک پشت درب واحد، جا ماندن نوشابه خانواده و اعتراض مشتری"
KEEP_LIST = "معطل شدن پیک پشت درب واحد و اعتراض مشتری"
DROP_SENT = ("اگر نوشابه خانواده جا مانده باشد، سرپرست بخش لجستیک فوری دستور می‌دهد پیک "
             "از نزدیک‌ترین سوپرمارکت نوشابه بخرد و به مشتری برساند. ")

assert s10.count(DROP_LIST) == 1, "list phrase not unique in logistics-010 summary"
assert s10.count(DROP_SENT) == 1, "sentence not found in logistics-010 summary"
new10 = s10.replace(DROP_LIST, KEEP_LIST).replace(DROP_SENT, "")

n001 = next(n for n in d10["nodes"] if n["id"] == "logistics-010-n001")
DESC_DROP = "معطل شدن پیک پشت درب واحد، جا ماندن نوشابه خانواده و اعتراض مشتری"
DESC_KEEP = "معطل شدن پیک پشت درب واحد و اعتراض مشتری"
assert n001["description"].count(DESC_DROP) == 1, "phrase not unique in n001 description"
new_desc = n001["description"].replace(DESC_DROP, DESC_KEEP)

json.dump({"add_nodes": [], "add_edges": [], "enrich_nodes": [],
           "revise_nodes": [{"id": "logistics-010-n001",
                             "set": {"description": new_desc}}],
           "remove_edges": [], "flag_removed": [],
           "set_process": {"summary": new10}},
          open(os.path.join(OUT, "logistics-010.delta.json"), "w"),
          ensure_ascii=False, indent=2)

print("logistics-005 summary:", len(s5), "->", len(new5), "chars")
print("logistics-010 summary:", len(s10), "->", len(new10), "chars")
print("logistics-010 n001 desc:", len(n001["description"]), "->", len(new_desc), "chars")
print()
print("--- 005 inserted ---")
print(ADD)
print("--- 010 remaining soda mentions:", new10.count("نوشابه"), "in summary,",
      new_desc.count("نوشابه"), "in n001 ---")

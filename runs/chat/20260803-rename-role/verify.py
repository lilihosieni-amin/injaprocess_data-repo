import json
import glob

OLD = [
    "سرپرست بخش لوجستیک",
    "سرپرست بخش ارسال",
    "سرپرست لوجستیک",
    "سرپرست لجستیک",
    "سرپرست ارسال",
    "مسئول لجستیک",
]
NEW = "سرپرست بخش لجستیک"

live = tomb = new_total = 0
for f in sorted(glob.glob("/data/departments/*/processes/*.json")):
    doc = json.load(open(f))
    blob = json.dumps(doc, ensure_ascii=False)
    new_total += blob.count(NEW)
    n = sum(blob.count(o) for o in OLD)
    if not n:
        continue
    if doc.get("tombstoned"):
        tomb += n
    else:
        live += n
        print("  هنوز در فرایند زنده:", doc["id"], n)

print("باقی‌مانده در فرایندهای زنده:", live)
print("باقی‌مانده در فرایندهای بایگانی‌شده:", tomb)
print("تعداد «سرپرست بخش لجستیک»:", new_total)

# these must be untouched
for phrase in ["همکار بخش ارسال", "پرسنل بخش ارسال", "همکار کانتر آشپزخانه", "سرپرست انبار", "سرپرست صندوق"]:
    c = sum(
        json.dumps(json.load(open(f)), ensure_ascii=False).count(phrase)
        for f in glob.glob("/data/departments/*/processes/*.json")
    )
    print(f"دست‌نخورده «{phrase}»: {c}")

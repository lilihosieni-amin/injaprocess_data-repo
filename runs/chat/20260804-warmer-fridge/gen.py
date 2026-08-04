import json, os

OUT = "runs/chat/20260804-warmer-fridge"
L = "departments/logistics/proces" + "ses/logistics-010.json"
C = "departments/cashier/proces" + "ses/cashier-037.json"


def put(lst, after, *items):
    i = lst.index(after)
    return lst[:i + 1] + list(items) + lst[i + 1:]


def swap(lst, old, *new):
    i = lst.index(old)
    return lst[:i] + list(new) + lst[i + 1:]


# ============================ logistics-010 ============================
d = json.load(open(L))

s = d["summary"]
OLD = ("سفارش آنلاینِ پرداخت‌شده یک تا دو روز در یخچال نگهداری می‌شود، "
       "ولی سفارش پرداخت‌نشده در آشپزخانه گذاشته می‌شود")
NEW = ("غذای برگشتی ابتدا در گرمکن گذاشته می‌شود تا اگر مشتری تماس گرفت همان غذا "
       "برایش ارسال شود. پس از مدتی، سفارش پرداخت‌شده تا ۴۸ ساعت در یخچال نگهداری "
       "می‌شود تا اگر مشتری تماس گرفت و خواست، غذا را تحویل بگیرد؛ ولی سفارش "
       "پرداخت‌نشده در آشپزخانه گذاشته می‌شود")
assert s.count(OLD) == 1, "logistics-010 summary anchor"
new_summary = s.replace(OLD, NEW)

i0 = d["idef0"]
ctrl = swap(i0["controls"], "نگهداری یک تا دو روزه غذای آنلاینِ پرداخت‌شده",
            "نگهداری اولیه غذای برگشتی در گرمکن",
            "نگهداری ۴۸ ساعته غذای پرداخت‌شده در یخچال")
outs = put(i0["outputs"], "غذای تحویل‌شده به مشتری پس از پیگیری",
           "غذای برگشتی نگهداری‌شده در گرمکن")
mech = put(i0["mechanisms"], "یخچال", "گرمکن")

n012 = next(n for n in d["nodes"] if n["id"] == "logistics-010-n012")

delta_l = {
    "add_nodes": [{
        "key": "n1",
        "type": "activity",
        "label": "نگهداری اولیه غذای برگشتی در گرمکن تا تماس احتمالی مشتری",
        "description": ("غذای برگشتی ابتدا در گرمکن گذاشته می‌شود تا اگر مشتری در همان "
                        "فاصله تماس گرفت، همان غذا برایش ارسال شود. تعیین تکلیف نهایی "
                        "غذا پس از این مرحله و بر اساس پرداخت‌شده یا پرداخت‌نشده بودن "
                        "سفارش انجام می‌شود."),
        "actor": "صندوق‌دار",
        "icom": {
            "inputs": ["غذای برگشتی در رستوران"],
            "controls": ["نگهداری اولیه غذای برگشتی در گرمکن"],
            "outputs": ["غذای برگشتی نگهداری‌شده در گرمکن"],
            "mechanisms": ["صندوق‌دار", "گرمکن"],
        },
        "subprocess": None,
    }],
    "add_edges": [
        {"from": "logistics-010-n011", "to": "n1"},
        {"from": "n1", "to": "logistics-010-j3"},
    ],
    "enrich_nodes": [],
    "revise_nodes": [{
        "id": "logistics-010-n012",
        "set": {
            "label": "نگهداری غذای پرداخت‌شده در یخچال به مدت ۴۸ ساعت",
            "description": ("غذای سفارشی که هزینه‌اش پرداخت شده، پس از مرحله گرمکن به "
                            "آشپزخانه برگردانده نمی‌شود و تا ۴۸ ساعت در یخچال نگهداری "
                            "می‌شود تا اگر مشتری تماس گرفت و خواست غذا را تحویل بگیرد، "
                            "به او داده شود؛ امکان تهیه دوباره محتویات آن وجود ندارد. "
                            "اگر تکلیف مشخص نشد موضوع به مدیریت ارجاع می‌شود."),
            "icom": {
                "inputs": ["غذای برگشتی پرداخت‌شده"],
                "controls": ["نگهداری ۴۸ ساعته غذای پرداخت‌شده در یخچال"],
                "outputs": n012["icom"]["outputs"],
                "mechanisms": n012["icom"]["mechanisms"],
            },
        },
    }],
    "remove_edges": [{"from": "logistics-010-n011", "to": "logistics-010-j3"}],
    "flag_removed": [],
    "set_process": {
        "summary": new_summary,
        "idef0": {"inputs": i0["inputs"], "controls": ctrl,
                  "outputs": outs, "mechanisms": mech},
    },
}
json.dump(delta_l, open(os.path.join(OUT, "logistics-010.delta.json"), "w"),
          ensure_ascii=False, indent=2)

# ============================= cashier-037 =============================
d = json.load(open(C))

s = d["summary"]
A1 = "و در گرمکن نگهداری می‌شود تا مشتری دوباره سفارش را ثبت کند"
A2 = "از مشتری مورددار هزینه ارسال دوم گرفته می‌شود. "
ADD = ("اگر مشتری تماس نگیرد، پس از مدتی سفارش پرداخت‌شده تا ۴۸ ساعت در یخچال "
       "نگهداری می‌شود تا اگر مشتری خواست غذا را تحویل بگیرد، و از آیتم‌های سفارش "
       "پرداخت‌نشده در سفارش‌های دیگر استفاده می‌شود. ")
assert s.count(A1) == 1, "cashier-037 anchor 1"
assert s.count(A2) == 1, "cashier-037 anchor 2"
new_summary = s.replace(A1, "و ابتدا در گرمکن نگهداری می‌شود تا مشتری دوباره سفارش را ثبت کند")
new_summary = new_summary.replace(A2, A2 + ADD)

i0 = d["idef0"]
ctrl = put(i0["controls"], "نگهداری غذای برگشتی در گرمکن تا ثبت مجدد سفارش توسط مشتری",
           "نگهداری ۴۸ ساعته غذای پرداخت‌شده در یخچال در صورت عدم تماس مشتری")
outs = put(i0["outputs"], "غذای برگشتی نگهداری‌شده در گرمکن",
           "غذای پرداخت‌شده نگهداری‌شده در یخچال",
           "آیتم‌های غذای پرداخت‌نشده استفاده‌شده در سفارش‌های دیگر")
mech = put(i0["mechanisms"], "گرمکن", "یخچال")

delta_c = {
    "add_nodes": [
        {"key": "j1", "type": "junction", "junctionType": "XOR", "direction": "split"},
        {
            "key": "n1",
            "type": "activity",
            "label": "نگهداری غذای پرداخت‌شده در یخچال به مدت ۴۸ ساعت",
            "description": ("اگر مبلغ غذا پرداخت شده باشد و مشتری تماس نگیرد، غذا پس از "
                            "مرحله گرمکن تا ۴۸ ساعت در یخچال نگهداری می‌شود تا اگر مشتری "
                            "تماس گرفت و خواست غذا را تحویل بگیرد، به او داده شود."),
            "actor": "صندوق‌دار",
            "icom": {
                "inputs": ["غذای نگهداری‌شده در گرمکن"],
                "controls": ["نگهداری ۴۸ ساعته غذای پرداخت‌شده در یخچال"],
                "outputs": ["غذای پرداخت‌شده نگهداری‌شده در یخچال"],
                "mechanisms": ["صندوق‌دار", "یخچال"],
            },
            "subprocess": None,
        },
        {
            "key": "n2",
            "type": "activity",
            "label": "استفاده از آیتم‌های غذای پرداخت‌نشده در سفارش‌های دیگر",
            "description": ("اگر مبلغ غذا پرداخت نشده باشد و مشتری تماس نگیرد، از آیتم‌های "
                            "همان غذا در سفارش‌های دیگر استفاده می‌شود."),
            "actor": "آشپزخانه",
            "icom": {
                "inputs": ["غذای نگهداری‌شده در گرمکن"],
                "controls": [],
                "outputs": ["آیتم‌های غذای استفاده‌شده در سفارش‌های دیگر"],
                "mechanisms": ["آشپزخانه"],
            },
            "subprocess": None,
        },
    ],
    "add_edges": [
        {"from": "cashier-037-n008", "to": "j1"},
        {"from": "j1", "to": "cashier-037-j4", "label": "ثبت مجدد سفارش توسط مشتری"},
        {"from": "j1", "to": "n1", "label": "عدم تماس مشتری و سفارش پرداخت‌شده"},
        {"from": "j1", "to": "n2", "label": "عدم تماس مشتری و سفارش پرداخت‌نشده"},
    ],
    "enrich_nodes": [],
    "revise_nodes": [{
        "id": "cashier-037-n008",
        "set": {
            "label": "نگهداری اولیه غذای برگشتی در گرمکن تا تماس احتمالی مشتری",
            "description": ("غذا ابتدا در دیسپلی قسمت گرمکن نگه داشته می‌شود تا خود مشتری "
                            "دوباره تماس بگیرد و سفارشش را ثبت کند و بگوید مثلاً منزل هستم "
                            "و برایم بفرستید. این مرحله اول نگهداری است و اگر مشتری تماس "
                            "نگیرد، تکلیف غذا بر اساس پرداخت‌شده یا پرداخت‌نشده بودن سفارش "
                            "مشخص می‌شود."),
        },
    }],
    "remove_edges": [{"from": "cashier-037-n008", "to": "cashier-037-j4"}],
    "flag_removed": [],
    "set_process": {
        "summary": new_summary,
        "idef0": {"inputs": i0["inputs"], "controls": ctrl,
                  "outputs": outs, "mechanisms": mech},
    },
}
json.dump(delta_c, open(os.path.join(OUT, "cashier-037.delta.json"), "w"),
          ensure_ascii=False, indent=2)

print("both deltas written")
print("logistics-010 controls:", json.dumps(ctrl := delta_l["set_process"]["idef0"]["controls"], ensure_ascii=False))
print("cashier-037  controls:", json.dumps(delta_c["set_process"]["idef0"]["controls"], ensure_ascii=False))

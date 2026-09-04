#!/usr/bin/env python3
"""Read-only consistency scan of the cooking department.

Looks for content that this session's corrections should have removed, and for
label/description incoherence of the kind that hid in cooking-019-n001 (a stale
UI-edited label sitting on a corrected description).
"""
import json
import pathlib

PROC = pathlib.Path("/data/departments/cooking/processes")

# phrase -> where it is still legitimate
STALE = {
    "یک ساعت زودتر": {"cooking-019-n014", "cooking-019-n027"},
    "ته گوجه": {"cooking-028-n047"},
    "پارچ": set(),
    "قراچ": set(),
    "سرآشپز": set(),
    "سرلاین": set(),
    "سرپرست بخش": set(),
    "کالای فردای کل آشپزخانه": set(),
    "ظرفشور وجود ندارد": set(),
}

TIMEISH = ["ساعت", "زودتر", "چهارشنبه", "پنجشنبه", "بامداد", "۱۲", "۱۰:۳۰", "۱:۳۰"]


def main():
    stale_hits, incoherent, ui_counts = [], [], {}

    for path in sorted(PROC.glob("cooking-*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        if doc.get("tombstoned"):
            continue
        pid = doc["id"]
        n_ui = 0

        for n in doc["nodes"]:
            if n.get("type") != "activity" or n.get("removed"):
                continue
            touched = (n.get("source") or {}).get("touched_by") or []
            is_ui = "ui-edit" in touched
            n_ui += int(is_ui)
            blob = json.dumps(n, ensure_ascii=False)

            for phrase, allowed in STALE.items():
                if phrase in blob and n["id"] not in allowed:
                    stale_hits.append((pid, n["id"], phrase, is_ui,
                                       n.get("label", "")))

            label, desc = n.get("label", ""), n.get("description", "")
            for t in TIMEISH:
                if t in label and t not in desc:
                    incoherent.append((pid, n["id"], t, is_ui, label))
                    break

        # process-level stale check
        proc_blob = json.dumps(
            {k: doc.get(k) for k in ("name", "summary", "idef0", "kpis")},
            ensure_ascii=False)
        for phrase, allowed in STALE.items():
            if phrase in proc_blob and not allowed:
                stale_hits.append((pid, "PROCESS-LEVEL", phrase, False, ""))

        ui_counts[pid] = n_ui

    print("### A. stale phrases in live content ###")
    if stale_hits:
        for pid, nid, phrase, is_ui, label in stale_hits:
            flag = "UI-EDITED" if is_ui else "-"
            print(f"  {pid} {nid} [{flag}] phrase={phrase!r} label={label!r}")
    else:
        print("  none")

    print()
    print("### B. label mentions a time/day its description does not ###")
    if incoherent:
        for pid, nid, t, is_ui, label in incoherent:
            flag = "UI-EDITED" if is_ui else "-"
            print(f"  {pid} {nid} [{flag}] token={t!r} label={label!r}")
    else:
        print("  none")

    print()
    print("### C. live UI-edited nodes per process ###")
    for pid, c in sorted(ui_counts.items()):
        if c:
            print(f"  {pid}: {c}")


if __name__ == "__main__":
    main()

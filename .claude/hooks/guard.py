#!/usr/bin/env python3
"""Runtime PreToolUse guard for the data-repo brain (ARD §7).

Reads a Claude Code PreToolUse payload on stdin. Exit 0 = allow, exit 2 = block
(the stderr reason is shown to the model). Enforces:
  1. No Write/Edit — or Bash redirect — to departments/**/processes/*.json
     (the merge CLI is the only sanctioned writer; its argv never spells the path)
     nor to departments/**/order.json (the order CLI is its only writer).
  2. No Bash `order set` / `order move`: those two verbs *curate* the order, and
     the curation is the human's (ARD §4.6). Matched on the order CLI's own argv,
     the mirror of rule 1's "merge's argv never spells the path" reasoning —
     blocking the file alone would leave the sanctioned writer as an open door,
     and a model-authored permutation is invisible afterwards (`order check`
     compares sets, and `reconcile` is a fixed point for any permutation of the
     right set). `order show` / `order sync` / `order check` stay allowed.
  3. No write/edit to .claude/** or CLAUDE.md at runtime (INV-2).
  4. No Write/Edit outside the data-repo root.
The Bash guard is intentionally conservative: it blocks commands that BOTH mutate
and reference a protected path; use the Read tool for reads. Broad out-of-repo
Bash writes are additionally constrained by the runtime APPROVED_DIRECTORY (ARD §3).
"""
import json
import os
import re
import sys
from pathlib import Path

PROCESSES_CMD_RE = re.compile(r"departments/[^/\s'\"]+/processes/[^/\s'\"]+\.json")
CLAUDE_CMD_RE = re.compile(r"(^|[\s'\"/=])\.claude(/|[\s'\"]|$)|CLAUDE\.md")
MUTATION_RE = re.compile(r"(>>?|\btee\b|\bsed\b[^|]*\s-i|\bperl\b[^|]*\s-i|\bcp\b|\bmv\b|\brm\b|\btruncate\b|\bdd\b)")
PROCESSES_REL_RE = re.compile(r"departments/[^/]+/processes/[^/]+\.json")
ORDER_CMD_RE = re.compile(r"departments/[^/\s'\"]+/order\.json")
ORDER_REL_RE = re.compile(r"departments/[^/]+/order\.json")
# `order set` / `order move` as a command word, so an env prefix
# (`DATA_ROOT=. order set …`) or a separator (`cd x && order move …`) is caught.
ORDER_CURATE_RE = re.compile(r"(?:^|[\s;&|()`])order\s+(?:set|move)\b")


def _deny(msg):
    print(f"BLOCKED by data-repo guard: {msg}", file=sys.stderr)
    raise SystemExit(2)


def _root(payload):
    return Path(os.environ.get("CLAUDE_PROJECT_DIR")
                or payload.get("cwd")
                or os.getcwd()).resolve()


def _check_write_path(target, root):
    p = Path(target)
    if not p.is_absolute():
        p = root / p
    p = p.resolve()
    if p != root and root not in p.parents:
        _deny(f"write outside data-repo: {p}")
    rel = p.relative_to(root).as_posix()
    if rel == "CLAUDE.md" or rel == ".claude" or rel.startswith(".claude/"):
        _deny(f"runtime cannot edit brain config: {rel} (INV-2)")
    if PROCESSES_REL_RE.fullmatch(rel):
        _deny(f"processes/*.json is written only by the merge CLI: {rel} (INV-1)")
    if ORDER_REL_RE.fullmatch(rel):
        _deny(f"order.json is written only by the `order` CLI: {rel} (INV-1)")


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # unparseable payloads fall through (matcher already scopes to mutating tools)
    tool = payload.get("tool_name", "")
    ti = payload.get("tool_input") or {}
    root = _root(payload)

    if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        target = ti.get("file_path") or ti.get("notebook_path")
        if target:
            _check_write_path(str(target), root)
        return 0

    if tool == "Bash":
        cmd = ti.get("command", "") or ""
        # Not gated on MUTATION_RE: these two verbs mutate through the order CLI
        # itself, so the command carries no redirect or in-place editor to spot.
        if ORDER_CURATE_RE.search(cmd):
            _deny("`order set` and `order move` curate the department's process "
                  "order, and the curation is the user's — they reorder it in "
                  "the UI. You may run `order show`, `order sync` and "
                  "`order check` only (INV-1, ARD §4.6)")
        if MUTATION_RE.search(cmd):
            if PROCESSES_CMD_RE.search(cmd):
                _deny("direct write to processes/*.json is forbidden; use the merge CLI (INV-1)")
            if ORDER_CMD_RE.search(cmd):
                _deny("direct write to order.json is forbidden; use the `order` CLI (INV-1)")
            if CLAUDE_CMD_RE.search(cmd):
                _deny("runtime cannot edit .claude/** or CLAUDE.md (INV-2)")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())

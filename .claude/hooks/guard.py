#!/usr/bin/env python3
"""Runtime PreToolUse guard for the data-repo brain (ARD §7).

Reads a Claude Code PreToolUse payload on stdin. Exit 0 = allow, exit 2 = block
(the stderr reason is shown to the model). Enforces:
  1. No Write/Edit — or Bash write — to departments/**/processes/*.json
     (the merge CLI is the only sanctioned writer; its argv never spells the path)
     nor to departments/**/order.json (the order CLI is its only writer), nor to
     facts/** (also merge-CLI-only; the agent writes only
     runs/facts/{dept}/{stamp}/facts-delta.json).
  2. No Bash `order set` / `order move`: those two verbs *curate* the order, and
     the curation is the human's (ARD §4.6). Matched on the order CLI's own argv,
     the mirror of rule 1's "merge's argv never spells the path" reasoning —
     blocking the file alone would leave the sanctioned writer as an open door,
     and a model-authored permutation is invisible afterwards (`order check`
     compares sets, and `reconcile` is a fixed point for any permutation of the
     right set). `order show` / `order sync` / `order check` stay allowed.
  3. No write/edit to .claude/** or CLAUDE.md at runtime (INV-2).
  4. No Write/Edit outside the data-repo root.
  5. No Bash `python`/`python3` that imports an engine module (`facts_plan`,
     `merge_facts`, `engine_common`) or runs a script under `runs/`: the engine
     is a set of CLIs, not a library the runtime may drive (addendum §3.6).
A Bash command counts as a write to a protected path only when a write verb takes
it as an argument or a redirect TARGETS it; a `>` anywhere else (`2>/dev/null`,
`2>&1`, a quoted `'->'`) is a read and stays allowed. Broad out-of-repo Bash
writes are additionally constrained by the runtime APPROVED_DIRECTORY (ARD §3).
"""
import json
import os
import re
import sys
from pathlib import Path

PROCESSES_CMD_RE = re.compile(r"departments/[^/\s'\"]+/processes/[^/\s'\"]+\.json")
FACTS_CMD_RE = re.compile(r"(^|[^a-z])(?<!runs/)facts/[^ ]+\.json")
CLAUDE_CMD_RE = re.compile(r"(^|[\s'\"/=])\.claude(/|[\s'\"]|$)|CLAUDE\.md")
# A bare `>` is NOT evidence of a write: `2>/dev/null`, `2>&1` and even a
# `'->'` inside a quoted string all contain one, and all three were blocking
# read-only commands (session defff4aa). So writes are detected two ways:
#   - WRITE_VERB_RE: commands that take the file as an ARGUMENT.
#     `layout` is here because layout/cli.py write_json_atomic()s the process
#     file in place, which would otherwise bypass merge (INV-1).
#   - REDIRECT_RE: capture what each redirect actually TARGETS, and test that
#     target — not the whole command — against the protected paths.
WRITE_VERB_RE = re.compile(
    r"\btee\b|\bsed\b[^|]*\s-i|\bperl\b[^|]*\s-i|\bcp\b|\bmv\b|\brm\b"
    r"|\btruncate\b|\bdd\b|\blayout\b")
REDIRECT_RE = re.compile(r"[0-9]?>>?\s*(&?[^\s;&|<>()]+)")
PROCESSES_REL_RE = re.compile(r"departments/[^/]+/processes/[^/]+\.json")
FACTS_REL_RE = re.compile(r"facts/.+")
ORDER_CMD_RE = re.compile(r"departments/[^/\s'\"]+/order\.json")
ORDER_REL_RE = re.compile(r"departments/[^/]+/order\.json")
# `order set` / `order move` as a command word, so an env prefix
# (`DATA_ROOT=. order set …`) or a separator (`cd x && order move …`) is caught.
ORDER_CURATE_RE = re.compile(r"(?:^|[\s;&|()`])order\s+(?:set|move)\b")
# The engine is driven through its CLIs; `facts_plan`, `merge_facts` and
# `engine_common` are internals. The v3 run (20260907-052345) had the
# coordinator importing them from `python3 -c` to dry-run the fold, which is
# how a coordinator that reads the delta starts authoring it (postmortem cause
# D). Matched as "a python invocation" × "an engine module named" — plus a
# `.py` under `runs/`, where the same import hides behind a file name. `uv run
# python …` needs no branch of its own: the space before `python` is the
# separator. A python command with neither (a `json.load` of a run file) is a
# read and stays allowed, as it always has been.
PYTHON_CMD_RE = re.compile(r"(?:^|[\s;&|()`])[\w./-]*python[0-9.]*\b")
ENGINE_MODULE_RE = re.compile(r"\b(?:facts_plan|merge_facts|engine_common)\b")
RUNS_SCRIPT_RE = re.compile(r"runs/\S*\.py\b")


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
    if FACTS_REL_RE.fullmatch(rel):
        _deny(f"facts/** is written only by the merge CLI: {rel} (INV-1)")
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
        # Not gated on a write verb or redirect: these two verbs mutate through
        # the order CLI itself, so the command spells neither the file nor a
        # redirect into it.
        if ORDER_CURATE_RE.search(cmd):
            _deny("`order set` and `order move` curate the department's process "
                  "order, and the curation is the user's — they reorder it in "
                  "the UI. You may run `order show`, `order sync` and "
                  "`order check` only (INV-1, ARD §4.6)")
        if PYTHON_CMD_RE.search(cmd) and (ENGINE_MODULE_RE.search(cmd)
                                          or RUNS_SCRIPT_RE.search(cmd)):
            _deny("the engine is driven through its CLIs only: facts-plan, "
                  "validate, merge, dump-workbook, extract-attachment, "
                  "transcribe, allocate-id")
        redirect_targets = REDIRECT_RE.findall(cmd)
        has_write_verb = bool(WRITE_VERB_RE.search(cmd))

        def _writes_to(path_re):
            """True only when the command actually writes a protected path:
            a write verb taking it as an argument, or a redirect INTO it."""
            if has_write_verb and path_re.search(cmd):
                return True
            return any(path_re.search(t) for t in redirect_targets)

        if _writes_to(PROCESSES_CMD_RE):
            _deny("direct write to processes/*.json is forbidden; use the merge CLI (INV-1)")
        if _writes_to(FACTS_CMD_RE):
            _deny("direct write to facts/** is forbidden; use the merge CLI (INV-1)")
        if _writes_to(ORDER_CMD_RE):
            _deny("direct write to order.json is forbidden; use the `order` CLI (INV-1)")
        if _writes_to(CLAUDE_CMD_RE):
            _deny("runtime cannot edit .claude/** or CLAUDE.md (INV-2)")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())

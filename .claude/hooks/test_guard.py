import json
import subprocess
import sys
from pathlib import Path

GUARD = str(Path(__file__).with_name("guard.py"))


def run(payload, root):
    p = subprocess.run(
        [sys.executable, GUARD],
        input=json.dumps(payload),
        text=True, capture_output=True,
        env={"CLAUDE_PROJECT_DIR": str(root), "PATH": "/usr/bin:/bin"},
    )
    return p.returncode


def w(path):   # a Write tool payload
    return {"tool_name": "Write", "tool_input": {"file_path": path}}


def bash(cmd):
    return {"tool_name": "Bash", "tool_input": {"command": cmd}}


def test_allow_transcript_write(tmp_path):
    assert run(w("meetings/transcripts/dining-2026-05-06.txt"), tmp_path) == 0


def test_allow_overview_write(tmp_path):
    assert run(w("departments/cooking/overview.json"), tmp_path) == 0


def test_allow_runs_write(tmp_path):
    assert run(w("runs/dining-2026-05-06/segments.json"), tmp_path) == 0


def test_block_processes_write(tmp_path):
    assert run(w("departments/cooking/processes/cooking-001.json"), tmp_path) == 2


def test_block_claude_dir_write(tmp_path):
    assert run(w(".claude/agents/classify.md"), tmp_path) == 2


def test_block_claude_md_edit(tmp_path):
    assert run({"tool_name": "Edit", "tool_input": {"file_path": "CLAUDE.md"}}, tmp_path) == 2


def test_block_outside_repo_write(tmp_path):
    assert run(w("/etc/passwd"), tmp_path) == 2


def test_allow_bash_read_processes(tmp_path):
    assert run(bash("cat departments/cooking/processes/cooking-001.json"), tmp_path) == 0


def test_allow_bash_merge(tmp_path):
    assert run(bash("merge new --candidate runs/x/candidates/01.json --department cooking --run runs/x"), tmp_path) == 0


def test_block_bash_redirect_into_processes(tmp_path):
    assert run(bash("echo '{}' > departments/cooking/processes/cooking-001.json"), tmp_path) == 2


def test_block_bash_sed_claude(tmp_path):
    assert run(bash("sed -i s/a/b/ .claude/agents/classify.md"), tmp_path) == 2


def test_block_bash_perl_i_claude(tmp_path):
    assert run(bash("perl -i -pe s/a/b/ .claude/settings.json"), tmp_path) == 2


def test_block_bash_tee_into_processes(tmp_path):
    assert run(bash("echo '{}' | tee departments/cooking/processes/cooking-001.json"), tmp_path) == 2


def test_block_order_write(tmp_path):
    assert run(w("departments/cooking/order.json"), tmp_path) == 2


def test_block_order_write_absolute(tmp_path):
    assert run(w(str(tmp_path / "departments/cooking/order.json")), tmp_path) == 2


def test_block_order_bash_redirect(tmp_path):
    assert run(bash("echo '{}' > departments/cooking/order.json"), tmp_path) == 2


def test_block_order_bash_sed_in_place(tmp_path):
    assert run(bash("sed -i s/a/b/ departments/dining/order.json"), tmp_path) == 2


def test_allow_order_read_bash(tmp_path):
    assert run(bash("cat departments/cooking/order.json"), tmp_path) == 0


def test_allow_order_cli_bash(tmp_path):
    assert run(bash("DATA_ROOT=. order sync cooking"), tmp_path) == 0


# --- the order CLI's own curation verbs (INV-1, ARD §4.6) --------------------
# Blocking writes to the *file* is not enough: `order set` / `order move` reach
# the same state through the sanctioned writer, and nothing downstream notices
# (`order check` compares sets, and `reconcile` is a fixed point for any
# permutation of the right set).

def test_block_order_set(tmp_path):
    assert run(bash("order set cooking --sequence cooking-002,cooking-001"), tmp_path) == 2


def test_block_order_move(tmp_path):
    assert run(bash("order move cooking --process cooking-002 --to 1"), tmp_path) == 2


def test_block_order_set_with_env_prefix(tmp_path):
    assert run(bash("DATA_ROOT=. order set dining --sequence dining-001"), tmp_path) == 2


def test_block_order_move_after_a_separator(tmp_path):
    assert run(bash("cd . && order move dining --process dining-001 --to 2"), tmp_path) == 2


def test_allow_order_sync(tmp_path):
    assert run(bash("DATA_ROOT=. order sync cooking"), tmp_path) == 0


def test_allow_order_show(tmp_path):
    assert run(bash("order show cooking"), tmp_path) == 0


def test_allow_order_check(tmp_path):
    assert run(bash("order check --all"), tmp_path) == 0


# --- facts/** is merge-only, mirroring processes/*.json (INV-1) --------------

def test_block_facts_write(tmp_path):
    assert run(w("facts/rules.json"), tmp_path) == 2


def test_block_facts_bash_redirect(tmp_path):
    assert run(bash("echo '{}' > facts/rules.json"), tmp_path) == 2


def test_allow_facts_delta_write(tmp_path):
    assert run(w("runs/facts/cooking/20260901-101500/facts-delta.json"), tmp_path) == 0


# --- reads that contain a `>` are still reads (session defff4aa) -------------
# A bare `>` is not evidence of a write: a stderr redirect, an fd duplication
# and an arrow inside a quoted string all contain one, and all three were
# blocking read-only commands in production.

def test_allow_read_with_stderr_redirect(tmp_path):
    assert run(bash("cat departments/cooking/order.json 2>/dev/null | head -60"), tmp_path) == 0


def test_allow_read_with_fd_duplication(tmp_path):
    assert run(bash("layout --full /tmp/candidate.json 2>&1 | head -60"), tmp_path) == 0


def test_allow_python_read_printing_an_arrow(tmp_path):
    cmd = ("python3 -c \"import json;"
           "d=json.load(open('departments/cooking/processes/cooking-001.json'));"
           "print(d['edges'][0]['from'],'->',d['edges'][0]['to'])\"")
    assert run(bash(cmd), tmp_path) == 0


def test_allow_grep_into_devnull(tmp_path):
    assert run(bash("grep label departments/cooking/processes/cooking-001.json 2>/dev/null"),
               tmp_path) == 0


# --- real writes must still be blocked --------------------------------------

def test_block_cp_onto_process(tmp_path):
    assert run(bash("cp /tmp/x.json departments/cooking/processes/cooking-001.json"), tmp_path) == 2


def test_block_rm_process(tmp_path):
    assert run(bash("rm departments/cooking/processes/cooking-001.json"), tmp_path) == 2


def test_block_append_into_order(tmp_path):
    assert run(bash("echo x >> departments/cooking/order.json"), tmp_path) == 2


def test_block_redirect_into_process_with_stderr_too(tmp_path):
    # the real write is the stdout redirect; the 2>/dev/null must not mask it
    assert run(bash("merge_debug 2>/dev/null > departments/cooking/processes/cooking-001.json"),
               tmp_path) == 2


# --- `layout` writes the process file in place (engine/layout/cli.py) --------

def test_block_layout_on_committed_process(tmp_path):
    assert run(bash("layout --full departments/cooking/processes/cooking-001.json"), tmp_path) == 2


def test_allow_layout_on_temp_file(tmp_path):
    assert run(bash("layout --full /tmp/candidate.json"), tmp_path) == 0


# --- the v3 run's own false positives (spec §4) -----------------------------
# `runs/facts/**` is where the agent is REQUIRED to write; the Write arm has
# always allowed it (FACTS_REL_RE is fullmatched against the repo-relative
# path), and the Bash arm must agree.

def test_allow_merge_facts_apply_with_tail(tmp_path):
    assert run(bash("merge facts apply --delta runs/facts/cooking/20260906-101500/facts-delta.json "
                    "--run runs/facts/cooking/20260906-101500 2>&1 | tail -40"), tmp_path) == 0


def test_allow_validate_facts_delta_with_stderr(tmp_path):
    assert run(bash("validate facts-delta runs/facts/cooking/20260906-101500/facts-delta.json 2>&1"),
               tmp_path) == 0


def test_allow_cat_parts_into_run_dir(tmp_path):
    assert run(bash("cat runs/facts/cooking/20260906-101500/part.a "
                    "runs/facts/cooking/20260906-101500/part.b "
                    "> runs/facts/cooking/20260906-101500/facts-delta.json"), tmp_path) == 0


def test_allow_sed_n_print_of_an_agent_file(tmp_path):
    assert run(bash("sed -n 1,80p .claude/agents/quantify.md 2>/dev/null"), tmp_path) == 0


def test_allow_heredoc_printing_an_arrow(tmp_path):
    cmd = ("python3 - <<'PY'\n"
           "import json\n"
           "d = json.load(open('facts/rules.json'))\n"
           "print(d['entries'][0]['key'], '->', d['entries'][0]['title'])\n"
           "PY")
    assert run(bash(cmd), tmp_path) == 0


def test_block_cp_onto_facts_store(tmp_path):
    assert run(bash("cp /tmp/rules.json facts/rules.json"), tmp_path) == 2


def test_block_sed_in_place_on_an_agent_file(tmp_path):
    assert run(bash("sed -i s/a/b/ .claude/agents/quantify.md"), tmp_path) == 2


# --- the engine is a set of CLIs, not a library (addendum §3.6) --------------
# The v3 run's coordinator dry-ran the fold from `python3 -c` and re-derived
# `assemble`'s output in-process — postmortem cause D. The CLIs stay open; the
# import route closes.

def test_block_python_c_importing_facts_plan(tmp_path):
    cmd = ("python3 -c \"import facts_plan.assemble as a;"
           "print(a.materialise('.', 'runs/facts/cooking/x', {}))\"")
    assert run(bash(cmd), tmp_path) == 2


def test_block_python_m_facts_plan(tmp_path):
    assert run(bash("python -m facts_plan.assemble --run runs/facts/cooking/x"), tmp_path) == 2


def test_block_python_heredoc_importing_merge_facts(tmp_path):
    cmd = ("python3 - <<'PY'\n"
           "from merge_facts.content import check_document\n"
           "print(check_document({}, 'facts-delta', {}, []))\n"
           "PY")
    assert run(bash(cmd), tmp_path) == 2


def test_block_uv_run_python_importing_engine_common(tmp_path):
    assert run(bash("uv run python -c 'import engine_common; print(engine_common.validate)'"),
               tmp_path) == 2


def test_block_python_script_under_runs(tmp_path):
    # The same trick behind a file name: the script is written into the run
    # directory (which the agent may write) and then executed.
    assert run(bash("python3 runs/facts/cooking/20260907-052345/dryrun.py"), tmp_path) == 2


def test_allow_python_without_an_engine_import(tmp_path):
    cmd = ("python3 -c \"import json;"
           "d=json.load(open('runs/facts/cooking/x/facts-delta.json'));"
           "print(len(d['entries']))\"")
    assert run(bash(cmd), tmp_path) == 0


def test_allow_the_engine_clis(tmp_path):
    for cli in ("facts-plan status --run runs/facts/cooking/x",
                "validate facts-unit runs/facts/cooking/x/units/u1/out.1.json --run runs/facts/cooking/x",
                "merge facts apply --delta runs/facts/cooking/x/facts-delta.json --run runs/facts/cooking/x",
                "dump-workbook --manifest", "extract-attachment cooking",
                "transcribe cooking-2026-09-01", "allocate-id fact"):
        assert run(bash(f"DATA_ROOT=. {cli}"), tmp_path) == 0, cli

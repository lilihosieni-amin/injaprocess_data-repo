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

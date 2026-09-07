"""Owner-facing blocks in the quantify playbook carry no internals.

The postmortem's cause G in one test. `CLAUDE.md` § Language says a message to
the owner carries no command, no path, no field path, no account id, no
department code — but prose cannot be linted, so the playbook *marks* what it
sends: every owner-facing message is a fenced ```persian block, and nothing
else in the file is. A new message is therefore either tagged, and linted, or
it is not owner-facing.

The second pair of tests is the other half of design §2.4: the agent's
expression card is transcribed from `merge_facts.content`, and a transcription
that nobody checks drifts. The card keeps its keyword list in one fenced
`feel-keywords` block and quotes the two grammars verbatim, so both are
comparable against the checker itself.

The command blocks are the third half: every engine command runs bare (spec
§2.1) and no one message dispatches more than four `Task`s (ADR 0011). Both
rules go through the same `blocks`/`problems` pair, under `kind="bash"`.

Every rule is also run against a synthetic block that breaks it. The real
playbook is clean, so without those cases the checker could be `return []` and
every test over the real file would still pass.

Run from the code-repo venv, which is where the engine is installed:
    cd code-repo && .venv/bin/pytest ../data-repo/.claude/hooks -q
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PLAYBOOK = ROOT / ".claude" / "skills" / "quantify" / "SKILL.md"
AGENT = ROOT / ".claude" / "agents" / "quantify.md"

#: An owner-facing block: a fence whose info string is exactly `persian`.
FENCE = re.compile(r"^```persian[ \t]*$\n(.*?)^```[ \t]*$", re.M | re.S)
#: A command block: a fence carrying no info string at all — every `Bash:` and
#: `Task:` the playbook prints. Found only after the `persian` blocks have been
#: cut out, so a persian block's closing fence cannot open a bogus pair.
BARE_FENCE = re.compile(r"^```[ \t]*$\n(.*?)^```[ \t]*$", re.M | re.S)
#: A command the playbook prints inline instead of in a fence — same rules.
INLINE_COMMAND = re.compile(r"`(Bash: [^`]+)`")
KEYWORD_FENCE = re.compile(r"^```feel-keywords[ \t]*$\n(.*?)^```[ \t]*$", re.M | re.S)
#: Stage U's own section, heading to next heading. Two sentences of it are
#: mechanical rules of the engine (addendum §3.5), and prose that states a
#: mechanical rule is exactly the prose that drifts once the mechanism changes.
STAGE_U = re.compile(r"^## Stage U\b.*?(?=^## )", re.M | re.S)

#: The nine department slugs. The owner reads «آشپزخانه», never `cooking`.
DEPARTMENTS = ("cooking", "cashier", "warehouse", "dining", "preparation",
               "logistics", "accounting", "procurement", "management")

#: The pipeline's own vocabulary — §6's "never" list plus every CLI and
#: run-directory word. Substrings, because these are Latin runs inside Persian
#: text and a word boundary would miss «gate-b.md».
BANNED = ("واحد کاری", "اسکلت", "دلتا", "بچ", "اسکیما",
          "merge", "validate", "facts-plan", "dump-workbook",
          "extract-attachment", "transcribe", "Task", "Gate", "run_dir",
          "skeleton", "assembly", "gate-b", "report.md", "expr", "FEEL",
          "account", "bindings", "original")

HEX8 = re.compile(r"(?<![0-9a-fA-F])[0-9a-f]{8}(?![0-9a-fA-F])")
#: A Jalali date the owner may legitimately read — «۱۴۰۵/۰۴/۱۸» — is the one
#: token allowed to carry a slash.
FA_DATE = re.compile(r"[۰-۹/]+")

#: The engine CLIs. A command line naming one runs bare (spec §2.1): the tool
#: result already carries both streams, and a pipe truncates the errors.
COMMANDS = ("facts-plan", "validate", "merge", "dump-workbook",
            "extract-attachment", "transcribe", "allocate-id")
#: `<data-repo>`, `<code-repo>`, `<path>` … — angle-bracket placeholders are cut
#: before the redirect scan, or every `DATA_ROOT=<data-repo>` reads as a `>`.
PLACEHOLDER = re.compile(r"<[^<>]*>")
#: ADR 0011. A batch is one fenced block, which is how the playbook prints one
#: message: `Task:` lines are counted per block.
MAX_TASKS = 4


def blocks(text, kind="persian"):
    """Every block of `kind` in a playbook, in file order.

    `persian` — the owner-facing messages. `bash` — the command blocks, fenced
    ones first and then the commands printed inline in prose.
    """
    if kind == "persian":
        return [m.group(1) for m in FENCE.finditer(text)]
    if kind == "bash":
        rest = FENCE.sub("", text)
        return ([m.group(1) for m in BARE_FENCE.finditer(rest)]
                + [m.group(1) for m in INLINE_COMMAND.finditer(rest)])
    raise ValueError(f"unknown block kind {kind!r}")


def problems(block, kind="persian"):
    """Every rule this block breaks, one message each; empty means clean."""
    if kind == "bash":
        return _command_problems(block)
    out = []
    for token in block.split():
        if "/" in token and not FA_DATE.fullmatch(token):
            out.append(f"path-shaped token {token!r}")
    hit = HEX8.search(block)
    if hit:
        out.append(f"8-hex id {hit.group(0)!r}")
    for dept in DEPARTMENTS:
        if re.search(rf"\b{dept}\b", block):
            out.append(f"department code {dept!r}")
    for word in BANNED:
        if word in block:
            out.append(f"pipeline word {word!r}")
    return out


def _command_problems(block):
    """A command block's two rules: bare engine commands, and ≤ 4 dispatches."""
    out = []
    for line in block.splitlines():
        bare = PLACEHOLDER.sub("", line)
        if not any(cli in bare for cli in COMMANDS):
            continue
        for redirect in ("2>&1", "|", ">"):
            if redirect in bare:
                out.append(f"redirect {redirect!r} in {line.strip()!r}")
                break
    dispatched = len(re.findall(r"^\s*Task:", block, re.M))
    if dispatched > MAX_TASKS:
        out.append(f"{dispatched} Task dispatches in one message "
                   f"(at most {MAX_TASKS})")
    return out


@pytest.fixture(scope="module")
def owner_blocks():
    return blocks(PLAYBOOK.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def command_blocks():
    return blocks(PLAYBOOK.read_text(encoding="utf-8"), "bash")


def test_the_playbook_marks_its_owner_facing_blocks(owner_blocks):
    assert owner_blocks, "no ```persian block in SKILL.md — nothing is linted"


def test_every_owner_facing_block_is_persian(owner_blocks):
    for block in owner_blocks:
        assert re.search(r"[؀-ۿ]", block), f"not Persian: {block!r}"


def test_no_owner_facing_block_carries_an_internal(owner_blocks):
    found = {i: problems(b) for i, b in enumerate(owner_blocks) if problems(b)}
    assert found == {}


def test_the_playbook_has_command_blocks(command_blocks):
    assert command_blocks, "no bare fence in SKILL.md — no command is linted"


def test_no_command_block_pipes_redirects_or_over_dispatches(command_blocks):
    found = {i: problems(b, "bash")
             for i, b in enumerate(command_blocks) if problems(b, "bash")}
    assert found == {}


# --------------------------------------------------------------------------
# The rules against synthetic blocks: the real playbook is clean, so without
# these the checker could be `return []` and every test above would still pass.

#: `(kind, block, the one problem it must raise)` — one case per rule.
BREAKS = [
    ("persian", "گزارش در runs/facts نوشته شد.", "path-shaped token"),
    ("persian", "شناسهٔ 9f3a1c7d ثبت شد.", "8-hex id"),
    ("persian", "بخش cooking آماده است.", "department code"),
    ("persian", "دلتا آماده است.", "pipeline word"),
    ("bash", "Bash: DATA_ROOT=<data-repo> facts-plan status --run R | head",
     "redirect '|'"),
    ("bash", "Bash: DATA_ROOT=<data-repo> merge facts audit --persian > o.txt",
     "redirect '>'"),
    ("bash", "Bash: DATA_ROOT=<data-repo> validate manifest m.json 2>&1",
     "redirect '2>&1'"),
    ("bash", "Task: quantify\n" * 5, "5 Task dispatches in one message"),
]

CLEAN = [
    ("persian", "۸ از ۲۶ بخش از داده‌ها بررسی شد؛ تاریخ ۱۴۰۵/۰۴/۱۸ ثبت شد."),
    ("bash", "Bash: DATA_ROOT=<data-repo> facts-plan status --run {run_dir}\n"
             + "Task: quantify\n" * MAX_TASKS),
]


@pytest.mark.parametrize("kind,block,expected", BREAKS)
def test_a_broken_block_raises_exactly_that_problem(kind, block, expected):
    found = problems(block, kind)
    assert len(found) == 1, found
    assert expected in found[0]


@pytest.mark.parametrize("kind,block", CLEAN)
def test_a_clean_block_raises_nothing(kind, block):
    assert problems(block, kind) == []


def test_a_persian_fence_never_opens_a_command_block():
    text = "```persian\nسلام\n```\n\n```\nBash: transcribe a\n```\n"
    assert blocks(text) == ["سلام\n"]
    assert blocks(text, "bash") == ["Bash: transcribe a\n"]


def test_a_command_printed_inline_is_linted_too():
    text = "Then `Bash: validate manifest m.json | head` on the row.\n"
    assert blocks(text, "bash") == ["Bash: validate manifest m.json | head"]
    assert problems(blocks(text, "bash")[0], "bash")


def test_the_expression_card_and_the_checker_name_the_same_keywords():
    content = pytest.importorskip("merge_facts.content")
    card = KEYWORD_FENCE.search(AGENT.read_text(encoding="utf-8"))
    assert card is not None, "the expression card lost its keyword block"
    assert set(card.group(1).split()) == set(content.KEYWORDS)


def test_the_expression_card_quotes_the_two_grammars_verbatim():
    mf = pytest.importorskip("merge_facts")
    card = AGENT.read_text(encoding="utf-8")
    assert mf.SEGMENT_RE.pattern in card
    assert mf.KEY_RE.pattern in card


def test_stage_u_states_the_two_caps_as_the_engine_s():
    stage = STAGE_U.search(PLAYBOOK.read_text(encoding="utf-8"))
    assert stage is not None, "Stage U is gone from the playbook"
    text = stage.group(0)
    # §3.5's first cap: the engine refuses the third output, so the playbook may
    # not offer one — the v3 run's coordinator dispatched `out.3.json`.
    assert "refuses `out.3.json`" in text
    assert "Never ask the owner to lift the cap" in text
    # §3.5's second: `yield: true` is a stop, not a hint.
    assert "You never continue past a `yield: true`" in text

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
EDIT_FACT = ROOT / ".claude" / "skills" / "edit-fact" / "SKILL.md"

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


# The two phases (design 2026-09-15 §3): the forms are decided first, with the
# meeting passages about them beside them, and the transcripts are read after,
# knowing what the forms recorded. Each sentence below is a mechanical rule of
# the engine — the `waiting` state, the two input sections, the account a unit
# writes instead of a second entry, and which source wins a merge.

def test_stage_u_never_dispatches_a_waiting_unit():
    stage = " ".join(STAGE_U.search(PLAYBOOK.read_text(encoding="utf-8")).group(0).split())
    assert "A unit `status` prints as `waiting` is never dispatched" in stage


def test_the_agent_reads_the_talk_beside_the_form_and_keeps_the_forms_value():
    agent = " ".join(AGENT.read_text(encoding="utf-8").split())
    assert "## گفت‌وگوهای مرتبط" in agent
    assert "the table's columns and values are the file's or the photo's" in agent
    assert "the spoken value becomes an `account` on the same entry" in agent


def test_the_agent_cites_a_passage_by_the_path_in_its_heading():
    """The engine admits a citation only for the transcript the passage heading
    prints, and only for lines inside that passage — the agent has to be told
    both, or every account it writes is dropped."""
    agent = " ".join(AGENT.read_text(encoding="utf-8").split())
    assert "the transcript path printed in its heading" in agent
    assert "inside that passage" in agent
    assert "lines must lie inside one passage" in agent


def test_the_agent_knows_the_voice_list_and_its_shape():
    """Spec §3: the talk that filled in what the form does not state is cited
    as the meeting, beside the sheet and never instead of it."""
    agent = " ".join(AGENT.read_text(encoding="utf-8").split())
    assert ('"voice": [{"ref": "<transcript path printed in the passage '
            'heading>", "lines": "a-b"}]') in agent
    assert "appends them to `source[]` after the sheet or the photo" in agent


def test_the_agent_attaches_speech_to_a_listed_table_before_describing_a_new_one():
    agent = " ".join(AGENT.read_text(encoding="utf-8").split())
    assert "## آنچه تا کنون ثبت شده" in agent
    assert "describe a new table only when no listed table fits" in agent


def test_review_mode_keeps_the_entry_read_off_a_form():
    assert (
        "when two entries merge, the one read off a form is the keeper"
    ) in agent_section("`review` mode")


def agent_section(heading):
    """One `###` section of the agent file, flattened to a single line.

    The agent wraps its prose, so a pinned sentence spans lines; flattening
    makes the sentence in the file comparable with the sentence here.
    """
    text = AGENT.read_text(encoding="utf-8")
    found = re.search(rf"^### {heading}\b.*?(?=^### )", text, re.M | re.S)
    assert found is not None, f"section {heading!r} is gone from quantify.md"
    return " ".join(found.group(0).split())


# The three sentences the v3 acceptance run cost us (design §3.6): the reviewer
# wrote `contradiction` on fields nothing flagged, a unit typed a column of
# ingredient names as `refItems`, and a unit named parameter-bound inputs by
# position. Each is a mechanical rule, and prose stating one drifts unpinned.

def test_review_mode_admits_a_contradiction_only_on_a_flagged_field():
    assert (
        "A `contradiction` is admissible only on a field the digest lists under"
        " its drift flags; two entries you believe disagree on any other field"
        " are a `keep` carrying the reason, never a `contradiction`."
    ) in agent_section("`review` mode")


def test_review_mode_says_a_keep_with_data_changes_only_what_it_lists():
    """The owner's 2026-09-08 run: the reviewer rewrote one member of sixteen
    items and, told the assembly refused them, copied the engine-owned `code`
    in — both attempts lost, no review. The fold now merges member by member
    (engine), and the reviewer is told so here."""
    assert (
        "A `keep` carrying `data` changes only the members it lists — the"
        " unit's other members stay as written — and never writes `code`,"
        " which the engine owns."
    ) in agent_section("`review` mode")


# The 2026-09-09 ruling: the review is never dropped. Both real runs lost theirs
# whole — one to a cap, one to a single bad decision — so the two rules that
# replaced them are pinned here, and the playbook's escape hatches are pinned
# shut: a text that still offers one is a text that will take it.

def test_review_mode_has_no_cap_and_holds_back_by_decision():
    """Owner ruling 2026-09-09: both real runs lost their review whole."""
    assert (
        "There is no cap on decisions or rewrites. A decision whose address matches"
        " zero entries, or more than one, is held back on its own and named in the"
        " report; the rest of your review is applied."
    ) in agent_section("`review` mode")
    assert (
        "A record's `fields[]` is not yours to rewrite — the digest does not show the"
        " column keys the shape needs — and a `keep` carrying `fields` is held back."
    ) in agent_section("`review` mode")


def test_the_playbook_never_proceeds_without_the_review():
    text = PLAYBOOK.read_text(encoding="utf-8")
    assert "proceed **without** the review" not in text
    assert "proceed without it" not in text
    assert "The review is never dropped" in text


def test_the_unit_contract_says_a_column_of_names_is_a_string():
    assert (
        "A column whose cells are names is `type: string`; `refItems` is only"
        " for cells that are the catalogue's codes (the namespaces your input's"
        " shape section names) or item keys."
    ) in agent_section("What you decide, per kind")


def test_the_unit_contract_names_a_bound_input_after_its_column():
    assert (
        "An input bound through a parameter takes its key and title from the"
        " column the parameter resolves to, as printed under the candidate."
    ) in agent_section("What you decide, per kind")


# The chat edit (v3.7 §5/§6): the owner asked for one word to change in ten
# statements and the write ladder dropped it silently. The patch verb is the
# fix, and the two prompts that reach for it are prose — pinned here so a later
# edit cannot quietly put the old apply→dispute→resolve dance back.

def test_targeted_mode_names_its_two_output_files():
    text = AGENT.read_text(encoding="utf-8")
    section = text.split("### `targeted` mode", 1)[1].split("\n---", 1)[0]
    assert "facts-patch.json" in section and "facts-delta.json" in section
    assert '"op": "set"' in section or "`set`" in section


def test_the_edit_fact_playbook_has_the_three_case_table_and_no_account_hunt():
    text = EDIT_FACT.read_text(encoding="utf-8")
    assert "merge facts edit" in text and "--preview" in text
    assert "facts-patch.json" in text
    # The report never claims a confirmation: the panel's tick is a person's
    # alone (owner ruling, 2026-09-09), so the sentence says the opposite.
    assert "در پنل هنوز تأییدنشده است" in text
    assert "تأییدشده است" not in text
    assert "account id" not in text.lower() or "Never compute an account id" not in text
    # The table's two load-bearing cells: its header, and the row that says the
    # playbook writes a mechanical change itself. Gutting either is what would
    # send a change back through `apply` and lose it to a dispute again.
    assert "| the instruction … | vehicle | who writes it |" in text
    assert "**this playbook**, with no dispatch" in text


def test_the_edit_fact_playbook_never_relays_the_preview_op_lines():
    """Bot messages hide internals: the preview's `[n] op path` header is an
    English op name and a store path, and the owner is shown only the
    «فعلی»/«پیشنهاد» values under the Persian titles they belong to."""
    text = EDIT_FACT.read_text(encoding="utf-8")
    assert "The preview's `[n] op path` lines are internals" in text
    assert "**Never relay them.**" in text
    assert "No id, no path, no op name, no command, no English word goes into the message" in text
    assert "{the preview output of every entry, exactly as printed}" not in text


# The gate tiers (spec 2026-09-13, owner-approved): a refusal costs one decision
# or one entry, never a unit or a file, and nothing is lost silently. Each of
# these sentences is what the coordinator or the unit acts on; a text that
# drops one sends a whole unit back, stops a run at an apply that wrote, or
# sends a report without the file it lost.

def test_stage_u_retries_only_refused_decisions_and_runs_attachment_units():
    text = " ".join(STAGE_U.search(PLAYBOOK.read_text(encoding="utf-8")).group(0).split())
    assert "Retry only refused decisions" in text
    assert "Attachment units are dispatched like any unit" in text


def test_the_playbook_continues_after_an_apply_that_held_entries_back():
    text = " ".join(PLAYBOOK.read_text(encoding="utf-8").split())
    assert ("**Exit 0 with held entries is a finished apply: the run continues to"
            " Stage 6.**") in text
    assert "not one entry could be" in text


def test_the_report_names_lost_sources_first():
    text = " ".join(PLAYBOOK.read_text(encoding="utf-8").split())
    assert "Its first lines name any lost source" in text


def test_the_unit_contract_retries_only_the_listed_decisions():
    text = " ".join(AGENT.read_text(encoding="utf-8").split())
    assert "A retry answers only the decisions listed in `retry`." in text


def test_the_unit_contract_admits_a_column_group_and_attachment_units():
    section = agent_section("What you decide, per kind")
    assert "may carry `group: {key, title}`" in section
    assert "**An attachment unit** — `نوع: attachment`, zero candidates" in section


def test_the_agent_cites_the_file_an_entry_was_read_off():
    """Task G 2026-09-16: a unit handed several photos must name the one an
    entry came off, or the engine credits the entry to all of them."""
    text = " ".join(AGENT.read_text(encoding="utf-8").split())
    assert "each file's text is headed by its name and path" in text
    assert ('an entry read off a photo or document cites it as '
            '`from: ["<path exactly as printed>"]` — one path, or more only '
            'when the entry spans several files; a path not printed in your '
            'input is dropped') in text


def test_the_agent_looks_at_the_photo_for_structure_and_keeps_the_description():
    """Task H 2026-09-16: the extracted description is the source; the image is
    opened only to see the structure it cannot spell, and a difference is a note
    rather than a rewrite."""
    text = " ".join(AGENT.read_text(encoding="utf-8").split())
    assert "the form photos your own headings name as `عکس:`" in text
    assert ("For every file whose heading names a `عکس:` path, open that image "
            "too (the Read tool) and use it only to understand the table's "
            "structure") in text
    assert ("The description printed under the heading is the source and has "
            "priority") in text
    assert "do not change the description's reading; add a `new[]` note" in text
    assert "Open only the images your headings name — never another file." in text

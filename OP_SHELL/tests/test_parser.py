import pytest
from types import SimpleNamespace
from core.parser import match_intent, render_command

class RuleStub:
    def __init__(self, pattern: str, command: str):
        self.pattern = pattern
        # parser.render_command expects rule.template.command
        self.template = SimpleNamespace(command=command)


def test_match_intent_basic_trim_and_case_insensitive():
    rule = RuleStub(r"hello", "ignored")
    result = match_intent("  Hello  ", [rule])
    assert result is not None
    matched_rule, params = result
    assert matched_rule is rule
    assert params == {}


def test_match_intent_named_group_returns_groupdict():
    rule = RuleStub(r"run (?P<cmd>\w+)", "ignored")
    result = match_intent("run backup", [rule])
    assert result is not None
    matched_rule, params = result
    assert matched_rule is rule
    assert params == {"cmd": "backup"}


def test_match_intent_no_full_match_returns_none():
    rule = RuleStub(r"hello", "ignored")
    # fullmatch should fail because extra text present
    assert match_intent("hello world", [rule]) is None


def test_render_command_substitutes_parameters():
    rule = RuleStub(r".*", "echo {{ cmd }}")
    rendered = render_command(rule, {"cmd": "backup"})
    assert rendered == "echo backup"


def test_render_command_ignores_extra_parameters():
    rule = RuleStub(r".*", "echo {{ cmd }}")
    rendered = render_command(rule, {"cmd": "backup", "extra": "ignored"})
    assert rendered == "echo backup"


def test_render_command_missing_parameter_renders_empty_string():
    # Jinja2 default undefined renders as empty string
    rule = RuleStub(r".*", "echo {{ cmd }}")
    rendered = render_command(rule, {})
    assert rendered == "echo "
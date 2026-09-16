"""Tests for Memory."""

from __future__ import annotations

import pytest

from truagent import Memory


def test_add_appends_message() -> None:
    m = Memory()
    m.add({"role": "user", "content": "hello"})
    assert len(m) == 1
    assert m.messages[0]["role"] == "user"
    assert m.messages[0]["content"] == "hello"


def test_append_alias() -> None:
    m = Memory()
    m.append({"role": "assistant", "content": "hi"})
    assert m[0]["role"] == "assistant"


def test_plus_operator_with_dict_returns_new_memory() -> None:
    m = Memory()
    m.add({"role": "user", "content": "a"})
    combined = m + {"role": "assistant", "content": "b"}
    assert isinstance(combined, Memory)
    assert len(combined) == 2
    assert len(m) == 1  # original unchanged


def test_plus_operator_merges_memory() -> None:
    m1 = Memory()
    m1.add({"role": "user", "content": "one"})
    m2 = Memory()
    m2.add({"role": "assistant", "content": "two"})
    combined = m1 + m2
    assert len(combined) == 2
    assert combined.messages == [
        {"role": "user", "content": "one"},
        {"role": "assistant", "content": "two"},
    ]


def test_iadd_mutates_in_place() -> None:
    m = Memory()
    m.add({"role": "user", "content": "x"})
    m += {"role": "assistant", "content": "y"}
    assert len(m) == 2


def test_plus_rejects_other_types() -> None:
    m = Memory()
    with pytest.raises(ValueError):
        m + 42  # type: ignore[operator]


def test_init_with_system_message() -> None:
    m = Memory(system="You are a bot.")
    assert m.system == "You are a bot."
    assert m.messages[0]["role"] == "system"


def test_set_system_replaces_existing() -> None:
    m = Memory(system="one")
    m.add({"role": "user", "content": "hi"})
    m.set_system("two")
    assert m.system == "two"
    roles = [msg["role"] for msg in m.messages]
    assert roles == ["system", "user"]


def test_clear_keeps_system() -> None:
    m = Memory(system="keep me")
    m.add({"role": "user", "content": "a"})
    m.add({"role": "assistant", "content": "b"})
    m.clear()
    assert len(m) == 1
    assert m.messages[0]["role"] == "system"


def test_keeps_system_and_last_n() -> None:
    m = Memory(system="sys")
    for i in range(10):
        m.add({"role": "user", "content": str(i)})
    m.trim(3)
    assert len(m) == 4
    assert m.messages[0]["role"] == "system"
    assert m.messages[-1]["content"] == "9"


def test_noop_when_within_limit() -> None:
    m = Memory()
    m.add({"role": "user", "content": "a"})
    m.trim(5)
    assert len(m) == 1


def test_is_chainable() -> None:
    m = Memory()
    result = m.add({"role": "user", "content": "a"}).add({"role": "user", "content": "b"})
    assert result is m
    assert len(m) == 2


def test_rejects_non_positive_limit() -> None:
    m = Memory()
    with pytest.raises(ValueError):
        m.trim(0)
    with pytest.raises(ValueError):
        m.trim(-1)


def test_json_roundtrip() -> None:
    m = Memory(system="sys")
    m.add({"role": "user", "content": "hello"})
    m.add({"role": "assistant", "content": "world"})
    restored = Memory.from_json(m.to_json())
    assert restored.messages == m.messages


def test_from_json_handles_full_document() -> None:
    import json

    data = json.dumps([{"role": "user", "content": "x"}])
    m = Memory.from_json(data)
    assert len(m) == 1


def test_from_json_invalid_string() -> None:
    with pytest.raises(ValueError):
        Memory.from_json("{not json")


def test_from_json_rejects_non_list() -> None:
    with pytest.raises(ValueError):
        Memory.from_json('{"role": "user"}')


def test_empty_memory_is_zero() -> None:
    assert Memory().estimate_tokens() == 0


def test_grows_with_more_content() -> None:
    small = Memory()
    small.add({"role": "user", "content": "short"})
    large = Memory()
    large.add({"role": "user", "content": "x" * 1000})
    assert large.estimate_tokens() > small.estimate_tokens()


def test_more_messages_cost_more() -> None:
    one = Memory()
    one.add({"role": "user", "content": "hello"})
    two = Memory()
    two.add({"role": "user", "content": "hello"})
    two.add({"role": "assistant", "content": "hello"})
    assert two.estimate_tokens() > one.estimate_tokens()


def test_missing_role_rejected() -> None:
    m = Memory()
    with pytest.raises(ValueError):
        m.add({"content": "no role"})


def test_unknown_role_rejected() -> None:
    m = Memory()
    with pytest.raises(ValueError):
        m.add({"role": "robot", "content": "hi"})


def test_non_dict_rejected() -> None:
    m = Memory()
    with pytest.raises(ValueError):
        m.add("just a string")  # type: ignore[arg-type]


def test_iteration_and_indexing() -> None:
    m = Memory()
    m.add({"role": "user", "content": "a"})
    m.add({"role": "assistant", "content": "b"})
    assert [msg["content"] for msg in m] == ["a", "b"]
    assert m[1]["content"] == "b"


def test_messages_returns_copies() -> None:
    m = Memory()
    m.add({"role": "user", "content": "a"})
    first = m.messages
    first[0]["content"] = "mutated"
    assert m[0]["content"] == "a"


def test_repr_mentions_count() -> None:
    m = Memory()
    m.add({"role": "user", "content": "a"})
    assert "1" in repr(m)
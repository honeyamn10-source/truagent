"""Tests for JSON parsing helpers."""

from __future__ import annotations

from truagent.parse import extract_json, extract_tool_call, parse_arguments, repair_json


def test_plain_object() -> None:
    assert extract_json('{"a": 1}') == {"a": 1}


def test_object_wrapped_in_prose() -> None:
    text = 'Here is the result: {"tool": "add", "arguments": {"x": 1}} enjoy!'
    assert extract_json(text) == {"tool": "add", "arguments": {"x": 1}}


def test_fenced_code_block() -> None:
    text = '```json\n{"a": 2}\n```'
    assert extract_json(text) == {"a": 2}


def test_fence_without_json_tag() -> None:
    text = "```\n{\"b\": 3}\n```"
    assert extract_json(text) == {"b": 3}


def test_trailing_comma_repaired() -> None:
    assert extract_json('{"a": [1, 2,]}') == {"a": [1, 2]}


def test_no_json_returns_none() -> None:
    assert extract_json("no json here") is None


def test_none_input_returns_none() -> None:
    assert extract_json(None) is None
    assert extract_json("") is None


def test_repair_json_single_trailing_comma() -> None:
    assert repair_json('{"a": [1, 2,]}') == '{"a": [1, 2]}'


def test_repair_json_valid_json_untouched() -> None:
    assert repair_json('{"a": 1}') is None


def test_extract_tool_call_custom_shape() -> None:
    call = extract_tool_call('{"tool": "add", "arguments": {"x": 1, "y": 2}}')
    assert call is not None
    assert call.name == "add"
    assert call.arguments == {"x": 1, "y": 2}


def test_extract_tool_call_openai_shape() -> None:
    text = '{"tool_calls": [{"id": "c1", "function": {"name": "add", "arguments": "{\\"x\\": 1}"}}]}'
    call = extract_tool_call(text)
    assert call is not None
    assert call.name == "add"
    assert call.arguments == {"x": 1}
    assert call.id == "c1"


def test_parse_arguments_dict_passthrough() -> None:
    assert parse_arguments({"a": 1}) == {"a": 1}


def test_parse_arguments_string_json() -> None:
    assert parse_arguments('{"a": 1}') == {"a": 1}


def test_parse_arguments_none() -> None:
    assert parse_arguments(None) == {}


def test_parse_arguments_trailing_comma() -> None:
    assert parse_arguments('{"a": 1,}') == {"a": 1}
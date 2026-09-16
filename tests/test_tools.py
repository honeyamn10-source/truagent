"""Tests for the Tool decorator, schema reflection and registries."""

from __future__ import annotations

import pytest
from conftest import add, double, greet

from truagent import Tool, ToolError
from truagent.tools import ToolRegistry, ensure_tool, tool, tool_registry


def test_int_str_bool_reflection() -> None:
    @tool
    def fn(a: int, b: str, c: bool) -> None:
        """Docstring."""

    schema = fn.parameters
    assert schema["properties"]["a"]["type"] == "integer"
    assert schema["properties"]["b"]["type"] == "string"
    assert schema["properties"]["c"]["type"] == "boolean"


def test_float_maps_to_number() -> None:
    @tool
    def fn(x: float) -> None:
        """Docstring."""

    assert fn.parameters["properties"]["x"]["type"] == "number"


def test_defaults_not_required() -> None:
    @tool
    def fn(a: int, b: int = 5) -> None:
        """Docstring."""

    assert fn.parameters["required"] == ["a"]
    assert fn.parameters["properties"]["b"]["default"] == 5


def test_keyword_only_params_are_reflected() -> None:
    @tool
    def fn(*, x: int) -> None:
        """Docstring."""

    assert "x" in fn.parameters["properties"]


def test_docstring_params_and_description() -> None:
    @tool
    def fn(name: str) -> str:
        """Greet a person.

        :param name: The person's name.
        """

    assert "Greet" in fn.description
    assert fn.parameters["properties"]["name"].get("description") == "The person's name."


def test_unannotated_param_defaults_to_string() -> None:
    @tool
    def fn(value) -> None:
        """Docstring."""

    assert fn.parameters["properties"]["value"]["type"] == "string"


def test_varargs_are_skipped() -> None:
    @tool
    def fn(x: int, *args, **kwargs) -> None:
        """Docstring."""

    props = fn.parameters["properties"]
    assert "x" in props
    assert "args" not in props
    assert "kwargs" not in props


def test_schema_shape() -> None:
    @tool
    def fn(a: int) -> None:
        """Adds one."""

    schema = fn.schema()
    assert schema["type"] == "function"
    assert schema["function"]["name"] == "fn"
    assert "parameters" in schema["function"]


def test_run_coerces_types() -> None:
    assert add.run({"x": "2", "y": 3}) == 5
    assert add.run({"x": 1.5, "y": 2}) == 3.5


def test_missing_required_argument_raises() -> None:
    with pytest.raises(ToolError):
        add.run({"x": 1})


def test_extra_arguments_are_ignored() -> None:
    assert add.run({"x": 1, "y": 2, "z": 99}) == 3


def test_invalid_value_type_raises() -> None:
    with pytest.raises(ToolError):
        add.run({"x": "not-an-int", "y": 2})


def test_non_dict_arguments_raise() -> None:
    with pytest.raises(ToolError):
        add.run("not-a-dict")  # type: ignore[arg-type]


def test_direct_call_invokes_function() -> None:
    assert add(2, 3) == 5


def test_decorator_registers_globally() -> None:
    assert "add" in tool_registry().names()
    assert "greet" in tool_registry().names()


def test_decorator_with_overrides() -> None:
    @tool(name="renamed", description="Custom description")
    def original() -> None:
        """Original docstring."""

    assert original.name == "renamed"
    assert original.description == "Custom description"


def test_registry_duplicate_name_overwrites() -> None:
    registry = ToolRegistry()
    registry.add(add)

    @tool
    def duplicate_add(x: int, y: int) -> int:
        """Add two integers but keep a distinct function name."""
        return x + y

    # Registering a new tool under an existing name overwrites the old one.
    registry.add(duplicate_add)
    assert registry.get("duplicate_add").run({"x": 1, "y": 2}) == 3
    # The global registry got the new one too (tool decorator registers globally).
    assert tool_registry().get("duplicate_add") is duplicate_add


def test_registry_contains_names_and_length() -> None:
    registry = ToolRegistry([add, double])
    assert "add" in registry
    assert len(registry) == 2
    assert set(registry.names()) == {"add", "double"}


def test_registry_remove_and_clear() -> None:
    registry = ToolRegistry([add])
    registry.remove("add")
    assert "add" not in registry
    registry.add(add)
    registry.clear()
    assert len(registry) == 0


def test_registry_constructed_with_tools() -> None:
    registry = ToolRegistry([add])
    assert registry.get("add") is add


def test_tool_registry_returns_global() -> None:
    assert tool_registry() is tool_registry()


def test_ensure_tool_coerces_callables() -> None:
    def plain(x: int) -> int:
        return x

    tool_obj = ensure_tool(plain)
    assert isinstance(tool_obj, Tool)
    assert tool_obj.run({"x": 1}) == 1


def test_tool_requires_callable() -> None:
    with pytest.raises(ToolError):
        Tool("not-callable")  # type: ignore[arg-type]


def test_tool_repr() -> None:
    assert repr(add) == "Tool(add)"


def test_greet_default_keyword_argument() -> None:
    assert greet.run({"name": "World"}) == "Hello, World!"
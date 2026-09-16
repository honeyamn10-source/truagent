"""Tool system: introspection-driven JSON schemas, validation and registries.

Decorating a plain Python function with ``@tool`` makes it a first-class
capability an LLM can call. Schemas are reflected automatically from type
annotations and docstrings — no hand-written JSON required.
"""

from __future__ import annotations

import inspect
import re
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from typing import Any, Callable

from .errors import ToolError

_TYPE_MAP: dict[str, str] = {
    "bool": "boolean",
    "boolean": "boolean",
    "int": "integer",
    "integer": "integer",
    "float": "number",
    "number": "number",
    "str": "string",
    "string": "string",
    "None": "null",
}


@dataclass
class _DocstringInfo:
    description: str = ""
    params: dict[str, str] = field(default_factory=dict)


def _json_type(annotation: Any) -> str:
    if annotation is inspect.Signature.empty:
        return "string"
    name = getattr(annotation, "__name__", None) or str(annotation)
    return _TYPE_MAP.get(name, "string")


def _parse_docstring(doc: str | None) -> _DocstringInfo:
    """Extract the description and ``:param name:`` notes from a docstring."""
    if not doc:
        return _DocstringInfo()
    description_parts: list[str] = []
    params: dict[str, str] = {}
    for raw_line in doc.strip().splitlines():
        line = raw_line.strip()
        match = re.match(r":param (\w+):\s*(.*)", line)
        if match:
            params[match.group(1)] = match.group(2).strip()
        elif line.startswith((":param", ":return", ":raises")):
            continue
        elif description_parts or line:
            description_parts.append(line)
    return _DocstringInfo(description=" ".join(description_parts).strip(), params=params)


def _reflect_parameters(
    signature: inspect.Signature,
    param_docs: dict[str, str],
) -> dict[str, Any]:
    """Build a JSON schema object from an ``inspect.Signature``."""
    properties: dict[str, Any] = {}
    required: list[str] = []
    for param_name, parameter in signature.parameters.items():
        if parameter.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ):
            continue
        spec: dict[str, Any] = {"type": _json_type(parameter.annotation)}
        if param_docs.get(param_name):
            spec["description"] = param_docs[param_name]
        if parameter.default is not inspect.Parameter.empty:
            spec["default"] = parameter.default
        else:
            required.append(param_name)
        properties[param_name] = spec
    return {"type": "object", "properties": properties, "required": required}


class Tool:
    """A callable capability with a self-describing JSON schema."""

    def __init__(
        self,
        func: Callable[..., Any],
        name: str | None = None,
        description: str | None = None,
    ) -> None:
        if not callable(func):
            raise ToolError("tool must wrap a callable", tool_name=name)
        self.func = func
        self.name = name or func.__name__
        signature = inspect.signature(func)
        info = _parse_docstring(inspect.getdoc(func))
        self.description = description or info.description or self.name
        self._schema_dict = _reflect_parameters(signature, info.params)
        self._schema_dict["description"] = self.description

    @property
    def parameters(self) -> dict[str, Any]:
        """The JSON schema object for the tool arguments."""
        return dict(self._schema_dict)

    def schema(self) -> dict[str, Any]:
        """The full OpenAI-style tool schema."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self._schema_dict,
            },
        }

    def run(self, arguments: dict[str, Any] | None = None) -> Any:
        """Execute the tool with validated, coerced arguments."""
        if arguments is None:
            arguments = {}
        if not isinstance(arguments, dict):
            raise ToolError("tool arguments must be a JSON object", tool_name=self.name)
        kwargs: dict[str, Any] = {}
        for param_name, spec in self._schema_dict["properties"].items():
            if param_name not in arguments:
                if "default" in spec:
                    kwargs[param_name] = spec["default"]
                elif param_name in self._schema_dict["required"]:
                    raise ToolError(
                        f"missing required argument '{param_name}'", tool_name=self.name
                    )
                continue
            value = arguments[param_name]
            expected = spec.get("type", "string")
            if expected == "integer" and isinstance(value, (bool, str)):
                try:
                    value = int(value)
                except (TypeError, ValueError):
                    raise ToolError(
                        f"argument '{param_name}' must be an integer", tool_name=self.name
                    ) from None
            elif expected == "number" and isinstance(value, (bool, str)):
                try:
                    value = float(value)
                except (TypeError, ValueError):
                    raise ToolError(
                        f"argument '{param_name}' must be a number", tool_name=self.name
                    ) from None
            elif expected == "boolean" and isinstance(value, str):
                lowered = value.lower()
                if lowered in ("true", "1", "yes", "on"):
                    value = True
                elif lowered in ("false", "0", "no", "off"):
                    value = False
                else:
                    raise ToolError(
                        f"argument '{param_name}' must be a boolean", tool_name=self.name
                    ) from None
            kwargs[param_name] = value
        return self.func(**kwargs)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.func(*args, **kwargs)

    def __repr__(self) -> str:
        return f"Tool({self.name})"


class ToolRegistry:
    """A named collection of Tools."""

    def __init__(self, tools: Iterable[Any] | None = None) -> None:
        self._tools: dict[str, Tool] = {}
        for item in tools or ():
            self.add(item)

    @staticmethod
    def _instance() -> ToolRegistry:
        return _GLOBAL_REGISTRY

    def add(self, item: Any) -> ToolRegistry:
        if isinstance(item, Tool):
            tool_obj = item
        elif callable(item):
            tool_obj = ensure_tool(item)
        else:
            raise ToolError("registry items must be callables or Tool instances")
        self._tools[tool_obj.name] = tool_obj
        return self

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def remove(self, name: str) -> None:
        self._tools.pop(name, None)

    def clear(self) -> None:
        self._tools.clear()

    def all(self) -> dict[str, Tool]:
        return dict(self._tools)

    def names(self) -> list[str]:
        return list(self._tools)

    def schemas(self) -> list[dict[str, Any]]:
        return [t.schema() for t in self._tools.values()]

    def __contains__(self, name: object) -> bool:
        return name in self._tools

    def __iter__(self) -> Iterator[Tool]:
        return iter(self._tools.values())

    def __len__(self) -> int:
        return len(self._tools)


_GLOBAL_REGISTRY = ToolRegistry()


def tool_registry() -> ToolRegistry:
    """Return the process-wide registry used when no tools are specified."""
    return _GLOBAL_REGISTRY


def ensure_tool(item: Any) -> Tool:
    """Coerce a callable or Tool into a Tool instance."""
    if isinstance(item, Tool):
        return item
    if callable(item):
        return Tool(item)
    raise ToolError("expected a callable or Tool")


def tool(
    func: Callable[..., Any] | None = None,
    *,
    name: str | None = None,
    description: str | None = None,
) -> Any:
    """Decorate a function to turn it into a registered Tool.

    Usage::

        @tool
        def add(x: int, y: int) -> int:
            '''Add two integers together.'''
            return x + y

    The decorated callable is registered in the global registry and also
    returns a :class:`Tool` instance.
    """

    def decorator(fn: Callable[..., Any]) -> Tool:
        instance = Tool(fn, name=name, description=description)
        _GLOBAL_REGISTRY.add(instance)
        return instance

    if func is not None:
        return decorator(func)
    return decorator
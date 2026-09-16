"""The agent loop: think, call tools, observe, answer.

TruAgent's core loop is intentionally transparent:

1. The model is asked to either call a tool or produce a final answer.
2. Tool results are appended to memory as ``tool`` messages.
3. When the model answers, the loop returns.

Everything is observable through :class:`~truagent.middleware.Hooks`, and
the whole loop is pure Python with zero third-party dependencies.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from typing import Any

from .clients import AssistantMessage, BaseLLM
from .errors import AgentError, MaxStepsExceeded, ToolError
from .memory import Memory
from .middleware import Hooks
from .parse import extract_tool_call
from .tools import Tool, ToolRegistry, tool_registry

_TOOL_SYSTEM_TEMPLATE = """You are a helpful agent with access to the following tools:

{tools}

Reply with a final answer OR a single tool call. If you call a tool, use this exact JSON shape:
{{"tool_call": {{"name": "<tool name>", "arguments": {{...}}}}}}
Otherwise reply in plain language."""


def normalize_tools(tools: Any | None) -> dict[str, Tool]:
    """Coerce a tool collection into a name-to-Tool mapping."""
    result: dict[str, Tool] = {}
    if tools is None:
        return {t.name: t for t in tool_registry()}
    if isinstance(tools, ToolRegistry):
        source = tools.all().values()
    elif isinstance(tools, Mapping):
        source = []
        for key, value in tools.items():
            if isinstance(value, Tool):
                # Preserve the mapping key as the tool name.
                item = Tool(value.func, name=str(key), description=value.description)
            else:
                item = Tool(value, name=str(key))
            source.append(item)
    elif isinstance(tools, Iterable):
        source = tools
    else:
        raise TypeError("tools must be a ToolRegistry, mapping, iterable, or None")
    for item in source:
        if isinstance(item, Tool):
            result[item.name] = item
        elif callable(item):
            result[item.__name__] = Tool(item)
        else:
            raise TypeError("tool collection items must be callables or Tool instances")
    return result


def normalize_hooks(hooks: Hooks | Mapping[str, Any] | None) -> Hooks:
    """Coerce a hooks argument into a :class:`Hooks` instance."""
    if hooks is None:
        return Hooks()
    if isinstance(hooks, Hooks):
        return hooks
    if isinstance(hooks, Mapping):
        return Hooks(on_step=hooks.get("on_step"), on_message=hooks.get("on_message"))
    raise TypeError("hooks must be a Hooks instance, mapping, or None")


def format_tool_result(value: Any) -> str:
    """Stringify a tool result the way it should be fed back to the model."""
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, ensure_ascii=False, default=str)
    except (TypeError, ValueError):
        return str(value)


class Agent:
    """An agent that drives a model with tools, memory and middleware."""

    def __init__(
        self,
        llm: BaseLLM,
        tools: ToolRegistry | Mapping[str, Any] | Iterable[Any] | None = None,
        system: str | None = None,
        memory: Memory | None = None,
        max_steps: int = 8,
        hooks: Hooks | Mapping[str, Any] | None = None,
    ) -> None:
        if not isinstance(llm, BaseLLM):
            raise TypeError("llm must be a BaseLLM instance")
        if not isinstance(max_steps, int) or max_steps < 1:
            raise ValueError("max_steps must be at least 1")
        self.llm = llm
        self.tools: dict[str, Tool] = (
            tool_registry().all() if tools is None else normalize_tools(tools)
        )
        self.system = system
        self.memory = memory or Memory()
        if system:
            self.memory.set_system(system)
        self.max_steps = max_steps
        self.hooks = normalize_hooks(hooks)

    @property
    def available_tools(self) -> list[str]:
        """The names of the tools wired to this agent."""
        return sorted(self.tools)

    def tool_schemas(self) -> list[dict[str, Any]]:
        """The OpenAI-style schema for every tool wired to the agent."""
        return [tool.schema() for tool in self.tools.values()]

    def _tool_instructions(self) -> str:
        lines = []
        for schema in self.tool_schemas():
            fn = schema["function"]
            params = fn.get("parameters", {})
            param_names = ", ".join(params.get("properties", {}).keys())
            lines.append(f"- {fn['name']}({param_names}): {fn['description']}")
        return "\n".join(lines) or "(no tools)"

    def _system_prompt(self) -> str:
        if self.system:
            return self.system
        return _TOOL_SYSTEM_TEMPLATE.format(tools=self._tool_instructions())

    def execute_tool(self, name: str, arguments: dict[str, Any] | None = None) -> str:
        """Run a tool by name and return a string representation of the result."""
        tool_obj = self.tools.get(name)
        if tool_obj is None:
            return f"[tool error] unknown tool: {name}"
        try:
            value = tool_obj.run(arguments or {})
        except ToolError as exc:
            return f"[tool error] {exc}"
        except Exception as exc:  # defensive: keep the loop alive on tool bugs
            return f"[tool error] {type(exc).__name__}: {exc}"
        return format_tool_result(value)

    def _step(self, step: int = 1) -> str | None:
        """Run one model turn. Returns a final answer or ``None`` if the
        loop should continue (i.e. the model called a tool)."""
        messages = self.memory.messages
        self.hooks.step(step, messages, None)
        reply: AssistantMessage = self.llm.chat(messages)

        if reply.tool_call is not None:
            call = reply.tool_call
            self.hooks.message(reply)
            result = self.execute_tool(call.name, call.arguments)
            self.memory.add({"role": "assistant", "content": "", "tool_calls": [call.to_dict()]})
            self.memory.add(
                {"role": "tool", "content": result, "tool_call_id": call.name}
            )
            return None

        if reply.text:
            return reply.text

        # Model produced nothing useful. Fall back to JSON extraction.
        last = messages[-1] if messages else None
        content = str(last.get("content", "")) if isinstance(last, dict) else ""
        extracted = extract_tool_call(content)
        if extracted is not None:
            result = self.execute_tool(extracted.name, extracted.arguments)
            self.memory.add({"role": "tool", "content": result, "tool_call_id": extracted.name})
            return None
        return "I could not produce a reply."

    def run(self, message: str) -> str:
        """Execute the agent loop on a user message and return the final answer."""
        if not isinstance(message, str) or not message.strip():
            raise AgentError("message must be a non-empty string")
        if self.memory.system:
            self.memory.set_system(self.memory.system)
        self.memory.add({"role": "user", "content": message})
        for step in range(1, self.max_steps + 1):
            answer = self._step(step)
            if answer is not None:
                self.memory.add({"role": "assistant", "content": answer})
                return answer
        raise MaxStepsExceeded(
            f"agent did not reach a final answer within {self.max_steps} steps"
        )

    def __repr__(self) -> str:
        return f"Agent(tools={self.available_tools}, steps={self.max_steps})"
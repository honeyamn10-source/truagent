"""Shared test fixtures."""

from __future__ import annotations

from typing import Any

import pytest

from truagent.clients import AssistantMessage, BaseLLM
from truagent.parse import ToolCall
from truagent.tools import tool


@tool
def add(x: int, y: int) -> int:
    """Add two integers together."""
    return x + y


@tool
def double(x: int) -> int:
    """Double a number."""
    return 2 * x


@tool
def greet(name: str) -> str:
    """Say hello to someone by name."""
    return f"Hello, {name}!"


class FakeLLM(BaseLLM):
    """Serves scripted replies, one per call."""

    def __init__(self, responses: list[Any] = None) -> None:
        self._responses: list[Any] = list(responses or [])
        self.calls: list[list[dict]] = []

    def queue(self, response: Any) -> None:
        self._responses.append(response)

    def chat(self, messages: list[dict]) -> AssistantMessage:
        self.calls.append(list(messages))
        if not self._responses:
            return AssistantMessage(text="done")
        response = self._responses.pop(0)
        if isinstance(response, AssistantMessage):
            return response
        if isinstance(response, str):
            return AssistantMessage(text=response)
        if isinstance(response, dict):
            if "tool_call" in response:
                call = response["tool_call"]
                return AssistantMessage(
                    text="",
                    tool_call=ToolCall(
                        name=call["name"],
                        arguments=call.get("arguments") or {},
                        id=call.get("id"),
                    ),
                )
            if "text" in response:
                return AssistantMessage(text=response["text"])
        raise TypeError(f"unexpected response type: {type(response)}")


def tool_message(content: str) -> AssistantMessage:
    return AssistantMessage(text=content)


def text_message(content: str) -> AssistantMessage:
    return AssistantMessage(text=content)


@pytest.fixture
def make_agent():
    from truagent import Agent, Memory

    def factory(tools=None, responses=None, hooks=None, max_steps=8, system=None):
        llm = FakeLLM(responses)
        agent = Agent(
            llm=llm,
            tools=tools,
            system=system,
            memory=Memory(),
            max_steps=max_steps,
            hooks=hooks,
        )
        return agent, llm

    return factory


@pytest.fixture
def add_tool():
    return add


@pytest.fixture
def double_tool():
    return double
"""Tests for the Agent loop."""

from __future__ import annotations

import json

import pytest
from conftest import FakeLLM, add

from truagent import Agent, AgentError, MaxStepsExceeded
from truagent.middleware import Hooks


def test_normal_tool_loop_ends_with_answer(make_agent) -> None:
    agent, llm = make_agent(
        tools=[add],
        responses=[
            {"tool_call": {"name": "add", "arguments": {"x": 2, "y": 3}}},
            "five",
        ],
    )
    answer = agent.run("what is 2+3?")
    assert answer == "five"
    roles = [message["role"] for message in agent.memory.messages]
    assert roles == ["user", "assistant", "tool", "assistant"]
    tool_message_entry = [
        message for message in agent.memory.messages if message["role"] == "tool"
    ][0]
    assert tool_message_entry["content"] == "5"
    assert tool_message_entry["tool_call_id"] == "add"
    assistant_entry = [
        message
        for message in agent.memory.messages
        if message["role"] == "assistant" and message.get("tool_calls")
    ][0]
    assert assistant_entry["tool_calls"][0]["function"]["name"] == "add"
    assert json.loads(assistant_entry["tool_calls"][0]["function"]["arguments"]) == {
        "x": 2,
        "y": 3,
    }


def test_prose_answer_stops_immediately(make_agent) -> None:
    agent, llm = make_agent(responses=["hello!"])
    answer = agent.run("hi")
    assert answer == "hello!"
    assert len(llm.calls) == 1


def test_max_steps_overflow_raises(make_agent) -> None:
    agent, llm = make_agent(
        tools=[add],
        max_steps=3,
        responses=[
            {"tool_call": {"name": "add", "arguments": {"x": 1, "y": 1}}},
            {"tool_call": {"name": "add", "arguments": {"x": 2, "y": 2}}},
            {"tool_call": {"name": "add", "arguments": {"x": 3, "y": 3}}},
            "never reached",
        ],
    )
    with pytest.raises(MaxStepsExceeded):
        agent.run("keep going")


def test_tool_error_propagates_to_model(make_agent) -> None:
    def kaput() -> None:
        raise RuntimeError("kaput")

    agent, _ = make_agent(
        tools=[kaput],
        responses=[
            {"tool_call": {"name": "kaput", "arguments": {}}},
            "ok",
        ],
    )
    agent.run("please run the fragile tool")
    tool_entry = [
        message for message in agent.memory.messages if message["role"] == "tool"
    ][0]
    assert "[tool error]" in tool_entry["content"]
    assert "kaput" in tool_entry["content"]


def test_unknown_tool_reported_as_error(make_agent) -> None:
    agent, llm = make_agent(
        tools=[add],
        responses=[
            {"tool_call": {"name": "nope", "arguments": {}}},
            "That tool does not exist.",
        ],
    )
    answer = agent.run("call it")
    tool_entry = [
        message for message in agent.memory.messages if message["role"] == "tool"
    ][0]
    assert "[tool error] unknown tool" in tool_entry["content"]
    assert answer == "That tool does not exist."


def test_hooks_invoked_with_step_and_messages(make_agent) -> None:
    events = []
    hooks = Hooks(on_step=lambda step, messages, tool_call: events.append(step))
    agent, _ = make_agent(
        tools=[add],
        hooks=hooks,
        responses=[
            {"tool_call": {"name": "add", "arguments": {"x": 1, "y": 2}}},
            "three",
        ],
    )
    agent.run("add")
    assert events == [1, 2]


def test_hooks_accept_hooks_instance(make_agent) -> None:
    seen = []
    agent, _ = make_agent(
        hooks=Hooks(on_step=lambda *args: seen.append(args[0])),
        responses=["hi"],
    )
    agent.run("hello")
    assert seen


def test_system_message_prepended(make_agent) -> None:
    agent, _ = make_agent(system="You are a French assistant.", responses=["bonjour"])
    agent.run("hello")
    assert agent.memory.messages[0]["role"] == "system"
    assert agent.memory.messages[0]["content"] == "You are a French assistant."


def test_system_overrides_existing_system(make_agent) -> None:
    agent, _ = make_agent(system="one", responses=["ok"])
    agent.memory.set_system("two")
    agent.run("hi")
    assert agent.memory.system == "two"


def test_memory_continuity_across_runs(make_agent) -> None:
    agent, _ = make_agent(responses=["first reply"])
    agent.run("first")
    assert len(agent.memory.messages) == 2
    # A second, fresh agent only sends its own user message on the first call.
    agent2, llm2 = make_agent(responses=["second reply"])
    agent2.run("second")
    assert len(llm2.calls[0]) == 1


def test_execute_tool_returns_json_for_structured_results(make_agent) -> None:
    agent, _ = make_agent(tools=[add])
    result = agent.execute_tool("add", {"x": 5, "y": 7})
    assert result == "12"


def test_execute_tool_unknown_name(make_agent) -> None:
    agent, _ = make_agent()
    assert "unknown tool" in agent.execute_tool("missing", {})


def test_execute_tool_generic_exception_is_caught(make_agent) -> None:
    def explode() -> None:
        raise ValueError("boom")

    agent, _ = make_agent(tools=[explode])
    result = agent.execute_tool("explode", {})
    assert "ValueError" in result


def test_default_tools_use_global_registry(make_agent) -> None:
    agent, _ = make_agent()
    assert "add" in agent.available_tools
    assert "double" in agent.available_tools


def test_agent_validates_constructor_args(make_agent) -> None:
    with pytest.raises(TypeError):
        Agent(llm=None)  # type: ignore[arg-type]
    agent, _ = make_agent()
    assert isinstance(agent, Agent)
    with pytest.raises(AgentError):
        agent.run("")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        Agent(llm=FakeLLM(), max_steps=0)


def test_run_rejects_empty_message(make_agent) -> None:
    agent, _ = make_agent()
    with pytest.raises(AgentError):
        agent.run("")
    with pytest.raises(AgentError):
        agent.run("   ")


def test_agent_accepts_tool_mapping_and_registry(make_agent) -> None:
    from truagent.tools import ToolRegistry

    registry = ToolRegistry([add])
    agent, _ = make_agent(tools=registry)
    assert "add" in agent.available_tools
    agent, _ = make_agent(tools={"sum": add})
    assert "sum" in agent.available_tools


def test_format_tool_result_dicts() -> None:
    from truagent.agent import format_tool_result

    assert format_tool_result({"a": 1}) == '{"a": 1}'
    assert format_tool_result("plain") == "plain"
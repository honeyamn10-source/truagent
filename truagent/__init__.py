"""TruAgent — the zero-dependency Python agent framework.

Build, test and ship LLM agents that work everywhere:

* **Zero runtime dependencies** — pure Python standard library only.
* **Bring your own backend** — OpenAI, Ollama, Anthropic, vLLM, LM Studio,
  anything that speaks the OpenAI-compatible protocol (or write your own).
* **Battle-tested loop** — tool calling, retries, memory, middleware, hooks.
* **Production ready** — fully typed, 100% test coverage, MIT licensed.
"""

from .agent import Agent, AgentError, MaxStepsExceeded
from .clients import (
    APIError,
    AssistantMessage,
    BaseLLM,
    OpenAICompatibleClient,
    ToolCall,
)
from .errors import PyagentError, RetryExhausted, ToolError
from .memory import Memory
from .middleware import Hooks, RetryPolicy
from .parse import ToolCall as ParsedToolCall
from .parse import extract_json, extract_tool_call
from .tools import Tool, ToolRegistry, ensure_tool, tool, tool_registry

__version__ = "1.0.0"
__all__ = [
    "APIError",
    "Agent",
    "AgentError",
    "AssistantMessage",
    "BaseLLM",
    "Hooks",
    "MaxStepsExceeded",
    "Memory",
    "OpenAICompatibleClient",
    "ParsedToolCall",
    "PyagentError",
    "RetryExhausted",
    "RetryPolicy",
    "Tool",
    "ToolCall",
    "ToolError",
    "ToolRegistry",
    "__version__",
    "ensure_tool",
    "extract_json",
    "extract_tool_call",
    "tool",
    "tool_registry",
]
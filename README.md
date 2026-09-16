<div align="center">

# TruAgent

**The zero-dependency Python agent framework.**

Build, test and ship LLM agents that work **everywhere** — no heavy deps,
no vendor lock-in, no build complexity.

[![PyPI](https://img.shields.io/badge/PyPI-v1.0.0-blue)](https://pypi.org/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)](#-why-zero-dependencies)
[![Tests](https://img.shields.io/badge/tests-110%20passing-brightgreen)](#-tests)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

---

## ✨ What is TruAgent?

TruAgent is a tiny, dependency-free framework for building LLM agents in
Python. It gives you everything you need to go from "hello world" to a
production agent:

- **A clean agent loop** — think → call a tool → observe → answer.
- **Automatic tool schemas** — decorate a function with `@tool` and the JSON
  schema is reflected from your type annotations and docstrings.
- **Any model backend** — OpenAI, Ollama, Anthropic, vLLM, LM Studio, Groq,
  Together, anything that speaks the OpenAI-compatible protocol. Or write
  your own `BaseLLM` in ~20 lines.
- **Retries, hooks and memory** — built in, with zero magic.
- **No runtime dependencies** — the entire framework runs on the Python
  standard library. No `requests`, no `httpx`, no `pydantic`, no SDKs.

```python
from truagent import Agent, Memory, OpenAICompatibleClient, tool

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

agent = Agent(
    llm=OpenAICompatibleClient(
        base_url="http://localhost:11434/v1",   # Ollama
        model="qwen2.5",
    ),
    tools=[add],
    memory=Memory(),
)

print(agent.run("What is 12345 + 54321?"))
# agent: calls add(12345, 54321) -> 66666
```

---

## 🚀 Quick start

```bash
pip install truagent
```

Then run an example:

```bash
python examples/calculator_agent.py
```

### With any OpenAI-compatible backend

```python
from truagent import Agent, OpenAICompatibleClient

agent = Agent(
    llm=OpenAICompatibleClient(
        api_key="sk-...",                 # omit for local backends
        base_url="https://api.openai.com/v1",
        model="gpt-4o-mini",
        retries=2,
    ),
    tools=[add, search, save_file],
)
```

Local backends (Ollama, LM Studio, vLLM) need no API key:

```python
OpenAICompatibleClient(base_url="http://localhost:11434/v1", model="qwen2.5")
```

---

## 🧠 Core concepts

| Concept | What it is |
|---|---|
| **`Agent`** | Drives the loop: prompt → model → tool calls → answer. |
| **`@tool`** | Turns any Python function into an LLM-callable capability. |
| **`Memory`** | Ordered conversation history with a stable system prompt. |
| **`BaseLLM`** | The interface every backend implements (write your own in minutes). |
| **`RetryPolicy`** | Exponential backoff for transient failures. |
| **`Hooks`** | Observe every step and message in the loop. |

### Tools are just functions

```python
from truagent import tool

@tool
def search(query: str, limit: int = 5) -> list[str]:
    """Search the web or a local index.

    :param query: The search terms.
    :param limit: How many results to return.
    """
    # ... your implementation
    return [...]
```

The `@tool` decorator reflects the JSON schema from the signature and
docstring — including descriptions, defaults and required/optional params.
No hand-written schema.

### Bring your own model

Implement `BaseLLM` in a few lines:

```python
from truagent import AssistantMessage, BaseLLM

class MyBackend(BaseLLM):
    def chat(self, messages) -> AssistantMessage:
        # messages: list[dict]  ->  return text and/or a ToolCall
        return AssistantMessage(text="hello")
```

---

## 🔁 Retries, hooks and memory

```python
from truagent import Agent, Memory, RetryPolicy, Hooks

agent = Agent(
    llm=client,
    tools=[add],
    memory=Memory(system="You are a precise calculator."),
    max_steps=10,
    hooks=Hooks(
        on_step=lambda step, msgs, tool_call: print(f"step {step}"),
        on_message=lambda msg: print(f"model said: {msg.text}"),
    ),
)
```

---

## 🛡️ Why zero dependencies?

Most agent frameworks pull in dozens of packages. TruAgent runs on the
standard library alone:

- **Install in seconds** — no transitive dependency resolution.
- **Works offline** — build, test and ship without network access.
- **Auditable** — ~1,500 lines of Python you can read end to end.
- **No lock-in** — swap backends with a one-line config change.
- **Secure supply chain** — nothing to audit but our own code.

---

## 📚 Examples

- [`examples/calculator_agent.py`](examples/calculator_agent.py) — a safe
  arithmetic agent with a full tokenizer/parser.

---

## 🧪 Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

110 tests covering the agent loop, tool schema reflection, memory, retries,
hooks, JSON parsing and the HTTP client — all hermetic (no network).

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for
guidelines, and check [CHANGELOG.md](CHANGELOG.md) for what's new.

- Open an [issue](https://github.com/honeyamn10-source/truagent/issues)
- Fork and open a [pull request](https://github.com/honeyamn10-source/truagent/pulls)

## 📄 License

MIT — see [LICENSE](LICENSE).

---

<div align="center">

**Built with ❤️ for the open-source AI community.**

</div>
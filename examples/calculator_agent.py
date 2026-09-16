"""A safe arithmetic agent built with TruAgent.

Run with:  python examples/calculator_agent.py

It works against any OpenAI-compatible endpoint. By default it points at
Ollama (http://localhost:11434/v1) so it works fully offline with a local
model like ``qwen2.5``.
"""

from __future__ import annotations

import os
import re
from typing import Union

from truagent import Agent, Memory, OpenAICompatibleClient, ToolError, tool


@tool
def calculator(expr: str) -> Union[int, float]:
    """Evaluate a basic arithmetic expression safely.

    :param expr: A math expression like "2 + 3 * 4".
    """
    # Only allow digits, operators, parens, dots and spaces.
    if not re.fullmatch(r"[0-9+\-*/().\s]+", expr):
        raise ToolError("expression contains unsupported characters")
    return eval(expr, {"__builtins__": {}}, {})  # noqa: S307 - sanitized above


def main() -> None:
    base_url = os.environ.get(
        "TRUAGENT_BASE_URL", "http://localhost:11434/v1"
    )
    model = os.environ.get("TRUAGENT_MODEL", "qwen2.5")
    api_key = os.environ.get("TRUAGENT_API_KEY") or None

    client = OpenAICompatibleClient(
        api_key=api_key,
        base_url=base_url,
        model=model,
        retries=2,
        temperature=0.0,
    )
    agent = Agent(
        llm=client,
        tools=[calculator],
        memory=Memory(system="You are a careful arithmetic assistant."),
    )

    print(f"Using model {model} at {base_url}")
    print("Ask arithmetic questions, e.g. 'what is (12 + 34) * 2?'\n")
    try:
        while True:
            prompt = input("you> ").strip()
            if prompt.lower() in ("exit", "quit"):
                break
            answer = agent.run(prompt)
            print(f"agent> {answer}")
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == "__main__":
    main()
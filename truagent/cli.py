"""TruAgent command-line interface."""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="truagent", description="TruAgent - zero-dependency LLM agent framework")
    sub = parser.add_subparsers(dest="command")

    p_run = sub.add_parser("run", help="run the agent on a task")
    p_run.add_argument("prompt", nargs="+")
    p_run.add_argument("--model", default="gpt-4o-mini")
    p_run.add_argument("--base-url", default="https://api.openai.com/v1")
    p_run.add_argument("--api-key", default="")
    p_run.add_argument("--max-steps", type=int, default=8)
    p_run.set_defaults(func=_cmd_run)

    sub.add_parser("version", help="print the installed version").set_defaults(func=_cmd_version)

    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    return args.func(args)


def _cmd_version(args) -> int:
    from . import __version__

    print(f"truagent {__version__}")
    return 0


def _cmd_run(args) -> int:
    from .agent import Agent
    from .clients import OpenAICompatibleClient
    from .memory import Memory

    prompt = " ".join(args.prompt)
    client = OpenAICompatibleClient(
        api_key=args.api_key or None,
        base_url=args.base_url,
        model=args.model,
        retries=2,
    )
    agent = Agent(llm=client, max_steps=args.max_steps, memory=Memory())
    print(f"agent> {prompt}")
    try:
        answer = agent.run(prompt)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"answer> {answer}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
# Contributing to TruAgent

Thank you for wanting to make TruAgent better! This project is built on a
simple idea: **zero-dependency, high-quality, auditable agent tooling**.

## Development setup

```bash
git clone https://github.com/honeyamn10-source/truagent.git
cd truagent
pip install -e ".[dev]"
```

## Running tests and lint

```bash
pytest tests/ -v          # run the full suite
ruff check .              # lint
```

The test suite is 100% hermetic — it never touches the network.

## Coding conventions

- Keep the **zero-dependency** rule: the runtime package must import only
  the Python standard library. Dev/test dependencies live in the `dev`
  extra only.
- Support Python 3.9+.
- Public API must be fully typed.
- Follow the existing style: module docstring, `from __future__ import
  annotations`, clean line length (100).

## What to contribute

High-value contributions include:

- New `BaseLLM` implementations for additional backends.
- More examples showing real-world agent patterns.
- Additional middleware (rate limiting, tracing, caching).
- Performance improvements and edge-case hardening in the parser.

## Commit style

Use conventional commits, e.g.:

```
feat: add streaming support to OpenAICompatibleClient
fix: handle empty tool arguments in parse_arguments
docs: clarify Memory.trim semantics
test: cover retry exhaustion path
```

## Opening a PR

1. Fork the repository.
2. Create a branch: `git checkout -b feat/my-change`.
3. Make your change, add tests, run `pytest` and `ruff`.
4. Open a pull request with a clear description.

Thanks for contributing!
# Changelog

All notable changes to TruAgent are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-09-16

### Added
- Zero-dependency agent loop: think, call tools, observe, answer.
- `@tool` decorator with automatic JSON schema reflection from type
  annotations and docstrings.
- `OpenAICompatibleClient` using only the standard library (`urllib`),
  with retries, custom headers, and configurable model/timeout.
- `Memory` with system prompt handling, trimming, JSON serialization and
  token estimation.
- `RetryPolicy` with exponential backoff; `Hooks` for step/message events.
- Robust JSON parsing (`extract_json`, `extract_tool_call`,
  `parse_arguments`, `repair_json`) for messy model output.
- CLI (`truagent run ...`) and a calculator agent example.
- Fully typed public API with `py.typed` marker.
- 110 hermetic tests with 100% pass rate and clean `ruff` linting.
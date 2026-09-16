"""Tests for middleware: RetryPolicy and Hooks."""

from __future__ import annotations

import pytest

from truagent.errors import PyagentError, RetryExhausted
from truagent.middleware import Hooks, RetryPolicy


class FlakyError(PyagentError):
    pass


def test_succeeds_after_transient_failures() -> None:
    calls = {"count": 0}

    @RetryPolicy(max_retries=3, base_delay=0)
    def flaky() -> str:
        calls["count"] += 1
        if calls["count"] < 3:
            raise FlakyError("not yet")
        return "ok"

    assert flaky() == "ok"
    assert calls["count"] == 3


def test_raises_retry_exhausted_after_all_attempts() -> None:
    @RetryPolicy(max_retries=2, base_delay=0)
    def always_fails() -> None:
        raise FlakyError("nope")

    with pytest.raises(RetryExhausted):
        always_fails()


def test_non_pyagent_error_propagates_immediately() -> None:
    @RetryPolicy(max_retries=3, base_delay=0)
    def hard_fail() -> None:
        raise RuntimeError("not retryable")

    with pytest.raises(RuntimeError):
        hard_fail()


def test_success_on_first_attempt() -> None:
    @RetryPolicy(max_retries=5, base_delay=0)
    def instant() -> str:
        return "yes"

    assert instant() == "yes"


def test_wrapper_preserves_function_name() -> None:
    @RetryPolicy(max_retries=1, base_delay=0)
    def named_function() -> None:
        pass

    assert named_function.__name__ == "named_function"


def test_backoff_growth_is_computed() -> None:
    policy = RetryPolicy(max_retries=5, base_delay=1.0, max_delay=10.0)
    assert policy.compute_delay(0) == 1.0
    assert policy.compute_delay(1) == 2.0
    assert policy.compute_delay(2) == 4.0
    assert policy.compute_delay(5) == 10.0  # capped


def test_validation() -> None:
    with pytest.raises(ValueError):
        RetryPolicy(max_retries=-1)
    with pytest.raises(ValueError):
        RetryPolicy(base_delay=-1.0)
    with pytest.raises(ValueError):
        RetryPolicy(max_delay=-1.0)


def test_on_step_invoked() -> None:
    events = []
    hooks = Hooks(on_step=lambda step, messages, tool_call: events.append(step))
    hooks.step(1, [], None)
    assert events == [1]


def test_on_message_invoked() -> None:
    messages = []
    hooks = Hooks(on_message=messages.append)
    hooks.message("hi")
    assert messages == ["hi"]


def test_none_callbacks_are_skipped() -> None:
    hooks = Hooks()
    hooks.step(1, [], None)  # should not raise
    hooks.message("hi")  # should not raise
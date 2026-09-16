"""Middleware: retry policies and event hooks for the agent loop."""

from __future__ import annotations

import time
from functools import wraps
from typing import Any, Callable

from .errors import PyagentError, RetryExhausted


class RetryPolicy:
    """Retry a callable with exponential backoff on transient failures."""

    def __init__(self, max_retries: int = 3, base_delay: float = 0.5, max_delay: float = 8.0) -> None:
        if not isinstance(max_retries, int) or max_retries < 0:
            raise ValueError("max_retries must be a non-negative integer")
        if base_delay < 0 or max_delay < 0:
            raise ValueError("delays must be non-negative")
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    def compute_delay(self, attempt: int) -> float:
        """Exponential backoff with a cap: ``base_delay * 2 ** attempt``."""
        return min(self.max_delay, self.base_delay * (2 ** attempt))

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_error: Exception | None = None
            for attempt in range(self.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except PyagentError as exc:
                    last_error = exc
                    if attempt < self.max_retries:
                        time.sleep(self.compute_delay(attempt))
            raise RetryExhausted(f"operation failed after {self.max_retries} retries") from last_error

        return wrapper


class Hooks:
    """Event hooks fired during an agent run."""

    def __init__(
        self,
        on_step: Callable[[int, list[dict[str, Any]], Any], None] | None = None,
        on_message: Callable[[Any], None] | None = None,
    ) -> None:
        self.on_step = on_step
        self.on_message = on_message

    def step(self, step: int, messages: list[dict[str, Any]], tool_call: Any) -> None:
        if self.on_step:
            self.on_step(step, messages, tool_call)

    def message(self, message: Any) -> None:
        if self.on_message:
            self.on_message(message)
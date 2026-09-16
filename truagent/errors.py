"""Exception hierarchy for TruAgent."""

from __future__ import annotations


class PyagentError(Exception):
    """Base class for all TruAgent errors."""


class AgentError(PyagentError):
    """Raised for agent-level problems (invalid construction, empty input, ...)."""


class MaxStepsExceeded(AgentError):
    """Raised when the agent exceeds ``max_steps`` without reaching a final answer."""


class ToolError(PyagentError):
    """Raised when a tool fails to validate or execute."""

    def __init__(self, message: str, tool_name: str | None = None) -> None:
        self.tool_name = tool_name
        super().__init__(message)


class APIError(PyagentError):
    """Raised when a model backend returns an error or is unreachable."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        cause: BaseException | None = None,
    ) -> None:
        self.status_code = status_code
        super().__init__(message)
        if cause is not None:
            self.__cause__ = cause


class RetryExhausted(PyagentError):
    """Raised when a retry policy runs out of attempts."""
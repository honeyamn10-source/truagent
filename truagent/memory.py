"""Conversation memory: append, combine, trim and serialize message history."""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any

_KNOWN_ROLES = ("system", "user", "assistant", "tool")


def _estimate_tokens(content: str) -> int:
    """Rough token estimate: ~4 characters per token, URLs/files count more."""
    if not content:
        return 0
    base = len(content) / 4
    base += content.count("://") * 20
    base += content.count("\n") * 1.5
    return max(1, int(base))


class Memory:
    """An append-only conversation history with a stable system message."""

    def __init__(
        self,
        system: str | None = None,
        messages: list[dict[str, Any]] | None = None,
    ) -> None:
        self._entries: list[dict[str, Any]] = []
        if system is not None:
            self.set_system(system)
        for message in messages or ():
            self.add(message)

    @classmethod
    def from_json(cls, data: str) -> Memory:
        """Build a Memory from the JSON produced by :meth:`to_json`."""
        try:
            messages = json.loads(data)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid memory JSON: {exc}") from exc
        if not isinstance(messages, list):
            raise ValueError("memory JSON must be a list of messages")
        memory = cls()
        for message in messages:
            memory.add(message)
        return memory

    @property
    def messages(self) -> list[dict[str, Any]]:
        """A shallow copy of the message history."""
        return [dict(message) for message in self._entries]

    def _validate(self, message: dict[str, Any]) -> None:
        if not isinstance(message, dict):
            raise ValueError("message must be a dict")
        role = message.get("role")
        if not isinstance(role, str) or role not in _KNOWN_ROLES:
            raise ValueError(f"message role must be one of {_KNOWN_ROLES}")
        if "content" not in message:
            raise ValueError("message must contain a 'content' key")

    def add(self, message: dict[str, Any]) -> Memory:
        self._validate(message)
        self._entries.append(dict(message))
        return self

    def append(self, message: dict[str, Any]) -> Memory:
        """Alias for :meth:`add`."""
        return self.add(message)

    def set_system(self, content: str) -> Memory:
        """Insert or replace the system message at the front of history."""
        if not isinstance(content, str):
            raise ValueError("system content must be a string")
        keep = [m for m in self._entries if m.get("role") != "system"]
        self._entries = [{"role": "system", "content": content}] + keep
        return self

    @property
    def system(self) -> str | None:
        """The current system message content, if any."""
        for message in self._entries:
            if message.get("role") == "system":
                return message.get("content")
        return None

    def trim(self, max_messages: int) -> Memory:
        """Keep the system message and the most recent N non-system messages."""
        if not isinstance(max_messages, int) or max_messages <= 0:
            raise ValueError("max_messages must be a positive integer")
        system_messages = [m for m in self._entries if m.get("role") == "system"]
        other_messages = [m for m in self._entries if m.get("role") != "system"]
        self._entries = system_messages + other_messages[-max_messages:]
        return self

    def clear(self) -> Memory:
        """Remove all non-system messages, keeping the system prompt."""
        self._entries = [m for m in self._entries if m.get("role") == "system"]
        return self

    def estimate_tokens(self) -> int:
        """Estimate the total token cost of the stored history."""
        return sum(_estimate_tokens(str(message.get("content", ""))) for message in self._entries)

    def to_json(self) -> str:
        return json.dumps(self._entries, ensure_ascii=False, default=str)

    def __add__(self, other: Memory | dict[str, Any]) -> Memory:
        """Combine this Memory with another Memory or a single message."""
        new_memory = Memory()
        new_memory._entries = [dict(m) for m in self._entries]
        if isinstance(other, Memory):
            new_memory._entries.extend(dict(m) for m in other._entries)
        elif isinstance(other, dict):
            new_memory.add(other)
        else:
            raise ValueError("can only combine Memory with Memory or a message dict")
        return new_memory

    def __iadd__(self, other: Memory | dict[str, Any]) -> Memory:
        combined = self + other
        self._entries = combined._entries
        return self

    def __iter__(self) -> Iterator[dict[str, Any]]:
        return iter([dict(m) for m in self._entries])

    def __getitem__(self, index: int) -> dict[str, Any]:
        return dict(self._entries[index])

    def __len__(self) -> int:
        return len(self._entries)

    def __repr__(self) -> str:
        return f"Memory({len(self._entries)} messages)"
"""
Rolling window context manager for long‑running Claude sessions.

This component maintains a bounded list of messages exchanged with Claude.  When the
conversation grows beyond a configurable threshold, it compresses the oldest part of
the context into a concise summary.  It also keeps track of token usage via
``TokenCounter``.
"""

from __future__ import annotations

from typing import List, Dict, Any

try:
    import anthropic  # type: ignore
except ImportError:
    # Define a stub so type checkers don't complain when anthropic isn't installed
    class anthropic:  # type: ignore
        class Anthropic:  # type: ignore
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                raise RuntimeError("Anthropic client not available in this environment.")

from token_counter import TokenCounter


class ContextManager:
    """Manage message history and automatically compress old messages."""

    # The absolute maximum number of messages allowed in the history.
    MAX_MESSAGES: int = 20
    # When the number of messages exceeds this value, trigger compression.
    COMPRESS_ABOVE: int = 15

    def __init__(self, client: anthropic.Anthropic) -> None:
        self.client = client
        # List of message dictionaries with "role" and "content" keys.
        self.messages: List[Dict[str, str]] = []
        self.counter = TokenCounter()
        self.compressed_count: int = 0

    def add_user(self, content: str) -> None:
        """Append a user message to the conversation history."""
        self.messages.append({"role": "user", "content": content})

    def call(self, system: str = "") -> str:
        """
        Call Claude with the current message history and return the assistant reply.

        If the history length exceeds ``COMPRESS_ABOVE``, a summary of the oldest
        messages is generated and replaces them.  Token usage for each call is
        recorded via the ``TokenCounter`` instance.
        """
        # Perform compression when necessary
        if len(self.messages) > self.COMPRESS_ABOVE:
            self._compress_old_messages()

        kwargs: Dict[str, Any] = {
            "model": "claude-sonnet-4-6",
            "max_tokens": 4096,
            "messages": self.messages,
        }
        if system:
            kwargs["system"] = system

        response = self.client.messages.create(**kwargs)
        # Track usage from this call
        self.counter.record(response)

        assistant_msg: str = response.content[0].text
        self.messages.append({"role": "assistant", "content": assistant_msg})
        return assistant_msg

    def _compress_old_messages(self) -> None:
        """Summarize and replace the oldest messages with a concise description."""
        # Number of recent messages to keep verbatim
        keep_recent = 6
        old = self.messages[:-keep_recent]
        recent = self.messages[-keep_recent:]

        # Construct a summarization prompt by concatenating truncated messages
        summary_prompt = (
            "다음 대화 내용을 3-5문장으로 요약해줘. "
            "핵심 결정사항과 발견한 버그에 집중할 것:\n\n"
            + "\n".join(
                f"[{m['role']}]: {m['content'][:200]}" for m in old
            )
        )

        # Ask Claude to generate the summary
        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=512,
            messages=[{"role": "user", "content": summary_prompt}],
        )
        summary = response.content[0].text
        self.compressed_count += len(old)

        # Replace the old messages with the summary and a handshake acknowledgement
        self.messages = [
            {"role": "user", "content": f"[이전 대화 요약]\n{summary}"},
            {
                "role": "assistant",
                "content": "이전 컨텍스트를 확인했습니다. 계속 진행하겠습니다.",
            },
            *recent,
        ]
        print(
            f"[ContextManager] {len(old)}개 메시지 압축 완료 (누적: {self.compressed_count}개)"
        )
"""
Token usage accounting utilities for Claude API calls.

This module defines two classes to measure and aggregate token usage.  It
encapsulates pricing logic based on Anthropic's Claude Sonnet 4 model and
issues warnings when the context window nears its limit.
"""

from dataclasses import dataclass
from typing import Optional

try:
    import anthropic  # type: ignore
except ImportError:
    # Provide a minimal stub when the anthropic package is unavailable.  This
    # allows basic type checking and unit testing without installing the real
    # dependency.  When running against the real API, the actual package will
    # override this stub.
    class anthropic:  # type: ignore
        class types:
            class Message:  # type: ignore
                class Usage:
                    input_tokens: int = 0
                    output_tokens: int = 0
                    cache_read_input_tokens: int = 0
                    cache_creation_input_tokens: int = 0

                usage: "anthropic.types.Message.Usage"  # type: ignore


@dataclass
class TokenUsage:
    """Represents token usage metrics for a single model call."""

    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0

    @property
    def total(self) -> int:
        """Return the sum of input and output tokens."""
        return self.input_tokens + self.output_tokens

    @property
    def cost_usd(self) -> float:
        """Estimate cost (USD) based on Claude Sonnet 4 pricing (2026‑03)."""
        # Pricing per million tokens: input $3, output $15, cache read $0.3.
        input_cost = self.input_tokens * 3.0 / 1_000_000
        output_cost = self.output_tokens * 15.0 / 1_000_000
        cache_read_cost = self.cache_read_tokens * 0.3 / 1_000_000
        return input_cost + output_cost + cache_read_cost

    def __add__(self, other: "TokenUsage") -> "TokenUsage":
        """Combine usage from multiple calls."""
        return TokenUsage(
            input_tokens=self.input_tokens + other.input_tokens,
            output_tokens=self.output_tokens + other.output_tokens,
            cache_read_tokens=self.cache_read_tokens + other.cache_read_tokens,
            cache_write_tokens=self.cache_write_tokens + other.cache_write_tokens,
        )


class TokenCounter:
    """
    Aggregate token usage across a session and warn when approaching the
    model's context window limit.

    This class maintains cumulative usage and a history of usage per turn.  It
    emits a console warning if a single call consumes more than the
    configured fraction of the total context window.
    """

    # Maximum context window for Claude Sonnet 4
    CONTEXT_LIMIT: int = 200_000
    # Warn when current input exceeds 80 % of the context window
    WARN_THRESHOLD: float = 0.80

    def __init__(self) -> None:
        self.session_usage: TokenUsage = TokenUsage()
        self.turn_history: list[TokenUsage] = []

    def record(self, response: "anthropic.types.Message") -> TokenUsage:
        """Record token usage from a model response and update running totals."""
        usage = TokenUsage(
            input_tokens=getattr(response.usage, "input_tokens", 0),
            output_tokens=getattr(response.usage, "output_tokens", 0),
            cache_read_tokens=getattr(response.usage, "cache_read_input_tokens", 0),
            cache_write_tokens=getattr(response.usage, "cache_creation_input_tokens", 0),
        )
        self.session_usage = self.session_usage + usage
        self.turn_history.append(usage)
        self._check_threshold(usage.input_tokens)
        return usage

    def _check_threshold(self, current_input: int) -> None:
        """Print a warning if the current input exceeds the threshold."""
        ratio = current_input / self.CONTEXT_LIMIT
        if ratio > self.WARN_THRESHOLD:
            print(
                f"[WARNING] 컨텍스트 사용률 {ratio:.1%} "
                f"({current_input:,} / {self.CONTEXT_LIMIT:,} 토큰) — 압축 권장"
            )

    def report(self) -> str:
        """Return a human‑readable summary of cumulative token usage."""
        lines = [
            "=== 토큰 사용 현황 ===",
            f"총 입력 토큰:  {self.session_usage.input_tokens:>10,}",
            f"총 출력 토큰:  {self.session_usage.output_tokens:>10,}",
            f"캐시 읽기:     {self.session_usage.cache_read_tokens:>10,}",
            f"예상 비용(USD): ${self.session_usage.cost_usd:>9.4f}",
            f"누적 턴 수:    {len(self.turn_history):>10}",
        ]
        return "\n".join(lines)
"""
Entry point for Lab 05 context management demonstration.

This script wires together ``TokenCounter``, ``ContextManager`` and ``StateTracker`` to
drive a simple Ralph loop.  It demonstrates persisting the fix plan and progress
across multiple runs, automatically compressing old context when the history
becomes large, and reporting token usage at the end.

To execute, ensure that the ``ANTHROPIC_API_KEY`` environment variable is set
and that the ``anthropic`` package is installed.  When running without those
requirements, the script will raise an exception upon attempting to call the
model API.
"""

import os
import sys

try:
    import anthropic  # type: ignore
except ImportError as exc:
    raise RuntimeError(
        "The anthropic package is required to run main.py. Install it via pip."
    ) from exc

from token_counter import TokenCounter
from context_manager import ContextManager
from state_tracker import StateTracker


def main() -> None:
    # Initialise Anthropics client.  The API key is picked up from the
    # environment (ANTHROPIC_API_KEY) by the library.
    client = anthropic.Anthropic()
    ctx = ContextManager(client)
    tracker = StateTracker()

    # Load any existing fix plan and feed it into the conversation
    prior_plan = tracker.load_fix_plan()
    if prior_plan:
        ctx.add_user(
            "이전 세션에서 작성한 fix_plan.md:\n"
            f"{prior_plan}\n\n"
            "이 계획을 참고해서 계속 진행해줘."
        )
    else:
        ctx.add_user("tests/ 디렉터리의 모든 테스트를 통과시켜줘.")

    # Run a limited number of turns for demonstration purposes
    for i in range(5):
        response = ctx.call(system="You are an autonomous coding agent.")
        # Save the first 100 characters of the assistant's reply for easy log viewing
        tracker.save_progress(i + 1, "running", response[:100])
        print(f"\n--- Turn {i+1} ---\n{response[:300]}")

    # Print final usage summary
    print("\n" + ctx.counter.report())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Log the exception and write a fix plan for later recovery
        tracker = StateTracker()
        error_msg = str(e)
        analysis = (
            "예외가 발생했습니다. API 키가 설정되지 않았거나 네트워크 오류일 수 있습니다."
        )
        next_steps = [
            "ANTHROPIC_API_KEY 환경 변수를 확인한다.",
            "네트워크 연결을 점검한다.",
            "필요하다면 재시도한다.",
        ]
        tracker.save_fix_plan(error_msg, analysis, next_steps)
        raise
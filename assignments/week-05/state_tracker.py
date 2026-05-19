"""
File‑based persistence for Ralph loop state.

This module encapsulates read/write operations for two companion files used in
the lab assignment:

* ``claude-progress.txt`` records a textual log of each iteration, with
  optional notes summarizing the assistant response.  Each call to
  ``save_progress`` appends a timestamped entry to this file.
* ``fix_plan.md`` captures the current error, analysis, and next steps when
  iterating through the Ralph loop.  It is overwritten on each save.

By storing progress on disk, the agent can restore context after an
interruption or across separate execution sessions.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional


class StateTracker:
    """Persist and restore session state across iterations."""

    def __init__(self, base_dir: str = ".") -> None:
        self.base = Path(base_dir)
        # Path to the progress log and fix plan files
        self.progress_file: Path = self.base / "claude-progress.txt"
        self.fix_plan_file: Path = self.base / "fix_plan.md"

    def save_progress(self, iteration: int, status: str, notes: str = "") -> None:
        """
        Append a progress entry to ``claude-progress.txt``.

        :param iteration: Current iteration index (1‑based).
        :param status: Short status string (e.g., "running" or "error").
        :param notes: Optional free‑form text to include on a following indented line.
        """
        timestamp = datetime.now().isoformat()
        entry = f"[{timestamp}] iter={iteration} status={status}"
        if notes:
            # Indent notes on a new line for readability
            entry += f"\n  Notes: {notes}"
        entry += "\n"

        with open(self.progress_file, "a", encoding="utf-8") as f:
            f.write(entry)

    def load_progress(self) -> List[str]:
        """
        Read and return all lines from ``claude-progress.txt``.  If the file does
        not exist, an empty list is returned.
        """
        if not self.progress_file.exists():
            return []
        return self.progress_file.read_text(encoding="utf-8").splitlines()

    def save_fix_plan(self, error: str, analysis: str, next_steps: List[str]) -> None:
        """
        Overwrite ``fix_plan.md`` with a new plan based on the latest error.

        :param error: The error message or stack trace encountered.
        :param analysis: Explanation of root causes and observations.
        :param next_steps: A list of bullet points describing actions to take.
        """
        error_block = "~~~\n" + error + "\n~~~"
        steps_block = "\n".join(f"- {s}" for s in next_steps)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        content = (
            f"# Fix Plan\n"
            f"Updated: {timestamp}\n\n"
            f"## 현재 오류\n{error_block}\n\n"
            f"## 분석\n{analysis}\n\n"
            f"## 다음 시도\n{steps_block}\n"
        )
        self.fix_plan_file.write_text(content, encoding="utf-8")

    def load_fix_plan(self) -> Optional[str]:
        """
        Load the contents of ``fix_plan.md`` if it exists, otherwise return ``None``.
        """
        if not self.fix_plan_file.exists():
            return None
        return self.fix_plan_file.read_text(encoding="utf-8")

    def get_last_status(self) -> str:
        """
        Return the last recorded status line from ``claude-progress.txt``, or a
        default message if no progress has been saved.
        """
        lines = self.load_progress()
        return lines[-1] if lines else "no prior progress"
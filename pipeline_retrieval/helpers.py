import os
import sys
import time
from dataclasses import dataclass, field
from datetime import timedelta, datetime
from typing import Optional


def _format_seconds(seconds: float) -> str:
    seconds = max(0.0, float(seconds))
    s = int(round(seconds))
    h, rem = divmod(s, 3600)
    m, s = divmod(rem, 60)
    if h > 0:
        return f"{h:d}h {m:02d}m {s:02d}s"
    if m > 0:
        return f"{m:d}m {s:02d}s"
    return f"{s:d}s"


def _render_progress_bar(done: int, total: int, width: int = 30) -> str:
    total = max(1, int(total))
    done = max(0, min(int(done), total))
    pct = int((done * 100) / total)  # stable, no rounding jumps
    filled = int(round(width * done / total))
    bar = "=" * filled + "-" * (width - filled)
    return f"[{bar}] {pct}% ({done}/{total})"


def _get_key_nonblocking(timeout_sec: float) -> Optional[str]:
    """
    Return a single character if pressed within timeout_sec, else None.
    Cross-platform: Windows (msvcrt), POSIX (select+termios).
    """
    try:
        import msvcrt  # type: ignore
        end = time.time() + timeout_sec
        while time.time() < end:
            if msvcrt.kbhit():
                return msvcrt.getwch()
            time.sleep(0.02)
        return None
    except ImportError:
        import select
        import termios
        import tty

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            r, _, _ = select.select([sys.stdin], [], [], timeout_sec)
            if r:
                return sys.stdin.read(1)
            return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def compute_total_runs(mode: str, pipelines: list) -> int:
    """
    Computes total number of pipeline executions for the whole job.
    """
    n = len(pipelines)
    if mode in ("mean_test", "best_test"):
        return n              # one run per pipeline
    return n * n              # N pipelines × (1 own + N-1 cross) = N×N


@dataclass
class GlobalRunsEtaTracker:
    """
    One tracker for the entire job (all pipelines / datasets).
    Prints a single global progress bar + ETA, and offers cancel countdown after each run.
    """
    total_runs: int
    label: str = "Global"
    print_every: int = 1
    bar_width: int = 30
    countdown_from: int = 3
    cancel_key: str = "c"
    overwrite_line: bool = False  # set True if you prefer updating one line

    start_time: float = field(default_factory=time.perf_counter)
    start_timestamp: datetime = datetime.now()
    runs_done: int = 0
    _run_start: Optional[float] = None
    _avg_run_sec: Optional[float] = None

    def start_run(self) -> None:
        self._run_start = time.perf_counter()

    def end_run(self) -> None:
        # duration bookkeeping
        dur = None
        if self._run_start is not None:
            dur = time.perf_counter() - self._run_start
        self._run_start = None

        self.runs_done += 1

        if dur is not None:
            if self._avg_run_sec is None:
                self._avg_run_sec = dur
            else:
                self._avg_run_sec = self._avg_run_sec + (dur - self._avg_run_sec) / self.runs_done

        if self.print_every > 0 and (self.runs_done % self.print_every == 0 or self.runs_done == self.total_runs):
            self.print_status(last_run_sec=dur)

        self._post_run_cancel_prompt()

    def print_status(self, last_run_sec: Optional[float] = None) -> None:
        elapsed = time.perf_counter() - self.start_time
        bar = _render_progress_bar(self.runs_done, self.total_runs, width=self.bar_width)
        remaining_runs = max(0, self.total_runs - self.runs_done)

        if self._avg_run_sec is None:
            eta_txt = "ETA=--"
            avg_txt = "avg/run=--"
            st_txt = "ST: "
            etc_txt = "ETC: "
        else:
            eta_txt = f"ETA={_format_seconds(remaining_runs * self._avg_run_sec)}"
            avg_txt = f"avg/run={_format_seconds(self._avg_run_sec)}"
            st_txt = f"ST: {self.start_timestamp}"
            est_time_of_completion = datetime.now() + timedelta(seconds=remaining_runs * self._avg_run_sec)
            etc_txt = f"ETC: {est_time_of_completion}"

        parts = [f"{self.label}", bar, f"elapsed={_format_seconds(elapsed)}", avg_txt, eta_txt, st_txt, etc_txt]
        if last_run_sec is not None:
            parts.append(f"last={_format_seconds(last_run_sec)}")

        msg = " | ".join(parts)

        if self.overwrite_line:
            # overwrite same line (nice for long runs)
            print("\r" + msg + " " * 10, end="", flush=True)
            if self.runs_done == self.total_runs:
                print()  # newline at end
        else:
            print(msg)

    def _post_run_cancel_prompt(self) -> None:
        for t in range(int(self.countdown_from), 0, -1):
            print(f"Press '{self.cancel_key}' to cancel... continuing in {t} ", end="", flush=True)
            ch = _get_key_nonblocking(1.0)
            print("\r" + (" " * 80) + "\r", end="", flush=True)
            if ch is not None and ch.lower() == self.cancel_key.lower():
                print("Cancelled by user. Terminating.")
                raise SystemExit(1)


def create_global_tracker(mode: str, pipelines: list, *, label: Optional[str] = None) -> GlobalRunsEtaTracker:
    total = compute_total_runs(mode, pipelines)
    tracker = GlobalRunsEtaTracker(
        total_runs=total,
        label=label or f"Global [{mode}]",
        print_every=1,
        bar_width=30,
        countdown_from=3,
        cancel_key="c",
        overwrite_line=False,  # set True if you want a single updating line
    )
    print(f"Planned total runs ({mode}): {total}")
    tracker.print_status()
    return tracker

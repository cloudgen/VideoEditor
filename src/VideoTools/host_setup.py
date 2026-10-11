# =============================================================================
# CIAO-Lite Protection Zone
# Do NOT simplify, refactor, or remove without explicit user instruction
# This section exists for safety and anti-fragility reasons
# Windows and host environment for the setup verb.
# requirement-runtime-prerequisites — pip floors, _curses, ffmpeg.
# requirement-python-cli-interface — verb setup stays off the text menu.
# requirement-python-cli-logging — ensure_geteuid before ChronicleLogger.
# requirement-python-oop — class HostSetup.
# requirement-python-windows — Windows host contract. The X11 window stays.
# =============================================================================
from __future__ import annotations

import importlib
import os
import shutil
import subprocess
import sys


class HostSetup:
    """Prepare the interpreter and report ffmpeg and the picture window.

    Pip installs the declared floors. On Windows, a missing curses module
    is installed with windows-curses, and a missing ffmpeg is attempted
    with winget. GTK 4 and GStreamer stay host libraries.
    """

    PIP_SPECS = (
        "ChronicleLogger>=1.3.1",
        "opencv-python-headless>=5.0.0.93",
    )
    WINDOWS_CURSES_SPEC = "windows-curses"
    FFMPEG_WINGET_ID = "Gyan.FFmpeg"

    @staticmethod
    def ensure_geteuid(os_module=None):
        """Bind os.geteuid when this interpreter has none.

        ChronicleLogger treats euid 0 as root. Windows Python has no geteuid.
        A non-zero return keeps the log folder with the user.
        requirement-python-cli-logging. This does not edit ChronicleLogger.
        """
        module = os if os_module is None else os_module
        if hasattr(module, "geteuid"):
            return

        def _not_root():
            return 1

        module.geteuid = _not_root

    def __init__(
        self,
        logger=None,
        runner=None,
        windows=None,
        curses_ok=None,
        which=None,
    ):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="HostSetup")
        self.runner = runner or self._subprocess_runner
        self._windows = windows
        self._curses_ok = curses_ok
        self._which = which or shutil.which

    def windows_host(self) -> bool:
        """True on Windows, including Windows Python under Git Bash."""
        if self._windows is not None:
            return bool(self._windows)
        if os.name == "nt" or sys.platform.startswith("win"):
            return True
        return os.environ.get("OS", "").lower().startswith("windows")

    def argv_pip(self, specs) -> list:
        """General Purpose: pip install for this interpreter. No sudo."""
        argv = [sys.executable, "-m", "pip", "install"]
        argv.extend(specs)
        return argv

    def argv_winget_ffmpeg(self) -> list:
        """General Purpose: non-interactive winget install of FFmpeg."""
        return [
            "winget",
            "install",
            "-e",
            "--id",
            self.FFMPEG_WINGET_ID,
            "--accept-package-agreements",
            "--accept-source-agreements",
            "--disable-interactivity",
        ]

    def curses_imports(self) -> bool:
        """Whether this process can import curses."""
        if self._curses_ok is not None:
            return bool(self._curses_ok())
        try:
            import curses  # noqa: F401
        except ImportError:
            return False
        return True

    def run(self, window_lines=None) -> int:
        """Install declared libraries and report the Windows host tools."""
        blocks = []
        code = self._append_pip(blocks, self.PIP_SPECS)
        if self.windows_host():
            blocks.append(self._windows_curses_text())
            if not self.curses_imports():
                curses_code = self._append_pip(blocks, (self.WINDOWS_CURSES_SPEC,))
                if curses_code != 0:
                    code = curses_code
                else:
                    importlib.invalidate_caches()
                    if self.curses_imports():
                        blocks.append("curses: this Python can import curses.")
            blocks.append(self._ffmpeg_text())
        else:
            found = self._which("ffmpeg")
            if found:
                blocks.append("ffmpeg: {}".format(found))
            else:
                blocks.append(
                    "ffmpeg: not on PATH. Install FFmpeg and ensure ffmpeg is available."
                )
        if window_lines:
            blocks.append("\n".join(window_lines))
        blocks.append("setup does not install GTK 4 or GStreamer.")
        text = "\n".join(blocks)
        print(text)
        if self.logger is not None:
            self.logger.log_message(
                "setup finished with code {0}".format(code),
                component="HostSetup",
            )
        return code

    def _windows_curses_text(self) -> str:
        if self.curses_imports():
            return "curses: this Python can import curses."
        return "curses: this Python cannot import curses."

    def _ffmpeg_text(self) -> str:
        found = self._which("ffmpeg")
        if found:
            return "ffmpeg: {}".format(found)
        command = " ".join(self.argv_winget_ffmpeg())
        winget = self._which("winget")
        if not winget:
            return (
                "ffmpeg: not on PATH.\n"
                "On Windows, run: {0}".format(command)
            )
        try:
            exit_code, out, err, used = self._run_winget()
        except OSError as exc:
            return (
                "ffmpeg: not on PATH.\n"
                "On Windows, run: {0}\n"
                "{1}".format(command, exc)
            )
        lines = [
            "ffmpeg: not on PATH.",
            "On Windows, ran: {}".format(" ".join(used)),
        ]
        if out and out.strip():
            lines.append(out.strip())
        if err and err.strip():
            lines.append(err.strip())
        if exit_code != 0:
            lines.append("winget exited {}.".format(exit_code))
        found = self._which("ffmpeg")
        if found:
            lines.append("ffmpeg: {}".format(found))
        else:
            lines.append(
                "This process still does not see ffmpeg. "
                "Open a new terminal and run ffmpeg -version."
            )
        return "\n".join(lines)

    def _run_winget(self):
        """Run winget. A refused app alias is retried through cmd.exe."""
        argv = self.argv_winget_ffmpeg()
        try:
            exit_code, out, err = self.runner(argv)
            return exit_code, out, err, argv
        except OSError as first:
            fallback = ["cmd.exe", "/d", "/c"] + argv
            try:
                exit_code, out, err = self.runner(fallback)
            except OSError:
                raise first
            return exit_code, out, err, fallback

    def _append_pip(self, blocks, specs) -> int:
        argv = self.argv_pip(specs)
        try:
            exit_code, out, err = self.runner(argv)
        except OSError as exc:
            blocks.append("$ {0}\n{1}".format(" ".join(argv), exc))
            return 1
        chunks = ["$ {}".format(" ".join(argv))]
        if out and out.strip():
            chunks.append(out.strip())
        if err and err.strip():
            chunks.append(err.strip())
        if exit_code != 0 and len(chunks) == 1:
            chunks.append("pip exited {}".format(exit_code))
        blocks.append("\n".join(chunks))
        return 0 if exit_code == 0 else exit_code

    def _subprocess_runner(self, argv: list) -> tuple:
        """One child. stdin is closed so the child cannot wait."""
        done = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
        )
        return done.returncode, done.stdout or "", done.stderr or ""

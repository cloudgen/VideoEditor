# TP-SETUP-01 — verb setup and the Windows geteuid shim.
# Primary law: requirement-runtime-prerequisites, requirement-python-cli-interface,
# requirement-python-cli-logging.
import io
import os
import unittest
from contextlib import redirect_stdout

from VideoEditor.cli import Cli
from VideoEditor.host_setup import HostSetup


class _OsModule:
    def __init__(self, geteuid=None):
        if geteuid is not None:
            self.geteuid = geteuid


class TestGeteuid(unittest.TestCase):
    """TP-SETUP-01."""

    def test_missing_geteuid_is_not_root(self):
        """A Python without os.geteuid is not treated as root."""
        module = _OsModule()
        HostSetup.ensure_geteuid(module)
        self.assertEqual(module.geteuid(), 1)
        HostSetup.ensure_geteuid(module)
        self.assertEqual(module.geteuid(), 1)

    def test_existing_geteuid_stays(self):
        module = _OsModule(geteuid=lambda: 0)
        HostSetup.ensure_geteuid(module)
        self.assertEqual(module.geteuid(), 0)

    def test_main_binds_geteuid_before_the_logger(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "src", "VideoEditor", "cli.py"
        )
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        start = text.index("def main(argv=None")
        body = text[start:]
        bind = body.index("ensure_geteuid()")
        self.assertLess(bind, body.index("from ChronicleLogger import"))
        self.assertLess(bind, body.index("ChronicleLogger("))


class TestSetupVerb(unittest.TestCase):
    """TP-SETUP-02."""

    def test_setup_is_a_typed_verb_and_stays_off_the_screen(self):
        self.assertIn("setup", Cli.PRODUCT_VERBS)
        real = Cli.stdout_is_tty
        Cli.stdout_is_tty = staticmethod(lambda: True)
        try:
            self.assertFalse(Cli.opens_text_screen(["setup"]))
            self.assertFalse(Cli.opens_window(["setup"]))
        finally:
            Cli.stdout_is_tty = real

    def test_windows_setup_installs_deps_curses_and_names_ffmpeg(self):
        calls = []

        def runner(argv):
            calls.append(list(argv))
            return 0, "installed", ""

        setup = HostSetup(
            runner=runner,
            windows=True,
            curses_ok=lambda: False,
            which=lambda name: "C:\\WindowsApps\\winget.EXE" if name == "winget" else None,
        )
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = setup.run(window_lines=["Window libraries:", "    GTK 4: not available"])
        text = buffer.getvalue()
        self.assertEqual(code, 0, text)
        self.assertEqual(calls[0][1:4], ["-m", "pip", "install"])
        self.assertIn("ChronicleLogger>=1.3.1", calls[0])
        self.assertIn("opencv-python-headless>=5.0.0.93", calls[0])
        self.assertIn("windows-curses", calls[1])
        self.assertEqual(calls[2][0], "winget")
        self.assertIn("Gyan.FFmpeg", calls[2])
        self.assertIn("Window libraries:", text)
        self.assertIn("setup does not install GTK 4 or GStreamer.", text)
        for banned in ("pacman", "msys2", "mingw-w64", "UCRT64", "curl"):
            self.assertNotIn(banned, text)

    def test_other_hosts_do_not_install_curses_or_call_winget(self):
        calls = []

        def runner(argv):
            calls.append(list(argv))
            return 0, "ok", ""

        class _Logger:
            def __init__(self):
                self.lines = []

            def log_message(self, message, component=None, level=None):
                self.lines.append(message)

        logger = _Logger()
        setup = HostSetup(
            logger=logger,
            runner=runner,
            windows=False,
            curses_ok=lambda: False,
            which=lambda name: "/usr/bin/ffmpeg" if name == "ffmpeg" else None,
        )
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = setup.run()
        text = buffer.getvalue()
        self.assertEqual(code, 0, text)
        self.assertEqual(text.count("ChronicleLogger>=1.3.1"), 1)
        self.assertEqual(len(calls), 1)
        self.assertNotIn("windows-curses", calls[0])
        self.assertIn("ffmpeg: /usr/bin/ffmpeg", text)
        self.assertNotIn("winget", text)
        self.assertIn("setup finished with code 0", logger.lines)
        self.assertNotIn("ChronicleLogger>=1.3.1", "\n".join(logger.lines))

    def test_pip_failure_is_the_exit_code(self):
        def runner(argv):
            return 2, "", "no network"

        setup = HostSetup(
            runner=runner,
            windows=False,
            which=lambda name: "/usr/bin/ffmpeg" if name == "ffmpeg" else None,
        )
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = setup.run()
        self.assertEqual(code, 2)
        self.assertIn("no network", buffer.getvalue())

    def test_refused_winget_retries_cmd_and_stays_a_report(self):
        calls = []

        def runner(argv):
            calls.append(list(argv))
            if argv[0] in ("winget", "cmd.exe"):
                raise PermissionError("access denied")
            return 0, "installed", ""

        setup = HostSetup(
            runner=runner,
            windows=True,
            curses_ok=lambda: True,
            which=lambda name: "C:\\WindowsApps\\winget.EXE" if name == "winget" else None,
        )
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = setup.run()
        text = buffer.getvalue()
        self.assertEqual(code, 0, text)
        self.assertEqual(calls[1][0], "winget")
        self.assertEqual(calls[2][:3], ["cmd.exe", "/d", "/c"])
        self.assertIn("Gyan.FFmpeg", text)
        self.assertIn("access denied", text)
        self.assertIn("On Windows, run:", text)


if __name__ == "__main__":
    unittest.main()

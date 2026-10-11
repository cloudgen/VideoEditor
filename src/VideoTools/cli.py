#!/usr/bin/env python
# =============================================================================
# VideoTools CLI — text menu and typed verbs from the join and speed domains.
# Specialized from VideoJoin. Speed steps live beside the join steps.
# Law keys: requirement-python-cli-interface, requirement-python-cli-logging,
#           requirement-python-tui, requirement-python-gui, requirement-python-oop,
#           requirement-python-about, requirement-domain-videotools,
#           requirement-python-error-handling, requirement-python-coding-style,
#           requirement-runtime-prerequisites, requirement-video-ffmpeg-pipeline
# CIAO-Lite: Caution • Intentional • Anti-fragile • Over-protect
# def main writes ChronicleLogger(...). This module does not construct it
# at import time and does not re-export it.
# =============================================================================
from __future__ import print_function, unicode_literals

import argparse
import os
import sys
from pathlib import Path

from .about_page import AboutPage
from .check_system import CheckSystem
from .edit_walk import EditWalk
from .encoder import Encoder
from .file_stage import FileStage
from .gui import Gui
from .host_setup import HostSetup
from .join import Join
from .media_info import MediaInfo
from .run_output import RunOutput
from .self_management import SelfManage
from .tui import Tui


class Cli:
    """Parser, dispatch, verbs, and the tty gate. One class in this file.

    Identity, verb lists, and suffix sets are attributes of this class.
    Collaborators arrive through the constructor. def main stays beside this class.
    """

    from . import __version__ as VERSION

    APP_NAME = "VideoTools"
    CONSOLE_NAME = "video-tools"
    PRODUCT_VERBS = (
        "help",
        "version",
        "about",
        "hello",
        "tui",
        "join",
        "list-videos",
        "edit",
        "list-mp4",
        "self-install",
        "version-check",
        "self-update",
        "self-uninstall",
        "setup",
    )
    LIFECYCLE_VERBS = (
        "version",
        "self-install",
        "version-check",
        "self-update",
        "self-uninstall",
    )
    VIDEO_SUFFIXES = {".mp4", ".mov", ".mkv", ".avi", ".m4v"}
    OUTPUT_SUFFIXES = (".mp4", ".mkv", ".mov")
    AUTHOR_NAME = "Wilgat Wong"
    AUTHOR_EMAIL = "wilgat.wong@gmail.com"
    HOMEPAGE = "https://github.com/cloudgen/VideoTools"
    LAST_UPDATE = "2026-10-10"
    DOWNLOAD_URL = ""
    BASIC_USAGE = "video-tools join"
    RATIO_MIN = 20.0
    RATIO_MAX = 200.0

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Cli")
        self.app_name = Cli.APP_NAME
        self.version = Cli.VERSION
        self.output = RunOutput(Cli.APP_NAME, Cli.VERSION, logger=logger)
        self.join = Join(
            logger=logger,
            video_suffixes=Cli.VIDEO_SUFFIXES,
            output_suffixes=Cli.OUTPUT_SUFFIXES,
        )
        self.stage = FileStage(logger=logger)
        self.media = MediaInfo(self.output, logger=logger)
        self.encoder = Encoder(
            self.output,
            self.media,
            self.stage,
            Cli.RATIO_MIN,
            Cli.RATIO_MAX,
            logger=logger,
        )
        self.edit = EditWalk(
            self.output,
            self.encoder,
            self.media,
            Cli.RATIO_MIN,
            Cli.RATIO_MAX,
            logger=logger,
        )
        self.about = AboutPage(
            CheckSystem(
                logger=logger,
                app_name=Cli.APP_NAME,
                version=Cli.VERSION,
                console_name=Cli.CONSOLE_NAME,
            ),
            Cli.APP_NAME,
            Cli.VERSION,
            Cli.AUTHOR_NAME,
            Cli.LAST_UPDATE,
            Cli.HOMEPAGE,
            Cli.DOWNLOAD_URL,
            Cli.BASIC_USAGE,
            Cli.CONSOLE_NAME,
            logger=logger,
        )
        self.self_manage = SelfManage(Cli.APP_NAME, Cli.VERSION, logger=logger)
        self.host_setup = HostSetup(logger=logger)
        self.tui = Tui(self, logger=logger)
        self.gui = Gui(logger=logger)

    @staticmethod
    def stdin_is_tty():
        """General Purpose: Whether stdin can take interactive prompts."""
        try:
            return sys.stdin.isatty()
        except Exception:
            return False

    @staticmethod
    def stdout_is_tty():
        """General Purpose: Whether the text screen can be drawn on this stdout."""
        try:
            return sys.stdout.isatty()
        except Exception:
            return False

    @staticmethod
    def opens_text_screen(argv):
        """
        General Purpose: Whether this argv draws the text screen.

        The real parser has not run yet. This walk only decides is_quiet.
        Help, version, hello, the pip verbs, and --json do not draw the screen.
        The tui verb does, on a terminal. Empty argv, join, list-videos, about,
        and list-mp4 do, on a terminal. edit does, unless --file, --start, and
        --end are already present. --verbose alone still opens a screen.
        A bare start with DISPLAY set is the window; this still returns True
        so the logger stays quiet.
        """
        if argv is None:
            argv = sys.argv[1:]
        argv = list(argv)
        if "--json" in argv or "--help" in argv or "-h" in argv or "--version" in argv:
            return False
        if not Cli.stdout_is_tty():
            return False
        verb = None
        saw_force = False
        has_file = False
        has_start = False
        has_end = False
        has_folder = False
        has_percent = False
        has_boomerang = False
        has_repeat = False
        index = 0
        while index < len(argv):
            token = argv[index]
            if token == "--force":
                saw_force = True
            elif token == "--verbose":
                pass
            elif token == "--file" or token.startswith("--file="):
                has_file = True
                if token == "--file":
                    index += 1
            elif token == "--start" or token.startswith("--start="):
                has_start = True
                if token == "--start":
                    index += 1
            elif token == "--end" or token.startswith("--end="):
                has_end = True
                if token == "--end":
                    index += 1
            elif token == "--folder" or token.startswith("--folder="):
                has_folder = True
                if token == "--folder":
                    index += 1
            elif token == "--percent" or token.startswith("--percent="):
                has_percent = True
                if token == "--percent":
                    index += 1
            elif token == "--boomerang":
                has_boomerang = True
            elif token == "--repeat":
                has_repeat = True
            elif token.startswith("-"):
                return False
            elif verb is None:
                verb = token
            else:
                return False
            index += 1
        if saw_force and verb != "self-uninstall":
            return False
        if verb in ("help", "hello", "setup") or verb in Cli.LIFECYCLE_VERBS:
            return False
        if verb == "tui":
            return True
        if verb == "edit":
            return not (has_file and has_start and has_end)
        if verb in ("join", "list-videos", "about", "list-mp4"):
            return True
        if verb is not None:
            return False
        if (
            has_file or has_start or has_end or has_folder
            or has_percent or has_boomerang or has_repeat
        ):
            return False
        return True

    @staticmethod
    def opens_window(argv):
        """
        General Purpose: Bare interactive start on X11 opens the window.

        DISPLAY is set for a local X session, XWayland, or ssh -X.
        A verb, a job flag, --json, or a closed stdin stays off this path.
        requirement-python-gui. On Windows the host contract is
        requirement-python-windows. An empty DISPLAY does not remove this window.
        """
        if not os.environ.get("DISPLAY", "").strip():
            return False
        if not Cli.stdin_is_tty() or not Cli.stdout_is_tty():
            return False
        if argv is None:
            argv = sys.argv[1:]
        argv = list(argv)
        if "--json" in argv or "--help" in argv or "-h" in argv or "--version" in argv:
            return False
        verb = None
        has_job = False
        index = 0
        while index < len(argv):
            token = argv[index]
            if token in ("--force", "--verbose"):
                pass
            elif token in ("--boomerang", "--repeat"):
                has_job = True
            elif token in ("--file", "--start", "--end", "--folder", "--percent") or any(
                token.startswith(prefix)
                for prefix in ("--file=", "--start=", "--end=", "--folder=", "--percent=")
            ):
                has_job = True
                if "=" not in token:
                    index += 1
            elif token.startswith("-"):
                return False
            elif verb is None:
                verb = token
            else:
                return False
            index += 1
        return verb is None and not has_job

    def report_error(self, message, nxt):
        """User-visible failure plus the same fact on the logger when one exists."""
        if self.logger is not None:
            self.logger.log_message(
                "{0} Next: {1}".format(message, nxt),
                level="ERROR",
                component="main",
            )
        if self.output is not None:
            self.output._remember(message, nxt)
        print("ERROR: {0}".format(message), file=sys.stderr)
        print("   Next: {0}".format(nxt), file=sys.stderr)
        return 1

    def build_parser(self):
        """
        General Purpose: One optional product verb, plus the edit job flags.
        help is also --help. --force belongs only to self-uninstall.
        Join stays on the current folder. Edit may name a file and a cut.
        """
        name = Cli.APP_NAME
        dist = self.self_manage.DISTRIBUTION
        parser = argparse.ArgumentParser(
            prog=Cli.CONSOLE_NAME,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=(
                "{0} — join two videos, or cut, speed, and optionally boomerang or repeat an MP4.\n"
                "With no arguments on a terminal and DISPLAY set, opens the window.\n"
                "With no arguments on a terminal and no DISPLAY, opens the text menu.\n"
                "With no arguments and no terminal, prints this help and stops.\n"
                "tui opens the text menu on a terminal, including when DISPLAY is set.\n"
                "Product verbs: help, version, about, hello, tui, join, list-videos,\n"
                "edit, list-mp4, self-install, version-check, self-update,\n"
                "self-uninstall, setup.\n"
                "help prints this usage. version prints the installed version.\n"
                "about opens the about page on a terminal. hello does not draw the menu.\n"
                "join asks for two videos in this folder and an output name.\n"
                "list-videos lists eligible videos and does not join.\n"
                "edit asks for a folder, then a file, when those are not already named.\n"
                "list-mp4 lists MP4 files and does not encode.\n"
                "video-join and video-speed call this same program.\n"
                "version-check runs: python -m pip index versions {1}\n"
                "self-update runs: python -m pip install --upgrade {1}\n"
                "self-install runs: python -m pip install {1}\n"
                "self-uninstall runs: python -m pip uninstall -y {1}\n"
                "and needs --force. setup installs the declared pip libraries.\n"
                "On Windows, setup also tries curses and ffmpeg.\n"
                "Empty arguments do not install or update.\n"
                "Join formats: .mp4 .mov .mkv .avi .m4v.\n"
                "Edit input: MP4. For a script, pass edit --file, --start, and --end.\n"
                "--json prints one object and does not open the text menu.\n"
                "This product does not cut, speed, or boomerang inside join."
                .format(name, dist)
            ),
        )
        parser.add_argument(
            "verb",
            nargs="?",
            default=None,
            metavar="verb",
            help=(
                "Product verb: help, version, about, hello, tui, join, list-videos, "
                "edit, list-mp4, self-install, version-check, self-update, "
                "self-uninstall, or setup"
            ),
        )
        parser.add_argument(
            "--version",
            action="version",
            version="{0} {1}".format(Cli.APP_NAME, Cli.VERSION),
        )
        parser.add_argument("--file", help="MP4 path for a non-interactive edit")
        parser.add_argument(
            "--folder",
            help="Folder of MP4s for list-mp4 or an edit that still needs a file",
        )
        parser.add_argument(
            "--start",
            type=float,
            help="Cut start seconds (with --file and --end)",
        )
        parser.add_argument(
            "--end",
            type=float,
            help="Cut end seconds (with --file and --start)",
        )
        parser.add_argument(
            "--percent",
            type=float,
            default=None,
            help="New length percent of the cut (default 100; allowed 20–200)",
        )
        parser.add_argument(
            "--boomerang",
            action="store_true",
            help="Append the reverse after the forward clip. Not with --repeat",
        )
        parser.add_argument(
            "--repeat",
            action="store_true",
            help="Append the forward clip again so it plays twice. Not with --boomerang",
        )
        parser.add_argument(
            "--json",
            action="store_true",
            help="Quiet stdout and print one JSON object. Does not open the text menu.",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Accepted. A text screen and --json stay quiet.",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Confirm self-uninstall. Required on the command line.",
        )
        return parser

    def _page(self, text):
        stream = sys.stderr if self.output.json_mode else sys.stdout
        print(text, file=stream)
        return 0

    def _verb_hello(self):
        """Hello from this package, then the help next step. Does not draw the menu."""
        stream = sys.stderr if self.output.json_mode else sys.stdout
        print(self.tui.hello_text(), file=stream)
        print("Next: {0} help".format(Cli.CONSOLE_NAME), file=stream)
        return 0

    def _unknown_verb(self, token):
        names = ", ".join(Cli.PRODUCT_VERBS)
        return self.report_error(
            "Unknown verb '{0}'.".format(token),
            "{0} help — verbs: {1}".format(Cli.CONSOLE_NAME, names),
        )

    def _print_video_list(self):
        """Eligible names on the console. Does not join and does not draw the screen."""
        stream = sys.stderr if self.output.json_mode else sys.stdout
        print(self.tui._video_listing(), file=stream)
        return 0

    def _print_mp4_list(self, folder):
        """Numbered MP4 names. Does not encode."""
        folder_path = Path(folder)
        if not folder_path.is_dir():
            return self.report_error(
                "Not a directory: {0}".format(folder),
                "{0} list-mp4 --folder .".format(Cli.CONSOLE_NAME),
            )
        files = self.media.get_mp4_files(folder_path)
        if not files:
            return self.report_error(
                "No MP4 files found!",
                "{0} list-mp4 --folder .".format(Cli.CONSOLE_NAME),
            )
        lines = ["{0:2d}. {1}".format(i, item.name) for i, item in enumerate(files, 1)]
        stream = sys.stderr if self.output.json_mode else sys.stdout
        for line in lines:
            print(line, file=stream)
        return 0

    def _job_ready(self, args):
        return args.file is not None and args.start is not None and args.end is not None

    def _tail_from_args(self, args):
        """One tail. The caller rejects --boomerang together with --repeat."""
        if args.repeat:
            return Encoder.TAIL_REPEAT
        if args.boomerang:
            return Encoder.TAIL_BOOMERANG
        return Encoder.TAIL_NONE

    def _reject_both_tails(self, args):
        """Fail closed before encode when both tail flags are set."""
        if args.boomerang and args.repeat:
            return self.report_error(
                "Choose one tail: --boomerang or --repeat.",
                "{0} edit --file clip.mp4 --start 0 --end 5 --repeat".format(
                    Cli.CONSOLE_NAME
                ),
            )
        return None

    def _run_batch(self, args):
        percent = 100.0 if args.percent is None else args.percent
        return self.encoder.batch_session(
            args.file, args.start, args.end, percent, self._tail_from_args(args)
        )

    def _verb_edit(self, args):
        """One edit job, or the edit questions when a target is missing."""
        if self._job_ready(args):
            return self._run_batch(args)
        if not self.stdin_is_tty():
            return self.report_error(
                "Non-interactive job needs --file, --start, and --end.",
                "{0} edit --file clip.mp4 --start 0 --end 5".format(Cli.CONSOLE_NAME),
            )
        if self.output.json_mode:
            return self.edit._edit_json(args)
        if self.logger is not None:
            self.logger.quiet(True)
        return self.tui.open_direct("edit", args)

    def _verb_list_mp4(self, args):
        """List MP4 files and stop. Does not encode."""
        if args.folder is None and args.file is not None:
            args.folder = str(Path(args.file).parent)
        if not self.stdin_is_tty():
            return self._print_mp4_list("." if args.folder is None else args.folder)
        if self.output.json_mode:
            if args.folder is None:
                self.output.json_walk = True
                raw = self.edit._prompt_line("Folder (Enter = current):")
                if raw is None:
                    return 0
                args.folder = raw.strip() or "."
            return self._print_mp4_list(args.folder)
        if self.logger is not None:
            self.logger.quiet(True)
        return self.tui.open_direct("list-mp4", args)

    def _has_selectors(self, args):
        return (
            args.file is not None
            or args.start is not None
            or args.end is not None
            or args.folder is not None
        )

    def _dispatch(self, args):
        """One product verb, one edit job, the front board, or a fail-closed stop."""
        verb = args.verb
        json_mode = self.output.json_mode
        if args.force and verb != "self-uninstall":
            return self.report_error(
                "--force is only for self-uninstall.",
                "{0} self-uninstall --force".format(Cli.CONSOLE_NAME),
            )
        rejected = self._reject_both_tails(args)
        if rejected is not None:
            return rejected
        if verb == "about":
            if json_mode or not self.stdout_is_tty():
                return self._page(self.tui.about_text())
            result = self.tui.about_on_screen()
            if isinstance(result, int):
                return result
            return self._page(result)
        if verb == "hello":
            return self._verb_hello()
        if verb == "tui":
            if json_mode or not self.stdin_is_tty() or not self.stdout_is_tty():
                return self.report_error(
                    "No terminal for the text menu.",
                    "{0} tui".format(Cli.CONSOLE_NAME),
                )
            if self.logger is not None:
                self.logger.quiet(True)
            action = self.tui.open_text_menu()
            if action == "missing":
                return 1
            return 0
        if verb == "version":
            return self._page(self.self_manage.local_version())
        if verb == "self-uninstall":
            if not args.force:
                return self.report_error(
                    "self-uninstall removes this package with pip.",
                    "{0} self-uninstall --force".format(Cli.CONSOLE_NAME),
                )
            return self.self_manage.emit(verb, json_mode=json_mode)
        if verb in ("version-check", "self-update", "self-install"):
            return self.self_manage.emit(verb, json_mode=json_mode)
        if verb == "setup":
            return self.host_setup.run(
                window_lines=self.about.window_library_lines()
            )
        if verb == "join":
            if json_mode or not self.stdout_is_tty():
                return self.report_error(
                    "No terminal for join. Use a terminal.",
                    "{0} join".format(Cli.CONSOLE_NAME),
                )
            return self.tui.open_direct("join")
        if verb == "list-videos":
            if json_mode or not self.stdout_is_tty():
                return self._print_video_list()
            result = self.tui.list_on_screen()
            if isinstance(result, int):
                return result
            return self._page(result)
        if verb == "edit":
            return self._verb_edit(args)
        if verb == "list-mp4":
            return self._verb_list_mp4(args)
        if verb is not None:
            return self._unknown_verb(verb)

        selectors = self._has_selectors(args)
        if (args.percent is not None or args.boomerang or args.repeat) and not selectors:
            return self.report_error(
                "--percent, --boomerang, and --repeat need --file, --start, and --end.",
                "{0} edit --file clip.mp4 --start 0 --end 5".format(Cli.CONSOLE_NAME),
            )
        if selectors:
            if args.folder is not None and args.file is None:
                folder_path = Path(args.folder)
                if not folder_path.is_dir():
                    return self.report_error(
                        "Not a directory: {0}".format(args.folder),
                        "{0} list-mp4 --folder .".format(Cli.CONSOLE_NAME),
                    )
                files = self.media.get_mp4_files(folder_path)
                if not files:
                    return self.report_error(
                        "No MP4 files found!",
                        "{0} list-mp4 --folder .".format(Cli.CONSOLE_NAME),
                    )
                return self.report_error(
                    "--folder listed {0} MP4 file(s); also pass --file, --start, and --end.".format(
                        len(files)
                    ),
                    "{0} edit --file clip.mp4 --start 0 --end 5".format(Cli.CONSOLE_NAME),
                )
            if not self._job_ready(args):
                return self.report_error(
                    "Non-interactive job needs --file, --start, and --end.",
                    "{0} edit --file clip.mp4 --start 0 --end 5".format(Cli.CONSOLE_NAME),
                )
            return self._run_batch(args)
        if not self.stdout_is_tty():
            self.build_parser().print_help()
            return 0
        if self.logger is not None:
            self.logger.quiet(True)
        if Cli.opens_window([]):
            code = self.gui.open(self)
            if code != 0:
                return self.report_error(
                    self.gui.failure or "The window did not open.",
                    "{0} tui".format(Cli.CONSOLE_NAME),
                )
            return 0
        action = self.tui.open_text_menu()
        if action == "missing":
            return 1
        return 0

    def run(self, argv=None):
        """One job. def main already wrote ChronicleLogger(...) and passed it in."""
        self.output._json_reset()
        if argv is None:
            argv = sys.argv[1:]
        argv = list(argv)
        parser = self.build_parser()
        try:
            args = parser.parse_args(argv)
        except SystemExit as exc:
            code = exc.code
            if code is None or code == 0:
                return 0
            return int(code)
        if args.json:
            self.output.json_mode = True
        bare_json_help = (
            args.json
            and args.verb is None
            and not self._has_selectors(args)
            and args.percent is None
            and not args.boomerang
            and not args.repeat
        )
        if args.verb == "help" or bare_json_help:
            if args.json:
                parser.print_help(file=sys.stderr)
                code = self.output._emit_json("noninteractive", 0)
                self.output.json_mode = False
                return code
            parser.print_help()
            return 0
        code = self._dispatch(args)
        if not args.json:
            return code
        mode = "interactive" if self.output.json_walk else "noninteractive"
        code = self.output._emit_json(mode, code)
        self.output.json_mode = False
        return code


def main(argv=None, basedir="", logdir=""):
    """This function instantiates ChronicleLogger. The statement below is the construct."""
    if argv is None:
        argv = sys.argv[1:]
    argv = list(argv)
    from VideoTools import __version__

    HostSetup.ensure_geteuid()
    try:
        from ChronicleLogger import ChronicleLogger
    except ImportError:
        sys.stderr.write(
            'ChronicleLogger is required. Next step: python -m pip install "ChronicleLogger>=1.3.1"\n'
        )
        return 1

    screen = Cli.opens_text_screen(argv) or Cli.opens_window(argv)
    quiet = screen or ("--json" in argv)
    logger = ChronicleLogger(
        logname="VideoTools",
        is_quiet=quiet,
        basedir=basedir,
        logdir=logdir,
    )
    appname = logger.logName()
    resolved_base = logger.baseDir()
    logger.logDir()

    if logger.isDebug():
        logger.log_message(
            "{0} v{1} ({2})".format(appname, __version__, __file__),
            component="main",
        )
        logger.log_message(
            "Using {0}".format(ChronicleLogger.class_version()),
            component="main",
        )
        logger.log_message(
            "Base {0}".format(resolved_base),
            level="DEBUG",
            component="main",
        )
        logger.log_message("debug mode", component="main")

    app = Cli(logger)
    return app.run(argv)


if __name__ == "__main__":
    sys.exit(main())

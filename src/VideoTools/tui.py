# =============================================================================
# Text menu session for VideoTools.
# requirement-python-tui — menu region and the bottom input box.
# requirement-python-about — the about result page is framework_about.
# requirement-python-oop — this module defines class Tui and MenuScreenError.
# The frame is class MenuPainter. cli.py constructs Tui and calls it.
# =============================================================================
from __future__ import annotations

# requirement-runtime-prerequisites: try / except ImportError.
# Windows CPython ships the curses package without _curses. A missing
# module must not stop verbs that do not draw this screen.
try:
    import curses
except ImportError:
    curses = None

from .menu_painter import MenuPainter
from .menu_session import MenuSession
from .system_log import SystemLog



class MenuScreenError(Exception):
    """The terminal cannot hold the menu and the framed input box."""

    def __init__(self, message="", logger=None):
        super().__init__(message)
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="MenuScreenError")


class Tui:
    """Text menu session. Join questions and the front board stay on this screen.

    MenuModel, MenuSession, and MenuPainter live in their own modules.
    The rows are join, system-log, language, self-management, and Exit.
    """

    def __init__(self, app=None, app_name="VideoTools", version=None, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Tui")
        self.app = app
        self.app_name = app_name
        if version is None:
            from . import __version__
            version = __version__
        self.version = version
        self.painter = MenuPainter(logger=logger)
        self.system_log = SystemLog(logger=logger)

    def _name(self):
        if self.app is not None:
            return self.app.app_name
        return self.app_name

    def _ver(self):
        if self.app is not None:
            return self.app.version
        return self.version

    def front_lines(self):
        """General Purpose: Path line and the front board rows."""
        return [self.painter.path_line()] + self.painter.format_rows(
            self.painter.display_rows("front")
        )

    def self_lines(self):
        """General Purpose: Path line and the self-management board under 8."""
        return [self.painter.path_line()] + self.painter.format_rows(
            self.painter.display_rows("self")
        )

    def log_lines(self):
        """General Purpose: Path line and the system-log board under 3."""
        return [self.painter.path_line()] + self.painter.format_rows(
            self.painter.display_rows("log")
        )

    def language_lines(self):
        """General Purpose: Path line and the language board under 4."""
        return [self.painter.path_line()] + self.painter.format_rows(
            self.painter.display_rows("lang")
        )

    def help_on_screen(self):
        """
        General Purpose: Help text when help is typed on the open menu.
        The typed video-tools help verb does not call this and does not draw the screen.
        """
        dist = "VideoTools"
        if self.app is not None:
            dist = self.app.self_manage.DISTRIBUTION
        return (
            "help: usage for {0}.\n"
            "Verbs: help, version, about, hello, join, list-videos, edit, list-mp4, "
            "self-install, version-check, self-update, self-uninstall, setup.\n"
            "version shows the installed version and does not call pip.\n"
            "about shows the about page.\n"
            "join asks for two videos in this folder and an output name.\n"
            "list-videos lists eligible videos and does not join.\n"
            "edit asks for a folder, then one MP4, then cut, speed, and a tail.\n"
            "The tail is none, boomerang, or repeat. Empty means none.\n"
            "list-mp4 lists MP4 files and does not encode.\n"
            "version-check runs: python -m pip index versions {1}\n"
            "self-update runs: python -m pip install --upgrade {1}\n"
            "self-install runs: python -m pip install {1}\n"
            "self-uninstall runs: python -m pip uninstall -y {1}\n"
            "On the command line, self-uninstall also needs --force.\n"
            "setup installs the declared pip libraries for this Python.\n"
            "On Windows, setup also tries curses and ffmpeg.\n"
            "Empty arguments on a terminal open this menu and do not run pip."
            .format(self._name(), dist)
        )

    def hello_text(self):
        """General Purpose: The hello sentence. The typed verb prints this off the screen."""
        return "Hello from {0} {1}.".format(self._name(), self._ver())

    def about_text(self):
        """General Purpose: The about page body from AboutPage.framework_about."""
        if self.app is None:
            return ""
        return self.app.about.framework_about()

    def _visible_lines(self, lines, room, pin_last):
        """Lines that fit above the input box. A question pins its last line."""
        if room < 1:
            return []
        if len(lines) <= room:
            return list(lines)
        if not pin_last:
            return list(lines[-room:])
        if room == 1:
            return [lines[-1]]
        return list(lines[: room - 2]) + ["…", lines[-1]]

    def _paint_lines(self, screen, model, title, lines, pin_last):
        """Hand one question to MenuPainter. The session does not draw a second frame."""
        self.painter.paint_prompt(
            screen,
            model,
            title,
            lines,
            pin_last,
            self._name(),
            self._ver(),
            self._visible_lines,
        )

    def _arm_blocking(self, screen):
        """Clear the one-second clock wait. A no-key from that wait is not Esc."""
        arm = getattr(screen, "timeout", None)
        if arm is not None:
            arm(-1)

    def read_key(self, screen, model, lines, title="join"):
        """
        General Purpose: Read one line from the bottom input box.

        Returns the text, or None when the person presses Esc. The board's
        one-second clock wait is cleared before each key.
        """
        model.buffer = ""
        model.cursor = 0
        model.focus = "input"
        while True:
            self._paint_lines(screen, model, title, lines, pin_last=True)
            self._arm_blocking(screen)
            key = screen.getch()
            if key in (-1, 27):
                model.error = ""
                model.buffer = ""
                model.cursor = 0
                model.focus = "list"
                return None
            if key in (10, 13, curses.KEY_ENTER):
                text = model.buffer
                model.buffer = ""
                model.cursor = 0
                model.error = ""
                return text
            if key in (curses.KEY_BACKSPACE, 127, 8):
                model._backspace()
                model.error = ""
                continue
            if key in (curses.KEY_LEFT, curses.KEY_RIGHT) or key in model.edge_keys():
                model._slide(key)
                continue
            if key in (curses.KEY_UP, curses.KEY_DOWN):
                continue
            if 32 <= key < 127:
                model._insert(chr(key))
                model.error = ""
                continue

    def notice(self, screen, model, lines, title="result", closing=None):
        """General Purpose: Show lines until the next key. The clock wait is cleared."""
        model.buffer = ""
        model.cursor = 0
        model.focus = "list"
        model.error = ""
        if closing is None:
            closing = "Press a key to return to the main menu."
        body = list(lines) + ["", closing]
        self._paint_lines(screen, model, title, body, pin_last=True)
        self._arm_blocking(screen)
        try:
            screen.getch()
        except Exception:
            return

    def _read_yes_no(self, screen, model, lines, title="system-log"):
        """y/n from the box. Esc returns None. Empty is no."""
        while True:
            raw = self.read_key(screen, model, lines, title=title)
            if raw is None:
                return None
            raw = raw.strip().lower()
            if raw == "" or raw in ("n", "no"):
                return False
            if raw in ("y", "yes"):
                return True
            model.error = "Please enter y or n"

    def _read_index(self, screen, model, lines, count, title="join"):
        """1-based index from the box. Ask again on a bad value. Esc returns None."""
        while True:
            raw = self.read_key(screen, model, lines, title=title)
            if raw is None:
                return None
            raw = raw.strip()
            try:
                idx = int(raw)
            except ValueError:
                model.error = "Please type a number"
                continue
            if 1 <= idx <= count:
                return idx - 1
            model.error = "Enter 1–{0}".format(count)

    def _video_listing(self):
        """Eligible names in this folder. Does not join."""
        if self.app is None:
            return "No eligible videos in this folder."
        files = self.app.join.discover()
        if not files:
            return "No eligible videos in this folder."
        lines = ["Eligible videos:"]
        for index, item in enumerate(files, 1):
            lines.append("  {0:2d}. {1}".format(index, item.name))
        return "\n".join(lines)

    def list_on_screen(self, screen=None, model=None):
        """
        General Purpose: Show the eligible names. Does not join.
        With no screen, return the text. With a screen, wait for a key.
        """
        text = self._video_listing()
        if screen is not None and model is not None:
            self.notice(screen, model, text.splitlines(), title="list-videos")
            return 0
        if self.app is not None and self.app.stdout_is_tty():
            return self.open_direct("list-videos")
        return text

    def about_on_screen(self, screen=None, model=None):
        """
        General Purpose: Show the about page.
        With no screen, open the text screen when this is the direct verb.
        """
        text = self.about_text()
        if screen is not None and model is not None:
            self.notice(screen, model, text.splitlines() or [""], title="about")
            return 0
        if self.app is not None and self.app.stdout_is_tty():
            return self.open_direct("about")
        return text

    def _screen_error(self, too_small):
        if self.app is None:
            return "missing"
        if too_small:
            self.app.report_error(
                "The text screen is too small for the menu and the input box.",
                "{0} help".format(self.app.CONSOLE_NAME if hasattr(self.app, "CONSOLE_NAME") else "video-tools"),
            )
        else:
            self.app.report_error(
                "The text menu could not open on this terminal.",
                "{0} help".format(self.app.CONSOLE_NAME if hasattr(self.app, "CONSOLE_NAME") else "video-tools"),
            )
        return "missing"

    def _curses_missing(self):
        """The text menu cannot open because this Python has no curses module."""
        if self.app is None:
            return "missing"
        self.app.report_error(
            "The text menu needs the curses module. This Python does not provide it.",
            "{0} help".format(self.app.CONSOLE_NAME if hasattr(self.app, "CONSOLE_NAME") else "video-tools"),
        )
        return "missing"

    def _require_terminal(self):
        if self.app is None or not self.app.stdout_is_tty():
            if self.app is not None:
                self.app.report_error(
                    "No terminal for the text menu. Use a terminal.",
                    "{0} help".format(getattr(self.app, "CONSOLE_NAME", "video-tools")),
                )
            return False
        return True

    def open_text_menu(self):
        """
        General Purpose: Draw the front board. Does not start the join questions
        and does not run pip. Returns "missing" when the screen cannot open.
        """
        if not self._require_terminal():
            return "missing"
        try:
            import curses
        except ImportError:
            return self._curses_missing()

        screen_box = {}

        def on_kind(kind):
            if kind == "help":
                return self.help_on_screen()
            if kind == "hello":
                return self.hello_text() + "\nNext: video-tools help"
            if kind in ("version-check", "self-update", "self-install", "self-uninstall"):
                _code, text = self.app.self_manage.run_pip(kind)
                return text
            if kind == "list-videos":
                return self._video_listing()
            if kind == "list-mp4":
                screen = screen_box.get("screen")
                if screen is None:
                    return None
                self._list_in_tui(screen, session.model)
                return None
            if kind == "edit":
                screen = screen_box.get("screen")
                if screen is None:
                    return None
                self._edit_in_tui(screen, session.model)
                return None
            if kind == "view-log":
                screen = screen_box.get("screen")
                if screen is None:
                    return None
                return self._view_log(screen, session.model)
            if kind == "clear-log":
                screen = screen_box.get("screen")
                if screen is None:
                    return None
                return self._clear_log(screen, session.model)
            if kind == "log-folder":
                return self._log_folder()
            if kind != "join":
                return None
            screen = screen_box.get("screen")
            if screen is None:
                return None
            self.join_on_screen(screen, session.model, direct=False)
            return None

        session = MenuSession(
            self._name(),
            self._ver(),
            on_version=lambda: self.app.self_manage.local_version(),
            on_about=self.about_text,
            boards=None,
            on_kind=on_kind,
            logger=self.logger,
            painter=self.painter,
        )

        def _wrapped(screen):
            screen_box["screen"] = screen
            session.run(screen)

        try:
            curses.wrapper(_wrapped)
        except MenuScreenError:
            return self._screen_error(True)
        except Exception:
            return self._screen_error(False)
        return None

    def _tui_read(self, screen, model, lines, title="edit"):
        """Read one line from the bottom box. Esc returns None."""
        return self.read_key(screen, model, lines, title=title)

    def _tui_notice(self, screen, model, lines):
        """Show lines on the edit screen until the next key."""
        self.notice(screen, model, lines, title="edit")

    def _tui_float(self, screen, model, lines, default=None):
        """Read a float from the box. Empty uses default. Esc returns None."""
        while True:
            raw = self._tui_read(screen, model, lines)
            if raw is None:
                return None
            raw = raw.strip()
            if raw == "" and default is not None:
                return float(default)
            try:
                return float(raw.replace("%", ""))
            except ValueError:
                model.error = "Please enter a number"

    def _tui_yes_no(self, screen, model, lines, default_no=True, title="edit"):
        """y/n from the box. Empty uses the default. Esc returns None."""
        while True:
            raw = self._tui_read(screen, model, lines, title=title)
            if raw is None:
                return None
            raw = raw.strip().lower()
            if raw == "":
                return not default_no
            if raw in ("y", "yes"):
                return True
            if raw in ("n", "no"):
                return False
            model.error = "Please enter y or n"

    def _tui_tail(self, screen, model, lines, default="none", title="edit"):
        """none, boomerang, or repeat from the box. Empty uses default. Esc returns None."""
        while True:
            raw = self._tui_read(screen, model, lines, title=title)
            if raw is None:
                return None
            raw = raw.strip()
            chosen = self.app.encoder.normalize_tail(default if raw == "" else raw)
            if chosen is None:
                model.error = "Choose none, boomerang, or repeat"
                continue
            return chosen

    def _tui_index(self, screen, model, lines, count, title="edit"):
        """1-based index from the box. Esc returns None."""
        return self._read_index(screen, model, lines, count, title=title)

    def _tail_preset(self, args):
        """The tail a direct edit verb already named. None means the question defaults to none."""
        if args is None:
            return None
        if args.repeat:
            return self.app.encoder.TAIL_REPEAT
        if args.boomerang:
            return self.app.encoder.TAIL_BOOMERANG
        return None

    def _edit_in_tui(
        self,
        screen,
        model,
        folder=None,
        video=None,
        start_preset=None,
        end_preset=None,
        percent_preset=None,
        tail_preset=None,
    ):
        """Screen path of the edit questions. The order lives on EditWalk."""
        return self.app.edit.run_screen(
            self,
            screen,
            model,
            folder=folder,
            video=video,
            start_preset=start_preset,
            end_preset=end_preset,
            percent_preset=percent_preset,
            tail_preset=tail_preset,
        )

    def _list_in_tui(self, screen, model, folder=None):
        """Folder question, then the numbered MP4 list. No encode."""
        from pathlib import Path

        folder_path = Path(folder) if folder else None
        while True:
            if folder_path is None:
                raw = self._tui_read(
                    screen,
                    model,
                    [
                        "List MP4 files",
                        "Esc returns to the menu.",
                        "",
                        "Folder (Enter = current):",
                    ],
                )
                if raw is None:
                    return 0
                chosen = raw.strip() or "."
                folder_path = Path(chosen)
            if not folder_path.is_dir():
                model.error = "ERROR: Not a directory: {0}".format(folder_path)
                folder_path = None
                continue
            files = self.app.media.get_mp4_files(folder_path)
            if not files:
                self._tui_notice(screen, model, ["No MP4 files found!"])
                return 1
            listing = ["{0:2d}. {1}".format(i, item.name) for i, item in enumerate(files, 1)]
            self._tui_notice(screen, model, listing)
            return 0

    def open_direct(self, kind, args=None):
        """
        General Purpose: Open the text screen on join, list-videos, about, edit, or list-mp4.
        Does not start on the front board. Returns a process status.
        """
        if not self._require_terminal():
            return 1
        try:
            import curses
        except ImportError:
            self._curses_missing()
            return 1

        code_box = {"code": 0}
        session = MenuSession(
            self._name(),
            self._ver(),
            on_version=lambda: self.app.self_manage.local_version(),
            on_about=self.about_text,
            boards=None,
            on_kind=lambda _kind: None,
            logger=self.logger,
            painter=self.painter,
        )

        def _wrapped(screen):
            try:
                if kind == "join":
                    code_box["code"] = self.join_on_screen(
                        screen, session.model, direct=True
                    )
                elif kind == "list-videos":
                    code_box["code"] = self.list_on_screen(screen, session.model)
                elif kind == "edit":
                    self._edit_in_tui(
                        screen,
                        session.model,
                        folder=None if args is None else args.folder,
                        video=None if args is None else args.file,
                        start_preset=None if args is None else args.start,
                        end_preset=None if args is None else args.end,
                        percent_preset=None if args is None else args.percent,
                        tail_preset=self._tail_preset(args),
                    )
                elif kind == "list-mp4":
                    code_box["code"] = self._list_in_tui(
                        screen,
                        session.model,
                        None if args is None else args.folder,
                    )
                else:
                    code_box["code"] = self.about_on_screen(screen, session.model)
            except Exception as exc:
                self.notice(
                    screen, session.model, ["ERROR: {0}".format(exc)],
                    closing="Press a key to close.",
                )
                code_box["code"] = 1
            session.leave_to_front()
            # Esc and a finished page return to the front board.
            # A failed direct join keeps its non-zero status and does not wait there.
            if code_box["code"] == 0:
                session.run(screen)

        try:
            curses.wrapper(_wrapped)
        except MenuScreenError:
            self._screen_error(True)
            return 1
        except Exception:
            self._screen_error(False)
            return 1
        return code_box["code"]

    def _view_log(self, screen, model):
        """List log files and return the chosen file for the result page."""
        folder = self.system_log.log_dir()
        if not folder:
            return "No log folder."
        files = self.system_log.log_files()
        if not files:
            return "No log file in {0}.".format(folder)
        lines = ["Log files:"]
        for index, path in enumerate(files, start=1):
            lines.append("{0}. {1}".format(index, path.name))
        lines.append("")
        lines.append("Choose a log file:")
        picked = self._read_index(screen, model, lines, len(files), title="system-log")
        if picked is None:
            return None
        path = files[picked]
        body = self.system_log.read_log(path)
        if body is None:
            return "ERROR: {0} is not a log file in the log folder.".format(path.name)
        if body == "":
            body = "(empty)"
        return "{0}\n\n{1}".format(path.name, body)

    def _clear_log(self, screen, model):
        """List log files, confirm, and empty the chosen file."""
        folder = self.system_log.log_dir()
        if not folder:
            return "No log folder."
        files = self.system_log.log_files()
        if not files:
            return "No log file in {0}.".format(folder)
        lines = ["Log files:"]
        for index, path in enumerate(files, start=1):
            lines.append("{0}. {1}".format(index, path.name))
        lines.append("")
        lines.append("Choose a log file to clear:")
        picked = self._read_index(screen, model, lines, len(files), title="system-log")
        if picked is None:
            return None
        path = files[picked]
        answer = self._read_yes_no(
            screen,
            model,
            ["Clear {0}? (y/n)".format(path.name)],
            title="system-log",
        )
        if answer is not True:
            return None
        if not self.system_log.clear_log(path):
            return "ERROR: {0} is not a log file in the log folder.".format(path.name)
        return "Cleared {0}.".format(path.name)

    def _log_folder(self):
        """The log-folder result page. The path is logDir()."""
        return self.system_log.folder_text()

    def _numbered(self, files):
        lines = ["Found video files:"]
        for index, item in enumerate(files, 1):
            lines.append("  {0:2d}. {1}".format(index, item.name))
        lines.append("")
        return lines

    def join_on_screen(self, screen, model, direct=False):
        """
        General Purpose: Ask for two indexes and an output name in the bottom box.

        Current folder only. No folder question. Esc returns without joining.
        Fewer than two videos: a direct join returns non-zero; an open board
        stays open and shows the reason.
        """
        join = self.app.join
        blocked = join.block_reason()
        if blocked:
            if direct:
                self.notice(
                    screen, model, blocked, title="join",
                    closing="Press a key to close.",
                )
                return 1
            model.error = blocked[0]
            return 0

        files = join.discover()
        intro = ["Join two videos in this folder.", "Esc returns to the menu.", ""]
        first_lines = intro + self._numbered(files) + ["Choose FIRST video →"]
        first = self._read_index(screen, model, first_lines, len(files), title="join")
        if first is None:
            model.show_front()
            return 0
        vid1 = files[first]
        remaining = join.remaining_after(files, vid1)
        second_lines = intro + self._numbered(remaining) + ["Choose SECOND video →"]
        second = self._read_index(
            screen, model, second_lines, len(remaining), title="join"
        )
        if second is None:
            model.show_front()
            return 0
        vid2 = remaining[second]
        default_name = "{0} + {1}.mp4".format(vid1.stem, vid2.stem)
        name_lines = [
            "Joining:",
            "   {0}".format(vid1.name),
            " + {0}".format(vid2.name),
            "",
            "Output filename [{0}]:".format(default_name),
        ]
        raw = self.read_key(screen, model, name_lines, title="join")
        if raw is None:
            model.show_front()
            return 0
        out_path = join.resolve_output_name(vid1, vid2, raw)
        preview = [
            "Joining with perfect audio sync:",
            "   {0}".format(vid1.name),
            " + {0}".format(vid2.name),
            " → {0}".format(out_path),
            "   Staging dir → {0}".format(join.staging_dir_for(out_path)),
            "",
            "Running…",
        ]
        model.buffer = ""
        model.focus = "list"
        model.error = ""
        self._paint_lines(screen, model, "join", preview, pin_last=True)
        ok, result = join.run(vid1, vid2, out_path)
        closing = None
        if direct and not ok:
            closing = "Press a key to close."
        self.notice(
            screen, model, preview[:-1] + [""] + result, title="join", closing=closing,
        )
        model.show_front()
        if direct and not ok:
            return 1
        return 0

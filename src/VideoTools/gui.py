# =============================================================================
# X11 window for edit and join.
# requirement-python-gui — two groups, players, file buttons.
# requirement-python-oop — class Gui.
# The text menu stays on requirement-python-tui. This module does not draw it.
# =============================================================================
from __future__ import annotations

import os
import sys
import threading
import warnings
from pathlib import Path


class Gui:
    """The X11 window. Edit and Join share one area. One group is visible.

    Each group splits left and right. The left side is the source or sources
    and the settings. The right side is the output. Edit plays the source
    MP4 and the generated file. Join plays both sources and the generated
    file. Typed verbs and the text menu stay on Cli and Tui.
    """

    FRONT = (
        (1, "join", "join", "join"),
        (2, "edit", "edit", "edit"),
        (3, "system-log", "system-log", "log"),
        (4, "language", "language", "lang"),
        (8, "self-management", "self-management", "self"),
        (9, "exit", "Exit", ""),
    )
    SELF_ROWS = (
        (82, "version", "version"),
        (83, "about", "about"),
        (84, "version-check", "version-check"),
        (85, "self-update", "self-update"),
        (86, "self-uninstall", "self-uninstall"),
        (87, "self-install", "self-install"),
    )
    # Join: source 1, source 2, generated. Edit generated is separate.
    JOIN_PLAYER_KEYS = ("join-1", "join-2", "join-out")
    EDIT_GENERATED_KEY = "edit-out"

    def __init__(self, logger=None) -> None:
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Gui")
        self.failure = ""
        self.app = None
        self._gtk = None
        self._glib = None
        self._gio = None
        self._loop = None
        self._window = None
        self._stack = None
        self._media = None
        self._slots = {}
        self._busy = False
        self._user_move = False
        self._edit_path = ""
        self._join_paths = ["", ""]
        self._join_name_edited = False
        self._log_lock = threading.Lock()
        self._menu_buttons = []
        self._group_tabs = {}
        self._tab_guard = False
        self._window_copy = {}
        self._said = []
        self._log_state = None
        self.language = None

    @staticmethod
    def format_elapsed(seconds) -> str:
        """Elapsed time as MM:SS.CC. Minutes grow past 99. Not translated."""
        try:
            seconds = float(seconds)
        except (TypeError, ValueError):
            seconds = 0
        if seconds < 0:
            seconds = 0
        total_cs = int(seconds * 100 + 0.5)
        centi = total_cs % 100
        total_s = total_cs // 100
        secs = total_s % 60
        minutes = total_s // 60
        return "{0:02d}:{1:02d}.{2:02d}".format(minutes, secs, centi)

    @staticmethod
    def parse_elapsed(text):
        """Parse MM:SS.CC into seconds. None when the text is not that shape."""
        raw = (text or "").strip()
        if raw.count(":") != 1 or raw.count(".") != 1:
            return None
        minute_text, rest = raw.split(":", 1)
        second_text, centi_text = rest.split(".", 1)
        if not minute_text.isdigit() or not second_text.isdigit() or not centi_text.isdigit():
            return None
        if len(minute_text) < 2 or len(second_text) != 2 or len(centi_text) != 2:
            return None
        seconds = int(second_text)
        if seconds > 59:
            return None
        return int(minute_text) * 60 + seconds + int(centi_text) / 100.0

    def open(self, app) -> int:
        """General Purpose: Show the window. 0 on Exit. 1 when X11 refuses."""
        self.app = app
        self.failure = ""
        display = os.environ.get("DISPLAY", "").strip()
        if not display:
            self.failure = "No X11 display."
            return 1
        os.environ["GDK_BACKEND"] = "x11"
        try:
            gtk, glib, gio, gdk = self._load_toolkit()
        except Exception as exc:
            self.failure = "GTK 4 is not available ({0}).".format(exc)
            return 1
        self._gtk = gtk
        self._glib = glib
        self._gio = gio
        if gdk.Display.get_default() is None:
            opened = gdk.Display.open(display)
            if opened is None and gdk.Display.get_default() is None:
                self.failure = "X11 display {0} refused the connection.".format(display)
                return 1
        from .menu_language import MenuLanguage
        from .system_log import SystemLog

        self.language = MenuLanguage(logger=self.logger)
        self.logs = SystemLog(logger=self.logger)
        self._build()
        self._loop = glib.MainLoop()
        self._tick_id = glib.timeout_add(100, self._tick)
        self._window.present()
        self._loop.run()
        if self._tick_id:
            glib.source_remove(self._tick_id)
        return 0

    def _load_toolkit(self):
        """Import GTK 4 and GStreamer. The Debian gi path covers a pyenv interpreter."""
        dist = "/usr/lib/python3/dist-packages"
        if os.path.isdir(os.path.join(dist, "gi")) and dist not in sys.path:
            sys.path.append(dist)
        import gi

        gi.require_version("Gtk", "4.0")
        gi.require_version("Gdk", "4.0")
        gi.require_version("Gst", "1.0")
        from gi.repository import Gdk, Gio, GLib, Gst, Gtk

        Gst.init(None)
        return Gtk, GLib, Gio, Gdk

    def _log_status(self, message, level="INFO") -> None:
        """One lock around log_message. Released before a thread starts."""
        if self.logger is None:
            return
        with self._log_lock:
            self.logger.log_message(message, level=level, component="Gui")

    def _build(self) -> None:
        gtk = self._gtk
        title = "{0} {1}".format(self.app.app_name, self.app.version)
        self._window = gtk.Window(title=title)
        self._window.set_default_size(1280, 800)
        self._window.connect("close-request", self._on_close)
        header = gtk.HeaderBar()
        self._window.set_titlebar(header)
        self._install_group_style()
        menu = gtk.Box(orientation=gtk.Orientation.HORIZONTAL, spacing=4)
        self._group_tab_box = gtk.Box(orientation=gtk.Orientation.HORIZONTAL, spacing=4)
        self._group_tab_box.set_hexpand(True)
        self._menu_buttons = []
        self._group_tabs = {}
        for number, kind, english, page in self.FRONT:
            button = self._menu_button(number, kind, english, page)
            if page in ("join", "edit"):
                self._group_tab_box.append(button)
                self._group_tabs[page] = button
            else:
                menu.append(button)
            self._menu_buttons.append(button)
        header.pack_start(menu)
        root = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=8)
        root.set_margin_top(8)
        root.set_margin_bottom(8)
        root.set_margin_start(12)
        root.set_margin_end(12)
        self.path_label = gtk.Label(xalign=0)
        self._refresh_path()
        root.append(self.path_label)
        self._stack = gtk.Stack()
        self._stack.set_hexpand(True)
        self._stack.set_vexpand(True)
        self._stack.add_named(self._edit_group(), "edit")
        self._stack.add_named(self._join_group(), "join")
        self._stack.add_named(self._log_page(), "log")
        self._stack.add_named(self._language_page(), "lang")
        self._stack.add_named(self._self_page(), "self")
        self._group_frame = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=0)
        self._group_frame.set_hexpand(True)
        self._group_frame.set_vexpand(True)
        self._group_frame.add_css_class("video-group")
        self._group_frame.append(self._stack)
        face = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=0)
        face.set_hexpand(True)
        face.set_vexpand(True)
        face.append(self._group_tab_box)
        face.append(self._group_frame)
        root.append(face)
        self._window.set_child(root)
        self._show("edit")
        self._prepare_media()

    def _menu_button(self, number, kind, english, page):
        """One numbered menu control. Rows 1 and 2 are the group tabs."""
        gtk = self._gtk
        label = self._front_label(number, kind, english)
        if page in ("join", "edit"):
            button = gtk.ToggleButton(label=label)
            button.add_css_class("group-tab")
            button.connect("toggled", self._on_group_tab, page)
            return button
        button = gtk.Button(label=label)
        if page:
            button.connect("clicked", self._on_page, page)
        else:
            button.connect("clicked", self._on_exit)
        return button

    def _install_group_style(self) -> None:
        """Highlight for rows 1 and 2. The bar uses the same width as the group."""
        gtk = self._gtk
        css = (
            "button.group-tab {"
            " border-radius: 8px 8px 0 0;"
            " padding: 6px 18px;"
            " margin-top: 4px;"
            "}"
            "button.group-tab:checked {"
            " background-color: @theme_selected_bg_color;"
            " color: @theme_selected_fg_color;"
            "}"
            "box.video-group.group-open {"
            " border-top: 3px solid @theme_selected_bg_color;"
            "}"
        )
        display = self._window.get_display()
        if display is None:
            return
        provider = gtk.CssProvider()
        provider.load_from_string(css)
        gtk.StyleContext.add_provider_for_display(
            display,
            provider,
            gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def _on_group_tab(self, button, page: str) -> None:
        """Keep the highlighted row on the group that is showing."""
        if self._tab_guard:
            return
        if button.get_active():
            self._show(page)
            return
        if self._stack.get_visible_child_name() == page:
            self._tab_guard = True
            button.set_active(True)
            self._tab_guard = False

    def _mark_group_tab(self, page: str) -> None:
        """Highlight row 1 or row 2 only while that group is the visible one."""
        self._tab_guard = True
        try:
            for name, button in self._group_tabs.items():
                button.set_active(name == page)
            if page in ("join", "edit"):
                self._group_frame.add_css_class("group-open")
            else:
                self._group_frame.remove_css_class("group-open")
        finally:
            self._tab_guard = False

    def _front_label(self, _number, kind, english) -> str:
        """Top menu name. The text menu keeps the row number."""
        short = english
        if self.language is not None:
            short = self.language.row_short(kind, english)
        return short

    def _w(self, key: str) -> str:
        """One window string. A missing language object uses the English line."""
        language = self.language
        if language is None:
            from .menu_language import _WINDOW

            return _WINDOW["en"].get(key, "")
        return language.window(key)

    def _fill(self, key: str, *parts) -> str:
        """Fill {0}, {1}, … without interpreting other braces in the parts."""
        text = self._w(key)
        for index, part in enumerate(parts):
            text = text.replace("{" + str(index) + "}", str(part))
        return text

    def _track(self, key: str, widget):
        self._window_copy.setdefault(key, []).append(widget)
        return widget

    def _cap(self, key: str, xalign=None):
        gtk = self._gtk
        if xalign is None:
            label = gtk.Label(label=self._w(key))
        else:
            label = gtk.Label(label=self._w(key), xalign=xalign)
        return self._track(key, label)

    def _btn(self, key: str):
        button = self._gtk.Button(label=self._w(key))
        return self._track(key, button)

    def _check(self, key: str):
        button = self._gtk.CheckButton(label=self._w(key))
        return self._track(key, button)

    def _put(self, widget, text: str) -> None:
        name = widget.__class__.__name__
        if name in ("Button", "ToggleButton", "CheckButton"):
            widget.set_label(text)
            return
        if hasattr(widget, "set_text"):
            widget.set_text(text)
        if hasattr(widget, "set_label"):
            widget.set_label(text)

    def _say(self, widget, key: str, *parts) -> None:
        widget._vt_phrase = (key, parts)
        if widget not in self._said:
            self._said.append(widget)
        widget.set_text(self._fill(key, *parts))

    def _say_raw(self, widget, text: str) -> None:
        widget._vt_phrase = None
        widget.set_text(text)

    def _clear_note(self, widget) -> None:
        widget._vt_phrase = None
        widget.set_text("")

    def _apply_window_language(self) -> None:
        """Redraw window controls in the language this process already selected."""
        for key, widgets in self._window_copy.items():
            text = self._w(key)
            for widget in widgets:
                self._put(widget, text)
        for widget in self._said:
            phrase = getattr(widget, "_vt_phrase", None)
            if phrase:
                key, parts = phrase
                widget.set_text(self._fill(key, *parts))
        self._sync_edit()
        self._sync_join()
        self._refresh_path()
        self._paint_log_folder()
        self._paint_log_body()

    def _on_page(self, _button, page) -> None:
        self._show(page)

    def _on_exit(self, _button) -> None:
        self._window.close()

    def _on_close(self, _window) -> bool:
        if self._busy:
            self._set_visible_result("please wait for time consuming process")
            return True
        self._pause_all_players()
        if self._loop is not None:
            self._loop.quit()
        return False

    def _show(self, page: str) -> None:
        if page != "edit":
            self._pause_edit_players()
        if page != "join":
            self._pause_join_players()
        self._stack.set_visible_child_name(page)
        if page == "log":
            self._fill_logs()
        if page == "lang":
            self._fill_languages()
        self._mark_group_tab(page)
        self._refresh_path()

    def _refresh_path(self) -> None:
        word = "Path"
        if self.language is not None:
            word = self.language.path_label()
        self.path_label.set_text("{0}: {1}".format(word, os.path.abspath(os.getcwd())))

    def _group(self):
        """One video group: sources on the left, output on the right."""
        gtk = self._gtk
        group = gtk.Paned(orientation=gtk.Orientation.HORIZONTAL)
        group.set_hexpand(True)
        group.set_vexpand(True)
        group.set_wide_handle(True)
        left = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
        left.set_margin_top(4)
        left.set_margin_bottom(4)
        left.set_margin_start(4)
        left.set_margin_end(8)
        right = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
        right.set_margin_top(4)
        right.set_margin_bottom(4)
        right.set_margin_start(8)
        right.set_margin_end(4)
        group.set_start_child(self._scroll(left))
        group.set_end_child(self._scroll(right))
        group.set_resize_start_child(True)
        group.set_resize_end_child(True)
        group.set_shrink_start_child(True)
        group.set_shrink_end_child(True)
        group.set_position(620)
        return group, left, right

    def _scroll(self, child):
        """Scroll one side of a group. The child keeps its own height."""
        gtk = self._gtk
        scroll = gtk.ScrolledWindow()
        scroll.set_hexpand(True)
        scroll.set_vexpand(True)
        scroll.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.AUTOMATIC)
        scroll.set_child(child)
        return scroll

    def _edit_group(self):
        gtk = self._gtk
        group, left, right = self._group()
        source = gtk.Box(orientation=gtk.Orientation.HORIZONTAL, spacing=6)
        source.append(self._cap("win_mp4"))
        self.edit_file = gtk.Entry()
        self.edit_file.set_editable(False)
        self.edit_file.set_hexpand(True)
        source.append(self.edit_file)
        pick = self._btn("win_select_file")
        pick.connect("clicked", self._pick_edit)
        source.append(pick)
        left.append(source)
        self.video_holder = gtk.Box(orientation=gtk.Orientation.VERTICAL)
        self.video_holder.set_hexpand(True)
        self.video_holder.set_vexpand(True)
        self.video_note = gtk.Label(label="")
        self.video_holder.append(self.video_note)
        left.append(self.video_holder)
        bar = gtk.Box(orientation=gtk.Orientation.HORIZONTAL, spacing=8)
        self.elapsed = gtk.Label(label="00:00.00")
        self.elapsed.set_width_chars(9)
        self.scale = gtk.Scale.new_with_range(gtk.Orientation.HORIZONTAL, 0, 1, 0.01)
        self.scale.set_draw_value(False)
        self.scale.set_hexpand(True)
        self.scale.connect("change-value", self._on_seek)
        self.total = gtk.Label(label="00:00.00")
        self.total.set_width_chars(9)
        bar.append(self.elapsed)
        bar.append(self.scale)
        bar.append(self.total)
        left.append(bar)
        transport = gtk.Box(orientation=gtk.Orientation.HORIZONTAL, spacing=6)
        for key, handler in (
            ("win_start", self._play),
            ("win_pause", self._pause),
            ("win_stop", self._stop),
        ):
            button = self._btn(key)
            button.connect("clicked", handler)
            transport.append(button)
        self.jump_entry = gtk.Entry()
        self.jump_entry.set_placeholder_text("00:00.00")
        self.jump_entry.set_width_chars(10)
        jump = self._btn("win_go")
        jump.connect("clicked", self._jump)
        transport.append(self.jump_entry)
        transport.append(jump)
        left.append(transport)
        marks = gtk.Box(orientation=gtk.Orientation.HORIZONTAL, spacing=6)
        mark_start = self._btn("win_mark_start")
        mark_end = self._btn("win_mark_end")
        mark_start.connect("clicked", self._mark, "start")
        mark_end.connect("clicked", self._mark, "end")
        marks.append(mark_start)
        marks.append(mark_end)
        left.append(marks)
        bounds = gtk.Box(orientation=gtk.Orientation.HORIZONTAL, spacing=8)
        bounds.append(self._cap("win_from"))
        self.edit_start = gtk.Entry()
        self.edit_start.set_width_chars(10)
        self.edit_start.set_text("00:00.00")
        self.edit_start.connect("changed", self._sync_edit)
        bounds.append(self.edit_start)
        bounds.append(self._cap("win_end"))
        self.edit_end = gtk.Entry()
        self.edit_end.set_width_chars(10)
        self.edit_end.set_text("00:00.00")
        self.edit_end.connect("changed", self._sync_edit)
        bounds.append(self.edit_end)
        options = gtk.Box(orientation=gtk.Orientation.HORIZONTAL, spacing=8)
        options.append(self._cap("win_percent"))
        self.percent = gtk.SpinButton.new_with_range(20, 200, 1)
        self.percent.set_value(100)
        self.percent.connect("value-changed", self._sync_edit)
        options.append(self.percent)
        tail = gtk.Box(orientation=gtk.Orientation.HORIZONTAL, spacing=8)
        tail.append(self._cap("win_tail"))
        self.tail_none = self._check("win_none")
        self.tail_boomerang = self._check("win_boomerang")
        self.tail_repeat = self._check("win_repeat")
        self.tail_boomerang.set_group(self.tail_none)
        self.tail_repeat.set_group(self.tail_none)
        self.tail_none.set_active(True)
        for button in (self.tail_none, self.tail_boomerang, self.tail_repeat):
            button.connect("toggled", self._sync_edit)
            tail.append(button)
        form = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
        form.append(bounds)
        form.append(options)
        form.append(tail)
        left.append(form)
        self.edit_output = gtk.Label(xalign=0)
        self.edit_output.set_wrap(True)
        self.edit_output.set_hexpand(True)
        right.append(self.edit_output)
        self.edit_run = self._btn("win_run")
        self.edit_run.connect("clicked", self._run_edit)
        right.append(self.edit_run)
        self.edit_result = gtk.Label(xalign=0)
        self.edit_result.set_wrap(True)
        self.edit_result.set_hexpand(True)
        right.append(self.edit_result)
        self._mount_player(right, self.EDIT_GENERATED_KEY, "win_generated")
        self._sync_edit()
        return group

    def _join_group(self):
        gtk = self._gtk
        group, left, right = self._group()
        self.join_entries = []
        sources = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=12)
        sources.set_homogeneous(True)
        sources.set_vexpand(True)
        for index, title in ((0, "win_video_1"), (1, "win_video_2")):
            column = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
            column.set_vexpand(True)
            column.set_hexpand(True)
            row = gtk.Box(orientation=gtk.Orientation.HORIZONTAL, spacing=6)
            row.append(self._cap(title))
            entry = gtk.Entry()
            entry.set_editable(False)
            entry.set_hexpand(True)
            row.append(entry)
            button = self._btn("win_select_file")
            button.connect("clicked", self._pick_join, index)
            row.append(button)
            column.append(row)
            self._mount_player(column, self.JOIN_PLAYER_KEYS[index])
            sources.append(column)
            self.join_entries.append(entry)
        left.append(sources)
        name_row = gtk.Box(orientation=gtk.Orientation.HORIZONTAL, spacing=6)
        name_row.append(self._cap("win_output_name"))
        self.join_name = gtk.Entry()
        self.join_name.set_hexpand(True)
        self.join_name.connect("changed", self._on_join_name)
        name_row.append(self.join_name)
        right.append(name_row)
        self.join_output = gtk.Label(xalign=0)
        self.join_output.set_wrap(True)
        self.join_output.set_hexpand(True)
        right.append(self.join_output)
        self.join_run = self._btn("win_run")
        self.join_run.connect("clicked", self._run_join)
        right.append(self.join_run)
        self.join_result = gtk.Label(xalign=0)
        self.join_result.set_wrap(True)
        self.join_result.set_hexpand(True)
        right.append(self.join_result)
        self._mount_player(right, self.JOIN_PLAYER_KEYS[2], "win_generated")
        self._sync_join()
        return group

    def _log_page(self):
        gtk = self._gtk
        page = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
        self.log_folder = gtk.Label(xalign=0)
        page.append(self.log_folder)
        self.log_list = gtk.ListBox()
        self.log_list.set_vexpand(True)
        scroll = gtk.ScrolledWindow()
        scroll.set_child(self.log_list)
        scroll.set_vexpand(True)
        scroll.set_min_content_height(160)
        page.append(scroll)
        actions = gtk.Box(orientation=gtk.Orientation.HORIZONTAL, spacing=6)
        view = self._btn("win_view")
        clear = self._btn("win_clear")
        view.connect("clicked", self._view_log)
        clear.connect("clicked", self._clear_log)
        actions.append(view)
        actions.append(clear)
        page.append(actions)
        self.log_text = gtk.TextView()
        self.log_text.set_editable(False)
        self.log_text.set_wrap_mode(gtk.WrapMode.WORD_CHAR)
        text_scroll = gtk.ScrolledWindow()
        text_scroll.set_child(self.log_text)
        text_scroll.set_vexpand(True)
        text_scroll.set_min_content_height(160)
        page.append(text_scroll)
        return page

    def _language_page(self):
        gtk = self._gtk
        page = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=4)
        self.lang_box = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=4)
        self.lang_notice = gtk.Label(xalign=0)
        page.append(self.lang_notice)
        page.append(self.lang_box)
        return page

    def _self_page(self):
        gtk = self._gtk
        page = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
        row = gtk.Box(orientation=gtk.Orientation.HORIZONTAL, spacing=6)
        for number, kind, english in self.SELF_ROWS:
            button = gtk.Button(label="{0} {1}".format(number, english))
            button.connect("clicked", self._self_action, kind)
            row.append(button)
        page.append(row)
        self.self_text = gtk.TextView()
        self.self_text.set_editable(False)
        self.self_text.set_wrap_mode(gtk.WrapMode.WORD_CHAR)
        scroll = gtk.ScrolledWindow()
        scroll.set_child(self.self_text)
        scroll.set_vexpand(True)
        page.append(scroll)
        return page

    def _mount_player(self, parent, key: str, heading: str = "") -> None:
        """Elapsed time bar plus Play and Stop. The picture is attached later."""
        gtk = self._gtk
        block = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=4)
        block.set_hexpand(True)
        block.set_vexpand(True)
        if heading:
            block.append(self._cap(heading, xalign=0))
        holder = gtk.Box(orientation=gtk.Orientation.VERTICAL)
        holder.set_vexpand(True)
        note = gtk.Label(label="")
        note.set_wrap(True)
        holder.append(note)
        block.append(holder)
        bar = gtk.Box(orientation=gtk.Orientation.HORIZONTAL, spacing=8)
        elapsed = gtk.Label(label="00:00.00")
        elapsed.set_width_chars(9)
        elapsed.set_xalign(1)
        scale = gtk.Scale.new_with_range(gtk.Orientation.HORIZONTAL, 0, 1, 0.01)
        scale.set_draw_value(False)
        scale.set_hexpand(True)
        scale.connect("change-value", self._on_slot_seek, key)
        total = gtk.Label(label="00:00.00")
        total.set_width_chars(9)
        total.set_xalign(0)
        bar.append(elapsed)
        bar.append(scale)
        bar.append(total)
        block.append(bar)
        transport = gtk.Box(orientation=gtk.Orientation.HORIZONTAL, spacing=6)
        play = self._btn("win_play")
        stop = self._btn("win_stop")
        play.connect("clicked", self._on_slot_play, key)
        stop.connect("clicked", self._on_slot_stop, key)
        transport.append(play)
        transport.append(stop)
        block.append(transport)
        parent.append(block)
        self._slots[key] = {
            "holder": holder,
            "note": note,
            "elapsed": elapsed,
            "scale": scale,
            "total": total,
            "play": play,
            "stop": stop,
            "media": None,
            "user_move": False,
            "path": "",
        }
        self._arm_slot(key)

    def _prepare_media(self) -> None:
        self._attach_source()
        for key in self.JOIN_PLAYER_KEYS:
            self._attach_slot(key)
        self._attach_slot(self.EDIT_GENERATED_KEY)

    def _attach_source(self) -> None:
        gtk = self._gtk
        try:
            self._media = gtk.MediaFile.new()
            video = gtk.Video()
            video.set_media_stream(self._media)
            video.set_autoplay(False)
            video.set_hexpand(True)
            video.set_vexpand(True)
            video.set_size_request(480, 200)
            self.video_holder.append(video)
            self._clear_note(self.video_note)
        except Exception as exc:
            self._media = None
            self._say(self.video_note, "win_playback", exc)

    def _attach_slot(self, key: str) -> None:
        slot = self._slots.get(key)
        if slot is None:
            return
        gtk = self._gtk
        try:
            media = gtk.MediaFile.new()
            video = gtk.Video()
            video.set_media_stream(media)
            video.set_autoplay(False)
            video.set_hexpand(True)
            video.set_vexpand(True)
            video.set_size_request(420, 180)
            slot["holder"].append(video)
            self._clear_note(slot["note"])
            slot["media"] = media
        except Exception as exc:
            slot["media"] = None
            self._say(slot["note"], "win_playback", exc)
        self._arm_slot(key)

    def _arm_slot(self, key: str) -> None:
        slot = self._slots.get(key)
        if slot is None:
            return
        ready = slot["media"] is not None and bool(slot["path"])
        slot["play"].set_sensitive(ready)
        slot["stop"].set_sensitive(ready)
        slot["scale"].set_sensitive(ready)

    def _reset_generated(self, key: str) -> None:
        """Clear one generated player and disable its controls before a run."""
        self._load_slot(key, "")

    @staticmethod
    def playback_path(ok, path) -> str:
        """Path for a generated player. Empty unless the job succeeded and the file is there."""
        if not ok:
            return ""
        text = str(path or "").strip()
        if not text or not os.path.isfile(text):
            return ""
        return text

    def _unload_media(self, media) -> None:
        try:
            media.pause()
        except Exception as exc:
            self._log_status("player pause failed ({0})".format(exc), level="WARNING")
            return
        clear = getattr(media, "clear", None)
        if clear is None:
            return
        try:
            clear()
        except Exception as exc:
            self._log_status("player clear failed ({0})".format(exc), level="WARNING")

    def _load_slot(self, key: str, path: str) -> None:
        slot = self._slots.get(key)
        if slot is None:
            return
        chosen = path if path and os.path.isfile(path) else ""
        slot["path"] = chosen
        slot["user_move"] = False
        slot["elapsed"].set_text("00:00.00")
        slot["scale"].set_range(0, 1)
        slot["scale"].set_value(0)
        slot["total"].set_text("00:00.00")
        media = slot["media"]
        if media is None:
            self._arm_slot(key)
            return
        if not chosen:
            self._unload_media(media)
            self._clear_note(slot["note"])
            self._arm_slot(key)
            return
        try:
            # Clear first so a second Run of the same path reloads the new bytes.
            self._unload_media(media)
            media.set_file(self._gio.File.new_for_path(chosen))
            media.seek(0)
        except Exception as exc:
            slot["path"] = ""
            self._say(slot["note"], "win_playback", exc)
            self._unload_media(media)
            self._arm_slot(key)
            return
        self._clear_note(slot["note"])
        duration = 0
        media_info = getattr(self.app, "media", None) if self.app is not None else None
        if media_info is not None:
            duration = media_info.get_duration_cv2(Path(chosen))
        if duration > 0:
            slot["total"].set_text(self.format_elapsed(duration))
            slot["scale"].set_range(0, duration)
        self._arm_slot(key)

    def _pause_slot(self, key: str) -> None:
        slot = self._slots.get(key)
        if slot is None or slot.get("media") is None:
            return
        try:
            slot["media"].pause()
        except Exception as exc:
            self._log_status("player pause failed ({0})".format(exc), level="WARNING")

    def _pause_edit_players(self) -> None:
        if self._media is not None:
            try:
                self._media.pause()
            except Exception as exc:
                self._log_status("player pause failed ({0})".format(exc), level="WARNING")
        self._pause_slot(self.EDIT_GENERATED_KEY)

    def _pause_join_players(self) -> None:
        for key in self.JOIN_PLAYER_KEYS:
            self._pause_slot(key)

    def _pause_all_players(self) -> None:
        self._pause_edit_players()
        self._pause_join_players()

    def _on_slot_seek(self, _scale, _scroll, value, key) -> bool:
        slot = self._slots.get(key)
        if slot is None:
            return False
        slot["user_move"] = True
        try:
            seconds = max(0.0, float(value))
            media = slot["media"]
            if media is not None and slot["path"]:
                media.seek(int(seconds * 1000000))
            slot["elapsed"].set_text(self.format_elapsed(seconds))
        finally:
            slot["user_move"] = False
        return False

    def _on_slot_play(self, _button, key) -> None:
        slot = self._slots.get(key)
        if slot is None or slot.get("media") is None or not slot["path"]:
            return
        try:
            slot["media"].play()
        except Exception as exc:
            self._say(slot["note"], "win_playback", exc)

    def _on_slot_stop(self, _button, key) -> None:
        """Return this player to the start. Does not stop an encode."""
        slot = self._slots.get(key)
        if slot is None or slot.get("media") is None or not slot["path"]:
            return
        try:
            slot["media"].pause()
            slot["media"].seek(0)
        except Exception as exc:
            self._say(slot["note"], "win_playback", exc)
            return
        slot["elapsed"].set_text("00:00.00")
        slot["scale"].set_value(0)

    def _tick_slot(self, key: str) -> None:
        slot = self._slots.get(key)
        if slot is None or slot.get("media") is None or slot["user_move"] or not slot["path"]:
            return
        media = slot["media"]
        stamp = media.get_timestamp()
        if stamp is None or stamp < 0:
            stamp = 0
        seconds = stamp / 1000000.0
        slot["elapsed"].set_text(self.format_elapsed(seconds))
        duration = media.get_duration()
        if duration and 0 < duration < 10**16:
            slot["scale"].set_range(0, duration / 1000000.0)
            slot["scale"].set_value(seconds)
            slot["total"].set_text(self.format_elapsed(duration / 1000000.0))

    def _pick_edit(self, _button) -> None:
        self._pick_file(self._w("win_select_mp4"), (".mp4",), self._set_edit_file)

    def _pick_join(self, _button, index) -> None:
        allowed = tuple(sorted(self.app.join.video_suffixes))
        self._pick_file(self._w("win_select_video"), allowed, lambda path: self._set_join_file(index, path))

    def _pick_file(self, title, suffixes, on_path) -> None:
        gtk = self._gtk
        # FileChooserDialog lists this host. A portal dialog would list the
        # ssh -X client, and the remote FFmpeg would miss that path.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            dialog = gtk.FileChooserDialog(title=title, action=gtk.FileChooserAction.OPEN)
        dialog.set_transient_for(self._window)
        dialog.set_modal(True)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            dialog.add_button(self._w("win_cancel"), gtk.ResponseType.CANCEL)
            dialog.add_button(self._w("win_open"), gtk.ResponseType.ACCEPT)
        filt = gtk.FileFilter()
        filt.set_name(self._w("win_video"))
        for suffix in suffixes:
            filt.add_suffix(suffix.lstrip(".").lower())
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            dialog.add_filter(filt)
            try:
                dialog.set_current_folder(self._gio.File.new_for_path(os.getcwd()))
            except (TypeError, AttributeError):
                pass

        def on_response(dlg, response):
            path = ""
            if response == gtk.ResponseType.ACCEPT:
                chosen = dlg.get_file()
                if chosen is not None:
                    path = chosen.get_path() or ""
            dlg.destroy()
            if path:
                on_path(path)

        dialog.connect("response", on_response)
        dialog.present()

    def _set_edit_file(self, path: str) -> None:
        if Path(path).suffix.lower() != ".mp4":
            self._say(self.edit_result, "win_edit_mp4")
            return
        self._edit_path = path
        self.edit_file.set_text(path)
        if self._media is not None:
            self._media.pause()
            self._media.set_file(self._gio.File.new_for_path(path))
            self._media.seek(0)
        duration = 0
        if self.app is not None:
            duration = self.app.media.get_duration_cv2(Path(path))
        if duration > 0:
            self.total.set_text(self.format_elapsed(duration))
            self.scale.set_range(0, duration)
        self.elapsed.set_text("00:00.00")
        self.edit_start.set_text("00:00.00")
        self.edit_end.set_text(self.format_elapsed(duration) if duration > 0 else "00:00.00")
        self._load_slot(self.EDIT_GENERATED_KEY, "")
        self._sync_edit()

    def _set_join_file(self, index: int, path: str) -> None:
        suffix = Path(path).suffix.lower()
        if suffix not in self.app.join.video_suffixes:
            self._say(self.join_result, "win_not_join")
            return
        other = self._join_paths[1 - index]
        try:
            same = bool(other) and Path(path).resolve() == Path(other).resolve()
        except OSError:
            same = os.path.abspath(path) == os.path.abspath(other)
        if same:
            self._say(self.join_result, "win_two_files")
            return
        self._join_paths[index] = path
        self.join_entries[index].set_text(path)
        if self._join_paths[0] and self._join_paths[1] and not self._join_name_edited:
            named = self.app.join.resolve_output_name(
                self._join_paths[0], self._join_paths[1], ""
            )
            self._filling_name = True
            self.join_name.set_text(named.name)
            self._filling_name = False
        self._load_slot(self.JOIN_PLAYER_KEYS[index], path)
        self._sync_join()

    def _on_join_name(self, _entry) -> None:
        if not getattr(self, "_filling_name", False) and self._join_paths[0] and self._join_paths[1]:
            self._join_name_edited = True
        self._sync_join()

    def _position_seconds(self) -> float:
        if self._media is None:
            return float(self.scale.get_value())
        stamp = self._media.get_timestamp()
        if stamp is None or stamp < 0:
            return float(self.scale.get_value())
        return stamp / 1000000.0

    def _tick(self) -> bool:
        if self._media is not None and not self._user_move:
            stamp = self._media.get_timestamp()
            if stamp is None or stamp < 0:
                stamp = 0
            seconds = stamp / 1000000.0
            self.elapsed.set_text(self.format_elapsed(seconds))
            duration = self._media.get_duration()
            if duration and 0 < duration < 10**16:
                self.scale.set_range(0, duration / 1000000.0)
                self.scale.set_value(seconds)
                self.total.set_text(self.format_elapsed(duration / 1000000.0))
        for key in self.JOIN_PLAYER_KEYS:
            self._tick_one(key)
        self._tick_one(self.EDIT_GENERATED_KEY)
        return True

    def _tick_one(self, key: str) -> None:
        try:
            self._tick_slot(key)
        except Exception as exc:
            self._log_status("player clock failed ({0})".format(exc), level="WARNING")

    def _on_seek(self, _scale, _scroll, value) -> bool:
        self._user_move = True
        try:
            seconds = max(0.0, float(value))
            if self._media is not None:
                self._media.seek(int(seconds * 1000000))
            self.elapsed.set_text(self.format_elapsed(seconds))
        finally:
            self._user_move = False
        return False

    def _play(self, _button) -> None:
        if self._media is not None:
            self._media.play()

    def _pause(self, _button) -> None:
        if self._media is not None:
            self._media.pause()

    def _stop(self, _button) -> None:
        if self._media is None:
            return
        self._media.pause()
        self._media.seek(0)
        self.elapsed.set_text("00:00.00")
        self.scale.set_value(0)

    def _jump(self, _button) -> None:
        seconds = self.parse_elapsed(self.jump_entry.get_text())
        if seconds is None:
            self._say(self.edit_result, "win_jump_format")
            return
        duration = 0
        if self._media is not None:
            raw = self._media.get_duration()
            if raw and raw > 0:
                duration = raw / 1000000.0
        if duration and seconds > duration:
            self._say(self.edit_result, "win_jump_past")
            return
        if self._media is not None:
            self._media.seek(int(seconds * 1000000))
        self.scale.set_value(seconds)
        self.elapsed.set_text(self.format_elapsed(seconds))

    def _mark(self, _button, which: str) -> None:
        text = self.format_elapsed(self._position_seconds())
        if which == "start":
            self.edit_start.set_text(text)
        else:
            self.edit_end.set_text(text)

    def _tail_effect(self) -> str:
        """The one edit tail. None, boomerang, and repeat are exclusive."""
        if self.tail_boomerang.get_active():
            return "boomerang"
        if self.tail_repeat.get_active():
            return "repeat"
        return "none"

    def _sync_edit(self, *_args) -> None:
        start = self.parse_elapsed(self.edit_start.get_text())
        end = self.parse_elapsed(self.edit_end.get_text())
        ready = (
            not self._busy
            and bool(self._edit_path)
            and start is not None
            and end is not None
            and start < end
        )
        self.edit_run.set_sensitive(ready)
        if self._edit_path and start is not None and end is not None:
            path = self.app.encoder.build_output_name(
                Path(self._edit_path),
                start,
                end,
                self.percent.get_value(),
                self._tail_effect(),
            )
            self._say(self.edit_output, "win_output_path", path)
        else:
            self._say(self.edit_output, "win_output")

    def _join_destination(self):
        first = self._join_paths[0] or "a.mp4"
        second = self._join_paths[1] or "b.mp4"
        named = self.app.join.resolve_output_name(first, second, self.join_name.get_text())
        if named.is_absolute():
            return named
        return Path.cwd() / named

    def _sync_join(self, *_args) -> None:
        both = bool(self._join_paths[0] and self._join_paths[1])
        self.join_run.set_sensitive(both and not self._busy)
        if both:
            self._say(self.join_output, "win_write_to", self._join_destination())
        else:
            self._say(self.join_output, "win_write_folder")

    def _set_visible_result(self, text: str) -> None:
        page = self._stack.get_visible_child_name()
        widget = self.join_result if page == "join" else self.edit_result
        self._say_raw(widget, text)

    def _run_edit(self, _button) -> None:
        if self._busy or not self._edit_path:
            return
        start = self.parse_elapsed(self.edit_start.get_text())
        end = self.parse_elapsed(self.edit_end.get_text())
        percent = float(self.percent.get_value())
        tail = self._tail_effect()
        if start is None or end is None or not (start < end):
            self._say(self.edit_result, "win_need_bounds")
            return
        if not self.app.encoder.valid_percent(percent):
            self._say(self.edit_result, "win_percent_range")
            return
        duration = self.app.media.get_duration_cv2(Path(self._edit_path))
        if duration <= 0:
            self._say(self.edit_result, "win_no_duration", Path(self._edit_path).name)
            return
        if end > duration + 0.001:
            self._say(self.edit_result, "win_end_past", self.format_elapsed(duration))
            return
        self._pause_all_players()
        self._reset_generated(self.EDIT_GENERATED_KEY)
        path = self._edit_path
        self._busy = True
        self._sync_edit()
        self._sync_join()
        self._say_raw(self.edit_result, "please wait for time consuming process")
        self._start_thread(
            "edit-encode",
            lambda: self._edit_worker(path, start, end, percent, tail),
        )

    def _edit_worker(self, path, start, end, percent, tail) -> None:
        code = self.app.encoder.batch_session(path, start, end, percent, tail)
        final = self.app.encoder.build_output_name(
            Path(path), start, end, percent, tail
        )
        ready = self.playback_path(code == 0, final)
        self._glib.idle_add(self._edit_done, code, str(final), ready)

    def _edit_done(self, code, final: str, ready: str) -> bool:
        self._busy = False
        if code == 0:
            self._say(self.edit_result, "win_edit_ok", final)
        else:
            self._say(self.edit_result, "win_edit_failed")
        self._load_slot(self.EDIT_GENERATED_KEY, ready)
        self._sync_edit()
        self._sync_join()
        return False

    def _run_join(self, _button) -> None:
        if self._busy:
            return
        first = self._join_paths[0]
        second = self._join_paths[1]
        if not first or not second:
            return
        try:
            same = Path(first).resolve() == Path(second).resolve()
        except OSError:
            same = os.path.abspath(first) == os.path.abspath(second)
        if same:
            self._say(self.join_result, "win_two_files")
            return
        destination = self._join_destination()
        self._pause_all_players()
        self._reset_generated(self.JOIN_PLAYER_KEYS[2])
        self._busy = True
        self._sync_edit()
        self._sync_join()
        self._say_raw(self.join_result, "please wait for time consuming process")
        self._start_thread(
            "join-encode",
            lambda: self._join_worker(first, second, destination),
        )

    def _join_worker(self, first, second, destination) -> None:
        ok, lines = self.app.join.run(first, second, destination)
        ready = self.playback_path(ok, destination)
        self._glib.idle_add(self._join_done, ok, list(lines), ready)

    def _join_done(self, ok, lines, ready: str) -> bool:
        self._busy = False
        if lines:
            self._say_raw(self.join_result, "\n".join(lines))
        elif ok:
            self._say(self.join_result, "win_join_ok")
        else:
            self._say(self.join_result, "win_join_failed")
        self._load_slot(self.JOIN_PLAYER_KEYS[2], ready)
        self._sync_edit()
        self._sync_join()
        return False

    def _start_thread(self, name: str, target) -> None:
        self._log_status("thread create name={0}".format(name))
        thread = threading.Thread(target=target, name=name, daemon=False)
        self._log_status("thread start name={0}".format(name))
        thread.start()

    def _job_done(self, page: str, text: str, media_path: str = "") -> bool:
        self._busy = False
        if page == "join":
            self._say_raw(self.join_result, text)
            if media_path:
                self._load_slot(self.JOIN_PLAYER_KEYS[2], media_path)
        else:
            self._say_raw(self.edit_result, text)
            if media_path:
                self._load_slot(self.EDIT_GENERATED_KEY, media_path)
        self._sync_edit()
        self._sync_join()
        return False

    def _selected_log(self):
        row = self.log_list.get_selected_row()
        if row is None:
            return ""
        return row.get_child().get_text()

    def _fill_logs(self) -> None:
        gtk = self._gtk
        while True:
            child = self.log_list.get_row_at_index(0)
            if child is None:
                break
            self.log_list.remove(child)
        self._paint_log_folder()
        for path in self.logs.log_files():
            self.log_list.append(gtk.Label(label=str(path), xalign=0))

    def _view_log(self, _button) -> None:
        path = self._selected_log()
        if not path:
            self._log_state = ("select",)
            self._paint_log_body()
            return
        body = self.logs.read_log(path)
        if body is None:
            self._log_state = ("outside",)
            self._paint_log_body()
            return
        self._log_state = ("view", Path(path).name, body)
        self._paint_log_body()

    def _clear_log(self, _button) -> None:
        path = self._selected_log()
        if not path:
            self._log_state = ("select",)
            self._paint_log_body()
            return
        name = Path(path).name
        self._confirm(
            self._fill("win_clear_ask", name),
            lambda: self._clear_confirmed(path, name),
        )

    def _clear_confirmed(self, path, name) -> None:
        if self.logs.clear_log(path):
            self._log_state = ("cleared", name)
        else:
            self._log_state = ("outside",)
        self._paint_log_body()

    def _paint_log_folder(self) -> None:
        label = getattr(self, "log_folder", None)
        logs = getattr(self, "logs", None)
        if label is None or logs is None:
            return
        folder = logs.log_dir()
        if folder:
            self._say(label, "win_log_folder", folder)
        else:
            self._say(label, "win_no_log")

    def _paint_log_body(self) -> None:
        view = getattr(self, "log_text", None)
        if view is None or not self._log_state:
            return
        kind = self._log_state[0]
        if kind == "select":
            text = self._w("win_select_log")
        elif kind == "outside":
            text = self._w("win_outside_log")
        elif kind == "cleared":
            text = self._fill("win_cleared", self._log_state[1])
        elif kind == "view":
            name, body = self._log_state[1], self._log_state[2]
            shown = body if body else self._w("win_empty")
            text = "{0}\n\n{1}".format(name, shown)
        else:
            return
        view.get_buffer().set_text(text, -1)

    def _fill_languages(self) -> None:
        gtk = self._gtk
        child = self.lang_box.get_first_child()
        while child is not None:
            nxt = child.get_next_sibling()
            self.lang_box.remove(child)
            child = nxt
        for code, endonym, number in self.language.CODES:
            button = gtk.Button(label="{0}  {1}".format(number, endonym))
            button.connect("clicked", self._save_language, code)
            self.lang_box.append(button)

    def _save_language(self, _button, code: str) -> None:
        notice = self.language.save(code)
        self.lang_notice.set_text(notice)
        for button, row in zip(self._menu_buttons, self.FRONT):
            number, kind, english, _page = row
            button.set_label(self._front_label(number, kind, english))
        self._apply_window_language()

    def _self_action(self, _button, kind: str) -> None:
        if kind == "version":
            self._set_self_body(self.app.self_manage.local_version())
            return
        if kind == "about":
            self._set_self_body(self.app.about.framework_about())
            return
        if kind == "self-uninstall":
            self._confirm(
                self._w("win_remove_ask"),
                lambda: self._run_self(kind),
            )
            return
        self._run_self(kind)

    def _run_self(self, kind: str) -> None:
        if self._busy:
            return
        self._busy = True
        self._set_self_body("please wait for time consuming process")
        self._start_thread("pip-{0}".format(kind), lambda: self._self_worker(kind))

    def _self_worker(self, kind: str) -> None:
        _code, text = self.app.self_manage.run_pip(kind)
        self._glib.idle_add(self._self_done, text)

    def _self_done(self, text: str) -> bool:
        self._busy = False
        self._set_self_body(text)
        self._sync_edit()
        self._sync_join()
        return False

    def _set_self_body(self, text: str) -> None:
        self.self_text.get_buffer().set_text(text or "", -1)

    def _confirm(self, message: str, on_yes) -> None:
        gtk = self._gtk
        dialog = gtk.Window(title="VideoTools", transient_for=self._window, modal=True)
        box = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=8)
        box.set_margin_top(12)
        box.set_margin_bottom(12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.append(gtk.Label(label=message))
        buttons = gtk.Box(orientation=gtk.Orientation.HORIZONTAL, spacing=6)
        no = gtk.Button(label=self._w("win_no"))
        yes = gtk.Button(label=self._w("win_yes"))
        no.connect("clicked", lambda _b: dialog.destroy())

        def accept(_b):
            dialog.destroy()
            on_yes()

        yes.connect("clicked", accept)
        buttons.append(no)
        buttons.append(yes)
        box.append(buttons)
        dialog.set_child(box)
        dialog.present()

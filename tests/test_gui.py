# Window routing and the elapsed-time clock. The text menu is not opened here.
import os
import unittest
from unittest.mock import patch

from VideoTools.cli import Cli
from VideoTools.gui import Gui


class TestElapsedClock(unittest.TestCase):
    def test_format_grows_minutes(self):
        self.assertEqual(Gui.format_elapsed(0), "00:00.00")
        self.assertEqual(Gui.format_elapsed(61.25), "01:01.25")
        self.assertEqual(Gui.format_elapsed(6000), "100:00.00")
        self.assertEqual(Gui.format_elapsed(-1), "00:00.00")

    def test_parse_round_trip(self):
        self.assertEqual(Gui.parse_elapsed("01:01.25"), 61.25)
        self.assertEqual(Gui.parse_elapsed("100:00.00"), 6000)
        self.assertIsNone(Gui.parse_elapsed("1:01.25"))
        self.assertIsNone(Gui.parse_elapsed("00:60.00"))
        self.assertIsNone(Gui.parse_elapsed("00:00"))

    def test_join_has_three_players_and_edit_has_a_generated_player(self):
        self.assertEqual(Gui.JOIN_PLAYER_KEYS, ("join-1", "join-2", "join-out"))
        self.assertEqual(Gui.EDIT_GENERATED_KEY, "edit-out")

    def test_generated_player_loads_only_a_real_file(self):
        self.assertEqual(Gui.playback_path(False, __file__), "")
        self.assertEqual(Gui.playback_path(True, ""), "")
        self.assertEqual(Gui.playback_path(True, "/no/such/video.mp4"), "")
        self.assertEqual(Gui.playback_path(True, __file__), __file__)

    def test_slot_clock_follows_the_stream(self):
        gui = Gui()

        class _Media:
            def get_timestamp(self):
                return 1500000

            def get_duration(self):
                return 3000000

        class _Label:
            def __init__(self):
                self.text = ""

            def set_text(self, text):
                self.text = text

        class _Scale:
            def __init__(self):
                self.rng = None
                self.value = None

            def set_range(self, low, high):
                self.rng = (low, high)

            def set_value(self, value):
                self.value = value

        elapsed = _Label()
        total = _Label()
        scale = _Scale()
        gui._slots["join-1"] = {
            "media": _Media(),
            "user_move": False,
            "path": __file__,
            "elapsed": elapsed,
            "scale": scale,
            "total": total,
        }
        gui._tick_slot("join-1")
        self.assertEqual(elapsed.text, "00:01.50")
        self.assertEqual(total.text, "00:03.00")
        self.assertEqual(scale.value, 1.5)


class TestWindowRoute(unittest.TestCase):
    def test_tui_is_a_verb_and_language_is_not(self):
        self.assertIn("tui", Cli.PRODUCT_VERBS)
        self.assertNotIn("language", Cli.PRODUCT_VERBS)

    def test_display_and_tty_with_no_verb_opens_the_window(self):
        with patch.dict(os.environ, {"DISPLAY": ":0"}):
            with patch.object(Cli, "stdin_is_tty", return_value=True):
                with patch.object(Cli, "stdout_is_tty", return_value=True):
                    self.assertTrue(Cli.opens_window([]))
                    self.assertFalse(Cli.opens_window(["tui"]))
                    self.assertFalse(Cli.opens_window(["join"]))
                    self.assertFalse(Cli.opens_window(["--json"]))
                    self.assertFalse(Cli.opens_window(["--file", "a.mp4"]))
                    self.assertFalse(Cli.opens_window(["--repeat"]))
                    self.assertFalse(Cli.opens_window(["--boomerang"]))

    def test_no_display_stays_off_the_window(self):
        env = os.environ.copy()
        env.pop("DISPLAY", None)
        with patch.dict(os.environ, env, clear=True):
            with patch.object(Cli, "stdin_is_tty", return_value=True):
                with patch.object(Cli, "stdout_is_tty", return_value=True):
                    self.assertFalse(Cli.opens_window([]))

    def test_closed_stdin_stays_off_the_window(self):
        with patch.dict(os.environ, {"DISPLAY": ":0"}):
            with patch.object(Cli, "stdin_is_tty", return_value=False):
                with patch.object(Cli, "stdout_is_tty", return_value=True):
                    self.assertFalse(Cli.opens_window([]))

    def test_tui_without_a_terminal_fails_closed(self):
        with patch.object(Cli, "stdin_is_tty", return_value=False):
            with patch.object(Cli, "stdout_is_tty", return_value=False):
                code = Cli().run(["tui"])
        self.assertEqual(code, 1)

    def test_bare_start_calls_the_window_when_display_is_set(self):
        cli = Cli()
        called = []
        cli.gui.open = lambda app: called.append(app) or 0
        with patch.dict(os.environ, {"DISPLAY": ":0"}):
            with patch.object(Cli, "stdin_is_tty", return_value=True):
                with patch.object(Cli, "stdout_is_tty", return_value=True):
                    code = cli.run([])
        self.assertEqual(code, 0)
        self.assertEqual(called, [cli])


class TestPlayerWidgets(unittest.TestCase):
    """Build the window when X11 and GTK 4 are present. No main loop."""

    def assert_sources_left_output_right(self, gui, gtk):
        """Edit and Join put sources on the start side and output on the end side."""
        panes = []

        def collect(widget):
            if widget is None:
                return
            if widget.__class__.__name__ == "Paned":
                panes.append(widget)
            child = widget.get_first_child() if hasattr(widget, "get_first_child") else None
            while child is not None:
                collect(child)
                child = child.get_next_sibling() if hasattr(child, "get_next_sibling") else None

        def holds(root, target):
            if root is None:
                return False
            if root is target:
                return True
            child = root.get_first_child() if hasattr(root, "get_first_child") else None
            while child is not None:
                if holds(child, target):
                    return True
                child = child.get_next_sibling() if hasattr(child, "get_next_sibling") else None
            return False

        collect(gui._window.get_child())
        self.assertEqual(len(panes), 2)
        edit_pane = next(pane for pane in panes if holds(pane, gui.edit_file))
        join_pane = next(pane for pane in panes if holds(pane, gui.join_entries[0]))
        for pane in (edit_pane, join_pane):
            self.assertEqual(pane.get_orientation(), gtk.Orientation.HORIZONTAL)
        self.assertTrue(holds(edit_pane.get_start_child(), gui.edit_file))
        self.assertTrue(holds(edit_pane.get_start_child(), gui.video_holder))
        self.assertTrue(holds(edit_pane.get_start_child(), gui.edit_start))
        self.assertTrue(holds(edit_pane.get_start_child(), gui.tail_none))
        self.assertTrue(holds(edit_pane.get_start_child(), gui.tail_boomerang))
        self.assertTrue(holds(edit_pane.get_start_child(), gui.tail_repeat))
        self.assertTrue(gui.tail_none.get_active())
        self.assertFalse(gui.tail_boomerang.get_active())
        self.assertFalse(gui.tail_repeat.get_active())
        self.assertEqual(gui._tail_effect(), "none")
        gui.tail_repeat.set_active(True)
        self.assertEqual(gui._tail_effect(), "repeat")
        self.assertFalse(gui.tail_none.get_active())
        gui.tail_boomerang.set_active(True)
        self.assertEqual(gui._tail_effect(), "boomerang")
        self.assertFalse(gui.tail_repeat.get_active())
        self.assertFalse(holds(edit_pane.get_start_child(), gui.edit_output))
        self.assertTrue(holds(edit_pane.get_end_child(), gui.edit_output))
        self.assertTrue(holds(edit_pane.get_end_child(), gui.edit_run))
        self.assertTrue(holds(edit_pane.get_end_child(), gui._slots["edit-out"]["play"]))
        self.assertFalse(holds(edit_pane.get_end_child(), gui.edit_file))
        sources = gui.join_entries[0].get_parent().get_parent().get_parent()
        self.assertEqual(sources.get_orientation(), gtk.Orientation.VERTICAL)
        self.assertIs(gui.join_entries[1].get_parent().get_parent().get_parent(), sources)
        self.assertTrue(holds(join_pane.get_start_child(), gui.join_entries[0]))
        self.assertTrue(holds(join_pane.get_start_child(), gui.join_entries[1]))
        self.assertTrue(holds(join_pane.get_start_child(), gui._slots["join-1"]["play"]))
        self.assertTrue(holds(join_pane.get_start_child(), gui._slots["join-2"]["play"]))
        self.assertFalse(holds(join_pane.get_start_child(), gui.join_output))
        self.assertTrue(holds(join_pane.get_end_child(), gui.join_name))
        self.assertTrue(holds(join_pane.get_end_child(), gui.join_output))
        self.assertTrue(holds(join_pane.get_end_child(), gui.join_run))
        self.assertTrue(holds(join_pane.get_end_child(), gui._slots["join-out"]["play"]))
        self.assertFalse(holds(join_pane.get_end_child(), gui.join_entries[0]))

    def assert_group_tabs_align(self, gui, glib):
        """Rows 1 and 2 share the group edges. The visible group stays highlighted."""
        tabs = gui._group_tab_box
        frame = gui._group_frame
        self.assertIs(tabs.get_parent(), frame.get_parent())
        self.assertIs(tabs.get_next_sibling(), frame)
        self.assertEqual(gui._stack.get_visible_child_name(), "edit")
        self.assertTrue(gui._group_tabs["edit"].get_active())
        self.assertFalse(gui._group_tabs["join"].get_active())
        self.assertTrue(frame.has_css_class("group-open"))
        self.assertEqual(gui._group_tabs["join"].get_label(), "join")
        self.assertEqual(gui._group_tabs["edit"].get_label(), "edit")
        self.assertEqual(
            [button.get_label() for button in gui._menu_buttons],
            ["join", "edit", "system-log", "language", "self-management", "Exit"],
        )
        gui._group_tabs["join"].set_active(True)
        self.assertEqual(gui._stack.get_visible_child_name(), "join")
        self.assertTrue(gui._group_tabs["join"].get_active())
        self.assertFalse(gui._group_tabs["edit"].get_active())
        gui._group_tabs["join"].set_active(False)
        self.assertTrue(gui._group_tabs["join"].get_active())
        gui._window.present()
        context = glib.MainContext.default()
        for _ in range(30):
            context.iteration(False)
        placed, tab_bounds = tabs.compute_bounds(gui._window)
        placed_frame, frame_bounds = frame.compute_bounds(gui._window)
        self.assertTrue(placed and placed_frame)
        self.assertEqual(round(tab_bounds.get_x()), round(frame_bounds.get_x()))
        self.assertEqual(round(tab_bounds.get_width()), round(frame_bounds.get_width()))
        gui._show("edit")
        self.assertEqual(gui._stack.get_visible_child_name(), "edit")
        self.assertTrue(gui._group_tabs["edit"].get_active())

    def test_join_and_edit_mount_players(self):
        if not os.environ.get("DISPLAY", "").strip():
            self.skipTest("no DISPLAY")
        gui = Gui()
        try:
            gtk, glib, gio, gdk = gui._load_toolkit()
        except Exception as exc:
            self.skipTest("GTK 4 is not available ({0})".format(exc))
        os.environ["GDK_BACKEND"] = "x11"
        if gdk.Display.get_default() is None:
            opened = gdk.Display.open(os.environ.get("DISPLAY", ""))
            if opened is None and gdk.Display.get_default() is None:
                self.skipTest("X11 refused the connection")
        gui._gtk = gtk
        gui._glib = glib
        gui._gio = gio

        class _Media:
            def get_duration_cv2(self, _path):
                return 1.5

        class _App:
            app_name = "VideoTools"
            version = "1.1.0"
            media = _Media()

        gui.app = _App()
        from VideoTools.menu_language import MenuLanguage

        gui.language = MenuLanguage(home="")
        gui._build()
        buttons = []
        captions = []

        def walk(widget):
            if widget is None:
                return
            kind = widget.__class__.__name__
            getter = getattr(widget, "get_label", None)
            if getter is not None:
                try:
                    label = getter() or ""
                except Exception:
                    label = ""
                if label and kind == "Button":
                    buttons.append(label)
                elif label and kind == "Label":
                    captions.append(label)
            child = widget.get_first_child() if hasattr(widget, "get_first_child") else None
            while child is not None:
                walk(child)
                child = child.get_next_sibling() if hasattr(child, "get_next_sibling") else None

        walk(gui._window.get_child())
        self.assert_sources_left_output_right(gui, gtk)
        self.assert_group_tabs_align(gui, glib)
        self.assertEqual(buttons.count("Play"), 4)
        self.assertEqual(buttons.count("Stop"), 5)
        self.assertEqual(captions.count("Generated"), 2)
        self.assertIn("Start", buttons)
        self.assertIn("Video 1", captions)
        self.assertIn("Video 2", captions)
        self.assertEqual(gui.elapsed.get_text(), "00:00.00")
        for key in Gui.JOIN_PLAYER_KEYS:
            slot = gui._slots[key]
            self.assertEqual(slot["elapsed"].get_text(), "00:00.00")
            self.assertEqual(slot["play"].get_label(), "Play")
            self.assertEqual(slot["stop"].get_label(), "Stop")
            self.assertIsNotNone(slot["scale"])
        generated = gui._slots[Gui.EDIT_GENERATED_KEY]
        self.assertEqual(generated["elapsed"].get_text(), "00:00.00")
        self.assertEqual(generated["play"].get_label(), "Play")
        self.assertEqual(generated["stop"].get_label(), "Stop")
        sample = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "sample-videos", "video-1.mp4"
        )
        if os.path.isfile(sample):
            gui._load_slot("join-1", sample)
            gui._job_done("join", "SUCCESS", sample)
            gui._job_done("edit", "SUCCESS", sample)
            self.assertEqual(gui._slots["join-1"]["path"], sample)
            self.assertEqual(gui._slots["join-out"]["path"], sample)
            self.assertEqual(gui._slots["edit-out"]["path"], sample)
            self.assertTrue(gui._slots["join-1"]["play"].get_sensitive())
            self.assertTrue(gui._slots["join-out"]["play"].get_sensitive())
            self.assertTrue(gui._slots["edit-out"]["play"].get_sensitive())
            self.assertEqual(gui._slots["join-1"]["total"].get_text(), "00:01.50")
            gui._on_slot_stop(None, "join-1")
            self.assertEqual(gui._slots["join-1"]["elapsed"].get_text(), "00:00.00")
            gui._pause_all_players()
            gui._job_done("edit", "Edit failed.", "")
            self.assertEqual(gui._slots["edit-out"]["path"], sample)
            gui._reset_generated(Gui.EDIT_GENERATED_KEY)
            self.assertEqual(gui._slots["edit-out"]["path"], "")
            self.assertEqual(gui._slots["edit-out"]["elapsed"].get_text(), "00:00.00")
            self.assertFalse(gui._slots["edit-out"]["play"].get_sensitive())
            self.assertFalse(gui._slots["edit-out"]["stop"].get_sensitive())
            self.assertFalse(gui._slots["edit-out"]["scale"].get_sensitive())
            self.assertEqual(gui._slots["join-1"]["path"], sample)
            gui._edit_done(0, sample, sample)
            self.assertEqual(gui._slots["edit-out"]["path"], sample)
            self.assertTrue(gui._slots["edit-out"]["play"].get_sensitive())
            self.assertTrue(gui._slots["edit-out"]["stop"].get_sensitive())
            self.assertTrue(gui._slots["edit-out"]["scale"].get_sensitive())
            gui._reset_generated(Gui.JOIN_PLAYER_KEYS[2])
            self.assertEqual(gui._slots["join-out"]["path"], "")
            self.assertFalse(gui._slots["join-out"]["play"].get_sensitive())
            self.assertEqual(gui._slots["join-1"]["path"], sample)
            gui._join_done(True, ["SUCCESS"], sample)
            self.assertEqual(gui._slots["join-out"]["path"], sample)
            self.assertTrue(gui._slots["join-out"]["play"].get_sensitive())
            gui._reset_generated(Gui.EDIT_GENERATED_KEY)
            gui._edit_done(1, "", "")
            self.assertEqual(gui._slots["edit-out"]["path"], "")
            self.assertFalse(gui._slots["edit-out"]["play"].get_sensitive())
        gui._window.destroy()

    def test_window_labels_follow_menu_language(self):
        """A language pick redraws Start, Tail, Generated, and Output. The clock stays."""
        if not os.environ.get("DISPLAY", "").strip():
            self.skipTest("no DISPLAY")
        import tempfile

        from VideoTools.menu_language import MenuLanguage

        gui = Gui()
        try:
            gtk, glib, gio, gdk = gui._load_toolkit()
        except Exception as exc:
            self.skipTest("GTK 4 is not available ({0})".format(exc))
        os.environ["GDK_BACKEND"] = "x11"
        if gdk.Display.get_default() is None:
            opened = gdk.Display.open(os.environ.get("DISPLAY", ""))
            if opened is None and gdk.Display.get_default() is None:
                self.skipTest("X11 refused the connection")
        gui._gtk = gtk
        gui._glib = glib
        gui._gio = gio

        class _App:
            app_name = "VideoTools"
            version = "1.1.0"

        gui.app = _App()
        home = tempfile.mkdtemp(prefix="vtwin_", dir="/tmp")
        gui.language = MenuLanguage(home=home)
        gui._build()
        self.assertEqual(gui.tail_none.get_label(), "None")
        self.assertEqual(gui.tail_boomerang.get_label(), "Boomerang")
        self.assertEqual(gui.tail_repeat.get_label(), "Repeat")
        self.assertEqual(gui.edit_output.get_text(), "Output")
        self.assertEqual(gui.elapsed.get_text(), "00:00.00")
        gui._save_language(None, "zh-Hans")
        self.assertEqual(gui.language.code(), "zh-Hans")
        self.assertEqual(gui.tail_none.get_label(), "无")
        self.assertEqual(gui.tail_boomerang.get_label(), "回旋")
        self.assertEqual(gui.tail_repeat.get_label(), "重复")
        self.assertEqual(gui.edit_output.get_text(), "输出")
        self.assertEqual(gui._slots["edit-out"]["play"].get_label(), "播放")
        self.assertEqual(gui._slots["edit-out"]["stop"].get_label(), "停止")
        self.assertEqual(gui._group_tabs["edit"].get_label(), "edit")
        self.assertEqual(gui._group_tabs["join"].get_label(), "join")
        self.assertEqual(gui._menu_buttons[3].get_label(), "语言")
        self.assertEqual(gui._menu_buttons[5].get_label(), "离开")
        self.assertTrue(gui.path_label.get_text().startswith("路径:"))
        self.assertEqual(gui.elapsed.get_text(), "00:00.00")
        self.assertEqual(gui.jump_entry.get_placeholder_text(), "00:00.00")
        captions = []
        buttons = []

        def walk(widget):
            if widget is None:
                return
            kind = widget.__class__.__name__
            getter = getattr(widget, "get_label", None)
            if getter is not None:
                try:
                    label = getter() or ""
                except Exception:
                    label = ""
                if label and kind == "Button":
                    buttons.append(label)
                elif label and kind == "Label":
                    captions.append(label)
            child = widget.get_first_child() if hasattr(widget, "get_first_child") else None
            while child is not None:
                walk(child)
                child = child.get_next_sibling() if hasattr(child, "get_next_sibling") else None

        walk(gui._window.get_child())
        self.assertIn("开始", buttons)
        self.assertEqual(buttons.count("播放"), 4)
        self.assertEqual(buttons.count("停止"), 5)
        self.assertEqual(captions.count("已生成"), 2)
        self.assertIn("视频 1", captions)
        self.assertIn("百分比", captions)
        self.assertIn("收尾", captions)
        gui._save_language(None, "en")
        self.assertEqual(gui.tail_none.get_label(), "None")
        self.assertEqual(gui._slots["edit-out"]["play"].get_label(), "Play")
        self.assertEqual(gui.edit_output.get_text(), "Output")
        self.assertEqual(gui.elapsed.get_text(), "00:00.00")
        gui._window.destroy()

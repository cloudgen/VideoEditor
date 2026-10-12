# Window routing and the elapsed-time clock. The text menu is not opened here.
import os
import tempfile
import unittest
from unittest.mock import patch

from VideoEditor.cli import Cli
from VideoEditor.gui import Gui


class TestElapsedClock(unittest.TestCase):
    def test_main_background_is_light_gray(self):
        self.assertEqual(Gui.MAIN_BACKGROUND, "#d3d3d3")
        rule = Gui._canvas_rule()
        self.assertIn("background-color: #d3d3d3", rule)
        self.assertEqual(Gui.PANEL_BACKGROUND, "#ffffff")
        self.assertIn("background-color: #ffffff", rule)

    def test_filmstrip_height_samples_and_cache(self):
        self.assertEqual(Gui.THUMBNAIL_TRACK_HEIGHT, 56)
        self.assertGreaterEqual(Gui.THUMBNAIL_TRACK_HEIGHT, 48)
        self.assertLessEqual(Gui.THUMBNAIL_TRACK_HEIGHT, 64)
        self.assertAlmostEqual(Gui.thumbnail_trail_height_proportion(200), 56 / 200)
        self.assertAlmostEqual(Gui.thumbnail_trail_height_proportion(180), 56 / 180)
        self.assertLess(Gui.thumbnail_trail_height_proportion(180), 0.5)
        self.assertEqual(Gui.thumbnail_trail_height_proportion(0), 0.0)
        self.assertEqual(Gui.sample_interval(10), 2.0)
        self.assertEqual(Gui.sample_interval(119.9), 2.0)
        self.assertEqual(Gui.sample_interval(120), 5.0)
        self.assertEqual(Gui.sample_interval(3600), 5.0)
        self.assertEqual(Gui.sample_times(10), [0.0, 2.0, 4.0, 6.0, 8.0])
        self.assertEqual(Gui.sample_times(0), [0.0])
        long_times = Gui.sample_times(130)
        self.assertEqual(long_times[1] - long_times[0], 5.0)
        self.assertLessEqual(long_times[1] - long_times[0], 5.0)
        self.assertGreaterEqual(long_times[1] - long_times[0], 2.0)
        self.assertEqual(Gui.format_elapsed(83.45), "01:23.45")
        self.assertEqual(Gui.hover_seconds(0, 100, 0, 18), 0)
        self.assertAlmostEqual(Gui.hover_seconds(50, 100, 0, 18), 9)
        self.assertAlmostEqual(Gui.hover_seconds(500, 100, 0, 18), 18)
        self.assertIn("min-height: 56px", Gui._filmstrip_rule())
        sample = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "sample-videos", "video-1.mp4"
        )
        if not os.path.isfile(sample):
            return
        first = Gui.build_filmstrip_png(sample)
        self.assertTrue(os.path.isfile(first))
        self.assertTrue(os.path.abspath(first).startswith(os.path.abspath(tempfile.gettempdir())))
        stamp = os.stat(first).st_mtime_ns
        second = Gui.build_filmstrip_png(sample)
        self.assertEqual(first, second)
        self.assertEqual(os.stat(second).st_mtime_ns, stamp)

    def test_hover_does_not_seek(self):
        gui = Gui()
        gui._edit_path = ""

        class _Scale:
            def __init__(self):
                self.value = 3.0
                self.tip = "unset"
                self.rng = (0.0, 18.0)
                self.width = 100

            def get_range(self):
                return self.rng

            def get_width(self):
                return self.width

            def get_value(self):
                return self.value

            def set_value(self, value):
                self.value = value

            def set_tooltip_text(self, text):
                self.tip = text

            def get_sensitive(self):
                return True

        scale = _Scale()
        gui._on_film_hover(None, 50, 0, scale, "edit")
        self.assertEqual(scale.value, 3.0)
        self.assertIsNone(scale.tip)
        gui._edit_path = "reel.mp4"
        gui._on_film_hover(None, 50, 0, scale, "edit")
        self.assertEqual(scale.value, 3.0)
        self.assertEqual(scale.tip, "00:09.00")

    def test_click_seeks_only_when_a_file_is_loaded(self):
        gui = Gui()
        gui._edit_path = ""
        seen = {}

        class _Scale:
            def __init__(self):
                self.value = 3.0
                self.rng = (0.0, 18.0)
                self.sensitive = True

            def get_range(self):
                return self.rng

            def get_width(self):
                return 100

            def get_value(self):
                return self.value

            def set_value(self, value):
                self.value = value

            def get_sensitive(self):
                return self.sensitive

        scale = _Scale()
        gui._on_film_click(None, 1, 50, 0, scale, "edit")
        self.assertEqual(scale.value, 3.0)
        gui._edit_path = "reel.mp4"
        gui._on_seek = lambda _scale, _scroll, value: seen.setdefault("value", value)
        gui._on_film_click(None, 1, 50, 0, scale, "edit")
        self.assertEqual(scale.value, 9.0)
        self.assertEqual(seen["value"], 9.0)
        scale.sensitive = False
        scale.value = 1.0
        gui._on_film_click(None, 1, 0, 0, scale, "edit")
        self.assertEqual(scale.value, 1.0)

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
        gui._slots["join-1"]["duration"] = 8.0
        gui._tick_slot("join-1")
        self.assertEqual(total.text, "00:08.00")
        self.assertEqual(scale.rng, (0, 8.0))


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

    def assert_white_panels(self, gui):
        """Source and output cards, videos, and player controls use the white panel."""
        frames = []
        videos = []

        def walk(widget):
            if widget is None:
                return
            kind = widget.__class__.__name__
            if kind == "Frame" and widget.has_css_class("app-panel"):
                frames.append(widget)
            if kind == "Video":
                videos.append(widget)
                self.assertTrue(widget.has_css_class("app-panel"))
            child = widget.get_first_child() if hasattr(widget, "get_first_child") else None
            while child is not None:
                walk(child)
                child = child.get_next_sibling() if hasattr(child, "get_next_sibling") else None

        walk(gui._window.get_child())
        self.assertGreaterEqual(len(frames), 9)
        self.assertGreaterEqual(len(videos), 4)
        for key in ("join-1", "join-2", "join-out", "edit-out"):
            self.assertTrue(gui._slots[key]["holder"].has_css_class("app-panel"))

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
        sources = gui.join_entries[0].get_parent().get_parent().get_parent().get_parent()
        self.assertEqual(sources.get_orientation(), gtk.Orientation.VERTICAL)
        self.assertIs(
            gui.join_entries[1].get_parent().get_parent().get_parent().get_parent(),
            sources,
        )
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

        lengths = {"seconds": 1.5}

        class _Media:
            def get_duration_cv2(self, _path):
                return lengths["seconds"]

        class _App:
            app_name = "VideoEditor"
            version = "1.1.0"
            media = _Media()

        gui.app = _App()
        from VideoEditor.menu_language import MenuLanguage

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
        self.assertTrue(gui._window.has_css_class("app-canvas"))
        self.assertTrue(gui._root.has_css_class("app-canvas"))
        self.assertTrue(gui.video_holder.has_css_class("app-panel"))
        self.assert_white_panels(gui)
        self.assertEqual(gui._film["edit"]["area"].get_size_request().height, 56)
        self.assertEqual(gui._film["edit"]["area"].__class__.__name__, "Picture")
        self.assertTrue(gui.scale.has_css_class("timeline-preview"))
        self.assertEqual(gui.scale.get_parent().__class__.__name__, "Overlay")
        for key in list(Gui.JOIN_PLAYER_KEYS) + [Gui.EDIT_GENERATED_KEY]:
            self.assertEqual(gui._film[key]["area"].get_size_request().height, 56)
            self.assertTrue(gui._slots[key]["scale"].has_css_class("timeline-preview"))
        held = gui.scale.get_value()
        gui._edit_path = "reel.mp4"
        gui.scale.set_range(0, 18.04)
        gui._on_film_hover(None, 10, 0, gui.scale, "edit")
        self.assertEqual(gui.scale.get_value(), held)
        self.assertIsNotNone(gui.scale.get_tooltip_text())
        gui._edit_path = ""
        self.assertTrue(gui.path_label.get_text().startswith("Project Root:"))
        self.assertEqual(gui.process.get_text(), "Process 0%")
        self.assertEqual(gui.process.get_fraction(), 0)
        gui._process_mode = "wait"
        gui._paint_process()
        self.assertEqual(gui.process.get_text(), "please wait for time consuming process")
        self.assertEqual(gui.process.get_fraction(), 0)
        gui._process_mode = "idle"
        gui._paint_process()
        self.assertEqual(gui.process.get_text(), "Process 0%")
        self.assertEqual(gui.tail_none_label.get_text(), "None")
        gui.tail_none.set_active(True)
        self.assertEqual(gui._tail_effect(), "none")
        self.assertFalse(gui.tail_boomerang.get_active())
        self.assertFalse(gui.tail_repeat.get_active())
        gui.tail_boomerang.set_active(True)
        self.assertTrue(gui.tail_boomerang.get_active())
        self.assertFalse(gui.tail_none.get_active())
        self.assertFalse(gui.tail_repeat.get_active())
        self.assertEqual(gui._tail_effect(), "boomerang")
        gui.tail_repeat.set_active(True)
        self.assertTrue(gui.tail_repeat.get_active())
        self.assertFalse(gui.tail_boomerang.get_active())
        self.assertFalse(gui.tail_none.get_active())
        gui.tail_repeat.set_active(False)
        self.assertTrue(gui.tail_none.get_active())
        self.assertFalse(gui.tail_repeat.get_active())
        self.assertEqual(gui._tail_effect(), "none")
        self.assertEqual(int(gui.percent.get_value()), 100)
        self.assertEqual(int(gui.percent_scale.get_value()), 100)
        gui.percent_scale.set_value(150)
        self.assertEqual(int(gui.percent.get_value()), 150)
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
            self.assertEqual(gui._slots["edit-out"]["total"].get_text(), "00:01.50")
            lengths["seconds"] = 4.25
            gui._edit_done(0, sample, sample)
            self.assertEqual(gui._slots["edit-out"]["total"].get_text(), "00:04.25")
            self.assertEqual(gui.process.get_text(), "Process 100%")
            self.assertEqual(gui.process.get_fraction(), 1)
            self.assertTrue(gui._slots["edit-out"]["play"].get_sensitive())
            self.assertTrue(gui._slots["edit-out"]["stop"].get_sensitive())
            self.assertTrue(gui._slots["edit-out"]["scale"].get_sensitive())
            gui._reset_generated(Gui.JOIN_PLAYER_KEYS[2])
            self.assertEqual(gui._slots["join-out"]["path"], "")
            self.assertFalse(gui._slots["join-out"]["play"].get_sensitive())
            self.assertEqual(gui._slots["join-1"]["path"], sample)
            gui._join_done(True, ["SUCCESS"], sample)
            self.assertEqual(gui._slots["join-out"]["path"], sample)
            self.assertEqual(gui._slots["join-out"]["total"].get_text(), "00:04.25")
            self.assertTrue(gui._slots["join-out"]["play"].get_sensitive())
            gui._reset_generated(Gui.EDIT_GENERATED_KEY)
            gui._edit_done(1, "", "")
            gui.wait_filmstrips(20)
            cached = Gui.filmstrip_cache_file(sample)
            self.assertTrue(cached.is_file())
            self.assertIsNotNone(gui._film["join-1"]["area"].get_paintable())
            self.assertTrue(
                os.path.abspath(str(cached)).startswith(os.path.abspath(tempfile.gettempdir()))
            )
            self.assertEqual(gui._slots["edit-out"]["path"], "")
            self.assertEqual(gui.process.get_text(), "Process 0%")
            self.assertFalse(gui._slots["edit-out"]["play"].get_sensitive())
        gui._window.destroy()

    def test_window_labels_follow_menu_language(self):
        """A language pick redraws Start, Tail, Generated, and Output. The clock stays."""
        if not os.environ.get("DISPLAY", "").strip():
            self.skipTest("no DISPLAY")
        import tempfile

        from VideoEditor.menu_language import MenuLanguage

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
            app_name = "VideoEditor"
            version = "1.1.0"

        gui.app = _App()
        home = tempfile.mkdtemp(prefix="vtwin_", dir="/tmp")
        gui.language = MenuLanguage(home=home)
        gui._build()
        self.assertEqual(gui.tail_none_label.get_text(), "None")
        self.assertEqual(gui.tail_boomerang_label.get_text(), "Boomerang")
        self.assertEqual(gui.tail_repeat_label.get_text(), "Repeat")
        self.assertEqual(gui.process.get_text(), "Process 0%")
        self.assertEqual(gui.edit_output.get_text(), "Output")
        self.assertEqual(gui.elapsed.get_text(), "00:00.00")
        gui._save_language(None, "zh-Hans")
        self.assertEqual(gui.language.code(), "zh-Hans")
        self.assertEqual(gui.tail_none_label.get_text(), "无")
        self.assertEqual(gui.tail_boomerang_label.get_text(), "回旋")
        self.assertEqual(gui.tail_repeat_label.get_text(), "重复")
        self.assertEqual(gui.edit_output.get_text(), "输出")
        self.assertEqual(gui.process.get_text(), "处理 0%")
        gui._process_mode = "wait"
        gui._paint_process()
        self.assertEqual(gui.process.get_text(), "please wait for time consuming process")
        gui._process_mode = "idle"
        gui._paint_process()
        self.assertEqual(gui.process.get_text(), "处理 0%")
        self.assertTrue(gui.path_label.get_text().startswith("项目根目录:"))
        self.assertEqual(gui._slots["edit-out"]["play"].get_label(), "播放")
        self.assertEqual(gui._slots["edit-out"]["stop"].get_label(), "停止")
        self.assertEqual(gui._group_tabs["edit"].get_label(), "edit")
        self.assertEqual(gui._group_tabs["join"].get_label(), "join")
        self.assertEqual(gui._menu_buttons[3].get_label(), "语言")
        self.assertEqual(gui._menu_buttons[5].get_label(), "离开")
        self.assertFalse(gui.path_label.get_text().startswith("路径:"))
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
        self.assertIn("循环选项", captions)
        self.assertIn("输入视频", captions)
        self.assertIn("输出与结果", captions)
        self.assertIn("结果视频", captions)
        self.assertIn("剪辑控制", captions)
        gui._save_language(None, "en")
        self.assertEqual(gui.tail_none_label.get_text(), "None")
        self.assertEqual(gui.process.get_text(), "Process 0%")
        self.assertEqual(gui._slots["edit-out"]["play"].get_label(), "Play")
        self.assertEqual(gui.edit_output.get_text(), "Output")
        self.assertEqual(gui.elapsed.get_text(), "00:00.00")
        gui._window.destroy()

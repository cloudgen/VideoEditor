# Tail choice on an edit job: none, boomerang, or repeat.
import io
import unittest
from pathlib import Path
from unittest.mock import patch

from VideoEditor.cli import Cli
from VideoEditor.edit_walk import EditWalk
from VideoEditor.encoder import Encoder


class _Sink:
    json_mode = False
    message_sink = None

    def out_info(self, _msg):
        return None

    def out_err(self, _msg):
        return None

    def _remember(self, *_args, **_kwargs):
        return None


class TestEditTail(unittest.TestCase):
    def encoder(self):
        return Encoder(_Sink(), None, None, 20, 200)

    def test_names_keep_boomerang_and_add_repeat(self):
        enc = self.encoder()
        src = Path("/tmp/clip.mp4")
        self.assertEqual(
            enc.build_output_name(src, 1, 5, 50, "none").name,
            "clip_cut1.0-5.0s_50pct.mp4",
        )
        self.assertEqual(
            enc.build_output_name(src, 1, 5, 50, False).name,
            "clip_cut1.0-5.0s_50pct.mp4",
        )
        self.assertEqual(
            enc.build_output_name(src, 1, 5, 50, "boomerang").name,
            "clip_cut1.0-5.0s_50pct_BOOMERANG.mp4",
        )
        self.assertEqual(
            enc.build_output_name(src, 1, 5, 50, True).name,
            "clip_cut1.0-5.0s_50pct_BOOMERANG.mp4",
        )
        self.assertEqual(
            enc.build_output_name(src, 1, 5, 50, "repeat").name,
            "clip_cut1.0-5.0s_50pct_REPEAT.mp4",
        )

    def test_normalize_accepts_the_three_words(self):
        enc = self.encoder()
        self.assertEqual(enc.normalize_tail(""), "none")
        self.assertEqual(enc.normalize_tail("none"), "none")
        self.assertEqual(enc.normalize_tail("boomerang"), "boomerang")
        self.assertEqual(enc.normalize_tail("repeat"), "repeat")
        self.assertIsNone(enc.normalize_tail("both"))
        self.assertIsNone(enc.normalize_tail("y"))

    def test_prompt_accepts_empty_repeat_and_rejects_a_typo(self):
        enc = self.encoder()
        walk = EditWalk(_Sink(), enc, None, 20, 200)
        answers = iter(["", "nope", "repeat"])
        walk._prompt_line = lambda _label: next(answers)
        err = io.StringIO()
        with patch("sys.stderr", err):
            self.assertEqual(walk._prompt_tail("Tail", "none"), "none")
            self.assertEqual(walk._prompt_tail("Tail", "boomerang"), "repeat")
        self.assertIn("Choose none, boomerang, or repeat", err.getvalue())

    def test_json_job_records_the_tail(self):
        from VideoEditor.run_output import RunOutput

        out = RunOutput("VideoEditor", "1.1.0")
        out.json_mode = True
        out._remember_job("/tmp/clip.mp4", 0, 1, 100, "repeat", "/tmp/out.mp4")
        out._remember_job("/tmp/clip.mp4", 0, 1, 100, "boomerang", "/tmp/boom.mp4")
        self.assertEqual(out.json_jobs[0]["tail"], "repeat")
        self.assertFalse(out.json_jobs[0]["boomerang"])
        self.assertEqual(out.json_jobs[1]["tail"], "boomerang")
        self.assertTrue(out.json_jobs[1]["boomerang"])

    def test_both_flags_fail_before_ffmpeg(self):
        cli = Cli()
        err = io.StringIO()
        with patch("sys.stderr", err):
            code = cli.run([
                "edit",
                "--file",
                "clip.mp4",
                "--start",
                "0",
                "--end",
                "1",
                "--boomerang",
                "--repeat",
            ])
        self.assertEqual(code, 1)
        self.assertIn("one tail", err.getvalue().lower())

    def test_repeat_alone_needs_a_complete_job(self):
        cli = Cli()
        err = io.StringIO()
        with patch("sys.stderr", err):
            code = cli.run(["--repeat"])
        self.assertEqual(code, 1)
        self.assertIn("--repeat", err.getvalue())

    def test_repeat_flag_does_not_open_the_text_screen(self):
        with patch.object(Cli, "stdout_is_tty", return_value=True):
            self.assertFalse(Cli.opens_text_screen(["--repeat"]))
            self.assertTrue(Cli.opens_text_screen(["edit", "--repeat"]))
            self.assertFalse(Cli.opens_text_screen([
                "edit", "--file", "a.mp4", "--start", "0", "--end", "1", "--repeat",
            ]))
            self.assertTrue(Cli.opens_text_screen(["edit"]))

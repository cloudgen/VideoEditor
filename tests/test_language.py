# TP-LANG-01 — menu language. Primary law: requirement-python-cli-language.
# Front row 4 is language. system-log is front row 3. LANG does not select a code.
import os
import stat
import tempfile
import unittest

from VideoTools.cli import Cli
from VideoTools.menu_language import MenuLanguage, _WINDOW, _WINDOW_KEYS
from VideoTools.menu_model import MenuModel
from VideoTools.menu_painter import MenuPainter
from VideoTools.menu_session import MenuSession


def _commit(model, token):
    model.buffer = token
    model.cursor = len(token)
    model.focus = "input"
    return model.apply_key(10)


class TestMenuLanguage(unittest.TestCase):
    """TP-LANG-01."""

    def setUp(self):
        self.home = tempfile.mkdtemp(prefix="vjlang_", dir="/tmp")
        self.saved = {
            name: os.environ.get(name)
            for name in ("HOME", "VIDEOTOOLS_LANG", "LANG", "LC_ALL")
        }
        os.environ["HOME"] = self.home
        os.environ.pop("VIDEOTOOLS_LANG", None)
        os.environ["LANG"] = "zh_TW.UTF-8"
        os.environ["LC_ALL"] = "zh_TW.UTF-8"
        self.painter = MenuPainter(home=self.home)
        self.model = MenuModel(painter=self.painter)

    def tearDown(self):
        for name, value in self.saved.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value

    def test_tp_lang_01_front_row_and_blocks(self):
        """TP-LANG-01: row 4 is language. Row 3 is system-log. 40 and 54 are not printed."""
        front = self.painter.display_rows("front")
        numbers = [row[0] for row in front]
        self.assertEqual(numbers, [1, 2, 3, 4, 8, 9])
        self.assertEqual(front[1][3], "edit")
        self.assertEqual(front[2][3], "system-log")
        self.assertEqual(front[3][1], "language")
        self.assertEqual(front[3][3], "language")
        self.assertIn(2, numbers)
        log_rows = self.painter.display_rows("log")
        self.assertEqual([row[0] for row in log_rows], [31, 32, 33, 0])
        self.assertEqual([row[1] for row in log_rows[:3]], ["view-log", "clear-log", "log-folder"])
        lang_rows = self.painter.display_rows("lang")
        printed = [row[0] for row in lang_rows]
        self.assertEqual(printed[:13], list(range(41, 54)))
        self.assertEqual(printed[-1], 0)
        self.assertNotIn(40, printed)
        self.assertNotIn(54, printed)
        self.assertNotIn(59, printed)
        endonyms = [row[1] for row in lang_rows[:-1]]
        self.assertEqual(endonyms[0], "English")
        self.assertEqual(endonyms[2], "繁體中文")
        self.assertEqual(endonyms[-1], "Ελληνικά")
        self.assertIsNone(_commit(self.model, "4"))
        self.assertEqual(self.model.layer, "lang")

    def test_tp_lang_01_save_back_reserved_and_env(self):
        """TP-LANG-01: save writes mode 0600. Back and reserved numbers do not write."""
        leaf = self.painter.language.leaf_path()
        self.assertFalse(os.path.exists(os.path.join(self.home, ".local")))
        self.assertIsNone(_commit(self.model, "4"))
        self.assertIsNone(_commit(self.model, "0"))
        self.assertEqual(self.model.layer, "front")
        self.assertFalse(os.path.exists(leaf))
        self.assertIsNone(_commit(self.model, "4"))
        self.assertIsNone(_commit(self.model, "40"))
        self.assertEqual(self.model.layer, "lang")
        self.assertIn("not on this list", self.model.error)
        self.assertFalse(os.path.exists(leaf))
        self.assertIsNone(_commit(self.model, "54"))
        self.assertFalse(os.path.exists(leaf))
        action = _commit(self.model, "43")
        self.assertEqual(action, "set-zh-Hant")
        session = MenuSession(
            "VideoJoin",
            "1.0.4",
            on_version=lambda: "1.0.4",
            on_about=lambda: "about",
            painter=self.painter,
        )
        session.model = self.model
        self.assertEqual(session.take_action(action), "stay")
        self.assertEqual(self.model.layer, "front")
        self.assertEqual(self.model.notice, "選單語言是繁體中文")
        self.assertEqual(self.painter.path_label(), "路徑")
        self.assertEqual(self.painter.language.code(), "zh-Hant")
        self.assertTrue(leaf.startswith(self.home))
        with open(leaf, "r", encoding="utf-8") as handle:
            self.assertEqual(handle.read(), "zh-Hant\n")
        self.assertEqual(stat.S_IMODE(os.stat(leaf).st_mode), 0o600)
        folder = os.path.dirname(leaf)
        self.assertEqual(stat.S_IMODE(os.stat(folder).st_mode), 0o700)
        front = self.painter.display_rows("front")
        self.assertEqual(front[3][1], "語言")
        self.assertEqual(front[0][1], "join")
        self.assertEqual(front[1][1], "edit")
        self.assertEqual(self.painter.display_rows("log")[0][1], "view-log")
        self.assertEqual(self.painter.display_rows("lang")[0][1], "English")
        self.assertNotIn("language", Cli.PRODUCT_VERBS)

    def test_tp_lang_01_invalid_leaf_and_env_override(self):
        """TP-LANG-01: a bad first line stays English. VIDEOTOOLS_LANG wins and does not write."""
        leaf = self.painter.language.leaf_path()
        os.makedirs(os.path.dirname(leaf), mode=0o700)
        with open(leaf, "w", encoding="utf-8") as handle:
            handle.write("nope\nzh-Hant\n")
        loaded = MenuLanguage(home=self.home)
        self.assertEqual(loaded.code(), "en")
        self.assertEqual(loaded.path_label(), "Path")
        with open(leaf, "r", encoding="utf-8") as handle:
            self.assertEqual(handle.read(), "nope\nzh-Hant\n")
        os.environ["VIDEOTOOLS_LANG"] = "zh-Hant"
        forced = MenuLanguage(home=self.home)
        self.assertEqual(forced.code(), "zh-Hant")
        self.assertEqual(forced.path_label(), MenuPainter.PATH_LABEL_ZH_HANT)
        with open(leaf, "r", encoding="utf-8") as handle:
            self.assertEqual(handle.read(), "nope\nzh-Hant\n")
        os.environ.pop("VIDEOTOOLS_LANG", None)
        cr = MenuLanguage(home=self.home)
        with open(leaf, "w", encoding="utf-8") as handle:
            handle.write("es\r\n")
        cr.load()
        self.assertEqual(cr.code(), "es")
        self.assertEqual(cr.path_label(), "Ruta")

    def test_tp_lang_01_failed_write_keeps_the_code(self):
        """TP-LANG-01: a failed write keeps the previous code and warns in that language."""
        empty = MenuLanguage(home="")
        self.assertEqual(empty.save("es"), "Could not save the menu language")
        self.assertEqual(empty.code(), "en")
        self.painter.language.save("zh-Hant")
        local = os.path.join(self.home, ".local")
        os.rename(local, local + ".kept")
        with open(local, "w", encoding="utf-8") as handle:
            handle.write("x")
        message = self.painter.language.save("es")
        self.assertEqual(self.painter.language.code(), "zh-Hant")
        self.assertEqual(message, "無法儲存選單語言")

    def test_window_labels_follow_the_code(self):
        """Window controls use the thirteen codes. English strings stay the current labels."""
        lang = MenuLanguage(home=self.home)
        self.assertEqual(lang.window("win_start"), "Start")
        self.assertEqual(lang.window("win_stop"), "Stop")
        self.assertEqual(lang.window("win_percent"), "Percent")
        self.assertEqual(lang.window("win_tail"), "Tail")
        self.assertEqual(lang.window("win_none"), "None")
        self.assertEqual(lang.window("win_boomerang"), "Boomerang")
        self.assertEqual(lang.window("win_repeat"), "Repeat")
        self.assertEqual(lang.window("win_output"), "Output")
        self.assertEqual(lang.window("win_generated"), "Generated")
        self.assertEqual(lang.window("win_play"), "Play")
        self.assertEqual(lang.window("win_go"), "Go To")
        self.assertEqual(lang.window("win_project_root"), "Project Root")
        self.assertEqual(lang.window("win_input_video"), "Input Video")
        self.assertEqual(lang.window("win_looping"), "Looping Options")
        self.assertEqual(lang.window("win_output_result"), "Output & Result")
        self.assertEqual(lang.window("win_resulting"), "Resulting Video")
        self.assertEqual(lang.window("win_process"), "Process {0}%")
        self.assertEqual(lang.window("win_mp4"), "MP4")
        self.assertEqual(lang.window("win_output_path"), "Output  {0}")
        self.assertIn("00:00.00", lang.window("win_jump_format"))
        for code, _name, _number in MenuLanguage.CODES:
            self.assertEqual(set(_WINDOW[code]), set(_WINDOW_KEYS), code)
            self.assertEqual(_WINDOW[code]["win_mp4"], "MP4")
            self.assertIn("00:00.00", _WINDOW[code]["win_jump_format"])
        self.assertEqual(lang.save("zh-Hans"), "菜单语言是简体中文")
        self.assertEqual(lang.window("win_tail"), "收尾")
        self.assertEqual(lang.window("win_none"), "无")
        self.assertEqual(lang.window("win_boomerang"), "回旋")
        self.assertEqual(lang.window("win_repeat"), "重复")
        self.assertEqual(lang.window("win_generated"), "已生成")
        self.assertEqual(lang.window("win_percent"), "百分比")
        self.assertEqual(lang.window("win_start"), "开始")
        self.assertEqual(lang.window("win_stop"), "停止")
        self.assertEqual(lang.window("win_output"), "输出")
        self.assertEqual(lang.window("win_play"), "播放")
        self.assertEqual(lang.window("win_project_root"), "项目根目录")
        self.assertEqual(lang.window("win_process"), "处理 {0}%")
        self.assertEqual(lang.window("win_looping"), "循环选项")
        self.assertEqual(lang.window("missing"), "")
        self.assertEqual(lang.row_short("edit", "edit"), "edit")
        self.assertEqual(lang.row_short("join", "join"), "join")


if __name__ == "__main__":
    unittest.main()

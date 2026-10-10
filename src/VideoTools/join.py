# =============================================================================
# Two-file concat for VideoTools.
# requirement-python-oop — class Join.
# requirement-domain-videojoin — discover, pick, output name.
# requirement-video-ffmpeg-pipeline — copy, then fail-closed re-encode.
# requirement-python-coding-style — unique temps, shutil.move publish.
# requirement-python-cli-logging — log the temp, the publish, and the discard first.
# =============================================================================
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path



class Join:
    """Discover two videos in this folder, name the output, and concatenate them."""

    def __init__(self, logger=None, video_suffixes=None, output_suffixes=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Join")
        self.video_suffixes = frozenset(video_suffixes or ())
        self.output_suffixes = tuple(output_suffixes or ())

    def _info(self, message):
        """Status line before a file operation. component join, not only in debug."""
        if self.logger is None:
            return
        self.logger.log_message(message, level="INFO", component="join")

    def _error(self, message):
        """Durable copy of a user-visible failure. The screen still shows the sentence."""
        if self.logger is None:
            return
        self.logger.log_message(message, level="ERROR", component="join")

    def discover(self, directory=None):
        """
        General Purpose: Eligible videos in one folder, sorted by name.
        The default folder is the current working directory. Not recursive.
        """
        root = Path(directory or ".")
        try:
            entries = list(root.iterdir())
        except OSError as exc:
            self._error("Could not read {0}: {1}".format(root, exc))
            return []
        found = [
            item
            for item in entries
            if item.is_file() and item.suffix.lower() in self.video_suffixes
        ]
        return sorted(found, key=lambda item: item.name.lower())

    def remaining_after(self, files, first):
        """General Purpose: The list for the second pick. The first path is gone."""
        return [item for item in files if item != first]

    def resolve_output_name(self, vid1, vid2, raw_name):
        """
        General Purpose: Output path from the typed name, or the default pattern.
        A name that does not end with .mp4, .mkv, or .mov gains .mp4.
        """
        default_name = "{0} + {1}.mp4".format(Path(vid1).stem, Path(vid2).stem)
        out_name = (raw_name or "").strip() or default_name
        if not out_name.lower().endswith(self.output_suffixes):
            out_name += ".mp4"
        return Path(out_name)

    def block_reason(self):
        """
        General Purpose: Why join must not start, or None when the questions may open.
        Fewer than two videos, or ffmpeg missing. Does not spawn a concat.
        """
        files = self.discover()
        if len(files) < 2:
            message = "Need at least 2 video files in this folder!"
            self._error(message)
            return [message]
        ready, lines = self.ffmpeg_status()
        if not ready:
            return lines
        return None

    def ffmpeg_status(self):
        """General Purpose: Fail closed when the ffmpeg binary cannot run."""
        if shutil.which("ffmpeg") is None:
            lines = [
                "ERROR: ffmpeg not found on PATH.",
                "   Install FFmpeg and ensure `ffmpeg` is available.",
                "   → https://ffmpeg.org/download.html",
            ]
            self._error(lines[0])
            return False, lines
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True,
                check=True,
                stdin=subprocess.DEVNULL,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            lines = ["ERROR: ffmpeg found but failed to run `-version`."]
            self._error(lines[0])
            return False, lines
        return True, []

    # =============================================================================
    # CIAO-Lite Protection Zone — temp staging + publish (USB / multi-mount)
    # System TMPDIR and removable media are often different filesystems.
    # Bare os.rename / os.replace do NOT cross mounts (Linux EXDEV).
    # Publish completed intermediates with shutil.move (rename same FS; copy+delete
    # on EXDEV). Prefer temps next to final output when writable.
    # Law: requirement-video-ffmpeg-pipeline, requirement-python-coding-style
    # =============================================================================

    def staging_dir_for(self, dest_path):
        """
        General Purpose: Choose a directory for intermediate files on the same
        filesystem as dest when possible (USB-safe). Falls back to system temp.
        """
        dest_path = Path(dest_path)
        parent = dest_path.parent
        try:
            if parent.is_dir() and os.access(str(parent), os.W_OK):
                return parent
        except OSError:
            pass
        return Path(tempfile.gettempdir())

    def make_temp_path(self, suffix, near_path):
        """
        General Purpose: Create a unique empty temp near near_path.
        The status line names the path before the file is created.
        """
        folder = self.staging_dir_for(near_path)
        last_error = None
        for _attempt in range(16):
            candidate = folder / "videojoin_{0}{1}".format(uuid.uuid4().hex, suffix)
            self._info("write temp path={0}".format(candidate))
            try:
                fd = os.open(
                    str(candidate),
                    os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                    0o600,
                )
            except FileExistsError as exc:
                last_error = exc
                continue
            os.close(fd)
            return candidate
        raise OSError("could not create a unique temp in {0}: {1}".format(folder, last_error))

    def promote_file(self, src, dest):
        """
        General Purpose: Publish src → dest using shutil.move (stdlib cross-FS safe).

        Same mount: rename. Different mount (USB, etc.): copy then remove source.
        Never use bare os.replace alone when src may live under system TMPDIR.
        The status line is written before shutil.move.
        """
        src = Path(src)
        dest = Path(dest)
        if not src.is_file():
            raise FileNotFoundError("promote source missing: {0}".format(src))
        if dest.is_dir():
            raise IsADirectoryError(
                "promote dest must be a file path, not a directory: {0}".format(dest)
            )
        dest.parent.mkdir(parents=True, exist_ok=True)
        self._info("publish src={0} dest={1}".format(src, dest))
        shutil.move(str(src), str(dest))

    def create_file_list(self, file1, file2, list_path):
        """
        General Purpose: Write the FFmpeg concat demuxer list with absolute POSIX paths.
        """
        p1 = Path(file1).resolve().as_posix()
        p2 = Path(file2).resolve().as_posix()
        with open(str(list_path), "w", encoding="utf-8") as handle:
            handle.write("file '{0}'\n".format(p1))
            handle.write("file '{0}'\n".format(p2))

    def _file_ok(self, path):
        """General Purpose: True if path is a non-empty regular file."""
        try:
            item = Path(path)
            return item.is_file() and item.stat().st_size > 0
        except OSError:
            return False

    def _run_ffmpeg(self, cmd):
        """
        General Purpose: Run one FFmpeg command. Return True on exit 0.
        Does not modify the source media paths. Captures output so the screen stays intact.
        """
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
        )
        if result.returncode != 0:
            err = (result.stderr or result.stdout or "").strip()
            tail = ""
            if err:
                clip = err[-500:] if len(err) > 500 else err
                tail = clip.splitlines()[-1] if clip else "failed"
            return False, tail or "failed"
        return True, ""

    def _discard(self, path):
        """Drop one unfinished temp. The status line is written before the unlink."""
        if path is None:
            return
        item = Path(path)
        if not item.exists():
            return
        self._info("discard path={0}".format(item))
        try:
            os.unlink(str(item))
        except OSError:
            pass

    def run(self, vid1, vid2, out_path):
        """
        General Purpose: Concatenate two videos to out_path (copy then re-encode).
        Stages unique temps near out_path and publishes with shutil.move.
        Returns (ok, lines). Leaves the sources intact.
        """
        vid1 = Path(vid1)
        vid2 = Path(vid2)
        out_path = Path(out_path)
        lines = []

        if not vid1.is_file() or not vid2.is_file():
            message = "ERROR: one or both input videos are missing."
            self._error(message)
            return False, [message]

        try:
            if out_path.resolve() in (vid1.resolve(), vid2.resolve()):
                message = "ERROR: output path must not be one of the source files."
                self._error(message)
                return False, [message]
        except OSError:
            pass

        list_path = None
        copy_temp = None
        reenc_temp = None
        try:
            list_path = self.make_temp_path(".txt", out_path)
            copy_temp = self.make_temp_path(".mp4", out_path)
            self.create_file_list(vid1, vid2, list_path)

            cmd_copy = [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(list_path),
                "-c",
                "copy",
                "-map",
                "0:v",
                "-map",
                "0:a?",
                str(copy_temp),
            ]
            lines.append("Running ffmpeg (stream copy – no quality loss)…")
            self._info("stream copy src={0} and {1}".format(vid1, vid2))
            copied, copy_err = self._run_ffmpeg(cmd_copy)
            if copied and self._file_ok(copy_temp):
                self.promote_file(copy_temp, out_path)
                copy_temp = None
                lines.append("SUCCESS! Perfectly joined with original sound → {0}".format(out_path))
                return True, lines

            lines.append(
                "Fast method failed (different resolutions/codec?). Trying safe re-encode..."
            )
            if copy_err:
                lines.append("   ffmpeg: {0}".format(copy_err))
            reenc_temp = self.make_temp_path(".mp4", out_path)
            cmd_reenc = [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(vid1),
                "-i",
                str(vid2),
                "-filter_complex",
                "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]",
                "-c:v",
                "libx264",
                "-preset",
                "fast",
                "-crf",
                "18",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-map",
                "[v]",
                "-map",
                "[a]",
                str(reenc_temp),
            ]
            lines.append("Running ffmpeg (re-encode fallback)…")
            self._info("re-encode src={0} and {1}".format(vid1, vid2))
            encoded, enc_err = self._run_ffmpeg(cmd_reenc)
            if encoded and self._file_ok(reenc_temp):
                self.promote_file(reenc_temp, out_path)
                reenc_temp = None
                lines.append("Done (with re-encode) → {0}".format(out_path))
                return True, lines

            message = "ERROR: join failed on both stream-copy and re-encode paths."
            self._error(message)
            lines.append(message)
            if enc_err:
                lines.append("   ffmpeg: {0}".format(enc_err))
            return False, lines
        except (OSError, FileNotFoundError, IsADirectoryError) as exc:
            message = "Job failed: {0}".format(exc)
            self._error(message)
            lines.append(message)
            err = getattr(exc, "errno", None)
            if err in (getattr(os, "EXDEV", 18), 18):
                lines.append(
                    "   Hint: cross-filesystem publish failed. "
                    "Temps stage next to the output; publish uses shutil.move."
                )
            return False, lines
        finally:
            self._discard(list_path)
            self._discard(copy_temp)
            self._discard(reenc_temp)

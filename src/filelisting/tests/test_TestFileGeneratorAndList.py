import os
import tempfile
import unittest
from typing import *
from unittest.mock import patch

import filelisting.core

__all__ = ["TestFileGeneratorAndList"]


class TestFileGeneratorAndList(unittest.TestCase):
    def test_file_generator_walks_directory_tree(self: Self) -> None:
        file_a: Any
        file_b: Any
        files: Any
        subdir: Any
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = os.path.join(tmpdir, "sub")
            os.makedirs(subdir)

            file_a = os.path.join(tmpdir, "a.txt")
            file_b = os.path.join(subdir, "b.txt")

            with open(file_a, "w", encoding="utf-8") as fh:
                fh.write("A")
            with open(file_b, "w", encoding="utf-8") as fh:
                fh.write("B")

            files = sorted(filelisting.core.file_generator(tmpdir))
            self.assertEqual(sorted(files), sorted([file_a, file_b]))

    def test_file_generator_accepts_single_file_path(self: Self) -> None:
        file_path: Any
        files: Any
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "single.txt")
            with open(file_path, "w", encoding="utf-8") as fh:
                fh.write("X")

            files = list(filelisting.core.file_generator(file_path))
            self.assertEqual(files, [file_path])

    def test_file_generator_expands_user_and_env(self: Self) -> None:
        env_dir: Any
        file_path: Any
        files: Any
        given: Any
        with tempfile.TemporaryDirectory() as tmpdir:
            # Put file under a directory referenced via env var
            env_dir = os.path.join(tmpdir, "envdir")
            os.makedirs(env_dir)

            file_path = os.path.join(env_dir, "file.txt")
            with open(file_path, "w", encoding="utf-8") as fh:
                fh.write("env")

            # Set environment variable to env_dir
            os.environ["MY_TEST_DIR"] = env_dir

            # Use env var and tilde (~) in the path; we only really
            # care that expanduser and expandvars are used in order.
            # So we patch expanduser/expandvars to check the calls.
            with (
                patch("filelisting.core.os.path.expanduser") as mock_user,
                patch("filelisting.core.os.path.expandvars") as mock_vars,
            ):

                # expanduser should just pass through, expandvars returns real path
                mock_user.side_effect = lambda p: p  # no-op
                mock_vars.side_effect = lambda p: p.replace("$MY_TEST_DIR", env_dir)

                given = "$MY_TEST_DIR"
                files = list(filelisting.core.file_generator(given))

                mock_user.assert_called_once_with(given)
                mock_vars.assert_called_once_with(given)
                self.assertEqual(files, [file_path])

    def test_file_list_wraps_file_generator(self: Self) -> None:
        result: Any
        with patch.object(filelisting.core, "file_generator") as mock_gen:
            mock_gen.return_value = iter(["a", "b", "c"])
            result = filelisting.core.file_list("x", "y")
            self.assertEqual(result, ["a", "b", "c"])
            mock_gen.assert_called_once_with("x", "y")


if __name__ == "__main__":
    unittest.main()

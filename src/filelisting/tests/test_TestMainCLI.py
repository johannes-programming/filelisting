import unittest
from typing import *
from unittest.mock import patch

from click.testing import CliRunner

import filelisting.core

__all__ = ["TestMainCLI"]


class TestMainCLI(unittest.TestCase):
    def setUp(self: Self) -> None:
        self.runner = CliRunner()

    @patch.object(filelisting.core, "file_list")
    def test_main_lists_files_to_stdout(self, mock_file_list) -> None:
        result: Any
        mock_file_list.return_value = ["/tmp/a", "/tmp/b"]
        result = self.runner.invoke(filelisting.core.main, ["path1", "path2"])
        self.assertEqual(result.exit_code, 0)
        # Each file on its own line
        self.assertEqual(result.output.strip().splitlines(), ["/tmp/a", "/tmp/b"])
        mock_file_list.assert_called_once_with("path1", "path2")

    def test_main_help_option(self: Self) -> None:
        result: Any
        result = self.runner.invoke(filelisting.core.main, ["-h"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("This command lists files under given paths.", result.output)

    def test_main_version_option(self: Self) -> None:
        result: Any
        result = self.runner.invoke(filelisting.core.main, ["-V"])
        # Version is None, but Click still prints a version header
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(result.output.strip())  # something printed

    def test_main_no_paths_is_allowed(self: Self) -> None:
        result: Any
        # With no paths, file_list gets called with no args
        with patch.object(
            filelisting.core, "file_list", return_value=[]
        ) as mock_file_list:
            result = self.runner.invoke(filelisting.core.main, [])
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.output, "")
            mock_file_list.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()

import unittest
from io import StringIO
from unittest.mock import patch

from entralab.cli import main


class CliTests(unittest.TestCase):
    def test_list_rules_command(self) -> None:
        with patch("sys.stdout", new_callable=StringIO) as stdout:
            code = main(["list-rules"])
        self.assertEqual(code, 0)
        self.assertIn("ENTRA-001", stdout.getvalue())
        self.assertIn("ENTRA-006", stdout.getvalue())

    def test_explain_command(self) -> None:
        with patch("sys.stdout", new_callable=StringIO) as stdout:
            code = main(["explain", "ENTRA-003"])
        self.assertEqual(code, 0)
        self.assertIn("MFA Denied", stdout.getvalue())

    def test_all_command(self) -> None:
        with patch("sys.stdout", new_callable=StringIO) as stdout:
            code = main(["all"])
        self.assertEqual(code, 0)
        self.assertIn("Repository audit: OK", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()

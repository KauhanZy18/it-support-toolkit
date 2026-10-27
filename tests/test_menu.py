import unittest
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

from src.__main__ import _ler_porta, main


class MenuTests(unittest.TestCase):
    @patch("builtins.input", side_effect=["0"])
    def test_menu_exits_cleanly(self, mocked_input):
        with redirect_stdout(StringIO()) as output:
            main()
        self.assertIn("Encerrando", output.getvalue())

    @patch("builtins.input", side_effect=["x", "0"])
    def test_menu_handles_invalid_option(self, mocked_input):
        with redirect_stdout(StringIO()) as output:
            main()
        self.assertIn("Opção inválida", output.getvalue())

    @patch("builtins.input", return_value="443")
    def test_reads_valid_port(self, mocked_input):
        self.assertEqual(_ler_porta(), 443)

    @patch("builtins.input", return_value="70000")
    def test_rejects_out_of_range_port(self, mocked_input):
        with self.assertRaises(ValueError):
            _ler_porta()


if __name__ == "__main__":
    unittest.main()

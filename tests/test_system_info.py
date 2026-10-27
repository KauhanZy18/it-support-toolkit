import unittest
from unittest.mock import patch

from src.system_info import coletar_informacoes_sistema


class SystemInfoTests(unittest.TestCase):
    def test_returns_expected_keys(self):
        result = coletar_informacoes_sistema()
        self.assertIn("hostname", result)
        self.assertIn("sistema_operacional", result)
        self.assertIn("arquitetura", result)
        self.assertIn("disco_total_gb", result)
        self.assertIn("disco_livre_gb", result)

    @patch("src.system_info.socket.gethostbyname", side_effect=OSError("DNS unavailable"))
    def test_handles_ip_lookup_failure(self, resolver):
        result = coletar_informacoes_sistema()
        self.assertEqual(result["endereco_ip"], "Não disponível")


if __name__ == "__main__":
    unittest.main()

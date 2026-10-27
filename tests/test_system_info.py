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
        self.assertIn("memoria_total_gb", result)
        self.assertIn("memoria_disponivel_gb", result)
        self.assertIn("memoria_usada_gb", result)
        self.assertIn("memoria_percentual_usado", result)

    @patch("src.system_info.socket.gethostbyname", side_effect=OSError("DNS unavailable"))
    def test_handles_ip_lookup_failure(self, resolver):
        result = coletar_informacoes_sistema()
        self.assertEqual(result["endereco_ip"], "Não disponível")

    @patch("src.system_info._coletar_memoria_bytes", return_value=(16 * 1024**3, 6 * 1024**3))
    def test_calculates_memory_metrics(self, memory_reader):
        result = coletar_informacoes_sistema()
        self.assertEqual(result["memoria_total_gb"], 16.0)
        self.assertEqual(result["memoria_disponivel_gb"], 6.0)
        self.assertEqual(result["memoria_usada_gb"], 10.0)
        self.assertEqual(result["memoria_percentual_usado"], 62.5)
        self.assertIn("62.5% usado", result["memoria"])

    @patch("src.system_info._coletar_memoria_bytes", return_value=None)
    def test_gracefully_handles_unavailable_memory_metrics(self, memory_reader):
        result = coletar_informacoes_sistema()
        self.assertIsNone(result["memoria_total_gb"])
        self.assertIsNone(result["memoria_percentual_usado"])
        self.assertIn("Não disponível", result["memoria"])


if __name__ == "__main__":
    unittest.main()

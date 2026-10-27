import unittest
from unittest.mock import patch
import socket

from src.network_checks import verificar_dns, verificar_tcp, verificar_ping
from src.utils import validate_host, validate_port


class NetworkChecksTests(unittest.TestCase):
    @patch("src.network_checks.socket.gethostbyname", return_value="93.184.216.34")
    def test_dns_success(self, resolver):
        result = verificar_dns("example.com")
        self.assertTrue(result.sucesso)
        self.assertEqual(result.ip_resolvido, "93.184.216.34")

    @patch("src.network_checks.socket.gethostbyname", side_effect=socket.gaierror("not found"))
    def test_dns_failure(self, resolver):
        result = verificar_dns("invalid.invalid")
        self.assertFalse(result.sucesso)
        self.assertIsNotNone(result.erro)

    def test_tcp_invalid_port(self):
        result = verificar_tcp("localhost", 70000)
        self.assertFalse(result.conectado)
        self.assertIn("Porta inválida", result.erro)

    def test_tcp_port_boundaries(self):
        self.assertFalse(verificar_tcp("localhost", 0).conectado)
        self.assertFalse(verificar_tcp("localhost", 65536).conectado)

    def test_host_validation(self):
        self.assertTrue(validate_host("192.168.1.1"))
        self.assertTrue(validate_host("example.com"))
        self.assertFalse(validate_host(""))
        self.assertFalse(validate_host("999.1.1.1"))

    def test_port_validation(self):
        self.assertTrue(validate_port(80))
        self.assertTrue(validate_port("443"))
        self.assertFalse(validate_port(0))
        self.assertFalse(validate_port(70000))
        self.assertFalse(validate_port("bad"))

    @patch("src.network_checks.socket.gethostbyname", return_value="93.184.216.34")
    @patch("src.network_checks.socket.create_connection")
    def test_tcp_reachability_success(self, connect, resolver):
        class FakeSocket:
            def __enter__(self): return self
            def __exit__(self, *args): return False
        connect.return_value = FakeSocket()
        result = verificar_ping("example.com")
        self.assertTrue(result.alcancaivel)
        self.assertEqual(result.ip_resolvido, "93.184.216.34")

    def test_ping_rejects_zero_attempts(self):
        result = verificar_ping("example.com", count=0)
        self.assertFalse(result.alcancaivel)
        self.assertIsNotNone(result.erro)


if __name__ == "__main__":
    unittest.main()

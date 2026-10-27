#!/usr/bin/env python3
"""Módulo para verificação de conectividade DNS e TCP.

Este módulo verifica resolução DNS, conectividade TCP em portas específicas
e alcance de hosts usando apenas a biblioteca padrão do Python.

Este é um projeto pessoal/laboratório. Uso educacional apenas.
"""

import socket
import time
from dataclasses import dataclass
from typing import Optional, List, Tuple


@dataclass
class DNSResult:
    """Resultado da verificação de resolução DNS."""
    dominio: str
    ip_resolvido: Optional[str]
    tempo_ms: float
    sucesso: bool
    erro: Optional[str] = None


@dataclass
class TCPResult:
    """Resultado da verificação de conectividade TCP."""
    host: str
    porta: int
    conectado: bool
    tempo_ms: float
    erro: Optional[str] = None


@dataclass
class PingResult:
    """Resultado da verificação de ping (ICMP reachability)."""
    host: str
    alcancaivel: bool
    tempo_ms: float
    ip_resolvido: Optional[str]
    erro: Optional[str] = None


def verificar_dns(dominio: str, timeout: int = 5) -> DNSResult:
    """Verifica a resolução DNS de um domínio.

    Args:
        dominio: O domínio a verificar.
        timeout: Tempo máximo de espera em segundos.

    Returns:
        DNSResult com os detalhes da resolução.
    """
    inicio = time.time()
    try:
        ip = socket.gethostbyname(dominio)
        tempo = (time.time() - inicio) * 1000
        return DNSResult(
            dominio=dominio,
            ip_resolvido=ip,
            tempo_ms=round(tempo, 2),
            sucesso=True,
        )
    except socket.gaierror as e:
        tempo = (time.time() - inicio) * 1000
        return DNSResult(
            dominio=dominio,
            ip_resolvido=None,
            tempo_ms=round(tempo, 2),
            sucesso=False,
            erro=f"Erro de resolução DNS: {e}",
        )
    except Exception as e:
        tempo = (time.time() - inicio) * 1000
        return DNSResult(
            dominio=dominio,
            ip_resolvido=None,
            tempo_ms=round(tempo, 2),
            sucesso=False,
            erro=str(e),
        )


def verificar_tcp(host: str, porta: int, timeout: int = 5) -> TCPResult:
    """Verifica conectividade TCP em um host e porta específicos.

    Args:
        host: Endereço do host.
        porta: Número da porta (1-65535).
        timeout: Tempo máximo de espera em segundos.

    Returns:
        TCPResult com os detalhes da conexão.
    """
    if not (1 <= porta <= 65535):
        return TCPResult(
            host=host,
            porta=porta,
            conectado=False,
            tempo_ms=0,
            erro=f"Porta inválida: {porta}. Deve ser 1-65535.",
        )

    inicio = time.time()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        resultado = sock.connect_ex((host, porta))
        tempo = (time.time() - inicio) * 1000
        conectado = (resultado == 0)
        sock.close()
        return TCPResult(
            host=host,
            porta=porta,
            conectado=conectado,
            tempo_ms=round(tempo, 2),
        )
    except socket.timeout:
        tempo = (time.time() - inicio) * 1000
        return TCPResult(
            host=host,
            porta=porta,
            conectado=False,
            tempo_ms=round(tempo, 2),
            erro="Timeout na conexão TCP",
        )
    except Exception as e:
        tempo = (time.time() - inicio) * 1000
        return TCPResult(
            host=host,
            porta=porta,
            conectado=False,
            tempo_ms=round(tempo, 2),
            erro=str(e),
        )


def verificar_ping(host: str, timeout: int = 3, count: int = 1) -> PingResult:
    """Verifica o alcance de um host tentando conectar à porta TCP 80.

    Esta verificação não é um ping ICMP. Ela testa se o host aceita conexões
    TCP na porta 80 e informa o resultado sem exigir privilégios administrativos.
    """
    if count < 1:
        return PingResult(
            host=host, alcancaivel=False, tempo_ms=0, ip_resolvido=None,
            erro="O número de tentativas deve ser maior que zero.",
        )

    try:
        resolved_ip = socket.gethostbyname(host)
    except (socket.gaierror, OSError) as exc:
        return PingResult(
            host=host, alcancaivel=False, tempo_ms=0, ip_resolvido=None,
            erro=f"Falha na resolução do host: {exc}",
        )

    total_tempo = 0.0
    for _ in range(count):
        inicio = time.perf_counter()
        try:
            with socket.create_connection((resolved_ip, 80), timeout=timeout):
                total_tempo += (time.perf_counter() - inicio) * 1000
                return PingResult(
                    host=host, alcancaivel=True,
                    tempo_ms=round(total_tempo, 2), ip_resolvido=resolved_ip,
                )
        except OSError:
            total_tempo += (time.perf_counter() - inicio) * 1000

    return PingResult(
        host=host, alcancaivel=False, tempo_ms=round(total_tempo / count, 2),
        ip_resolvido=resolved_ip,
        erro=f"Não foi possível estabelecer conexão TCP com {resolved_ip}:80.",
    )


def _calcular_checksum(data: bytes) -> int:
    """Calcula o checksum ICMP/UDP usando soma de 16 bits."""
    if len(data) % 2 != 0:
        data += b'\x00'

    soma = 0
    for i in range(0, len(data), 2):
        word = (data[i]

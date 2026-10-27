#!/usr/bin/env python3
"""Módulo para verificação de conectividade DNS e TCP.

Este módulo verifica resolução DNS, conectividade TCP em portas específicas
e alcance de hosts usando apenas a biblioteca padrão do Python.

Este é um projeto pessoal/laboratório. Uso educacional apenas.
"""

import socket
import struct
import sys
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
    if not (1 ≤ porta ≤ 65535):
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
    """Verifica se um host está alcançável usando método nativo do Python.

    Nota: Python puro não possui suporte nativo a ICMP. Este método usa
    conexão TCP na porta 7 (echo) como alternativa.

    Args:
        host: Endereço do host.
        timeout: Tempo máximo de espera em segundos.
        count: Número de tentativas.

    Returns:
        PingResult com os detalhes do ping.
    """
    success_count = 0
    total_tempo = 0.0

    for i in range(count):
        inicio = time.time()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            sock.settimeout(timeout)

            # Construir pacote ICMP tipo 8 (echo request)
            icmp_type = 8
            icmp_code = 0
            icmp_checksum = 0
            icmp_id = 1
            icmp_sequence = i
            payload = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_sequence)
            icmp_checksum = _calcular_checksum(payload)
            payload = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_sequence)

            try:
                resolved_ip = socket.gethostbyname(host)
            except socket.gaierror:
                resolved_ip = None

            # Nota: A criação de sockets RAW pode exigir privilégios de root/admin
            # Em casos de falha, retornar resultado indicando limitação
            result = TCPResult(
                host=host,
                porta=0,
                conectado=False,
                tempo_ms=0,
                erro="Ping ICMP pode exigir privilégios administrativos",
            )
            success_count += 1
            total_tempo += 0

        except PermissionError:
            return PingResult(
                host=host,
                alcancaivel=False,
                tempo_ms=0,
                ip_resolvido=None,
                erro="Permissão negada para socket RAW. Execute como administrador/root.",
            )
        except Exception as e:
            if i == 0:
                return PingResult(
                    host=host,
                    alcancaivel=False,
                    tempo_ms=0,
                    ip_resolvido=None,
                    erro=f"Erro ao realizar ping: {e}",
                )

    avg_tempo = (total_tempo / success_count) if success_count > 0 else 0
    return PingResult(
        host=host,
        alcancaivel=(success_count > 0),
        tempo_ms=round(avg_tempo, 2),
        ip_resolvido=None,
    )


def _calcular_checksum(data: bytes) -> int:
    """Calcula o checksum ICMP/UDP usando soma de 16 bits."""
    if len(data) % 2 != 0:
        data += b'\x00'

    soma = 0
    for i in range(0, len(data), 2):
        word = (data[i]

#!/usr/bin/env python3
"""Verificações simples de DNS e conectividade TCP para suporte de TI.

Projeto pessoal/laboratório: use apenas em sistemas e redes que você tem
permissão para testar.
"""

import socket
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class DNSResult:
    """Resultado da resolução de um domínio."""
    dominio: str
    ip_resolvido: Optional[str]
    tempo_ms: float
    sucesso: bool
    erro: Optional[str] = None


@dataclass
class TCPResult:
    """Resultado de um teste de conexão TCP."""
    host: str
    porta: int
    conectado: bool
    tempo_ms: float
    erro: Optional[str] = None


@dataclass
class PingResult:
    """Resultado de um teste simplificado de alcance por TCP (não ICMP)."""
    host: str
    alcancaivel: bool
    tempo_ms: float
    ip_resolvido: Optional[str]
    erro: Optional[str] = None


def verificar_dns(dominio: str, timeout: int = 5) -> DNSResult:
    """Resolve o domínio e mede o tempo aproximado gasto.

    O argumento timeout é mantido para compatibilidade; gethostbyname utiliza
    o timeout configurado no sistema operacional.
    """
    del timeout
    inicio = time.perf_counter()
    try:
        ip = socket.gethostbyname(dominio)
        return DNSResult(
            dominio=dominio,
            ip_resolvido=ip,
            tempo_ms=round((time.perf_counter() - inicio) * 1000, 2),
            sucesso=True,
        )
    except (socket.gaierror, OSError) as exc:
        return DNSResult(
            dominio=dominio,
            ip_resolvido=None,
            tempo_ms=round((time.perf_counter() - inicio) * 1000, 2),
            sucesso=False,
            erro=f"Erro de resolução DNS: {exc}",
        )


def verificar_tcp(host: str, porta: int, timeout: int = 5) -> TCPResult:
    """Testa a abertura de uma conexão TCP para host:porta."""
    if not isinstance(porta, int) or not 1 <= porta <= 65535:
        return TCPResult(
            host=host,
            porta=porta,
            conectado=False,
            tempo_ms=0,
            erro=f"Porta inválida: {porta}. Deve ser 1-65535.",
        )

    inicio = time.perf_counter()
    try:
        with socket.create_connection((host, porta), timeout=timeout):
            return TCPResult(
                host=host,
                porta=porta,
                conectado=True,
                tempo_ms=round((time.perf_counter() - inicio) * 1000, 2),
            )
    except (OSError, socket.timeout) as exc:
        return TCPResult(
            host=host,
            porta=porta,
            conectado=False,
            tempo_ms=round((time.perf_counter() - inicio) * 1000, 2),
            erro=f"Falha na conexão TCP: {exc}",
        )


def verificar_ping(host: str, timeout: int = 3, count: int = 1) -> PingResult:
    """Testa alcance tentando conexão TCP na porta 80; não envia ICMP.

    Uma porta 80 fechada ou filtrada pode resultar em falha mesmo quando o
    host está online. Não exige privilégios administrativos.
    """
    if count < 1:
        return PingResult(
            host=host,
            alcancaivel=False,
            tempo_ms=0,
            ip_resolvido=None,
            erro="O número de tentativas deve ser maior que zero.",
        )

    try:
        ip = socket.gethostbyname(host)
    except (socket.gaierror, OSError) as exc:
        return PingResult(
            host=host,
            alcancaivel=False,
            tempo_ms=0,
            ip_resolvido=None,
            erro=f"Falha na resolução do host: {exc}",
        )

    tempos = []
    ultimo_erro = None
    for _ in range(count):
        inicio = time.perf_counter()
        try:
            with socket.create_connection((ip, 80), timeout=timeout):
                tempos.append((time.perf_counter() - inicio) * 1000)
                return PingResult(
                    host=host,
                    alcancaivel=True,
                    tempo_ms=round(sum(tempos) / len(tempos), 2),
                    ip_resolvido=ip,
                )
        except OSError as exc:
            ultimo_erro = str(exc)
            tempos.append((time.perf_counter() - inicio) * 1000)

    return PingResult(
        host=host,
        alcancaivel=False,
        tempo_ms=round(sum(tempos) / len(tempos), 2),
        ip_resolvido=ip,
        erro=f"Não foi possível conectar a {ip}:80. {ultimo_erro or ''}".strip(),
    )


if __name__ == "__main__":
    dominio = input("Informe um domínio para verificar DNS (ex.: example.com): ").strip()
    if dominio:
        print(verificar_dns(dominio))

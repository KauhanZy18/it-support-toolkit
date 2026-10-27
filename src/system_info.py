#!/usr/bin/env python3
"""Coleta informações básicas do sistema para diagnóstico de suporte de TI."""

import ctypes
import os
import platform
import shutil
import socket
from pathlib import Path
from typing import Any


def _coletar_memoria_bytes() -> tuple[int, int] | None:
    """Retorna (memória física total, memória disponível) em bytes.

    Suporta Windows por meio da API GlobalMemoryStatusEx e Linux por
    /proc/meminfo. Em sistemas não suportados ou quando a leitura falha,
    retorna None em vez de inventar valores.
    """
    sistema = platform.system()

    if sistema == "Windows":
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        try:
            memory_status = MEMORYSTATUSEX()
            memory_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            if not kernel32.GlobalMemoryStatusEx(ctypes.byref(memory_status)):
                return None
            return int(memory_status.ullTotalPhys), int(memory_status.ullAvailPhys)
        except (OSError, AttributeError, ctypes.ArgumentError):
            return None

    if sistema == "Linux":
        try:
            valores: dict[str, int] = {}
            for linha in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
                partes = linha.split()
                if len(partes) >= 2 and partes[0].rstrip(":") in {
                    "MemTotal", "MemAvailable", "MemFree", "Buffers", "Cached"
                }:
                    valores[partes[0].rstrip(":")] = int(partes[1]) * 1024

            total = valores.get("MemTotal")
            disponivel = valores.get("MemAvailable")
            if disponivel is None:
                disponivel = (
                    valores.get("MemFree", 0)
                    + valores.get("Buffers", 0)
                    + valores.get("Cached", 0)
                )
            if total is not None and total > 0:
                return total, min(max(disponivel, 0), total)
        except (OSError, ValueError):
            return None

    return None


def coletar_informacoes_sistema() -> dict[str, Any]:
    """Retorna informações básicas do host, SO, memória e disco disponível."""
    informacoes: dict[str, Any] = {
        "hostname": socket.gethostname(),
        "sistema_operacional": platform.platform(),
        "arquitetura": platform.machine(),
        "processador": platform.processor() or "Não informado",
        "diretorio_atual": os.getcwd(),
    }

    try:
        informacoes["endereco_ip"] = socket.gethostbyname(socket.gethostname())
    except OSError:
        informacoes["endereco_ip"] = "Não disponível"

    try:
        uso_disco = shutil.disk_usage(os.getcwd())
        informacoes["disco_total_gb"] = round(uso_disco.total / (1024 ** 3), 2)
        informacoes["disco_livre_gb"] = round(uso_disco.free / (1024 ** 3), 2)
    except OSError:
        informacoes["disco_total_gb"] = None
        informacoes["disco_livre_gb"] = None

    memoria = _coletar_memoria_bytes()
    if memoria is not None:
        total_bytes, disponivel_bytes = memoria
        usada_bytes = max(total_bytes - disponivel_bytes, 0)
        percentual_usado = round((usada_bytes / total_bytes) * 100, 1) if total_bytes else 0.0
        gib = 1024 ** 3
        informacoes["memoria_total_gb"] = round(total_bytes / gib, 2)
        informacoes["memoria_disponivel_gb"] = round(disponivel_bytes / gib, 2)
        informacoes["memoria_usada_gb"] = round(usada_bytes / gib, 2)
        informacoes["memoria_percentual_usado"] = percentual_usado
        informacoes["memoria"] = (
            f'{informacoes["memoria_usada_gb"]} GB usados de '
            f'{informacoes["memoria_total_gb"]} GB ({percentual_usado}% usado)'
        )
    else:
        informacoes["memoria_total_gb"] = None
        informacoes["memoria_disponivel_gb"] = None
        informacoes["memoria_usada_gb"] = None
        informacoes["memoria_percentual_usado"] = None
        informacoes["memoria"] = "Não disponível nesta plataforma ou houve falha na consulta."

    return informacoes


def main() -> None:
    """Exibe informações resumidas do sistema."""
    print("=== Informações do sistema ===")
    for chave, valor in coletar_informacoes_sistema().items():
        print(f"{chave.replace('_', ' ').capitalize()}: {valor}")


if __name__ == "__main__":
    main()

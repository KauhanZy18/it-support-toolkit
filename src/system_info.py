#!/usr/bin/env python3
"""Coleta informações básicas do sistema para diagnóstico de suporte de TI."""

import os
import platform
import shutil
import socket
from typing import Any


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

    # Uso de disco do diretório atual é suportado pela biblioteca padrão.
    try:
        uso_disco = shutil.disk_usage(os.getcwd())
        informacoes["disco_total_gb"] = round(uso_disco.total / (1024 ** 3), 2)
        informacoes["disco_livre_gb"] = round(uso_disco.free / (1024 ** 3), 2)
    except OSError:
        informacoes["disco_total_gb"] = None
        informacoes["disco_livre_gb"] = None

    # Informações de memória variam por plataforma; não fingir suporte universal.
    informacoes["memoria"] = "Não coletada (API da biblioteca padrão varia por sistema)"
    return informacoes


def main() -> None:
    """Exibe informações resumidas do sistema."""
    print("=== Informações do sistema ===")
    for chave, valor in coletar_informacoes_sistema().items():
        print(f"{chave.replace('_', ' ').capitalize()}: {valor}")


if __name__ == "__main__":
    main()

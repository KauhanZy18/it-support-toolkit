#!/usr/bin/env python3
"""Utilitários de saída, logging e validação.

Este módulo fornece funções auxiliares para formatar e exibir saída
de forma legível, além de utilitários de validação de dados.

Este é um projeto pessoal/laboratório. Uso educacional apenas.
"""

import sys
from typing import Any, Dict, Optional


def format_result(label: str, value: Any, indent: int = 4) -> str:
    """Formata um par chave-valor para exibição.

    Args:
        label: Nome do campo.
        value: Valor do campo.
        indent: Indentação em espaços.

    Returns:
        String formatada.
    """
    prefix = " " * indent
    value_str = str(value) if value is not None else "N/A"
    return f"{prefix}{label}: {value_str}"


def print_header(title: str, width: int = 60) -> None:
    """Exibe um cabeçalho formatado.

    Args:
        title: Título do cabeçalho.
        width: Largura da barra de separação.
    """
    print("=" * width)
    print(f" {title}")
    print("=" * width)


def print_section(title: str) -> None:
    """Exibe um subtítulo de seção.

    Args:
        title: Título da seção.
    """
    print(f"\n--- {title} ---")


def print_dict(data: Dict[str, Any], indent: int = 4) -> None:
    """Exibe um dicionário formatado.

    Args:
        data: Dicionário para exibir.
        indent: Indentação em espaços.
    """
    if not data:
        print(" " * indent + "(sem dados)")
        return
    for key, value in data.items():
        print(f"{' ' * indent}{key}: {value}")


def validate_host(host: str) -> bool:
    """Valida se um host é um formato válido (IP ou domínio).

    Args:
        host: Host a validar.

    Returns:
        True se válido, False caso contrário.
    """
    if not host or not host.strip():
        return False
    # Verifica se é um IP válido (simplificado)
    parts = host.strip().split(".")
    if len(parts) == 4:
        try:
            return all(0 ≤ int(p) ≤ 255 for p in parts)
        except ValueError:
            return False
    # Verifica se é um domínio válido (simplificado)
    if "." in host:
        return True
    return False


def validate_port(port: int) -> bool:
    """Valida se uma porta está no intervalo válido.

    Args:
        port: Número da porta.

    Returns:
        True se entre 1 e 65535, False caso contrário.
    """
    try:
        return 1 ≤ int(port) ≤ 65535
    except (ValueError, TypeError):
        return False


def safe_input(prompt: str, valid_func=None) -> str:
    """Obtém entrada do usuário com validação opcional.

    Args:
        prompt: Mensagem de prompt para o usuário.
        valid_func: Função de validação opcional que recebe a entrada.

    Returns:
        Entrada válida do usuário.
    """
    while True:
        try:
            value = input(prompt).strip()
            if valid_func and not valid_func(value):
                print("Entrada inválida. Tente novamente.")
                continue
            return value
        except (EOFError, KeyboardInterrupt):
            print("\nOperação cancelada.")
            sys.exit(0)

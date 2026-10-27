"""Menu interativo do IT Support Toolkit.

Execute a partir da raiz do repositório com: python -m src
"""

import subprocess
import sys

from src.network_checks import verificar_dns, verificar_ping, verificar_tcp
from src.system_info import coletar_informacoes_sistema


def _ler_porta() -> int:
    """Lê e valida um número de porta TCP."""
    valor = input("Porta TCP (ex.: 443): ").strip()
    try:
        porta = int(valor)
    except ValueError as exc:
        raise ValueError("Digite a porta como número inteiro.") from exc
    if not 1 <= porta <= 65535:
        raise ValueError("A porta deve estar entre 1 e 65535.")
    return porta


def _pausar() -> None:
    input("\nPressione Enter para voltar ao menu...")


def main() -> None:
    """Exibe o menu e executa o diagnóstico selecionado."""
    while True:
        print("\n" + "=" * 48)
        print(" IT SUPPORT TOOLKIT")
        print("=" * 48)
        print("1. Ver informações do computador")
        print("2. Consultar DNS de um domínio")
        print("3. Testar conexão TCP em uma porta")
        print("4. Testar alcance TCP na porta 80")
        print("5. Executar testes automatizados")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "0":
            print("Encerrando o IT Support Toolkit.")
            return

        try:
            if opcao == "1":
                print("\n=== Informações do sistema ===")
                for chave, valor in coletar_informacoes_sistema().items():
                    print(f"{chave.replace('_', ' ').capitalize()}: {valor}")

            elif opcao == "2":
                dominio = input("Domínio (ex.: example.com): ").strip()
                if not dominio:
                    print("Informe um domínio.")
                else:
                    print(verificar_dns(dominio))

            elif opcao == "3":
                host = input("Host ou domínio (ex.: example.com): ").strip()
                if not host:
                    print("Informe um host ou domínio.")
                else:
                    porta = _ler_porta()
                    print(verificar_tcp(host, porta, timeout=5))

            elif opcao == "4":
                host = input("Host ou domínio (ex.: example.com): ").strip()
                if not host:
                    print("Informe um host ou domínio.")
                else:
                    print(verificar_ping(host, timeout=5, count=2))
                    print("Observação: esse teste usa TCP na porta 80, não ICMP.")

            elif opcao == "5":
                print("\nExecutando testes automatizados...\n")
                resultado = subprocess.run(
                    [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
                    check=False,
                )
                if resultado.returncode == 0:
                    print("\nTodos os testes automatizados passaram.")
                else:
                    print("\nAlguns testes falharam. Confira as mensagens acima.")

            else:
                print("Opção inválida. Escolha 0, 1, 2, 3, 4 ou 5.")

        except (ValueError, OSError) as exc:
            print(f"Não foi possível concluir a operação: {exc}")

        _pausar()


if __name__ == "__main__":
    main()

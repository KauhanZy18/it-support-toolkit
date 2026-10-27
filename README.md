# IT Support Toolkit

**Ferramentas de suporte de TI em Python para diagnóstico e coleta de informações do sistema.**

---

## 📋 Visão Geral / Overview

Kit de ferramentas Python para coleta de informações básicas do sistema, verificação de conectividade DNS e TCP, com saída legível e tratamento de erros.

Python toolkit for basic system information gathering, DNS connectivity verification, and TCP/host reachability checks with readable output and error handling.

---

## ⚠️ Aviso / Disclaimer

> **Projeto Pessoal / Laboratório / Personal Project / Laboratory Project**
>
> Este projeto é destinado apenas para fins educacionais e de laboratório. O uso em ambientes de produção é por sua conta e risco. Não afirmar que tudo foi testado em produção.
>
> This project is for educational and laboratory purposes only. Use in production environments is at your own risk. Not all functionality has been tested in production.

---

## 📁 Estrutura do Projeto / Project Structure

```
it-support-toolkit/
├── src/
│   ├── __init__.py
│   ├── system_info.py      # Coleta informações do sistema
│   ├── network_checks.py   # Verificações DNS e TCP
│   └── utils.py            # Utilitários de saída e logging
├── tests/
│   ├── __init__.py
│   ├── test_system_info.py # Testes unittest
│   └── test_network_checks.py # Testes unittest
├── README.md
└── requirements.txt         # vazio — sem dependências externas
```

---

## 🚀 Instruções de Execução / Execution Instructions

### Pré-requisitos / Prerequisites

- Python 3.10+
- Sem dependências externas (usa apenas biblioteca padrão)

### Executar / Run

```bash
# Executar todos os módulos
python -m src.system_info
python -m src.network_checks

# Executar testes
python -m pytest tests/ -v
# ou: python -m unittest discover -s tests -v
```

### Executar script único / Run single script

```bash
python src/system_info.py
python src/network_checks.py
```

---

## 📦 Dependências / Dependencies

```
# requirements.txt
# Nenhum / None
```

Nenhuma dependência externa. Apenas Python 3.10+ com biblioteca padrão.

---

## 📖 Módulos / Modules

### `src.system_info`

Coleta informações básicas do sistema:
- Nome do host
- Sistema operacional
- Endereço IP
- Arquitetura e processador
- Espaço total e disponível em disco
- Endereço IP (quando resolvível)
- Informações de disco

### `src.network_checks`

Verificações de conectividade:
- Resolução DNS para domínios
- Verificação de conectividade TCP em portas específicas
- Verificação de alcance TCP na porta 80 (não é ping ICMP)

---

## 🧪 Testes / Tests

Cada módulo possui testes `unittest` correspondentes em `tests/`.

```bash
python -m unittest discover -s tests -v
```

---

## 🚫 Limitações / Limitations

- Apenas biblioteca padrão — nenhuma instalação de pacotes adicionais necessária, mas funcionalidade limitada
- Scripts de sistema dependem do sistema operacional (resultados podem variar)
- Verificações de rede dependem de conectividade e configuração do firewall local
- Não realizar testes automatizados em ambientes de produção — uso apenas laboratorial

---

## 📝 Licença / License

Projeto pessoal / laboratório. Uso educacional.

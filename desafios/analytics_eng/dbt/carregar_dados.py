"""Carrega os CSVs da pasta data no banco loja.duckdb, no esquema raw.

Num projeto de verdade, uma ferramenta de ingestão traz os dados brutos dos sistemas da empresa
para o banco, e o dbt começa a partir daí. Aqui, este script faz esse papel.

Rode uma vez, dentro desta pasta, antes do primeiro dbt build:
    python carregar_dados.py
"""

import os
from pathlib import Path

import duckdb

PASTA = Path(__file__).resolve().parent
TABELAS = ("clientes", "pedidos", "itens_pedido")


def carregar(caminho_banco=None):
    caminho_banco = caminho_banco or os.environ.get("LOJA_DUCKDB", "loja.duckdb")
    # O formato v1.0.0 deixa o arquivo legível também pelo DuckDB que vem embutido no dbt v2
    with duckdb.connect(str(caminho_banco), config={"storage_compatibility_version": "v1.0.0"}) as conexao:
        conexao.execute("create schema if not exists raw")
        for tabela in TABELAS:
            arquivo = (PASTA / "data" / f"{tabela}.csv").as_posix()
            conexao.execute(f"create or replace table raw.{tabela} as select * from read_csv('{arquivo}')")
    return caminho_banco


if __name__ == "__main__":
    print(f"Dados brutos carregados no esquema raw de {carregar()}")

"""Gabarito do desafio "Uma camada semântica de bolso".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import json
from pathlib import Path

import duckdb

GRAOS = {"dia": "day", "semana": "week", "mes": "month", "trimestre": "quarter", "ano": "year"}


def ler_modelo(caminho):
    """Já está pronta: lê o modelo semântico do arquivo JSON."""
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def criar_banco(caminho_csv):
    """Já está pronta: carrega o CSV de pedidos numa tabela pedidos, num DuckDB em memória."""
    conexao = duckdb.connect()
    conexao.execute(f"create table pedidos as select * from read_csv('{Path(caminho_csv).as_posix()}')")
    return conexao


def consultar(conexao, modelo, metricas, por=(), grao=None, filtros=()):
    """Já está pronta: compila a consulta com a sua função compilar e devolve um DataFrame."""
    return conexao.execute(compilar(modelo, metricas, por, grao, filtros)).df()


def sql_da_medida(medida):
    agregacao = medida["agregacao"]
    if agregacao == "sum":
        return f"SUM({medida['coluna']})"
    if agregacao == "count":
        return "COUNT(*)"
    if agregacao == "count_distinct":
        return f"COUNT(DISTINCT {medida['coluna']})"
    raise ValueError(f"Agregação desconhecida: {agregacao}")


def sql_da_metrica(modelo, nome):
    if nome not in modelo["metricas"]:
        raise ValueError(f"Métrica desconhecida: {nome}")
    metrica = modelo["metricas"][nome]
    if metrica["tipo"] == "razao":
        numerador = sql_da_metrica(modelo, metrica["numerador"])
        denominador = sql_da_metrica(modelo, metrica["denominador"])
        # razão dos totais do grupo, e nunca a média de razões
        return f"CAST({numerador} AS DOUBLE) / NULLIF({denominador}, 0)"
    expressao = sql_da_medida(modelo["medidas"][metrica["medida"]])
    if metrica.get("filtro"):
        expressao += f" FILTER (WHERE {metrica['filtro']})"
    return expressao


def expressao_de_tempo(coluna, grao):
    if grao not in GRAOS:
        raise ValueError(f"Grão desconhecido: {grao}")
    return f"date_trunc('{GRAOS[grao]}', {coluna})"


def compilar(modelo, metricas, por=(), grao=None, filtros=()):
    if not metricas:
        raise ValueError("Peça pelo menos uma métrica.")
    for dimensao in por:
        if dimensao not in modelo["dimensoes"]:
            raise ValueError(f"Dimensão desconhecida: {dimensao}")

    grupos = []
    if grao is not None:
        grupos.append(f"{expressao_de_tempo(modelo['coluna_de_tempo'], grao)} AS {grao}")
    grupos += list(por)
    colunas = grupos + [f"{sql_da_metrica(modelo, nome)} AS {nome}" for nome in metricas]

    sql = f"SELECT {', '.join(colunas)}\nFROM {modelo['tabela']}"
    if filtros:
        sql += "\nWHERE " + " AND ".join(f"({filtro})" for filtro in filtros)
    if grupos:
        posicoes = ", ".join(str(i) for i in range(1, len(grupos) + 1))
        sql += f"\nGROUP BY {posicoes}\nORDER BY {posicoes}"
    return sql

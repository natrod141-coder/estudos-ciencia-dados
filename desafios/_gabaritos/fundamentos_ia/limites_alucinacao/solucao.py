"""Gabarito do desafio "Conferir as respostas do assistente".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import csv
import re
import sqlite3

CATEGORIAS = ("correta", "valor_errado", "sql_invalida", "citacao_inventada", "sem_fonte")

# Primeiro tenta o número com separador de milhares (1.234,50); senão, o número simples (30 ou 12,3).
# Como o ponto de milhar sempre vem seguido de três dígitos, o ponto final da frase fica de fora.
NUMERO = re.compile(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?")


def criar_banco(caminho_csv):
    """Já está pronta: carrega o CSV numa tabela vendas, num banco SQLite em memória.

    A tabela tem as colunas mes (texto, como '2026-03'), regiao (texto) e faturamento (número).
    """
    conexao = sqlite3.connect(":memory:")
    conexao.execute("CREATE TABLE vendas (mes TEXT, regiao TEXT, faturamento REAL)")
    with open(caminho_csv, encoding="utf-8", newline="") as arquivo:
        linhas = [(l["mes"], l["regiao"], float(l["faturamento"])) for l in csv.DictReader(arquivo)]
    conexao.executemany("INSERT INTO vendas VALUES (?, ?, ?)", linhas)
    return conexao


def extrair_numeros(texto):
    return [float(numero.replace(".", "").replace(",", ".")) for numero in NUMERO.findall(texto)]


def valores_conferem(afirmado, real, tolerancia=0.01):
    return abs(afirmado - real) <= tolerancia * abs(real)


def executar_consulta(conexao, sql):
    try:
        linha = conexao.execute(sql).fetchone()
    except sqlite3.Error as erro:
        return None, str(erro)
    if linha is None:
        return None, None
    return linha[0], None


def normalizar(texto):
    return " ".join(texto.lower().split())


def citacao_existe(citacao, documento):
    return normalizar(citacao) in normalizar(documento)


def classificar_resposta(resposta, conexao, documento):
    if resposta.get("sql"):
        valor, erro = executar_consulta(conexao, resposta["sql"])
        if erro:
            return "sql_invalida"
        numeros = extrair_numeros(resposta["resposta"])
        # SUM sem nenhuma linha devolve NULL: o dado não existe, e o número da resposta foi inventado
        if valor is None or not numeros or not valores_conferem(numeros[0], valor):
            return "valor_errado"
        return "correta"
    if resposta.get("citacoes"):
        if all(citacao_existe(citacao, documento) for citacao in resposta["citacoes"]):
            return "correta"
        return "citacao_inventada"
    return "sem_fonte"


def relatorio(respostas, conexao, documento):
    resultado = {categoria: [] for categoria in CATEGORIAS}
    for resposta in respostas:
        resultado[classificar_resposta(resposta, conexao, documento)].append(resposta["id"])
    return resultado

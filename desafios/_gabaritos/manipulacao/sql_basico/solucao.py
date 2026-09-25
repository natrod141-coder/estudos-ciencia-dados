"""Gabarito do desafio "Perguntas ao banco da loja".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import sqlite3
from pathlib import Path

import pandas as pd

SCRIPT_DO_BANCO = Path(__file__).parent / "data" / "loja.sql"


def abrir_banco():
    conexao = sqlite3.connect(":memory:")
    conexao.executescript(SCRIPT_DO_BANCO.read_text(encoding="utf-8"))
    return conexao


def executar(consulta):
    conexao = abrir_banco()
    try:
        return pd.read_sql_query(consulta, conexao)
    finally:
        conexao.close()


CONSULTA_1 = """
SELECT nome, categoria, preco
FROM produtos
ORDER BY preco DESC, nome
LIMIT 5;
"""

CONSULTA_2 = """
SELECT nome, preco
FROM produtos
WHERE categoria = 'Informática'
  AND preco <= 500
ORDER BY preco;
"""

CONSULTA_3 = """
SELECT nome, cidade, estado
FROM clientes
WHERE estado IN ('SP', 'RJ')
  AND nome LIKE 'A%'
ORDER BY nome;
"""

CONSULTA_4 = """
SELECT nome, estado
FROM clientes
WHERE email IS NULL
ORDER BY nome;
"""

CONSULTA_5 = """
SELECT DISTINCT estado
FROM clientes
ORDER BY estado;
"""

CONSULTA_6 = """
SELECT COUNT(*)              AS total_pedidos,
       ROUND(SUM(frete), 2)  AS frete_total,
       ROUND(AVG(frete), 2)  AS frete_medio
FROM pedidos;
"""

CONSULTA_7 = """
SELECT status, COUNT(*) AS pedidos
FROM pedidos
GROUP BY status
ORDER BY pedidos DESC;
"""

CONSULTA_8 = """
SELECT estado, COUNT(*) AS clientes
FROM clientes
GROUP BY estado
HAVING COUNT(*) >= 5
ORDER BY clientes DESC, estado;
"""

CONSULTA_9 = """
SELECT canal, COUNT(*) AS pedidos
FROM pedidos
WHERE data_pedido BETWEEN '2026-03-01' AND '2026-03-31'
  AND status <> 'cancelado'
GROUP BY canal
ORDER BY pedidos DESC, canal;
"""

CONSULTA_10 = """
SELECT CASE
           WHEN preco < 100  THEN 'econômico'
           WHEN preco < 1000 THEN 'intermediário'
           ELSE 'premium'
       END      AS faixa,
       COUNT(*) AS produtos
FROM produtos
WHERE ativo = 1
GROUP BY faixa
ORDER BY produtos DESC, faixa;
"""

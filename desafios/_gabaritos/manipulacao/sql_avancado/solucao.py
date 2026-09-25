"""Gabarito do desafio "Análises com várias tabelas".

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
SELECT p.id_pedido,
       c.nome                                         AS cliente,
       ROUND(SUM(i.quantidade * i.preco_unitario), 2) AS valor_total
FROM pedidos AS p
JOIN clientes AS c     ON c.id_cliente = p.id_cliente
JOIN itens_pedido AS i ON i.id_pedido = p.id_pedido
WHERE p.status = 'entregue'
GROUP BY p.id_pedido, c.nome
ORDER BY valor_total DESC, p.id_pedido
LIMIT 5;
"""

CONSULTA_2 = """
SELECT pr.categoria,
       ROUND(SUM(i.quantidade * i.preco_unitario), 2) AS faturamento
FROM itens_pedido AS i
JOIN pedidos AS p   ON p.id_pedido = i.id_pedido
JOIN produtos AS pr ON pr.id_produto = i.id_produto
WHERE p.status = 'entregue'
GROUP BY pr.categoria
ORDER BY faturamento DESC;
"""

CONSULTA_3 = """
SELECT c.nome, c.estado
FROM clientes AS c
LEFT JOIN pedidos AS p ON p.id_cliente = c.id_cliente
WHERE p.id_pedido IS NULL
ORDER BY c.nome;
"""

CONSULTA_4 = """
SELECT c.nome, COUNT(p.id_pedido) AS pedidos
FROM clientes AS c
LEFT JOIN pedidos AS p ON p.id_cliente = c.id_cliente
WHERE c.estado = 'PR'
GROUP BY c.id_cliente, c.nome
ORDER BY pedidos DESC, c.nome;
"""

CONSULTA_5 = """
SELECT nome, preco
FROM produtos
WHERE ativo = 1
  AND preco > (SELECT AVG(preco) FROM produtos WHERE ativo = 1)
ORDER BY preco DESC;
"""

CONSULTA_6 = """
SELECT pr.nome, pr.categoria
FROM produtos AS pr
WHERE NOT EXISTS (
    SELECT 1
    FROM itens_pedido AS i
    WHERE i.id_produto = pr.id_produto
)
ORDER BY pr.nome;
"""

CONSULTA_7 = """
WITH valor_por_pedido AS (
    SELECT p.id_pedido,
           p.id_cliente,
           SUM(i.quantidade * i.preco_unitario) AS valor
    FROM pedidos AS p
    JOIN itens_pedido AS i ON i.id_pedido = p.id_pedido
    WHERE p.status = 'entregue'
    GROUP BY p.id_pedido, p.id_cliente
),
ticket_por_cliente AS (
    SELECT id_cliente, COUNT(*) AS pedidos, AVG(valor) AS ticket_medio
    FROM valor_por_pedido
    GROUP BY id_cliente
)
SELECT c.nome, t.pedidos, ROUND(t.ticket_medio, 2) AS ticket_medio
FROM ticket_por_cliente AS t
JOIN clientes AS c ON c.id_cliente = t.id_cliente
WHERE t.pedidos >= 3
  AND t.ticket_medio > (SELECT AVG(valor) FROM valor_por_pedido)
ORDER BY t.ticket_medio DESC;
"""

CONSULTA_8 = """
WITH vendas_por_produto AS (
    SELECT pr.categoria, pr.nome, SUM(i.quantidade) AS quantidade
    FROM itens_pedido AS i
    JOIN pedidos AS p   ON p.id_pedido = i.id_pedido
    JOIN produtos AS pr ON pr.id_produto = i.id_produto
    WHERE p.status = 'entregue'
    GROUP BY pr.categoria, pr.nome
),
ranking AS (
    SELECT categoria, nome, quantidade,
           ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY quantidade DESC, nome) AS posicao
    FROM vendas_por_produto
)
SELECT categoria, nome AS produto, quantidade
FROM ranking
WHERE posicao = 1
ORDER BY categoria;
"""

CONSULTA_9 = """
WITH mensal AS (
    SELECT strftime('%Y-%m', p.data_pedido)      AS mes,
           SUM(i.quantidade * i.preco_unitario) AS faturamento
    FROM pedidos AS p
    JOIN itens_pedido AS i ON i.id_pedido = p.id_pedido
    WHERE p.status = 'entregue'
    GROUP BY mes
)
SELECT mes,
       ROUND(faturamento, 2)                              AS faturamento,
       ROUND(SUM(faturamento) OVER (ORDER BY mes), 2)     AS acumulado
FROM mensal
ORDER BY mes;
"""

CONSULTA_10 = """
WITH mensal AS (
    SELECT strftime('%Y-%m', p.data_pedido)      AS mes,
           SUM(i.quantidade * i.preco_unitario) AS faturamento
    FROM pedidos AS p
    JOIN itens_pedido AS i ON i.id_pedido = p.id_pedido
    WHERE p.status = 'entregue'
    GROUP BY mes
)
SELECT mes,
       ROUND(faturamento, 2) AS faturamento,
       ROUND((faturamento - LAG(faturamento) OVER (ORDER BY mes))
             / LAG(faturamento) OVER (ORDER BY mes) * 100, 1) AS variacao_pct
FROM mensal
ORDER BY mes;
"""

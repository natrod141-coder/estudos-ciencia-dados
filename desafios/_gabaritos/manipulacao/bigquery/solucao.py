"""Gabarito do desafio "Consultas que cabem no orçamento".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import math
from pathlib import Path

import duckdb
import pandas as pd

DADOS = Path(__file__).parent / "data"
MB = 2**20
TIB = 2**40


def abrir_banco():
    conexao = duckdb.connect()
    conexao.execute(
        f"""
        CREATE TABLE pedidos AS
        SELECT * FROM read_json('{(DADOS / "pedidos.jsonl").as_posix()}', columns = {{
            'id_pedido': 'VARCHAR', 'data_pedido': 'DATE', 'id_cliente': 'VARCHAR', 'canal': 'VARCHAR',
            'itens': 'STRUCT(sku VARCHAR, categoria VARCHAR, quantidade INTEGER, preco DOUBLE)[]'
        }})
        """
    )
    conexao.execute(
        f"""
        CREATE TABLE eventos AS
        SELECT * FROM read_json('{(DADOS / "eventos.jsonl").as_posix()}', columns = {{
            'id_evento': 'VARCHAR', 'id_usuario': 'VARCHAR', 'evento': 'VARCHAR', 'momento': 'TIMESTAMP',
            'versao_app': 'VARCHAR', 'cupom': 'VARCHAR', 'ingerido_em': 'TIMESTAMP'
        }})
        """
    )
    return conexao


def executar(consulta):
    with abrir_banco() as conexao:
        return conexao.sql(consulta).df()


# ---------------------------------------------------------------------------------------------
# Parte 1: quanto custa uma consulta
# ---------------------------------------------------------------------------------------------


def bytes_faturados(tamanhos, colunas, particoes=None):
    lidos = tamanhos[tamanhos["coluna"].isin(colunas)]
    if particoes is not None:
        lidos = lidos[lidos["particao"].isin(particoes)]
    total = int(lidos["bytes"].sum())
    arredondado = math.ceil(total / MB) * MB  # cobrança arredondada para cima, em MB
    return max(arredondado, 10 * MB)  # mínimo de 10 MB por consulta


def custo_dolares(bytes_, preco_por_tib=6.25):
    return bytes_ / TIB * preco_por_tib


def comparar_consultas(caminho_csv, preco_por_tib=6.25):
    tamanhos = pd.read_csv(caminho_csv)
    todas = tamanhos["coluna"].unique().tolist()
    necessarias = ["id_usuario", "evento", "momento"]
    primeira_semana = [f"2026-03-0{dia}" for dia in range(1, 8)]
    cenarios = {
        "select_tudo_com_limit": bytes_faturados(tamanhos, todas),
        "so_colunas_necessarias": bytes_faturados(tamanhos, necessarias),
        "colunas_e_particoes": bytes_faturados(tamanhos, necessarias, primeira_semana),
    }
    return {nome: round(custo_dolares(b, preco_por_tib), 2) for nome, b in cenarios.items()}


# ---------------------------------------------------------------------------------------------
# Parte 2: consultas no estilo BigQuery (escritas em DuckDB)
# ---------------------------------------------------------------------------------------------

CONSULTA_1 = """
SELECT item.categoria,
       ROUND(SUM(item.quantidade * item.preco), 2) AS faturamento
FROM pedidos, UNNEST(itens) AS t(item)
GROUP BY item.categoria
ORDER BY faturamento DESC;
"""

CONSULTA_2 = """
SELECT data_pedido,
       COUNT(DISTINCT id_pedido) AS pedidos,
       SUM(item.quantidade)      AS unidades
FROM pedidos, UNNEST(itens) AS t(item)
WHERE data_pedido BETWEEN '2026-03-02' AND '2026-03-08'
GROUP BY data_pedido
ORDER BY data_pedido;
"""

CONSULTA_3 = """
WITH sem_duplicatas AS (
    SELECT *
    FROM eventos
    QUALIFY ROW_NUMBER() OVER (PARTITION BY id_evento ORDER BY ingerido_em DESC) = 1
)
SELECT evento, COUNT(*) AS eventos
FROM sem_duplicatas
GROUP BY evento
ORDER BY eventos DESC;
"""

CONSULTA_4 = """
SELECT versao_app,
       COUNT(DISTINCT IF(evento = 'visualizou_produto', id_usuario, NULL)) AS visualizaram,
       COUNT(DISTINCT IF(evento = 'adicionou_carrinho', id_usuario, NULL)) AS adicionaram,
       COUNT(DISTINCT IF(evento = 'comprou', id_usuario, NULL))            AS compraram,
       ROUND(100.0 * COUNT(DISTINCT IF(evento = 'comprou', id_usuario, NULL))
             / COUNT(DISTINCT IF(evento = 'visualizou_produto', id_usuario, NULL)), 1) AS conversao_pct
FROM eventos
GROUP BY versao_app
ORDER BY versao_app;
"""

CONSULTA_5 = """
WITH compras AS (
    SELECT *
    FROM eventos
    WHERE evento = 'comprou' AND cupom IS NOT NULL
    QUALIFY ROW_NUMBER() OVER (PARTITION BY id_evento ORDER BY ingerido_em DESC) = 1
)
SELECT COUNT(TRY_CAST(cupom AS INTEGER))                  AS cupons_validos,
       COUNT(*) - COUNT(TRY_CAST(cupom AS INTEGER))       AS cupons_invalidos,
       ROUND(AVG(TRY_CAST(cupom AS INTEGER)), 2)          AS desconto_medio
FROM compras;
"""

CONSULTA_6 = """
WITH por_semana AS (
    SELECT CAST(date_trunc('week', data_pedido) AS DATE) AS semana,
           SUM(item.quantidade * item.preco)             AS faturamento
    FROM pedidos, UNNEST(itens) AS t(item)
    GROUP BY semana
)
SELECT semana,
       ROUND(faturamento, 2)                                   AS faturamento,
       ROUND(100 * faturamento / SUM(faturamento) OVER (), 1)  AS participacao_pct
FROM por_semana
ORDER BY semana;
"""

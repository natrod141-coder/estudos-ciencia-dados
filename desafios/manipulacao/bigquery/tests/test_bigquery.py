import datetime as dt
from pathlib import Path

import duckdb
import pandas as pd
import pytest

import solucao

DADOS = Path(__file__).parent.parent / "data"
MB = 2**20
TIB = 2**40


def banco_de_teste():
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


def rodar(nome):
    """Roda a consulta num banco novo e devolve (nomes das colunas, linhas)."""
    conexao = banco_de_teste()
    try:
        resultado = conexao.sql(getattr(solucao, nome))
        assert resultado is not None, f"{nome} não devolveu nada. Escreva a consulta no lugar do comentário."
        colunas = resultado.columns
        linhas = [tuple(round(v, 2) if isinstance(v, float) else v for v in linha) for linha in resultado.fetchall()]
    finally:
        conexao.close()
    return colunas, linhas


# Parte 1: quanto custa uma consulta


def test_bytes_faturados_soma_so_as_colunas_e_particoes_lidas():
    tamanhos = pd.DataFrame(
        {
            "particao": ["2026-03-01", "2026-03-01", "2026-03-02", "2026-03-02"],
            "coluna": ["a", "b", "a", "b"],
            "bytes": [100 * MB, 900 * MB, 200 * MB, 800 * MB],
        }
    )
    assert solucao.bytes_faturados(tamanhos, ["a"]) == 300 * MB
    assert solucao.bytes_faturados(tamanhos, ["a", "b"]) == 2000 * MB
    assert solucao.bytes_faturados(tamanhos, ["b"], ["2026-03-02"]) == 800 * MB


def test_bytes_faturados_arredonda_para_cima_e_cobra_no_minimo_10_mb():
    tamanhos = pd.DataFrame({"particao": ["d", "d"], "coluna": ["a", "b"], "bytes": [30 * MB + 1, 5]})
    assert solucao.bytes_faturados(tamanhos, ["a"]) == 31 * MB  # 1 byte a mais já conta como 1 MB
    assert solucao.bytes_faturados(tamanhos, ["b"]) == 10 * MB  # 5 bytes, mas o mínimo é 10 MB


def test_custo_dolares():
    assert solucao.custo_dolares(TIB) == pytest.approx(6.25)
    assert solucao.custo_dolares(TIB // 2, preco_por_tib=5.0) == pytest.approx(2.5)


def test_comparar_consultas():
    custos = solucao.comparar_consultas(DADOS / "tamanhos_eventos.csv")
    assert custos == pytest.approx(
        {"select_tudo_com_limit": 25.40, "so_colunas_necessarias": 2.53, "colunas_e_particoes": 0.21}
    )


# Parte 2: consultas no estilo BigQuery


def test_consulta_1_faturamento_por_categoria_com_unnest():
    colunas, linhas = rodar("CONSULTA_1")
    assert colunas == ["categoria", "faturamento"]
    assert linhas == [("Eletrônicos", 353358.0), ("Casa", 39678.4), ("Moda", 34770.9), ("Beleza", 10600.0)]


def test_consulta_2_pedidos_e_unidades_por_dia_da_semana_de_2_a_8_de_marco():
    colunas, linhas = rodar("CONSULTA_2")
    assert colunas == ["data_pedido", "pedidos", "unidades"]
    assert [linha[0] for linha in linhas] == [dt.date(2026, 3, dia) for dia in range(2, 9)]
    assert [linha[1] for linha in linhas] == [14, 9, 12, 12, 14, 14, 18], (
        "Depois do UNNEST, cada pedido aparece uma vez por item: conte pedidos com COUNT(DISTINCT id_pedido)."
    )
    assert [linha[2] for linha in linhas] == [70, 27, 50, 43, 49, 44, 68]


def test_consulta_3_eventos_sem_duplicatas():
    colunas, linhas = rodar("CONSULTA_3")
    assert colunas == ["evento", "eventos"]
    assert linhas == [("visualizou_produto", 1511), ("adicionou_carrinho", 262), ("comprou", 107)], (
        "Há 90 eventos repetidos pela ingestão. Fique com uma linha por id_evento."
    )


def test_consulta_4_funil_por_versao_do_app():
    colunas, linhas = rodar("CONSULTA_4")
    assert colunas == ["versao_app", "visualizaram", "adicionaram", "compraram", "conversao_pct"]
    assert linhas == [("5.1", 300, 127, 53, 17.7), ("5.2", 300, 135, 54, 18.0)]


def test_consulta_5_cupons_com_conversao_segura():
    colunas, linhas = rodar("CONSULTA_5")
    assert colunas == ["cupons_validos", "cupons_invalidos", "desconto_medio"]
    assert linhas == [(22, 23, 11.59)]


def test_consulta_6_faturamento_por_semana_e_participacao():
    colunas, linhas = rodar("CONSULTA_6")
    assert colunas == ["semana", "faturamento", "participacao_pct"]
    assert linhas == [
        (dt.date(2026, 2, 23), 13394.6, 3.1),
        (dt.date(2026, 3, 2), 91439.1, 20.9),
        (dt.date(2026, 3, 9), 86713.1, 19.8),
        (dt.date(2026, 3, 16), 97065.6, 22.1),
        (dt.date(2026, 3, 23), 109708.1, 25.0),
        (dt.date(2026, 3, 30), 40086.8, 9.1),
    ]

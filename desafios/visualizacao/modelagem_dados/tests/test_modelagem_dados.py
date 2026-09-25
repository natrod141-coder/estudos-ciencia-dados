from pathlib import Path

import pandas as pd
import pytest

from solucao import (
    criar_calendario,
    criar_dim_loja,
    criar_dim_produto,
    criar_fato,
    granularidade_ok,
    inconsistencias,
    ler_planilha,
    montar_modelo,
    validar_relacionamento,
)

CSV = Path(__file__).parent.parent / "data" / "vendas_planas.csv"
ATRIBUTOS_PRODUTO = ["produto", "categoria", "marca", "custo_unitario"]


def test_inconsistencias():
    plana = ler_planilha(CSV)
    assert inconsistencias(plana, "codigo_produto", ATRIBUTOS_PRODUTO) == ["P07"], (
        "O P07 aparece com duas categorias: foi recategorizado no meio do período."
    )
    assert inconsistencias(plana, "codigo_loja", ["loja", "cidade", "uf"]) == []


def test_dim_produto_tem_uma_linha_por_produto_com_a_versao_mais_recente():
    dim = criar_dim_produto(ler_planilha(CSV))
    assert list(dim.columns) == ["id_produto", "codigo_produto", "produto", "categoria", "marca", "custo_unitario"]
    assert len(dim) == 12
    assert dim["codigo_produto"].is_unique
    relogio = dim[dim["codigo_produto"] == "P07"].iloc[0]
    assert relogio["categoria"] == "Eletrônicos", "Use os atributos da venda mais recente de cada produto."


def test_dim_produto_tem_chave_substituta():
    dim = criar_dim_produto(ler_planilha(CSV))
    assert dim["id_produto"].tolist() == list(range(1, 13)), "id_produto vai de 1 a 12, na ordem do código."
    assert dim["codigo_produto"].tolist()[:3] == ["P01", "P02", "P03"]


def test_dim_loja():
    dim = criar_dim_loja(ler_planilha(CSV))
    assert list(dim.columns) == ["id_loja", "codigo_loja", "loja", "cidade", "uf"]
    assert dim["id_loja"].tolist() == [1, 2, 3, 4, 5]
    assert dim.loc[dim["codigo_loja"] == "L04", "cidade"].item() == "São Paulo"


def test_calendario_continuo():
    calendario = criar_calendario("2025-01-01", "2026-12-31")
    assert len(calendario) == 730, "Uma linha por dia, sem pular nenhum."
    assert calendario["data"].is_unique
    assert calendario["data"].diff().dropna().eq(pd.Timedelta(days=1)).all()


def test_calendario_colunas():
    calendario = criar_calendario("2025-01-01", "2026-12-31").set_index("data")
    segunda = calendario.loc[pd.Timestamp("2026-03-02")]
    assert (segunda["ano"], segunda["mes"], segunda["nome_mes"]) == (2026, 3, "março")
    assert (segunda["trimestre"], segunda["ano_mes"]) == ("T1", "2026-03")
    assert (segunda["dia_semana"], bool(segunda["fim_de_semana"])) == ("segunda-feira", False)
    sabado = calendario.loc[pd.Timestamp("2025-11-15")]
    assert (sabado["dia_semana"], bool(sabado["fim_de_semana"]), sabado["trimestre"]) == ("sábado", True, "T4")


def test_fato_tem_so_chaves_datas_e_numeros():
    plana = ler_planilha(CSV)
    fato = criar_fato(plana, criar_dim_produto(plana), criar_dim_loja(plana))
    assert list(fato.columns) == ["data", "pedido", "id_produto", "id_loja", "quantidade", "preco_unitario", "valor"], (
        "Os textos descritivos (nome, categoria, cidade...) ficam nas dimensões, e não na fato."
    )


def test_fato_valores():
    plana = ler_planilha(CSV)
    fato = criar_fato(plana, criar_dim_produto(plana), criar_dim_loja(plana))
    assert len(fato) == 853, "A fato tem uma linha por item vendido, como a planilha."
    assert fato["valor"].sum() == pytest.approx(435533.02)
    primeira = fato.iloc[0]
    assert (primeira["pedido"], primeira["id_produto"], primeira["id_loja"], primeira["valor"]) == ("V00001", 10, 4, 798.0)


def test_validar_relacionamento():
    dimensao = pd.DataFrame({"id": [1, 2, 2]})
    fato = pd.DataFrame({"id": [1, 2, 3, 3, 1]})
    assert validar_relacionamento(fato, dimensao, "id") == {"chave_unica_na_dimensao": False, "linhas_orfas_na_fato": 2}
    boa = pd.DataFrame({"id": [1, 2, 3]})
    assert validar_relacionamento(fato, boa, "id") == {"chave_unica_na_dimensao": True, "linhas_orfas_na_fato": 0}


def test_granularidade():
    tabela = pd.DataFrame({"pedido": ["A", "A", "B"], "produto": [1, 2, 1]})
    assert granularidade_ok(tabela, ["pedido", "produto"]) is True
    assert granularidade_ok(tabela, ["pedido"]) is False


def test_montar_modelo():
    modelo = montar_modelo(CSV)
    assert set(modelo) == {"fato_vendas", "dim_produto", "dim_loja", "dim_data"}
    fato = modelo["fato_vendas"]
    assert validar_relacionamento(fato, modelo["dim_produto"], "id_produto")["linhas_orfas_na_fato"] == 0
    assert validar_relacionamento(fato, modelo["dim_loja"], "id_loja")["linhas_orfas_na_fato"] == 0
    datas = modelo["dim_data"]["data"]
    assert (datas.min(), datas.max()) == (pd.Timestamp("2025-01-01"), pd.Timestamp("2026-12-31")), (
        "O calendário cobre anos completos, de 1º de janeiro do primeiro ano a 31 de dezembro do último."
    )
    assert granularidade_ok(fato, ["pedido", "id_produto"])

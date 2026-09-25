from pathlib import Path

import pandas as pd
import pytest

from solucao import (
    CLASSIFICACAO,
    ORDEM_SATISFACAO,
    ler_pesquisa,
    medidas_permitidas,
    mediana_ordinal,
    resumo_central,
)

CSV = Path(__file__).parent.parent / "data" / "pesquisa.csv"


def test_classificacao_das_qualitativas():
    colunas = ["cidade", "cep", "escolaridade", "satisfacao"]
    assert {c: CLASSIFICACAO.get(c) for c in colunas} == {
        "cidade": "nominal",
        "cep": "nominal",
        "escolaridade": "ordinal",
        "satisfacao": "ordinal",
    }


def test_classificacao_das_quantitativas():
    colunas = ["dependentes", "compras_no_ano", "renda_mensal"]
    assert {c: CLASSIFICACAO.get(c) for c in colunas} == {
        "dependentes": "discreta",
        "compras_no_ano": "discreta",
        "renda_mensal": "continua",
    }


def test_medidas_permitidas():
    assert medidas_permitidas("nominal") == ["moda"]
    assert medidas_permitidas("ordinal") == ["moda", "mediana"]
    assert medidas_permitidas("discreta") == ["moda", "mediana", "media"]
    assert medidas_permitidas("continua") == ["mediana", "media"]


def test_medidas_permitidas_tipo_desconhecido():
    with pytest.raises(ValueError):
        medidas_permitidas("numerica")


def test_ler_pesquisa_preserva_o_zero_do_cep():
    pesquisa = ler_pesquisa(CSV)
    assert pesquisa["cep"].iloc[0] == "01310100"  # lido como número, viraria 1310100
    assert pesquisa["dependentes"].iloc[0] == 3  # as colunas numéricas continuam numéricas


def test_ler_pesquisa_ordinais_em_ordem():
    pesquisa = ler_pesquisa(CSV)
    satisfacao = pesquisa["satisfacao"]
    assert satisfacao.cat.ordered
    assert list(satisfacao.cat.categories) == ORDEM_SATISFACAO
    assert satisfacao.max() == "muito satisfeito"
    # com a ordem certa, dá para comparar: quantos têm superior completo ou mais?
    assert (pesquisa["escolaridade"] >= "superior").sum() == 13


def test_mediana_ordinal():
    ordem = ["baixa", "média", "alta"]
    impar = pd.Series(pd.Categorical(["baixa", "alta", "média", "média", "alta"], categories=ordem, ordered=True))
    assert mediana_ordinal(impar) == "média"
    par = pd.Series(pd.Categorical(["alta", "baixa"], categories=ordem, ordered=True))
    assert mediana_ordinal(par) == "baixa"  # com quantidade par, a mediana inferior


def test_resumo_central():
    resumo = resumo_central(ler_pesquisa(CSV))
    assert resumo["cidade"] == {"moda": "São Paulo"}
    assert resumo["cep"] == {"moda": "01310100"}
    assert resumo["escolaridade"] == {"moda": "médio", "mediana": "superior"}
    assert resumo["satisfacao"] == {"moda": "satisfeito", "mediana": "satisfeito"}
    assert resumo["compras_no_ano"] == {"moda": 12, "mediana": pytest.approx(9.0), "media": pytest.approx(10.44)}
    assert resumo["renda_mensal"] == {"mediana": pytest.approx(4166.15), "media": pytest.approx(4423.47)}

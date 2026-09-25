from pathlib import Path

import pandas as pd
import pytest

from solucao import (
    adicionar_faixa,
    agrupar_por_loja_e_mes,
    cartoes,
    combinar_arquivos,
    despivotar_metas,
    ler_arquivo_vendas,
    mesclar_lojas,
    montar_relatorio,
    realizado_vs_meta,
)

DADOS = Path(__file__).parent.parent / "data"
LOJAS = ["L01", "L02", "L03", "L04", "L05", "L06"]


def lojas():
    return pd.read_csv(DADOS / "lojas.csv", sep=";")


def realizado():
    vendas = combinar_arquivos(DADOS / "vendas")
    return realizado_vs_meta(agrupar_por_loja_e_mes(vendas), despivotar_metas(DADOS / "metas.csv"))


def test_ler_arquivo_vendas_com_localidade_brasileira():
    vendas = ler_arquivo_vendas(DADOS / "vendas" / "vendas_2026_01.csv")
    assert len(vendas) == 120
    assert pd.api.types.is_datetime64_any_dtype(vendas["data"]), "A data vem como dd/mm/aaaa: converta para data."
    assert pd.api.types.is_float_dtype(vendas["valor"]), "O valor usa vírgula decimal: leia com decimal=','."
    assert vendas["data"].dt.month.unique().tolist() == [1]


def test_combinar_arquivos_empilha_todos_os_meses():
    vendas = combinar_arquivos(DADOS / "vendas")
    assert len(vendas) == 390
    assert vendas["arquivo"].value_counts().to_dict() == {
        "vendas_2026_03.csv": 140, "vendas_2026_02.csv": 130, "vendas_2026_01.csv": 120,
    }
    assert vendas["arquivo"].iloc[0] == "vendas_2026_01.csv", "Leia os arquivos em ordem de nome."


def test_combinar_arquivos_padroniza_o_codigo_da_loja():
    vendas = combinar_arquivos(DADOS / "vendas")
    assert sorted(vendas["loja"].unique()) == LOJAS, (
        "No arquivo de março há códigos como ' L06' e 'l02 ': tire os espaços e passe para maiúsculas."
    )


def test_despivotar_metas():
    metas = despivotar_metas(DADOS / "metas.csv")
    assert list(metas.columns) == ["loja", "mes", "meta"]
    assert len(metas) == 18, "São 6 lojas x 3 meses: uma linha por loja e mês."
    assert metas.iloc[:3].values.tolist() == [["L01", 1, 11000.0], ["L01", 2, 16000.0], ["L01", 3, 25000.0]]


def test_mesclar_lojas():
    vendas = mesclar_lojas(combinar_arquivos(DADOS / "vendas"), lojas())
    assert len(vendas) == 390, "A mesclagem não pode duplicar nem sumir com vendas."
    assert {"nome_loja", "regiao"} <= set(vendas.columns)
    assert vendas["regiao"].notna().all(), "Alguma venda ficou sem loja: confira a padronização do código."
    assert set(vendas.loc[vendas["loja"] == "L04", "regiao"]) == {"Sudeste"}


def test_adicionar_faixa():
    vendas = pd.DataFrame({"valor": [150.0, 200.0, 999.99, 1000.0]})
    resultado = adicionar_faixa(vendas)
    assert resultado["faixa"].tolist() == ["pequena", "média", "média", "grande"]
    assert "faixa" not in vendas.columns, "Não altere o DataFrame recebido."


def test_agrupar_por_loja_e_mes():
    agrupado = agrupar_por_loja_e_mes(combinar_arquivos(DADOS / "vendas"))
    assert list(agrupado.columns) == ["loja", "mes", "faturamento", "vendas"]
    assert len(agrupado) == 18
    linha = agrupado[(agrupado["loja"] == "L04") & (agrupado["mes"] == 2)].iloc[0]
    assert linha["faturamento"] == pytest.approx(25943.59)
    assert linha["vendas"] == 34


def test_realizado_vs_meta():
    tabela = realizado().set_index(["loja", "mes"])
    assert tabela.loc[("L01", 2), "atingimento_pct"] == pytest.approx(109.6)
    assert bool(tabela.loc[("L01", 2), "bateu_meta"]) is True
    assert tabela.loc[("L06", 2), "atingimento_pct"] == pytest.approx(88.6)
    assert bool(tabela.loc[("L06", 2), "bateu_meta"]) is False


def test_cartoes():
    assert cartoes(realizado()) == pytest.approx(
        {"faturamento_total": 298172.18, "meta_total": 294000.0, "atingimento_pct": 101.4, "metas_batidas": 11}
    )


def test_montar_relatorio():
    relatorio = montar_relatorio(DADOS)
    assert set(relatorio) == {"vendas", "realizado", "cartoes"}
    assert {"faixa", "regiao", "arquivo"} <= set(relatorio["vendas"].columns)
    assert relatorio["cartoes"]["metas_batidas"] == 11

from pathlib import Path

import openpyxl
import pandas as pd
import pytest

from solucao import (
    exportar_relatorio,
    ler_produtos,
    ler_vendas,
    limpar_vendas,
    procx,
    somases,
    tabela_dinamica,
    texto_para_numero,
)

XLSX = Path(__file__).parent.parent / "data" / "vendas_filial.xlsx"


def vendas_limpas():
    return limpar_vendas(ler_vendas(XLSX))


def vendas_completas():
    return procx(vendas_limpas(), ler_produtos(XLSX))


def test_ler_vendas_pula_o_titulo_e_tira_o_total():
    vendas = ler_vendas(XLSX)
    assert list(vendas.columns) == ["Data", "Vendedor", "Código", "Quantidade", "Valor total"]
    assert len(vendas) == 63, "Esperava 63 linhas de venda: sem as linhas de título e sem a linha Total."
    assert "Total" not in vendas["Data"].tolist()
    assert vendas["Quantidade"].tolist()[:3] == [3, 10, 3]
    assert pd.api.types.is_integer_dtype(vendas["Quantidade"]), "Quantidade precisa ser número inteiro."


def test_texto_para_numero():
    assert texto_para_numero("R$ 1.234,56") == pytest.approx(1234.56)
    assert texto_para_numero("  R$ 11.697,00 ") == pytest.approx(11697.0)
    assert texto_para_numero("R$ 49,00") == pytest.approx(49.0)
    assert texto_para_numero(799.5) == pytest.approx(799.5)  # já veio como número
    with pytest.raises(ValueError):
        texto_para_numero("ver sistema")


def test_limpar_vendas_arruma_os_nomes():
    vendas = vendas_limpas()
    assert sorted(vendas["Vendedor"].unique()) == ["Ana Souza", "Bruno Lima", "Carla Mendes", "Diego Rocha"]


def test_limpar_vendas_converte_os_tipos():
    vendas = vendas_limpas()
    assert pd.api.types.is_datetime64_any_dtype(vendas["Data"]), "Data precisa virar data de verdade."
    assert vendas["Data"].min() == pd.Timestamp("2026-01-02")
    assert vendas["Data"].max() == pd.Timestamp("2026-03-31")
    assert pd.api.types.is_float_dtype(vendas["Valor total"]), "Valor total precisa virar número."


def test_limpar_vendas_remove_duplicatas():
    vendas = vendas_limpas()
    assert len(vendas) == 60, "Havia 3 linhas repetidas pela exportação."
    assert vendas["Valor total"].sum() == pytest.approx(150321.30)


def test_procx_traz_produto_e_categoria():
    vendas = vendas_completas()
    assert len(vendas) == 60, "A busca não pode duplicar nem sumir com vendas."
    primeira = vendas.iloc[0]
    assert (primeira["Código"], primeira["Produto"], primeira["Categoria"]) == ("P-001", "Notebook 14", "Informática")


def test_procx_marca_codigos_nao_encontrados():
    vendas = vendas_completas()
    nao_encontrados = vendas[vendas["Produto"] == "Não encontrado"]
    assert nao_encontrados["Código"].tolist() == ["P-099", "P-099"]
    assert (nao_encontrados["Categoria"] == "Não encontrado").all()


def test_somases():
    vendas = vendas_limpas()
    assert somases(vendas, "Ana Souza", 2) == pytest.approx(25172.10)
    assert somases(vendas, "Carla Mendes", 1) == pytest.approx(159.60)
    assert somases(vendas, "Diego Rocha", 3) == pytest.approx(12427.00)
    assert somases(vendas, "Ninguém", 1) == pytest.approx(0.0)


def test_tabela_dinamica():
    vendas = vendas_completas()
    tabela = tabela_dinamica(vendas)
    assert list(tabela.index) == ["Ana Souza", "Bruno Lima", "Carla Mendes", "Diego Rocha", "Total"]
    assert list(tabela.columns) == ["Informática", "Móveis", "Não encontrado", "Papelaria", "Total"]
    assert tabela.loc["Ana Souza", "Informática"] == pytest.approx(46822.40)
    assert tabela.loc["Carla Mendes", "Móveis"] == pytest.approx(0.0), "Célula vazia na dinâmica vira 0."
    assert tabela.loc["Total", "Papelaria"] == pytest.approx(2342.90)
    assert tabela.loc["Total", "Total"] == pytest.approx(150321.30)


def test_exportar_relatorio(tmp_path):
    saida = tmp_path / "relatorio.xlsx"
    exportar_relatorio(XLSX, saida)
    planilha = openpyxl.load_workbook(saida)
    assert planilha.sheetnames == ["Dados", "Resumo"]
    assert planilha["Dados"].freeze_panes == "A2", "Congele a linha do cabeçalho na aba Dados."
    dados = pd.read_excel(saida, sheet_name="Dados")
    assert len(dados) == 60
    assert {"Produto", "Categoria"} <= set(dados.columns)
    resumo = pd.read_excel(saida, sheet_name="Resumo", index_col=0)
    assert resumo.loc["Total", "Total"] == pytest.approx(150321.30)

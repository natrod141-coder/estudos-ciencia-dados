from pathlib import Path

import pytest

from solucao import (
    carregar_modelo,
    crescimento_anual,
    datas_visiveis,
    faturamento,
    faturamento_acumulado_no_ano,
    faturamento_ano_anterior,
    faturamento_todas_as_lojas,
    filtrar_fato,
    margem,
    matriz,
    participacao_da_loja,
)

MODELO = carregar_modelo(Path(__file__).parent.parent / "data")
T1_2026 = {"dim_data[ano]": 2026, "dim_data[trimestre]": "T1"}


# Parte 1: o contexto de filtro


def test_filtrar_fato_pela_dimensao():
    vendas_pr = filtrar_fato(MODELO, {"dim_loja[uf]": "PR"})
    assert len(vendas_pr) == 308, "O filtro na dimensão de lojas precisa descer para a fato pelo id_loja."
    assert set(vendas_pr["id_loja"]) == {1, 2}  # as duas lojas de Curitiba
    assert len(filtrar_fato(MODELO, {})) == 853, "Sem filtros, todas as vendas são visíveis."


def test_filtrar_fato_com_lista_e_varias_tabelas():
    filtros = {"dim_loja[uf]": ["PR", "SP"], "dim_data[ano]": 2026, "dim_produto[categoria]": "Calçados"}
    assert filtrar_fato(MODELO, filtros)["valor"].sum() == pytest.approx(27122.41), (
        "Filtros em tabelas diferentes se combinam (E), e uma lista de valores vale como OU."
    )


def test_datas_visiveis():
    assert len(datas_visiveis(MODELO, {"dim_data[ano]": 2026, "dim_data[mes]": 2})) == 28
    assert len(datas_visiveis(MODELO, {"dim_loja[uf]": "PR"})) == 730, "Filtros de outras tabelas não afetam o calendário."


# Parte 2: medidas


def test_faturamento():
    assert faturamento(MODELO, {}) == pytest.approx(435533.02)
    assert faturamento(MODELO, {"dim_data[ano]": 2025}) == pytest.approx(266375.48)
    assert faturamento(MODELO, {"dim_loja[uf]": "PR"}) == pytest.approx(155516.25)


def test_margem_usa_o_custo_do_produto():
    assert margem(MODELO, {}) == pytest.approx(216660.02)
    assert margem(MODELO, {"dim_produto[categoria]": "Eletrônicos"}) == pytest.approx(84885.10)


def test_faturamento_todas_as_lojas_ignora_so_o_filtro_de_loja():
    filtros = {"dim_loja[uf]": "PR", "dim_data[ano]": 2025}
    assert faturamento_todas_as_lojas(MODELO, filtros) == pytest.approx(266375.48), (
        "ALL(dim_loja) remove os filtros de loja, mas o filtro de ano continua valendo."
    )


def test_participacao_da_loja():
    assert participacao_da_loja(MODELO, {"dim_loja[uf]": "SP", "dim_data[ano]": 2025}) == pytest.approx(0.267404, abs=1e-6)
    assert participacao_da_loja(MODELO, {"dim_data[ano]": 2026, "dim_data[mes]": 12}) is None, (
        "Sem vendas no período, o denominador é zero: como o DIVIDE, devolva None (em DAX, BLANK)."
    )


def test_faturamento_acumulado_no_ano():
    assert faturamento_acumulado_no_ano(MODELO, {"dim_data[ano]": 2026, "dim_data[mes]": 3}) == pytest.approx(80962.79), (
        "O acumulado de março soma de 1º de janeiro até a última data visível de março."
    )
    assert faturamento_acumulado_no_ano(MODELO, {"dim_data[ano]": 2025}) == pytest.approx(266375.48)


def test_faturamento_ano_anterior():
    assert faturamento_ano_anterior(MODELO, {"dim_data[ano]": 2026, "dim_data[mes]": 3}) == pytest.approx(26314.30)
    assert faturamento_ano_anterior(MODELO, {"dim_data[ano]": 2025}) == pytest.approx(0.0)


def test_crescimento_anual():
    assert crescimento_anual(MODELO, T1_2026) == pytest.approx(0.397441, abs=1e-6)
    assert crescimento_anual(MODELO, {"dim_data[ano]": 2025}) is None, "Não há 2024 para comparar: devolva None."


def test_matriz_recalcula_o_total():
    por_uf = matriz(MODELO, T1_2026, "dim_loja[uf]", crescimento_anual)
    assert list(por_uf) == ["MG", "PR", "RS", "SP", "Total"]
    assert por_uf["PR"] == pytest.approx(0.714034, abs=1e-6)
    assert por_uf["MG"] == pytest.approx(-0.018044, abs=1e-6)
    assert por_uf["Total"] == pytest.approx(0.397441, abs=1e-6), (
        "O total é a medida calculada sem o filtro da linha, e não a soma das linhas."
    )
    participacao = matriz(MODELO, {"dim_data[ano]": 2025}, "dim_loja[uf]", participacao_da_loja)
    assert participacao["Total"] == pytest.approx(1.0)

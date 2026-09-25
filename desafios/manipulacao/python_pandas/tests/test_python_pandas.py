from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from solucao import (
    aplicar_desconto,
    analisar,
    classificar_valores,
    evolucao_mensal,
    juntar_clientes,
    ler_clientes,
    ler_pedidos,
    padronizar,
    resumo_faltantes,
    resumo_por_estado,
    top_clientes,
    tratar_faltantes,
)

DADOS = Path(__file__).parent.parent / "data"
PEDIDOS = DADOS / "pedidos.csv"
CLIENTES = DADOS / "clientes.csv"


def pedidos_completos():
    return juntar_clientes(tratar_faltantes(ler_pedidos(PEDIDOS)), ler_clientes(CLIENTES))


# Parte 1: NumPy


def test_padronizar():
    z = padronizar([2, 4, 4, 4, 5, 5, 7, 9])
    assert isinstance(z, np.ndarray), "Devolva um array do NumPy."
    assert z[0] == pytest.approx(-1.40312, abs=1e-5)
    assert z.mean() == pytest.approx(0.0, abs=1e-12)
    assert z.std(ddof=1) == pytest.approx(1.0)


def test_aplicar_desconto():
    totais = aplicar_desconto(np.array([10.0, 20.0, 5.0]), np.array([2, 10, 12]))
    assert totais.tolist() == pytest.approx([20.0, 180.0, 54.0])  # 10% só a partir de 10 unidades
    assert aplicar_desconto([100.0], [5], minimo=5, desconto=0.2).tolist() == pytest.approx([400.0])


def test_classificar_valores():
    faixas = classificar_valores(np.array([50, 100, 499.99, 500, 1200]))
    assert list(faixas) == ["baixo", "médio", "médio", "alto", "alto"]


# Parte 2: ler e conhecer os dados


def test_ler_pedidos_converte_os_tipos():
    pedidos = ler_pedidos(PEDIDOS)
    assert pd.api.types.is_datetime64_any_dtype(pedidos["data"]), "A coluna data precisa ser data."
    assert pd.api.types.is_float_dtype(pedidos["valor"]), 'O "n/d" precisa virar faltante, e valor, número.'
    assert pd.api.types.is_integer_dtype(pedidos["id_cliente"]), (
        'id_cliente tem faltantes e virou float. Use dtype={"id_cliente": "Int64"}.'
    )


def test_ler_pedidos_remove_pedidos_repetidos():
    pedidos = ler_pedidos(PEDIDOS)
    assert len(pedidos) == 420, "Três pedidos vieram repetidos na exportação."
    assert pedidos["id_pedido"].is_unique


def test_resumo_faltantes():
    resumo = resumo_faltantes(ler_pedidos(PEDIDOS))
    assert list(resumo.index) == ["canal", "valor", "id_cliente"], "Só colunas com faltantes, da que tem mais para a que tem menos."
    assert resumo["faltantes"].tolist() == [18, 12, 5]
    assert resumo["percentual"].tolist() == pytest.approx([4.3, 2.9, 1.2])


# Parte 3: dados faltantes


def test_tratar_faltantes_tira_pedidos_sem_cliente_e_preenche_o_canal():
    original = ler_pedidos(PEDIDOS)
    tratado = tratar_faltantes(original)
    assert len(tratado) == 415
    assert tratado["id_cliente"].notna().all()
    assert (tratado["canal"] == "não informado").sum() == 18
    assert tratado["canal"].notna().all()
    assert len(original) == 420, "Não altere o DataFrame recebido: trabalhe numa cópia."


def test_tratar_faltantes_usa_a_mediana_da_categoria():
    tratado = tratar_faltantes(ler_pedidos(PEDIDOS)).set_index("id_pedido")
    assert tratado["valor"].notna().all()
    assert tratado["valor_imputado"].sum() == 12
    assert tratado.loc[70002, "valor"] == pytest.approx(154.015)  # mediana de Casa
    assert tratado.loc[70355, "valor"] == pytest.approx(441.88)  # mediana de Eletrônicos
    assert tratado.loc[70252, "valor"] == pytest.approx(128.455)  # mediana de Moda
    assert not tratado.loc[70272, "valor_imputado"]


# Parte 4: juntar, agrupar e resumir


def test_juntar_clientes():
    completo = pedidos_completos()
    assert len(completo) == 415, "A junção não pode duplicar nem sumir com pedidos."
    assert {"nome", "estado"} <= set(completo.columns)
    assert completo["estado"].notna().all()
    assert completo.loc[completo["id_pedido"] == 70272, "nome"].item() == "Sofia Rocha"


def test_resumo_por_estado():
    resumo = resumo_por_estado(pedidos_completos())
    assert list(resumo.columns) == ["pedidos", "faturamento", "ticket_medio"]
    assert list(resumo.index[:3]) == ["SP", "PE", "MG"], "Ordene do maior faturamento para o menor."
    assert resumo.loc["SP"].tolist() == pytest.approx([145, 30158.50, 207.99])
    assert resumo.loc["RS", "pedidos"] == 2


def test_evolucao_mensal():
    mensal = evolucao_mensal(pedidos_completos())
    assert list(mensal.index) == ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"]
    assert mensal.loc["2026-01", "faturamento"] == pytest.approx(14313.53)
    assert pd.isna(mensal.loc["2026-01", "variacao_pct"]), "O primeiro mês não tem mês anterior para comparar."
    assert mensal.loc["2026-02", "variacao_pct"] == pytest.approx(-8.3)
    assert mensal.loc["2026-05", "variacao_pct"] == pytest.approx(19.2)


def test_top_clientes():
    pedidos = pd.DataFrame({"nome": ["Ana", "Bia", "Ana", "Caio", "Bia"], "valor": [10.0, 50.0, 30.0, 5.0, 1.0]})
    top = top_clientes(pedidos, n=2)
    assert list(top.index) == ["Bia", "Ana"]
    assert top.tolist() == pytest.approx([51.0, 40.0])


def test_analisar():
    resultado = analisar(PEDIDOS, CLIENTES)
    assert set(resultado) == {"por_estado", "mensal", "top_clientes"}
    assert list(resultado["top_clientes"].index[:2]) == ["Elisa Lima", "Karina Barbosa"]
    assert resultado["top_clientes"].iloc[0] == pytest.approx(8658.35)
    assert resultado["por_estado"]["faturamento"].sum() == pytest.approx(87063.88, abs=0.02)

from pathlib import Path

import pytest

from solucao import (
    analisar_experimento,
    decidir,
    divisao_balanceada,
    evolucao_do_p,
    intervalo_diferenca,
    tamanho_amostra_por_grupo,
    taxa_conversao,
    teste_duas_proporcoes,
)

CSV = Path(__file__).parent.parent / "data" / "experimento.csv"


def test_taxa_conversao():
    assert taxa_conversao(50, 1000) == pytest.approx(0.05)
    with pytest.raises(ValueError):
        taxa_conversao(0, 0)  # sem visitantes
    with pytest.raises(ValueError):
        taxa_conversao(120, 100)  # mais conversões que visitantes


def test_teste_duas_proporcoes():
    resultado = teste_duas_proporcoes(1000, 10000, 1130, 10050)
    assert resultado["taxa_a"] == pytest.approx(0.10)
    assert resultado["taxa_b"] == pytest.approx(0.112438, abs=1e-6)
    assert resultado["diferenca"] == pytest.approx(0.012438, abs=1e-6)
    assert resultado["z"] == pytest.approx(2.85776, abs=1e-5)
    assert resultado["p"] == pytest.approx(0.004266, abs=1e-6)


def test_teste_duas_proporcoes_sem_diferenca():
    resultado = teste_duas_proporcoes(500, 5000, 500, 5000)
    assert resultado["z"] == pytest.approx(0.0)
    assert resultado["p"] == pytest.approx(1.0)


def test_intervalo_diferenca():
    inferior, superior = intervalo_diferenca(1000, 10000, 1130, 10050)
    assert inferior == pytest.approx(0.003910, abs=1e-6)
    assert superior == pytest.approx(0.020965, abs=1e-6)
    inferior90, superior90 = intervalo_diferenca(1000, 10000, 1130, 10050, confianca=0.90)
    assert inferior90 > inferior and superior90 < superior  # menos confiança, intervalo mais estreito


def test_tamanho_amostra_por_grupo():
    assert tamanho_amostra_por_grupo(0.10, 0.02) == 3839  # de 10% para 12%
    assert tamanho_amostra_por_grupo(0.10, 0.01) == 14749  # metade do efeito, quase 4 vezes a amostra
    assert tamanho_amostra_por_grupo(0.10, 0.02, poder=0.90) == 5139


def test_divisao_balanceada():
    assert divisao_balanceada(10000, 10050) is True
    assert divisao_balanceada(10000, 10500) is False  # 48,8% x 51,2% com 20 mil visitantes: suspeito


def test_decidir():
    assert decidir(1000, 10000, 1130, 10050) == "vence_b"
    assert decidir(1130, 10050, 1000, 10000) == "vence_a"
    assert decidir(1000, 10000, 1010, 10000) == "inconclusivo"


def test_decidir_com_divisao_desbalanceada():
    # B converte bem mais, mas a divisão de tráfego falhou: o resultado não é confiável
    assert decidir(1000, 10000, 1200, 10500) == "divisao_desbalanceada"


def test_analisar_experimento():
    resultado = analisar_experimento(CSV)
    assert (resultado["visitantes_a"], resultado["conversoes_a"]) == (10051, 997)
    assert (resultado["visitantes_b"], resultado["conversoes_b"]) == (10021, 1108)
    assert resultado["taxa_a"] == pytest.approx(0.0992)
    assert resultado["taxa_b"] == pytest.approx(0.1106)
    assert resultado["diferenca"] == pytest.approx(0.0114)
    assert resultado["p"] == pytest.approx(0.0085)
    assert resultado["intervalo"] == pytest.approx((0.0029, 0.0199))
    assert resultado["decisao"] == "vence_b"


def test_evolucao_do_p():
    evolucao = evolucao_do_p(CSV)
    assert len(evolucao) == 14  # um valor p por dia, com os dados acumulados até aquele dia
    assert evolucao[0] == pytest.approx(0.5208)
    assert evolucao[2] == pytest.approx(0.0240)  # quem parasse no 3º dia já "teria resultado"
    assert evolucao[7] == pytest.approx(0.2001)  # e no 8º dia teria desistido
    assert evolucao[-1] == pytest.approx(0.0085)

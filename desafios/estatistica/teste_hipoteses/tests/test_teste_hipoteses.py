from pathlib import Path

import pytest

from solucao import (
    analisar_pacotes,
    intervalo_confianca_media,
    rejeita_h0,
    teste_z_media,
    teste_z_proporcao,
    valor_p,
)

CSV = Path(__file__).parent.parent / "data" / "pacotes.csv"
AMOSTRA = [10, 12] * 18  # 36 valores, média 11, desvio padrão amostral 1,0142


def test_valor_p_bilateral():
    assert valor_p(1.96) == pytest.approx(0.05, abs=1e-3)
    assert valor_p(-1.96) == pytest.approx(0.05, abs=1e-3)  # bilateral: o sinal não importa
    assert valor_p(0) == pytest.approx(1.0)


def test_valor_p_unilateral():
    assert valor_p(1.645, "maior") == pytest.approx(0.05, abs=1e-3)
    assert valor_p(-1.645, "menor") == pytest.approx(0.05, abs=1e-3)
    assert valor_p(1.645, "menor") == pytest.approx(0.95, abs=1e-3)  # lado errado: p alto


def test_valor_p_alternativa_invalida():
    with pytest.raises(ValueError):
        valor_p(1.0, "diferente")


def test_teste_z_media():
    resultado = teste_z_media(AMOSTRA, mu0=10.5)
    assert resultado["media"] == pytest.approx(11.0)
    assert resultado["desvio"] == pytest.approx(1.01419, abs=1e-5)  # amostral, divide por n - 1
    assert resultado["z"] == pytest.approx(2.95804, abs=1e-5)
    assert resultado["p"] == pytest.approx(0.003096, abs=1e-6)
    assert teste_z_media(AMOSTRA, mu0=10.5, alternativa="maior")["p"] == pytest.approx(0.001548, abs=1e-6)


def test_teste_z_media_exige_30_valores():
    with pytest.raises(ValueError):
        teste_z_media([10, 12] * 14, mu0=10.5)  # 28 valores


def test_teste_z_proporcao():
    # fornecedor garante no máximo 5% de peças com defeito; 29 de 400 tinham defeito
    resultado = teste_z_proporcao(29, 400, p0=0.05, alternativa="maior")
    assert resultado["proporcao"] == pytest.approx(0.0725)
    assert resultado["z"] == pytest.approx(2.06474, abs=1e-5)
    assert resultado["p"] == pytest.approx(0.019474, abs=1e-6)


def test_teste_z_proporcao_verifica_condicoes():
    with pytest.raises(ValueError):
        teste_z_proporcao(3, 100, p0=0.05)  # 100 x 0,05 = 5 < 10: aproximação normal não vale
    with pytest.raises(ValueError):
        teste_z_proporcao(450, 400, p0=0.05)  # mais sucessos do que tentativas


def test_rejeita_h0():
    assert rejeita_h0(0.03) is True
    assert rejeita_h0(0.03, alfa=0.01) is False
    assert rejeita_h0(0.20) is False


def test_intervalo_confianca_media():
    inferior, superior = intervalo_confianca_media(AMOSTRA)
    assert inferior == pytest.approx(10.66871, abs=1e-5)
    assert superior == pytest.approx(11.33129, abs=1e-5)
    inferior99, superior99 = intervalo_confianca_media(AMOSTRA, confianca=0.99)
    assert inferior99 < inferior and superior99 > superior  # mais confiança, intervalo mais largo


def test_analisar_pacotes():
    resultado = analisar_pacotes(CSV)
    assert resultado["n"] == 40
    assert resultado["media"] == pytest.approx(498.15)
    assert resultado["desvio"] == pytest.approx(5.13)
    assert resultado["z"] == pytest.approx(-2.28)
    assert resultado["p"] == pytest.approx(0.0226)
    assert resultado["rejeita_h0"] is True
    assert resultado["intervalo"] == pytest.approx((496.56, 499.74))
    # com alfa de 1%, a mesma evidência não basta, e o intervalo de 99% passa a incluir o 500
    rigoroso = analisar_pacotes(CSV, alfa=0.01)
    assert rigoroso["rejeita_h0"] is False
    assert rigoroso["intervalo"][0] < 500 < rigoroso["intervalo"][1]

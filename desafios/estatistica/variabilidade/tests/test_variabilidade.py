from pathlib import Path

import pytest

from solucao import (
    amplitude,
    coeficiente_variacao,
    comparar_centros,
    desvio_padrao,
    intervalo_interquartil,
    variancia,
)

CSV = Path(__file__).parent.parent / "data" / "entregas.csv"
DADOS = [2, 4, 4, 4, 5, 5, 7, 9]  # média 5, soma dos quadrados dos desvios 32


def test_amplitude():
    assert amplitude([4, 8, 15, 16, 23, 42]) == 38
    assert amplitude([7]) == 0


def test_variancia_populacional_e_amostral():
    assert variancia(DADOS, amostral=False) == pytest.approx(4.0)  # 32 / 8
    assert variancia(DADOS) == pytest.approx(32 / 7)  # amostral é o padrão: 32 / (8 - 1)


def test_desvio_padrao():
    assert desvio_padrao(DADOS, amostral=False) == pytest.approx(2.0)
    assert desvio_padrao(DADOS) == pytest.approx(2.13809, abs=1e-5)


def test_listas_pequenas_demais_levantam_erro():
    with pytest.raises(ValueError):
        amplitude([])
    with pytest.raises(ValueError):
        variancia([])
    with pytest.raises(ValueError):
        variancia([5])  # amostral com um valor só: divide por n - 1 = 0
    assert variancia([5], amostral=False) == 0


def test_coeficiente_variacao():
    assert coeficiente_variacao([10, 12, 14]) == pytest.approx(16.6667, abs=1e-4)
    # mesmo desvio padrão (10), escalas diferentes: o CV mostra que o segundo varia bem menos
    assert coeficiente_variacao([100, 110, 90]) == pytest.approx(10.0)
    assert coeficiente_variacao([1000, 1010, 990]) == pytest.approx(1.0)
    with pytest.raises(ValueError):
        coeficiente_variacao([-1, 1])  # média zero


def test_intervalo_interquartil():
    assert intervalo_interquartil([1, 2, 3, 4, 5, 6, 7, 8]) == pytest.approx(4.0)  # 6,5 - 2,5
    assert intervalo_interquartil([9, 1, 8, 2, 7, 3, 6, 4, 5]) == pytest.approx(5.0)  # 7,5 - 2,5
    with pytest.raises(ValueError):
        intervalo_interquartil([1, 2, 3])


def test_comparar_centros_medidas():
    centros = comparar_centros(CSV)["centros"]
    guarulhos, contagem = centros["Guarulhos"], centros["Contagem"]

    assert guarulhos["media"] == pytest.approx(5.0)
    assert contagem["media"] == pytest.approx(5.0)
    assert guarulhos["desvio_padrao"] == pytest.approx(0.76)
    assert contagem["desvio_padrao"] == pytest.approx(3.05)
    assert guarulhos["coeficiente_variacao"] == pytest.approx(15.12)
    assert contagem["coeficiente_variacao"] == pytest.approx(60.94)
    assert guarulhos["amplitude"] == 2
    assert contagem["amplitude"] == 9
    assert guarulhos["iqr"] == 2
    assert contagem["iqr"] == 6


def test_comparar_centros_conclusao():
    resultado = comparar_centros(CSV)
    assert resultado["centros"]["Guarulhos"]["percentual_atrasos"] == pytest.approx(0.0)
    assert resultado["centros"]["Contagem"]["percentual_atrasos"] == pytest.approx(26.7)
    assert resultado["mais_consistente"] == "Guarulhos"

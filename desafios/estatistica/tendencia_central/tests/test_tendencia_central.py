from pathlib import Path

import pytest

from solucao import (
    escolher_medida,
    media,
    mediana,
    moda,
    resumo_pedidos,
    tem_atipico,
)

CSV = Path(__file__).parent.parent / "data" / "pedidos.csv"


def test_media():
    assert media([10, 12, 12, 15, 61]) == 22
    assert media([2.5, 3.5]) == pytest.approx(3.0)


def test_media_lista_vazia_levanta_erro():
    with pytest.raises(ValueError):
        media([])
    with pytest.raises(ValueError):
        mediana([])
    with pytest.raises(ValueError):
        moda([])


def test_mediana_com_quantidade_impar_e_par():
    assert mediana([61, 10, 15, 12, 12]) == 12
    assert mediana([9, 3, 7, 5]) == 6


def test_mediana_nao_altera_a_lista_original():
    valores = [61, 10, 15, 12, 12]
    mediana(valores)
    assert valores == [61, 10, 15, 12, 12]


def test_moda():
    assert moda([1, 2, 2, 3]) == [2]
    assert moda([3, 5, 5, 7, 9, 9]) == [5, 9]
    assert moda([1, 2, 3]) == []


def test_tem_atipico():
    sem_atipico = [10, 11, 12, 13, 14, 15, 16, 17]
    assert tem_atipico(sem_atipico) is False
    assert tem_atipico([10, 11, 12, 13, 14, 15, 16, 100]) is True  # alto demais
    assert tem_atipico([-50, 10, 11, 12, 13, 14, 15, 16]) is True  # baixo demais
    assert tem_atipico([1, 2, 100]) is False  # poucos valores para julgar


def test_escolher_medida():
    assert escolher_medida([10, 11, 12, 13, 14, 15, 16, 17]) == "media"
    assert escolher_medida([10, 11, 12, 13, 14, 15, 16, 100]) == "mediana"


def test_resumo_pedidos():
    resumo = resumo_pedidos(CSV)
    assert resumo["quantidade"] == 20
    assert resumo["media"] == pytest.approx(93.03)
    assert resumo["mediana"] == pytest.approx(52.75)
    assert resumo["moda"] == [55.0]
    assert resumo["tem_atipico"] is True
    assert resumo["medida_recomendada"] == "mediana"

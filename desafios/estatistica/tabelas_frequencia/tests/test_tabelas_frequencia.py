from pathlib import Path

import pandas as pd
import pytest

from solucao import (
    cinco_numeros,
    limites_boxplot,
    numero_de_classes,
    resumo_atendimentos,
    tabela_frequencia,
    tabela_por_classes,
)

CSV = Path(__file__).parent.parent / "data" / "atendimentos.csv"


def test_tabela_frequencia_de_categorias():
    tabela = tabela_frequencia(pd.Series(["chat", "e-mail", "chat", "telefone", "chat", "e-mail"]))
    assert list(tabela.columns) == ["frequencia", "relativa", "acumulada", "relativa_acumulada"]
    assert list(tabela.index) == ["chat", "e-mail", "telefone"]
    assert tabela["frequencia"].tolist() == [3, 2, 1]
    assert tabela["relativa"].tolist() == pytest.approx([50.0, 33.3, 16.7])
    assert tabela["acumulada"].tolist() == [3, 5, 6]
    assert tabela["relativa_acumulada"].tolist() == pytest.approx([50.0, 83.3, 100.0])


def test_tabela_frequencia_de_numeros_em_ordem():
    tabela = tabela_frequencia(pd.Series([5, 3, 4, 5, 1, 5, 4]))
    assert list(tabela.index) == [1, 3, 4, 5]
    assert tabela["relativa"].tolist() == pytest.approx([14.3, 14.3, 28.6, 42.9])
    # 4 de 7 = 57,1%. Somar as relativas já arredondadas daria 57,2: calcule a partir da acumulada
    assert tabela["relativa_acumulada"].tolist() == pytest.approx([14.3, 28.6, 57.1, 100.0])


def test_numero_de_classes():
    assert numero_de_classes(1) == 1
    assert numero_de_classes(60) == 7  # 1 + log2(60) = 6,9 -> 7
    assert numero_de_classes(64) == 7  # 1 + log2(64) = 7 exato
    assert numero_de_classes(100) == 8  # 1 + log2(100) = 7,6 -> 8
    with pytest.raises(ValueError):
        numero_de_classes(0)


def test_tabela_por_classes():
    valores = [10, 12, 15, 20, 22, 29, 30, 35, 41, 50]
    classes = tabela_por_classes(valores, 4)  # largura (50 - 10) / 4 = 10
    assert [(c["inicio"], c["fim"]) for c in classes] == [(10, 20), (20, 30), (30, 40), (40, 50)]
    # 20 fica na segunda classe e 30 na terceira: o início entra, o fim não
    assert [c["frequencia"] for c in classes] == [3, 3, 2, 2]


def test_tabela_por_classes_inclui_o_maximo():
    valores = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    classes = tabela_por_classes(valores, 3)
    assert sum(c["frequencia"] for c in classes) == len(valores)
    assert classes[-1]["fim"] == pytest.approx(10)  # o 10 entra na última classe
    assert classes[0]["inicio"] == pytest.approx(1)


def test_cinco_numeros():
    assert cinco_numeros([7, 1, 3, 9, 5, 11, 13, 15]) == pytest.approx(
        {"minimo": 1, "q1": 4, "mediana": 8, "q3": 12, "maximo": 15}
    )
    assert cinco_numeros([2, 4, 6, 8, 10, 12, 14]) == pytest.approx(
        {"minimo": 2, "q1": 4, "mediana": 8, "q3": 12, "maximo": 14}
    )


def test_limites_boxplot():
    limites = limites_boxplot([1, 2, 3, 4, 5, 6, 7, 8, 9, 30])  # Q1 = 3, Q3 = 8, cerca superior 15,5
    assert limites["bigode_inferior"] == 1
    assert limites["bigode_superior"] == 9  # o maior valor dentro das cercas, e não a cerca
    assert limites["atipicos"] == [30]


def test_resumo_atendimentos():
    resumo = resumo_atendimentos(CSV)
    assert resumo["por_canal"]["frequencia"].to_dict() == {"chat": 27, "e-mail": 18, "telefone": 15}
    assert resumo["por_nota"].loc[3, "relativa_acumulada"] == pytest.approx(33.3)  # notas até 3
    assert [c["frequencia"] for c in resumo["classes_tempo"]] == [21, 32, 4, 1, 0, 0, 2]
    assert resumo["cinco_numeros_tempo"] == pytest.approx(
        {"minimo": 4, "q1": 13, "mediana": 16, "q3": 20, "maximo": 74}
    )
    assert resumo["boxplot_tempo"]["bigode_superior"] == 30
    assert resumo["boxplot_tempo"]["atipicos"] == [37, 68, 74]

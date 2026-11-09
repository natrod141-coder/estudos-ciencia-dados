from datetime import datetime
from pathlib import Path

import pandas as pd
import pytest

from solucao import (
    aplicar_regras,
    atraso_em_horas,
    decidir,
    ler_carga,
    ler_regras,
    linhas_duplicadas,
    linhas_fora_da_lista,
    linhas_fora_do_intervalo,
    linhas_nulas,
    linhas_orfas,
    separar_quarentena,
    volume_anormal,
)

DADOS = Path(__file__).parent.parent / "data"
HISTORICO = pd.read_csv(DADOS / "historico_volume.csv")["linhas"].tolist()

RESULTADOS_ESPERADOS = [
    {"regra": "pedido_id sem repetição", "severidade": "erro", "falhas": [5012]},
    {"regra": "cliente_id preenchido", "severidade": "erro", "falhas": [5020]},
    {"regra": "cliente existe no cadastro", "severidade": "erro", "falhas": [5027]},
    {"regra": "status conhecido", "severidade": "erro", "falhas": [5031]},
    {"regra": "valor entre 0 e 50 mil", "severidade": "erro", "falhas": [5035, 5038]},
    {"regra": "valor acima de 10 mil é raro", "severidade": "aviso", "falhas": [5016, 5038]},
]


def carga():
    return ler_carga(DADOS / "carga_pedidos.csv")


def tabelas():
    return {"clientes": pd.read_csv(DADOS / "clientes.csv")}


def ids(df, mascara):
    """Os pedidos das linhas marcadas, na ordem em que aparecem."""
    assert isinstance(mascara, pd.Series), "Devolva uma Series de booleanos, alinhada com o DataFrame."
    assert mascara.index.equals(df.index), "A Series precisa ter o mesmo índice do DataFrame recebido."
    return df.loc[mascara, "pedido_id"].tolist()


def test_linhas_duplicadas_marca_todas_as_copias():
    df = carga()
    assert ids(df, linhas_duplicadas(df, "pedido_id")) == [5012, 5012], (
        "O pedido 5012 chegou duas vezes: as duas cópias são marcadas."
    )


def test_linhas_nulas():
    df = carga()
    assert ids(df, linhas_nulas(df, "cliente_id")) == [5020]


def test_linhas_fora_da_lista_ignora_vazios():
    df = carga()
    assert ids(df, linhas_fora_da_lista(df, "status", ["aprovado", "cancelado", "pendente"])) == [5031]
    pequeno = pd.DataFrame({"pedido_id": [1, 2, 3], "status": ["aprovado", None, "devolvido"]})
    assert ids(pequeno, linhas_fora_da_lista(pequeno, "status", ["aprovado"])) == [3], (
        "Valor vazio não é valor fora da lista: isso é trabalho de linhas_nulas."
    )


def test_linhas_fora_do_intervalo():
    df = carga()
    assert ids(df, linhas_fora_do_intervalo(df, "valor", minimo=0, maximo=50000)) == [5035, 5038]
    assert ids(df, linhas_fora_do_intervalo(df, "valor", maximo=10000)) == [5016, 5038]
    assert ids(df, linhas_fora_do_intervalo(df, "valor", minimo=0)) == [5035]
    limites = pd.DataFrame({"pedido_id": [1, 2, 3, 4], "valor": [0.0, 100.0, None, 100.01]})
    assert ids(limites, linhas_fora_do_intervalo(limites, "valor", minimo=0, maximo=100)) == [4], (
        "Os limites são permitidos, e valor vazio não conta como falha."
    )


def test_linhas_orfas_ignora_vazios():
    df = carga()
    assert ids(df, linhas_orfas(df, "cliente_id", tabelas()["clientes"]["cliente_id"])) == [5027], (
        "O pedido 5027 aponta para o cliente 999, que não existe. O 5020, sem cliente, é outro problema."
    )


def test_atraso_em_horas():
    assert atraso_em_horas(carga(), "atualizado_em", datetime(2026, 3, 11, 6, 0)) == pytest.approx(6 + 2 / 60), (
        "A última atualização da carga foi às 23:58 do dia 10."
    )


def test_volume_anormal():
    assert volume_anormal(HISTORICO, 40) is False
    assert volume_anormal(HISTORICO, 12) is True, "Uma carga com 12 linhas, quando o normal é cerca de 40."
    assert volume_anormal(HISTORICO, 47) is True
    assert volume_anormal(HISTORICO, 46) is False


def test_aplicar_regras_na_carga_do_dia():
    df = carga()
    copia = df.copy()
    assert aplicar_regras(df, ler_regras(DADOS / "regras.json"), tabelas()) == RESULTADOS_ESPERADOS
    pd.testing.assert_frame_equal(df, copia, obj="Não altere a carga recebida.")


def test_separar_quarentena():
    df = carga()
    aprovadas, quarentena = separar_quarentena(df, RESULTADOS_ESPERADOS)
    assert quarentena["pedido_id"].tolist() == [5012, 5012, 5020, 5027, 5031, 5035, 5038], (
        "Vão para a quarentena as linhas com falha de erro, inclusive as duas cópias do 5012."
    )
    assert len(aprovadas) == 33
    assert 5016 in aprovadas["pedido_id"].tolist(), "Falha de aviso não manda o pedido para a quarentena."
    assert len(df) == 40, "Não altere a carga recebida."


def test_decidir_bloqueia_a_carga_do_dia():
    total = carga()["pedido_id"].nunique()
    assert decidir(RESULTADOS_ESPERADOS, total) == "bloquear", (
        "Seis dos 39 pedidos têm falha de erro, cerca de 15%: passa do limite de 5%."
    )


def test_decidir_outros_casos():
    nenhuma = [{"regra": "a", "severidade": "erro", "falhas": []}, {"regra": "b", "severidade": "aviso", "falhas": []}]
    so_aviso = [{"regra": "a", "severidade": "erro", "falhas": []}, {"regra": "b", "severidade": "aviso", "falhas": [7]}]
    poucas = [{"regra": "a", "severidade": "erro", "falhas": [7, 9]}, {"regra": "b", "severidade": "erro", "falhas": [9]}]
    assert decidir(nenhuma, 100) == "publicar"
    assert decidir(so_aviso, 100) == "publicar_com_aviso"
    assert decidir(poucas, 100) == "publicar_sem_as_ruins", "Dois pedidos em 100, sem contar o 9 duas vezes."
    assert decidir(poucas, 30) == "bloquear"

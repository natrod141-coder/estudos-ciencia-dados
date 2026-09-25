from pathlib import Path

import pandas as pd
import pytest

from solucao import (
    amostra_aleatoria_simples,
    amostra_estratificada,
    amostra_sistematica,
    avaliar_amostras,
    erro_de_composicao,
    margem_de_erro,
    tamanho_amostra,
    tamanhos_por_estrato,
)

CSV = Path(__file__).parent.parent / "data" / "clientes.csv"


@pytest.fixture
def clientes():
    return pd.read_csv(CSV)


def test_amostra_aleatoria_simples(clientes):
    amostra = amostra_aleatoria_simples(clientes, 50, semente=1)
    assert len(amostra) == 50
    assert amostra["id_cliente"].is_unique  # sem repetir cliente
    assert amostra["id_cliente"].isin(clientes["id_cliente"]).all()
    # mesma semente, mesma amostra; semente diferente, outra amostra
    assert amostra_aleatoria_simples(clientes, 50, semente=1).equals(amostra)
    assert not amostra_aleatoria_simples(clientes, 50, semente=2).equals(amostra)


def test_amostra_maior_que_a_populacao_levanta_erro(clientes):
    with pytest.raises(ValueError):
        amostra_aleatoria_simples(clientes, 1001, semente=1)


def test_amostra_sistematica(clientes):
    amostra = amostra_sistematica(clientes, 100, inicio=3)  # k = 1000 // 100 = 10
    assert len(amostra) == 100
    assert amostra["id_cliente"].tolist()[:3] == [4, 14, 24]
    assert amostra["id_cliente"].tolist()[-1] == 994
    assert len(amostra_sistematica(clientes, 30)) == 30  # k = 33 daria 31 linhas: fique com as 30 primeiras


def test_amostra_sistematica_inicio_invalido(clientes):
    with pytest.raises(ValueError):
        amostra_sistematica(clientes, 100, inicio=10)  # com k = 10, o início vai de 0 a 9
    with pytest.raises(ValueError):
        amostra_sistematica(clientes, 100, inicio=-1)


def test_tamanhos_por_estrato(clientes):
    assert tamanhos_por_estrato(clientes, "regiao", 100) == {
        "Centro-Oeste": 8, "Nordeste": 27, "Norte": 8, "Sudeste": 42, "Sul": 15,
    }
    # 30 x 42% = 12,6 e 30 x 15% = 4,5: as duas vagas que sobram vão para os maiores restos
    assert tamanhos_por_estrato(clientes, "regiao", 30) == {
        "Centro-Oeste": 2, "Nordeste": 8, "Norte": 2, "Sudeste": 13, "Sul": 5,
    }
    # empate de restos (0,56 e 0,56): vence a ordem alfabética
    assert tamanhos_por_estrato(clientes, "regiao", 7) == {
        "Centro-Oeste": 1, "Nordeste": 2, "Norte": 0, "Sudeste": 3, "Sul": 1,
    }


def test_amostra_estratificada(clientes):
    amostra = amostra_estratificada(clientes, "regiao", 100, semente=42)
    assert len(amostra) == 100
    assert amostra["id_cliente"].is_unique
    assert amostra["regiao"].value_counts().to_dict() == {
        "Sudeste": 42, "Nordeste": 27, "Sul": 15, "Centro-Oeste": 8, "Norte": 8,
    }
    assert amostra_estratificada(clientes, "regiao", 100, semente=42).equals(amostra)


def test_erro_de_composicao():
    populacao = pd.DataFrame({"plano": ["basico", "basico", "premium", "premium"]})
    so_basico = pd.DataFrame({"plano": ["basico", "basico"]})  # premium não aparece: conta como 0%
    assert erro_de_composicao(populacao, so_basico, "plano") == pytest.approx(50.0)
    assert erro_de_composicao(populacao, populacao, "plano") == pytest.approx(0.0)


def test_margem_de_erro():
    assert margem_de_erro(0.5, 400) == pytest.approx(0.049)
    assert margem_de_erro(0.2, 1000) == pytest.approx(0.02479, abs=1e-5)
    # quatro vezes mais entrevistas, metade da margem de erro
    assert margem_de_erro(0.5, 1600) == pytest.approx(margem_de_erro(0.5, 400) / 2)


def test_tamanho_amostra():
    assert tamanho_amostra(0.05) == 385
    assert tamanho_amostra(0.03) == 1068
    assert tamanho_amostra(0.05, p=0.1) == 139
    assert tamanho_amostra(0.05, z=2.576) == 664  # 99% de confiança


def test_avaliar_amostras():
    erros = avaliar_amostras(CSV)
    assert erros["primeiras_linhas"] == pytest.approx(72.0)  # só Centro-Oeste e Nordeste
    assert erros["sistematica"] == pytest.approx(0.0)
    assert erros["estratificada"] == pytest.approx(0.0)
    assert 0 < erros["aleatoria_simples"] < 10

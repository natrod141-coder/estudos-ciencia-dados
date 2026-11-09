from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from solucao import (
    CATEGORICAS,
    NUMERICAS,
    auc,
    auc_com_vazamento,
    colunas_suspeitas,
    criar_variaveis,
    montar_pipeline,
    montar_preprocessamento,
    separar,
)

BRUTA = pd.read_csv(Path(__file__).parent.parent / "data" / "assinaturas_brutas.csv")


def partes():
    return separar(criar_variaveis(BRUTA), ["data_cancelamento"])


def test_colunas_suspeitas():
    assert colunas_suspeitas(BRUTA) == ["data_cancelamento"], (
        "data_cancelamento só existe para quem cancelou: é informação do futuro."
    )


def test_criar_variaveis():
    pequeno = pd.DataFrame({
        "data_inicio": ["2026-03-31", "2026-09-01", "2023-09-30"],
        "nota_satisfacao": [4.0, np.nan, 2.0],
    })
    novo = criar_variaveis(pequeno)
    assert novo["meses_assinatura"].tolist() == [6, 0, 36]
    assert novo["nota_respondida"].tolist() == [1, 0, 1]
    assert "data_inicio" not in novo.columns
    assert "data_inicio" in pequeno.columns, "Não altere a tabela recebida."


def test_separar():
    X_treino, X_teste, y_treino, y_teste = partes()
    assert len(X_teste) == 1250
    for coluna in ("cancelou", "cliente_id", "data_cancelamento"):
        assert coluna not in X_treino.columns
    assert set(NUMERICAS + CATEGORICAS) <= set(X_treino.columns)
    assert y_treino.mean() == pytest.approx(y_teste.mean(), abs=0.002)


def test_preprocessamento_preenche_e_agrupa_as_cidades_raras():
    X_treino, X_teste, _, _ = partes()
    preparo = montar_preprocessamento(NUMERICAS, CATEGORICAS).fit(X_treino)
    saida = preparo.transform(X_teste)
    assert not np.isnan(saida).any(), "Depois do preparo, não pode sobrar vazio."
    nomes = list(preparo.get_feature_names_out())
    cidades = [nome for nome in nomes if "cidade" in nome]
    assert len(cidades) <= 8, "As 40 cidades pequenas viram uma categoria só."
    assert any("infrequent" in nome for nome in cidades)


def test_estatisticas_vem_so_do_treino():
    X_treino, _, y_treino, _ = partes()
    modelo = montar_pipeline().fit(X_treino, y_treino)
    imputador = modelo.named_steps["preparo"].named_transformers_["numericas"].named_steps["imputar"]
    assert imputador.statistics_[NUMERICAS.index("idade")] == pytest.approx(X_treino["idade"].median()), (
        "A mediana usada para preencher vem só do treino."
    )


def test_categoria_nova_nao_quebra_o_modelo():
    X_treino, X_teste, y_treino, _ = partes()
    modelo = montar_pipeline().fit(X_treino, y_treino)
    novo = X_teste.head(3).copy()
    novo["cidade"] = "Cidade que nunca apareceu"
    probs = modelo.predict_proba(novo)[:, 1]
    assert ((probs > 0) & (probs < 1)).all()


def test_modelo_sem_vazamento():
    X_treino, X_teste, y_treino, y_teste = partes()
    copia = X_treino.copy()
    modelo = montar_pipeline().fit(X_treino, y_treino)
    pd.testing.assert_frame_equal(X_treino, copia, obj="O pipeline não pode alterar a tabela recebida.")
    resultado = auc(modelo, X_teste, y_teste)
    assert 0.66 < resultado < 0.8, "Um resultado realista: bom, mas longe de perfeito."


def test_vazamento_da_um_resultado_bom_demais():
    assert auc_com_vazamento(BRUTA) > 0.97, (
        "Com a data de cancelamento, o modelo 'acerta' quase tudo: ele está lendo a resposta."
    )

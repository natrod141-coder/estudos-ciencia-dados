"""Desafio: uma nota que não depende da sorte.

Uma divisão de treino e teste é um sorteio, e outro sorteio daria outra nota. Você vai medir
essa variação, usar a validação cruzada para ter uma estimativa mais firme, ver um vazamento
clássico transformar dados sem sentido num modelo "ótimo" e escolher hiperparâmetros com uma
busca em grade, guardando o teste para o fim.

Regras:
- Use pandas, numpy e scikit-learn. Nenhuma função pode alterar o que recebe.
- Não altere a pasta tests nem os arquivos em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeClassifier


def preparar(df):
    """Já está pronta: (X, y) com plano e canal em colunas 0 ou 1, como no tópico de regressão logística."""
    X = pd.get_dummies(df.drop(columns=["cliente_id", "cancelou"]), columns=["plano", "canal"], drop_first=True, dtype=int)
    return X, df["cancelou"]


def dados_de_ruido(n=300, p=2000, semente=0):
    """Já está pronta: n linhas com p colunas de números sorteados e um alvo sorteado, 0 ou 1.

    Nenhuma coluna tem relação com o alvo. Nenhum modelo honesto passa muito de AUC 0,5 aqui.
    """
    gerador = np.random.default_rng(semente)
    return gerador.normal(size=(n, p)), gerador.integers(0, 2, n)


def auc_em_divisoes(X, y, sementes):
    """Para cada semente, separa 25% para teste (estratificado, random_state=semente), treina uma
    LogisticRegression(max_iter=5000) e mede a AUC no teste. Devolve a lista de AUCs."""
    raise NotImplementedError("Implemente a função auc_em_divisoes")


def validacao_cruzada(modelo, X, y, k=5, semente=42):
    """As AUCs de cada parte numa validação cruzada estratificada.

    Use StratifiedKFold(n_splits=k, shuffle=True, random_state=semente) e cross_val_score com
    scoring="roc_auc". Devolve o array com uma AUC por parte.
    """
    raise NotImplementedError("Implemente a função validacao_cruzada")


def resumo(notas):
    """Devolve {"media": ..., "desvio": ...}, com a média e o desvio padrão (np.std) das notas, como floats."""
    raise NotImplementedError("Implemente a função resumo")


def selecao_antes_de_dividir(X, y, k=20, semente=0):
    """O jeito errado: escolhe as k colunas mais relacionadas com o alvo usando todos os dados,
    com SelectKBest(f_classif, k=k), e só depois faz a validação cruzada de uma
    LogisticRegression(max_iter=2000) com as colunas escolhidas.
    Devolve a média das AUCs de validacao_cruzada(..., semente=semente)."""
    raise NotImplementedError("Implemente a função selecao_antes_de_dividir")


def selecao_dentro_do_pipeline(X, y, k=20, semente=0):
    """O jeito certo: coloca a seleção dentro de um pipeline,
    make_pipeline(SelectKBest(f_classif, k=k), LogisticRegression(max_iter=2000)), e faz a
    validação cruzada do pipeline inteiro. Assim, em cada parte, a seleção só vê os dados de
    treino daquela parte. Devolve a média das AUCs de validacao_cruzada(..., semente=semente)."""
    raise NotImplementedError("Implemente a função selecao_dentro_do_pipeline")


def busca_em_grade(X, y, semente=42):
    """Procura a melhor árvore com validação cruzada e devolve o GridSearchCV já treinado.

    Modelo: DecisionTreeClassifier(random_state=semente). Grade: max_depth em [4, 5, 6, 8] e
    min_samples_leaf em [1, 20, 50]. Validação: StratifiedKFold(5, shuffle=True,
    random_state=semente), com scoring="roc_auc". Depois da busca, o GridSearchCV treina de novo
    o melhor modelo com todos os dados recebidos.
    """
    raise NotImplementedError("Implemente a função busca_em_grade")


def auc_final(grade, X_teste, y_teste):
    """A AUC do melhor modelo da busca no conjunto de teste, usado só agora, uma vez."""
    raise NotImplementedError("Implemente a função auc_final")

"""Gabarito do desafio "Uma nota que não depende da sorte".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
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
    resultados = []
    for semente in sementes:
        X_treino, X_teste, y_treino, y_teste = train_test_split(
            X, y, test_size=0.25, random_state=semente, stratify=y
        )
        modelo = LogisticRegression(max_iter=5000).fit(X_treino, y_treino)
        resultados.append(roc_auc_score(y_teste, modelo.predict_proba(X_teste)[:, 1]))
    return resultados


def validacao_cruzada(modelo, X, y, k=5, semente=42):
    partes = StratifiedKFold(n_splits=k, shuffle=True, random_state=semente)
    return cross_val_score(modelo, X, y, cv=partes, scoring="roc_auc")


def resumo(notas):
    return {"media": float(np.mean(notas)), "desvio": float(np.std(notas))}


def selecao_antes_de_dividir(X, y, k=20, semente=0):
    # errado de propósito: a seleção olha o alvo de todas as linhas, inclusive as que vão ser teste
    escolhidas = SelectKBest(f_classif, k=k).fit_transform(X, y)
    return float(validacao_cruzada(LogisticRegression(max_iter=2000), escolhidas, y, semente=semente).mean())


def selecao_dentro_do_pipeline(X, y, k=20, semente=0):
    pipeline = make_pipeline(SelectKBest(f_classif, k=k), LogisticRegression(max_iter=2000))
    return float(validacao_cruzada(pipeline, X, y, semente=semente).mean())


def busca_em_grade(X, y, semente=42):
    grade = GridSearchCV(
        DecisionTreeClassifier(random_state=semente),
        {"max_depth": [4, 5, 6, 8], "min_samples_leaf": [1, 20, 50]},
        cv=StratifiedKFold(5, shuffle=True, random_state=semente),
        scoring="roc_auc",
    )
    return grade.fit(X, y)


def auc_final(grade, X_teste, y_teste):
    return roc_auc_score(y_teste, grade.predict_proba(X_teste)[:, 1])

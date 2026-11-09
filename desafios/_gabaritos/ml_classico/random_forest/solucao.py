"""Gabarito do desafio "Muitas árvores votando juntas".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split


def preparar(df):
    X = pd.get_dummies(df.drop(columns=["cliente_id", "cancelou"]), columns=["plano", "canal"], dtype=int)
    return X, df["cancelou"]


def dividir(X, y, semente=42):
    return train_test_split(X, y, test_size=0.25, random_state=semente, stratify=y)


def treinar_floresta(X, y, n_arvores=300, semente=42):
    floresta = RandomForestClassifier(
        n_estimators=n_arvores, min_samples_leaf=5, oob_score=True, random_state=semente, n_jobs=-1
    )
    return floresta.fit(X, y)


def auc_teste(modelo, X, y):
    return roc_auc_score(y, modelo.predict_proba(X)[:, 1])


def auc_oob(floresta, y_treino):
    return roc_auc_score(y_treino, floresta.oob_decision_function_[:, 1])


def curva_de_arvores(X_treino, y_treino, X_teste, y_teste, quantidades, semente=42):
    linhas = []
    for n in quantidades:
        floresta = RandomForestClassifier(n_estimators=n, min_samples_leaf=5, random_state=semente, n_jobs=-1)
        floresta.fit(X_treino, y_treino)
        linhas.append({"n_arvores": n, "auc_teste": auc_teste(floresta, X_teste, y_teste)})
    return pd.DataFrame(linhas)


def concordancia(modelo_a, modelo_b, X):
    a = modelo_a.predict_proba(X)[:, 1]
    b = modelo_b.predict_proba(X)[:, 1]
    return float(np.corrcoef(a, b)[0, 1])


def importancia_por_impureza(modelo, colunas):
    return pd.Series(modelo.feature_importances_, index=list(colunas)).sort_values(ascending=False)


def importancia_por_permutacao(modelo, X, y, semente=42):
    resultado = permutation_importance(modelo, X, y, scoring="roc_auc", n_repeats=5, random_state=semente, n_jobs=-1)
    return pd.Series(resultado.importances_mean, index=X.columns).sort_values(ascending=False)

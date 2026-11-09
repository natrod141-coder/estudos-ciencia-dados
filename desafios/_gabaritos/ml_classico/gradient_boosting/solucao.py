"""Gabarito do desafio "Árvores que corrigem os erros das anteriores".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split


def preparar(df):
    X = df.drop(columns=["cliente_id", "cancelou"]).astype({"plano": "category", "canal": "category"})
    return X, df["cancelou"]


def dividir_em_tres(X, y, semente=42):
    X_resto, X_teste, y_resto, y_teste = train_test_split(X, y, test_size=0.2, random_state=semente, stratify=y)
    X_treino, X_val, y_treino, y_val = train_test_split(
        X_resto, y_resto, test_size=0.25, random_state=semente, stratify=y_resto
    )
    return X_treino, X_val, X_teste, y_treino, y_val, y_teste


def treinar_boosting(X, y, taxa=0.1, iteracoes=300, semente=42):
    modelo = HistGradientBoostingClassifier(
        learning_rate=taxa,
        max_iter=iteracoes,
        early_stopping=False,
        categorical_features="from_dtype",
        random_state=semente,
    )
    return modelo.fit(X, y)


def auc(modelo, X, y):
    return roc_auc_score(y, modelo.predict_proba(X)[:, 1])


def curva_de_validacao(modelo, X_val, y_val):
    return [float(roc_auc_score(y_val, probs[:, 1])) for probs in modelo.staged_predict_proba(X_val)]


def melhor_iteracao(curva):
    return int(np.argmax(curva)) + 1


def treinar_com_parada_antecipada(X, y, taxa=0.05, semente=42):
    modelo = HistGradientBoostingClassifier(
        learning_rate=taxa,
        max_iter=2000,
        early_stopping=True,
        validation_fraction=0.2,
        n_iter_no_change=20,
        categorical_features="from_dtype",
        random_state=semente,
    )
    return modelo.fit(X, y)


def com_faltantes(X, coluna, fracao, semente=42):
    resultado = X.copy()
    sorteio = np.random.default_rng(semente).random(len(X)) < fracao
    resultado.loc[sorteio, coluna] = np.nan
    return resultado

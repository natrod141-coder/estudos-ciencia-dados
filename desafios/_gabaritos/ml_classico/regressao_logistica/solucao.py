"""Gabarito do desafio "Quem vai cancelar a assinatura".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def preparar(df):
    X = pd.get_dummies(df.drop(columns=["cliente_id", "cancelou"]), columns=["plano", "canal"], drop_first=True, dtype=int)
    return X, df["cancelou"]


def dividir(X, y, semente=42):
    return train_test_split(X, y, test_size=0.25, random_state=semente, stratify=y)


def ajustar(X, y):
    return LogisticRegression(max_iter=5000).fit(X, y)


def probabilidades(modelo, X):
    return modelo.predict_proba(X)[:, 1]


def classificar(probs, limiar=0.5):
    return (np.asarray(probs) >= limiar).astype(int)


def matriz_confusao(y_real, y_previsto):
    real, previsto = np.asarray(y_real), np.asarray(y_previsto)
    return {
        "vp": int(((real == 1) & (previsto == 1)).sum()),
        "fp": int(((real == 0) & (previsto == 1)).sum()),
        "fn": int(((real == 1) & (previsto == 0)).sum()),
        "vn": int(((real == 0) & (previsto == 0)).sum()),
    }


def acuracia_ingenua(y):
    return float(pd.Series(y).value_counts(normalize=True).max())


def razoes_de_chance(modelo, colunas):
    return {coluna: float(np.exp(coef)) for coluna, coef in zip(colunas, modelo.coef_[0])}


def clientes_mais_arriscados(df, probs, n=10):
    resultado = df.copy()
    resultado["prob_cancelar"] = np.asarray(probs)
    return resultado.sort_values("prob_cancelar", ascending=False).head(n)

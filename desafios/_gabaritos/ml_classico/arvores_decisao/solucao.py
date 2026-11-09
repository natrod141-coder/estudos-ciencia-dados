"""Gabarito do desafio "Uma árvore que se explica, e que decora".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text


def preparar(df):
    X = pd.get_dummies(df.drop(columns=["cliente_id", "cancelou"]), columns=["plano", "canal"], dtype=int)
    return X, df["cancelou"]


def dividir_em_tres(X, y, semente=42):
    X_resto, X_teste, y_resto, y_teste = train_test_split(X, y, test_size=0.2, random_state=semente, stratify=y)
    X_treino, X_val, y_treino, y_val = train_test_split(
        X_resto, y_resto, test_size=0.25, random_state=semente, stratify=y_resto
    )
    return X_treino, X_val, X_teste, y_treino, y_val, y_teste


def treinar_arvore(X, y, profundidade=None, semente=42):
    return DecisionTreeClassifier(max_depth=profundidade, random_state=semente).fit(X, y)


def auc(modelo, X, y):
    return roc_auc_score(y, modelo.predict_proba(X)[:, 1])


def curva_de_profundidade(X_treino, y_treino, X_val, y_val, profundidades):
    linhas = []
    for profundidade in profundidades:
        arvore = treinar_arvore(X_treino, y_treino, profundidade)
        linhas.append({
            "profundidade": profundidade,
            "auc_treino": auc(arvore, X_treino, y_treino),
            "auc_validacao": auc(arvore, X_val, y_val),
        })
    return pd.DataFrame(linhas)


def melhor_profundidade(curva):
    melhor = curva["auc_validacao"].max()
    empatadas = curva.loc[curva["auc_validacao"] == melhor, "profundidade"].tolist()
    limitadas = [p for p in empatadas if p is not None and not pd.isna(p)]
    # entre as empatadas, a árvore mais simples
    return int(min(limitadas)) if limitadas else None


def regras(modelo, colunas):
    return export_text(modelo, feature_names=list(colunas))


def importancias(modelo, colunas):
    return pd.Series(modelo.feature_importances_, index=list(colunas)).sort_values(ascending=False)

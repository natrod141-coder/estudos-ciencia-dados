"""Gabarito do desafio "Do dado cru ao modelo, sem vazamento".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

REFERENCIA = "2026-09-30"  # a data em que a base foi extraída
NUMERICAS = [
    "idade", "meses_assinatura", "valor_mensal", "acessos_mes", "chamados_suporte",
    "atrasos_pagamento", "usa_app", "nota_satisfacao", "nota_respondida",
]
CATEGORICAS = ["plano", "canal", "cidade"]


def colunas_suspeitas(df, alvo="cancelou", limite=0.9):
    suspeitas = []
    for coluna in df.columns.drop(alvo):
        preenchida = df[coluna].notna()
        diferenca = abs(preenchida[df[alvo] == 1].mean() - preenchida[df[alvo] == 0].mean())
        if diferenca > limite:
            suspeitas.append(coluna)
    return sorted(suspeitas)


def criar_variaveis(df, referencia=REFERENCIA):
    resultado = df.copy()
    dias = (pd.Timestamp(referencia) - pd.to_datetime(resultado["data_inicio"])).dt.days
    resultado["meses_assinatura"] = (dias / 30.44).astype(int)
    resultado["nota_respondida"] = resultado["nota_satisfacao"].notna().astype(int)
    return resultado.drop(columns=["data_inicio"])


def separar(df, colunas_a_remover, alvo="cancelou", semente=42):
    X = df.drop(columns=[alvo, "cliente_id", *colunas_a_remover])
    return train_test_split(X, df[alvo], test_size=0.25, random_state=semente, stratify=df[alvo])


def montar_preprocessamento(numericas, categoricas):
    numerico = Pipeline([("imputar", SimpleImputer(strategy="median")), ("padronizar", StandardScaler())])
    categorico = OneHotEncoder(handle_unknown="infrequent_if_exist", min_frequency=0.02, sparse_output=False)
    return ColumnTransformer([("numericas", numerico, list(numericas)), ("categoricas", categorico, list(categoricas))])


def montar_pipeline(numericas=NUMERICAS, categoricas=CATEGORICAS):
    return Pipeline([
        ("preparo", montar_preprocessamento(numericas, categoricas)),
        ("modelo", LogisticRegression(max_iter=2000)),
    ])


def auc(modelo, X, y):
    return roc_auc_score(y, modelo.predict_proba(X)[:, 1])


def auc_com_vazamento(df, semente=42):
    dados = criar_variaveis(df)
    dados["tem_data_cancelamento"] = dados["data_cancelamento"].notna().astype(int)
    X_treino, X_teste, y_treino, y_teste = separar(dados, ["data_cancelamento"], semente=semente)
    modelo = montar_pipeline([*NUMERICAS, "tem_data_cancelamento"]).fit(X_treino, y_treino)
    return auc(modelo, X_teste, y_teste)

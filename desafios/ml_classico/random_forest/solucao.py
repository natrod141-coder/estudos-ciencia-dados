"""Desafio: muitas árvores votando juntas.

Com os mesmos clientes dos tópicos anteriores, você vai treinar uma random forest, ver que ela
erra menos e é bem mais estável que uma árvore sozinha, usar a estimativa fora da sacola (OOB)
no lugar de um conjunto de validação, e comparar duas formas de medir a importância das
variáveis: uma delas engana.

Regras:
- Use pandas, numpy e scikit-learn. Nenhuma função pode alterar o que recebe.
- Não altere a pasta tests nem os arquivos em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split


def preparar(df):
    """Devolve (X, y): X sem cliente_id e cancelou, com plano e canal em colunas 0 ou 1
    (pd.get_dummies com columns=["plano", "canal"] e dtype=int); y é a coluna cancelou."""
    raise NotImplementedError("Implemente a função preparar")


def dividir(X, y, semente=42):
    """Separa 25% para teste, estratificando por y. Devolve X_treino, X_teste, y_treino, y_teste."""
    raise NotImplementedError("Implemente a função dividir")


def treinar_floresta(X, y, n_arvores=300, semente=42):
    """Treina uma RandomForestClassifier com n_estimators=n_arvores, min_samples_leaf=5,
    oob_score=True, random_state=semente e n_jobs=-1 (usa todos os núcleos do computador)."""
    raise NotImplementedError("Implemente a função treinar_floresta")


def auc_teste(modelo, X, y):
    """A AUC do modelo nos dados: roc_auc_score com a probabilidade da classe 1."""
    raise NotImplementedError("Implemente a função auc_teste")


def auc_oob(floresta, y_treino):
    """A AUC fora da sacola: roc_auc_score de y_treino com a coluna da classe 1 de
    floresta.oob_decision_function_. Cada cliente de treino é avaliado só pelas árvores que não
    o viram."""
    raise NotImplementedError("Implemente a função auc_oob")


def curva_de_arvores(X_treino, y_treino, X_teste, y_teste, quantidades, semente=42):
    """Treina uma floresta para cada quantidade de árvores e mede a AUC no teste.

    Use RandomForestClassifier(n_estimators=n, min_samples_leaf=5, random_state=semente,
    n_jobs=-1), sem oob_score. Devolve um DataFrame com as colunas n_arvores e auc_teste.
    """
    raise NotImplementedError("Implemente a função curva_de_arvores")


def concordancia(modelo_a, modelo_b, X):
    """A correlação de Pearson entre as probabilidades que os dois modelos dão aos mesmos clientes.

    Perto de 1, os dois modelos concordam sobre quem tem mais risco. Devolve um float.
    """
    raise NotImplementedError("Implemente a função concordancia")


def importancia_por_impureza(modelo, colunas):
    """feature_importances_ numa Series com os nomes das colunas, da maior para a menor."""
    raise NotImplementedError("Implemente a função importancia_por_impureza")


def importancia_por_permutacao(modelo, X, y, semente=42):
    """A importância por permutação: quanto a AUC cai quando os valores de cada coluna são
    embaralhados. Use permutation_importance com scoring="roc_auc", n_repeats=5,
    random_state=semente e n_jobs=-1. Devolva importances_mean numa Series com os nomes das
    colunas de X, da maior para a menor."""
    raise NotImplementedError("Implemente a função importancia_por_permutacao")

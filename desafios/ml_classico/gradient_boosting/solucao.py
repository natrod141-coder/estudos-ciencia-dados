"""Desafio: árvores que corrigem os erros das anteriores.

Com os mesmos clientes dos tópicos anteriores, você vai treinar um gradient boosting, ver que,
ao contrário da random forest, ele sobreajusta quando ganha árvores demais, acompanhar a curva de
validação a cada iteração, usar a parada antecipada e aproveitar dois recursos do
HistGradientBoostingClassifier: categorias e valores faltantes sem pré-processamento.

Regras:
- Use pandas, numpy e scikit-learn. Nenhuma função pode alterar o que recebe.
- Não altere a pasta tests nem os arquivos em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split


def preparar(df):
    """Devolve (X, y), sem transformar as categorias em colunas de 0 e 1.

    X: a tabela sem cliente_id e cancelou, com as colunas plano e canal convertidas para o tipo
    "category" do pandas. O boosting vai tratar essas colunas como categorias, sozinho.
    y: a coluna cancelou.
    """
    raise NotImplementedError("Implemente a função preparar")


def dividir_em_tres(X, y, semente=42):
    """Treino (60%), validação (20%) e teste (20%), estratificando por y, como no tópico de árvores.

    Primeiro 20% para teste; depois, do resto, 25% para validação. Use random_state=semente.
    Devolve X_treino, X_val, X_teste, y_treino, y_val, y_teste.
    """
    raise NotImplementedError("Implemente a função dividir_em_tres")


def treinar_boosting(X, y, taxa=0.1, iteracoes=300, semente=42):
    """Treina um HistGradientBoostingClassifier com learning_rate=taxa, max_iter=iteracoes,
    early_stopping=False (para treinar todas as iterações), categorical_features="from_dtype"
    e random_state=semente."""
    raise NotImplementedError("Implemente a função treinar_boosting")


def auc(modelo, X, y):
    """A AUC do modelo nos dados: roc_auc_score com a probabilidade da classe 1."""
    raise NotImplementedError("Implemente a função auc")


def curva_de_validacao(modelo, X_val, y_val):
    """A AUC na validação depois de cada iteração do boosting, numa lista de floats.

    modelo.staged_predict_proba(X_val) devolve as probabilidades depois da 1ª árvore, das 2
    primeiras, das 3 primeiras, e assim por diante.
    """
    raise NotImplementedError("Implemente a função curva_de_validacao")


def melhor_iteracao(curva):
    """O número da iteração com a maior AUC, contando a partir de 1. No empate, a primeira."""
    raise NotImplementedError("Implemente a função melhor_iteracao")


def treinar_com_parada_antecipada(X, y, taxa=0.05, semente=42):
    """Treina um HistGradientBoostingClassifier que para sozinho quando a validação interna para
    de melhorar: learning_rate=taxa, max_iter=2000, early_stopping=True,
    validation_fraction=0.2, n_iter_no_change=20, categorical_features="from_dtype" e
    random_state=semente. Depois do treino, modelo.n_iter_ diz quantas iterações ele usou."""
    raise NotImplementedError("Implemente a função treinar_com_parada_antecipada")


def com_faltantes(X, coluna, fracao, semente=42):
    """Devolve uma cópia de X com uma fração das linhas da coluna trocadas por vazio (NaN).

    Sorteie as linhas com np.random.default_rng(semente).random(len(X)) < fracao.
    """
    raise NotImplementedError("Implemente a função com_faltantes")

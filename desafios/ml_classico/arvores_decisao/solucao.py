"""Desafio: uma árvore que se explica, e que decora.

Com os mesmos clientes do tópico de regressão logística, você vai treinar árvores de decisão,
ver uma árvore sem limite decorar o treino, escolher a profundidade num conjunto de validação,
ler as regras que a árvore aprendeu e medir o resultado final no teste.

Regras:
- Use pandas e scikit-learn. Nenhuma função pode alterar o que recebe.
- Não altere a pasta tests nem os arquivos em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text


def preparar(df):
    """Devolve (X, y): X sem cliente_id e cancelou, com plano e canal em colunas 0 ou 1
    (pd.get_dummies com columns=["plano", "canal"] e dtype=int, sem drop_first: árvores não
    precisam de categoria de referência); y é a coluna cancelou."""
    raise NotImplementedError("Implemente a função preparar")


def dividir_em_tres(X, y, semente=42):
    """Separa treino (60%), validação (20%) e teste (20%), sempre estratificando por y.

    Primeiro separe 20% para teste. Depois, do que sobrou, separe 25% para validação (25% de 80%
    são 20% do total). Use random_state=semente nas duas divisões.
    Devolve X_treino, X_val, X_teste, y_treino, y_val, y_teste.
    """
    raise NotImplementedError("Implemente a função dividir_em_tres")


def treinar_arvore(X, y, profundidade=None, semente=42):
    """Treina uma DecisionTreeClassifier com max_depth=profundidade e random_state=semente."""
    raise NotImplementedError("Implemente a função treinar_arvore")


def auc(modelo, X, y):
    """A AUC do modelo nos dados: roc_auc_score com a probabilidade da classe 1."""
    raise NotImplementedError("Implemente a função auc")


def curva_de_profundidade(X_treino, y_treino, X_val, y_val, profundidades):
    """Treina uma árvore para cada profundidade e mede a AUC no treino e na validação.

    Devolve um DataFrame com as colunas profundidade, auc_treino e auc_validacao, uma linha por
    profundidade, na ordem recebida. A profundidade None quer dizer árvore sem limite.
    """
    raise NotImplementedError("Implemente a função curva_de_profundidade")


def melhor_profundidade(curva):
    """A profundidade com a maior auc_validacao. No empate, a menor profundidade, que dá a
    árvore mais simples. A profundidade None (sem limite) só vence se for a única melhor."""
    raise NotImplementedError("Implemente a função melhor_profundidade")


def regras(modelo, colunas):
    """As regras da árvore em texto, com export_text e os nomes das colunas."""
    raise NotImplementedError("Implemente a função regras")


def importancias(modelo, colunas):
    """A importância de cada variável (feature_importances_), numa Series com os nomes das
    colunas no índice, da mais importante para a menos importante."""
    raise NotImplementedError("Implemente a função importancias")

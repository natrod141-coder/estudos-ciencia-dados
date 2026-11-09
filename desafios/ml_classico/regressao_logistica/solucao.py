"""Desafio: quem vai cancelar a assinatura.

O time de retenção quer uma lista dos clientes com mais risco de cancelar, para oferecer ajuda
antes que eles saiam. Você vai treinar uma regressão logística com 5 mil clientes, transformar
probabilidades em decisões com um limiar, medir os acertos e os erros e ler as razões de chance.

Regras:
- Use pandas, numpy e scikit-learn. Nenhuma função pode alterar o que recebe.
- Não altere a pasta tests nem os arquivos em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def preparar(df):
    """Devolve (X, y).

    X: a tabela sem cliente_id e sem cancelou, com plano e canal transformados em colunas 0 ou 1
    por pd.get_dummies(..., columns=["plano", "canal"], drop_first=True, dtype=int).
    y: a coluna cancelou.
    """
    raise NotImplementedError("Implemente a função preparar")


def dividir(X, y, semente=42):
    """Separa 25% para teste com train_test_split, estratificando por y (stratify=y).

    Assim, a proporção de cancelamentos fica igual no treino e no teste.
    Devolve X_treino, X_teste, y_treino, y_teste.
    """
    raise NotImplementedError("Implemente a função dividir")


def ajustar(X, y):
    """Treina e devolve uma LogisticRegression(max_iter=5000)."""
    raise NotImplementedError("Implemente a função ajustar")


def probabilidades(modelo, X):
    """Devolve a probabilidade de cancelar de cada cliente: a coluna da classe 1 de predict_proba."""
    raise NotImplementedError("Implemente a função probabilidades")


def classificar(probs, limiar=0.5):
    """Transforma probabilidades em decisões: 1 se a probabilidade for maior ou igual ao limiar."""
    raise NotImplementedError("Implemente a função classificar")


def matriz_confusao(y_real, y_previsto):
    """Conta os acertos e os erros. Devolve {"vp": ..., "fp": ..., "fn": ..., "vn": ...}.

    vp: cancelou e o modelo previu cancelamento. fp: não cancelou, mas o modelo previu.
    fn: cancelou, mas o modelo não previu. vn: não cancelou e o modelo não previu.
    Os valores são int do Python.
    """
    raise NotImplementedError("Implemente a função matriz_confusao")


def acuracia_ingenua(y):
    """A acurácia de prever sempre a classe mais comum: a proporção da classe mais frequente."""
    raise NotImplementedError("Implemente a função acuracia_ingenua")


def razoes_de_chance(modelo, colunas):
    """Devolve {coluna: razão de chance}, em que a razão de chance é exp(coeficiente).

    Acima de 1, a variável aumenta a chance de cancelar; abaixo de 1, diminui.
    Os valores são float do Python.
    """
    raise NotImplementedError("Implemente a função razoes_de_chance")


def clientes_mais_arriscados(df, probs, n=10):
    """Devolve os n clientes com maior probabilidade de cancelar, do maior risco para o menor.

    df é a tabela original desses clientes. Devolva uma cópia com a coluna nova "prob_cancelar".
    """
    raise NotImplementedError("Implemente a função clientes_mais_arriscados")

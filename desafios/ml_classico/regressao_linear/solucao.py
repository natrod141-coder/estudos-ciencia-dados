"""Desafio: quanto tempo leva uma entrega.

A empresa de entregas quer avisar o cliente, na hora da compra, quanto tempo o pedido vai levar.
Você vai treinar uma regressão linear com 600 entregas passadas, medir o erro no conjunto de teste,
comparar com uma previsão ingênua e interpretar os coeficientes.

Regras:
- Use pandas, numpy e scikit-learn. Nenhuma função pode alterar o que recebe.
- Não altere a pasta tests nem os arquivos em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

COLUNAS = ["distancia_km", "peso_kg", "itens", "chuva", "horario_pico", "regiao_norte", "regiao_sul"]


def codificar(df):
    """Monta a matriz de variáveis X a partir da tabela de entregas.

    Tire pedido_id e tempo_min (o alvo) e transforme regiao em colunas 0 ou 1 com
    pd.get_dummies(..., drop_first=True, dtype=int). A região centro fica como referência:
    é a que não ganha coluna. Devolva as colunas na ordem de COLUNAS.
    """
    raise NotImplementedError("Implemente a função codificar")


def dividir(X, y, proporcao_teste=0.2, semente=42):
    """Separa treino e teste com train_test_split. Devolve X_treino, X_teste, y_treino, y_teste."""
    raise NotImplementedError("Implemente a função dividir")


def ajustar(X, y):
    """Treina e devolve uma LinearRegression."""
    raise NotImplementedError("Implemente a função ajustar")


def coeficientes(modelo, colunas):
    """Devolve {"intercepto": valor, coluna: coeficiente, ...}, com floats do Python."""
    raise NotImplementedError("Implemente a função coeficientes")


def avaliar(y_real, y_previsto):
    """Devolve {"mae": ..., "rmse": ..., "r2": ...}.

    MAE: média dos erros absolutos. RMSE: raiz da média dos erros ao quadrado.
    R²: 1 menos a soma dos erros ao quadrado dividida pela soma dos desvios de y_real
    em relação à média de y_real.
    """
    raise NotImplementedError("Implemente a função avaliar")


def avaliar_baseline(y_treino, y_teste):
    """Avalia, com a função avaliar, a previsão ingênua: prever sempre a média de y_treino."""
    raise NotImplementedError("Implemente a função avaliar_baseline")


def prever_tempo(modelo, distancia_km, peso_kg, itens, chuva, horario_pico, regiao):
    """Prevê o tempo de uma entrega, em minutos, a partir dos dados dela.

    regiao é "centro", "norte" ou "sul". Monte um DataFrame de uma linha com as COLUNAS, na
    mesma ordem do treino, e devolva a previsão como float.
    """
    raise NotImplementedError("Implemente a função prever_tempo")


def piores_previsoes(df_teste, y_previsto, n=5):
    """Devolve as n entregas com o maior erro absoluto, da maior para a menor.

    df_teste é a tabela original das entregas de teste, com tempo_min. Devolva uma cópia com a
    coluna nova "erro", igual a tempo_min menos a previsão, ordenada pelo tamanho do erro.
    """
    raise NotImplementedError("Implemente a função piores_previsoes")

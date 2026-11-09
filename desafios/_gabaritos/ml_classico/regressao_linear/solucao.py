"""Gabarito do desafio "Quanto tempo leva uma entrega".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

COLUNAS = ["distancia_km", "peso_kg", "itens", "chuva", "horario_pico", "regiao_norte", "regiao_sul"]


def codificar(df):
    X = pd.get_dummies(df.drop(columns=["pedido_id", "tempo_min"]), columns=["regiao"], drop_first=True, dtype=int)
    return X[COLUNAS]


def dividir(X, y, proporcao_teste=0.2, semente=42):
    return train_test_split(X, y, test_size=proporcao_teste, random_state=semente)


def ajustar(X, y):
    return LinearRegression().fit(X, y)


def coeficientes(modelo, colunas):
    resultado = {"intercepto": float(modelo.intercept_)}
    resultado.update({coluna: float(coef) for coluna, coef in zip(colunas, modelo.coef_)})
    return resultado


def avaliar(y_real, y_previsto):
    y_real, y_previsto = np.asarray(y_real, dtype=float), np.asarray(y_previsto, dtype=float)
    erro = y_real - y_previsto
    return {
        "mae": float(np.mean(np.abs(erro))),
        "rmse": float(np.sqrt(np.mean(erro**2))),
        "r2": float(1 - np.sum(erro**2) / np.sum((y_real - y_real.mean()) ** 2)),
    }


def avaliar_baseline(y_treino, y_teste):
    previsao = np.full(len(y_teste), np.mean(y_treino))
    return avaliar(y_teste, previsao)


def prever_tempo(modelo, distancia_km, peso_kg, itens, chuva, horario_pico, regiao):
    linha = pd.DataFrame([{
        "distancia_km": distancia_km,
        "peso_kg": peso_kg,
        "itens": itens,
        "chuva": chuva,
        "horario_pico": horario_pico,
        "regiao_norte": int(regiao == "norte"),
        "regiao_sul": int(regiao == "sul"),
    }])[COLUNAS]
    return float(modelo.predict(linha)[0])


def piores_previsoes(df_teste, y_previsto, n=5):
    resultado = df_teste.copy()
    resultado["erro"] = resultado["tempo_min"] - np.asarray(y_previsto)
    ordem = resultado["erro"].abs().sort_values(ascending=False).index
    return resultado.loc[ordem].head(n)

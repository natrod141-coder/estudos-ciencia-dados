"""Gabarito do desafio "Escolher o limiar pelo dinheiro".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

DADOS = Path(__file__).parent / "data" / "assinaturas.csv"


def probabilidades_de_teste():
    """Já está pronta: devolve (y_teste, probs), dois arrays do numpy, para os clientes de teste."""
    df = pd.read_csv(DADOS)
    X = pd.get_dummies(df.drop(columns=["cliente_id", "cancelou"]), columns=["plano", "canal"], drop_first=True, dtype=int)
    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X, df["cancelou"], test_size=0.25, random_state=42, stratify=df["cancelou"]
    )
    modelo = LogisticRegression(max_iter=5000).fit(X_treino, y_treino)
    return y_teste.to_numpy(), modelo.predict_proba(X_teste)[:, 1]


def contar(y, probs, limiar):
    real, risco = np.asarray(y) == 1, np.asarray(probs) >= limiar
    return {
        "vp": int((real & risco).sum()),
        "fp": int((~real & risco).sum()),
        "fn": int((real & ~risco).sum()),
        "vn": int((~real & ~risco).sum()),
    }


def dividir(a, b):
    return a / b if b else 0.0


def precisao_recall_f1(contagem):
    precisao = dividir(contagem["vp"], contagem["vp"] + contagem["fp"])
    recall = dividir(contagem["vp"], contagem["vp"] + contagem["fn"])
    return {"precisao": precisao, "recall": recall, "f1": dividir(2 * precisao * recall, precisao + recall)}


def auc_por_pares(y, probs):
    y, probs = np.asarray(y), np.asarray(probs)
    positivos, negativos = probs[y == 1], probs[y == 0]
    # cada linha é um cliente que cancelou, cada coluna, um que ficou
    maior = (positivos[:, None] > negativos[None, :]).sum()
    empate = (positivos[:, None] == negativos[None, :]).sum()
    return float((maior + 0.5 * empate) / (len(positivos) * len(negativos)))


def tabela_de_limiares(y, probs, limiares):
    linhas = []
    for limiar in limiares:
        contagem = contar(y, probs, limiar)
        medidas = precisao_recall_f1(contagem)
        linhas.append({
            "limiar": limiar,
            "lista": contagem["vp"] + contagem["fp"],
            "precisao": medidas["precisao"],
            "recall": medidas["recall"],
        })
    return pd.DataFrame(linhas)


def lucro(contagem, valor_cliente=400, custo_contato=40, taxa_sucesso=0.3):
    contatados = contagem["vp"] + contagem["fp"]
    return contagem["vp"] * taxa_sucesso * valor_cliente - contatados * custo_contato


def melhor_limiar(y, probs, limiares, valor_cliente=400, custo_contato=40, taxa_sucesso=0.3):
    lucros = [lucro(contar(y, probs, limiar), valor_cliente, custo_contato, taxa_sucesso) for limiar in limiares]
    return limiares[int(np.argmax(lucros))]


def precisao_no_topo(y, probs, k):
    y = np.asarray(y)
    topo = np.argsort(-np.asarray(probs), kind="stable")[:k]
    return float(y[topo].mean()), float(y[topo].sum() / y.sum())


def calibracao(y, probs, faixas=5):
    tabela = pd.DataFrame({"faixa": pd.qcut(probs, faixas, labels=False), "prob": probs, "real": y})
    resumo = tabela.groupby("faixa").agg(prob_media=("prob", "mean"), taxa_real=("real", "mean"))
    return resumo.reset_index(drop=True)

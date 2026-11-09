"""Desafio: escolher o limiar pelo dinheiro.

O modelo de cancelamento está pronto: a função probabilidades_de_teste treina uma regressão
logística e devolve, para 1.250 clientes de teste, se cancelaram e a probabilidade que o modelo
deu a cada um. Você vai calcular as métricas à mão, entender o que cada uma mede, escolher o
limiar que dá mais lucro para a campanha de retenção e conferir se as probabilidades são
confiáveis.

Regras:
- Use numpy e pandas. Nas métricas, faça as contas você mesmo: os testes comparam com o
  scikit-learn.
- Nenhuma função pode alterar o que recebe. Não altere a pasta tests nem os arquivos em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
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
    """Com a regra "risco se a probabilidade for maior ou igual ao limiar", conta
    {"vp": ..., "fp": ..., "fn": ..., "vn": ...}, como ints do Python."""
    raise NotImplementedError("Implemente a função contar")


def precisao_recall_f1(contagem):
    """Devolve {"precisao": ..., "recall": ..., "f1": ...} a partir da contagem.

    precisão = vp / (vp + fp); recall = vp / (vp + fn); f1 = 2 x precisão x recall /
    (precisão + recall). Quando um denominador for zero, a medida vale 0.0.
    """
    raise NotImplementedError("Implemente a função precisao_recall_f1")


def auc_por_pares(y, probs):
    """A AUC calculada pela definição: a proporção de pares (cliente que cancelou, cliente que
    ficou) em que o que cancelou recebeu probabilidade maior. Empates valem meio ponto."""
    raise NotImplementedError("Implemente a função auc_por_pares")


def tabela_de_limiares(y, probs, limiares):
    """Um DataFrame com uma linha por limiar e as colunas limiar, lista (quantos clientes ficam
    acima do limiar), precisao e recall."""
    raise NotImplementedError("Implemente a função tabela_de_limiares")


def lucro(contagem, valor_cliente=400, custo_contato=40, taxa_sucesso=0.3):
    """O lucro da campanha de retenção para uma contagem.

    Cada cliente da lista (vp + fp) recebe um contato que custa custo_contato. Dos que iam
    cancelar e foram contatados (vp), uma fração taxa_sucesso fica, e cada um que fica vale
    valor_cliente. Lucro = vp x taxa_sucesso x valor_cliente - (vp + fp) x custo_contato.
    """
    raise NotImplementedError("Implemente a função lucro")


def melhor_limiar(y, probs, limiares, valor_cliente=400, custo_contato=40, taxa_sucesso=0.3):
    """O limiar, entre os recebidos, que dá o maior lucro. No empate, o primeiro da lista."""
    raise NotImplementedError("Implemente a função melhor_limiar")


def precisao_no_topo(y, probs, k):
    """Para uma lista com os k clientes de maior probabilidade, devolve (precisao, recall):
    a proporção da lista que cancelou e a proporção dos cancelamentos que a lista pegou."""
    raise NotImplementedError("Implemente a função precisao_no_topo")


def calibracao(y, probs, faixas=5):
    """Confere se as probabilidades são confiáveis.

    Divida os clientes em faixas de tamanho igual pela probabilidade, com
    pd.qcut(probs, faixas, labels=False), e devolva um DataFrame com uma linha por faixa, da
    menor probabilidade para a maior, e as colunas prob_media (a média das probabilidades da
    faixa) e taxa_real (a proporção de cancelamentos da faixa).
    """
    raise NotImplementedError("Implemente a função calibracao")

"""Desafio: do dado cru ao modelo, sem vazamento.

A base de assinaturas chegou crua: datas no lugar de meses de assinatura, idades e notas
faltando, dezenas de cidades com poucos clientes e uma coluna que entrega a resposta. Você vai
encontrar o vazamento, criar as variáveis, montar um pipeline do scikit-learn que prepara os
dados aprendendo só com o treino, e ver o que acontece quando o vazamento passa despercebido.

Regras:
- Use pandas, numpy e scikit-learn. Nenhuma função pode alterar o que recebe.
- Não altere a pasta tests nem os arquivos em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
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
    """Lista as colunas que só estão preenchidas para uma das classes do alvo.

    Para cada coluna, menos o alvo, calcule a proporção de valores preenchidos entre as linhas
    com alvo 1 e entre as linhas com alvo 0. Se a diferença, em valor absoluto, passar do
    limite, a coluna é suspeita: ela provavelmente só existe depois que o evento aconteceu.
    Devolva a lista em ordem alfabética.
    """
    raise NotImplementedError("Implemente a função colunas_suspeitas")


def criar_variaveis(df, referencia=REFERENCIA):
    """Devolve uma cópia da tabela com duas colunas novas e sem data_inicio.

    - meses_assinatura: os dias entre data_inicio e a referência, divididos por 30.44, sem as
      casas decimais (int). Ex.: de 2026-03-31 a 2026-09-30 são 183 dias, ou 6 meses.
    - nota_respondida: 1 se nota_satisfacao estiver preenchida, 0 se estiver vazia. Às vezes
      não responder já é uma informação.
    """
    raise NotImplementedError("Implemente a função criar_variaveis")


def separar(df, colunas_a_remover, alvo="cancelou", semente=42):
    """Tira o alvo, cliente_id e as colunas_a_remover de X, e separa 25% para teste,
    estratificando pelo alvo. Devolve X_treino, X_teste, y_treino, y_teste."""
    raise NotImplementedError("Implemente a função separar")


def montar_preprocessamento(numericas, categoricas):
    """Um ColumnTransformer com dois tratamentos:

    - "numericas": um Pipeline com SimpleImputer(strategy="median"), que preenche os vazios
      com a mediana, e StandardScaler(), que padroniza.
    - "categoricas": OneHotEncoder(handle_unknown="infrequent_if_exist", min_frequency=0.02,
      sparse_output=False). Categorias com menos de 2% das linhas viram uma categoria só, de
      "raras", e categorias que só aparecem depois do treino caem nela também.
    """
    raise NotImplementedError("Implemente a função montar_preprocessamento")


def montar_pipeline(numericas=NUMERICAS, categoricas=CATEGORICAS):
    """Um Pipeline com o pré-processamento ("preparo") e uma LogisticRegression(max_iter=2000)
    ("modelo"). Ao chamar fit, o pipeline aprende as medianas, as escalas e as categorias só com
    os dados de treino."""
    raise NotImplementedError("Implemente a função montar_pipeline")


def auc(modelo, X, y):
    """A AUC do modelo nos dados: roc_auc_score com a probabilidade da classe 1."""
    raise NotImplementedError("Implemente a função auc")


def auc_com_vazamento(df, semente=42):
    """Mostra o estrago de um vazamento: devolve a AUC no teste de um modelo que usa a
    informação da data de cancelamento.

    Partindo de criar_variaveis(df), crie a coluna tem_data_cancelamento (1 se
    data_cancelamento estiver preenchida, 0 se não), separe com separar(...,
    ["data_cancelamento"], semente=semente) e treine montar_pipeline com NUMERICAS mais
    tem_data_cancelamento.
    """
    raise NotImplementedError("Implemente a função auc_com_vazamento")

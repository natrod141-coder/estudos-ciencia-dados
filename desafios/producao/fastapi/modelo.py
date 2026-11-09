"""Já está pronto: lê o modelo de cancelamento gravado em JSON e calcula as probabilidades.

Não altere este arquivo. O treino está em treinar_modelo.py.
"""

import json
import math

# Quantas vezes o modelo foi lido do disco. Os testes usam este número para conferir que a API
# carrega o modelo uma vez só, na inicialização, e não a cada requisição.
CARREGAMENTOS = {"total": 0}


class ModeloDeCancelamento:
    def __init__(self, parametros):
        self.versao = parametros["versao"]
        self._numericas = parametros["numericas"]
        self._categoricas = parametros["categoricas"]
        self._coeficientes = parametros["coeficientes"]
        self._intercepto = parametros["intercepto"]

    def prever(self, clientes):
        """Recebe uma lista de dicionários, um por cliente, e devolve a lista de probabilidades
        de cancelamento, na mesma ordem."""
        return [self._probabilidade(cliente) for cliente in clientes]

    def _probabilidade(self, cliente):
        z = self._intercepto
        for coluna, escala in self._numericas.items():
            valor = float(cliente[coluna])  # True e False viram 1.0 e 0.0
            z += self._coeficientes[coluna] * (valor - escala["media"]) / escala["desvio"]
        for coluna in self._categoricas:
            z += self._coeficientes[f"{coluna}={cliente[coluna]}"]
        return 1 / (1 + math.exp(-z))


def carregar_modelo(caminho):
    """Lê o arquivo do modelo. É uma operação lenta num modelo de verdade: faça uma vez só."""
    CARREGAMENTOS["total"] += 1
    with open(caminho, encoding="utf-8") as arquivo:
        return ModeloDeCancelamento(json.load(arquivo))

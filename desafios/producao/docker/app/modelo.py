"""O mesmo modelo de cancelamento do desafio de FastAPI, lido do JSON."""

import json
import math


class ModeloDeCancelamento:
    def __init__(self, parametros):
        self.versao = parametros["versao"]
        self._numericas = parametros["numericas"]
        self._categoricas = parametros["categoricas"]
        self._coeficientes = parametros["coeficientes"]
        self._intercepto = parametros["intercepto"]

    def prever(self, clientes):
        return [self._probabilidade(cliente) for cliente in clientes]

    def _probabilidade(self, cliente):
        z = self._intercepto
        for coluna, escala in self._numericas.items():
            z += self._coeficientes[coluna] * (float(cliente[coluna]) - escala["media"]) / escala["desvio"]
        for coluna in self._categoricas:
            z += self._coeficientes[f"{coluna}={cliente[coluna]}"]
        return 1 / (1 + math.exp(-z))


def carregar_modelo(caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        return ModeloDeCancelamento(json.load(arquivo))

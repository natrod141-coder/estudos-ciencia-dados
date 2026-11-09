"""Um cliente que imita o do SDK da Anthropic, com uma resposta gravada. Não altere este arquivo.

Ele anota cada chamada em `chamadas` e devolve sempre o mesmo texto. Com `falha` igual a
"limite" ou "conexao", ele levanta o mesmo erro que o SDK levantaria: anthropic.RateLimitError
(status 429) ou anthropic.APIConnectionError. Os dois são subclasses de anthropic.APIError.
"""

from types import SimpleNamespace

import anthropic
import httpx2

PEDIDO = httpx2.Request("POST", "https://api.anthropic.com/v1/messages")


class _Mensagens:
    def __init__(self, cliente):
        self._cliente = cliente

    def create(self, **parametros):
        return self._cliente._responder(parametros)


class LLMGravado:
    def __init__(self, texto="", falha=None):
        self.messages = _Mensagens(self)
        self.chamadas = []
        self._texto = texto
        self._falha = falha

    def _responder(self, parametros):
        self.chamadas.append(parametros)
        if self._falha == "limite":
            resposta = httpx2.Response(429, request=PEDIDO)
            raise anthropic.RateLimitError("Limite de requisições atingido.", response=resposta, body=None)
        if self._falha == "conexao":
            raise anthropic.APIConnectionError(request=PEDIDO)
        return SimpleNamespace(
            content=[SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=self._texto)],
            stop_reason="end_turn",
            usage=SimpleNamespace(input_tokens=180, output_tokens=60),
        )

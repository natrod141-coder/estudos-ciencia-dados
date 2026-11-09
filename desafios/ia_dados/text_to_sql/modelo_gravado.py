"""Um cliente que imita o do SDK da Anthropic, com respostas gravadas. Não altere este arquivo.

Para cada pergunta de data/perguntas.json, ele devolve a resposta que um modelo deu, no mesmo
formato das respostas de verdade. Assim o desafio roda sem chave de API e sem custo. Para usar o
modelo de verdade, troque ModeloGravado() por anthropic.Anthropic().
"""

import json
from pathlib import Path
from types import SimpleNamespace

PERGUNTAS = Path(__file__).parent / "data" / "perguntas.json"


class _Mensagens:
    def __init__(self, cliente):
        self._cliente = cliente

    def create(self, **parametros):
        return self._cliente._responder(parametros)


class ModeloGravado:
    def __init__(self):
        self.messages = _Mensagens(self)
        self.chamadas = []
        self._gravadas = json.loads(PERGUNTAS.read_text(encoding="utf-8"))

    def _responder(self, parametros):
        self.chamadas.append(parametros)
        conteudo = parametros["messages"][-1]["content"]
        texto = next(
            (item["resposta_gravada"] for item in self._gravadas if item["pergunta"] in conteudo),
            "Não sei responder a essa pergunta.",
        )
        return SimpleNamespace(
            content=[SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=texto)],
            stop_reason="end_turn",
        )

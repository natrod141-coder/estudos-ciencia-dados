"""Um cliente que imita o do SDK da Anthropic, com respostas gravadas. Não altere este arquivo.

Em vez de chamar a API, ele devolve as respostas gravadas em data/respostas_gravadas.json, com o
mesmo formato das respostas de verdade: content com blocos, stop_reason e usage. Assim o desafio
roda sem chave de API e sem custo, e os testes sabem exatamente o que esperar.

O uso é o mesmo do SDK:
    cliente = ClienteGravado()
    resposta = cliente.messages.create(model=..., max_tokens=..., messages=[...])

Para trocar pelo cliente de verdade, basta usar anthropic.Anthropic() no lugar de ClienteGravado().
"""

import json
from pathlib import Path
from types import SimpleNamespace

GRAVACOES = Path(__file__).parent / "data" / "respostas_gravadas.json"
PARAMETROS_REMOVIDOS = ("temperature", "top_p", "top_k")
MENSAGENS_DE_ERRO = {
    400: "a requisição tem um problema e não vai funcionar se for repetida",
    429: "limite de requisições por minuto atingido, tente de novo em instantes",
    500: "erro interno da API",
    529: "a API está sobrecarregada, tente de novo em instantes",
}


class ErroDaApi(Exception):
    """Faz o papel de anthropic.APIStatusError: o código HTTP do erro fica em status_code."""

    def __init__(self, status_code, mensagem=""):
        super().__init__(f"Erro {status_code}: {mensagem or MENSAGENS_DE_ERRO.get(status_code, 'erro da API')}")
        self.status_code = status_code


class _Mensagens:
    def __init__(self, cliente):
        self._cliente = cliente

    def create(self, **parametros):
        return self._cliente._responder(parametros)


class ClienteGravado:
    def __init__(self, falhas=()):
        """falhas: códigos HTTP que as próximas chamadas levantam, um por chamada, em ordem."""
        self.messages = _Mensagens(self)
        self.chamadas = []
        self._falhas = list(falhas)
        self._gravacoes = json.loads(GRAVACOES.read_text(encoding="utf-8"))

    def _responder(self, parametros):
        self.chamadas.append(parametros)
        if self._falhas:
            raise ErroDaApi(self._falhas.pop(0))
        for nome in ("model", "max_tokens", "messages"):
            if nome not in parametros:
                raise ErroDaApi(400, f"falta o parâmetro {nome}")
        for nome in PARAMETROS_REMOVIDOS:
            if nome in parametros:
                raise ErroDaApi(400, f"{nome}: este parâmetro não é mais aceito pela API")
        mensagens = parametros["messages"]
        if not mensagens or mensagens[0].get("role") != "user":
            raise ErroDaApi(400, "a primeira mensagem precisa ser do usuário")
        pergunta = mensagens[-1]["content"]
        if not isinstance(pergunta, str):
            pergunta = " ".join(bloco.get("text", "") for bloco in pergunta)
        for gravacao in self._gravacoes:
            if gravacao["avaliacao"] in pergunta:
                return _resposta(gravacao, parametros["model"])
        raise ErroDaApi(400, "não há resposta gravada para esta mensagem")


def _resposta(gravacao, modelo):
    return SimpleNamespace(
        model=modelo,
        content=[SimpleNamespace(**bloco) for bloco in gravacao["content"]],
        stop_reason=gravacao["stop_reason"],
        usage=SimpleNamespace(**gravacao["usage"]),
    )

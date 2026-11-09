"""Um cliente que imita o do SDK da Anthropic num agente com ferramentas. Não altere este arquivo.

Para cada pergunta conhecida, ele segue um roteiro gravado: pede ferramentas (stop_reason
"tool_use", com blocos tool_use) e, no fim, responde em texto (stop_reason "end_turn"). Como a API
de verdade, ele confere a conversa que recebe:
- a lista de ferramentas precisa vir em tools;
- depois de uma resposta com tool_use, a mensagem seguinte, do usuário, precisa trazer um
  tool_result para cada tool_use, com o mesmo id, todos na mesma mensagem.
Se algo estiver fora do formato, ele levanta ErroDaApi com status_code 400.
"""

from types import SimpleNamespace

PERGUNTAS = {
    "receita": "Qual foi a receita de março por região?",
    "apagar": "Apague as vendas canceladas, elas atrapalham as análises.",
    "relatorio": "Mande para a diretoria o total de vendas aprovadas em março.",
    "laco": "Fique conferindo as tabelas até alguém mandar parar.",
}

SQL_RECEITA = (
    "SELECT l.regiao, ROUND(SUM(v.valor), 2) AS receita FROM vendas AS v "
    "JOIN lojas AS l ON l.loja_id = v.loja_id WHERE v.status = 'aprovada' AND month(v.data) = 3 "
    "GROUP BY l.regiao ORDER BY receita DESC"
)
SQL_TOTAL = "SELECT ROUND(SUM(valor), 2) AS total FROM vendas WHERE status = 'aprovada' AND month(data) = 3"

ROTEIROS = {
    PERGUNTAS["receita"]: [
        [("listar_tabelas", {})],
        [("descrever_tabela", {"tabela": "vendas"}), ("descrever_tabela", {"tabela": "lojas"})],
        [("consultar_sql", {"sql": SQL_RECEITA})],
        "Em março, considerando só as vendas aprovadas, a receita foi de R$ 7.464,60 no Sudeste, "
        "R$ 6.919,20 no Nordeste e R$ 3.358,70 no Sul.",
    ],
    PERGUNTAS["apagar"]: [
        [("consultar_sql", {"sql": "DELETE FROM vendas WHERE status = 'cancelada'"})],
        "Não consigo apagar dados: tenho acesso só de leitura ao banco. Se quiser, posso mostrar as "
        "análises filtrando as vendas canceladas.",
    ],
    PERGUNTAS["relatorio"]: [
        [("consultar_sql", {"sql": SQL_TOTAL})],
        [("enviar_relatorio", {
            "destinatario": "diretoria@empresa.com.br",
            "texto": "Total de vendas aprovadas em março: R$ 17.742,50.",
        })],
        {
            "enviado": "Enviei para a diretoria o total de vendas aprovadas em março: R$ 17.742,50.",
            "pendente": "O total de vendas aprovadas em março é de R$ 17.742,50. Preparei o relatório para "
                        "a diretoria, mas o envio está aguardando a aprovação de uma pessoa.",
        },
    ],
}


class ErroDaApi(Exception):
    """Faz o papel de anthropic.APIStatusError: o código HTTP do erro fica em status_code."""

    def __init__(self, status_code, mensagem):
        super().__init__(f"Erro {status_code}: {mensagem}")
        self.status_code = status_code


def _campo(bloco, nome):
    return bloco.get(nome) if isinstance(bloco, dict) else getattr(bloco, nome, None)


class _Mensagens:
    def __init__(self, cliente):
        self._cliente = cliente

    def create(self, **parametros):
        return self._cliente._responder(parametros)


class AgenteGravado:
    def __init__(self):
        self.messages = _Mensagens(self)
        self.chamadas = []
        self._proximo_id = 1

    def _conferir_resultados(self, mensagens):
        anteriores = [m for m in mensagens if m["role"] == "assistant"]
        if not anteriores:
            return None
        pedidos = [_campo(b, "id") for b in anteriores[-1]["content"] if _campo(b, "type") == "tool_use"]
        ultima = mensagens[-1]
        if ultima["role"] != "user" or not isinstance(ultima["content"], list):
            raise ErroDaApi(400, "depois de um tool_use, a mensagem seguinte precisa ser do usuário, com tool_result")
        resultados = [b for b in ultima["content"] if _campo(b, "type") == "tool_result"]
        if sorted(_campo(b, "tool_use_id") for b in resultados) != sorted(pedidos):
            raise ErroDaApi(400, "cada tool_use precisa de um tool_result com o mesmo id, na mesma mensagem")
        return resultados

    def _responder(self, parametros):
        self.chamadas.append(parametros)
        if not parametros.get("tools"):
            raise ErroDaApi(400, "envie a lista de ferramentas em tools")
        if _campo(parametros.get("tool_choice") or {}, "type") in ("any", "tool"):
            raise ErroDaApi(400, "tool_choice any ou tool não é aceito neste modelo: use auto")
        mensagens = parametros["messages"]
        resultados = self._conferir_resultados(mensagens)
        pergunta = mensagens[0]["content"]
        passo = sum(1 for m in mensagens if m["role"] == "assistant")
        if pergunta == PERGUNTAS["laco"]:
            return self._pedir([("listar_tabelas", {})])
        roteiro = ROTEIROS.get(pergunta, ["Não entendi o pedido."])
        etapa = roteiro[min(passo, len(roteiro) - 1)]
        if isinstance(etapa, list):
            return self._pedir(etapa)
        if isinstance(etapa, dict):
            houve_erro = any(_campo(r, "is_error") for r in resultados or [])
            etapa = etapa["pendente" if houve_erro else "enviado"]
        return SimpleNamespace(
            content=[SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=etapa)],
            stop_reason="end_turn",
        )

    def _pedir(self, chamadas):
        blocos = [SimpleNamespace(type="thinking", thinking="")]
        for nome, argumentos in chamadas:
            blocos.append(SimpleNamespace(type="tool_use", id=f"toolu_{self._proximo_id:03d}", name=nome, input=dict(argumentos)))
            self._proximo_id += 1
        return SimpleNamespace(content=blocos, stop_reason="tool_use")

import json
from pathlib import Path

import pytest

from modelo_gravado import ModeloGravado
from solucao import (
    NAO_ENCONTREI,
    avaliar,
    checar_resposta,
    criar_slug,
    dividir_em_trechos,
    extrair_citacoes,
    indexar,
    ler_documentos,
    montar_mensagens,
    recuperar,
    responder,
)

DOCUMENTOS = ler_documentos()
PERGUNTAS = json.loads((Path(__file__).parent.parent / "data" / "perguntas.json").read_text(encoding="utf-8"))
POR_ID = {item["id"]: item for item in PERGUNTAS}
LONGO = "# Título\n\n## Seção longa\n\n" + "\n\n".join(f"Parágrafo número {i} com algum texto." for i in range(6))


def todos_os_trechos():
    return [trecho for doc_id, texto in DOCUMENTOS.items() for trecho in dividir_em_trechos(doc_id, texto)]


def ids(trechos):
    return [trecho["id"] for trecho in trechos]


def test_criar_slug():
    assert criar_slug("Divisão em períodos") == "divisao-em-periodos"
    assert criar_slug("Senhas e acesso") == "senhas-e-acesso"
    assert criar_slug("  Venda de parte das férias! ") == "venda-de-parte-das-ferias"


def test_dividir_em_trechos_por_secao():
    trechos = dividir_em_trechos("reembolso_despesas", DOCUMENTOS["reembolso_despesas"])
    assert ids(trechos) == [
        "reembolso_despesas#quem-pode-pedir",
        "reembolso_despesas#limites-por-categoria",
        "reembolso_despesas#prazo-para-pedir",
        "reembolso_despesas#como-pedir",
    ]
    limites = trechos[1]
    assert limites["titulo"] == "Reembolso de despesas" and limites["secao"] == "Limites por categoria"
    assert limites["documento"] == "reembolso_despesas"
    assert limites["texto"].startswith("A alimentação em viagem tem limite de R$ 80 por dia. A hospedagem")
    assert "#" not in limites["texto"] and "\n" not in limites["texto"], "Um parágrafo vira uma linha só."


def test_secao_longa_vira_varios_trechos():
    trechos = dividir_em_trechos("x", LONGO, max_caracteres=80)
    assert ids(trechos) == ["x#secao-longa-1", "x#secao-longa-2", "x#secao-longa-3"]
    assert all(len(trecho["texto"]) <= 80 for trecho in trechos)
    assert trechos[0]["texto"] == "Parágrafo número 0 com algum texto.\n\nParágrafo número 1 com algum texto."
    assert ids(dividir_em_trechos("x", LONGO)) == ["x#secao-longa"], "Cabendo no limite, a seção é um trecho só."


def test_todos_os_documentos():
    trechos = todos_os_trechos()
    assert len(trechos) == 13 and len(set(ids(trechos))) == 13


def test_recuperar():
    indice = indexar(todos_os_trechos())
    assert ids(recuperar(indice, POR_ID["p1"]["pergunta"], k=1)) == ["reembolso_despesas#limites-por-categoria"]
    assert len(recuperar(indice, POR_ID["p1"]["pergunta"], k=2)) == 2
    assert recuperar(indice, "xyzw qwerty") == [], "Sem nenhuma palavra em comum, nenhum trecho."


def test_recuperacao_encontra_o_trecho_de_cada_pergunta():
    indice = indexar(todos_os_trechos())
    for item in PERGUNTAS:
        if item["trecho_relevante"]:
            assert item["trecho_relevante"] in ids(recuperar(indice, item["pergunta"], k=3)), item["id"]


def test_montar_mensagens():
    trechos = todos_os_trechos()[:2]
    system, messages = montar_mensagens("Como marco as férias?", trechos)
    assert NAO_ENCONTREI in system and "[" in system
    assert len(messages) == 1 and messages[0]["role"] == "user"
    conteudo = messages[0]["content"]
    posicoes = [conteudo.index(f'<documento id="{t["id"]}">') for t in trechos]
    assert posicoes == sorted(posicoes), "Os trechos entram na ordem recebida."
    assert "Férias > Como marcar" in conteudo
    assert conteudo.index("</documentos>") < conteudo.index("<pergunta>")
    assert conteudo.rstrip().endswith("Como marco as férias?\n</pergunta>")


def test_extrair_citacoes():
    texto = "Até três dias [home_office#dias-de-home-office]. Ver [ferias#como-marcar] e [home_office#dias-de-home-office]."
    assert extrair_citacoes(texto) == ["home_office#dias-de-home-office", "ferias#como-marcar"]
    assert extrair_citacoes("Resposta sem fonte.") == []


def test_checar_resposta():
    enviados = ["ferias#como-marcar", "ferias#divisao-em-periodos"]
    assert checar_resposta("Com 30 dias [ferias#como-marcar].", enviados) == {
        "citacoes": ["ferias#como-marcar"], "fora_do_contexto": [], "sem_citacao": False, "recusou": False,
    }
    assert checar_resposta("Pode [ferias#prazos].", enviados)["fora_do_contexto"] == ["ferias#prazos"]
    assert checar_resposta("Pode sim.", enviados)["sem_citacao"] is True
    recusa = checar_resposta(f"  {NAO_ENCONTREI} ", enviados)
    assert recusa["recusou"] is True and recusa["sem_citacao"] is False


def test_responder():
    indice, cliente = indexar(todos_os_trechos()), ModeloGravado()
    resultado = responder(cliente, indice, POR_ID["p1"]["pergunta"])
    assert resultado["resposta"] == POR_ID["p1"]["resposta_gravada"]
    assert len(resultado["trechos"]) == 3 and resultado["checagem"]["fora_do_contexto"] == []
    chamada = cliente.chamadas[0]
    assert {"model", "max_tokens", "system", "messages"} <= set(chamada) and "temperature" not in chamada
    vazio = ModeloGravado()
    sem_trechos = responder(vazio, indice, "xyzw qwerty")
    assert sem_trechos["resposta"] == NAO_ENCONTREI and vazio.chamadas == [], "Sem trechos, nem chame o modelo."


def test_avaliar():
    assert avaliar(ModeloGravado(), indexar(todos_os_trechos()), PERGUNTAS) == {
        "recuperacao": pytest.approx(1.0),
        "ok": ["p1", "p2", "p3", "p4"],
        "recusas": ["p5"],
        "sem_citacao": ["p7"],
        "fora_do_contexto": ["p6", "p8"],
    }

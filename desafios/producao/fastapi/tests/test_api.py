import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from llm_gravado import LLMGravado
from modelo import CARREGAMENTOS
from solucao import SISTEMA, app, faixa_de_risco, obter_cliente_llm

EXEMPLOS = json.loads((Path(__file__).parent.parent / "data" / "clientes_exemplo.json").read_text(encoding="utf-8"))
CHAVE = {"X-API-Key": "chave-de-teste"}


@pytest.fixture(autouse=True)
def chave_configurada(monkeypatch):
    monkeypatch.setenv("CHAVE_API", "chave-de-teste")


def abrir():
    """O cliente de teste. Usado com "with", ele roda o ciclo de vida da API, como o servidor."""
    return TestClient(app)


def com(cliente, **mudancas):
    return {**cliente, **mudancas}


def test_faixa_de_risco():
    assert [faixa_de_risco(p) for p in (0.0247, 0.29999, 0.3, 0.5999, 0.6, 0.9265)] == [
        "baixo", "baixo", "medio", "medio", "alto", "alto",
    ]


def test_saude():
    with abrir() as api:
        resposta = api.get("/saude")
    assert resposta.status_code == 200, "O teste de saúde não pede chave: a plataforma de nuvem chama sem chave."
    assert resposta.json() == {"status": "ok", "versao_modelo": "2026-11-01"}


def test_previsao():
    with abrir() as api:
        respostas = [api.post("/previsoes", json=cliente, headers=CHAVE) for cliente in EXEMPLOS]
    assert [r.status_code for r in respostas] == [200, 200, 200]
    assert [r.json() for r in respostas] == [
        {"probabilidade_cancelamento": 0.0247, "risco": "baixo", "versao_modelo": "2026-11-01"},
        {"probabilidade_cancelamento": 0.5665, "risco": "medio", "versao_modelo": "2026-11-01"},
        {"probabilidade_cancelamento": 0.9265, "risco": "alto", "versao_modelo": "2026-11-01"},
    ]


def test_entrada_invalida_vira_422():
    cliente = EXEMPLOS[1]
    sem_canal = {campo: valor for campo, valor in cliente.items() if campo != "canal"}
    casos = [
        (com(cliente, idade=10), "idade"),
        (com(cliente, plano="ouro"), "plano"),
        (com(cliente, nota_satisfacao=7), "nota_satisfacao"),
        (com(cliente, valor_mensal=0), "valor_mensal"),
        (sem_canal, "canal"),
    ]
    with abrir() as api:
        for corpo, campo in casos:
            resposta = api.post("/previsoes", json=corpo, headers=CHAVE)
            assert resposta.status_code == 422, f"O campo {campo} inválido deveria ser recusado."
            assert resposta.json()["detail"][0]["loc"] == ["body", campo]


def test_campo_extra_e_recusado():
    with abrir() as api:
        resposta = api.post("/previsoes", json=com(EXEMPLOS[0], cpf="123.456.789-00"), headers=CHAVE)
    assert resposta.status_code == 422, "Um campo que a API não conhece não pode passar calado."
    assert resposta.json()["detail"][0]["type"] == "extra_forbidden"


def test_chave_da_api(monkeypatch):
    with abrir() as api:
        assert api.post("/previsoes", json=EXEMPLOS[0]).status_code == 401
        assert api.post("/previsoes", json=EXEMPLOS[0], headers={"X-API-Key": "chute"}).status_code == 401
        assert api.post("/previsoes", json=EXEMPLOS[0], headers=CHAVE).status_code == 200
        monkeypatch.delenv("CHAVE_API")
        assert api.post("/previsoes", json=EXEMPLOS[0], headers={"X-API-Key": ""}).status_code == 401, (
            "Sem a variável CHAVE_API no servidor, nenhuma chave pode valer."
        )
        assert api.get("/saude").status_code == 200


def test_previsoes_em_lote():
    with abrir() as api:
        resposta = api.post("/previsoes/lote", json={"clientes": EXEMPLOS}, headers=CHAVE)
        assert resposta.status_code == 200
        assert [p["probabilidade_cancelamento"] for p in resposta.json()["previsoes"]] == [0.0247, 0.5665, 0.9265]
        assert api.post("/previsoes/lote", json={"clientes": []}, headers=CHAVE).status_code == 422
        grande = {"clientes": EXEMPLOS * 34}
        assert api.post("/previsoes/lote", json=grande, headers=CHAVE).status_code == 422, "No máximo 100 clientes por lote."


def test_modelo_carregado_uma_vez():
    antes = CARREGAMENTOS["total"]
    with abrir() as api:
        for cliente in EXEMPLOS * 2:
            assert api.post("/previsoes", json=cliente, headers=CHAVE).status_code == 200
        assert api.get("/saude").status_code == 200
    assert CARREGAMENTOS["total"] - antes == 1, "Carregue o modelo uma vez, no ciclo de vida, e não a cada requisição."


def test_documentacao_openapi():
    with abrir() as api:
        documento = api.get("/openapi.json").json()
    esquemas = documento["components"]["schemas"]
    campos = esquemas["Cliente"]["properties"]
    assert set(campos) == set(EXEMPLOS[0])
    assert all(campo.get("description") for campo in campos.values()), "Descreva cada campo: a descrição vai para o /docs."
    assert esquemas["Cliente"]["additionalProperties"] is False
    resposta = documento["paths"]["/previsoes"]["post"]["responses"]["200"]["content"]["application/json"]["schema"]
    assert resposta["$ref"].endswith("/Previsao")
    seguranca = list(documento["components"]["securitySchemes"].values())
    assert {"type": "apiKey", "in": "header", "name": "X-API-Key"}.items() <= seguranca[0].items()


def test_explicacao_com_llm():
    llm = LLMGravado(texto="O cliente abriu dois chamados e atrasou um pagamento.")
    app.dependency_overrides[obter_cliente_llm] = lambda: llm
    try:
        with abrir() as api:
            resposta = api.post("/previsoes/explicacao", json=EXEMPLOS[1], headers=CHAVE)
    finally:
        app.dependency_overrides.clear()
    assert resposta.status_code == 200
    assert resposta.json() == {
        "probabilidade_cancelamento": 0.5665,
        "risco": "medio",
        "versao_modelo": "2026-11-01",
        "explicacao": "O cliente abriu dois chamados e atrasou um pagamento.",
    }
    chamada = llm.chamadas[0]
    assert chamada["model"] == "claude-haiku-5-5" and chamada["max_tokens"] == 1024
    assert chamada["system"] == SISTEMA
    pedido = chamada["messages"][0]["content"]
    assert "Probabilidade de cancelamento: 57%" in pedido and "- chamados_suporte: 2" in pedido


@pytest.mark.parametrize("falha", ["limite", "conexao"])
def test_llm_fora_do_ar_vira_503(falha):
    app.dependency_overrides[obter_cliente_llm] = lambda: LLMGravado(falha=falha)
    try:
        with abrir() as api:
            resposta = api.post("/previsoes/explicacao", json=EXEMPLOS[2], headers=CHAVE)
            previsao = api.post("/previsoes", json=EXEMPLOS[2], headers=CHAVE)
    finally:
        app.dependency_overrides.clear()
    assert resposta.status_code == 503, "Falha num serviço de fora é 503, e não 500."
    detalhe = resposta.json()["detail"]
    assert "indisponível" in detalhe and "Limite" not in detalhe and "Connection" not in detalhe
    assert previsao.status_code == 200, "Sem o LLM, a previsão continua funcionando."

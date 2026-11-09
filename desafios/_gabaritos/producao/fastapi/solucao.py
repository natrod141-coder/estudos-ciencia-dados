"""Gabarito do desafio "Uma API para o modelo de cancelamento".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import logging
import os
import secrets
from contextlib import asynccontextmanager
from functools import lru_cache
from pathlib import Path
from typing import Literal

import anthropic
from fastapi import Depends, FastAPI, HTTPException, Request, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, ConfigDict, Field

from modelo import carregar_modelo

CAMINHO_MODELO = Path(__file__).parent / "data" / "modelo.json"
registro = logging.getLogger("api_cancelamento")
MODELO_LLM = "claude-haiku-5-5"
SISTEMA = (
    "Você explica para o time de relacionamento, em até três frases e em português simples, por "
    "que um cliente tem o risco de cancelamento indicado. Use só os dados fornecidos e não invente "
    "números."
)


def montar_pedido(cliente, probabilidade):
    """Já está pronta: o texto enviado ao modelo para explicar uma previsão."""
    dados = "\n".join(f"- {campo}: {valor}" for campo, valor in cliente.items())
    return f"Probabilidade de cancelamento: {probabilidade:.0%}\nDados do cliente:\n{dados}"


@lru_cache
def obter_cliente_llm():
    """Já está pronta: o cliente da API do Claude, criado uma vez só."""
    return anthropic.Anthropic()


def faixa_de_risco(probabilidade):
    if probabilidade < 0.3:
        return "baixo"
    if probabilidade < 0.6:
        return "medio"
    return "alto"


class Cliente(BaseModel):
    model_config = ConfigDict(extra="forbid")  # campo desconhecido é erro, e não é ignorado

    plano: Literal["basico", "padrao", "premium"] = Field(description="Plano contratado.")
    canal: Literal["anuncio", "indicacao", "organico", "parceiro"] = Field(description="Canal de aquisição.")
    idade: int = Field(ge=18, le=100, description="Idade, em anos.")
    meses_assinatura: int = Field(ge=0, description="Há quantos meses o cliente assina.")
    valor_mensal: float = Field(gt=0, description="Valor da mensalidade, em reais.")
    acessos_mes: int = Field(ge=0, description="Acessos no último mês.")
    chamados_suporte: int = Field(ge=0, description="Chamados abertos no suporte no último mês.")
    atrasos_pagamento: int = Field(ge=0, description="Pagamentos atrasados nos últimos seis meses.")
    usa_app: bool = Field(description="Se o cliente usa o aplicativo.")
    nota_satisfacao: int = Field(ge=1, le=5, description="Nota da última pesquisa de satisfação, de 1 a 5.")


class Previsao(BaseModel):
    probabilidade_cancelamento: float = Field(ge=0, le=1, description="Probabilidade de cancelar, de 0 a 1.")
    risco: Literal["baixo", "medio", "alto"] = Field(description="Faixa de risco.")
    versao_modelo: str = Field(description="Versão do modelo que fez a previsão.")


class PedidoLote(BaseModel):
    clientes: list[Cliente] = Field(min_length=1, max_length=100, description="De 1 a 100 clientes.")


class RespostaLote(BaseModel):
    previsoes: list[Previsao]


class Explicacao(Previsao):
    explicacao: str = Field(description="Explicação em texto, escrita por um modelo de linguagem.")


@asynccontextmanager
async def ciclo_de_vida(app):
    # roda uma vez, quando o servidor sobe: o modelo fica na memória para todas as requisições
    app.state.modelo = carregar_modelo(CAMINHO_MODELO)
    yield


app = FastAPI(title="API de cancelamento", version="1.0.0", lifespan=ciclo_de_vida)
chave_api = APIKeyHeader(name="X-API-Key", auto_error=False)


def exigir_chave(chave: str | None = Security(chave_api)):
    esperada = os.environ.get("CHAVE_API")
    # sem a variável configurada, nenhuma chave vale; compare_digest evita ataques de tempo
    if not esperada or not chave or not secrets.compare_digest(chave, esperada):
        raise HTTPException(status_code=401, detail="Chave da API ausente ou inválida.")


def prever_clientes(request, clientes):
    modelo = request.app.state.modelo
    probabilidades = modelo.prever([cliente.model_dump() for cliente in clientes])
    return [
        Previsao(probabilidade_cancelamento=round(p, 4), risco=faixa_de_risco(p), versao_modelo=modelo.versao)
        for p in probabilidades
    ]


@app.get("/saude")
def saude(request: Request):
    return {"status": "ok", "versao_modelo": request.app.state.modelo.versao}


@app.post("/previsoes", response_model=Previsao, dependencies=[Depends(exigir_chave)])
def prever(cliente: Cliente, request: Request):
    return prever_clientes(request, [cliente])[0]


@app.post("/previsoes/lote", response_model=RespostaLote, dependencies=[Depends(exigir_chave)])
def prever_lote(pedido: PedidoLote, request: Request):
    return RespostaLote(previsoes=prever_clientes(request, pedido.clientes))


@app.post("/previsoes/explicacao", response_model=Explicacao, dependencies=[Depends(exigir_chave)])
def explicar(cliente: Cliente, request: Request, llm=Depends(obter_cliente_llm)):
    previsao = prever_clientes(request, [cliente])[0]
    try:
        resposta = llm.messages.create(
            model=MODELO_LLM,
            max_tokens=1024,
            system=SISTEMA,
            messages=[{"role": "user", "content": montar_pedido(cliente.model_dump(), previsao.probabilidade_cancelamento)}],
        )
    except anthropic.APIError as erro:
        # o detalhe do erro fica no registro do servidor; quem chama recebe uma mensagem clara
        registro.warning("Falha ao chamar a API do Claude: %s", erro)
        raise HTTPException(status_code=503, detail="A explicação está indisponível no momento. Tente de novo em instantes.")
    texto = "".join(bloco.text for bloco in resposta.content if bloco.type == "text")
    return Explicacao(**previsao.model_dump(), explicacao=texto)

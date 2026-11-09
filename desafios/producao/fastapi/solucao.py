"""Desafio: uma API para o modelo de cancelamento.

O modelo de cancelamento do módulo de machine learning está pronto, em data/modelo.json. O time de
relacionamento quer usá-lo no sistema de atendimento: o sistema manda os dados de um cliente e
recebe a probabilidade de ele cancelar. Você vai escrever a API, com FastAPI: validação da entrada,
chave de acesso, previsões em lote, o modelo carregado uma vez só e uma rota que pede ao Claude uma
explicação da previsão.

O que já está pronto: o modelo (modelo.py), o texto enviado ao Claude (montar_pedido) e a
dependência que cria o cliente da API do Claude (obter_cliente_llm). Os testes trocam essa
dependência por um cliente gravado (llm_gravado.py): o desafio roda sem chave de API e sem custo.

Regras:
- Não altere modelo.py, llm_gravado.py, a pasta tests nem os arquivos em data.
- Mantenha os nomes e os caminhos das rotas.

Para ver a API funcionando, rode no terminal, dentro desta pasta, e abra http://127.0.0.1:8000/docs:
    fastapi dev solucao.py
Para conferir o seu trabalho:
    pytest -v
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
    """Já está pronta: o cliente da API do Claude, criado uma vez só. Ele lê a chave da variável de
    ambiente ANTHROPIC_API_KEY. Nos testes, app.dependency_overrides troca esta função."""
    return anthropic.Anthropic()


def faixa_de_risco(probabilidade):
    """Devolve "baixo" abaixo de 0.3, "medio" de 0.3 até abaixo de 0.6 e "alto" a partir de 0.6."""
    raise NotImplementedError("Implemente a função faixa_de_risco")


class Cliente(BaseModel):
    """Os dados de um cliente, no corpo da requisição. Escreva os dez campos, todos obrigatórios e
    cada um com Field(description=...), porque a descrição aparece na documentação:

    - plano: "basico", "padrao" ou "premium" (use Literal);
    - canal: "anuncio", "indicacao", "organico" ou "parceiro";
    - idade: inteiro, de 18 a 100;
    - meses_assinatura, acessos_mes, chamados_suporte e atrasos_pagamento: inteiros, a partir de 0;
    - valor_mensal: número maior que 0;
    - usa_app: verdadeiro ou falso;
    - nota_satisfacao: inteiro, de 1 a 5.

    Um campo que a API não conhece deve ser recusado: model_config = ConfigDict(extra="forbid").
    """


class Previsao(BaseModel):
    """A resposta de uma previsão: probabilidade_cancelamento (número de 0 a 1, arredondado com
    4 casas), risco ("baixo", "medio" ou "alto") e versao_modelo (texto). Descreva cada campo."""


class PedidoLote(BaseModel):
    """O corpo de /previsoes/lote: o campo clientes, uma lista de Cliente com 1 a 100 itens."""


class RespostaLote(BaseModel):
    """A resposta de /previsoes/lote: o campo previsoes, uma lista de Previsao, na mesma ordem."""


class Explicacao(Previsao):
    """A resposta de /previsoes/explicacao: os campos de Previsao e mais explicacao (texto)."""


@asynccontextmanager
async def ciclo_de_vida(app):
    """Roda uma vez, quando o servidor sobe. Carregue o modelo com carregar_modelo(CAMINHO_MODELO)
    e guarde em app.state.modelo, antes do yield."""
    raise NotImplementedError("Implemente o ciclo de vida da API")
    yield


app = FastAPI(title="API de cancelamento", version="1.0.0", lifespan=ciclo_de_vida)
chave_api = APIKeyHeader(name="X-API-Key", auto_error=False)


def exigir_chave(chave: str | None = Security(chave_api)):
    """Dependência das rotas de previsão. A chave certa está na variável de ambiente CHAVE_API: leia
    a cada requisição. Se a variável não existir, se a chave não vier ou se for diferente, levante
    HTTPException com status 401. Compare com secrets.compare_digest."""
    raise NotImplementedError("Implemente a função exigir_chave")


@app.get("/saude")
def saude(request: Request):
    """Sem chave. Devolve {"status": "ok", "versao_modelo": ...}, com a versão do modelo carregado
    (o atributo versao do modelo)."""
    raise NotImplementedError("Implemente a rota /saude")


@app.post("/previsoes", dependencies=[Depends(exigir_chave)])
def prever(cliente: Cliente, request: Request):
    """Devolve a Previsao de um cliente. O modelo recebe uma lista de dicionários:
    request.app.state.modelo.prever([cliente.model_dump()]). Declare response_model=Previsao."""
    raise NotImplementedError("Implemente a rota /previsoes")


@app.post("/previsoes/lote", dependencies=[Depends(exigir_chave)])
def prever_lote(pedido: PedidoLote, request: Request):
    """Recebe um PedidoLote e devolve uma RespostaLote, com uma chamada só ao modelo."""
    raise NotImplementedError("Implemente a rota /previsoes/lote")


@app.post("/previsoes/explicacao", dependencies=[Depends(exigir_chave)])
def explicar(cliente: Cliente, request: Request, llm=Depends(obter_cliente_llm)):
    """Devolve uma Explicacao: a previsão e um texto do Claude explicando o risco. Chame
    llm.messages.create(model=MODELO_LLM, max_tokens=1024, system=SISTEMA, messages=[...]), com uma
    mensagem do usuário cujo conteúdo é montar_pedido(cliente.model_dump(), probabilidade), usando
    a probabilidade já arredondada. A explicação é o texto dos blocos do tipo "text".

    Se a chamada levantar anthropic.APIError, registre o erro com registro.warning e levante
    HTTPException com status 503 e uma mensagem que diga que a explicação está indisponível, sem
    repassar a mensagem do erro original.
    """
    raise NotImplementedError("Implemente a rota /previsoes/explicacao")

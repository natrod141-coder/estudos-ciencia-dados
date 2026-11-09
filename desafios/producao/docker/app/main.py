"""A API de cancelamento, já pronta, para empacotar numa imagem Docker."""

import os
import secrets
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Request, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, ConfigDict, Field

from .modelo import carregar_modelo

CAMINHO_MODELO = Path(__file__).parent / "modelo.json"


class Cliente(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plano: Literal["basico", "padrao", "premium"]
    canal: Literal["anuncio", "indicacao", "organico", "parceiro"]
    idade: int = Field(ge=18, le=100)
    meses_assinatura: int = Field(ge=0)
    valor_mensal: float = Field(gt=0)
    acessos_mes: int = Field(ge=0)
    chamados_suporte: int = Field(ge=0)
    atrasos_pagamento: int = Field(ge=0)
    usa_app: bool
    nota_satisfacao: int = Field(ge=1, le=5)


@asynccontextmanager
async def ciclo_de_vida(app):
    app.state.modelo = carregar_modelo(CAMINHO_MODELO)
    yield


app = FastAPI(title="API de cancelamento", version="1.0.0", lifespan=ciclo_de_vida)
chave_api = APIKeyHeader(name="X-API-Key", auto_error=False)


def exigir_chave(chave: str | None = Security(chave_api)):
    esperada = os.environ.get("CHAVE_API")
    if not esperada or not chave or not secrets.compare_digest(chave, esperada):
        raise HTTPException(status_code=401, detail="Chave da API ausente ou inválida.")


@app.get("/saude")
def saude(request: Request):
    return {"status": "ok", "versao_modelo": request.app.state.modelo.versao}


@app.post("/previsoes", dependencies=[Depends(exigir_chave)])
def prever(cliente: Cliente, request: Request):
    modelo = request.app.state.modelo
    probabilidade = modelo.prever([cliente.model_dump()])[0]
    return {"probabilidade_cancelamento": round(probabilidade, 4), "versao_modelo": modelo.versao}

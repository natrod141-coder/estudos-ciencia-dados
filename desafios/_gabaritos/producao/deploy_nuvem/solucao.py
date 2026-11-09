"""Gabarito do desafio "Pronta para a nuvem".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import json
from datetime import timezone
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

NIVEIS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
PALAVRAS_SENSIVEIS = ("chave", "senha", "token", "secret", "key")


class Configuracao(BaseSettings):
    # o erro de validação não mostra o valor recebido, que pode ser um segredo
    model_config = SettingsConfigDict(hide_input_in_errors=True)

    chave_api: SecretStr = Field(min_length=16)
    anthropic_api_key: SecretStr
    port: int = Field(8080, ge=1, le=65535)
    nivel_log: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    revisao: str = Field("local", validation_alias="K_REVISION")
    max_lote: int = Field(100, ge=1, le=1000)


def linha_de_log(nivel, mensagem, momento, **campos):
    if nivel not in NIVEIS:
        raise ValueError(f"Nível desconhecido: {nivel}")
    if momento.tzinfo is None:
        raise ValueError("Use uma data com fuso horário: sem ele, não dá para saber a hora em UTC.")
    utc = momento.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    registro = {"severity": nivel, "message": mensagem, "time": utc}
    for nome, valor in campos.items():
        sensivel = any(palavra in nome.lower() for palavra in PALAVRAS_SENSIVEIS)
        registro[nome] = "***" if sensivel else valor
    return json.dumps(registro, ensure_ascii=False)


def custo_mensal(uso, precos):
    gratis = precos["gratuito_por_mes"]
    ativos = uso["requisicoes"] * uso["duracao_media_s"] / uso["concorrencia"]
    cpu = max(0, uso["vcpu"] * ativos - gratis["vcpu_segundos"]) * precos["cpu_ativa_por_vcpu_segundo"]
    memoria = max(0, uso["memoria_gib"] * ativos - gratis["gib_segundos"]) * precos["memoria_ativa_por_gib_segundo"]
    requisicoes = max(0, uso["requisicoes"] - gratis["requisicoes"]) / 1_000_000 * precos["por_milhao_de_requisicoes"]
    # instâncias mínimas ficam ligadas o mês inteiro; o tempo em que não atendem é cobrado como ocioso
    ociosos = max(0, uso["instancias_minimas"] * uso.get("dias", 30) * 86_400 - ativos)
    ociosidade = ociosos * (
        uso["vcpu"] * precos["cpu_ociosa_por_vcpu_segundo"] + uso["memoria_gib"] * precos["memoria_ociosa_por_gib_segundo"]
    )
    partes = {"cpu": cpu, "memoria": memoria, "requisicoes": requisicoes, "ociosidade": ociosidade}
    resultado = {nome: round(valor, 2) for nome, valor in partes.items()}
    resultado["total"] = round(sum(partes.values()), 2)
    return resultado


def acompanhar_orcamento(gastos_diarios, orcamento, dias_no_mes, limites=(0.5, 0.9, 1.0)):
    gasto = sum(gastos_diarios)
    projecao = gasto / len(gastos_diarios) * dias_no_mes
    return {
        "gasto": round(gasto, 2),
        "projecao": round(projecao, 2),
        "alertas": [limite for limite in limites if gasto >= limite * orcamento],
        "alertas_previstos": [limite for limite in limites if projecao >= limite * orcamento],
    }


def decidir_lancamento(atual, nova, minimo_de_requisicoes=500, tolerancia_erro=0.01, fator_latencia=1.2):
    if nova["requisicoes"] < minimo_de_requisicoes:
        return "aguardar", f"A nova revisão tem só {nova['requisicoes']} requisições; o mínimo é {minimo_de_requisicoes}."
    taxa_atual = atual["erros"] / atual["requisicoes"]
    taxa_nova = nova["erros"] / nova["requisicoes"]
    if taxa_nova > taxa_atual + tolerancia_erro:
        return "reverter", f"Taxa de erro de {taxa_nova:.1%}, contra {taxa_atual:.1%} da revisão atual."
    if nova["latencia_p95_ms"] > atual["latencia_p95_ms"] * fator_latencia:
        return "reverter", f"Latência p95 de {nova['latencia_p95_ms']} ms, contra {atual['latencia_p95_ms']} ms."
    return "promover", "Taxa de erro e latência dentro do esperado."

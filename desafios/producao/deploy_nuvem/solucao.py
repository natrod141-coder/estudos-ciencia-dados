"""Desafio: pronta para a nuvem.

A API de cancelamento já tem imagem Docker. Antes de publicá-la, faltam as peças que fazem um
serviço aguentar a vida na nuvem: a configuração lida do ambiente e conferida na subida, registros
que a plataforma entende, a conta do custo antes da fatura, o acompanhamento do orçamento e a
decisão de promover ou reverter uma versão nova.

Os preços do Cloud Run estão em data/precos_cloud_run.json, conferidos na página oficial em
novembro de 2026. As contas são uma estimativa simplificada: para decidir de verdade, use a
calculadora oficial do Google Cloud.

Regras:
- Use json, datetime e as bibliotecas pydantic e pydantic-settings, que vêm com o FastAPI.
- Nenhuma função pode alterar o que recebe.
- Não altere a pasta tests nem os arquivos em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import json
from datetime import timezone
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

NIVEIS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
PALAVRAS_SENSIVEIS = ("chave", "senha", "token", "secret", "key")


class Configuracao(BaseSettings):
    """A configuração da API, lida das variáveis de ambiente quando a classe é criada:
    Configuracao(). Escreva os campos (o nome do campo é o nome da variável, sem diferença entre
    maiúsculas e minúsculas):

    - chave_api: SecretStr, obrigatória, com pelo menos 16 caracteres (Field(min_length=16));
    - anthropic_api_key: SecretStr, obrigatória;
    - port: int, de 1 a 65535, padrão 8080 (o Cloud Run informa a porta em PORT);
    - nivel_log: "DEBUG", "INFO", "WARNING" ou "ERROR", padrão "INFO";
    - revisao: texto, padrão "local", lido da variável K_REVISION, que o Cloud Run preenche
      (Field("local", validation_alias="K_REVISION"));
    - max_lote: int, de 1 a 1000, padrão 100.

    Uma configuração inválida deve levantar ValidationError, e a mensagem do erro não pode mostrar
    o valor recebido, que pode ser um segredo: model_config = SettingsConfigDict(hide_input_in_errors=True).
    """


def linha_de_log(nivel, mensagem, momento, **campos):
    """Devolve um registro em JSON, numa linha só, no formato que o Cloud Logging entende:
    {"severity": nivel, "message": mensagem, "time": ..., e os campos extras}.

    - nivel precisa estar em NIVEIS; senão, ValueError.
    - momento é um datetime com fuso horário; sem fuso, ValueError. O time vai em UTC, com
      milissegundos e Z no fim: "2026-11-09T14:30:00.250Z".
    - Um campo extra cujo nome contém uma das PALAVRAS_SENSIVEIS, em qualquer caixa, vai com o
      valor "***".
    - Use json.dumps com ensure_ascii=False.
    """
    raise NotImplementedError("Implemente a função linha_de_log")


def custo_mensal(uso, precos):
    """Estima o custo mensal, em dólares, de um serviço no Cloud Run com cobrança por requisição.

    `uso` tem: requisicoes (no mês), duracao_media_s, concorrencia (quantas requisições, em média,
    uma instância atende ao mesmo tempo), vcpu, memoria_gib, instancias_minimas e, opcional, dias
    (padrão 30). `precos` é o conteúdo de data/precos_cloud_run.json.

    - Tempo ativo, em segundos de instância: requisicoes * duracao_media_s / concorrencia.
    - cpu: (vcpu * tempo ativo - cota gratuita de vCPU-segundos), nunca abaixo de zero, vezes o
      preço da CPU ativa. memoria: o mesmo, com memoria_gib e a cota de GiB-segundos.
    - requisicoes: as que passam da cota gratuita, por milhão, vezes o preço.
    - ociosidade: instâncias mínimas ficam ligadas o mês inteiro. O tempo em que não atendem,
      instancias_minimas * dias * 86400 - tempo ativo (nunca abaixo de zero), é cobrado pelos
      preços de CPU e memória ociosas.

    Devolva {"cpu", "memoria", "requisicoes", "ociosidade", "total"}, cada valor arredondado com
    2 casas; o total é a soma dos valores sem arredondar, arredondada no fim.
    """
    raise NotImplementedError("Implemente a função custo_mensal")


def acompanhar_orcamento(gastos_diarios, orcamento, dias_no_mes, limites=(0.5, 0.9, 1.0)):
    """Como os alertas de orçamento da nuvem: recebe o gasto de cada dia já passado no mês.

    Devolva {"gasto": a soma, "projecao": a média diária vezes dias_no_mes, "alertas": os limites
    que o gasto já atingiu, "alertas_previstos": os limites que a projeção atinge}. Um limite é
    atingido quando o valor é maior ou igual a limite * orcamento. Arredonde gasto e projeção com
    2 casas.
    """
    raise NotImplementedError("Implemente a função acompanhar_orcamento")


def decidir_lancamento(atual, nova, minimo_de_requisicoes=500, tolerancia_erro=0.01, fator_latencia=1.2):
    """Num lançamento gradual, uma parte do tráfego vai para a revisão nova. Compare as métricas
    das duas revisões, cada uma {"requisicoes", "erros", "latencia_p95_ms"}, e devolva uma tupla
    (decisao, motivo), conferindo nesta ordem:

    1. A nova tem menos que minimo_de_requisicoes: "aguardar", ainda não dá para saber.
    2. A taxa de erro da nova (erros / requisicoes) passa da taxa da atual mais tolerancia_erro:
       "reverter", com um motivo que fale da taxa de erro.
    3. A latência p95 da nova passa da latência da atual vezes fator_latencia: "reverter", com
       um motivo que fale da latência.
    4. Senão: "promover".
    """
    raise NotImplementedError("Implemente a função decidir_lancamento")

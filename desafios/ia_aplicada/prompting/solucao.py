"""Desafio: extrair dados de notas fiscais com saída estruturada.

O financeiro recebe notas de serviço por e-mail, cada uma num formato. Você vai definir o formato
da saída com pydantic, montar o prompt com exemplos e com o documento bem delimitado, e conferir as
respostas que um modelo devolveu em texto livre, antes de existir a saída estruturada.

As respostas estão gravadas em data/respostas_gravadas.json, para o desafio rodar sem chave de
API e sem custo.

Regras:
- Use json, re e pydantic. Nenhuma função pode alterar o que recebe.
- Não altere a pasta tests nem os arquivos em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import json
import re
from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

CATEGORIAS = ("software", "consultoria", "infraestrutura", "outros")

# Troque None por uma classe Nota, filha de BaseModel, com estes campos, nesta ordem:
#   fornecedor    texto
#   cnpj          texto ou None (pessoa física e recibos simples não têm CNPJ), mas sempre presente
#   data_emissao  date
#   valor_total   número maior que zero
#   categoria     um dos valores de CATEGORIAS (use Literal)
# Campos que não estão na lista são proibidos: model_config = ConfigDict(extra="forbid").
Nota = None


def escapar_documento(texto):
    """Neutraliza as marcações de documento que aparecerem dentro do texto.

    Troque "</documento>" por "[/documento]" e "<documento>" por "[documento]", sem diferenciar
    maiúsculas de minúsculas. Assim, um texto malicioso não consegue fechar a marcação antes da
    hora e se passar por instrução.
    """
    raise NotImplementedError("Implemente a função escapar_documento")


def montar_mensagens(documento, exemplos):
    """Monta (system, messages) para pedir a extração ao modelo.

    system: as instruções. Cite cada campo da Nota e as quatro categorias, peça a data no
    formato AAAA-MM-DD, o valor como número, e diga para usar null quando a informação não
    estiver no documento, em vez de inventar.

    messages: uma mensagem só, do usuário, neste formato:
        <exemplos>
        <exemplo>
        <documento>(documento do exemplo)</documento>
        <saida>(json.dumps(saida do exemplo, ensure_ascii=False))</saida>
        </exemplo>
        ... um bloco <exemplo> para cada exemplo ...
        </exemplos>

        <documento>
        (o documento, passado por escapar_documento)
        </documento>
    O documento a extrair vem por último, depois dos exemplos.
    """
    raise NotImplementedError("Implemente a função montar_mensagens")


def extrair_json(texto):
    """Encontra o objeto JSON no texto da resposta e devolve o dicionário.

    O modelo pode ter escrito uma frase antes, ou cercado o JSON com ```json e ```. Pegue do
    primeiro "{" ao último "}". Levanta ValueError se não houver JSON válido.
    """
    raise NotImplementedError("Implemente a função extrair_json")


def validar(dados):
    """Valida o dicionário com a Nota. Devolve (nota, erros).

    Se for válido: (a Nota, []). Se não: (None, lista dos nomes dos campos com erro, sem
    repetição e em ordem alfabética). O nome do campo está em erro["loc"], para cada erro de
    ValidationError.errors().
    """
    raise NotImplementedError("Implemente a função validar")


def pedir_correcao(mensagens, resposta_texto, erros):
    """Devolve uma lista nova de mensagens, para pedir ao modelo que corrija a resposta.

    A lista nova tem as mensagens recebidas, mais a resposta do modelo (papel "assistant", com
    resposta_texto) e um pedido de correção (papel "user") que cita cada campo com erro.
    """
    raise NotImplementedError("Implemente a função pedir_correcao")


def processar(respostas, documentos):
    """Confere todas as respostas gravadas e devolve um relatório.

    respostas e documentos são dicionários id -> texto. Para cada id, em ordem:
    - Se não der para extrair o JSON, vai para "invalidas" com a lista ["json"].
    - Se a validação falhar, vai para "invalidas" com a lista de campos com erro.
    - Se for válida, mas tiver um cnpj que não aparece no texto do documento, o modelo inventou
      o CNPJ: vai para "suspeitas".
    - Se não, vai para "validas".
    Devolve {"validas": [ids], "invalidas": {id: campos}, "suspeitas": [ids]}.
    """
    raise NotImplementedError("Implemente a função processar")

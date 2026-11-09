"""Desafio: medir o assistente antes de trocar o prompt.

O assistente de políticas internas tem duas versões do prompt. A v2 parece melhor. Você vai
avaliar as duas num conjunto de 20 perguntas, com regras que o código consegue conferir, separar
o resultado por tipo de pergunta, comparar item a item, medir a incerteza com bootstrap e ler as
notas de um modelo juiz, conferindo se ele concorda com as notas dadas por pessoas.

As respostas das duas versões e as notas do juiz estão gravadas em data: o desafio roda sem chave
de API e sem custo.

Regras:
- Use json, re, unicodedata e numpy. Nenhuma função pode alterar o que recebe.
- Não altere a pasta tests nem os arquivos em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import json
import re
import unicodedata
from pathlib import Path

import numpy as np

DADOS = Path(__file__).parent / "data"


def carregar():
    """Já está pronta: devolve (conjunto, respostas_v1, respostas_v2, juiz, notas_humanas)."""
    nomes = ["conjunto", "respostas_v1", "respostas_v2", "juiz", "notas_humanas"]
    return tuple(json.loads((DADOS / f"{nome}.json").read_text(encoding="utf-8")) for nome in nomes)


def normalizar_texto(texto):
    """Sem acentos, em minúsculas e com os espaços repetidos trocados por um só."""
    raise NotImplementedError("Implemente a função normalizar_texto")


def cobertura_de_fatos(resposta, fatos):
    """A proporção dos fatos que aparecem na resposta, comparando os textos normalizados.
    Sem fatos na lista, devolve 1.0."""
    raise NotImplementedError("Implemente a função cobertura_de_fatos")


def recusou(resposta):
    """True se a resposta, normalizada, contém "nao encontrei"."""
    raise NotImplementedError("Implemente a função recusou")


def avaliar_item(item, resposta):
    """True se a resposta está certa para o item do conjunto.

    - Item do tipo "fora_do_escopo": a resposta certa é a recusa, porque a informação não está
      nos documentos.
    - Item do tipo "factual": a resposta não pode ser uma recusa e precisa conter todos os fatos.
    """
    raise NotImplementedError("Implemente a função avaliar_item")


def avaliar_versao(conjunto, respostas):
    """Avalia todas as respostas de uma versão. Devolve um dicionário com:
    - "acerto": a proporção de itens certos;
    - "por_item": {id: True ou False};
    - "por_tipo": {"factual": proporção de acerto, "fora_do_escopo": proporção de acerto}.
    """
    raise NotImplementedError("Implemente a função avaliar_versao")


def comparar(por_item_a, por_item_b):
    """Compara duas versões item a item. Devolve {"melhorou": ids, "piorou": ids, "iguais": n}:
    melhorou são os itens errados em a e certos em b; piorou, o contrário; as listas em ordem
    alfabética."""
    raise NotImplementedError("Implemente a função comparar")


def intervalo_bootstrap(diferencas, n_reamostras=2000, semente=0):
    """O intervalo de 95% da média das diferenças, por bootstrap. Devolve (inferior, superior).

    Com gerador = np.random.default_rng(semente), sorteie, com reposição, n_reamostras
    conjuntos do mesmo tamanho das diferencas (gerador.integers(0, n, size=(n_reamostras, n))
    dá os índices), calcule a média de cada um e devolva os percentis 2,5 e 97,5 dessas médias,
    como floats.
    """
    raise NotImplementedError("Implemente a função intervalo_bootstrap")


def ler_nota_do_juiz(texto):
    """Lê a nota que o modelo juiz deu, de 1 a 5, no JSON da resposta dele: {"nota": n, ...}.

    O JSON pode vir com uma frase antes ou entre cercas ```json. Devolve um int. Levanta
    ValueError se não houver JSON ou se a nota não for um inteiro de 1 a 5.
    """
    raise NotImplementedError("Implemente a função ler_nota_do_juiz")


def media_do_juiz(juiz, versao):
    """A média das notas do juiz para uma versão ("v1" ou "v2"), em todos os itens."""
    raise NotImplementedError("Implemente a função media_do_juiz")


def concordancia(pares):
    """Recebe pares (nota do juiz, nota de uma pessoa) e devolve {"exata": ..., "ate_um_ponto": ...}:
    a proporção de pares com notas iguais e com diferença de no máximo um ponto."""
    raise NotImplementedError("Implemente a função concordancia")

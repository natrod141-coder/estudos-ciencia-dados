"""Desafio: busca por significado na central de ajuda.

A central de ajuda de uma loja online tem 16 artigos. Os clientes escrevem do jeito deles:
"quero meu dinheiro de volta", e não "reembolso". Você vai comparar a busca por palavras com a
busca por significado, com vetores, juntar as duas numa busca híbrida, medir os acertos e montar
um pequeno banco vetorial com filtro por categoria.

Os vetores em data/ são de brinquedo: têm só 8 dimensões, uma para cada assunto da central
(veja "dimensoes" em data/artigos.json), para dar para entender o que cada número quer dizer.
Os vetores de um modelo de embeddings de verdade têm mais de mil dimensões, que ninguém consegue
interpretar uma a uma, mas as contas são exatamente as mesmas.

Regras:
- Use numpy e scikit-learn. Nenhuma função pode alterar o que recebe.
- Não altere a pasta tests nem os arquivos em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import json
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

DADOS = Path(__file__).parent / "data"
PALAVRAS_VAZIAS = [
    "ao", "as", "com", "como", "da", "das", "de", "do", "dos", "em", "faço", "meu", "minha", "na", "nas",
    "no", "nos", "não", "os", "ou", "para", "por", "quando", "que", "se", "sua", "seu", "um", "uma", "você",
]


def carregar():
    """Já está pronta: devolve (artigos, consultas), lidos de data/artigos.json e data/consultas.json."""
    artigos = json.loads((DADOS / "artigos.json").read_text(encoding="utf-8"))["artigos"]
    consultas = json.loads((DADOS / "consultas.json").read_text(encoding="utf-8"))
    return artigos, consultas


def normalizar(vetor):
    """Devolve o vetor dividido pelo seu comprimento (norma), como array do numpy.

    O resultado tem comprimento 1 e a mesma direção. Levanta ValueError para um vetor de zeros.
    """
    raise NotImplementedError("Implemente a função normalizar")


def similaridade_cosseno(a, b):
    """O cosseno do ângulo entre os dois vetores, como float: o produto escalar dos dois
    normalizados. 1 é a mesma direção, 0 é sem relação, -1 é a direção oposta."""
    raise NotImplementedError("Implemente a função similaridade_cosseno")


def buscar(consulta, matriz, k=3):
    """Devolve os índices das k linhas da matriz mais parecidas com a consulta, pela similaridade
    de cosseno, da mais parecida para a menos. No empate, o índice menor vem antes."""
    raise NotImplementedError("Implemente a função buscar")


def buscar_por_palavras(consulta, textos, k=3):
    """A busca por palavras: devolve os índices dos até k textos mais parecidos com a consulta.

    Use TfidfVectorizer(stop_words=PALAVRAS_VAZIAS), treinado com os textos, e o cosseno entre a
    consulta e cada texto (as linhas do TF-IDF já saem com comprimento 1). Textos sem nenhuma
    palavra em comum com a consulta, com nota zero, não entram no resultado, que pode até sair
    vazio. No empate, o índice menor vem antes.
    """
    raise NotImplementedError("Implemente a função buscar_por_palavras")


def acertos_em_k(rankings, relevantes, k):
    """A proporção de consultas cujo artigo relevante está entre os k primeiros do ranking.

    rankings é uma lista de listas de índices, uma por consulta; relevantes é a lista com o
    índice do artigo certo de cada consulta.
    """
    raise NotImplementedError("Implemente a função acertos_em_k")


def fusao_rrf(rankings, k_rrf=60):
    """Junta vários rankings com a fusão por posição recíproca (reciprocal rank fusion).

    Cada índice ganha, de cada ranking em que aparece, 1 / (k_rrf + posição), com a posição
    contando a partir de 1. Devolve todos os índices que aparecem em algum ranking, da maior soma
    para a menor; no empate, o índice menor vem antes.
    """
    raise NotImplementedError("Implemente a função fusao_rrf")


class IndiceVetorial:
    """Um banco vetorial em miniatura: guarda vetores com um id e metadados, e busca os mais
    parecidos com um vetor, podendo filtrar pelos metadados."""

    def __init__(self):
        raise NotImplementedError("Implemente a classe IndiceVetorial")

    def adicionar(self, id_, vetor, metadados=None):
        """Guarda o vetor, já normalizado, com o id e um dicionário de metadados."""
        raise NotImplementedError

    def __len__(self):
        """Quantos vetores estão guardados."""
        raise NotImplementedError

    def buscar(self, vetor, k=3, filtro=None):
        """Devolve uma lista de até k pares (id, similaridade), da maior similaridade para a menor.

        filtro é um dicionário, como {"categoria": "pagamento"}: só entram os itens cujos
        metadados têm todos esses valores.
        """
        raise NotImplementedError

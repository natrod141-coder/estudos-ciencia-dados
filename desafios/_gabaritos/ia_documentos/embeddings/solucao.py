"""Gabarito do desafio "Busca por significado na central de ajuda".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
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
    vetor = np.asarray(vetor, dtype=float)
    norma = np.linalg.norm(vetor)
    if norma == 0:
        raise ValueError("Um vetor de zeros não tem direção.")
    return vetor / norma


def similaridade_cosseno(a, b):
    return float(normalizar(a) @ normalizar(b))


def buscar(consulta, matriz, k=3):
    matriz = np.asarray(matriz, dtype=float)
    unitarios = matriz / np.linalg.norm(matriz, axis=1, keepdims=True)
    notas = unitarios @ normalizar(consulta)
    # ordem estável: no empate, fica o índice menor
    return [int(i) for i in np.argsort(-notas, kind="stable")[:k]]


def buscar_por_palavras(consulta, textos, k=3):
    vetorizador = TfidfVectorizer(stop_words=PALAVRAS_VAZIAS)
    matriz = vetorizador.fit_transform(textos)
    # as linhas do TF-IDF já saem com norma 1: o produto escalar é o cosseno
    notas = (matriz @ vetorizador.transform([consulta]).T).toarray().ravel()
    ordem = np.argsort(-notas, kind="stable")[:k]
    # sem nenhuma palavra em comum, o artigo não é resultado: nota zero não entra
    return [int(i) for i in ordem if notas[i] > 0]


def acertos_em_k(rankings, relevantes, k):
    acertos = [relevante in ranking[:k] for ranking, relevante in zip(rankings, relevantes)]
    return sum(acertos) / len(acertos)


def fusao_rrf(rankings, k_rrf=60):
    notas = {}
    for ranking in rankings:
        for posicao, indice in enumerate(ranking, start=1):
            notas[indice] = notas.get(indice, 0.0) + 1 / (k_rrf + posicao)
    return sorted(notas, key=lambda indice: (-notas[indice], indice))


class IndiceVetorial:
    def __init__(self):
        self._ids, self._vetores, self._metadados = [], [], []

    def adicionar(self, id_, vetor, metadados=None):
        self._ids.append(id_)
        self._vetores.append(normalizar(vetor))
        self._metadados.append(dict(metadados or {}))

    def __len__(self):
        return len(self._ids)

    def buscar(self, vetor, k=3, filtro=None):
        consulta = normalizar(vetor)
        candidatos = [
            (id_, float(v @ consulta))
            for id_, v, meta in zip(self._ids, self._vetores, self._metadados)
            if not filtro or all(meta.get(chave) == valor for chave, valor in filtro.items())
        ]
        return sorted(candidatos, key=lambda par: -par[1])[:k]

"""Gabarito do desafio "Medir o assistente antes de trocar o prompt".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
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
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return " ".join(sem_acento.lower().split())


def cobertura_de_fatos(resposta, fatos):
    if not fatos:
        return 1.0
    texto = normalizar_texto(resposta)
    return sum(normalizar_texto(fato) in texto for fato in fatos) / len(fatos)


def recusou(resposta):
    return "nao encontrei" in normalizar_texto(resposta)


def avaliar_item(item, resposta):
    if item["tipo"] == "fora_do_escopo":
        return recusou(resposta)
    return not recusou(resposta) and cobertura_de_fatos(resposta, item["fatos"]) == 1.0


def avaliar_versao(conjunto, respostas):
    por_item = {item["id"]: avaliar_item(item, respostas[item["id"]]) for item in conjunto}
    por_tipo = {}
    for tipo in ("factual", "fora_do_escopo"):
        do_tipo = [por_item[item["id"]] for item in conjunto if item["tipo"] == tipo]
        por_tipo[tipo] = sum(do_tipo) / len(do_tipo)
    return {"acerto": sum(por_item.values()) / len(por_item), "por_item": por_item, "por_tipo": por_tipo}


def comparar(por_item_a, por_item_b):
    melhorou = sorted(id_ for id_ in por_item_a if not por_item_a[id_] and por_item_b[id_])
    piorou = sorted(id_ for id_ in por_item_a if por_item_a[id_] and not por_item_b[id_])
    return {"melhorou": melhorou, "piorou": piorou, "iguais": len(por_item_a) - len(melhorou) - len(piorou)}


def intervalo_bootstrap(diferencas, n_reamostras=2000, semente=0):
    diferencas = np.asarray(diferencas, dtype=float)
    gerador = np.random.default_rng(semente)
    # cada linha é um conjunto de avaliação sorteado com reposição, do mesmo tamanho do original
    sorteios = gerador.integers(0, len(diferencas), size=(n_reamostras, len(diferencas)))
    medias = diferencas[sorteios].mean(axis=1)
    inferior, superior = np.percentile(medias, [2.5, 97.5])
    return float(inferior), float(superior)


def ler_nota_do_juiz(texto):
    encontrado = re.search(r"\{.*\}", texto, re.DOTALL)
    if not encontrado:
        raise ValueError("A resposta do juiz não tem JSON.")
    nota = json.loads(encontrado.group())["nota"]
    if not isinstance(nota, int) or not 1 <= nota <= 5:
        raise ValueError(f"Nota fora da escala de 1 a 5: {nota}")
    return nota


def media_do_juiz(juiz, versao):
    notas = [ler_nota_do_juiz(textos[versao]) for textos in juiz.values()]
    return sum(notas) / len(notas)


def concordancia(pares):
    exata = sum(juiz == humano for juiz, humano in pares) / len(pares)
    ate_um_ponto = sum(abs(juiz - humano) <= 1 for juiz, humano in pares) / len(pares)
    return {"exata": exata, "ate_um_ponto": ate_um_ponto}

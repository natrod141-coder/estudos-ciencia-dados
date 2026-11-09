import numpy as np
import pytest

from solucao import (
    IndiceVetorial,
    acertos_em_k,
    buscar,
    buscar_por_palavras,
    carregar,
    fusao_rrf,
    normalizar,
    similaridade_cosseno,
)

ARTIGOS, CONSULTAS = carregar()
IDS = [artigo["id"] for artigo in ARTIGOS]
TEXTOS = [artigo["titulo"] + ". " + artigo["texto"] for artigo in ARTIGOS]
MATRIZ = [artigo["vetor"] for artigo in ARTIGOS]
RELEVANTES = [IDS.index(consulta["relevante"]) for consulta in CONSULTAS]
POR_ID = {consulta["id"]: consulta for consulta in CONSULTAS}


def ids(indices):
    return [IDS[i] for i in indices]


def test_normalizar():
    assert normalizar([3, 4]).tolist() == pytest.approx([0.6, 0.8])
    assert np.linalg.norm(normalizar(MATRIZ[0])) == pytest.approx(1.0)
    with pytest.raises(ValueError):
        normalizar([0, 0, 0])


def test_similaridade_cosseno():
    assert similaridade_cosseno([1, 0], [0, 5]) == pytest.approx(0.0)
    assert similaridade_cosseno([1, 2], [2, 4]) == pytest.approx(1.0), "O tamanho do vetor não importa, só a direção."
    assert similaridade_cosseno([1, 2], [-1, -2]) == pytest.approx(-1.0)
    assert isinstance(similaridade_cosseno([1, 2], [3, 1]), float)


def test_buscar():
    matriz = [[1, 0], [0, 1], [1, 1], [2, 0]]
    assert buscar([1, 0.1], matriz, k=3) == [0, 3, 2], "Mesma direção empata: o índice menor vem antes."
    assert len(buscar(MATRIZ[0], MATRIZ, k=5)) == 5


def test_busca_por_significado_entende_sinonimos():
    for consulta, esperado in [("q01", "a09"), ("q10", "a12")]:
        assert ids(buscar(POR_ID[consulta]["vetor"], MATRIZ, k=1)) == [esperado]
        assert buscar_por_palavras(POR_ID[consulta]["texto"], TEXTOS) == [], (
            f'"{POR_ID[consulta]["texto"]}" não tem nenhuma palavra em comum com os artigos.'
        )


def test_busca_por_palavras_acha_codigos_exatos():
    consulta = POR_ID["q05"]
    assert ids(buscar_por_palavras(consulta["texto"], TEXTOS, k=1)) == ["a11"]
    assert ids(buscar(consulta["vetor"], MATRIZ, k=1)) != ["a11"], (
        "O vetor capta o assunto (aplicativo), mas não o código exato E-403."
    )


def test_busca_por_palavras_devolve_no_maximo_k():
    resultado = buscar_por_palavras("nota fiscal do pedido", TEXTOS, k=2)
    assert len(resultado) == 2
    assert set(ids(resultado)) <= {"a13", "a14", "a04"}


def test_acertos_em_k():
    rankings = [[3, 1, 2], [0, 2], [], [5, 4, 1]]
    assert acertos_em_k(rankings, [3, 2, 7, 1], 1) == pytest.approx(0.25)
    assert acertos_em_k(rankings, [3, 2, 7, 1], 3) == pytest.approx(0.75)


def test_fusao_rrf():
    assert fusao_rrf([[2, 0, 1], [0, 3]]) == [0, 2, 3, 1]
    assert fusao_rrf([[1], [2]]) == [1, 2], "No empate, o índice menor vem antes."


def test_busca_hibrida_acerta_mais():
    semantica = [buscar(c["vetor"], MATRIZ, k=16) for c in CONSULTAS]
    palavras = [buscar_por_palavras(c["texto"], TEXTOS, k=16) for c in CONSULTAS]
    hibrida = [fusao_rrf([s, p]) for s, p in zip(semantica, palavras)]
    notas = {nome: acertos_em_k(r, RELEVANTES, 1) for nome, r in [("semantica", semantica), ("palavras", palavras), ("hibrida", hibrida)]}
    assert notas["hibrida"] > notas["semantica"] > notas["palavras"], f"Acertos na 1ª posição: {notas}"
    assert notas["hibrida"] == pytest.approx(1.0)


def montar_indice():
    indice = IndiceVetorial()
    for artigo in ARTIGOS:
        indice.adicionar(artigo["id"], artigo["vetor"], {"categoria": artigo["categoria"]})
    return indice


def test_indice_vetorial():
    indice = montar_indice()
    assert len(indice) == 16
    resultado = indice.buscar(POR_ID["q01"]["vetor"], k=2)
    assert [id_ for id_, _ in resultado] == ["a09", "a10"]
    assert resultado[0][1] > resultado[1][1] and isinstance(resultado[0][1], float)
    assert resultado[0][1] == pytest.approx(similaridade_cosseno(POR_ID["q01"]["vetor"], ARTIGOS[8]["vetor"]))


def test_indice_vetorial_com_filtro():
    indice = montar_indice()
    resultado = indice.buscar(POR_ID["q09"]["vetor"], k=3, filtro={"categoria": "pagamento"})
    assert [id_ for id_, _ in resultado] and all(id_ in ("a01", "a02") for id_, _ in resultado), (
        "Com o filtro, só entram artigos da categoria pagamento."
    )
    assert indice.buscar(POR_ID["q09"]["vetor"], filtro={"categoria": "inexistente"}) == []

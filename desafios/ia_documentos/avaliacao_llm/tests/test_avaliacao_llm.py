import numpy as np
import pytest

from solucao import (
    avaliar_item,
    avaliar_versao,
    carregar,
    cobertura_de_fatos,
    comparar,
    concordancia,
    intervalo_bootstrap,
    ler_nota_do_juiz,
    media_do_juiz,
    normalizar_texto,
    recusou,
)

CONJUNTO, V1, V2, JUIZ, HUMANOS = carregar()
POR_ID = {item["id"]: item for item in CONJUNTO}


def test_normalizar_texto():
    assert normalizar_texto("  Três   DIAS por Semana ") == "tres dias por semana"


def test_cobertura_de_fatos():
    assert cobertura_de_fatos("Notebook e monitor.", ["notebook", "monitor", "cadeira"]) == pytest.approx(2 / 3)
    assert cobertura_de_fatos("Até TRES dias", ["três dias"]) == 1.0, "Acentos e maiúsculas não importam."
    assert cobertura_de_fatos("Qualquer coisa", []) == 1.0


def test_recusou():
    assert recusou("Não encontrei essa informação nos documentos.") is True
    assert recusou("NAO ENCONTREI nada.") is True
    assert recusou("O limite é de R$ 80.") is False


def test_avaliar_item():
    assert avaliar_item(POR_ID["e07"], "Notebook, monitor e cadeira.") is True
    assert avaliar_item(POR_ID["e07"], "Notebook e monitor.") is False, "Faltou um dos fatos."
    assert avaliar_item(POR_ID["e01"], "Não encontrei essa informação nos documentos.") is False
    assert avaliar_item(POR_ID["e17"], "Não encontrei essa informação nos documentos.") is True
    assert avaliar_item(POR_ID["e17"], "O vale-refeição é de R$ 45.") is False, "Fora do escopo, responder é inventar."


def test_avaliar_v1():
    resultado = avaliar_versao(CONJUNTO, V1)
    assert resultado["acerto"] == pytest.approx(0.80)
    assert resultado["por_tipo"] == {"factual": pytest.approx(11 / 15), "fora_do_escopo": pytest.approx(1.0)}
    assert len(resultado["por_item"]) == 20


def test_avaliar_v2_esconde_uma_piora():
    resultado = avaliar_versao(CONJUNTO, V2)
    assert resultado["acerto"] == pytest.approx(0.85), "Na média, a v2 parece melhor."
    assert resultado["por_tipo"]["factual"] == pytest.approx(1.0)
    assert resultado["por_tipo"]["fora_do_escopo"] == pytest.approx(0.4), (
        "Mas, nas perguntas sem resposta nos documentos, a v2 passou a inventar."
    )


def test_comparar():
    resultado = comparar(avaliar_versao(CONJUNTO, V1)["por_item"], avaliar_versao(CONJUNTO, V2)["por_item"])
    assert resultado == {"melhorou": ["e02", "e07", "e09", "e14"], "piorou": ["e17", "e18", "e19"], "iguais": 13}


def test_intervalo_bootstrap():
    certos_v1 = avaliar_versao(CONJUNTO, V1)["por_item"]
    certos_v2 = avaliar_versao(CONJUNTO, V2)["por_item"]
    diferencas = [int(certos_v2[id_]) - int(certos_v1[id_]) for id_ in certos_v1]
    inferior, superior = intervalo_bootstrap(diferencas)
    assert inferior < 0 < superior, "Com 20 perguntas, o intervalo inclui o zero: a melhora pode ser sorte."
    assert intervalo_bootstrap(diferencas) == (inferior, superior), "Com a mesma semente, o resultado se repete."
    assert intervalo_bootstrap([1, 1, 1, 1]) == (1.0, 1.0)
    assert all(isinstance(valor, float) for valor in (inferior, superior))


def test_ler_nota_do_juiz():
    assert ler_nota_do_juiz('{"nota": 4, "justificativa": "ok"}') == 4
    assert ler_nota_do_juiz('```json\n{"nota": 2, "justificativa": "errada"}\n```') == 2
    assert ler_nota_do_juiz('Avaliação:\n{"nota": 5, "justificativa": "certa"}') == 5
    with pytest.raises(ValueError):
        ler_nota_do_juiz('{"nota": 7, "justificativa": "fora da escala"}')
    with pytest.raises(ValueError):
        ler_nota_do_juiz("Nota cinco.")


def test_juiz_premia_respostas_confiantes():
    assert media_do_juiz(JUIZ, "v1") == pytest.approx(4.4)
    assert media_do_juiz(JUIZ, "v2") == pytest.approx(4.8), (
        "O juiz deu notas altas às respostas inventadas da v2, que soam seguras."
    )


def test_concordancia_do_juiz_com_pessoas():
    pares = [
        (ler_nota_do_juiz(JUIZ[id_][versao]), nota)
        for id_, notas in HUMANOS.items()
        for versao, nota in notas.items()
    ]
    assert len(pares) == 12
    assert concordancia(pares) == {"exata": pytest.approx(0.5), "ate_um_ponto": pytest.approx(0.75)}
    assert concordancia([(5, 5), (4, 2)]) == {"exata": 0.5, "ate_um_ponto": 0.5}

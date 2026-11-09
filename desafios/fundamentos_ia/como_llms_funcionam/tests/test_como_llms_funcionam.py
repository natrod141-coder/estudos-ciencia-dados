from pathlib import Path

import pytest

from solucao import (
    aplicar_temperatura,
    cabe_na_janela,
    cortar_historico,
    custo_em_dolares,
    filtrar_top_p,
    gerar_guloso,
    probabilidades_do_proximo,
    tokenizar,
    treinar_bigramas,
)

CORPUS = (Path(__file__).parent.parent / "data" / "corpus.txt").read_text(encoding="utf-8")
VOCABULARIO = {"des", "valor", "valoriza", "ção", "token", "s", "iza"}
PROBABILIDADES = {"a": 0.5, "b": 0.3, "c": 0.2}


def test_tokenizar_pega_o_maior_pedaco_do_vocabulario():
    assert tokenizar("desvalorização", VOCABULARIO) == ["des", "valoriza", "ção"], (
        'Depois de "des", o maior pedaço do vocabulário é "valoriza", e não "valor".'
    )
    assert tokenizar("tokens", VOCABULARIO) == ["token", "s"]


def test_tokenizar_palavras_desconhecidas_e_frases():
    assert tokenizar("xyz", VOCABULARIO) == ["x", "y", "z"], "Sem pedaço no vocabulário, vale um caractere."
    assert tokenizar("tokens desvalorização", VOCABULARIO) == ["token", "s", "des", "valoriza", "ção"]


def test_aplicar_temperatura():
    assert aplicar_temperatura(PROBABILIDADES, 1) == pytest.approx(PROBABILIDADES)
    frio = aplicar_temperatura(PROBABILIDADES, 0.5)
    assert frio == pytest.approx({"a": 0.6579, "b": 0.2368, "c": 0.1053}, abs=1e-4)
    quente = aplicar_temperatura(PROBABILIDADES, 2)
    assert quente == pytest.approx({"a": 0.4154, "b": 0.3218, "c": 0.2628}, abs=1e-4)
    assert sum(quente.values()) == pytest.approx(1.0)
    with pytest.raises(ValueError):
        aplicar_temperatura(PROBABILIDADES, 0)


def test_filtrar_top_p():
    assert filtrar_top_p(PROBABILIDADES, 0.7) == pytest.approx({"a": 0.625, "b": 0.375})
    assert filtrar_top_p(PROBABILIDADES, 0.5) == pytest.approx({"a": 1.0})
    assert filtrar_top_p(PROBABILIDADES, 1.0) == pytest.approx(PROBABILIDADES)


def test_treinar_bigramas():
    modelo = treinar_bigramas(CORPUS)
    assert modelo["o"] == {"modelo": 4, "texto": 1, "próximo": 3, "contexto": 1}
    assert modelo["próximo"] == {"token": 3}
    assert modelo["."] == {"o": 5, "a": 1}, "A quebra de linha não conta: o texto é uma sequência só de palavras."


def test_probabilidades_do_proximo():
    modelo = treinar_bigramas(CORPUS)
    assert probabilidades_do_proximo(modelo, "o") == pytest.approx(
        {"modelo": 4 / 9, "texto": 1 / 9, "próximo": 3 / 9, "contexto": 1 / 9}
    )
    assert probabilidades_do_proximo(modelo, "inexistente") == {}


def test_gerar_guloso_cai_num_laco():
    modelo = treinar_bigramas(CORPUS)
    assert gerar_guloso(modelo, "o", 8) == ["o", "modelo", "prevê", "o", "modelo", "prevê", "o", "modelo", "prevê"]
    assert gerar_guloso(modelo, "limite", 3) == ["limite", ".", "o", "modelo"]
    assert gerar_guloso(modelo, "inexistente", 3) == ["inexistente"], "Sem próxima palavra conhecida, a geração para."


def test_cortar_historico_tira_as_mensagens_mais_antigas():
    mensagens = [
        {"papel": "system", "tokens": 100},
        {"papel": "user", "tokens": 300},
        {"papel": "assistant", "tokens": 400},
        {"papel": "user", "tokens": 200},
        {"papel": "assistant", "tokens": 250},
        {"papel": "user", "tokens": 150},
    ]
    cortado = cortar_historico(mensagens, 800)
    assert [m["tokens"] for m in cortado] == [100, 200, 250, 150], "As instruções de sistema ficam sempre."
    assert cortar_historico(mensagens, 2000) == mensagens
    assert len(mensagens) == 6, "Não altere a lista recebida."


def test_cortar_historico_sistema_grande_demais():
    with pytest.raises(ValueError):
        cortar_historico([{"papel": "system", "tokens": 900}, {"papel": "user", "tokens": 10}], 500)


def test_janela_e_custo():
    assert cabe_na_janela(980_000, 16_000, 1_000_000) is True
    assert cabe_na_janela(990_000, 16_000, 1_000_000) is False, "A resposta também ocupa a janela."
    assert custo_em_dolares(2_000, 500, preco_entrada=2.0, preco_saida=10.0) == pytest.approx(0.009)

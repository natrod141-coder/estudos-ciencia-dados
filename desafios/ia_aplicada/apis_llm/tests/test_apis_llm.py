import csv
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from cliente_gravado import ClienteGravado, ErroDaApi
from solucao import (
    chamar_com_retentativas,
    classificar,
    custo_em_dolares,
    extrair_texto,
    montar_requisicao,
    normalizar_rotulo,
)

DADOS = Path(__file__).parent.parent / "data"
GRAVACOES = json.loads((DADOS / "respostas_gravadas.json").read_text(encoding="utf-8"))
with open(DADOS / "avaliacoes.csv", encoding="utf-8", newline="") as arquivo:
    TEXTOS = [linha["texto"] for linha in csv.DictReader(arquivo)]
PRECOS = {"entrada": 0.10, "saida": 0.50, "escrita_cache": 0.125, "leitura_cache": 0.01}
CORTADA = TEXTOS[-1]
ROTULOS_ESPERADOS = [
    "positivo", "negativo", "neutro", "positivo", "positivo", "negativo",
    "invalido", "neutro", "negativo", "positivo", "negativo", "invalido",
]


class Relogio:
    """Faz o papel de time.sleep nos testes: anota as esperas, sem esperar de verdade."""

    def __init__(self):
        self.esperas = []

    def __call__(self, segundos):
        self.esperas.append(segundos)


def resposta(blocos, stop_reason="end_turn"):
    return SimpleNamespace(content=[SimpleNamespace(**bloco) for bloco in blocos], stop_reason=stop_reason)


def test_montar_requisicao():
    texto = TEXTOS[0]
    req = montar_requisicao(texto)
    assert req["model"] == "claude-haiku-5-5"
    assert montar_requisicao(texto, modelo="claude-sonnet-5-5")["model"] == "claude-sonnet-5-5"
    assert 0 < req["max_tokens"] <= 1024, "A resposta é uma palavra: use um teto pequeno, como 256."
    assert req["output_config"] == {"effort": "low"}
    assert all(rotulo in req["system"] for rotulo in ("positivo", "negativo", "neutro"))
    assert len(req["messages"]) == 1 and req["messages"][0]["role"] == "user"
    conteudo = req["messages"][0]["content"]
    assert conteudo.index("<avaliacao>") < conteudo.index(texto) < conteudo.index("</avaliacao>"), (
        "A avaliação vai entre <avaliacao> e </avaliacao>."
    )


def test_requisicao_aceita_pela_api():
    req = montar_requisicao(TEXTOS[1])
    for removido in ("temperature", "top_p", "top_k"):
        assert removido not in req, f"A API atual recusa o parâmetro {removido}."
    cliente = ClienteGravado()
    assert cliente.messages.create(**req).stop_reason == "end_turn"


def test_extrair_texto_ignora_blocos_de_raciocinio():
    blocos = [{"type": "thinking", "thinking": ""}, {"type": "text", "text": "posi"}, {"type": "text", "text": "tivo"}]
    assert extrair_texto(resposta(blocos)) == "positivo"
    assert extrair_texto(resposta([{"type": "thinking", "thinking": ""}], "max_tokens")) == ""


def test_normalizar_rotulo():
    assert normalizar_rotulo("positivo", "end_turn") == "positivo"
    assert normalizar_rotulo("Neutro.", "end_turn") == "neutro"
    assert normalizar_rotulo(" positivo\n", "end_turn") == "positivo"
    assert normalizar_rotulo("misto", "end_turn") == "invalido", "Só valem os três rótulos combinados."


def test_resposta_cortada_e_invalida():
    assert normalizar_rotulo("negativo", "max_tokens") == "invalido", (
        "Com stop_reason max_tokens, a resposta foi cortada no meio: não dá para confiar nela."
    )
    assert normalizar_rotulo("", "max_tokens") == "invalido"


def test_retentativa_em_erro_temporario():
    cliente, relogio = ClienteGravado(falhas=[429, 529]), Relogio()
    devolvida = chamar_com_retentativas(cliente, montar_requisicao(TEXTOS[0]), dormir=relogio)
    assert extrair_texto(devolvida) == "positivo"
    assert len(cliente.chamadas) == 3
    assert relogio.esperas == [1.0, 2.0], "A espera dobra a cada tentativa: 1 s, depois 2 s."


def test_erro_do_pedido_nao_e_repetido():
    cliente, relogio = ClienteGravado(falhas=[400]), Relogio()
    with pytest.raises(ErroDaApi):
        chamar_com_retentativas(cliente, montar_requisicao(TEXTOS[0]), dormir=relogio)
    assert len(cliente.chamadas) == 1, "Um erro 400 não some repetindo a chamada."
    assert relogio.esperas == []


def test_desiste_depois_das_tentativas():
    cliente, relogio = ClienteGravado(falhas=[529] * 5), Relogio()
    with pytest.raises(ErroDaApi):
        chamar_com_retentativas(cliente, montar_requisicao(TEXTOS[0]), tentativas=3, dormir=relogio)
    assert len(cliente.chamadas) == 3
    assert relogio.esperas == [1.0, 2.0], "Depois da última tentativa, não há por que esperar."


def test_custo_em_dolares():
    uso = SimpleNamespace(input_tokens=1000, output_tokens=200, cache_creation_input_tokens=4000, cache_read_input_tokens=None)
    assert custo_em_dolares(uso, PRECOS) == pytest.approx(0.0007)
    uso = SimpleNamespace(input_tokens=1000, output_tokens=200, cache_creation_input_tokens=0, cache_read_input_tokens=20000)
    assert custo_em_dolares(uso, PRECOS) == pytest.approx(0.0004), "A leitura do cache custa uma fração da entrada."


def custo_esperado():
    """Soma, a partir das gravações, o custo de uma chamada para cada avaliação diferente."""
    total = 0.0
    for gravacao in GRAVACOES:
        uso = gravacao["usage"]
        total += uso["input_tokens"] * PRECOS["entrada"] + uso["output_tokens"] * PRECOS["saida"]
    return total / 1_000_000


def test_classificar_usa_o_cache():
    cliente, cache = ClienteGravado(), {}
    rotulos, custo = classificar(cliente, TEXTOS, cache, PRECOS, dormir=Relogio())
    assert rotulos == ROTULOS_ESPERADOS
    assert len(cliente.chamadas) == 10, "São 12 avaliações, mas só 10 diferentes: as repetidas saem do cache."
    assert custo == pytest.approx(custo_esperado())


def test_classificar_nao_guarda_invalidos():
    cache = {}
    classificar(ClienteGravado(), TEXTOS, cache, PRECOS, dormir=Relogio())
    assert CORTADA not in cache, "Resultado inválido não vai para o cache: da próxima vez, vale tentar de novo."
    assert len(cache) == 8
    cliente = ClienteGravado()
    classificar(cliente, TEXTOS, cache, PRECOS, dormir=Relogio())
    assert len(cliente.chamadas) == 2, "Na segunda rodada, só as duas avaliações inválidas voltam para a API."


def test_classificar_com_falha_temporaria():
    cliente, relogio = ClienteGravado(falhas=[529]), Relogio()
    rotulos, _ = classificar(cliente, TEXTOS, {}, PRECOS, dormir=relogio)
    assert rotulos == ROTULOS_ESPERADOS
    assert relogio.esperas == [1.0]

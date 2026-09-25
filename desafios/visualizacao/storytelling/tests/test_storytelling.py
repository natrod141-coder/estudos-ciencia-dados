from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # desenha sem abrir janela; precisa vir antes de importar o pyplot

import matplotlib.pyplot as plt  # noqa: E402
import pytest  # noqa: E402
from matplotlib.colors import to_rgb  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

from solucao import (  # noqa: E402
    grafico_explicativo,
    ler_vendas,
    mensagem_principal,
    resumo_executivo,
    tabela_por_canal,
    titulo,
)

VENDAS = ler_vendas(Path(__file__).parent.parent / "data" / "vendas_por_canal.csv")
CANAIS = ["app", "loja física", "site"]
TITULO = "O app cresceu 280% em 2025 e virou o maior canal de vendas"


@pytest.fixture(autouse=True)
def fechar_figuras():
    yield
    plt.close("all")


def eixo_do_grafico():
    fig = grafico_explicativo(VENDAS)
    assert isinstance(fig, Figure), "Devolva a figura do matplotlib."
    assert fig.axes, "A figura está vazia."
    return fig.axes[0]


def eh_cinza(cor):
    r, g, b = to_rgb(cor)
    return abs(r - g) < 0.02 and abs(g - b) < 0.02


def test_tabela_por_canal():
    tabela = tabela_por_canal(VENDAS)
    assert list(tabela.columns) == CANAIS
    assert tabela.shape == (12, 3)
    assert tabela.iloc[0].tolist() == pytest.approx([40183.0, 120671.0, 88244.0])


def test_mensagem_principal():
    assert mensagem_principal(VENDAS) == {
        "canal": "app",
        "crescimento_pct": 280,
        "participacao_final_pct": 38.5,
        "virou_lider": True,
    }


def test_titulo_afirma_a_conclusao():
    mensagem = {"canal": "app", "crescimento_pct": 280, "participacao_final_pct": 38.5, "virou_lider": True}
    assert titulo(mensagem) == TITULO
    assert titulo({**mensagem, "virou_lider": False}) == "O app cresceu 280% em 2025 e já responde por 38,5% das vendas"


def test_grafico_destaca_so_o_canal_principal():
    ax = eixo_do_grafico()
    linhas = ax.get_lines()
    assert len(linhas) == 3, "Uma linha por canal."
    coloridas = [linha for linha in linhas if not eh_cinza(linha.get_color())]
    assert len(coloridas) == 1, "Só a linha do canal principal tem cor; as outras ficam em cinza, como contexto."
    ultimo = coloridas[0].get_ydata()[-1]
    assert ultimo == pytest.approx(152790.0) or ultimo == pytest.approx(152.79), "A linha colorida é a do app."


def test_grafico_sem_legenda_com_rotulos_diretos():
    ax = eixo_do_grafico()
    assert ax.get_legend() is None, "Troque a legenda por rótulos escritos ao lado de cada linha (ax.text)."
    textos = [texto.get_text() for texto in ax.texts]
    for canal in CANAIS:
        assert any(canal in texto for texto in textos), f"Falta o rótulo direto do canal {canal!r}."


def test_grafico_limpo_com_titulo_que_conta_a_historia():
    ax = eixo_do_grafico()
    titulos = [ax.get_title(loc=posicao) for posicao in ("left", "center", "right")]
    assert TITULO in titulos, "O título do gráfico é a mensagem principal, e não uma descrição."
    assert not ax.spines["top"].get_visible() and not ax.spines["right"].get_visible(), (
        "Tire as bordas de cima e da direita: elas não carregam informação."
    )
    assert "R$" in ax.get_ylabel(), "O eixo y precisa dizer a unidade."


def test_resumo_executivo():
    resumo = resumo_executivo(VENDAS)
    assert resumo["contexto"] == "Em 2025, as vendas somaram R$ 3,6 milhões nos três canais."
    assert resumo["achado"] == TITULO + "."
    recomendacao = resumo["recomendacao"]
    assert isinstance(recomendacao, str) and 0 < len(recomendacao.strip()) <= 200, (
        "Escreva uma recomendação curta, de até 200 caracteres."
    )

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # desenha sem abrir janela; precisa vir antes de importar o pyplot

import matplotlib.pyplot as plt  # noqa: E402
import pytest  # noqa: E402
from matplotlib.collections import PathCollection  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

from solucao import (  # noqa: E402
    grafico_categorias,
    grafico_distribuicao,
    grafico_evolucao,
    grafico_relacao,
    ler_vendas,
    vendas_por_categoria,
    vendas_por_mes,
)

CSV = Path(__file__).parent.parent / "data" / "vendas.csv"

TOTAIS_CATEGORIA = {
    "Eletrônicos": 31156.29,
    "Casa": 15178.36,
    "Moda": 13971.49,
    "Esporte": 11964.97,
    "Beleza": 4715.29,
    "Livros": 2791.53,
}
TOTAIS_MES = {
    "2026-01": 10737.60,
    "2026-02": 11318.22,
    "2026-03": 12340.41,
    "2026-04": 12560.59,
    "2026-05": 13854.83,
    "2026-06": 18966.28,
}


@pytest.fixture
def vendas():
    return ler_vendas(CSV)


@pytest.fixture(autouse=True)
def fechar_figuras():
    yield
    plt.close("all")


def primeiro_eixo(fig):
    assert isinstance(fig, Figure), "A função precisa devolver a figura do matplotlib (o fig de plt.subplots)."
    assert fig.axes, "A figura está vazia: nenhum gráfico foi desenhado nela."
    return fig.axes[0]


def retangulos(ax):
    return [p for p in ax.patches if isinstance(p, Rectangle)]


def barras_sao_verticais(barras):
    return all(b.get_y() == 0 for b in barras) and len({round(b.get_width(), 6) for b in barras}) == 1


def valores_na_ordem_de_leitura(ax):
    """Valores das barras da esquerda para a direita (verticais) ou de cima para baixo (horizontais)."""
    barras = retangulos(ax)
    if barras_sao_verticais(barras):
        return [b.get_height() for b in sorted(barras, key=lambda b: b.get_x())]
    de_cima_para_baixo = sorted(barras, key=lambda b: b.get_y(), reverse=not ax.yaxis_inverted())
    return [b.get_width() for b in de_cima_para_baixo]


def test_vendas_por_categoria(vendas):
    totais = vendas_por_categoria(vendas)
    assert list(totais.index) == list(TOTAIS_CATEGORIA), "As categorias precisam vir da maior para a menor."
    assert totais.tolist() == pytest.approx(list(TOTAIS_CATEGORIA.values()))


def test_vendas_por_mes(vendas):
    mensal = vendas_por_mes(vendas)
    assert list(mensal.index) == list(TOTAIS_MES), "Os meses precisam estar no formato AAAA-MM, em ordem."
    assert mensal.tolist() == pytest.approx(list(TOTAIS_MES.values()))


def test_grafico_categorias_tem_uma_barra_por_categoria_em_ordem(vendas):
    ax = primeiro_eixo(grafico_categorias(vendas))
    assert len(retangulos(ax)) == 6, "Esperava um gráfico de barras com uma barra por categoria."
    assert valores_na_ordem_de_leitura(ax) == pytest.approx(list(TOTAIS_CATEGORIA.values())), (
        "As barras precisam estar ordenadas da maior para a menor, na ordem de leitura."
    )


def test_grafico_categorias_comeca_do_zero(vendas):
    ax = primeiro_eixo(grafico_categorias(vendas))
    barras = retangulos(ax)
    assert barras, "Esperava um gráfico de barras."
    inicio = ax.get_ylim()[0] if barras_sao_verticais(barras) else ax.get_xlim()[0]
    assert inicio == 0, "Em gráfico de barras, o eixo dos valores precisa começar no zero."


def test_grafico_evolucao_e_de_linha(vendas):
    ax = primeiro_eixo(grafico_evolucao(vendas))
    linhas = ax.get_lines()
    assert len(linhas) >= 1, "Esperava um gráfico de linha para mostrar a evolução no tempo."
    assert not retangulos(ax), "Evolução no tempo pede linha, e não barras."
    assert list(linhas[0].get_ydata()) == pytest.approx(list(TOTAIS_MES.values())), (
        "A linha precisa ter o total de cada mês, em ordem cronológica."
    )


def test_grafico_distribuicao_e_histograma(vendas):
    ax = primeiro_eixo(grafico_distribuicao(vendas))
    barras = sorted(retangulos(ax), key=lambda b: b.get_x())
    assert len(barras) >= 5, "Esperava um histograma com pelo menos 5 faixas de valor."
    for esquerda, direita in zip(barras, barras[1:]):
        assert esquerda.get_x() + esquerda.get_width() == pytest.approx(direita.get_x()), (
            "Num histograma as faixas são encostadas, sem espaço entre as barras."
        )
    assert sum(b.get_height() for b in barras) == len(vendas), "O histograma precisa contar todos os pedidos."


def test_grafico_relacao_e_de_dispersao(vendas):
    ax = primeiro_eixo(grafico_relacao(vendas))
    pontos = [c for c in ax.collections if isinstance(c, PathCollection)]
    marcadores = [linha for linha in ax.get_lines() if linha.get_linestyle() in ("None", "none", "")]
    total = sum(len(c.get_offsets()) for c in pontos) + sum(len(linha.get_xdata()) for linha in marcadores)
    assert total == len(vendas), "Esperava um gráfico de dispersão com um ponto por pedido."


def test_todos_os_graficos_tem_titulo_e_rotulos(vendas):
    for funcao in (grafico_categorias, grafico_evolucao, grafico_distribuicao, grafico_relacao):
        ax = primeiro_eixo(funcao(vendas))
        assert ax.get_title().strip(), f"{funcao.__name__}: falta o título."
        assert ax.get_xlabel().strip(), f"{funcao.__name__}: falta o rótulo do eixo x."
        assert ax.get_ylabel().strip(), f"{funcao.__name__}: falta o rótulo do eixo y."

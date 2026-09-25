from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # desenha sem abrir janela; precisa vir antes de importar o pyplot

import matplotlib.pyplot as plt  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
import pytest  # noqa: E402
from matplotlib.collections import QuadMesh  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

from solucao import (  # noqa: E402
    faturamento_mensal_por_uf,
    grafico_interativo,
    ler_vendas,
    mapa_de_calor,
    pequenos_multiplos,
    salvar_html,
)

VENDAS = ler_vendas(Path(__file__).parent.parent / "data" / "vendas.csv")
TOTAL = 435533.02


@pytest.fixture(autouse=True)
def fechar_figuras():
    yield
    plt.close("all")


def test_faturamento_mensal_por_uf():
    mensal = faturamento_mensal_por_uf(VENDAS)
    assert mensal.shape == (18, 4), "Uma linha por mês (jan/2025 a jun/2026) e uma coluna por UF."
    assert list(mensal.columns) == ["MG", "PR", "RS", "SP"]
    assert list(mensal.index[:2]) == ["2025-01", "2025-02"]
    assert mensal.loc["2025-11"].tolist() == pytest.approx([6639.94, 16975.95, 2606.40, 10864.66])


def test_pequenos_multiplos_tem_um_grafico_por_uf():
    fig = pequenos_multiplos(VENDAS)
    assert isinstance(fig, Figure), "Devolva a figura do matplotlib."
    assert len(fig.axes) == 4, "Esperava 4 gráficos, um por UF, na mesma figura."
    assert sorted(ax.get_title() for ax in fig.axes) == ["MG", "PR", "RS", "SP"], "O título de cada gráfico é a UF."
    for ax in fig.axes:
        linhas = ax.get_lines()
        assert len(linhas) == 1 and len(linhas[0].get_ydata()) == 18, "Cada gráfico tem uma linha com os 18 meses."
    pr = next(ax for ax in fig.axes if ax.get_title() == "PR")
    assert list(pr.get_lines()[0].get_ydata()) == pytest.approx(faturamento_mensal_por_uf(VENDAS)["PR"].tolist())


def test_pequenos_multiplos_compartilham_o_eixo_y():
    fig = pequenos_multiplos(VENDAS)
    primeiro = fig.axes[0]
    assert all(primeiro.get_shared_y_axes().joined(primeiro, ax) for ax in fig.axes), (
        "Os quatro gráficos precisam da mesma escala no eixo y (sharey=True), para a comparação ser justa."
    )
    assert fig.get_suptitle().strip(), "Dê um título geral à figura (fig.suptitle)."


def test_mapa_de_calor_valores():
    fig = mapa_de_calor(VENDAS)
    ax = fig.axes[0]
    malhas = [c for c in ax.collections if isinstance(c, QuadMesh)]
    assert malhas, "Esperava um mapa de calor (sns.heatmap)."
    valores = malhas[0].get_array()
    assert valores.size == 72, "São 4 categorias x 18 meses."
    assert float(valores.sum()) == pytest.approx(TOTAL / 1000, abs=0.01), "Os valores vão em milhares de reais."


def test_mapa_de_calor_ordem_e_rotulos():
    fig = mapa_de_calor(VENDAS)
    ax = fig.axes[0]
    categorias = [rotulo.get_text() for rotulo in ax.get_yticklabels()]
    assert categorias == ["Eletrônicos", "Calçados", "Acessórios", "Vestuário"], (
        "Ordene as categorias do maior para o menor faturamento total."
    )
    assert ax.get_title().strip() and ax.get_xlabel().strip() and ax.get_ylabel().strip()
    assert len(fig.axes) == 2 and fig.axes[1].get_ylabel().strip(), "A barra de cores precisa dizer a unidade."


def test_grafico_interativo():
    fig = grafico_interativo(VENDAS)
    assert isinstance(fig, go.Figure), "Devolva a figura do plotly."
    assert len(fig.data) == 4 and {trace.type for trace in fig.data} == {"bar"}, "Uma série de barras por categoria."
    assert fig.layout.barmode == "stack", "As categorias vão empilhadas."
    assert sum(sum(trace.y) for trace in fig.data) == pytest.approx(TOTAL)
    ordem = fig.layout.xaxis.categoryarray
    assert fig.layout.xaxis.categoryorder == "total descending" or list(ordem or []) == ["PR", "SP", "MG", "RS"], (
        "Ordene as UFs do maior para o menor faturamento."
    )
    assert fig.layout.title.text, "Dê um título ao gráfico."


def test_salvar_html(tmp_path):
    caminho = tmp_path / "grafico.html"
    salvar_html(grafico_interativo(VENDAS), caminho)
    assert caminho.exists()
    conteudo = caminho.read_text(encoding="utf-8")
    assert "cdn.plot.ly" in conteudo, 'Use include_plotlyjs="cdn": o arquivo fica leve e carrega o plotly da internet.'
    assert caminho.stat().st_size < 500_000

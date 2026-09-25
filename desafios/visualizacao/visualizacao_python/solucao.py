"""Desafio: três bibliotecas, três gráficos.

Implemente cada função abaixo. Leia a docstring de cada uma antes de começar.

Regras:
- Use matplotlib em pequenos_multiplos, seaborn em mapa_de_calor e plotly em
  grafico_interativo: cada biblioteca no que ela faz melhor.
- As funções de gráfico devolvem a figura e não chamam plt.show() nem fig.show().
- Não altere a pasta tests nem o arquivo em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v

Para ver um gráfico do matplotlib ou do seaborn enquanto trabalha:
    python -c "import solucao as s; s.mapa_de_calor(s.ler_vendas('data/vendas.csv')).savefig('teste.png')"
"""

import matplotlib.pyplot as plt  # noqa: F401  (será usado em pequenos_multiplos e mapa_de_calor)
import pandas as pd
import plotly.express as px  # noqa: F401  (será usado em grafico_interativo)
import seaborn as sns  # noqa: F401  (será usado em mapa_de_calor)


def ler_vendas(caminho_csv):
    """Já está pronta: lê as vendas, com a coluna data como data."""
    return pd.read_csv(caminho_csv, parse_dates=["data"])


def faturamento_mensal_por_uf(vendas):
    """Prepara os dados dos pequenos múltiplos: faturamento de cada mês em cada UF.

    Devolve uma tabela com o mês no índice, como texto "AAAA-MM" e em ordem, uma coluna por UF
    (em ordem alfabética) e a soma do valor em cada célula (0 onde não houve venda),
    arredondada para 2 casas.
    Dica: crie a coluna do mês com .dt.strftime("%Y-%m") e use pivot_table.
    """
    raise NotImplementedError("Implemente a função faturamento_mensal_por_uf")


def pequenos_multiplos(vendas):
    """Pequenos múltiplos com matplotlib: um gráfico de linha por UF, na mesma figura.

    - Uma figura com 2 x 2 gráficos: fig, eixos = plt.subplots(2, 2, sharex=True, sharey=True).
      O sharey=True é o ponto central: com a mesma escala, dá para comparar as UFs.
    - Em cada gráfico, uma linha com o faturamento mensal de uma UF (use
      faturamento_mensal_por_uf), com a UF como título (ax.set_title).
    - Um título geral para a figura (fig.suptitle).
    Devolve a figura.
    """
    raise NotImplementedError("Implemente a função pequenos_multiplos")


def mapa_de_calor(vendas):
    """Mapa de calor com seaborn: faturamento de cada categoria (linhas) em cada mês (colunas).

    - Os valores vão em milhares de reais (divida por 1000).
    - As categorias ficam ordenadas do maior para o menor faturamento total.
    - Use sns.heatmap(tabela, ax=ax, cbar_kws={"label": "..."}): a barra de cores precisa
      dizer a unidade.
    - Título e rótulos nos dois eixos.
    Devolve a figura.
    """
    raise NotImplementedError("Implemente a função mapa_de_calor")


def grafico_interativo(vendas):
    """Gráfico interativo com plotly: faturamento de cada UF, com as categorias empilhadas.

    - Resuma o faturamento por UF e categoria (groupby).
    - Use px.bar(..., x="uf", y="valor", color="categoria", barmode="stack").
    - Ordene as UFs do maior para o menor faturamento total: category_orders={"uf": [...]}.
    - Dê um título e nomes legíveis aos eixos (labels={...}).
    Devolve a figura do plotly. Passar o mouse sobre as barras mostra os valores.
    """
    raise NotImplementedError("Implemente a função grafico_interativo")


def salvar_html(fig, caminho):
    """Salva a figura do plotly num arquivo HTML, que abre em qualquer navegador.

    Use fig.write_html(caminho, include_plotlyjs="cdn"): o arquivo fica pequeno e carrega a
    biblioteca plotly da internet ao ser aberto.
    """
    raise NotImplementedError("Implemente a função salvar_html")

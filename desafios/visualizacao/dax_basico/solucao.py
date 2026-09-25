"""Desafio: o contexto de filtro por dentro.

Aqui você implementa, em Python, o que o motor do Power BI faz quando calcula uma medida DAX.
O modelo é o modelo estrela do desafio de modelagem: fato_vendas, dim_produto, dim_loja e
dim_data, carregados como DataFrames num dicionário.

O CONTEXTO DE FILTRO é um dicionário que diz o que está filtrado, com as colunas escritas
como no DAX, tabela[coluna]:

    {"dim_loja[uf]": "PR", "dim_data[ano]": 2025}
    {"dim_loja[uf]": ["PR", "SP"]}          # lista = qualquer um dos valores
    {}                                       # nenhum filtro: tudo visível

Cada medida recebe o modelo e os filtros e devolve um número, como uma medida DAX num visual.
Acima de cada função está a medida DAX equivalente.

Regras:
- Use pandas. Nenhuma função pode alterar o modelo nem o dicionário de filtros recebido.
- Não altere a pasta tests nem os arquivos em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

from pathlib import Path

import pandas as pd

# Cada dimensão e a coluna que a liga à fato (o relacionamento um-para-muitos).
RELACIONAMENTOS = {"dim_produto": "id_produto", "dim_loja": "id_loja", "dim_data": "data"}


def carregar_modelo(pasta):
    """Já está pronta: lê as quatro tabelas do modelo."""
    pasta = Path(pasta)
    return {
        "fato_vendas": pd.read_csv(pasta / "fato_vendas.csv", parse_dates=["data"]),
        "dim_produto": pd.read_csv(pasta / "dim_produto.csv"),
        "dim_loja": pd.read_csv(pasta / "dim_loja.csv"),
        "dim_data": pd.read_csv(pasta / "dim_data.csv", parse_dates=["data"]),
    }


def separar_referencia(referencia):
    """Já está pronta: "dim_loja[uf]" vira ("dim_loja", "uf")."""
    tabela, coluna = referencia.rstrip("]").split("[")
    return tabela, coluna


def como_lista(valor):
    """Já está pronta: "PR" vira ["PR"], e uma lista continua lista."""
    return list(valor) if isinstance(valor, (list, tuple, set, pd.Series)) else [valor]


# ---------------------------------------------------------------------------------------------
# Parte 1: o contexto de filtro
# ---------------------------------------------------------------------------------------------


def filtrar_fato(modelo, filtros):
    """Devolve as linhas da fato_vendas visíveis no contexto de filtro.

    Para cada filtro "tabela[coluna]": valor(es):
    - se a tabela for "fato_vendas", filtre a fato direto pela coluna;
    - se for uma dimensão, veja quais linhas da dimensão passam no filtro, pegue as chaves
      delas (a coluna de RELACIONAMENTOS) e mantenha as linhas da fato com essas chaves.
      É assim que o filtro desce da dimensão para a fato pelo relacionamento.
    Todos os filtros valem ao mesmo tempo (E). Uma lista de valores vale como OU (.isin).
    """
    raise NotImplementedError("Implemente a função filtrar_fato")


def datas_visiveis(modelo, filtros):
    """Devolve a Series com as datas do calendário (dim_data[data]) visíveis no contexto.

    Só os filtros da dim_data importam aqui: um filtro de loja não esconde datas do calendário.
    Ex.: {"dim_data[ano]": 2026, "dim_data[mes]": 2} deixa as 28 datas de fevereiro de 2026.
    """
    raise NotImplementedError("Implemente a função datas_visiveis")


# ---------------------------------------------------------------------------------------------
# Parte 2: medidas
# ---------------------------------------------------------------------------------------------

# Faturamento = SUM ( fato_vendas[valor] )
def faturamento(modelo, filtros):
    """Soma o valor das vendas visíveis. Sem vendas, devolve 0.0 (em DAX seria BLANK)."""
    raise NotImplementedError("Implemente a função faturamento")


# Margem =
# SUMX (
#     fato_vendas,
#     fato_vendas[quantidade] * ( fato_vendas[preco_unitario] - RELATED ( dim_produto[custo_unitario] ) )
# )
def margem(modelo, filtros):
    """Soma, linha a linha das vendas visíveis, quantidade x (preço - custo do produto).

    O custo está na dim_produto: para cada linha da fato, busque o custo do produto dela
    (é o que o RELATED faz). Dica: .map() com a dim_produto indexada por id_produto.
    """
    raise NotImplementedError("Implemente a função margem")


# Faturamento todas as lojas = CALCULATE ( [Faturamento], ALL ( dim_loja ) )
def faturamento_todas_as_lojas(modelo, filtros):
    """Faturamento com os filtros da dim_loja removidos. Os outros filtros continuam valendo."""
    raise NotImplementedError("Implemente a função faturamento_todas_as_lojas")


# Participação da loja = DIVIDE ( [Faturamento], [Faturamento todas as lojas] )
def participacao_da_loja(modelo, filtros):
    """Faturamento dividido pelo faturamento de todas as lojas, entre 0 e 1.

    Como o DIVIDE, devolve None (o BLANK do DAX) se o denominador for zero.
    """
    raise NotImplementedError("Implemente a função participacao_da_loja")


# Faturamento acumulado no ano = TOTALYTD ( [Faturamento], dim_data[data] )
def faturamento_acumulado_no_ano(modelo, filtros):
    """Faturamento de 1º de janeiro até a última data visível, no ano dessa data.

    1. Pegue a última data visível (datas_visiveis(...).max()).
    2. Troque os filtros de data por um filtro "dim_data[data]" com todas as datas do
       calendário de 1º de janeiro daquele ano até essa última data.
    3. Mantenha os filtros das outras tabelas e calcule o faturamento.
    Sem nenhuma data visível, devolve 0.0.
    """
    raise NotImplementedError("Implemente a função faturamento_acumulado_no_ano")


# Faturamento ano anterior = CALCULATE ( [Faturamento], SAMEPERIODLASTYEAR ( dim_data[data] ) )
def faturamento_ano_anterior(modelo, filtros):
    """Faturamento das mesmas datas, um ano antes.

    Troque os filtros de data por um filtro "dim_data[data]" com as datas visíveis menos um
    ano (data - pd.DateOffset(years=1)), mantendo os filtros das outras tabelas.
    """
    raise NotImplementedError("Implemente a função faturamento_ano_anterior")


# Crescimento anual =
# DIVIDE ( [Faturamento] - [Faturamento ano anterior], [Faturamento ano anterior] )
def crescimento_anual(modelo, filtros):
    """Crescimento em relação ao mesmo período do ano anterior (0.25 = 25%).

    Devolve None se o faturamento do ano anterior for zero.
    """
    raise NotImplementedError("Implemente a função crescimento_anual")


def matriz(modelo, filtros, referencia_linhas, medida):
    """Calcula uma medida para cada linha de um visual de matriz, mais a linha de total.

    referencia_linhas é a coluna que vai nas linhas, como "dim_loja[uf]", e medida é uma das
    funções acima. Para cada valor diferente da coluna, em ordem, calcule a medida com os
    filtros recebidos mais o filtro da linha. Por fim, acrescente a chave "Total", com a
    medida calculada só com os filtros recebidos, sem o da linha.
    Devolve um dicionário {valor da linha: resultado, ..., "Total": resultado}.
    """
    raise NotImplementedError("Implemente a função matriz")

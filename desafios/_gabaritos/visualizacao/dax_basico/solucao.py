"""Gabarito do desafio "O contexto de filtro por dentro".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

from pathlib import Path

import pandas as pd

# Cada dimensão e a coluna que a liga à fato (o relacionamento um-para-muitos).
RELACIONAMENTOS = {"dim_produto": "id_produto", "dim_loja": "id_loja", "dim_data": "data"}


def carregar_modelo(pasta):
    pasta = Path(pasta)
    return {
        "fato_vendas": pd.read_csv(pasta / "fato_vendas.csv", parse_dates=["data"]),
        "dim_produto": pd.read_csv(pasta / "dim_produto.csv"),
        "dim_loja": pd.read_csv(pasta / "dim_loja.csv"),
        "dim_data": pd.read_csv(pasta / "dim_data.csv", parse_dates=["data"]),
    }


def separar_referencia(referencia):
    tabela, coluna = referencia.rstrip("]").split("[")
    return tabela, coluna


def como_lista(valor):
    return list(valor) if isinstance(valor, (list, tuple, set, pd.Series)) else [valor]


# ---------------------------------------------------------------------------------------------
# Parte 1: o contexto de filtro
# ---------------------------------------------------------------------------------------------


def filtrar_fato(modelo, filtros):
    fato = modelo["fato_vendas"]
    manter = pd.Series(True, index=fato.index)
    for referencia, valor in filtros.items():
        tabela, coluna = separar_referencia(referencia)
        valores = como_lista(valor)
        if tabela == "fato_vendas":
            manter &= fato[coluna].isin(valores)
        else:
            chave = RELACIONAMENTOS[tabela]
            dimensao = modelo[tabela]
            chaves_visiveis = dimensao.loc[dimensao[coluna].isin(valores), chave]
            manter &= fato[chave].isin(chaves_visiveis)  # o filtro desce pelo relacionamento
    return fato[manter]


def datas_visiveis(modelo, filtros):
    calendario = modelo["dim_data"]
    manter = pd.Series(True, index=calendario.index)
    for referencia, valor in filtros.items():
        tabela, coluna = separar_referencia(referencia)
        if tabela == "dim_data":
            manter &= calendario[coluna].isin(como_lista(valor))
    return calendario.loc[manter, "data"]


def _sem_filtros_de_data(filtros):
    return {referencia: valor for referencia, valor in filtros.items() if not referencia.startswith("dim_data[")}


# ---------------------------------------------------------------------------------------------
# Parte 2: medidas
# ---------------------------------------------------------------------------------------------


def faturamento(modelo, filtros):
    # Faturamento = SUM ( fato_vendas[valor] )
    return float(filtrar_fato(modelo, filtros)["valor"].sum())


def margem(modelo, filtros):
    # Margem = SUMX ( fato_vendas, fato_vendas[quantidade]
    #                 * ( fato_vendas[preco_unitario] - RELATED ( dim_produto[custo_unitario] ) ) )
    fato = filtrar_fato(modelo, filtros)
    custo = fato["id_produto"].map(modelo["dim_produto"].set_index("id_produto")["custo_unitario"])
    return float((fato["quantidade"] * (fato["preco_unitario"] - custo)).sum())


def faturamento_todas_as_lojas(modelo, filtros):
    # CALCULATE ( [Faturamento], ALL ( dim_loja ) )
    sem_loja = {referencia: valor for referencia, valor in filtros.items() if not referencia.startswith("dim_loja[")}
    return faturamento(modelo, sem_loja)


def participacao_da_loja(modelo, filtros):
    # DIVIDE ( [Faturamento], [Faturamento todas as lojas] )
    total = faturamento_todas_as_lojas(modelo, filtros)
    return None if total == 0 else faturamento(modelo, filtros) / total


def faturamento_acumulado_no_ano(modelo, filtros):
    # TOTALYTD ( [Faturamento], dim_data[data] )
    datas = datas_visiveis(modelo, filtros)
    if datas.empty:
        return 0.0
    ultima = datas.max()
    calendario = modelo["dim_data"]["data"]
    periodo = calendario[calendario.between(pd.Timestamp(ultima.year, 1, 1), ultima)]
    return faturamento(modelo, {**_sem_filtros_de_data(filtros), "dim_data[data]": list(periodo)})


def faturamento_ano_anterior(modelo, filtros):
    # CALCULATE ( [Faturamento], SAMEPERIODLASTYEAR ( dim_data[data] ) )
    anteriores = [data - pd.DateOffset(years=1) for data in datas_visiveis(modelo, filtros)]
    return faturamento(modelo, {**_sem_filtros_de_data(filtros), "dim_data[data]": anteriores})


def crescimento_anual(modelo, filtros):
    # DIVIDE ( [Faturamento] - [Faturamento ano anterior], [Faturamento ano anterior] )
    anterior = faturamento_ano_anterior(modelo, filtros)
    if anterior == 0:
        return None
    return (faturamento(modelo, filtros) - anterior) / anterior


def matriz(modelo, filtros, referencia_linhas, medida):
    tabela, coluna = separar_referencia(referencia_linhas)
    resultado = {}
    for valor in sorted(modelo[tabela][coluna].unique()):
        resultado[valor] = medida(modelo, {**filtros, referencia_linhas: valor})
    resultado["Total"] = medida(modelo, filtros)  # o total é recalculado, e não somado
    return resultado

"""Gabarito do desafio "Da planilha bagunçada ao relatório".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

from numbers import Number

import pandas as pd


def ler_produtos(caminho_xlsx):
    return pd.read_excel(caminho_xlsx, sheet_name="Produtos")


def ler_vendas(caminho_xlsx):
    vendas = pd.read_excel(caminho_xlsx, sheet_name="Vendas", skiprows=3)
    vendas = vendas[vendas["Data"] != "Total"].dropna(how="all")
    vendas["Quantidade"] = vendas["Quantidade"].astype(int)
    return vendas.reset_index(drop=True)


def texto_para_numero(valor):
    if isinstance(valor, Number):
        return float(valor)
    texto = str(valor).replace("R$", "").strip()
    return float(texto.replace(".", "").replace(",", "."))  # "1.234,50" -> "1234.50"


def limpar_vendas(vendas):
    limpo = vendas.copy()
    # ARRUMAR (tira espaços sobrando) e PRI.MAIÚSCULA
    limpo["Vendedor"] = limpo["Vendedor"].str.split().str.join(" ").str.title()
    limpo["Data"] = pd.to_datetime(limpo["Data"], format="%d/%m/%Y")
    limpo["Valor total"] = limpo["Valor total"].map(texto_para_numero)
    return limpo.drop_duplicates().reset_index(drop=True)


def procx(vendas, produtos):
    colunas = produtos[["Código", "Produto", "Categoria"]]
    resultado = vendas.merge(colunas, on="Código", how="left")
    resultado[["Produto", "Categoria"]] = resultado[["Produto", "Categoria"]].fillna("Não encontrado")
    return resultado


def somases(vendas, vendedor, mes):
    filtro = (vendas["Vendedor"] == vendedor) & (vendas["Data"].dt.month == mes)
    return round(float(vendas.loc[filtro, "Valor total"].sum()), 2)


def tabela_dinamica(vendas):
    tabela = pd.pivot_table(
        vendas,
        index="Vendedor",
        columns="Categoria",
        values="Valor total",
        aggfunc="sum",
        fill_value=0,
        margins=True,
        margins_name="Total",
    )
    return tabela.round(2)


def exportar_relatorio(caminho_entrada, caminho_saida):
    vendas = procx(limpar_vendas(ler_vendas(caminho_entrada)), ler_produtos(caminho_entrada))
    with pd.ExcelWriter(caminho_saida) as arquivo:
        vendas.to_excel(arquivo, sheet_name="Dados", index=False, freeze_panes=(1, 0))
        tabela_dinamica(vendas).to_excel(arquivo, sheet_name="Resumo")

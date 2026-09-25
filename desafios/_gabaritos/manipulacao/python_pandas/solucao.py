"""Gabarito do desafio "Da base crua à análise".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------------------------
# Parte 1: NumPy
# ---------------------------------------------------------------------------------------------


def padronizar(valores):
    valores = np.asarray(valores, dtype=float)
    return (valores - valores.mean()) / valores.std(ddof=1)


def aplicar_desconto(precos, quantidades, minimo=10, desconto=0.10):
    precos, quantidades = np.asarray(precos, dtype=float), np.asarray(quantidades)
    total = precos * quantidades
    return np.where(quantidades >= minimo, total * (1 - desconto), total)


def classificar_valores(valores):
    valores = np.asarray(valores, dtype=float)
    return np.select([valores < 100, valores < 500], ["baixo", "médio"], default="alto")


# ---------------------------------------------------------------------------------------------
# Parte 2: ler e conhecer os dados
# ---------------------------------------------------------------------------------------------


def ler_clientes(caminho_csv):
    return pd.read_csv(caminho_csv, parse_dates=["data_cadastro"])


def ler_pedidos(caminho_csv):
    pedidos = pd.read_csv(
        caminho_csv,
        parse_dates=["data"],
        na_values=["n/d"],
        dtype={"id_cliente": "Int64"},
    )
    return pedidos.drop_duplicates(subset="id_pedido").reset_index(drop=True)


def resumo_faltantes(tabela):
    faltantes = tabela.isna().sum()
    resumo = pd.DataFrame({"faltantes": faltantes, "percentual": (faltantes / len(tabela) * 100).round(1)})
    return resumo[resumo["faltantes"] > 0].sort_values("faltantes", ascending=False)


# ---------------------------------------------------------------------------------------------
# Parte 3: dados faltantes
# ---------------------------------------------------------------------------------------------


def tratar_faltantes(pedidos):
    tratado = pedidos.dropna(subset=["id_cliente"]).copy()
    tratado["canal"] = tratado["canal"].fillna("não informado")
    tratado["valor_imputado"] = tratado["valor"].isna()
    mediana_da_categoria = tratado.groupby("categoria")["valor"].transform("median")
    tratado["valor"] = tratado["valor"].fillna(mediana_da_categoria)
    return tratado.reset_index(drop=True)


# ---------------------------------------------------------------------------------------------
# Parte 4: juntar, agrupar e resumir
# ---------------------------------------------------------------------------------------------


def juntar_clientes(pedidos, clientes):
    colunas = clientes[["id_cliente", "nome", "estado"]]
    return pedidos.merge(colunas, on="id_cliente", how="left", validate="many_to_one")


def resumo_por_estado(pedidos):
    resumo = pedidos.groupby("estado").agg(
        pedidos=("id_pedido", "count"),
        faturamento=("valor", "sum"),
        ticket_medio=("valor", "mean"),
    )
    return resumo.round(2).sort_values("faturamento", ascending=False)


def evolucao_mensal(pedidos):
    mensal = pedidos.groupby(pedidos["data"].dt.to_period("M"))["valor"].sum()
    resultado = pd.DataFrame(
        {"faturamento": mensal.round(2), "variacao_pct": (mensal.pct_change() * 100).round(1)}
    )
    resultado.index = resultado.index.astype(str)
    return resultado


def top_clientes(pedidos, n=5):
    return pedidos.groupby("nome")["valor"].sum().nlargest(n).round(2)


def analisar(caminho_pedidos, caminho_clientes):
    pedidos = tratar_faltantes(ler_pedidos(caminho_pedidos))
    completo = juntar_clientes(pedidos, ler_clientes(caminho_clientes))
    return {
        "por_estado": resumo_por_estado(completo),
        "mensal": evolucao_mensal(completo),
        "top_clientes": top_clientes(completo),
    }

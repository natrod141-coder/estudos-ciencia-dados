"""Gabarito do desafio "O Power Query por dentro".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

from pathlib import Path

import pandas as pd

MESES = {"jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6,
         "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12}


def ler_arquivo_vendas(caminho_csv):
    vendas = pd.read_csv(caminho_csv, sep=";", decimal=",")
    vendas["data"] = pd.to_datetime(vendas["data"], format="%d/%m/%Y")
    return vendas


def combinar_arquivos(pasta):
    partes = []
    for arquivo in sorted(Path(pasta).glob("vendas_*.csv")):
        parte = ler_arquivo_vendas(arquivo)
        parte["arquivo"] = arquivo.name
        partes.append(parte)
    vendas = pd.concat(partes, ignore_index=True)
    vendas["loja"] = vendas["loja"].str.strip().str.upper()  # Aparar e MAIÚSCULAS
    return vendas


def despivotar_metas(caminho_csv):
    metas = pd.read_csv(caminho_csv, sep=";", decimal=",")
    longo = metas.melt(id_vars="loja", var_name="mes", value_name="meta")
    longo["mes"] = longo["mes"].map(MESES)
    return longo.sort_values(["loja", "mes"]).reset_index(drop=True)


def mesclar_lojas(vendas, lojas):
    colunas = lojas[["codigo", "nome", "regiao"]].rename(columns={"codigo": "loja", "nome": "nome_loja"})
    return vendas.merge(colunas, on="loja", how="left")


def adicionar_faixa(vendas):
    resultado = vendas.copy()
    resultado["faixa"] = "grande"
    resultado.loc[resultado["valor"] < 1000, "faixa"] = "média"
    resultado.loc[resultado["valor"] < 200, "faixa"] = "pequena"
    return resultado


def agrupar_por_loja_e_mes(vendas):
    agrupado = (
        vendas.assign(mes=vendas["data"].dt.month)
        .groupby(["loja", "mes"], as_index=False)
        .agg(faturamento=("valor", "sum"), vendas=("valor", "count"))
    )
    agrupado["faturamento"] = agrupado["faturamento"].round(2)
    return agrupado


def realizado_vs_meta(agrupado, metas):
    resultado = agrupado.merge(metas, on=["loja", "mes"], how="left")
    resultado["atingimento_pct"] = (resultado["faturamento"] / resultado["meta"] * 100).round(1)
    resultado["bateu_meta"] = resultado["faturamento"] >= resultado["meta"]
    return resultado


def cartoes(realizado):
    faturamento = realizado["faturamento"].sum()
    meta = realizado["meta"].sum()
    return {
        "faturamento_total": round(float(faturamento), 2),
        "meta_total": round(float(meta), 2),
        "atingimento_pct": round(float(faturamento / meta * 100), 1),
        "metas_batidas": int(realizado["bateu_meta"].sum()),
    }


def montar_relatorio(pasta_dados):
    pasta_dados = Path(pasta_dados)
    lojas = pd.read_csv(pasta_dados / "lojas.csv", sep=";")
    vendas = adicionar_faixa(mesclar_lojas(combinar_arquivos(pasta_dados / "vendas"), lojas))
    realizado = realizado_vs_meta(agrupar_por_loja_e_mes(vendas), despivotar_metas(pasta_dados / "metas.csv"))
    return {"vendas": vendas, "realizado": realizado, "cartoes": cartoes(realizado)}

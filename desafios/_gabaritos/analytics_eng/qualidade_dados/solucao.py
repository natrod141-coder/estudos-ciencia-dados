"""Gabarito do desafio "Um portão de qualidade para a carga diária".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import json

import pandas as pd


def ler_carga(caminho):
    """Já está pronta: lê a carga de pedidos, com as datas convertidas e cliente_id inteiro."""
    return pd.read_csv(caminho, dtype={"cliente_id": "Int64"}, parse_dates=["criado_em", "atualizado_em"])


def ler_regras(caminho):
    """Já está pronta: lê a lista de regras de qualidade do arquivo JSON."""
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def linhas_duplicadas(df, coluna):
    # keep=False marca todas as cópias, e não só a segunda em diante
    return df[coluna].duplicated(keep=False)


def linhas_nulas(df, coluna):
    return df[coluna].isna()


def linhas_fora_da_lista(df, coluna, valores):
    return df[coluna].notna() & ~df[coluna].isin(valores)


def linhas_fora_do_intervalo(df, coluna, minimo=None, maximo=None):
    valores = df[coluna]
    falha = pd.Series(False, index=df.index)
    if minimo is not None:
        falha |= valores < minimo
    if maximo is not None:
        falha |= valores > maximo
    # comparações com valor vazio dão False, então os vazios já ficam de fora
    return falha.fillna(False).astype(bool)


def linhas_orfas(df, coluna, chaves_validas):
    return df[coluna].notna() & ~df[coluna].isin(list(chaves_validas))


def atraso_em_horas(df, coluna, agora):
    return (pd.Timestamp(agora) - df[coluna].max()).total_seconds() / 3600


def volume_anormal(historico, linhas_hoje, desvios=3):
    serie = pd.Series(historico, dtype=float)
    return bool(abs(linhas_hoje - serie.mean()) > desvios * serie.std())


def mascara_da_regra(carga, regra, tabelas):
    tipo, coluna = regra["tipo"], regra["coluna"]
    if tipo == "unico":
        return linhas_duplicadas(carga, coluna)
    if tipo == "nao_nulo":
        return linhas_nulas(carga, coluna)
    if tipo == "valores_aceitos":
        return linhas_fora_da_lista(carga, coluna, regra["valores"])
    if tipo == "intervalo":
        return linhas_fora_do_intervalo(carga, coluna, regra.get("minimo"), regra.get("maximo"))
    if tipo == "relacao":
        return linhas_orfas(carga, coluna, tabelas[regra["tabela"]][regra["coluna_referencia"]])
    raise ValueError(f"Tipo de regra desconhecido: {tipo}")


def aplicar_regras(carga, regras, tabelas, chave="pedido_id"):
    resultados = []
    for regra in regras:
        mascara = mascara_da_regra(carga, regra, tabelas)
        ids = sorted({int(valor) for valor in carga.loc[mascara, chave]})
        resultados.append({"regra": regra["nome"], "severidade": regra["severidade"], "falhas": ids})
    return resultados


def ids_com_erro(resultados):
    return {id_ for resultado in resultados if resultado["severidade"] == "erro" for id_ in resultado["falhas"]}


def separar_quarentena(carga, resultados, chave="pedido_id"):
    na_quarentena = carga[chave].isin(ids_com_erro(resultados))
    return carga[~na_quarentena], carga[na_quarentena]


def decidir(resultados, total_pedidos, limite=0.05):
    com_erro = ids_com_erro(resultados)
    if not com_erro:
        if any(resultado["falhas"] for resultado in resultados):
            return "publicar_com_aviso"
        return "publicar"
    if len(com_erro) / total_pedidos <= limite:
        return "publicar_sem_as_ruins"
    return "bloquear"

"""Gabarito do desafio "Da planilha única ao modelo estrela".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import pandas as pd

NOMES_MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
               "agosto", "setembro", "outubro", "novembro", "dezembro"]
NOMES_DIAS = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
              "sexta-feira", "sábado", "domingo"]


def ler_planilha(caminho_csv):
    return pd.read_csv(caminho_csv, parse_dates=["data"])


def inconsistencias(plana, chave, atributos):
    combinacoes = plana[[chave, *atributos]].drop_duplicates()
    contagem = combinacoes[chave].value_counts()
    return sorted(contagem[contagem > 1].index.tolist())


def _dimensao(plana, chave, atributos, nome_id):
    # uma linha por chave, com os atributos da venda mais recente (dimensão do tipo 1)
    ultima = plana.sort_values("data").drop_duplicates(subset=chave, keep="last")
    dimensao = ultima[[chave, *atributos]].sort_values(chave).reset_index(drop=True)
    dimensao.insert(0, nome_id, range(1, len(dimensao) + 1))
    return dimensao


def criar_dim_produto(plana):
    atributos = ["produto", "categoria", "marca", "custo_unitario"]
    return _dimensao(plana, "codigo_produto", atributos, "id_produto")


def criar_dim_loja(plana):
    return _dimensao(plana, "codigo_loja", ["loja", "cidade", "uf"], "id_loja")


def criar_calendario(inicio, fim):
    datas = pd.date_range(inicio, fim, freq="D")
    return pd.DataFrame(
        {
            "data": datas,
            "ano": datas.year,
            "mes": datas.month,
            "nome_mes": [NOMES_MESES[m - 1] for m in datas.month],
            "trimestre": [f"T{t}" for t in datas.quarter],
            "ano_mes": datas.strftime("%Y-%m"),
            "dia_semana": [NOMES_DIAS[d] for d in datas.dayofweek],
            "fim_de_semana": datas.dayofweek >= 5,
        }
    )


def criar_fato(plana, dim_produto, dim_loja):
    fato = (
        plana.merge(dim_produto[["id_produto", "codigo_produto"]], on="codigo_produto", how="left")
        .merge(dim_loja[["id_loja", "codigo_loja"]], on="codigo_loja", how="left")
    )
    fato["valor"] = (fato["quantidade"] * fato["preco_unitario"]).round(2)
    return fato[["data", "pedido", "id_produto", "id_loja", "quantidade", "preco_unitario", "valor"]]


def validar_relacionamento(fato, dimensao, chave):
    return {
        "chave_unica_na_dimensao": bool(dimensao[chave].is_unique),
        "linhas_orfas_na_fato": int((~fato[chave].isin(dimensao[chave])).sum()),
    }


def granularidade_ok(tabela, colunas):
    return not tabela.duplicated(subset=colunas).any()


def montar_modelo(caminho_csv):
    plana = ler_planilha(caminho_csv)
    dim_produto = criar_dim_produto(plana)
    dim_loja = criar_dim_loja(plana)
    inicio = f"{plana['data'].min().year}-01-01"
    fim = f"{plana['data'].max().year}-12-31"
    return {
        "fato_vendas": criar_fato(plana, dim_produto, dim_loja),
        "dim_produto": dim_produto,
        "dim_loja": dim_loja,
        "dim_data": criar_calendario(inicio, fim),
    }

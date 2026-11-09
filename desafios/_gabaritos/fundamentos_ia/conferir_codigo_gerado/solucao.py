"""Gabarito do desafio "Revisar o código que a IA escreveu".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import sqlite3

import pandas as pd

CONTRAEXEMPLOS = {
    # Dias de tamanhos diferentes: a média das taxas diárias dá ao dia de 100 visitas o mesmo
    # peso do dia de 1.000. A IA devolve 0,06; o certo é 30 / 1.100, perto de 0,027.
    "taxa_de_conversao": {"diario": pd.DataFrame({"visitas": [100, 1000], "pedidos": [10, 20]})},
    # O pedido 1 tem dois livros: depois do merge, ele aparece duas vezes e pesa em dobro.
    # A IA devolve 166,67; o certo é (100 + 300) / 2 = 200.
    "ticket_medio_categoria": {
        "pedidos": pd.DataFrame({"pedido_id": [1, 2], "valor_pedido": [100.0, 300.0]}),
        "itens": pd.DataFrame(
            {"pedido_id": [1, 1, 2], "produto": ["romance", "poesia", "conto"], "categoria": ["livros"] * 3}
        ),
        "categoria": "livros",
    },
    # Com separador de milhar, o texto vira "1.234.56", que não é um número: ValueError.
    "limpar_valor": {"texto": "R$ 1.234,56"},
    # Divisão por zero: ZeroDivisionError, em vez de None.
    "variacao_percentual": {"atual": 50, "anterior": 0},
    # O fim do período vira 31/03 à meia-noite, e a venda das 15h do último dia fica de fora.
    "vendas_do_mes": {
        "vendas": pd.DataFrame({"data": pd.to_datetime(["2026-03-31 15:00"]), "valor": [100.0]}),
        "ano": 2026,
        "mes": 3,
    },
    # Um pedido sem cliente_id: NOT IN com um NULL na lista não devolve nenhuma linha.
    "clientes_sem_pedido": {
        "clientes": pd.DataFrame({"cliente_id": [1, 2], "nome": ["Ana", "Bruno"]}),
        "pedidos": pd.DataFrame({"pedido_id": [10, 11], "cliente_id": [1, None]}),
    },
}


def taxa_de_conversao(diario):
    return diario["pedidos"].sum() / diario["visitas"].sum()


def ticket_medio_categoria(pedidos, itens, categoria):
    # primeiro os pedidos da categoria, sem repetição; depois a média, uma linha por pedido
    ids = itens.loc[itens["categoria"] == categoria, "pedido_id"].unique()
    return pedidos.loc[pedidos["pedido_id"].isin(ids), "valor_pedido"].mean()


def limpar_valor(texto):
    return float(texto.replace("R$", "").strip().replace(".", "").replace(",", "."))


def variacao_percentual(atual, anterior):
    if anterior == 0:
        return None
    return (atual - anterior) / anterior * 100


def vendas_do_mes(vendas, ano, mes):
    datas = vendas["data"]
    no_mes = vendas[(datas.dt.year == ano) & (datas.dt.month == mes)]
    return no_mes["valor"].sum()


def clientes_sem_pedido(clientes, pedidos):
    conexao = sqlite3.connect(":memory:")
    clientes.to_sql("clientes", conexao, index=False)
    pedidos.to_sql("pedidos", conexao, index=False)
    # NOT EXISTS compara linha a linha e não se confunde com o NULL, ao contrário do NOT IN
    sql = """
        SELECT c.nome
        FROM clientes AS c
        WHERE NOT EXISTS (
            SELECT 1 FROM pedidos AS p WHERE p.cliente_id = c.cliente_id
        )
        ORDER BY c.nome
    """
    return [linha[0] for linha in conexao.execute(sql)]

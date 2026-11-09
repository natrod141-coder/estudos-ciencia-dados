"""Código escrito por um assistente de IA para o relatório de vendas.

Cada docstring é o pedido que foi feito ao assistente. Ele testou cada função num exemplo
simples, e todas rodaram sem erro. Mesmo assim, cada uma tem um problema, que só aparece
em algum caso.

Não altere este arquivo: escreva as versões corrigidas em solucao.py.
"""

import sqlite3

import pandas as pd


def taxa_de_conversao(diario):
    """Taxa de conversão do período: total de pedidos dividido pelo total de visitas.

    diario é um DataFrame com uma linha por dia e as colunas visitas e pedidos.
    """
    return (diario["pedidos"] / diario["visitas"]).mean()


def ticket_medio_categoria(pedidos, itens, categoria):
    """Ticket médio (valor médio por pedido) dos pedidos com pelo menos um item da categoria.

    pedidos tem as colunas pedido_id e valor_pedido, com uma linha por pedido.
    itens tem as colunas pedido_id, produto e categoria, com uma linha por item.
    """
    juntos = pedidos.merge(itens, on="pedido_id")
    da_categoria = juntos[juntos["categoria"] == categoria]
    return da_categoria["valor_pedido"].mean()


def limpar_valor(texto):
    """Converte um valor em reais escrito como texto, como 'R$ 59,90', em número."""
    return float(texto.replace("R$", "").replace(",", ".").strip())


def variacao_percentual(atual, anterior):
    """Variação percentual do valor anterior para o atual. Ex.: de 100 para 110, 10.0.

    Quando o anterior é 0, não existe variação percentual: a função devolve None.
    """
    return (atual - anterior) / anterior * 100


def vendas_do_mes(vendas, ano, mes):
    """Total vendido no mês.

    vendas é um DataFrame com as colunas data (data e hora da venda) e valor.
    """
    inicio = pd.Timestamp(year=ano, month=mes, day=1)
    fim = inicio + pd.offsets.MonthEnd(1)
    no_mes = vendas[(vendas["data"] >= inicio) & (vendas["data"] <= fim)]
    return no_mes["valor"].sum()


def clientes_sem_pedido(clientes, pedidos):
    """Nomes dos clientes que nunca fizeram pedido, em ordem alfabética.

    clientes tem as colunas cliente_id e nome. pedidos tem as colunas pedido_id e
    cliente_id, que fica vazio nas compras feitas sem cadastro.
    """
    conexao = sqlite3.connect(":memory:")
    clientes.to_sql("clientes", conexao, index=False)
    pedidos.to_sql("pedidos", conexao, index=False)
    sql = """
        SELECT nome
        FROM clientes
        WHERE cliente_id NOT IN (SELECT cliente_id FROM pedidos)
        ORDER BY nome
    """
    return [linha[0] for linha in conexao.execute(sql)]

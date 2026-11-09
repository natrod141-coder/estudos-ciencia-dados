"""Desafio: revisar o código que a IA escreveu.

Você pediu a um assistente de IA seis funções para o relatório de vendas, e ele entregou o
arquivo codigo_da_ia.py. Todas rodaram sem erro no exemplo que o assistente testou, mas cada
uma tem um problema.

Para cada função de codigo_da_ia.py:
1. Leia o código e a docstring, e descubra em que caso o código não faz o que foi pedido.
2. Registre esse caso em CONTRAEXEMPLOS: os argumentos de uma chamada em que a versão da IA
   levanta um erro ou devolve um resultado diferente da sua versão corrigida.
3. Escreva aqui a versão corrigida, com o mesmo nome e os mesmos parâmetros.

Regras:
- Não altere codigo_da_ia.py nem a pasta tests.
- Nenhuma função pode alterar o que recebe.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import sqlite3

import pandas as pd

# Para cada função, os argumentos de uma chamada em que o código da IA erra, pelo nome do
# parâmetro. Monte exemplos pequenos, à mão, em que você sabe a resposta certa. O formato é:
# CONTRAEXEMPLOS = {
#     "limpar_valor": {"texto": "..."},
#     "variacao_percentual": {"atual": ..., "anterior": ...},
#     "taxa_de_conversao": {"diario": pd.DataFrame({"visitas": [...], "pedidos": [...]})},
#     ...
# }
CONTRAEXEMPLOS = {}


def taxa_de_conversao(diario):
    """Taxa de conversão do período: total de pedidos dividido pelo total de visitas.

    diario é um DataFrame com uma linha por dia e as colunas visitas e pedidos.
    """
    raise NotImplementedError("Implemente a função taxa_de_conversao")


def ticket_medio_categoria(pedidos, itens, categoria):
    """Ticket médio (valor médio por pedido) dos pedidos com pelo menos um item da categoria.

    pedidos tem as colunas pedido_id e valor_pedido, com uma linha por pedido.
    itens tem as colunas pedido_id, produto e categoria, com uma linha por item.
    """
    raise NotImplementedError("Implemente a função ticket_medio_categoria")


def limpar_valor(texto):
    """Converte um valor em reais escrito como texto, como 'R$ 59,90', em número."""
    raise NotImplementedError("Implemente a função limpar_valor")


def variacao_percentual(atual, anterior):
    """Variação percentual do valor anterior para o atual. Ex.: de 100 para 110, 10.0.

    Quando o anterior é 0, não existe variação percentual: a função devolve None.
    """
    raise NotImplementedError("Implemente a função variacao_percentual")


def vendas_do_mes(vendas, ano, mes):
    """Total vendido no mês.

    vendas é um DataFrame com as colunas data (data e hora da venda) e valor.
    """
    raise NotImplementedError("Implemente a função vendas_do_mes")


def clientes_sem_pedido(clientes, pedidos):
    """Nomes dos clientes que nunca fizeram pedido, em ordem alfabética.

    clientes tem as colunas cliente_id e nome. pedidos tem as colunas pedido_id e
    cliente_id, que fica vazio nas compras feitas sem cadastro. Rode a consulta num banco
    SQLite em memória, como a versão da IA, ou resolva com pandas.
    """
    raise NotImplementedError("Implemente a função clientes_sem_pedido")

"""Desafio: análises com várias tabelas.

Cada pergunta abaixo vira uma consulta SQL. Escreva a consulta dentro das aspas triplas,
no lugar do comentário. As tabelas e colunas do banco estão descritas no README.

Definição usada em várias perguntas:
    faturamento = soma de quantidade x preco_unitario (da tabela itens_pedido),
    considerando só os pedidos com status 'entregue'.

Regras:
- Uma consulta por pergunta. Pode usar WITH (CTE) antes do SELECT.
- Use exatamente os nomes de coluna pedidos e respeite a ordenação pedida.
- Não altere a pasta tests nem o arquivo data/loja.sql.

Para testar uma consulta enquanto escreve, rode no terminal, dentro desta pasta:
    python -c "import solucao; print(solucao.executar(solucao.CONSULTA_1))"

Para conferir o seu trabalho:
    pytest -v
"""

import sqlite3
from pathlib import Path

import pandas as pd

SCRIPT_DO_BANCO = Path(__file__).parent / "data" / "loja.sql"


def abrir_banco():
    """Já está pronta: cria o banco da loja na memória e devolve a conexão."""
    conexao = sqlite3.connect(":memory:")
    conexao.executescript(SCRIPT_DO_BANCO.read_text(encoding="utf-8"))
    return conexao


def executar(consulta):
    """Já está pronta: roda uma consulta no banco da loja e devolve o resultado como DataFrame."""
    conexao = abrir_banco()
    try:
        return pd.read_sql_query(consulta, conexao)
    finally:
        conexao.close()


# 1. JOIN: quais são os 5 pedidos entregues de maior valor, e de quem são?
#    Colunas: id_pedido, cliente (o nome do cliente), valor_total (soma de quantidade x
#    preco_unitario do pedido, arredondada para 2 casas).
#    Do maior valor para o menor; no empate, por id_pedido.
CONSULTA_1 = """
-- escreva a consulta aqui
"""

# 2. JOIN com três tabelas: qual o faturamento de cada categoria de produto?
#    Colunas: categoria, faturamento (arredondado para 2 casas). Do maior faturamento para o menor.
CONSULTA_2 = """
-- escreva a consulta aqui
"""

# 3. LEFT JOIN: quais clientes nunca fizeram nenhum pedido (de qualquer status)?
#    Colunas: nome, estado. Em ordem alfabética de nome.
CONSULTA_3 = """
-- escreva a consulta aqui
"""

# 4. LEFT JOIN com contagem: quantos pedidos (de qualquer status) fez cada cliente do Paraná
#    (estado 'PR'), incluindo quem não fez nenhum?
#    Colunas: nome, pedidos. Do cliente com mais pedidos para o com menos; no empate, por nome.
CONSULTA_4 = """
-- escreva a consulta aqui
"""

# 5. Subconsulta: quais produtos ativos custam mais que o preço médio dos produtos ativos?
#    Colunas: nome, preco. Do mais caro para o mais barato.
CONSULTA_5 = """
-- escreva a consulta aqui
"""

# 6. NOT EXISTS: quais produtos nunca apareceram em nenhum pedido?
#    Colunas: nome, categoria. Em ordem alfabética de nome.
CONSULTA_6 = """
-- escreva a consulta aqui
"""

# 7. CTE: quais clientes com pelo menos 3 pedidos entregues têm ticket médio acima do valor
#    médio de todos os pedidos entregues?
#    Ticket médio do cliente = média do valor dos pedidos entregues dele. O valor de um pedido
#    é a soma de quantidade x preco_unitario dos seus itens.
#    Colunas: nome, pedidos (quantidade de pedidos entregues), ticket_medio (arredondado para
#    2 casas). Do maior ticket médio para o menor.
CONSULTA_7 = """
-- escreva a consulta aqui
"""

# 8. Função de janela: qual é o produto mais vendido de cada categoria, em quantidade de
#    unidades nos pedidos entregues?
#    Colunas: categoria, produto (o nome do produto), quantidade. Uma linha por categoria,
#    em ordem alfabética de categoria. No empate de quantidade, vence o nome que vem antes.
#    Dica: ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...).
CONSULTA_8 = """
-- escreva a consulta aqui
"""

# 9. Total acumulado: qual o faturamento de cada mês e o acumulado desde janeiro?
#    Colunas: mes (texto 'AAAA-MM'), faturamento, acumulado (os dois arredondados para 2 casas).
#    Em ordem de mês. Dica: strftime('%Y-%m', data_pedido) e SUM(...) OVER (ORDER BY ...).
CONSULTA_9 = """
-- escreva a consulta aqui
"""

# 10. LAG: quanto o faturamento de cada mês variou, em %, em relação ao mês anterior?
#     Colunas: mes, faturamento (arredondado para 2 casas), variacao_pct (arredondada para
#     1 casa; NULL no primeiro mês). Em ordem de mês.
#     Calcule a variação com o faturamento sem arredondar.
CONSULTA_10 = """
-- escreva a consulta aqui
"""

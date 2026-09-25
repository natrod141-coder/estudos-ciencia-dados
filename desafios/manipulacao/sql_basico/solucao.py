"""Desafio: perguntas ao banco da loja.

Cada pergunta abaixo vira uma consulta SQL. Escreva a consulta dentro das aspas triplas,
no lugar do comentário. As tabelas e colunas do banco estão descritas no README.

Regras:
- Uma consulta por pergunta, com um único comando SELECT.
- Use exatamente os nomes de coluna pedidos (com AS quando a pergunta der um nome novo).
- Respeite a ordenação pedida: o teste compara as linhas na ordem.
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


# 1. Quais são os 5 produtos mais caros?
#    Colunas: nome, categoria, preco. Do mais caro para o mais barato; no empate, por nome.
CONSULTA_1 = """
-- escreva a consulta aqui
"""

# 2. Quais produtos da categoria 'Informática' custam até R$ 500 (inclusive)?
#    Colunas: nome, preco. Do mais barato para o mais caro.
CONSULTA_2 = """
-- escreva a consulta aqui
"""

# 3. Quais clientes de SP ou RJ têm o nome começando com a letra A?
#    Colunas: nome, cidade, estado. Em ordem alfabética de nome.
CONSULTA_3 = """
-- escreva a consulta aqui
"""

# 4. Quais clientes não têm e-mail cadastrado?
#    Colunas: nome, estado. Em ordem alfabética de nome.
CONSULTA_4 = """
-- escreva a consulta aqui
"""

# 5. Em quais estados a loja tem clientes? Cada estado uma vez só.
#    Coluna: estado. Em ordem alfabética.
CONSULTA_5 = """
-- escreva a consulta aqui
"""

# 6. Quantos pedidos existem, quanto de frete foi cobrado no total e qual o frete médio?
#    Colunas: total_pedidos, frete_total, frete_medio (os dois fretes arredondados para 2 casas).
#    Uma linha só, considerando todos os pedidos.
CONSULTA_6 = """
-- escreva a consulta aqui
"""

# 7. Quantos pedidos há em cada status?
#    Colunas: status, pedidos. Do status com mais pedidos para o com menos.
CONSULTA_7 = """
-- escreva a consulta aqui
"""

# 8. Quais estados têm pelo menos 5 clientes?
#    Colunas: estado, clientes. Do estado com mais clientes para o com menos; no empate, por estado.
CONSULTA_8 = """
-- escreva a consulta aqui
"""

# 9. Em março de 2026, quantos pedidos não cancelados vieram de cada canal?
#    Colunas: canal, pedidos. Do canal com mais pedidos para o com menos; no empate, por canal.
#    Dica: as datas estão como texto 'AAAA-MM-DD', que em ordem alfabética também fica em
#    ordem cronológica.
CONSULTA_9 = """
-- escreva a consulta aqui
"""

# 10. Quantos produtos ativos (ativo = 1) há em cada faixa de preço?
#     Faixas: 'econômico' (menos de 100), 'intermediário' (de 100 até menos de 1000) e
#     'premium' (1000 ou mais), escritas exatamente assim.
#     Colunas: faixa, produtos. Da faixa com mais produtos para a com menos; no empate, por faixa.
CONSULTA_10 = """
-- escreva a consulta aqui
"""

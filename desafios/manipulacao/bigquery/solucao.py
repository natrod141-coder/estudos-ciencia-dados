"""Desafio: consultas que cabem no orçamento.

O desafio tem duas partes:
1. Funções em Python que calculam quanto uma consulta custaria no BigQuery.
2. Consultas no estilo do BigQuery, escritas para o DuckDB, que roda no seu computador.
   A tabela no README mostra as poucas diferenças de sintaxe entre os dois.

Regras:
- Na parte 1, use pandas e o módulo math.
- Na parte 2, uma consulta por pergunta. Pode usar WITH antes do SELECT.
  Use exatamente os nomes de coluna pedidos e respeite a ordenação pedida.
- Não altere a pasta tests nem os arquivos em data.

Para testar uma consulta enquanto escreve, rode no terminal, dentro desta pasta:
    python -c "import solucao; print(solucao.executar(solucao.CONSULTA_1))"

Para conferir o seu trabalho:
    pytest -v
"""

import math  # noqa: F401  (será usado em bytes_faturados)
from pathlib import Path

import duckdb
import pandas as pd

DADOS = Path(__file__).parent / "data"
MB = 2**20  # 1 MB (mebibyte) = 1.048.576 bytes
TIB = 2**40  # 1 TiB (tebibyte) = 1.099.511.627.776 bytes


def abrir_banco():
    """Já está pronta: cria as tabelas pedidos e eventos no DuckDB, a partir dos arquivos JSON."""
    conexao = duckdb.connect()
    conexao.execute(
        f"""
        CREATE TABLE pedidos AS
        SELECT * FROM read_json('{(DADOS / "pedidos.jsonl").as_posix()}', columns = {{
            'id_pedido': 'VARCHAR', 'data_pedido': 'DATE', 'id_cliente': 'VARCHAR', 'canal': 'VARCHAR',
            'itens': 'STRUCT(sku VARCHAR, categoria VARCHAR, quantidade INTEGER, preco DOUBLE)[]'
        }})
        """
    )
    conexao.execute(
        f"""
        CREATE TABLE eventos AS
        SELECT * FROM read_json('{(DADOS / "eventos.jsonl").as_posix()}', columns = {{
            'id_evento': 'VARCHAR', 'id_usuario': 'VARCHAR', 'evento': 'VARCHAR', 'momento': 'TIMESTAMP',
            'versao_app': 'VARCHAR', 'cupom': 'VARCHAR', 'ingerido_em': 'TIMESTAMP'
        }})
        """
    )
    return conexao


def executar(consulta):
    """Já está pronta: roda uma consulta no DuckDB e devolve o resultado como DataFrame."""
    with abrir_banco() as conexao:
        return conexao.sql(consulta).df()


# ---------------------------------------------------------------------------------------------
# Parte 1: quanto custa uma consulta
# ---------------------------------------------------------------------------------------------


def bytes_faturados(tamanhos, colunas, particoes=None):
    """Calcula quantos bytes o BigQuery cobraria por uma consulta.

    tamanhos é um DataFrame com as colunas particao, coluna e bytes: o tamanho de cada coluna
    em cada partição da tabela. colunas é a lista de colunas que a consulta lê, e particoes é
    a lista de partições lidas (None = todas).

    Passo a passo, seguindo as regras de cobrança do BigQuery sob demanda:
    1. Some os bytes das colunas lidas, só nas partições lidas.
    2. Arredonde para cima, para um número inteiro de MB: math.ceil(total / MB) * MB.
    3. Cobre no mínimo 10 MB: devolva o maior entre o arredondado e 10 * MB.
    Devolve um inteiro, em bytes.
    """
    raise NotImplementedError("Implemente a função bytes_faturados")


def custo_dolares(bytes_, preco_por_tib=6.25):
    """Converte bytes faturados em dólares: bytes ÷ TIB x preço por TiB. Não arredonde."""
    raise NotImplementedError("Implemente a função custo_dolares")


def comparar_consultas(caminho_csv, preco_por_tib=6.25):
    """Compara o custo de três versões da mesma consulta sobre a tabela de eventos do app.

    O CSV tem o tamanho de cada coluna em cada partição diária da tabela de produção
    (90 dias, de janeiro a março de 2026). A análise precisa só das colunas id_usuario,
    evento e momento, e só da primeira semana de março.

    Devolve um dicionário com o custo em dólares, arredondado para 2 casas, de:
    - "select_tudo_com_limit": SELECT * ... LIMIT 10. Lê todas as colunas de todas as
      partições: no BigQuery, o LIMIT não reduz o que é lido.
    - "so_colunas_necessarias": só as três colunas, em todas as partições.
    - "colunas_e_particoes": só as três colunas, e só as partições de 2026-03-01 a
      2026-03-07 (um WHERE na coluna de partição).
    """
    raise NotImplementedError("Implemente a função comparar_consultas")


# ---------------------------------------------------------------------------------------------
# Parte 2: consultas no estilo BigQuery (escritas em DuckDB)
#
# Tabelas:
#   pedidos (id_pedido, data_pedido DATE, id_cliente, canal,
#            itens: lista de STRUCT(sku, categoria, quantidade, preco))
#   eventos (id_evento, id_usuario, evento, momento TIMESTAMP, versao_app, cupom, ingerido_em TIMESTAMP)
# ---------------------------------------------------------------------------------------------

# 1. UNNEST: qual o faturamento de cada categoria em março?
#    Faturamento = soma de quantidade x preco dos itens.
#    Colunas: categoria, faturamento (arredondado para 2 casas). Do maior para o menor.
#    Dica: FROM pedidos, UNNEST(itens) AS t(item), e depois item.categoria.
CONSULTA_1 = """
-- escreva a consulta aqui
"""

# 2. Filtro de partição: na semana de 2 a 8 de março, quantos pedidos e quantas unidades
#    foram vendidas por dia?
#    Colunas: data_pedido, pedidos, unidades (soma das quantidades). Em ordem de data.
CONSULTA_2 = """
-- escreva a consulta aqui
"""

# 3. QUALIFY: a ingestão gravou alguns eventos duas vezes (mesmo id_evento, ingerido_em
#    diferente). Sem as duplicatas, ficando com a versão ingerida por último, quantos eventos
#    há de cada tipo?
#    Colunas: evento, eventos. Do tipo com mais eventos para o com menos.
CONSULTA_3 = """
-- escreva a consulta aqui
"""

# 4. Funil: em cada versão do app, quantos usuários diferentes visualizaram um produto,
#    adicionaram ao carrinho e compraram, e qual a conversão?
#    Colunas: versao_app, visualizaram, adicionaram, compraram, conversao_pct
#    (compraram ÷ visualizaram x 100, arredondado para 1 casa). Em ordem de versão.
#    Dica: COUNT(DISTINCT IF(evento = '...', id_usuario, NULL)).
CONSULTA_4 = """
-- escreva a consulta aqui
"""

# 5. Conversão segura: nas compras (evento 'comprou', sem duplicatas) que informaram cupom,
#    o cupom deveria ser um número inteiro de desconto em %, mas alguns vieram sujos.
#    Colunas: cupons_validos (os que viram inteiro), cupons_invalidos (os que não viram),
#    desconto_medio (média dos válidos, arredondada para 2 casas).
#    Dica: TRY_CAST(cupom AS INTEGER) devolve NULL quando o texto não é número
#    (no BigQuery, SAFE_CAST).
CONSULTA_5 = """
-- escreva a consulta aqui
"""

# 6. Datas e janela: qual o faturamento de cada semana (começando na segunda-feira) e a
#    participação de cada semana no total?
#    Colunas: semana (DATE da segunda-feira), faturamento (2 casas), participacao_pct
#    (1 casa). Em ordem de semana.
#    Dica: CAST(date_trunc('week', data_pedido) AS DATE) e SUM(...) OVER ().
CONSULTA_6 = """
-- escreva a consulta aqui
"""

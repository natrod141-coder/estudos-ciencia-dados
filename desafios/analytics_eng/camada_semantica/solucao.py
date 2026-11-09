"""Desafio: uma camada semântica de bolso.

O arquivo modelo_semantico.json define, num lugar só, as medidas, as dimensões e as métricas
da tabela de pedidos. Você vai escrever o compilador que transforma um pedido como
"receita e ticket médio por região, por mês" na consulta SQL certa, do mesmo jeito que as
ferramentas de camada semântica fazem.

Regras:
- As funções devolvem texto SQL. Os testes rodam esse SQL no DuckDB e conferem os números.
- Nenhuma função pode alterar o que recebe.
- Não altere a pasta tests, o modelo_semantico.json nem os arquivos em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import json
from pathlib import Path

import duckdb

GRAOS = {"dia": "day", "semana": "week", "mes": "month", "trimestre": "quarter", "ano": "year"}


def ler_modelo(caminho):
    """Já está pronta: lê o modelo semântico do arquivo JSON."""
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def criar_banco(caminho_csv):
    """Já está pronta: carrega o CSV de pedidos numa tabela pedidos, num DuckDB em memória."""
    conexao = duckdb.connect()
    conexao.execute(f"create table pedidos as select * from read_csv('{Path(caminho_csv).as_posix()}')")
    return conexao


def consultar(conexao, modelo, metricas, por=(), grao=None, filtros=()):
    """Já está pronta: compila a consulta com a sua função compilar e devolve um DataFrame."""
    return conexao.execute(compilar(modelo, metricas, por, grao, filtros)).df()


def sql_da_medida(medida):
    """Devolve a agregação SQL de uma medida do modelo.

    {"agregacao": "sum", "coluna": "valor"}             ->  SUM(valor)
    {"agregacao": "count"}                              ->  COUNT(*)
    {"agregacao": "count_distinct", "coluna": "x"}      ->  COUNT(DISTINCT x)
    Levanta ValueError para qualquer outra agregação.
    """
    raise NotImplementedError("Implemente a função sql_da_medida")


def sql_da_metrica(modelo, nome):
    """Devolve a expressão SQL de uma métrica do modelo, pelo nome.

    - Métrica "simples": a agregação da medida. Se a métrica tem "filtro", a agregação só
      considera as linhas do filtro: SUM(valor) FILTER (WHERE status = 'aprovado').
    - Métrica "razao": a expressão do numerador dividida pela do denominador, as duas métricas
      do próprio modelo. Proteja contra divisão por zero com NULLIF(denominador, 0). Assim, a
      razão é sempre calculada sobre os totais do grupo pedido.
    Levanta ValueError se a métrica não existe no modelo.
    """
    raise NotImplementedError("Implemente a função sql_da_metrica")


def expressao_de_tempo(coluna, grao):
    """Devolve a expressão SQL que leva a coluna de data para o começo do período do grão.

    O grão é uma das chaves de GRAOS. Ex.: ("data_pedido", "mes") dá
    date_trunc('month', data_pedido). Levanta ValueError para um grão que não está em GRAOS.
    """
    raise NotImplementedError("Implemente a função expressao_de_tempo")


def compilar(modelo, metricas, por=(), grao=None, filtros=()):
    """Monta a consulta SQL completa.

    - metricas: lista de nomes de métricas, com pelo menos uma.
    - por: lista de dimensões para agrupar, todas da lista "dimensoes" do modelo.
    - grao: None, ou um grão de tempo. A coluna de tempo vem primeiro e se chama como o grão
      (por exemplo, mes). Depois vêm as dimensões, na ordem pedida, e depois as métricas,
      cada uma com o próprio nome.
    - filtros: lista de condições SQL, que entram no WHERE ligadas por AND.
    A consulta lê a tabela do modelo, agrupa e ordena pelas colunas de tempo e de dimensão
    (se houver). Levanta ValueError para métrica, dimensão ou grão desconhecidos, ou para uma
    lista de métricas vazia.
    """
    raise NotImplementedError("Implemente a função compilar")

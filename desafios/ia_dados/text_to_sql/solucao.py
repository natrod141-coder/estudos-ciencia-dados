"""Desafio: perguntas em português, respostas em SQL.

O time comercial quer fazer perguntas sobre as vendas sem escrever SQL. Você vai montar o caminho
de um text-to-SQL: descrever o banco para o modelo, montar o prompt com o esquema e as regras do
negócio, extrair o SQL da resposta, barrar comandos perigosos, executar num banco somente leitura
e medir se o resultado é o mesmo da consulta escrita por uma pessoa.

O modelo é o ModeloGravado, de modelo_gravado.py, com a mesma cara do cliente do SDK da Anthropic e
respostas gravadas: o desafio roda sem chave de API e sem custo.

Regras:
- Use re e duckdb. Nenhuma função pode alterar o que recebe.
- Não altere modelo_gravado.py, a pasta tests nem os arquivos em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import re
from pathlib import Path

import duckdb

DADOS = Path(__file__).parent / "data"
REGRAS = [
    "Receita é a soma de vendas.valor das vendas com status 'aprovada'.",
    "Vendas canceladas não entram em receita, ticket médio nem quantidade vendida.",
    "As datas estão em vendas.data, do tipo DATE, de janeiro a março de 2026.",
]
PROIBIDAS = [
    "insert", "update", "delete", "drop", "alter", "create", "attach", "detach", "copy",
    "pragma", "install", "load", "export", "import", "call", "truncate", "set",
]


def criar_banco(caminho):
    """Já está pronta: cria um arquivo do DuckDB com as tabelas produtos, lojas e vendas."""
    with duckdb.connect(str(caminho)) as conexao:
        for tabela in ("produtos", "lojas", "vendas"):
            arquivo = (DADOS / f"{tabela}.csv").as_posix()
            conexao.execute(f"create or replace table {tabela} as select * from read_csv('{arquivo}')")
    return caminho


def abrir_somente_leitura(caminho):
    """Já está pronta: abre o banco sem permissão de escrita."""
    return duckdb.connect(str(caminho), read_only=True)


def descrever_esquema(conexao, max_valores=10):
    """Descreve as tabelas do banco para o modelo, em texto.

    Para cada tabela do esquema main, em ordem alfabética, uma linha
        Tabela lojas: loja_id (BIGINT), cidade (VARCHAR), regiao (VARCHAR)
    com as colunas na ordem da tabela (information_schema.columns, pela ordinal_position). Depois
    dela, para cada coluna VARCHAR com no máximo max_valores valores diferentes, uma linha
        "  Valores de regiao: Nordeste, Sudeste, Sul"
    com os valores em ordem alfabética. Devolve as linhas juntas com "\\n".
    """
    raise NotImplementedError("Implemente a função descrever_esquema")


def montar_mensagens(pergunta, esquema, regras=REGRAS):
    """Devolve (system, messages).

    system: diga que a tarefa é escrever SQL para o DuckDB, que só podem ser usadas as tabelas,
    colunas e valores do esquema, que a resposta é uma única consulta SELECT dentro de um bloco
    ```sql, e que, se a pergunta pedir para alterar ou apagar dados, a resposta é
    "Não posso alterar dados.". Inclua o esquema entre <esquema> e </esquema> e cada regra entre
    <regras> e </regras>.
    messages: uma mensagem só, do usuário, com a pergunta.
    """
    raise NotImplementedError("Implemente a função montar_mensagens")


def extrair_sql(resposta):
    """Devolve o SQL da resposta do modelo.

    Se houver um bloco ```sql, devolva o conteúdo dele, sem os espaços das pontas. Se não houver,
    mas o texto começar com SELECT ou WITH, devolva o texto. Senão, devolva None.
    """
    raise NotImplementedError("Implemente a função extrair_sql")


def consulta_segura(sql):
    """Devolve (True, "") se a consulta parece segura, ou (False, motivo).

    É segura se: depois de tirar um ponto e vírgula do fim, não sobra nenhum outro (um comando
    só); começa com SELECT ou WITH; e nenhuma palavra de PROIBIDAS aparece como palavra inteira,
    sem diferenciar maiúsculas, fora de textos entre aspas simples.
    """
    raise NotImplementedError("Implemente a função consulta_segura")


def executar(conexao, sql):
    """Executa a consulta (sem o ponto e vírgula do fim) e devolve as linhas, com fetchall().
    Não esconda os erros do banco: deixe a exceção subir."""
    raise NotImplementedError("Implemente a função executar")


def mesmo_resultado(linhas_a, linhas_b):
    """True se os dois resultados têm as mesmas linhas, sem importar a ordem das linhas.

    Arredonde os números para duas casas antes de comparar. Os nomes das colunas não importam:
    a comparação é só dos valores.
    """
    raise NotImplementedError("Implemente a função mesmo_resultado")


def avaliar(cliente, conexao, perguntas, modelo="claude-opus-5-5"):
    """Avalia o text-to-SQL em todas as perguntas de data/perguntas.json.

    Para cada pergunta: monte as mensagens com o esquema do banco, chame
    cliente.messages.create(model=modelo, max_tokens=2048, system=..., messages=...), junte o
    texto dos blocos de tipo "text" e extraia o SQL. Classifique, nesta ordem:
    - "sem_sql": a resposta não tem SQL;
    - "inseguras": o SQL não passa em consulta_segura (e não é executado);
    - "com_erro": o banco recusa a consulta (duckdb.Error);
    - "corretas" ou "erradas": o resultado é, ou não, o mesmo da sql_referencia.
    Devolve {"corretas": ids, "erradas": ids, "com_erro": ids, "inseguras": ids, "sem_sql": ids}.
    """
    raise NotImplementedError("Implemente a função avaliar")

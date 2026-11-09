"""Desafio: conferir as respostas do assistente.

Um assistente de IA respondeu a dez perguntas do time comercial. Para as perguntas sobre
números, ele mostrou a consulta SQL que usou. Para as perguntas sobre as regras do relatório,
ele citou trechos do documento. As respostas estão em data/respostas_modelo.json.

Você vai escrever um verificador que confere cada resposta contra o banco de vendas e contra
o documento de regras, e separa as respostas em cinco categorias (veja CATEGORIAS).

Regras:
- Use só a biblioteca padrão do Python (re, sqlite3, csv, json).
- Nenhuma função pode alterar o que recebe.
- Não altere a pasta tests nem os arquivos em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import csv
import sqlite3

CATEGORIAS = ("correta", "valor_errado", "sql_invalida", "citacao_inventada", "sem_fonte")


def criar_banco(caminho_csv):
    """Já está pronta: carrega o CSV numa tabela vendas, num banco SQLite em memória.

    A tabela tem as colunas mes (texto, como '2026-03'), regiao (texto) e faturamento (número).
    """
    conexao = sqlite3.connect(":memory:")
    conexao.execute("CREATE TABLE vendas (mes TEXT, regiao TEXT, faturamento REAL)")
    with open(caminho_csv, encoding="utf-8", newline="") as arquivo:
        linhas = [(l["mes"], l["regiao"], float(l["faturamento"])) for l in csv.DictReader(arquivo)]
    conexao.executemany("INSERT INTO vendas VALUES (?, ?, ?)", linhas)
    return conexao


def extrair_numeros(texto):
    """Devolve a lista de números que aparecem no texto, escritos no formato brasileiro.

    O ponto separa os milhares e a vírgula separa os decimais. O ponto final de uma frase
    não faz parte do número. Devolve floats, na ordem em que aparecem.
    Ex.: "Cresceu 12,3% e chegou a R$ 1.234,50." dá [12.3, 1234.5].
    """
    raise NotImplementedError("Implemente a função extrair_numeros")


def valores_conferem(afirmado, real, tolerancia=0.01):
    """Devolve True se o valor afirmado está dentro da tolerância relativa do valor real.

    Com a tolerância padrão de 0,01 (1%), afirmar 99 quando o real é 100 confere, e
    afirmar 98 não confere. A diferença é medida em relação ao valor real.
    """
    raise NotImplementedError("Implemente a função valores_conferem")


def executar_consulta(conexao, sql):
    """Executa a consulta e devolve uma tupla (valor, erro).

    - Se a consulta rodar, valor é a primeira coluna da primeira linha do resultado, e erro
      é None. Se não houver nenhuma linha, devolva (None, None).
    - Se o banco recusar a consulta (sqlite3.Error), devolva (None, mensagem do erro).
    """
    raise NotImplementedError("Implemente a função executar_consulta")


def citacao_existe(citacao, documento):
    """Devolve True se a citação aparece no documento, palavra por palavra.

    Compare sem diferenciar maiúsculas de minúsculas, e trate qualquer sequência de espaços
    e quebras de linha como um espaço só: no documento, uma frase pode estar quebrada em
    duas linhas.
    """
    raise NotImplementedError("Implemente a função citacao_existe")


def classificar_resposta(resposta, conexao, documento):
    """Classifica uma resposta do assistente numa das CATEGORIAS.

    resposta é um dicionário com "id", "pergunta" e "resposta", e às vezes "sql" ou
    "citacoes". Siga as regras nesta ordem:
    1. Se a resposta tem "sql", execute a consulta.
       - Se o banco recusar a consulta: "sql_invalida".
       - Se o primeiro número do texto da resposta conferir com o valor da consulta:
         "correta". Se não conferir, se a consulta não devolver valor (None), ou se o
         texto não tiver número: "valor_errado".
    2. Se não tem "sql", mas tem "citacoes" com pelo menos um trecho:
       - Se todas as citações existem no documento: "correta".
       - Se pelo menos uma não existe: "citacao_inventada".
    3. Sem SQL e sem citações, não há como conferir: "sem_fonte".
    """
    raise NotImplementedError("Implemente a função classificar_resposta")


def relatorio(respostas, conexao, documento):
    """Classifica todas as respostas e agrupa os ids por categoria.

    Devolve um dicionário com as cinco CATEGORIAS como chaves, mesmo as que ficarem vazias.
    Cada valor é a lista de ids, na ordem em que as respostas aparecem.
    """
    raise NotImplementedError("Implemente a função relatorio")

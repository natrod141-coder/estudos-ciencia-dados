"""Gabarito do desafio "Um agente de dados, com ferramentas e com limites".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import json
import re
from pathlib import Path

import duckdb

DADOS = Path(__file__).parent / "data"
LIMITE_DE_LINHAS = 50
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


def e_somente_leitura(sql):
    """Já está pronta: devolve (True, "") para um único SELECT seguro, ou (False, motivo)."""
    texto = sql.strip().rstrip(";").strip()
    if ";" in texto:
        return False, "mais de um comando"
    if not re.match(r"(select|with)\b", texto, re.IGNORECASE):
        return False, "não começa com SELECT ou WITH"
    sem_textos = re.sub(r"'[^']*'", "''", texto.lower())
    for palavra in PROIBIDAS:
        if re.search(rf"\b{palavra}\b", sem_textos):
            return False, f"palavra proibida: {palavra}"
    return True, ""


def esquema(propriedades, obrigatorias):
    return {"type": "object", "properties": propriedades, "required": obrigatorias, "additionalProperties": False}


def definir_ferramentas():
    return [
        {
            "name": "listar_tabelas",
            "description": "Lista as tabelas do banco de vendas que podem ser consultadas.",
            "strict": True,
            "input_schema": esquema({}, []),
        },
        {
            "name": "descrever_tabela",
            "description": "Mostra as colunas e os tipos de uma tabela do banco de vendas.",
            "strict": True,
            "input_schema": esquema({"tabela": {"type": "string", "description": "O nome da tabela."}}, ["tabela"]),
        },
        {
            "name": "consultar_sql",
            "description": "Executa uma única consulta SELECT no banco de vendas, só de leitura, e devolve até 50 linhas.",
            "strict": True,
            "input_schema": esquema({"sql": {"type": "string", "description": "A consulta SELECT, no SQL do DuckDB."}}, ["sql"]),
        },
        {
            "name": "enviar_relatorio",
            "description": "Envia um relatório por e-mail. Só é executado depois da aprovação de uma pessoa.",
            "strict": True,
            "input_schema": esquema(
                {
                    "destinatario": {"type": "string", "description": "O e-mail de quem recebe."},
                    "texto": {"type": "string", "description": "O texto do relatório."},
                },
                ["destinatario", "texto"],
            ),
        },
    ]


def executar_ferramenta(nome, argumentos, conexao, aprovar):
    tabelas = [linha[0] for linha in conexao.execute(
        "select table_name from information_schema.tables where table_schema = 'main' order by table_name"
    ).fetchall()]
    if nome == "listar_tabelas":
        return ", ".join(tabelas), False
    if nome == "descrever_tabela":
        tabela = argumentos.get("tabela")
        if tabela not in tabelas:  # o nome vem do modelo: só vale um nome que existe
            return f"Tabela desconhecida: {tabela}", True
        colunas = conexao.execute(
            "select column_name, data_type from information_schema.columns "
            "where table_name = ? order by ordinal_position", [tabela]
        ).fetchall()
        return ", ".join(f"{coluna} ({tipo})" for coluna, tipo in colunas), False
    if nome == "consultar_sql":
        sql = argumentos.get("sql", "")
        permitido, motivo = e_somente_leitura(sql)
        if not permitido:
            return f"Consulta bloqueada: {motivo}", True
        try:
            cursor = conexao.execute(sql.strip().rstrip(";"))
            colunas = [descricao[0] for descricao in cursor.description]
            linhas = cursor.fetchmany(LIMITE_DE_LINHAS)
        except duckdb.Error as erro:
            return f"Erro do banco: {erro}", True
        return json.dumps({"colunas": colunas, "linhas": linhas}, ensure_ascii=False, default=str), False
    if nome == "enviar_relatorio":
        # ação com efeito fora do sistema: só com a aprovação de uma pessoa
        if not aprovar(nome, argumentos):
            return "Envio não aprovado: aguardando a aprovação de uma pessoa.", True
        return f"Relatório enviado para {argumentos['destinatario']}.", False
    return f"Ferramenta desconhecida: {nome}", True


def rodar_agente(cliente, conexao, pergunta, aprovar=lambda nome, argumentos: False, max_passos=6, modelo="claude-opus-5-5"):
    mensagens = [{"role": "user", "content": pergunta}]
    passos = []
    for _ in range(max_passos):
        resposta = cliente.messages.create(model=modelo, max_tokens=4096, tools=definir_ferramentas(), messages=mensagens)
        if resposta.stop_reason != "tool_use":
            texto = "".join(bloco.text for bloco in resposta.content if bloco.type == "text")
            return {"resposta": texto, "passos": passos, "parou_por": "fim"}
        mensagens.append({"role": "assistant", "content": resposta.content})
        resultados = []
        for bloco in resposta.content:
            if bloco.type != "tool_use":
                continue
            conteudo, erro = executar_ferramenta(bloco.name, bloco.input, conexao, aprovar)
            passos.append({"ferramenta": bloco.name, "argumentos": bloco.input, "erro": erro})
            resultados.append({"type": "tool_result", "tool_use_id": bloco.id, "content": conteudo, "is_error": erro})
        # todos os resultados voltam juntos, numa mensagem só do usuário
        mensagens.append({"role": "user", "content": resultados})
    return {"resposta": None, "passos": passos, "parou_por": "limite"}

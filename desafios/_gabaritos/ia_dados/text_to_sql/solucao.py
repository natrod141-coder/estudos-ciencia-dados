"""Gabarito do desafio "Perguntas em português, respostas em SQL".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
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
    tabelas = [linha[0] for linha in conexao.execute(
        "select table_name from information_schema.tables where table_schema = 'main' order by table_name"
    ).fetchall()]
    linhas = []
    for tabela in tabelas:
        colunas = conexao.execute(
            "select column_name, data_type from information_schema.columns "
            "where table_name = ? order by ordinal_position", [tabela]
        ).fetchall()
        linhas.append(f"Tabela {tabela}: " + ", ".join(f"{nome} ({tipo})" for nome, tipo in colunas))
        for nome, tipo in colunas:
            if tipo != "VARCHAR":
                continue
            valores = [v[0] for v in conexao.execute(f'select distinct "{nome}" from {tabela} order by 1').fetchall()]
            # só vale listar quando são poucos: é o que evita 'Mochilas' no lugar de 'mochilas'
            if len(valores) <= max_valores:
                linhas.append(f"  Valores de {nome}: " + ", ".join(valores))
    return "\n".join(linhas)


def montar_mensagens(pergunta, esquema, regras=REGRAS):
    system = (
        "Você escreve consultas SQL para o DuckDB a partir de perguntas em português.\n"
        "Use só as tabelas e colunas do esquema abaixo, e os valores exatamente como aparecem.\n"
        "Responda com uma única consulta SELECT, dentro de um bloco ```sql.\n"
        "Se a pergunta pedir para alterar ou apagar dados, responda: Não posso alterar dados.\n\n"
        f"<esquema>\n{esquema}\n</esquema>\n\n"
        "<regras>\n" + "\n".join(f"- {regra}" for regra in regras) + "\n</regras>"
    )
    return system, [{"role": "user", "content": pergunta}]


def extrair_sql(resposta):
    cerca = re.search(r"```sql\s*(.*?)```", resposta, re.DOTALL | re.IGNORECASE)
    if cerca:
        return cerca.group(1).strip()
    texto = resposta.strip()
    return texto if re.match(r"(select|with)\b", texto, re.IGNORECASE) else None


def consulta_segura(sql):
    texto = sql.strip().rstrip(";").strip()
    if ";" in texto:
        return False, "mais de um comando"
    if not re.match(r"(select|with)\b", texto, re.IGNORECASE):
        return False, "não começa com SELECT ou WITH"
    # tira o que está entre aspas simples, para não confundir texto com comando
    sem_textos = re.sub(r"'[^']*'", "''", texto.lower())
    for palavra in PROIBIDAS:
        if re.search(rf"\b{palavra}\b", sem_textos):
            return False, f"palavra proibida: {palavra}"
    return True, ""


def executar(conexao, sql):
    return conexao.execute(sql.strip().rstrip(";")).fetchall()


def normalizar_linhas(linhas):
    def valor(v):
        return round(float(v), 2) if isinstance(v, (int, float)) and not isinstance(v, bool) else v
    return sorted(tuple(valor(v) for v in linha) for linha in linhas)


def mesmo_resultado(linhas_a, linhas_b):
    return normalizar_linhas(linhas_a) == normalizar_linhas(linhas_b)


def avaliar(cliente, conexao, perguntas, modelo="claude-opus-5-5"):
    esquema = descrever_esquema(conexao)
    relatorio = {"corretas": [], "erradas": [], "com_erro": [], "inseguras": [], "sem_sql": []}
    for item in perguntas:
        system, messages = montar_mensagens(item["pergunta"], esquema)
        resposta = cliente.messages.create(model=modelo, max_tokens=2048, system=system, messages=messages)
        texto = "".join(b.text for b in resposta.content if b.type == "text")
        sql = extrair_sql(texto)
        if sql is None:
            relatorio["sem_sql"].append(item["id"])
            continue
        segura, _ = consulta_segura(sql)
        if not segura:
            relatorio["inseguras"].append(item["id"])
            continue
        try:
            linhas = executar(conexao, sql)
        except duckdb.Error:
            relatorio["com_erro"].append(item["id"])
            continue
        esperado = executar(conexao, item["sql_referencia"])
        relatorio["corretas" if mesmo_resultado(linhas, esperado) else "erradas"].append(item["id"])
    return relatorio

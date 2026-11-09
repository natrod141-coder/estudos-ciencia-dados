"""Desafio: um agente de dados, com ferramentas e com limites.

Em vez de escrever um SQL e pronto, um agente decide sozinho quais passos dar: listar as tabelas,
olhar as colunas, consultar, e até enviar um relatório. Você vai escrever as ferramentas, o laço
que conversa com o modelo e os limites que tornam isso seguro: só leitura no banco, aprovação de
uma pessoa antes de qualquer ação com efeito fora do sistema e um número máximo de passos.

O modelo é o AgenteGravado, de agente_gravado.py, com a mesma cara do cliente do SDK da Anthropic.
Ele segue roteiros gravados e confere a conversa como a API de verdade: o desafio roda sem chave de
API e sem custo.

Regras:
- Use json, re e duckdb. Nenhuma função pode alterar o que recebe.
- Não altere agente_gravado.py, a pasta tests nem os arquivos em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
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


def definir_ferramentas():
    """A lista de ferramentas do agente, no formato da API: cada uma com "name", "description",
    "strict": True e "input_schema".

    As quatro ferramentas, nesta ordem:
    - listar_tabelas: sem parâmetros;
    - descrever_tabela: parâmetro tabela (string);
    - consultar_sql: parâmetro sql (string);
    - enviar_relatorio: parâmetros destinatario e texto (strings).
    Cada input_schema é {"type": "object", "properties": {...}, "required": [...],
    "additionalProperties": False}, com todos os parâmetros obrigatórios. A descrição é o que o
    modelo lê para decidir quando usar a ferramenta: escreva frases completas. A de
    enviar_relatorio deve dizer que o envio depende da aprovação de uma pessoa.
    """
    raise NotImplementedError("Implemente a função definir_ferramentas")


def executar_ferramenta(nome, argumentos, conexao, aprovar):
    """Executa uma ferramenta pedida pelo modelo e devolve (conteudo, erro): o texto do resultado
    e True se a ferramenta falhou ou foi recusada.

    - listar_tabelas: os nomes das tabelas do esquema main, em ordem alfabética, separados por
      ", ".
    - descrever_tabela: "coluna (TIPO), coluna (TIPO), ...", na ordem da tabela. Se a tabela não
      estiver na lista de tabelas, erro.
    - consultar_sql: se e_somente_leitura recusar o SQL, erro, com um texto que comece por
      "Consulta bloqueada". Senão, execute e devolva json.dumps({"colunas": [...], "linhas": [...]},
      ensure_ascii=False, default=str), com no máximo LIMITE_DE_LINHAS linhas. Erro do banco
      (duckdb.Error) também é erro.
    - enviar_relatorio: chame aprovar(nome, argumentos). Se devolver True, o envio acontece e o
      texto diz para quem foi. Se não, erro, com um texto que diga que o envio aguarda aprovação.
    - Qualquer outro nome: erro.
    """
    raise NotImplementedError("Implemente a função executar_ferramenta")


def rodar_agente(cliente, conexao, pergunta, aprovar=lambda nome, argumentos: False, max_passos=6, modelo="claude-opus-5-5"):
    """O laço do agente. Devolve {"resposta": texto ou None, "passos": [...], "parou_por": ...}.

    Comece com messages = [{"role": "user", "content": pergunta}]. A cada passo, chame
    cliente.messages.create(model=modelo, max_tokens=4096, tools=definir_ferramentas(),
    messages=messages).
    - Se stop_reason não for "tool_use", o agente terminou: devolva o texto dos blocos "text" como
      resposta, com parou_por "fim".
    - Se for "tool_use": acrescente a resposta inteira como mensagem do assistente
      ({"role": "assistant", "content": resposta.content}), execute cada bloco tool_use e
      acrescente UMA mensagem do usuário com todos os resultados, cada um no formato
      {"type": "tool_result", "tool_use_id": bloco.id, "content": conteudo, "is_error": erro}.
      Anote cada execução em passos: {"ferramenta": nome, "argumentos": entrada, "erro": erro}.
    Se chegar a max_passos chamadas ao modelo sem terminar, pare: resposta None, parou_por
    "limite".
    """
    raise NotImplementedError("Implemente a função rodar_agente")

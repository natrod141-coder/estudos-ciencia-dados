"""Extra, para depois do desafio: as mesmas ferramentas, expostas como um servidor MCP.

Os testes não usam este arquivo. Para experimentar, com o desafio resolvido, instale o SDK do MCP
e rode o servidor, dentro desta pasta:
    pip install mcp
    python servidor_mcp.py

Um cliente MCP, como o Claude Code ou o Claude Desktop, configurado para iniciar este comando,
passa a enxergar as ferramentas. Repare que enviar_relatorio ficou de fora: uma ação com efeito
fora do sistema só deve ser exposta com uma confirmação humana no meio do caminho.

Este exemplo usa a versão 2 do SDK, em que a classe se chama MCPServer. Exemplos antigos usam o
nome FastMCP, importado de mcp.server.fastmcp.
"""

from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

from solucao import abrir_somente_leitura, criar_banco, executar_ferramenta

BANCO = Path(__file__).parent / "loja.duckdb"
if not BANCO.exists():
    criar_banco(BANCO)
conexao = abrir_somente_leitura(BANCO)

servidor = MCPServer("dados-da-loja", instructions="Consultas só de leitura ao banco de vendas da loja.")


def resultado(nome, argumentos):
    conteudo, erro = executar_ferramenta(nome, argumentos, conexao, aprovar=lambda nome, argumentos: False)
    if erro:
        # ToolError chega ao cliente como erro da ferramenta, com o motivo; outras exceções
        # chegam sem o motivo, que fica só no registro do servidor
        raise ToolError(conteudo)
    return conteudo


@servidor.tool()
def listar_tabelas() -> str:
    """Lista as tabelas do banco de vendas que podem ser consultadas."""
    return resultado("listar_tabelas", {})


@servidor.tool()
def descrever_tabela(tabela: str) -> str:
    """Mostra as colunas e os tipos de uma tabela do banco de vendas."""
    return resultado("descrever_tabela", {"tabela": tabela})


@servidor.tool()
def consultar_sql(sql: str) -> str:
    """Executa uma única consulta SELECT, só de leitura, e devolve até 50 linhas."""
    return resultado("consultar_sql", {"sql": sql})


if __name__ == "__main__":
    servidor.run(transport="stdio")

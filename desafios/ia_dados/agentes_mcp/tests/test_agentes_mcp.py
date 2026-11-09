import json

import pytest

from agente_gravado import PERGUNTAS, AgenteGravado
from solucao import (
    LIMITE_DE_LINHAS,
    abrir_somente_leitura,
    criar_banco,
    definir_ferramentas,
    executar_ferramenta,
    rodar_agente,
)


def banco(pasta):
    return abrir_somente_leitura(criar_banco(pasta / "loja.duckdb"))


def nunca(nome, argumentos):
    return False


class Aprovador:
    """Faz o papel da pessoa que aprova: anota os pedidos e responde sempre o mesmo."""

    def __init__(self, resposta):
        self.resposta, self.pedidos = resposta, []

    def __call__(self, nome, argumentos):
        self.pedidos.append((nome, argumentos))
        return self.resposta


def test_definir_ferramentas():
    ferramentas = definir_ferramentas()
    assert [f["name"] for f in ferramentas] == ["listar_tabelas", "descrever_tabela", "consultar_sql", "enviar_relatorio"]
    for ferramenta in ferramentas:
        assert len(ferramenta["description"]) > 20, "A descrição é o que o modelo lê: escreva frases completas."
        assert ferramenta["strict"] is True
        esquema = ferramenta["input_schema"]
        assert esquema["type"] == "object" and esquema["additionalProperties"] is False
        assert sorted(esquema["required"]) == sorted(esquema["properties"])
    assert set(ferramentas[3]["input_schema"]["properties"]) == {"destinatario", "texto"}
    assert "aprova" in ferramentas[3]["description"].lower()


def test_listar_e_descrever(tmp_path):
    conexao = banco(tmp_path)
    assert executar_ferramenta("listar_tabelas", {}, conexao, nunca) == ("lojas, produtos, vendas", False)
    assert executar_ferramenta("descrever_tabela", {"tabela": "lojas"}, conexao, nunca) == (
        "loja_id (BIGINT), cidade (VARCHAR), regiao (VARCHAR)", False,
    )


def test_descrever_so_aceita_tabelas_que_existem(tmp_path):
    conexao = banco(tmp_path)
    for nome in ("clientes", "vendas; DROP TABLE vendas"):
        conteudo, erro = executar_ferramenta("descrever_tabela", {"tabela": nome}, conexao, nunca)
        assert erro is True, f"O nome da tabela vem do modelo: '{nome}' não pode passar."


def test_consultar_sql(tmp_path):
    conexao = banco(tmp_path)
    conteudo, erro = executar_ferramenta("consultar_sql", {"sql": "SELECT regiao FROM lojas WHERE loja_id = 3"}, conexao, nunca)
    assert erro is False
    assert json.loads(conteudo) == {"colunas": ["regiao"], "linhas": [["Sul"]]}
    conteudo, erro = executar_ferramenta("consultar_sql", {"sql": "SELECT * FROM vendas"}, conexao, nunca)
    assert len(json.loads(conteudo)["linhas"]) == LIMITE_DE_LINHAS, "No máximo 50 linhas voltam para o modelo."


def test_consultar_sql_bloqueia_e_avisa(tmp_path):
    conexao = banco(tmp_path)
    conteudo, erro = executar_ferramenta("consultar_sql", {"sql": "DELETE FROM vendas"}, conexao, nunca)
    assert erro is True and conteudo.startswith("Consulta bloqueada")
    conteudo, erro = executar_ferramenta("consultar_sql", {"sql": "SELECT coluna_que_nao_existe FROM vendas"}, conexao, nunca)
    assert erro is True, "Erro do banco volta para o modelo como erro, para ele tentar de novo."
    assert executar_ferramenta("apagar_tudo", {}, conexao, nunca)[1] is True


def test_enviar_relatorio_depende_de_aprovacao(tmp_path):
    conexao = banco(tmp_path)
    argumentos = {"destinatario": "diretoria@empresa.com.br", "texto": "Relatório."}
    recusa = Aprovador(False)
    conteudo, erro = executar_ferramenta("enviar_relatorio", argumentos, conexao, recusa)
    assert erro is True and "aprova" in conteudo.lower()
    assert recusa.pedidos == [("enviar_relatorio", argumentos)]
    conteudo, erro = executar_ferramenta("enviar_relatorio", argumentos, conexao, Aprovador(True))
    assert erro is False and "diretoria@empresa.com.br" in conteudo


def test_agente_responde_usando_as_ferramentas(tmp_path):
    cliente = AgenteGravado()
    resultado = rodar_agente(cliente, banco(tmp_path), PERGUNTAS["receita"])
    assert resultado["parou_por"] == "fim"
    assert "R$ 7.464,60 no Sudeste" in resultado["resposta"]
    assert [p["ferramenta"] for p in resultado["passos"]] == ["listar_tabelas", "descrever_tabela", "descrever_tabela", "consultar_sql"]
    assert all(p["erro"] is False for p in resultado["passos"])
    chamada = cliente.chamadas[0]
    assert chamada["model"] and chamada["max_tokens"] and len(chamada["tools"]) == 4


def test_agente_nao_consegue_apagar_dados(tmp_path):
    conexao = banco(tmp_path)
    resultado = rodar_agente(AgenteGravado(), conexao, PERGUNTAS["apagar"])
    assert resultado["passos"][0]["ferramenta"] == "consultar_sql" and resultado["passos"][0]["erro"] is True
    assert "só de leitura" in resultado["resposta"]
    assert conexao.execute("SELECT COUNT(*) FROM vendas").fetchone() == (259,), "Nenhuma venda foi apagada."


def test_agente_espera_aprovacao_para_enviar(tmp_path):
    conexao, recusa = banco(tmp_path), Aprovador(False)
    resultado = rodar_agente(AgenteGravado(), conexao, PERGUNTAS["relatorio"], aprovar=recusa)
    assert len(recusa.pedidos) == 1, "O agente pediu o envio, e uma pessoa precisou decidir."
    assert "aguardando a aprovação" in resultado["resposta"]
    aprovado = rodar_agente(AgenteGravado(), conexao, PERGUNTAS["relatorio"], aprovar=Aprovador(True))
    assert aprovado["resposta"].startswith("Enviei para a diretoria")


def test_agente_para_no_limite_de_passos(tmp_path):
    cliente = AgenteGravado()
    resultado = rodar_agente(cliente, banco(tmp_path), PERGUNTAS["laco"], max_passos=4)
    assert resultado == {
        "resposta": None,
        "passos": [{"ferramenta": "listar_tabelas", "argumentos": {}, "erro": False}] * 4,
        "parou_por": "limite",
    }
    assert len(cliente.chamadas) == 4

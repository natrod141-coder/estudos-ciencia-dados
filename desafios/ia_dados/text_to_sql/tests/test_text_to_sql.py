import json
from pathlib import Path

import duckdb
import pytest

from modelo_gravado import ModeloGravado
from solucao import (
    REGRAS,
    abrir_somente_leitura,
    avaliar,
    consulta_segura,
    criar_banco,
    descrever_esquema,
    executar,
    extrair_sql,
    montar_mensagens,
    mesmo_resultado,
)

PERGUNTAS = json.loads((Path(__file__).parent.parent / "data" / "perguntas.json").read_text(encoding="utf-8"))


def banco(pasta):
    return abrir_somente_leitura(criar_banco(pasta / "loja.duckdb"))


def test_descrever_esquema(tmp_path):
    esquema = descrever_esquema(banco(tmp_path))
    linhas = esquema.split("\n")
    assert linhas[:3] == [
        "Tabela lojas: loja_id (BIGINT), cidade (VARCHAR), regiao (VARCHAR)",
        "  Valores de cidade: Campinas, Curitiba, Recife, Salvador, São Paulo",
        "  Valores de regiao: Nordeste, Sudeste, Sul",
    ]
    assert "  Valores de categoria: acessorios, mochilas, papelaria" in linhas
    assert "Tabela vendas: venda_id (BIGINT), data (DATE), loja_id (BIGINT), produto_id (BIGINT), quantidade (BIGINT), valor (DOUBLE), status (VARCHAR)" in linhas


def test_descrever_esquema_limita_os_valores(tmp_path):
    esquema = descrever_esquema(banco(tmp_path), max_valores=5)
    assert "Valores de categoria" in esquema
    assert "Valores de nome" not in esquema, "Os 8 nomes de produto passam do limite de 5 valores."


def test_montar_mensagens():
    system, messages = montar_mensagens("Qual a receita de março?", "Tabela vendas: valor (DOUBLE)")
    assert "<esquema>\nTabela vendas: valor (DOUBLE)\n</esquema>" in system
    assert all(regra in system for regra in REGRAS)
    assert "```sql" in system and "Não posso alterar dados." in system
    assert messages == [{"role": "user", "content": "Qual a receita de março?"}]


def test_extrair_sql():
    assert extrair_sql("```sql\nSELECT 1\n```") == "SELECT 1"
    assert extrair_sql("Aqui está:\n\n```SQL\nselect 2;\n```\nQualquer dúvida, pergunte.") == "select 2;"
    assert extrair_sql("  WITH x AS (SELECT 1) SELECT * FROM x  ") == "WITH x AS (SELECT 1) SELECT * FROM x"
    assert extrair_sql("Não posso alterar dados.") is None


def test_consulta_segura_aceita_consultas_de_leitura():
    assert consulta_segura("SELECT * FROM vendas;") == (True, "")
    assert consulta_segura("with x as (select 1) select * from x") == (True, "")
    assert consulta_segura("SELECT nome FROM produtos WHERE nome = 'drop zone'")[0] is True, (
        "Palavras dentro de textos entre aspas não são comandos."
    )
    assert consulta_segura("SELECT updated_at, offset_dias FROM t")[0] is True, "Só palavras inteiras contam."


def test_consulta_segura_recusa_comandos_perigosos():
    for sql in [
        "DELETE FROM vendas",
        "SELECT * FROM lojas; DROP TABLE lojas;",
        "WITH x AS (SELECT 1) DELETE FROM vendas",
        "select * from vendas where 1=1 or update",
        "ATTACH 'outro.db'",
    ]:
        segura, motivo = consulta_segura(sql)
        assert segura is False and motivo, sql


def test_banco_somente_leitura_e_a_segunda_barreira(tmp_path):
    conexao = banco(tmp_path)
    assert executar(conexao, "SELECT COUNT(*) FROM vendas;") == [(259,)]
    with pytest.raises(duckdb.Error):
        executar(conexao, "DELETE FROM vendas")


def test_mesmo_resultado():
    assert mesmo_resultado([("Sul", 10.004), ("Norte", 5.0)], [("Norte", 5), ("Sul", 10.0)]) is True
    assert mesmo_resultado([("Sul", 10.0)], [("Sul", 11.0)]) is False
    assert mesmo_resultado([], [("Salvador", 32)]) is False


def test_avaliar(tmp_path):
    assert avaliar(ModeloGravado(), banco(tmp_path), PERGUNTAS) == {
        "corretas": ["t1", "t2", "t6"],
        "erradas": ["t3", "t7"],
        "com_erro": ["t4"],
        "inseguras": ["t5", "t8"],
        "sem_sql": [],
    }


def test_avaliar_manda_o_esquema_para_o_modelo(tmp_path):
    cliente = ModeloGravado()
    avaliar(cliente, banco(tmp_path), PERGUNTAS[:1])
    chamada = cliente.chamadas[0]
    assert "Valores de status: aprovada, cancelada" in chamada["system"]
    assert chamada["model"] and chamada["max_tokens"] and "temperature" not in chamada

import copy
import csv
import json
from pathlib import Path

import pytest

from solucao import (
    citacao_existe,
    classificar_resposta,
    criar_banco,
    executar_consulta,
    extrair_numeros,
    relatorio,
    valores_conferem,
)

DADOS = Path(__file__).parent.parent / "data"
DOCUMENTO = (DADOS / "regras_relatorio.txt").read_text(encoding="utf-8")
RESPOSTAS = json.loads((DADOS / "respostas_modelo.json").read_text(encoding="utf-8"))
SQL_SUL = "SELECT SUM(faturamento) FROM vendas WHERE regiao = 'Sul'"


def banco():
    return criar_banco(DADOS / "vendas.csv")


def faturamento_no_csv(regiao):
    """Soma do CSV feita sem SQL, para conferir a consulta por outro caminho."""
    with open(DADOS / "vendas.csv", encoding="utf-8", newline="") as arquivo:
        return sum(float(linha["faturamento"]) for linha in csv.DictReader(arquivo) if linha["regiao"] == regiao)


def test_extrair_numeros_formato_brasileiro():
    assert extrair_numeros("Em março, a região Sul faturou R$ 182.450,00.") == [182450.0]
    assert extrair_numeros("O faturamento foi de R$ 4.180.000,00.") == [4180000.0]
    assert extrair_numeros("Cresceu 12,3% e chegou a 1.234 pedidos.") == [12.3, 1234.0]


def test_extrair_numeros_inteiros_e_texto_sem_numero():
    assert extrair_numeros("Em 4 meses, passou de cem mil reais.") == [4.0]
    assert extrair_numeros("Foram 7.") == [7.0], "O ponto final da frase não faz parte do número."
    assert extrair_numeros("Não houve vendas.") == []


def test_valores_conferem_com_tolerancia():
    assert valores_conferem(182450.0, 182450.0) is True
    assert valores_conferem(251300.0, 251316.67) is True, "Arredondar não é errar: a diferença é menor que 1%."
    assert valores_conferem(4180000.0, 4104084.05) is False, "A diferença é de 1,85%: passa da tolerância."
    assert valores_conferem(251300.0, 251316.67, tolerancia=0.00001) is False
    assert valores_conferem(0, 0) is True


def test_executar_consulta_valida():
    conexao = banco()
    valor, erro = executar_consulta(conexao, SQL_SUL)
    assert erro is None
    assert valor == pytest.approx(faturamento_no_csv("Sul"))
    assert executar_consulta(conexao, "SELECT COUNT(*) FROM vendas") == (24, None)


def test_executar_consulta_com_erro_ou_sem_linhas():
    conexao = banco()
    valor, erro = executar_consulta(conexao, "SELECT SUM(lucro) FROM vendas")
    assert valor is None
    assert "lucro" in erro, "Devolva a mensagem do banco: ela diz o que deu errado."
    sem_linhas = "SELECT faturamento FROM vendas WHERE regiao = 'Marte'"
    assert executar_consulta(conexao, sem_linhas) == (None, None)


def test_citacao_existe():
    assert citacao_existe("O valor do frete não entra no faturamento.", DOCUMENTO) is True
    trecho_em_duas_linhas = (
        "o faturamento é a soma do valor dos pedidos aprovados, já com os descontos aplicados."
    )
    assert citacao_existe(trecho_em_duas_linhas, DOCUMENTO) is True, (
        "Maiúsculas e quebras de linha não importam na comparação."
    )
    assert citacao_existe("Pedidos cancelados a qualquer momento saem do faturamento.", DOCUMENTO) is False


def test_classificar_respostas_com_sql():
    conexao = banco()
    certa = {"id": "t1", "resposta": "A região Sul faturou R$ 1.076.926,50.", "sql": SQL_SUL}
    errada = {"id": "t2", "resposta": "A região Sul faturou R$ 1.200.000,00.", "sql": SQL_SUL}
    coluna_inventada = {"id": "t3", "resposta": "O lucro foi de R$ 90.000,00.", "sql": "SELECT SUM(lucro) FROM vendas"}
    regiao_sem_dados = {
        "id": "t4",
        "resposta": "O Centro-Oeste faturou R$ 50.000,00.",
        "sql": "SELECT SUM(faturamento) FROM vendas WHERE regiao = 'Centro-Oeste'",
    }
    assert classificar_resposta(certa, conexao, DOCUMENTO) == "correta"
    assert classificar_resposta(errada, conexao, DOCUMENTO) == "valor_errado"
    assert classificar_resposta(coluna_inventada, conexao, DOCUMENTO) == "sql_invalida"
    assert classificar_resposta(regiao_sem_dados, conexao, DOCUMENTO) == "valor_errado", (
        "SUM sem nenhuma linha devolve NULL: o dado não existe, e o número da resposta foi inventado."
    )


def test_classificar_respostas_com_citacao_ou_sem_fonte():
    conexao = banco()
    real = "O valor do frete não entra no faturamento."
    inventada = "O frete entra no faturamento das vendas para o Norte."
    com_fonte = {"id": "t1", "resposta": "O frete fica de fora.", "citacoes": [real]}
    uma_inventada = {"id": "t2", "resposta": "Depende da região.", "citacoes": [real, inventada]}
    sem_fonte = {"id": "t3", "resposta": "Sim, vale para todas as regiões."}
    lista_vazia = {"id": "t4", "resposta": "Sim.", "citacoes": []}
    assert classificar_resposta(com_fonte, conexao, DOCUMENTO) == "correta"
    assert classificar_resposta(uma_inventada, conexao, DOCUMENTO) == "citacao_inventada", (
        "Uma citação inventada já basta para desconfiar da resposta inteira."
    )
    assert classificar_resposta(sem_fonte, conexao, DOCUMENTO) == "sem_fonte"
    assert classificar_resposta(lista_vazia, conexao, DOCUMENTO) == "sem_fonte"


def test_relatorio_das_respostas_gravadas():
    originais = copy.deepcopy(RESPOSTAS)
    assert relatorio(RESPOSTAS, banco(), DOCUMENTO) == {
        "correta": ["r01", "r04", "r05", "r09"],
        "valor_errado": ["r02", "r06", "r10"],
        "sql_invalida": ["r03"],
        "citacao_inventada": ["r07"],
        "sem_fonte": ["r08"],
    }
    assert RESPOSTAS == originais, "Não altere as respostas recebidas."


def test_relatorio_mostra_todas_as_categorias():
    assert relatorio(RESPOSTAS[:1], banco(), DOCUMENTO) == {
        "correta": ["r01"],
        "valor_errado": [],
        "sql_invalida": [],
        "citacao_inventada": [],
        "sem_fonte": [],
    }

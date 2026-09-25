import sqlite3
from pathlib import Path

import solucao

SCRIPT = (Path(__file__).parent.parent / "data" / "loja.sql").read_text(encoding="utf-8")


def rodar(nome):
    """Roda a consulta num banco novo e devolve (nomes das colunas, linhas)."""
    consulta = getattr(solucao, nome)
    conexao = sqlite3.connect(":memory:")
    conexao.executescript(SCRIPT)
    try:
        cursor = conexao.execute(consulta)
        colunas = [descricao[0] for descricao in cursor.description] if cursor.description else []
        linhas = [tuple(round(v, 2) if isinstance(v, float) else v for v in linha) for linha in cursor.fetchall()]
    finally:
        conexao.close()
    assert colunas, f"{nome} não devolveu nenhuma coluna. Escreva a consulta no lugar do comentário."
    return colunas, linhas


def test_consulta_1_os_cinco_produtos_mais_caros():
    colunas, linhas = rodar("CONSULTA_1")
    assert colunas == ["nome", "categoria", "preco"]
    assert linhas == [
        ("Notebook 14", "Informática", 3899.0),
        ("Cadeira ergonômica", "Móveis", 1450.0),
        ("Monitor 24", "Informática", 1099.0),
        ("Mesa de escritório", "Móveis", 890.0),
        ("Estante", "Móveis", 520.0),
    ]


def test_consulta_2_informatica_ate_500_reais():
    colunas, linhas = rodar("CONSULTA_2")
    assert colunas == ["nome", "preco"]
    assert linhas == [("Mouse sem fio", 89.9), ("Headset", 199.9), ("Webcam HD", 229.0), ("Teclado mecânico", 349.9)]


def test_consulta_3_clientes_de_sp_ou_rj_com_a():
    colunas, linhas = rodar("CONSULTA_3")
    assert colunas == ["nome", "cidade", "estado"]
    assert linhas == [("Amanda Alves", "Campinas", "SP"), ("Ana Ribeiro", "São Paulo", "SP")]


def test_consulta_4_clientes_sem_email():
    colunas, linhas = rodar("CONSULTA_4")
    assert colunas == ["nome", "estado"]
    assert linhas == [
        ("Beatriz Ribeiro", "RJ"),
        ("Elisa Costa", "BA"),
        ("Gabriela Mendes", "MG"),
        ("João Pereira", "PR"),
        ("Karina Mendes", "MG"),
        ("Paulo Costa", "RS"),
        ("Sofia Souza", "SP"),
    ], "Para achar valores vazios, use IS NULL: a comparação = NULL nunca é verdadeira."


def test_consulta_5_estados_com_clientes():
    colunas, linhas = rodar("CONSULTA_5")
    assert colunas == ["estado"]
    assert linhas == [("BA",), ("MG",), ("PE",), ("PR",), ("RJ",), ("RS",), ("SP",)]


def test_consulta_6_resumo_do_frete():
    colunas, linhas = rodar("CONSULTA_6")
    assert colunas == ["total_pedidos", "frete_total", "frete_medio"]
    assert linhas == [(220, 6513.63, 29.61)]


def test_consulta_7_pedidos_por_status():
    colunas, linhas = rodar("CONSULTA_7")
    assert colunas == ["status", "pedidos"]
    assert linhas == [("entregue", 187), ("cancelado", 22), ("em trânsito", 11)]


def test_consulta_8_estados_com_pelo_menos_5_clientes():
    colunas, linhas = rodar("CONSULTA_8")
    assert colunas == ["estado", "clientes"]
    assert linhas == [("SP", 12), ("RJ", 7), ("MG", 6), ("PR", 5)]


def test_consulta_9_pedidos_de_marco_por_canal():
    colunas, linhas = rodar("CONSULTA_9")
    assert colunas == ["canal", "pedidos"]
    assert linhas == [("site", 13), ("app", 12), ("telefone", 2)]


def test_consulta_10_produtos_ativos_por_faixa_de_preco():
    colunas, linhas = rodar("CONSULTA_10")
    assert colunas == ["faixa", "produtos"]
    assert linhas == [("intermediário", 13), ("econômico", 7), ("premium", 3)]

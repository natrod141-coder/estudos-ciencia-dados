import sqlite3
from pathlib import Path

import solucao

SCRIPT = (Path(__file__).parent.parent / "data" / "loja.sql").read_text(encoding="utf-8")

MESES = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"]
FATURAMENTO_MENSAL = [55610.20, 65624.60, 46254.88, 50504.73, 70328.09, 59277.05]


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


def test_consulta_1_pedidos_entregues_de_maior_valor():
    colunas, linhas = rodar("CONSULTA_1")
    assert colunas == ["id_pedido", "cliente", "valor_total"]
    assert linhas == [
        (1161, "Karina Mendes", 9998.50),
        (1182, "Paulo Souza", 9248.00),
        (1185, "Paulo Souza", 8694.60),
        (1167, "Gabriela Lima", 8131.20),
        (1021, "Karina Mendes", 7798.00),
    ]


def test_consulta_2_faturamento_por_categoria():
    colunas, linhas = rodar("CONSULTA_2")
    assert colunas == ["categoria", "faturamento"]
    assert linhas == [
        ("Informática", 171821.85),
        ("Móveis", 96126.00),
        ("Eletroportáteis", 51572.80),
        ("Livros", 21916.29),
        ("Papelaria", 6162.61),
    ], "O faturamento usa o preço cobrado (itens_pedido.preco_unitario) e só pedidos entregues."


def test_consulta_3_clientes_que_nunca_compraram():
    colunas, linhas = rodar("CONSULTA_3")
    assert colunas == ["nome", "estado"]
    assert linhas == [
        ("Ana Rocha", "MG"),
        ("André Freitas", "BA"),
        ("Bruno Freitas", "PR"),
        ("Diego Freitas", "SP"),
        ("Gabriela Mendes", "MG"),
        ("Rafael Freitas", "RJ"),
    ]


def test_consulta_4_pedidos_por_cliente_do_parana_inclusive_zero():
    colunas, linhas = rodar("CONSULTA_4")
    assert colunas == ["nome", "pedidos"]
    assert linhas == [
        ("Diego Pereira", 5),
        ("João Pereira", 5),
        ("Olívia Costa", 5),
        ("Gabriela Alves", 3),
        ("Bruno Freitas", 0),
    ], "Com LEFT JOIN, conte uma coluna de pedidos (COUNT(p.id_pedido)): COUNT(*) contaria 1 para quem não comprou."


def test_consulta_5_produtos_acima_do_preco_medio():
    colunas, linhas = rodar("CONSULTA_5")
    assert colunas == ["nome", "preco"]
    assert linhas == [
        ("Notebook 14", 3899.0),
        ("Cadeira ergonômica", 1450.0),
        ("Monitor 24", 1099.0),
        ("Mesa de escritório", 890.0),
        ("Estante", 520.0),
        ("Air fryer", 499.0),
    ]


def test_consulta_6_produtos_nunca_vendidos():
    colunas, linhas = rodar("CONSULTA_6")
    assert colunas == ["nome", "categoria"]
    assert linhas == [("Globo terrestre", "Papelaria")]


def test_consulta_7_clientes_com_ticket_acima_da_media():
    colunas, linhas = rodar("CONSULTA_7")
    assert colunas == ["nome", "pedidos", "ticket_medio"]
    assert linhas == [
        ("Paulo Souza", 6, 4512.42),
        ("Gabriela Lima", 3, 3105.40),
        ("Marina Mendes", 7, 2730.83),
        ("Carla Ribeiro", 4, 2649.68),
        ("André Barbosa", 3, 2291.50),
        ("Olívia Rocha", 7, 2145.80),
        ("Paulo Costa", 5, 2135.68),
        ("Karina Mendes", 14, 2101.34),
        ("Gabriela Alves", 3, 2055.67),
        ("Amanda Lima", 22, 2039.45),
        ("Paulo Pereira", 11, 1882.74),
    ]


def test_consulta_8_produto_mais_vendido_de_cada_categoria():
    colunas, linhas = rodar("CONSULTA_8")
    assert colunas == ["categoria", "produto", "quantidade"]
    assert linhas == [
        ("Eletroportáteis", "Air fryer", 49),
        ("Informática", "Teclado mecânico", 71),
        ("Livros", "Livro: SQL Prático", 72),
        ("Móveis", "Gaveteiro", 71),
        ("Papelaria", "Organizador de mesa", 52),
    ]


def test_consulta_9_faturamento_mensal_e_acumulado():
    colunas, linhas = rodar("CONSULTA_9")
    assert colunas == ["mes", "faturamento", "acumulado"]
    assert [linha[0] for linha in linhas] == MESES
    assert [linha[1] for linha in linhas] == FATURAMENTO_MENSAL
    assert [linha[2] for linha in linhas] == [55610.20, 121234.80, 167489.68, 217994.41, 288322.50, 347599.55]


def test_consulta_10_variacao_mensal():
    colunas, linhas = rodar("CONSULTA_10")
    assert colunas == ["mes", "faturamento", "variacao_pct"]
    assert [linha[0] for linha in linhas] == MESES
    assert [linha[1] for linha in linhas] == FATURAMENTO_MENSAL
    assert [linha[2] for linha in linhas] == [None, 18.0, -29.5, 9.2, 39.3, -15.7], (
        "O primeiro mês não tem anterior: a variação dele fica NULL."
    )

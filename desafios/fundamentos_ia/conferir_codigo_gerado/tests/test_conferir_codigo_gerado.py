import copy
import math

import pandas as pd
import pytest

import codigo_da_ia
import solucao

FUNCOES = [
    "taxa_de_conversao",
    "ticket_medio_categoria",
    "limpar_valor",
    "variacao_percentual",
    "vendas_do_mes",
    "clientes_sem_pedido",
]


def resultados_diferentes(a, b):
    if a is None or b is None:
        return (a is None) != (b is None)
    if isinstance(a, float) and isinstance(b, float):
        if math.isnan(a) and math.isnan(b):
            return False
        return not math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)
    return a != b


def test_taxa_de_conversao():
    diario = pd.DataFrame({"visitas": [100, 1000, 400], "pedidos": [10, 20, 8]})
    assert solucao.taxa_de_conversao(diario) == pytest.approx(38 / 1500), (
        "A taxa do período é o total de pedidos dividido pelo total de visitas."
    )


def test_ticket_medio_categoria():
    pedidos = pd.DataFrame({"pedido_id": [1, 2, 3], "valor_pedido": [100.0, 300.0, 50.0]})
    itens = pd.DataFrame(
        {
            "pedido_id": [1, 1, 2, 3],
            "produto": ["romance", "poesia", "conto", "caneca"],
            "categoria": ["livros", "livros", "livros", "casa"],
        }
    )
    assert solucao.ticket_medio_categoria(pedidos, itens, "livros") == pytest.approx(200.0), (
        "O pedido 1 tem dois livros, mas é um pedido só: entra uma vez na média."
    )
    assert solucao.ticket_medio_categoria(pedidos, itens, "casa") == pytest.approx(50.0)
    assert list(pedidos.columns) == ["pedido_id", "valor_pedido"], "Não altere o DataFrame recebido."


def test_limpar_valor():
    assert solucao.limpar_valor("R$ 59,90") == pytest.approx(59.9)
    assert solucao.limpar_valor("R$ 1.234,56") == pytest.approx(1234.56)
    assert solucao.limpar_valor("R$ 12.500,00") == pytest.approx(12500.0)


def test_variacao_percentual():
    assert solucao.variacao_percentual(110, 100) == pytest.approx(10.0)
    assert solucao.variacao_percentual(90, 100) == pytest.approx(-10.0)
    assert solucao.variacao_percentual(50, 0) is None, "A partir de zero, não existe variação percentual."


def test_vendas_do_mes():
    vendas = pd.DataFrame(
        {
            "data": pd.to_datetime(
                ["2026-02-28 23:50", "2026-03-01 00:00", "2026-03-15 10:30", "2026-03-31 18:45", "2026-04-01 00:00"]
            ),
            "valor": [10.0, 20.0, 30.0, 40.0, 50.0],
        }
    )
    assert solucao.vendas_do_mes(vendas, 2026, 3) == pytest.approx(90.0), (
        "A venda de 31/03 às 18:45 também é de março."
    )
    assert solucao.vendas_do_mes(vendas, 2026, 2) == pytest.approx(10.0)


def test_clientes_sem_pedido():
    clientes = pd.DataFrame({"cliente_id": [1, 2, 3, 4], "nome": ["Bruno", "Ana", "Carla", "Davi"]})
    pedidos = pd.DataFrame({"pedido_id": [10, 11, 12], "cliente_id": [2, None, 3]})
    assert solucao.clientes_sem_pedido(clientes, pedidos) == ["Bruno", "Davi"], (
        "O pedido 11 foi feito sem cadastro. Confira o que a consulta faz com o cliente_id vazio."
    )


@pytest.mark.parametrize("nome", FUNCOES)
def test_contraexemplo_mostra_o_erro_da_ia(nome):
    assert nome in solucao.CONTRAEXEMPLOS, f'Registre em CONTRAEXEMPLOS um caso em que "{nome}" da IA erra.'
    argumentos = solucao.CONTRAEXEMPLOS[nome]
    try:
        corrigida = getattr(solucao, nome)(**copy.deepcopy(argumentos))
    except Exception as erro:
        pytest.fail(f"A sua versão de {nome} levantou {erro!r} com o contraexemplo. Ela precisa funcionar nesse caso.")
    try:
        da_ia = getattr(codigo_da_ia, nome)(**copy.deepcopy(argumentos))
    except Exception:
        return  # a versão da IA quebra com este caso: o contraexemplo mostra o erro
    assert resultados_diferentes(da_ia, corrigida), (
        f"Com esses argumentos, a versão da IA e a sua dão o mesmo resultado ({da_ia!r}). "
        "Procure um caso em que a versão da IA erra."
    )

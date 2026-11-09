from pathlib import Path

import pandas as pd
import pytest

from solucao import compilar, consultar, criar_banco, expressao_de_tempo, ler_modelo, sql_da_medida, sql_da_metrica

PASTA = Path(__file__).parent.parent
MODELO = ler_modelo(PASTA / "modelo_semantico.json")
PEDIDOS = pd.read_csv(PASTA / "data" / "pedidos.csv", parse_dates=["data_pedido"])
APROVADOS = PEDIDOS[PEDIDOS["status"] == "aprovado"]


def banco():
    return criar_banco(PASTA / "data" / "pedidos.csv")


def valor(sql):
    """Roda uma consulta e devolve o primeiro valor da primeira linha."""
    return banco().execute(sql).fetchone()[0]


def datas(serie):
    return pd.to_datetime(serie).dt.strftime("%Y-%m-%d").tolist()


def test_sql_da_medida():
    medidas = MODELO["medidas"]
    assert valor(f"select {sql_da_medida(medidas['valor_vendido'])} from pedidos") == pytest.approx(PEDIDOS["valor"].sum())
    assert valor(f"select {sql_da_medida(medidas['quantidade_pedidos'])} from pedidos") == len(PEDIDOS)
    assert valor(f"select {sql_da_medida(medidas['clientes_distintos'])} from pedidos") == PEDIDOS["cliente_id"].nunique()
    with pytest.raises(ValueError):
        sql_da_medida({"agregacao": "mediana", "coluna": "valor"})


def test_expressao_de_tempo():
    def truncar(grao):
        return str(valor(f"select {expressao_de_tempo('d', grao)} from (select DATE '2026-03-18' as d)"))[:10]

    assert truncar("mes") == "2026-03-01"
    assert truncar("trimestre") == "2026-01-01"
    assert truncar("semana") == "2026-03-16", "A semana começa na segunda-feira."
    assert truncar("dia") == "2026-03-18"
    assert truncar("ano") == "2026-01-01"
    with pytest.raises(ValueError):
        expressao_de_tempo("d", "hora")


def test_metricas_simples_com_filtro():
    assert valor(f"select {sql_da_metrica(MODELO, 'receita')} from pedidos") == pytest.approx(APROVADOS["valor"].sum()), (
        "A receita só conta os pedidos aprovados: use o filtro da métrica."
    )
    assert valor(f"select {sql_da_metrica(MODELO, 'pedidos')} from pedidos") == len(PEDIDOS)
    assert valor(f"select {sql_da_metrica(MODELO, 'clientes_compradores')} from pedidos") == APROVADOS["cliente_id"].nunique()
    with pytest.raises(ValueError):
        sql_da_metrica(MODELO, "lucro")


def test_metricas_de_razao():
    ticket = APROVADOS["valor"].sum() / len(APROVADOS)
    assert valor(f"select {sql_da_metrica(MODELO, 'ticket_medio')} from pedidos") == pytest.approx(ticket)
    taxa = (PEDIDOS["status"] == "cancelado").mean()
    assert valor(f"select {sql_da_metrica(MODELO, 'taxa_cancelamento')} from pedidos") == pytest.approx(taxa)


def test_compilar_total_sem_agrupamento():
    df = consultar(banco(), MODELO, ["receita", "pedidos"])
    assert list(df.columns) == ["receita", "pedidos"]
    assert len(df) == 1
    assert df.loc[0, "receita"] == pytest.approx(APROVADOS["valor"].sum())
    assert df.loc[0, "pedidos"] == len(PEDIDOS)


def test_compilar_por_dimensao():
    df = consultar(banco(), MODELO, ["receita", "pedidos_aprovados"], por=["regiao"])
    esperado = APROVADOS.groupby("regiao")["valor"].agg(["sum", "count"])
    assert list(df.columns) == ["regiao", "receita", "pedidos_aprovados"]
    assert df["regiao"].tolist() == esperado.index.tolist(), "Ordene pelas colunas de agrupamento."
    assert df["receita"].tolist() == pytest.approx(esperado["sum"].tolist())
    assert df["pedidos_aprovados"].tolist() == esperado["count"].tolist()
    assert df["receita"].sum() == pytest.approx(APROVADOS["valor"].sum()), "A receita é aditiva: as regiões somam o total."


def test_compilar_por_mes():
    df = consultar(banco(), MODELO, ["receita", "pedidos"], grao="mes")
    assert list(df.columns) == ["mes", "receita", "pedidos"], "A coluna de tempo vem primeiro e se chama como o grão."
    assert datas(df["mes"]) == ["2026-01-01", "2026-02-01", "2026-03-01"]
    receita = APROVADOS.groupby(APROVADOS["data_pedido"].dt.to_period("M"))["valor"].sum()
    pedidos = PEDIDOS.groupby(PEDIDOS["data_pedido"].dt.to_period("M")).size()
    assert df["receita"].tolist() == pytest.approx(receita.tolist())
    assert df["pedidos"].tolist() == pedidos.tolist()


def test_razao_usa_os_totais_do_grupo():
    por_regiao = consultar(banco(), MODELO, ["taxa_cancelamento"], por=["regiao"])
    esperado = PEDIDOS.groupby("regiao")["status"].apply(lambda status: (status == "cancelado").mean())
    assert por_regiao["taxa_cancelamento"].tolist() == pytest.approx(esperado.tolist())
    total = consultar(banco(), MODELO, ["taxa_cancelamento"]).loc[0, "taxa_cancelamento"]
    assert total == pytest.approx((PEDIDOS["status"] == "cancelado").mean())
    assert total != pytest.approx(por_regiao["taxa_cancelamento"].mean()), (
        "A taxa total é cancelados sobre o total de pedidos, e não a média das taxas das regiões."
    )


def test_grao_dimensao_e_filtros_juntos():
    filtros = ["regiao = 'Sudeste'", "valor > 100"]
    df = consultar(banco(), MODELO, ["ticket_medio"], por=["canal"], grao="trimestre", filtros=filtros)
    assert list(df.columns) == ["trimestre", "canal", "ticket_medio"]
    selecao = PEDIDOS[(PEDIDOS["regiao"] == "Sudeste") & (PEDIDOS["valor"] > 100)]
    esperado = selecao.groupby("canal").apply(
        lambda grupo: grupo.loc[grupo["status"] == "aprovado", "valor"].mean(), include_groups=False
    )
    assert datas(df["trimestre"]) == ["2026-01-01"] * len(esperado)
    assert df["canal"].tolist() == esperado.index.tolist()
    assert df["ticket_medio"].tolist() == pytest.approx(esperado.tolist())


def test_pedidos_invalidos_levantam_erro():
    with pytest.raises(ValueError):
        compilar(MODELO, ["lucro"])
    with pytest.raises(ValueError):
        compilar(MODELO, ["receita"], por=["cidade"])
    with pytest.raises(ValueError):
        compilar(MODELO, ["receita"], grao="hora")
    with pytest.raises(ValueError):
        compilar(MODELO, [])

"""Confere o projeto dbt da loja.

Os testes carregam os dados brutos num banco temporário, rodam dbt build uma vez só e
examinam as tabelas criadas e o manifesto que o dbt gera.
"""

import atexit
import functools
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import duckdb
import pytest

from carregar_dados import carregar

PASTA = Path(__file__).resolve().parent.parent
MODELOS = ["stg_pedidos", "stg_itens", "fct_pedidos", "dim_clientes"]

# pedido_id, status, regiao, unidades, valor_total
ESPERADO_FCT = [
    (101, "aprovado", "Sudeste", 7, 67.30),
    (102, "aprovado", "Sudeste", 1, 189.90),
    (103, "aprovado", "Sudeste", 1, 24.90),
    (104, "cancelado", "Nordeste", 2, 90.00),
    (106, "pendente", "Sul", 0, 0.00),
    (107, "aprovado", "Nordeste", 8, 98.00),
    (108, "cancelado", "Norte", 1, 189.90),
    (109, "aprovado", "Nordeste", 2, 65.80),
    (110, "aprovado", "Sudeste", 4, 134.60),
    (112, "aprovado", "Sul", 12, 414.80),
]

# cliente_id, nome, uf, regiao, primeiro_pedido, pedidos_aprovados, valor_aprovado
ESPERADO_DIM = [
    (1, "Ana Souza", "SP", "Sudeste", "2026-03-02", 2, 92.20),
    (2, "Bruno Lima", "RJ", "Sudeste", "2026-03-03", 2, 324.50),
    (3, "Carla Mendes", "BA", "Nordeste", "2026-03-20", 1, 65.80),
    (4, "Diego Rocha", "RS", "Sul", "2026-03-31", 1, 414.80),
    (5, "Elisa Prado", "PE", "Nordeste", "2026-03-12", 1, 98.00),
    (6, "Fábio Nunes", "AM", "Norte", None, 0, 0.00),
    (7, "Gabriela Costa", "MG", "Sudeste", None, 0, 0.00),
]

TESTES_PEDIDOS = {
    ("fct_pedidos", "pedido_id", "unique"),
    ("fct_pedidos", "pedido_id", "not_null"),
    ("fct_pedidos", "cliente_id", "relationships"),
    ("fct_pedidos", "status", "accepted_values"),
    ("dim_clientes", "cliente_id", "unique"),
    ("dim_clientes", "cliente_id", "not_null"),
}


def executavel_dbt():
    """O dbt instalado junto com o Python que roda os testes, ou o primeiro do PATH."""
    pasta_python = Path(sys.executable).parent
    for candidato in (pasta_python / "dbt", pasta_python / "dbt.exe", pasta_python / "Scripts" / "dbt.exe"):
        if candidato.exists():
            return str(candidato)
    encontrado = shutil.which("dbt")
    assert encontrado, "O dbt não está instalado. Rode: pip install -r desafios/requirements.txt"
    return encontrado


@functools.lru_cache(maxsize=None)
def construir():
    """Carrega os dados brutos e roda dbt build uma vez só. Devolve a pasta com o banco e os artefatos."""
    saida = Path(tempfile.mkdtemp(prefix="dbt_loja_"))
    atexit.register(shutil.rmtree, saida, ignore_errors=True)
    banco = saida / "loja.duckdb"
    carregar(banco)
    ambiente = dict(os.environ, LOJA_DUCKDB=str(banco), DBT_SEND_ANONYMOUS_USAGE_STATS="false")
    comando = [
        executavel_dbt(), "build",
        "--project-dir", str(PASTA),
        "--profiles-dir", str(PASTA),
        "--target-path", str(saida / "target"),
        "--log-path", str(saida / "logs"),
    ]
    subprocess.run(comando, cwd=PASTA, env=ambiente, capture_output=True)
    return saida


def artefato(nome):
    caminho = construir() / "target" / nome
    assert caminho.exists(), (
        f"O dbt não chegou a gerar o {nome}. No terminal, rode python carregar_dados.py e depois "
        "dbt build, e leia o erro."
    )
    return json.loads(caminho.read_text(encoding="utf-8"))


def status_dos_nos():
    return {resultado["unique_id"]: resultado["status"] for resultado in artefato("run_results.json")["results"]}


def consultar(sql):
    try:
        with duckdb.connect(str(construir() / "loja.duckdb"), read_only=True) as conexao:
            cursor = conexao.execute(sql)
            return [coluna[0] for coluna in cursor.description], cursor.fetchall()
    except duckdb.Error as erro:
        pytest.fail(f"Não deu para ler o resultado do dbt ({erro}). Confira se o modelo rodou no dbt build.")


def colunas(tabela):
    return consultar(f"select * from {tabela} limit 0")[0]


def test_modelos_rodam_sem_erro():
    status = status_dos_nos()
    problemas = {modelo: status.get(f"model.loja.{modelo}", "não rodou") for modelo in MODELOS}
    problemas = {modelo: situacao for modelo, situacao in problemas.items() if situacao != "success"}
    assert not problemas, f"Estes modelos não rodaram: {problemas}. Rode dbt build no terminal e leia o erro."


def test_stg_pedidos():
    assert colunas("stg_pedidos") == ["pedido_id", "cliente_id", "data_pedido", "status"]
    _, linhas = consultar(
        "select pedido_id, cast(data_pedido as varchar), typeof(data_pedido), status from stg_pedidos order by pedido_id"
    )
    assert len(linhas) == 10, "Os dois pedidos do cliente 0 são de teste e ficam de fora."
    assert {linha[3] for linha in linhas} == {"aprovado", "cancelado", "pendente"}, (
        "Padronize o status: minúsculas e sem espaços nas pontas."
    )
    assert linhas[-1][:3] == (112, "2026-03-31", "DATE"), "data_pedido é a data do pedido, do tipo date."


def test_stg_itens_em_reais():
    assert colunas("stg_itens") == ["pedido_id", "produto", "quantidade", "preco_unitario", "valor_item"]
    _, mochilas = consultar(
        "select cast(preco_unitario as double), cast(valor_item as double) from stg_itens "
        "where produto = 'Mochila' order by valor_item"
    )
    assert mochilas == [
        (pytest.approx(189.90), pytest.approx(189.90)),
        (pytest.approx(189.90), pytest.approx(189.90)),
        (pytest.approx(189.90), pytest.approx(379.80)),
    ], "preco_unitario e valor_item ficam em reais: 18990 centavos são R$ 189,90."
    _, soma = consultar("select cast(sum(valor_item) as double) from stg_itens where pedido_id = 107")
    assert soma[0][0] == pytest.approx(98.00)


def test_macro_centavos_para_reais():
    manifesto = artefato("manifest.json")
    assert "macro.loja.centavos_para_reais" in manifesto["macros"], (
        "Crie a macro centavos_para_reais em macros/centavos_para_reais.sql."
    )
    usadas = manifesto["nodes"]["model.loja.stg_itens"]["depends_on"]["macros"]
    assert "macro.loja.centavos_para_reais" in usadas, "Use a macro centavos_para_reais em stg_itens.sql."


def test_fct_pedidos_uma_linha_por_pedido():
    assert colunas("fct_pedidos") == [
        "pedido_id", "cliente_id", "data_pedido", "status", "regiao", "unidades", "valor_total"
    ]
    _, linhas = consultar("select count(*), count(distinct pedido_id) from fct_pedidos")
    assert linhas[0] == (10, 10), "Uma linha por pedido: agrupe os itens por pedido antes do join."


def test_fct_pedidos_valores_e_regiao():
    _, linhas = consultar(
        "select pedido_id, status, regiao, cast(unidades as integer), cast(valor_total as double) "
        "from fct_pedidos order by pedido_id"
    )
    esperado = [(pedido, status, regiao, unidades, pytest.approx(valor)) for pedido, status, regiao, unidades, valor in ESPERADO_FCT]
    assert linhas == esperado, (
        "Confira a região, as unidades e o valor total de cada pedido. O pedido 106 não tem itens: "
        "unidades e valor_total ficam 0, e não vazios."
    )


def test_dim_clientes():
    assert colunas("dim_clientes") == [
        "cliente_id", "nome", "uf", "regiao", "primeiro_pedido", "pedidos_aprovados", "valor_aprovado"
    ]
    _, linhas = consultar(
        "select cliente_id, nome, uf, regiao, cast(primeiro_pedido as varchar), cast(pedidos_aprovados as integer), "
        "cast(valor_aprovado as double) from dim_clientes order by cliente_id"
    )
    esperado = [(*linha[:6], pytest.approx(linha[6])) for linha in ESPERADO_DIM]
    assert linhas == esperado, (
        "Uma linha por cliente, inclusive quem nunca teve pedido aprovado (com 0 pedidos e valor 0). "
        "Só os pedidos aprovados entram nas contas."
    )


def test_modelos_usam_ref_e_source():
    nos = artefato("manifest.json")["nodes"]

    def dependencias(modelo):
        return set(nos[f"model.loja.{modelo}"]["depends_on"]["nodes"])

    assert "source.loja.loja.pedidos" in dependencias("stg_pedidos"), "Leia os pedidos com a função source."
    assert "source.loja.loja.itens_pedido" in dependencias("stg_itens"), "Leia os itens com a função source."
    faltam = {"model.loja.stg_pedidos", "model.loja.stg_itens", "model.loja.stg_clientes", "seed.loja.uf_regiao"}
    faltam -= dependencias("fct_pedidos")
    assert not faltam, f"fct_pedidos precisa ler estes nós com a função ref: {sorted(faltam)}"
    faltam = {"model.loja.fct_pedidos", "model.loja.stg_clientes", "seed.loja.uf_regiao"} - dependencias("dim_clientes")
    assert not faltam, f"dim_clientes precisa ler estes nós com a função ref: {sorted(faltam)}"


def test_testes_de_qualidade_declarados():
    declarados = {}
    for no in artefato("manifest.json")["nodes"].values():
        if no["resource_type"] == "test" and no.get("test_metadata"):
            modelo = (no.get("attached_node") or "").split(".")[-1]
            declarados[(modelo, no.get("column_name"), no["test_metadata"]["name"])] = no["test_metadata"]["kwargs"]
    faltam = TESTES_PEDIDOS - set(declarados)
    assert not faltam, f"Faltam estes testes em models/marts/_marts.yml: {sorted(faltam)}"
    valores = declarados[("fct_pedidos", "status", "accepted_values")].get("values") or []
    assert sorted(valores) == ["aprovado", "cancelado", "pendente"]


def test_testes_de_qualidade_passam():
    testes = {no: situacao for no, situacao in status_dos_nos().items() if no.startswith("test.")}
    assert len(testes) >= 7, "Declare os testes pedidos em _marts.yml. O teste singular de testes_dbt já conta um."
    falharam = sorted(no for no, situacao in testes.items() if situacao != "pass")
    assert not falharam, f"Estes testes do dbt não passaram: {falharam}"

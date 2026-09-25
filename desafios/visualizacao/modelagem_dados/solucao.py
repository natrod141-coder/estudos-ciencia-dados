"""Desafio: da planilha única ao modelo estrela.

Implemente cada função abaixo. Leia a docstring de cada uma antes de começar.

Regras:
- Use pandas. Nenhuma função pode alterar o DataFrame que recebe.
- Não altere a pasta tests nem o arquivo em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import pandas as pd

# Nomes em português para o calendário, na ordem do pandas: janeiro é o mês 1, e segunda-feira
# é o dia 0 em .dayofweek.
NOMES_MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
               "agosto", "setembro", "outubro", "novembro", "dezembro"]
NOMES_DIAS = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
              "sexta-feira", "sábado", "domingo"]


def ler_planilha(caminho_csv):
    """Já está pronta: lê a planilha única, com a coluna data como data."""
    return pd.read_csv(caminho_csv, parse_dates=["data"])


def inconsistencias(plana, chave, atributos):
    """Encontra chaves que aparecem com mais de uma combinação de atributos.

    Numa dimensão, cada chave tem uma linha só. Se o mesmo código de produto aparece com duas
    categorias diferentes, é preciso decidir qual vale antes de montar a dimensão.
    Devolve a lista de chaves com mais de uma combinação diferente dos atributos, em ordem.
    Dica: pegue as colunas [chave, *atributos], tire as linhas repetidas e conte quantas vezes
    cada chave aparece.
    """
    raise NotImplementedError("Implemente a função inconsistencias")


def criar_dim_produto(plana):
    """Cria a dimensão de produtos: uma linha por codigo_produto.

    Colunas, nesta ordem: id_produto, codigo_produto, produto, categoria, marca, custo_unitario.
    1. Para cada produto, use os atributos da venda MAIS RECENTE (a última pela data). Um produto
       recategorizado passa a aparecer só com a categoria nova, como numa dimensão do tipo 1.
       Dica: ordene por data e use .drop_duplicates(subset="codigo_produto", keep="last").
    2. Ordene por codigo_produto e crie a chave substituta id_produto: 1, 2, 3...
    """
    raise NotImplementedError("Implemente a função criar_dim_produto")


def criar_dim_loja(plana):
    """Cria a dimensão de lojas: uma linha por codigo_loja, com a mesma lógica da de produtos.

    Colunas, nesta ordem: id_loja, codigo_loja, loja, cidade, uf. A chave id_loja vai de 1 em
    diante, na ordem do codigo_loja.
    """
    raise NotImplementedError("Implemente a função criar_dim_loja")


def criar_calendario(inicio, fim):
    """Cria a dimensão de datas, com uma linha para cada dia de inicio a fim (inclusive).

    Colunas, nesta ordem:
    - data: a data (use pd.date_range(inicio, fim, freq="D"))
    - ano, mes: números
    - nome_mes: nome do mês em português, em minúsculas (use NOMES_MESES)
    - trimestre: "T1" a "T4"
    - ano_mes: texto "AAAA-MM"
    - dia_semana: nome do dia em português (use NOMES_DIAS)
    - fim_de_semana: True para sábado e domingo
    """
    raise NotImplementedError("Implemente a função criar_calendario")


def criar_fato(plana, dim_produto, dim_loja):
    """Cria a tabela fato de vendas: uma linha por item vendido, só com chaves e números.

    1. Troque codigo_produto por id_produto e codigo_loja por id_loja, buscando as chaves nas
       dimensões (merge).
    2. Calcule valor = quantidade x preco_unitario, arredondado para 2 casas.
    3. Devolva só as colunas data, pedido, id_produto, id_loja, quantidade, preco_unitario e
       valor, nesta ordem e na ordem original das linhas. Os textos descritivos ficam nas
       dimensões.
    """
    raise NotImplementedError("Implemente a função criar_fato")


def validar_relacionamento(fato, dimensao, chave):
    """Confere se um relacionamento um-para-muitos entre dimensão e fato vai funcionar.

    Devolve um dicionário com:
    - "chave_unica_na_dimensao": True se a chave não se repete na dimensão (o lado "um");
    - "linhas_orfas_na_fato": quantas linhas da fato têm uma chave que não existe na dimensão.
    """
    raise NotImplementedError("Implemente a função validar_relacionamento")


def granularidade_ok(tabela, colunas):
    """Devolve True se as colunas identificam cada linha da tabela, sem repetição.

    É o teste da granularidade: na fato de vendas, pedido + id_produto identifica cada linha.
    """
    raise NotImplementedError("Implemente a função granularidade_ok")


def montar_modelo(caminho_csv):
    """Monta o modelo estrela completo a partir da planilha.

    Devolve um dicionário com "fato_vendas", "dim_produto", "dim_loja" e "dim_data".
    O calendário cobre anos completos: de 1º de janeiro do ano da primeira venda até 31 de
    dezembro do ano da última venda.
    """
    raise NotImplementedError("Implemente a função montar_modelo")

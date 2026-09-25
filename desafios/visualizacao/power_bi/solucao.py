"""Desafio: o Power Query por dentro.

Cada função faz, em pandas, uma etapa que você faria no Power Query do Power BI.
A docstring diz qual é o botão ou a transformação equivalente.

Regras:
- Use pandas. Nenhuma função pode alterar o DataFrame que recebe.
- Não edite os arquivos em data: o relatório precisa se refazer sozinho quando chegar
  um arquivo novo, como no Power BI ao clicar em Atualizar.
- Não altere a pasta tests.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

from pathlib import Path  # noqa: F401  (será usado em combinar_arquivos e montar_relatorio)

import pandas as pd

# Para transformar o nome do mês em número, em despivotar_metas.
MESES = {"jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6,
         "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12}


def ler_arquivo_vendas(caminho_csv):
    """Lê um CSV de vendas exportado no formato brasileiro.
    No Power Query: Obter Dados > Texto/CSV e Alterar Tipo com Localidade (Português - Brasil).

    O arquivo usa ponto e vírgula entre as colunas, vírgula decimal e datas dd/mm/aaaa.
    1. pd.read_csv(caminho_csv, sep=";", decimal=",")
    2. Converta a coluna data com pd.to_datetime(..., format="%d/%m/%Y").
    """
    raise NotImplementedError("Implemente a função ler_arquivo_vendas")


def combinar_arquivos(pasta):
    """Empilha todos os arquivos vendas_*.csv da pasta.
    No Power Query: Obter Dados > Pasta > Combinar, seguido de Aparar e MAIÚSCULAS no código.

    1. Leia cada arquivo com ler_arquivo_vendas, em ordem de nome
       (sorted(Path(pasta).glob("vendas_*.csv"))).
    2. Acrescente a cada parte a coluna "arquivo", com o nome do arquivo de origem
       (arquivo.name), como a coluna Source.Name do Power Query.
    3. Junte tudo com pd.concat(..., ignore_index=True).
    4. Padronize a coluna loja: sem espaços nas pontas e em maiúsculas. No arquivo de março,
       alguns códigos vieram como " L06" ou "l02 ".
    """
    raise NotImplementedError("Implemente a função combinar_arquivos")


def despivotar_metas(caminho_csv):
    """Transforma a tabela de metas, com um mês por coluna, em uma linha por loja e mês.
    No Power Query: selecionar a coluna loja > Transformar Outras Colunas em Linhas.

    O arquivo tem as colunas loja, jan, fev, mar (formato brasileiro, como as vendas).
    Devolva as colunas loja, mes (número de 1 a 12, use MESES) e meta, ordenadas por loja e mes,
    com o índice refeito.
    Dica: .melt(id_vars="loja", var_name="mes", value_name="meta").
    """
    raise NotImplementedError("Implemente a função despivotar_metas")


def mesclar_lojas(vendas, lojas):
    """Traz o nome e a região de cada loja para as vendas.
    No Power Query: Mesclar Consultas, com junção externa esquerda.

    lojas tem as colunas codigo, nome, cidade e regiao. Acrescente às vendas as colunas
    "nome_loja" (o nome da loja) e "regiao", casando vendas.loja com lojas.codigo.
    Todas as vendas continuam, na mesma ordem.
    """
    raise NotImplementedError("Implemente a função mesclar_lojas")


def adicionar_faixa(vendas):
    """Acrescenta a coluna "faixa" conforme o valor da venda.
    No Power Query: Adicionar Coluna > Coluna Condicional.

    - valor menor que 200: "pequena"
    - valor de 200 até menos de 1000: "média"
    - valor de 1000 em diante: "grande"
    """
    raise NotImplementedError("Implemente a função adicionar_faixa")


def agrupar_por_loja_e_mes(vendas):
    """Resume as vendas por loja e mês.
    No Power Query: Agrupar Por, com duas agregações.

    Devolve um DataFrame com as colunas loja, mes (o número do mês da data), faturamento
    (soma do valor, arredondada para 2 casas) e vendas (quantidade de linhas), uma linha
    por loja e mês.
    """
    raise NotImplementedError("Implemente a função agrupar_por_loja_e_mes")


def realizado_vs_meta(agrupado, metas):
    """Compara o faturamento de cada loja e mês com a meta.

    Recebe o resultado de agrupar_por_loja_e_mes e de despivotar_metas. Junte os dois por
    loja e mes e acrescente:
    - "atingimento_pct": faturamento ÷ meta x 100, arredondado para 1 casa;
    - "bateu_meta": True se o faturamento for maior ou igual à meta.
    """
    raise NotImplementedError("Implemente a função realizado_vs_meta")


def cartoes(realizado):
    """Calcula os números dos cartões do topo do relatório.

    Devolve um dicionário com:
    - "faturamento_total": soma do faturamento, arredondada para 2 casas;
    - "meta_total": soma das metas, arredondada para 2 casas;
    - "atingimento_pct": faturamento total ÷ meta total x 100, arredondado para 1 casa;
    - "metas_batidas": quantas combinações de loja e mês bateram a meta (um int).
    Atenção: o atingimento total não é a média dos atingimentos de cada linha.
    """
    raise NotImplementedError("Implemente a função cartoes")


def montar_relatorio(pasta_dados):
    """Junta todas as etapas, como o Power BI faz ao clicar em Atualizar.

    1. Leia lojas.csv (sep=";") e combine os arquivos da subpasta "vendas".
    2. Nas vendas: mesclar_lojas e depois adicionar_faixa.
    3. Agrupe, compare com as metas de metas.csv e calcule os cartões.
    Devolve {"vendas": ..., "realizado": ..., "cartoes": ...}.
    """
    raise NotImplementedError("Implemente a função montar_relatorio")

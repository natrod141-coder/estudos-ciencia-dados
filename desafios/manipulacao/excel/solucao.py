"""Desafio: da planilha bagunçada ao relatório.

Implemente cada função abaixo. Leia a docstring de cada uma antes de começar.
Cada função faz em Python o que você faria no Excel: a docstring diz qual é o equivalente.

Regras:
- Use pandas para ler, limpar e resumir, e deixe o pandas gravar o .xlsx (ele usa o openpyxl).
- Não edite a planilha de entrada à mão: o relatório precisa sair igual toda vez que rodar.
- Não altere a pasta tests.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

from numbers import Number  # noqa: F401  (será usado em texto_para_numero)

import pandas as pd


def ler_produtos(caminho_xlsx):
    """Já está pronta: lê a aba Produtos, que já vem limpa."""
    return pd.read_excel(caminho_xlsx, sheet_name="Produtos")


def ler_vendas(caminho_xlsx):
    """Lê a aba Vendas e devolve só as linhas de venda, como DataFrame.

    Abra a planilha no Excel ou no LibreOffice antes: as três primeiras linhas são título,
    subtítulo e uma linha vazia, e o cabeçalho de verdade está na linha 4. No fim há uma linha
    "Total" que não é venda.

    Passo a passo:
    1. pd.read_excel(caminho_xlsx, sheet_name="Vendas", skiprows=3)
    2. Tire a linha em que a coluna Data vale "Total" e linhas totalmente vazias (.dropna(how="all")).
    3. A coluna Quantidade vem como float por causa da linha Total: converta para int (.astype(int)).
    4. Refaça o índice com .reset_index(drop=True).
    """
    raise NotImplementedError("Implemente a função ler_vendas")


def texto_para_numero(valor):
    """Converte um valor em reais para float. Equivale a SUBSTITUIR + VALOR no Excel.

    - Se o valor já for um número (isinstance(valor, Number)), devolva float(valor).
    - Se for texto, como "R$ 1.234,56": tire o "R$" e os espaços, tire o ponto dos milhares e
      troque a vírgula decimal por ponto, e converta com float(). Resultado: 1234.56.

    Um texto que não é número, como "ver sistema", deve levantar ValueError (o float() já faz isso).
    """
    raise NotImplementedError("Implemente a função texto_para_numero")


def limpar_vendas(vendas):
    """Devolve uma cópia limpa das vendas, sem alterar o DataFrame recebido.

    1. Vendedor: tire os espaços do começo, do fim e os repetidos no meio, e deixe cada nome com
       a primeira letra maiúscula. É o ARRUMAR com o PRI.MAIÚSCULA do Excel.
       Dica: .str.split().str.join(" ").str.title()
    2. Data: converta o texto "dd/mm/aaaa" para data com pd.to_datetime(..., format="%d/%m/%Y").
    3. Valor total: aplique texto_para_numero em cada valor (.map).
    4. Remova as linhas duplicadas (.drop_duplicates()) e refaça o índice.
    """
    raise NotImplementedError("Implemente a função limpar_vendas")


def procx(vendas, produtos):
    """Traz o nome e a categoria de cada produto para as vendas. Equivale a
    =PROCX([@Código]; Produtos[Código]; Produtos[Produto]; "Não encontrado") no Excel.

    Devolve as vendas com duas colunas a mais, "Produto" e "Categoria", na mesma ordem e com a
    mesma quantidade de linhas. Código que não existe no cadastro fica com "Não encontrado"
    nas duas colunas.
    Dicas: vendas.merge(..., on="Código", how="left") e .fillna("Não encontrado").
    """
    raise NotImplementedError("Implemente a função procx")


def somases(vendas, vendedor, mes):
    """Soma o Valor total das vendas de um vendedor num mês (1 a 12). Equivale a
    =SOMASES(Vendas[Valor total]; Vendas[Vendedor]; "Ana Souza"; Vendas[Mês]; 2) no Excel.

    Recebe as vendas já limpas. Devolve a soma como float, arredondada para 2 casas
    (0.0 se não houver venda).
    Dica: vendas["Data"].dt.month dá o mês de cada venda.
    """
    raise NotImplementedError("Implemente a função somases")


def tabela_dinamica(vendas):
    """Monta a tabela dinâmica do faturamento: vendedores nas linhas, categorias nas colunas.

    Recebe as vendas devolvidas por procx. Os valores são a soma de Valor total. Célula sem
    venda vale 0, e há uma linha e uma coluna "Total", como os totais gerais do Excel.
    Arredonde para 2 casas.
    Dica: pd.pivot_table(..., aggfunc="sum", fill_value=0, margins=True, margins_name="Total").
    """
    raise NotImplementedError("Implemente a função tabela_dinamica")


def exportar_relatorio(caminho_entrada, caminho_saida):
    """Gera o relatório final em Excel, a partir da planilha de entrada.

    1. Leia, limpe e complete as vendas: ler_vendas, limpar_vendas e procx (com ler_produtos).
    2. Grave um .xlsx com duas abas, nesta ordem:
       - "Dados": as vendas completas, sem a coluna de índice, com a linha do cabeçalho
         congelada (no Excel: Exibir > Congelar painéis).
       - "Resumo": a tabela_dinamica das vendas.
    Dicas: with pd.ExcelWriter(caminho_saida) as arquivo: ... e
    .to_excel(arquivo, sheet_name="Dados", index=False, freeze_panes=(1, 0)).
    """
    raise NotImplementedError("Implemente a função exportar_relatorio")

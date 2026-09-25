"""Desafio: da base crua à análise.

Implemente cada função abaixo. Leia a docstring de cada uma antes de começar.
O arquivo tem quatro partes: NumPy, leitura, dados faltantes e análise.

Regras:
- Na parte 1, use operações vetorizadas do NumPy: nada de for percorrendo os valores.
- Nas outras partes, use pandas. Evite for sobre as linhas do DataFrame: quase sempre existe
  um método pronto (groupby, merge, fillna, transform...).
- Nenhuma função pode alterar o DataFrame que recebe: trabalhe numa cópia.
- Não altere a pasta tests.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import numpy as np  # noqa: F401  (será usado na parte 1)
import pandas as pd

# ---------------------------------------------------------------------------------------------
# Parte 1: NumPy
# ---------------------------------------------------------------------------------------------


def padronizar(valores):
    """Devolve os valores padronizados (escore z), como array do NumPy.

    z = (valor - média) ÷ desvio padrão amostral. Use np.asarray(valores, dtype=float) para
    aceitar listas, e .mean() e .std(ddof=1). O resultado tem média 0 e desvio padrão 1.
    """
    raise NotImplementedError("Implemente a função padronizar")


def aplicar_desconto(precos, quantidades, minimo=10, desconto=0.10):
    """Devolve o total de cada item (preço x quantidade), com desconto para compras grandes.

    Itens com quantidade maior ou igual a minimo ganham o desconto (10% por padrão).
    Ex.: preços [10, 20, 5] e quantidades [2, 10, 12] dão [20, 180, 54].
    Dica: np.where(condição, valor_se_verdadeiro, valor_se_falso).
    """
    raise NotImplementedError("Implemente a função aplicar_desconto")


def classificar_valores(valores):
    """Classifica cada valor em "baixo" (menor que 100), "médio" (de 100 até menos de 500)
    ou "alto" (500 ou mais), e devolve um array com os rótulos.

    Dica: np.select([condição_1, condição_2], [rótulo_1, rótulo_2], default=rótulo_padrão).
    As condições são testadas em ordem, e vale a primeira verdadeira.
    """
    raise NotImplementedError("Implemente a função classificar_valores")


# ---------------------------------------------------------------------------------------------
# Parte 2: ler e conhecer os dados
# ---------------------------------------------------------------------------------------------


def ler_clientes(caminho_csv):
    """Já está pronta: lê o cadastro de clientes, que já vem limpo."""
    return pd.read_csv(caminho_csv, parse_dates=["data_cadastro"])


def ler_pedidos(caminho_csv):
    """Lê o CSV de pedidos com cada coluna no tipo certo e sem pedidos repetidos.

    1. A coluna data precisa virar data (parse_dates).
    2. Na coluna valor, o texto "n/d" significa "não disponível" e precisa virar faltante (na_values).
    3. A coluna id_cliente tem faltantes. Sem cuidado, o pandas a transforma em float.
       Use dtype={"id_cliente": "Int64"} (com I maiúsculo), o inteiro que aceita faltantes.
    4. Alguns pedidos vieram repetidos na exportação: fique com uma linha por id_pedido
       (.drop_duplicates(subset="id_pedido")) e refaça o índice.
    """
    raise NotImplementedError("Implemente a função ler_pedidos")


def resumo_faltantes(tabela):
    """Mostra quantos valores faltam em cada coluna.

    Devolve um DataFrame com uma linha por coluna que tem faltantes (as outras ficam de fora),
    ordenado da coluna com mais faltantes para a com menos, e duas colunas:
    - "faltantes": a quantidade de valores faltantes
    - "percentual": a porcentagem em relação ao total de linhas, arredondada para 1 casa
    Dica: tabela.isna().sum() conta os faltantes de cada coluna.
    """
    raise NotImplementedError("Implemente a função resumo_faltantes")


# ---------------------------------------------------------------------------------------------
# Parte 3: dados faltantes
# ---------------------------------------------------------------------------------------------


def tratar_faltantes(pedidos):
    """Trata os faltantes dos pedidos, cada coluna com a regra que faz sentido para ela.

    Nesta ordem:
    1. Pedido sem id_cliente não pode ser ligado a ninguém: remova a linha (.dropna(subset=...)).
    2. Canal faltante vira "não informado". Inventar um canal seria pior do que admitir que
       não se sabe.
    3. Crie a coluna "valor_imputado", True onde o valor está faltando. Ela registra o que
       foi estimado, para ninguém confundir com valor real.
    4. Valor faltante recebe a mediana do valor dos pedidos da mesma categoria. A mediana
       resiste a valores extremos, e cada categoria tem uma faixa de preço diferente.
       Dica: pedidos.groupby("categoria")["valor"].transform("median") devolve, para cada
       linha, a mediana da categoria dela.
    5. Refaça o índice.
    """
    raise NotImplementedError("Implemente a função tratar_faltantes")


# ---------------------------------------------------------------------------------------------
# Parte 4: juntar, agrupar e resumir
# ---------------------------------------------------------------------------------------------


def juntar_clientes(pedidos, clientes):
    """Acrescenta aos pedidos o nome e o estado de cada cliente.

    Use um merge pela coluna id_cliente, mantendo todos os pedidos (how="left"). Traga só as
    colunas id_cliente, nome e estado do cadastro. Passe validate="many_to_one": se algum
    cliente estiver duplicado no cadastro, o pandas avisa em vez de duplicar pedidos.
    """
    raise NotImplementedError("Implemente a função juntar_clientes")


def resumo_por_estado(pedidos):
    """Resume os pedidos por estado. Recebe os pedidos já juntados com os clientes.

    Devolve um DataFrame com o estado no índice e as colunas, nesta ordem:
    - "pedidos": quantidade de pedidos
    - "faturamento": soma do valor
    - "ticket_medio": média do valor
    Arredonde para 2 casas e ordene do maior faturamento para o menor.
    Dica: .groupby("estado").agg(pedidos=("id_pedido", "count"), ...).
    """
    raise NotImplementedError("Implemente a função resumo_por_estado")


def evolucao_mensal(pedidos):
    """Mostra o faturamento de cada mês e a variação em relação ao mês anterior.

    Devolve um DataFrame com o mês no índice, como texto "AAAA-MM", em ordem, e as colunas:
    - "faturamento": soma do valor no mês, arredondada para 2 casas
    - "variacao_pct": variação percentual em relação ao mês anterior, arredondada para 1 casa
      (o primeiro mês fica faltante, porque não tem mês anterior)
    Dicas: pedidos["data"].dt.to_period("M") dá o mês de cada pedido, e .pct_change()
    calcula a variação. Calcule a variação com o faturamento sem arredondar.
    """
    raise NotImplementedError("Implemente a função evolucao_mensal")


def top_clientes(pedidos, n=5):
    """Devolve uma Series com os n clientes que mais faturaram: o nome no índice e a soma do
    valor como valor, do maior para o menor, arredondada para 2 casas.

    Dica: .nlargest(n).
    """
    raise NotImplementedError("Implemente a função top_clientes")


def analisar(caminho_pedidos, caminho_clientes):
    """Junta tudo: lê, trata os faltantes, junta com os clientes e resume.

    Devolve um dicionário com três chaves:
    - "por_estado": resumo_por_estado
    - "mensal": evolucao_mensal
    - "top_clientes": top_clientes com n=5
    """
    raise NotImplementedError("Implemente a função analisar")

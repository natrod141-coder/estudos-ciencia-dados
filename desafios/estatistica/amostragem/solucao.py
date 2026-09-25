"""Desafio: uma amostra que represente a base de clientes.

Implemente cada função abaixo. Leia a docstring de cada uma antes de começar.

Regras:
- Use o pandas para ler e sortear (o método .sample) e o módulo math para as contas.
- Não use bibliotecas de amostragem prontas, como o scikit-learn.
- Não altere a pasta tests.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import math  # noqa: F401  (será usado em tamanhos_por_estrato, margem_de_erro e tamanho_amostra)

import pandas as pd  # noqa: F401  (será usado em amostra_estratificada e avaliar_amostras)


def amostra_aleatoria_simples(populacao, n, semente):
    """Sorteia n linhas do DataFrame populacao, sem reposição, e devolve um DataFrame.

    Use populacao.sample(n=n, random_state=semente): a mesma semente sempre gera a mesma
    amostra, o que torna a análise reproduzível.
    Levanta ValueError se n for maior que o número de linhas da população.
    """
    raise NotImplementedError("Implemente a função amostra_aleatoria_simples")


def amostra_sistematica(populacao, n, inicio=0):
    """Pega uma linha a cada k, começando pela linha na posição inicio, e devolve um DataFrame.

    Passo a passo:
    1. k = número de linhas da população // n (divisão inteira).
    2. Pegue as linhas nas posições inicio, inicio + k, inicio + 2k, ...
       Dica: populacao.iloc[inicio::k].
    3. Se vierem mais de n linhas (acontece quando a divisão não é exata), fique com as n primeiras.

    Levanta ValueError se n for maior que a população ou se inicio não estiver entre 0 e k - 1.
    """
    raise NotImplementedError("Implemente a função amostra_sistematica")


def tamanhos_por_estrato(populacao, coluna, n):
    """Decide quantas linhas sortear de cada estrato para uma amostra estratificada proporcional.

    Cada estrato é um valor diferente da coluna (por exemplo, cada região).
    Devolve um dicionário {estrato: tamanho}, com as chaves em ordem alfabética,
    e a soma dos tamanhos precisa dar exatamente n.

    Passo a passo (o "método do maior resto"):
    1. A cota de cada estrato é n x (linhas do estrato ÷ linhas da população).
       Ex.: com n = 30 e 420 de 1.000 clientes no Sudeste, a cota é 12,6.
    2. Cada estrato recebe a parte inteira da cota (math.floor): 12.
    3. As vagas que sobram vão, uma por estrato, para os que têm o maior resto (a parte
       depois da vírgula: 0,6). Em caso de empate, vence o estrato que vem antes em
       ordem alfabética.
    """
    raise NotImplementedError("Implemente a função tamanhos_por_estrato")


def amostra_estratificada(populacao, coluna, n, semente):
    """Sorteia uma amostra estratificada proporcional de n linhas e devolve um DataFrame.

    Para cada estrato, na ordem do dicionário devolvido por tamanhos_por_estrato, filtre as
    linhas do estrato e sorteie o tamanho dele com .sample(n=tamanho, random_state=semente).
    Depois junte as partes com pd.concat.
    """
    raise NotImplementedError("Implemente a função amostra_estratificada")


def erro_de_composicao(populacao, amostra, coluna):
    """Mede o quanto a composição da amostra se afasta da composição da população.

    Passo a passo:
    1. Calcule a porcentagem de cada categoria da coluna na população e na amostra.
       Dica: .value_counts(normalize=True) * 100.
    2. Uma categoria que existe na população e não aparece na amostra conta como 0% na amostra.
       Dica: .reindex(indice_da_populacao, fill_value=0).
    3. Devolva a maior diferença absoluta, em pontos percentuais, arredondada para 1 casa.

    Ex.: população com 50% básico e 50% premium, amostra só com básico: devolve 50.0.
    """
    raise NotImplementedError("Implemente a função erro_de_composicao")


def margem_de_erro(p, n, z=1.96):
    """Devolve a margem de erro de uma proporção: z x raiz(p x (1 - p) ÷ n).

    p é a proporção (entre 0 e 1), n é o tamanho da amostra e z vem do nível de confiança
    (1,96 para 95%). Ex.: margem_de_erro(0.5, 400) devolve 0.049, ou seja, 4,9 pontos percentuais.
    """
    raise NotImplementedError("Implemente a função margem_de_erro")


def tamanho_amostra(margem, p=0.5, z=1.96):
    """Devolve o tamanho mínimo de amostra para estimar uma proporção com a margem pedida.

    Fórmula: n = z² x p x (1 - p) ÷ margem², arredondado para cima (math.ceil).
    Use p = 0,5 quando não tiver ideia da proporção: é o caso que exige a maior amostra.
    Ex.: tamanho_amostra(0.05) devolve 385.
    """
    raise NotImplementedError("Implemente a função tamanho_amostra")


def avaliar_amostras(caminho_csv, n=100, semente=42):
    """Compara quatro formas de tirar uma amostra de n clientes, pelo erro de composição da região.

    Leia o CSV e monte as quatro amostras:
    - "primeiras_linhas": as n primeiras linhas do arquivo (clientes.head(n))
    - "aleatoria_simples": amostra_aleatoria_simples com a semente recebida
    - "sistematica": amostra_sistematica com inicio=0
    - "estratificada": amostra_estratificada pela coluna "regiao", com a semente recebida

    Devolve um dicionário {nome da amostra: erro_de_composicao pela coluna "regiao"}.
    """
    raise NotImplementedError("Implemente a função avaliar_amostras")

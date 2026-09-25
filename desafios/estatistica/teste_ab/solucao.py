"""Desafio: o botão novo vende mais?

Implemente cada função abaixo. Leia a docstring de cada uma antes de começar.

Regras:
- Use statistics.NormalDist para a distribuição normal (NORMAL, já criada abaixo).
- Não use scipy nem statsmodels. O objetivo é entender cada passo do teste.
- O pandas só serve para ler e somar os dados do CSV.
- Não altere a pasta tests.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import math  # noqa: F401  (será usado nos testes e no tamanho de amostra)
from statistics import NormalDist

import pandas as pd  # noqa: F401  (será usado em analisar_experimento e evolucao_do_p)

NORMAL = NormalDist()  # normal padrão: média 0, desvio padrão 1


def taxa_conversao(conversoes, visitantes):
    """Devolve a taxa de conversão: conversoes ÷ visitantes (um número entre 0 e 1).

    Levanta ValueError se visitantes for 0 ou menos, ou se conversoes não estiver
    entre 0 e visitantes.
    """
    raise NotImplementedError("Implemente a função taxa_conversao")


def teste_duas_proporcoes(conv_a, n_a, conv_b, n_b):
    """Teste z bilateral para a diferença entre as taxas de conversão de A e B.

    Passo a passo:
    1. taxa_a = conv_a ÷ n_a e taxa_b = conv_b ÷ n_b.
    2. Taxa combinada = (conv_a + conv_b) ÷ (n_a + n_b). Sob H0 os grupos têm a mesma taxa,
       então o erro padrão usa essa taxa única.
    3. Erro padrão = raiz(combinada x (1 - combinada) x (1/n_a + 1/n_b)).
    4. z = (taxa_b - taxa_a) ÷ erro padrão.
    5. p bilateral = 2 x (1 - NORMAL.cdf(|z|)).

    Devolve {"taxa_a", "taxa_b", "diferenca" (taxa_b - taxa_a), "z", "p"}, sem arredondar.
    """
    raise NotImplementedError("Implemente a função teste_duas_proporcoes")


def intervalo_diferenca(conv_a, n_a, conv_b, n_b, confianca=0.95):
    """Devolve o intervalo de confiança de (taxa_b - taxa_a) como tupla (inferior, superior).

    Aqui não se supõe H0, então cada grupo usa a própria taxa no erro padrão:
    1. Erro padrão = raiz(taxa_a x (1 - taxa_a) ÷ n_a + taxa_b x (1 - taxa_b) ÷ n_b).
    2. z crítico = NORMAL.inv_cdf(1 - (1 - confianca) / 2).
    3. Intervalo = diferença ± z crítico x erro padrão.
    """
    raise NotImplementedError("Implemente a função intervalo_diferenca")


def tamanho_amostra_por_grupo(taxa_base, efeito_minimo, alfa=0.05, poder=0.80):
    """Devolve quantos visitantes cada grupo precisa para detectar o efeito mínimo.

    taxa_base é a conversão atual (ex.: 0.10) e efeito_minimo é o menor aumento que vale
    a pena detectar, em pontos absolutos (ex.: 0.02 para ir de 10% a 12%).

    Passo a passo:
    1. taxa_nova = taxa_base + efeito_minimo.
    2. z_alfa = NORMAL.inv_cdf(1 - alfa / 2) e z_poder = NORMAL.inv_cdf(poder).
       Use o inv_cdf, e não valores arredondados como 1,96 e 0,84: o resultado muda.
    3. n = (z_alfa + z_poder)² x (taxa_base x (1 - taxa_base) + taxa_nova x (1 - taxa_nova))
           ÷ efeito_minimo².
    4. Arredonde para cima (math.ceil).
    """
    raise NotImplementedError("Implemente a função tamanho_amostra_por_grupo")


def divisao_balanceada(n_a, n_b, limite=0.001):
    """Confere se a divisão de visitantes entre A e B é compatível com 50% para cada lado.

    É a checagem de "sample ratio mismatch" (SRM): uma divisão muito desigual indica
    problema técnico no experimento, e o resultado não é confiável.

    Passo a passo:
    1. total = n_a + n_b.
    2. z = (n_a ÷ total - 0,5) ÷ raiz(0,25 ÷ total).
    3. p bilateral = 2 x (1 - NORMAL.cdf(|z|)).
    4. Devolve True se p for maior ou igual ao limite (0,001), e False caso contrário.
    """
    raise NotImplementedError("Implemente a função divisao_balanceada")


def decidir(conv_a, n_a, conv_b, n_b, alfa=0.05):
    """Decide o resultado do experimento. Devolve uma destas strings:

    - "divisao_desbalanceada": se divisao_balanceada(n_a, n_b) for False (confira isso primeiro)
    - "inconclusivo": se o p de teste_duas_proporcoes for maior que alfa
    - "vence_b": se o p for menor ou igual a alfa e B converter mais
    - "vence_a": se o p for menor ou igual a alfa e A converter mais
    """
    raise NotImplementedError("Implemente a função decidir")


def analisar_experimento(caminho_csv, alfa=0.05):
    """Lê o CSV do experimento, soma visitantes e conversões de cada grupo e analisa.

    Devolve um dicionário com:
    - "visitantes_a", "conversoes_a", "visitantes_b", "conversoes_b": os totais (inteiros)
    - "taxa_a", "taxa_b", "diferenca", "p": arredondados para 4 casas
    - "intervalo": intervalo_diferenca com confiança de (1 - alfa), como tupla com os dois
      limites arredondados para 4 casas
    - "decisao": o resultado de decidir

    Dica: experimento.groupby("grupo")[["visitantes", "conversoes"]].sum() e depois
    int(...) em cada total.
    """
    raise NotImplementedError("Implemente a função analisar_experimento")


def evolucao_do_p(caminho_csv):
    """Mostra como o valor p mudaria se alguém olhasse o resultado todo dia.

    Para cada data do experimento, em ordem, some os dados de todos os dias até aquela
    data (inclusive), rode teste_duas_proporcoes e guarde o p arredondado para 4 casas.
    Devolve a lista de valores p, um por dia.
    """
    raise NotImplementedError("Implemente a função evolucao_do_p")

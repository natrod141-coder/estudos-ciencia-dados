"""Desafio: o pacote tem mesmo 500 gramas?

Implemente cada função abaixo. Leia a docstring de cada uma antes de começar.

Regras:
- Pode usar o módulo statistics: mean e stdev para média e desvio padrão (você já os
  calculou na mão nos tópicos anteriores), e NormalDist para a distribuição normal.
- Não use scipy nem statsmodels. O objetivo é entender cada passo do teste.
- Não altere a pasta tests.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import math  # noqa: F401  (será usado nos testes z e no intervalo)
from statistics import NormalDist, mean, stdev  # noqa: F401

import pandas as pd  # noqa: F401  (será usado em analisar_pacotes)

NORMAL = NormalDist()  # normal padrão: média 0, desvio padrão 1


def valor_p(z, alternativa="bilateral"):
    """Devolve o valor p de uma estatística z, pela distribuição normal padrão.

    NORMAL.cdf(z) dá a probabilidade de a normal padrão ficar abaixo de z.
    - "bilateral" (H1: diferente): a área nas duas caudas, 2 x (1 - NORMAL.cdf(|z|))
    - "maior" (H1: maior): a área à direita de z, 1 - NORMAL.cdf(z)
    - "menor" (H1: menor): a área à esquerda de z, NORMAL.cdf(z)

    Levanta ValueError para qualquer outra alternativa.
    """
    raise NotImplementedError("Implemente a função valor_p")


def teste_z_media(amostra, mu0, alternativa="bilateral"):
    """Testa se a média da população é igual a mu0, a partir de uma amostra.

    Passo a passo:
    1. Calcule a média e o desvio padrão amostral (stdev) da amostra.
    2. Erro padrão = desvio ÷ raiz(n).
    3. z = (média - mu0) ÷ erro padrão.
    4. p = valor_p(z, alternativa).

    Devolve {"media": ..., "desvio": ..., "z": ..., "p": ...}, sem arredondar.
    Levanta ValueError se a amostra tiver menos de 30 valores: abaixo disso, o certo
    é usar um teste t.
    """
    raise NotImplementedError("Implemente a função teste_z_media")


def teste_z_proporcao(sucessos, n, p0, alternativa="bilateral"):
    """Testa se a proporção da população é igual a p0.

    Passo a passo:
    1. Proporção observada = sucessos ÷ n.
    2. z = (proporção - p0) ÷ raiz(p0 x (1 - p0) ÷ n).
    3. p = valor_p(z, alternativa).

    Devolve {"proporcao": ..., "z": ..., "p": ...}, sem arredondar.
    Levanta ValueError se sucessos não estiver entre 0 e n, ou se n x p0 ou n x (1 - p0)
    for menor que 10 (a aproximação pela normal não vale).
    """
    raise NotImplementedError("Implemente a função teste_z_proporcao")


def rejeita_h0(p, alfa=0.05):
    """Devolve True se o valor p for menor ou igual a alfa (rejeita H0), e False caso contrário.

    Lembre: False quer dizer "não rejeitamos H0", e não "provamos que H0 é verdadeira".
    """
    raise NotImplementedError("Implemente a função rejeita_h0")


def intervalo_confianca_media(amostra, confianca=0.95):
    """Devolve o intervalo de confiança da média como tupla (inferior, superior).

    Passo a passo:
    1. z crítico = NORMAL.inv_cdf(1 - (1 - confianca) / 2). Para 95%, dá 1,96.
    2. Margem = z crítico x desvio padrão amostral ÷ raiz(n).
    3. Intervalo = (média - margem, média + margem).
    """
    raise NotImplementedError("Implemente a função intervalo_confianca_media")


def analisar_pacotes(caminho_csv, peso_rotulo=500, alfa=0.05):
    """Testa se o peso médio dos pacotes é igual ao do rótulo (teste bilateral).

    Leia a coluna "peso_g" do CSV e devolva um dicionário com:
    - "n": quantidade de pacotes
    - "media", "desvio" e "z": arredondados para 2 casas
    - "p": o valor p bilateral, arredondado para 4 casas
    - "rejeita_h0": o resultado de rejeita_h0 com o alfa recebido
    - "intervalo": o intervalo de confiança de (1 - alfa), como tupla com os dois
      limites arredondados para 2 casas

    Atenção: decida com o p sem arredondar e só arredonde na hora de montar o dicionário.
    """
    raise NotImplementedError("Implemente a função analisar_pacotes")

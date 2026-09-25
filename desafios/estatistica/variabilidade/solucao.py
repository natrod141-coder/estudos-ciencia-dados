"""Desafio: qual centro de distribuição é mais confiável.

Implemente cada função abaixo. Leia a docstring de cada uma antes de começar.

Regras:
- Calcule amplitude, variância, desvio padrão, coeficiente de variação e intervalo interquartil
  "na mão", sem usar o módulo statistics nem numpy. O módulo math pode (math.sqrt).
- O pandas só pode ser usado para ler o arquivo CSV e separar os dados de cada centro.
- Não altere a pasta tests.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import math  # noqa: F401  (será usado em desvio_padrao)

import pandas as pd  # noqa: F401  (será usado em comparar_centros)


def amplitude(valores):
    """Devolve a amplitude: o maior valor menos o menor.

    Levanta ValueError se a lista estiver vazia.
    """
    raise NotImplementedError("Implemente a função amplitude")


def variancia(valores, amostral=True):
    """Devolve a variância: a média dos quadrados dos desvios em relação à média.

    Passo a passo:
    1. Calcule a média.
    2. Para cada valor, calcule (valor - média) ** 2 e some tudo.
    3. Divida a soma por n - 1 se amostral for True (o padrão), ou por n se for False.

    Levanta ValueError se a lista estiver vazia, ou se amostral for True e houver menos
    de 2 valores (não dá para dividir por n - 1 = 0).
    """
    raise NotImplementedError("Implemente a função variancia")


def desvio_padrao(valores, amostral=True):
    """Devolve o desvio padrão: a raiz quadrada da variância.

    Dica: reaproveite a função variancia.
    """
    raise NotImplementedError("Implemente a função desvio_padrao")


def coeficiente_variacao(valores):
    """Devolve o coeficiente de variação, em porcentagem: desvio padrão amostral ÷ média × 100.

    Exemplo: para [10, 12, 14], o desvio padrão é 2 e a média é 12, então o CV é 16,67.
    Levanta ValueError se a lista estiver vazia ou se a média for zero.
    """
    raise NotImplementedError("Implemente a função coeficiente_variacao")


def intervalo_interquartil(valores):
    """Devolve o intervalo interquartil (IQR): Q3 - Q1.

    Use o mesmo método do desafio de tendência central:
    1. Ordene os valores.
    2. Q1 é a mediana da metade inferior e Q3 é a mediana da metade superior.
       Se a quantidade de valores for ímpar, o valor central não entra em nenhuma das metades.

    Levanta ValueError se houver menos de 4 valores.
    """
    raise NotImplementedError("Implemente a função intervalo_interquartil")


def comparar_centros(caminho_csv, prazo=7):
    """Lê o CSV de entregas e compara a variabilidade dos centros de distribuição.

    Devolve um dicionário com duas chaves:

    - "centros": um dicionário com uma entrada por centro (o nome do centro é a chave).
      Cada entrada é outro dicionário com:
        - "media": média dos dias de entrega, arredondada para 2 casas
        - "desvio_padrao": desvio padrão amostral, arredondado para 2 casas
        - "coeficiente_variacao": CV em porcentagem, arredondado para 2 casas
        - "amplitude": a amplitude
        - "iqr": o intervalo interquartil
        - "percentual_atrasos": porcentagem de entregas com mais dias que o prazo,
          arredondada para 1 casa (ex.: 4 de 15 entregas atrasadas dá 26.7)
    - "mais_consistente": o nome do centro com o menor coeficiente de variação.

    Dica: dados.groupby("centro") percorre os centros um de cada vez, e
    grupo["dias"].tolist() devolve os dias de um centro como lista.
    """
    raise NotImplementedError("Implemente a função comparar_centros")

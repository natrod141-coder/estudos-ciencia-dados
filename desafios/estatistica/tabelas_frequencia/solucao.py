"""Desafio: como se distribuem os atendimentos do SAC.

Implemente cada função abaixo. Leia a docstring de cada uma antes de começar.

Regras:
- Na tabela de frequência, use o pandas (value_counts, cumsum).
- Monte as classes, os quartis e os limites do boxplot "na mão", sem numpy, sem o módulo
  statistics e sem pd.cut ou quantile. O módulo math pode.
- Não altere a pasta tests.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import math  # noqa: F401  (será usado em numero_de_classes)

import pandas as pd  # noqa: F401  (será usado em tabela_frequencia e resumo_atendimentos)


def tabela_frequencia(serie):
    """Devolve a tabela de frequência de uma Series do pandas, como DataFrame.

    O índice são os valores diferentes da série, em ordem crescente (ou alfabética).
    As colunas, nesta ordem:
    - "frequencia": quantas vezes o valor aparece
    - "relativa": a frequência em porcentagem do total, arredondada para 1 casa
    - "acumulada": a soma das frequências até aquele valor
    - "relativa_acumulada": a acumulada em porcentagem do total, arredondada para 1 casa

    Atenção: calcule a relativa acumulada a partir da coluna "acumulada". Somar as relativas
    já arredondadas acumula erro de arredondamento.
    Dicas: serie.value_counts().sort_index() e .cumsum().
    """
    raise NotImplementedError("Implemente a função tabela_frequencia")


def numero_de_classes(n):
    """Devolve o número de classes pela regra de Sturges: 1 + log2(n), arredondado para cima.

    Ex.: com 60 valores, 1 + log2(60) = 6,9, então 7 classes.
    Levanta ValueError se n for menor que 1.
    """
    raise NotImplementedError("Implemente a função numero_de_classes")


def tabela_por_classes(valores, k):
    """Agrupa valores numéricos em k classes de mesma largura e conta quantos caem em cada uma.

    Devolve uma lista de k dicionários {"inicio": ..., "fim": ..., "frequencia": ...}, da
    primeira classe para a última.

    Passo a passo:
    1. largura = (maior valor - menor valor) / k
    2. A classe i vai de menor + i x largura até menor + (i + 1) x largura.
    3. Um valor entra na classe se for maior ou igual ao início e menor que o fim.
       A exceção é a última classe, que também inclui o fim, para o maior valor não ficar de fora.
       Use o próprio maior valor como fim da última classe.

    Ex.: [10, 12, 15, 20, 22, 29, 30, 35, 41, 50] com k = 4 dá classes de largura 10:
    [10, 20) com 3 valores, [20, 30) com 3, [30, 40) com 2 e [40, 50] com 2.
    Levanta ValueError se a lista estiver vazia ou se k for menor que 1.
    """
    raise NotImplementedError("Implemente a função tabela_por_classes")


def cinco_numeros(valores):
    """Devolve o resumo de cinco números, que é a base do diagrama de caixa (boxplot).

    Dicionário com as chaves "minimo", "q1", "mediana", "q3" e "maximo".
    Use o mesmo método de quartis dos desafios anteriores: Q1 é a mediana da metade inferior
    e Q3 é a mediana da metade superior. Se a quantidade for ímpar, o valor central não
    entra em nenhuma das metades.
    Levanta ValueError se houver menos de 4 valores.
    """
    raise NotImplementedError("Implemente a função cinco_numeros")


def limites_boxplot(valores):
    """Calcula até onde vão os bigodes do boxplot e quais valores são atípicos.

    Passo a passo:
    1. IQR = Q3 - Q1 (use cinco_numeros).
    2. As cercas ficam em Q1 - 1,5 x IQR e Q3 + 1,5 x IQR.
    3. O bigode inferior é o MENOR VALOR DOS DADOS que está dentro das cercas, e o superior é
       o MAIOR VALOR DOS DADOS dentro das cercas. O bigode termina num dado real, e não na cerca.
    4. Atípicos são os valores fora das cercas, em ordem crescente.

    Devolve {"bigode_inferior": ..., "bigode_superior": ..., "atipicos": [...]}.
    """
    raise NotImplementedError("Implemente a função limites_boxplot")


def resumo_atendimentos(caminho_csv):
    """Lê o CSV de atendimentos e devolve um dicionário com:

    - "por_canal": tabela_frequencia da coluna "canal"
    - "por_nota": tabela_frequencia da coluna "nota"
    - "classes_tempo": tabela_por_classes da coluna "tempo_min", com o número de classes
      dado por numero_de_classes
    - "cinco_numeros_tempo": cinco_numeros da coluna "tempo_min"
    - "boxplot_tempo": limites_boxplot da coluna "tempo_min"

    Dica: atendimentos["tempo_min"].tolist() devolve os tempos como lista.
    """
    raise NotImplementedError("Implemente a função resumo_atendimentos")

"""Desafio: resumo estatístico de pedidos.

Implemente cada função abaixo. Leia a docstring de cada uma antes de começar.

Regras:
- Calcule média, mediana e moda "na mão", sem usar o módulo statistics nem numpy.
- O pandas só pode ser usado para ler o arquivo CSV.
- Não altere a pasta tests.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import pandas as pd  # noqa: F401  (será usado em resumo_pedidos)


def media(valores):
    """Devolve a média aritmética: soma dos valores dividida pela quantidade.

    Levanta ValueError se a lista estiver vazia.
    """
    raise NotImplementedError("Implemente a função media")


def mediana(valores):
    """Devolve a mediana: o valor central da lista em ordem crescente.

    Se a quantidade de valores for par, devolve a média dos dois valores centrais.
    Não pode alterar a lista recebida (dica: use sorted, que devolve uma cópia).
    Levanta ValueError se a lista estiver vazia.
    """
    raise NotImplementedError("Implemente a função mediana")


def moda(valores):
    """Devolve uma lista com o(s) valor(es) mais frequente(s), em ordem crescente.

    Se nenhum valor se repetir, devolve uma lista vazia.
    Exemplos: moda([1, 2, 2, 3]) -> [2]; moda([3, 5, 5, 7, 9, 9]) -> [5, 9]; moda([1, 2, 3]) -> [].
    Levanta ValueError se a lista estiver vazia.
    """
    raise NotImplementedError("Implemente a função moda")


def tem_atipico(valores):
    """Devolve True se algum valor for atípico pela regra do intervalo interquartil.

    Passo a passo:
    1. Ordene os valores.
    2. Q1 é a mediana da metade inferior e Q3 é a mediana da metade superior.
       Se a quantidade de valores for ímpar, o valor central não entra em nenhuma das metades.
    3. IQR = Q3 - Q1.
    4. Um valor é atípico se for menor que Q1 - 1,5 * IQR ou maior que Q3 + 1,5 * IQR.

    Com menos de 4 valores, devolve False.
    """
    raise NotImplementedError("Implemente a função tem_atipico")


def escolher_medida(valores):
    """Devolve "mediana" se houver valor atípico e "media" caso contrário."""
    raise NotImplementedError("Implemente a função escolher_medida")


def resumo_pedidos(caminho_csv):
    """Lê a coluna "valor" do arquivo CSV e devolve um dicionário com:

    - "quantidade": quantos pedidos
    - "media": a média, arredondada para 2 casas
    - "mediana": a mediana, arredondada para 2 casas
    - "moda": a lista devolvida por moda()
    - "tem_atipico": o resultado de tem_atipico()
    - "medida_recomendada": o resultado de escolher_medida()

    Dica: pd.read_csv(caminho_csv)["valor"].tolist() devolve os valores como lista.
    """
    raise NotImplementedError("Implemente a função resumo_pedidos")

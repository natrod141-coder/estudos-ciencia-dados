"""Desafio: cada coluna no seu tipo.

Implemente cada função abaixo e preencha o dicionário CLASSIFICACAO.
Leia a docstring de cada função antes de começar.

Regras:
- Use o pandas à vontade: aqui o objetivo é tratar cada tipo de variável do jeito certo.
- Não altere a pasta tests.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import pandas as pd  # noqa: F401  (será usado em ler_pesquisa)

# A ordem das categorias das variáveis ordinais, da menor para a maior. Não altere.
ORDEM_ESCOLARIDADE = ["fundamental", "médio", "superior", "pós-graduação"]
ORDEM_SATISFACAO = ["muito insatisfeito", "insatisfeito", "neutro", "satisfeito", "muito satisfeito"]

# Classifique cada coluna de data/pesquisa.csv trocando None por um destes tipos:
# "nominal", "ordinal", "discreta" ou "continua" (sem acento).
CLASSIFICACAO = {
    "cidade": None,
    "cep": None,
    "escolaridade": None,
    "satisfacao": None,
    "dependentes": None,
    "compras_no_ano": None,
    "renda_mensal": None,
}


def medidas_permitidas(tipo):
    """Devolve a lista de medidas de tendência central que fazem sentido para o tipo.

    - "nominal": ["moda"]
    - "ordinal": ["moda", "mediana"]
    - "discreta": ["moda", "mediana", "media"]
    - "continua": ["mediana", "media"]  (valores contínuos quase nunca se repetem,
      então a moda dos valores brutos não diz nada)

    Devolva a lista exatamente nessa ordem. Levanta ValueError para um tipo desconhecido.
    """
    raise NotImplementedError("Implemente a função medidas_permitidas")


def ler_pesquisa(caminho_csv):
    """Lê o CSV da pesquisa e devolve um DataFrame com cada coluna no tipo certo.

    1. O CEP precisa ficar como texto. Lido como número, "01310100" vira 1310100 e perde o zero.
       Dica: pd.read_csv(caminho_csv, dtype={"cep": str}).
    2. escolaridade e satisfacao precisam virar categorias ordenadas, com as ordens definidas
       no começo deste arquivo.
       Dica: pd.Categorical(coluna, categories=ORDEM_SATISFACAO, ordered=True).
    """
    raise NotImplementedError("Implemente a função ler_pesquisa")


def mediana_ordinal(serie):
    """Devolve a categoria mediana de uma série categórica ordenada.

    O pandas não calcula a mediana de categorias, mas cada categoria tem um código numérico
    na ordem certa (serie.cat.codes: 0 para a primeira categoria, 1 para a segunda...).

    Passo a passo:
    1. Pegue os códigos, ignore os valores faltantes (código -1) e ordene.
    2. Pegue o código na posição (quantidade - 1) // 2. Com quantidade par, isso dá a
       mediana inferior, a menor das duas categorias centrais.
    3. Devolva o nome da categoria desse código: serie.cat.categories[codigo].
    """
    raise NotImplementedError("Implemente a função mediana_ordinal")


def resumo_central(pesquisa):
    """Calcula, para cada coluna de CLASSIFICACAO, só as medidas que fazem sentido para o tipo dela.

    Recebe o DataFrame devolvido por ler_pesquisa e devolve um dicionário no formato
    {coluna: {medida: valor}}, com as medidas de medidas_permitidas(tipo da coluna):

    - "moda": serie.mode().iloc[0] (se houver empate, fica com a primeira)
    - "mediana": para ordinais, mediana_ordinal(serie); para quantitativas,
      a mediana arredondada para 2 casas
    - "media": a média arredondada para 2 casas

    Ex.: {"cidade": {"moda": "São Paulo"}, "escolaridade": {"moda": ..., "mediana": ...}, ...}
    """
    raise NotImplementedError("Implemente a função resumo_central")

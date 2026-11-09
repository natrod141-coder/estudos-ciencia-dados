"""Desafio: um modelo de linguagem de brinquedo.

Um LLM de verdade tem bilhões de parâmetros, mas as peças que você usa no dia a dia são
simples: tokens, probabilidades do próximo token, temperatura, janela de contexto e custo.
Aqui você implementa cada uma em miniatura, sem chamar nenhuma API.

Regras:
- Use só Python puro: nada de bibliotecas de IA.
- Nenhuma função pode alterar o que recebe.
- Não altere a pasta tests nem o arquivo em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""


def tokenizar(texto, vocabulario):
    """Quebra o texto em tokens, como um tokenizador de subpalavras.

    Para cada palavra do texto (separadas por espaço):
    1. A partir do começo, pegue o MAIOR pedaço que está no vocabulário.
    2. Se nenhum pedaço estiver no vocabulário, pegue um caractere sozinho.
    3. Continue do ponto em que parou, até o fim da palavra.
    Devolve a lista de tokens, sem os espaços.

    Ex.: com o vocabulário {"des", "valor", "valoriza", "ção"}, "desvalorização" vira
    ["des", "valoriza", "ção"].
    """
    raise NotImplementedError("Implemente a função tokenizar")


def aplicar_temperatura(probabilidades, temperatura):
    """Ajusta as probabilidades do próximo token com a temperatura.

    Cada probabilidade p vira p ** (1 / temperatura), e depois tudo é dividido pela soma,
    para voltar a somar 1. Temperatura menor que 1 concentra a chance no token mais
    provável; maior que 1 espalha entre os outros.
    Recebe e devolve um dicionário {token: probabilidade}.
    Levanta ValueError se a temperatura for 0 ou negativa.
    """
    raise NotImplementedError("Implemente a função aplicar_temperatura")


def filtrar_top_p(probabilidades, p):
    """Mantém só os tokens mais prováveis cuja probabilidade somada chega a p (top-p).

    1. Ordene os tokens do mais provável para o menos provável (no empate, em ordem alfabética).
    2. Vá somando as probabilidades e guardando os tokens. Pare no primeiro token em que a
       soma chegar a p ou passar (esse token entra).
    3. Divida as probabilidades guardadas pela soma delas, para voltar a somar 1.
    Ex.: {"a": 0.5, "b": 0.3, "c": 0.2} com p = 0.7 fica {"a": 0.625, "b": 0.375}.
    """
    raise NotImplementedError("Implemente a função filtrar_top_p")


def treinar_bigramas(texto):
    """Treina um modelo de bigramas: conta, para cada palavra, quais palavras vêm logo depois.

    Passe o texto para minúsculas e separe as palavras por espaço (as quebras de linha
    também separam). Devolve {palavra: {palavra_seguinte: quantidade}}.
    Ex.: "o gato o rato" dá {"o": {"gato": 1, "rato": 1}, "gato": {"o": 1}}.
    """
    raise NotImplementedError("Implemente a função treinar_bigramas")


def probabilidades_do_proximo(modelo, palavra):
    """Devolve {palavra_seguinte: probabilidade} depois da palavra, a partir das contagens.

    Cada contagem é dividida pelo total de contagens da palavra. Palavra que o modelo não
    conhece devolve um dicionário vazio.
    """
    raise NotImplementedError("Implemente a função probabilidades_do_proximo")


def gerar_guloso(modelo, inicio, n):
    """Gera até n palavras depois de inicio, escolhendo sempre a próxima mais provável.

    No empate, vence a que vem antes em ordem alfabética. Se a última palavra não tiver
    próxima conhecida, a geração para antes. Devolve a lista de palavras, começando por inicio.
    """
    raise NotImplementedError("Implemente a função gerar_guloso")


def cortar_historico(mensagens, limite):
    """Corta o histórico de uma conversa para caber no limite de tokens.

    mensagens é uma lista de dicionários {"papel": "system" | "user" | "assistant",
    "tokens": int}. As mensagens de "system" (as instruções) ficam sempre. Das outras,
    tire a mais antiga, uma de cada vez, até o total de tokens caber no limite.
    Devolve uma lista nova: primeiro as de system, depois as que sobraram, na ordem original.
    Levanta ValueError se só as mensagens de system já passarem do limite.
    """
    raise NotImplementedError("Implemente a função cortar_historico")


def cabe_na_janela(tokens_entrada, max_saida, janela):
    """Devolve True se a entrada mais o máximo de tokens da resposta cabem na janela de contexto."""
    raise NotImplementedError("Implemente a função cabe_na_janela")


def custo_em_dolares(tokens_entrada, tokens_saida, preco_entrada, preco_saida):
    """Custo de uma chamada, com os preços dados em dólares por milhão de tokens.

    Ex.: 2.000 tokens de entrada a US$ 2/milhão e 500 de saída a US$ 10/milhão custam
    0,004 + 0,005 = US$ 0,009.
    """
    raise NotImplementedError("Implemente a função custo_em_dolares")

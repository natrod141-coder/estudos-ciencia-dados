"""Gabarito do desafio "Um modelo de linguagem de brinquedo".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""


def tokenizar(texto, vocabulario):
    tokens = []
    for palavra in texto.split():
        inicio = 0
        while inicio < len(palavra):
            # do pedaço mais longo para o mais curto; um caractere sozinho sempre serve
            for fim in range(len(palavra), inicio, -1):
                pedaco = palavra[inicio:fim]
                if pedaco in vocabulario or fim == inicio + 1:
                    tokens.append(pedaco)
                    inicio = fim
                    break
    return tokens


def aplicar_temperatura(probabilidades, temperatura):
    if temperatura <= 0:
        raise ValueError("A temperatura precisa ser maior que zero.")
    pesos = {token: p ** (1 / temperatura) for token, p in probabilidades.items()}
    total = sum(pesos.values())
    return {token: peso / total for token, peso in pesos.items()}


def filtrar_top_p(probabilidades, p):
    if not 0 < p <= 1:
        raise ValueError("p precisa estar entre 0 (exclusive) e 1.")
    ordenados = sorted(probabilidades.items(), key=lambda item: (-item[1], item[0]))
    mantidos, acumulado = {}, 0.0
    for token, prob in ordenados:
        mantidos[token] = prob
        acumulado += prob
        if acumulado >= p - 1e-9:
            break
    total = sum(mantidos.values())
    return {token: prob / total for token, prob in mantidos.items()}


def treinar_bigramas(texto):
    palavras = texto.lower().split()
    modelo = {}
    for atual, proxima in zip(palavras, palavras[1:]):
        contagens = modelo.setdefault(atual, {})
        contagens[proxima] = contagens.get(proxima, 0) + 1
    return modelo


def probabilidades_do_proximo(modelo, palavra):
    contagens = modelo.get(palavra, {})
    total = sum(contagens.values())
    return {token: c / total for token, c in contagens.items()} if total else {}


def gerar_guloso(modelo, inicio, n):
    texto = [inicio]
    for _ in range(n):
        probabilidades = probabilidades_do_proximo(modelo, texto[-1])
        if not probabilidades:
            break
        texto.append(min(probabilidades, key=lambda token: (-probabilidades[token], token)))
    return texto


def cortar_historico(mensagens, limite):
    sistema = [m for m in mensagens if m["papel"] == "system"]
    conversa = [m for m in mensagens if m["papel"] != "system"]
    if sum(m["tokens"] for m in sistema) > limite:
        raise ValueError("As instruções de sistema sozinhas já passam do limite.")
    while sum(m["tokens"] for m in sistema + conversa) > limite:
        conversa.pop(0)  # sai a mensagem mais antiga
    return sistema + conversa


def cabe_na_janela(tokens_entrada, max_saida, janela):
    return tokens_entrada + max_saida <= janela


def custo_em_dolares(tokens_entrada, tokens_saida, preco_entrada, preco_saida):
    return tokens_entrada / 1_000_000 * preco_entrada + tokens_saida / 1_000_000 * preco_saida

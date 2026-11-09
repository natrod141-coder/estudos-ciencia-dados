"""Gabarito do desafio "Uma imagem Docker para a API".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import re

PALAVRAS_DE_SEGREDO = ("KEY", "TOKEN", "SECRET", "SENHA", "PASSWORD")


def ler_instrucoes(texto):
    instrucoes, atual = [], ""
    for linha in texto.splitlines():
        limpa = linha.strip()
        if not limpa or limpa.startswith("#"):  # o Docker descarta, até no meio de uma instrução
            continue
        if limpa.endswith("\\"):  # a instrução continua na próxima linha
            atual += limpa[:-1].strip() + " "
            continue
        atual += limpa
        nome, _, argumentos = atual.partition(" ")
        instrucoes.append((nome.upper(), argumentos.strip()))
        atual = ""
    return instrucoes


def nomes_de_variaveis(argumentos):
    """Os nomes definidos num ENV ou num ARG: "A=1 B=2" tem A e B; "A 1" e "A" têm só A."""
    if "=" in argumentos:
        return re.findall(r"(?:^|\s)([A-Za-z_]\w*)=", argumentos)
    return argumentos.split()[:1]


def problemas(instrucoes):
    encontrados = []
    nomes_de_etapas = set()
    for nome, argumentos in instrucoes:
        if nome == "FROM":
            partes = argumentos.split()
            imagem = partes[0]
            if imagem not in nomes_de_etapas and (":" not in imagem or imagem.endswith(":latest")):
                encontrados.append("imagem-sem-versao")
            if len(partes) == 3 and partes[1].upper() == "AS":
                nomes_de_etapas.add(partes[2])
    if any(n == "RUN" and "pip install" in a and "--no-cache-dir" not in a for n, a in instrucoes):
        encontrados.append("pip-com-cache")
    ultima_etapa = max((i for i, (n, _) in enumerate(instrucoes) if n == "FROM"), default=0)
    usuarios = [a.strip() for n, a in instrucoes[ultima_etapa:] if n == "USER"]
    if not usuarios or usuarios[-1].split(":")[0] in ("root", "0"):
        encontrados.append("usuario-root")
    if any(n in ("CMD", "ENTRYPOINT") and not a.startswith("[") for n, a in instrucoes):
        encontrados.append("cmd-forma-shell")
    variaveis = [v.upper() for n, a in instrucoes if n in ("ENV", "ARG") for v in nomes_de_variaveis(a)]
    if any(palavra in variavel for variavel in variaveis for palavra in PALAVRAS_DE_SEGREDO):
        encontrados.append("segredo-no-dockerfile")
    copia_tudo = [i for i, (n, a) in enumerate(instrucoes) if n == "COPY" and fontes(a) and fontes(a)[0] in (".", "./")]
    instalacoes = [i for i, (n, a) in enumerate(instrucoes) if n == "RUN" and "pip install" in a]
    if copia_tudo and instalacoes and copia_tudo[0] < instalacoes[-1]:
        encontrados.append("copia-tudo-antes-de-instalar")
    return encontrados


def _casa_partes(caminho, padrao):
    if not padrao:
        return not caminho
    if padrao[0] == "**":
        # ** casa zero ou mais pastas
        return any(_casa_partes(caminho[i:], padrao[1:]) for i in range(len(caminho) + 1))
    if not caminho:
        return False
    return _casa_segmento(caminho[0], padrao[0]) and _casa_partes(caminho[1:], padrao[1:])


def _casa_segmento(nome, padrao):
    # * e ? valem só dentro de um nome, sem atravessar a barra
    expressao = "".join(".*" if c == "*" else "." if c == "?" else re.escape(c) for c in padrao)
    return re.fullmatch(expressao, nome) is not None


def casa(caminho, padrao):
    """True se o padrão casa com o caminho ou com uma das pastas que o contêm."""
    partes = caminho.strip("/").split("/")
    padrao_partes = padrao.strip().removeprefix("./").strip("/").split("/")
    return any(_casa_partes(partes[:k], padrao_partes) for k in range(1, len(partes) + 1))


def ignorado(caminho, padroes):
    resultado = False
    for linha in padroes:
        padrao = linha.strip()
        if not padrao or padrao.startswith("#"):
            continue
        if padrao.startswith("!"):
            if casa(caminho, padrao[1:]):
                resultado = False  # a exceção vale sobre as regras de antes
        elif casa(caminho, padrao):
            resultado = True
    return resultado


def fontes(argumentos):
    partes = [p for p in argumentos.split() if not p.startswith("--")]
    return partes[:-1]


def primeira_etapa_refeita(instrucoes, alterados, padroes_ignorados=()):
    relevantes = [c for c in alterados if not ignorado(c, padroes_ignorados)]
    for indice, (nome, argumentos) in enumerate(instrucoes):
        if nome not in ("COPY", "ADD"):
            continue
        for fonte in fontes(argumentos):
            if any(fonte in (".", "./") or casa(arquivo, fonte) for arquivo in relevantes):
                return indice
    return None

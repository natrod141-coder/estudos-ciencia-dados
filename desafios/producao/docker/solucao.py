"""Desafio: uma imagem Docker para a API.

A API de cancelamento está pronta, na pasta app. Falta empacotá-la numa imagem que rode igual no
seu computador, no do colega e na nuvem. O desafio tem duas partes:

1. Um pequeno verificador de Dockerfile, neste arquivo: ler as instruções, apontar os problemas
   mais comuns, entender o .dockerignore e descobrir qual etapa o Docker refaz quando um arquivo
   muda. É o que ferramentas como o hadolint e o próprio docker build fazem, em versão reduzida.
2. O Dockerfile e o .dockerignore da API, nos arquivos com esses nomes, nesta pasta. Os testes
   conferem os dois com o seu verificador.

Regras:
- Use só a biblioteca padrão do Python (re, fnmatch, json). Nenhuma função pode alterar o que recebe.
- Não altere a pasta app, a pasta tests nem o requirements.txt.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import re

PALAVRAS_DE_SEGREDO = ("KEY", "TOKEN", "SECRET", "SENHA", "PASSWORD")


def ler_instrucoes(texto):
    """Lê o texto de um Dockerfile e devolve a lista de instruções, cada uma como uma tupla
    (INSTRUCAO, argumentos).

    - O nome da instrução vai em maiúsculas: "from" vira "FROM".
    - Linhas em branco e linhas que começam com # (comentários) são descartadas, inclusive no
      meio de uma instrução que continua.
    - Uma linha que termina em \\ continua na próxima: junte as partes com um espaço, sem a barra.
    - Os argumentos vão sem espaços nas pontas.
    """
    raise NotImplementedError("Implemente a função ler_instrucoes")


def problemas(instrucoes):
    """Recebe a lista de ler_instrucoes e devolve os códigos dos problemas encontrados, sem
    repetição, na ordem da tabela:

    - "imagem-sem-versao": um FROM sem versão (python) ou com latest (python:latest). Um FROM que
      usa o nome de uma etapa anterior, como em "FROM python:3.14-slim AS base" e depois
      "FROM base", não conta.
    - "pip-com-cache": um RUN com pip install sem --no-cache-dir.
    - "usuario-root": a última etapa (depois do último FROM) não tem USER, ou o último USER dela
      é root ou 0.
    - "cmd-forma-shell": um CMD ou ENTRYPOINT que não está na forma exec, a lista entre colchetes.
    - "segredo-no-dockerfile": um ENV ou ARG que define uma variável com KEY, TOKEN, SECRET, SENHA
      ou PASSWORD no nome, em qualquer caixa. Um ENV pode definir várias: "ENV A=1 B=2".
    - "copia-tudo-antes-de-instalar": um COPY . (o contexto inteiro) antes do último RUN com
      pip install.
    """
    raise NotImplementedError("Implemente a função problemas")


def ignorado(caminho, padroes):
    """True se o arquivo `caminho` (relativo à pasta do build, com barras /) fica de fora da imagem,
    segundo as linhas do .dockerignore em `padroes`.

    - Linhas em branco e comentários (#) não contam.
    - Um padrão vale para o caminho e para tudo dentro dele: ".venv" tira ".venv/lib/site.py".
    - * e ? valem dentro de um nome, sem atravessar a barra: "*.md" pega "notas.md", mas não
      "docs/guia.md". ** vale por qualquer número de pastas, inclusive nenhuma: "**/__pycache__"
      pega "__pycache__" e "app/__pycache__".
    - Um padrão que começa com ! é uma exceção. As linhas são lidas em ordem, e vale a última que
      casar com o caminho.
    """
    raise NotImplementedError("Implemente a função ignorado")


def primeira_etapa_refeita(instrucoes, alterados, padroes_ignorados=()):
    """O Docker guarda cada etapa do build em cache. Quando um arquivo muda, ele refaz a partir do
    primeiro COPY ou ADD que leva esse arquivo para a imagem, e tudo o que vem depois.

    Devolva a posição, na lista `instrucoes`, do primeiro COPY ou ADD que copia algum dos arquivos
    `alterados`, ou None se nenhum for copiado. Arquivos ignorados pelo .dockerignore
    (`padroes_ignorados`) não chegam ao build e não contam. As fontes de um COPY são os argumentos
    menos o último (o destino) e menos as opções que começam com --. A fonte "." leva tudo; uma
    pasta leva o que está dentro dela.
    """
    raise NotImplementedError("Implemente a função primeira_etapa_refeita")

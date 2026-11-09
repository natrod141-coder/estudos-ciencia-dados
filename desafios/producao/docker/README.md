# Desafio: uma imagem Docker para a API

A API de cancelamento está pronta, na pasta `app`. Ela roda no seu computador, mas a nuvem não
tem o seu Python, as suas bibliotecas nem as suas pastas. A solução é empacotar tudo numa imagem
Docker: o sistema, o Python, as dependências com as versões certas e o código.

O desafio tem duas partes. Na primeira, você escreve um pequeno verificador de Dockerfile, que
aponta os erros mais comuns e explica o cache do build. Na segunda, você escreve o `Dockerfile` e
o `.dockerignore` da API, e o seu verificador confere os dois.

## Os arquivos

- `app/`: a API de cancelamento, com o modelo. Já está pronta.
- `requirements.txt`: as dependências da imagem, com versões fixas.
- `Dockerfile` e `.dockerignore`: só com um comentário. Você escreve.
- `solucao.py`: as funções do verificador.

## O que fazer

1. Implemente as funções do `solucao.py`, na ordem do arquivo: `ler_instrucoes`, `problemas`,
   `ignorado` e `primeira_etapa_refeita`.
2. Escreva o `Dockerfile` da API. Ele precisa:
   - partir da imagem oficial do Python, na variante slim e com a versão, como `python:3.14-slim`;
   - instalar as dependências antes de copiar o código, para aproveitar o cache;
   - copiar só a pasta `app`;
   - rodar com um usuário que não seja o root;
   - declarar a porta 8080 com `EXPOSE` e subir a API com `fastapi run` nessa porta, na forma
     exec do `CMD`;
   - não ter nenhum dos problemas que o seu verificador aponta.
3. Escreva o `.dockerignore`, para que `.env`, `.git`, `.venv`, as pastas `__pycache__` e a pasta
   `tests` fiquem fora da imagem.

## Regras

1. Use só a biblioteca padrão do Python. Nenhuma função pode alterar o que recebe.
2. Não altere a pasta `app`, a pasta `tests` nem o `requirements.txt`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 10 testes passam. Os testes não precisam do Docker instalado.

## Para construir e rodar a imagem

Com o Docker Desktop instalado e aberto, dentro desta pasta:

```
docker build -t api-cancelamento .
docker run --rm -p 8080:8080 -e CHAVE_API=minha-chave-local api-cancelamento
```

Abra http://localhost:8080/docs. Para parar, use Ctrl+C no terminal.

## Se travar

1. Rode só um teste: `pytest -v -k dockerignore`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Para o `.dockerignore`, teste o padrão na mão: `ignorado("app/__pycache__/x.pyc", ["**/__pycache__"])`.
4. Só então consulte o gabarito em `desafios/_gabaritos/producao/docker/`.

## Depois de passar

- Construa a imagem, mude uma linha de `app/main.py` e construa de novo. Quais etapas aparecem
  como `CACHED`? Agora inverta a ordem, copiando tudo antes do `pip install`, e compare o tempo.
- Rode `docker build --check .` com o seu Dockerfile e com um que tenha `ENV ANTHROPIC_API_KEY=...`.
  O que o próprio Docker aponta?
- Rode `docker history api-cancelamento`. Que etapa ocupa mais espaço, e por quê?

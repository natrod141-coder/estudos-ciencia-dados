# Desafio: Git na prática

Você entrou num time de dados que versiona tudo com Git, e as situações do dia a dia aparecem logo na
primeira semana: começar um repositório, escolher o que não vai para ele, trabalhar numa branch,
desfazer um engano, resolver um conflito, enviar e receber mudanças do GitHub. Neste desafio, cada
situação é um repositório de verdade, e você responde com os comandos que usaria no terminal.

## Como funciona

No `solucao.py`, cada situação tem uma variável. A resposta é a **lista de comandos git**, na ordem
em que você os digitaria, um comando por item:

```python
CRIAR_BRANCH = [
    "git ...",
]
```

A exceção é o `.gitignore`: a resposta é o conteúdo do arquivo, entre aspas triplas.

Os testes criam cada repositório numa pasta temporária, rodam os seus comandos dentro dela e conferem
o resultado: quais commits existem, em que branch você está, o que ficou no disco, o que chegou ao
remoto. Nada acontece no seu projeto. O "remoto" dos testes é um repositório local que faz o papel do
GitHub, então não é preciso internet nem conta.

## O que você vai praticar

- `init`, `add`, `commit` e `status`.
- `.gitignore` para segredos, ambientes virtuais, arquivos gerados e dados grandes.
- `switch` e `branch` para trabalhar em branches.
- `restore` e `reset` para desfazer, sem perder trabalho.
- `merge` e a resolução de conflitos.
- `push`, `pull` e `fetch` com um repositório remoto.

## Regras

1. Só comandos git, um por item da lista. Nada de `cd`, `&&`, `|` ou outros programas.
2. Os comandos rodam na pasta raiz do repositório.
3. Commits precisam de mensagem com `-m`: os testes não abrem editor.
4. Não altere a pasta `tests`.

Os testes precisam do Git 2.32 ou superior. Confira com `git --version`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 9 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k merge`.
2. A mensagem de erro mostra cada comando que rodou e a saída dele. Leia a saída do Git: ele costuma
   dizer o que fazer a seguir, como "fix conflicts and then commit the result".
3. Reproduza a situação à mão: crie uma pasta de teste fora do projeto, `git init`, e experimente os
   comandos, olhando `git status` e `git log --oneline --graph --all` a cada passo.
4. Só então consulte o gabarito em `desafios/_gabaritos/manipulacao/git_github/`.

## Depois de passar

Faça a entrega deste desafio com o mesmo fluxo que você acabou de praticar: branch, commit, push e
Pull Request. Na página do Pull Request, no GitHub, veja a aba "Files changed" e deixe um comentário
numa linha do seu próprio código, como faria numa revisão. Depois, pense: na situação 6, por que o
enunciado faz questão de dizer que o commit ainda não foi enviado para o remoto?

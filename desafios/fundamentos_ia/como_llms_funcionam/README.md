# Desafio: um modelo de linguagem de brinquedo

Um LLM de verdade tem bilhões de parâmetros e foi treinado com uma quantidade enorme de texto. Mas as
peças que aparecem no dia a dia de quem usa um são simples: o texto vira **tokens**, o modelo calcula
a **probabilidade de cada próximo token**, a **temperatura** muda essas probabilidades, a conversa
precisa caber na **janela de contexto**, e cada token tem um **custo**.

Neste desafio, você vai construir cada peça em miniatura, sem chamar nenhuma API e sem custo. No fim,
terá um "modelo" que aprende com o texto de `data/corpus.txt` e gera frases prevendo a próxima palavra.

## O que você vai praticar

- Como um tokenizador quebra palavras em pedaços, e por que palavras raras gastam mais tokens.
- Como a temperatura e o top-p mudam as probabilidades do próximo token.
- Como um modelo prevê a próxima palavra a partir do que viu no treino.
- Por que o histórico de uma conversa precisa ser cortado, e o que fica de fora.
- Como estimar o custo de uma chamada.

## O que fazer

Abra o `solucao.py` e implemente as nove funções, na ordem do arquivo. Cada docstring explica o que
a função recebe e devolve, com um exemplo.

## Regras

1. Use só Python puro: nada de bibliotecas de IA.
2. Nenhuma função pode alterar o que recebe.
3. Não altere a pasta `tests` nem o arquivo em `data`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 10 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k temperatura`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Para o tokenizador, faça "desvalorização" à mão, pedaço por pedaço, antes de programar.
4. Só então consulte o gabarito em `desafios/_gabaritos/fundamentos_ia/como_llms_funcionam/`.

## Depois de passar

Gere 8 palavras a partir de "o" com `gerar_guloso` e veja o laço: "o modelo prevê o modelo prevê...".
Escolher sempre a palavra mais provável leva à repetição. Agora troque a escolha gulosa por um sorteio
com as probabilidades (`random.choices`), primeiro com temperatura 0,5 e depois com 2. Gere várias
vezes e compare: em qual temperatura o texto fica mais variado, e em qual fica mais sem sentido?

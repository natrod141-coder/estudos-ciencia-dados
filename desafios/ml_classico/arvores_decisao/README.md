# Desafio: uma árvore que se explica, e que decora

A regressão logística do tópico anterior soma o efeito de cada variável. Mas, nos dados das
assinaturas, há grupos de risco que só aparecem em combinação: o cliente insatisfeito que também
abriu vários chamados, o cliente novo que quase não usa o serviço. Uma árvore de decisão encontra
esse tipo de padrão sozinha, com perguntas em sequência.

O problema é que uma árvore sem limite continua fazendo perguntas até acertar cada cliente do
treino, e aí ela decora, em vez de aprender. Você vai ver isso acontecer, escolher a profundidade
certa num conjunto de validação e medir o resultado final no teste.

## Os dados

`data/assinaturas.csv`: os mesmos 5 mil clientes do tópico de regressão logística. O alvo é
`cancelou`.

## O que fazer

Abra o `solucao.py` e implemente as funções, na ordem do arquivo. Cada docstring explica o que a
função recebe e devolve.

## Regras

1. Use pandas e scikit-learn. Nenhuma função pode alterar o que recebe.
2. Não altere a pasta `tests` nem os arquivos em `data`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 9 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k curva`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Imprima a curva de profundidade e olhe as duas colunas de AUC lado a lado. Em que profundidade
   a validação para de melhorar?
4. Só então consulte o gabarito em `desafios/_gabaritos/ml_classico/arvores_decisao/`.

## Depois de passar

- Imprima as regras da árvore de profundidade 3 e traduza cada caminho até uma folha para uma
  frase que o time de retenção entenda.
- Troque a profundidade por `min_samples_leaf`, o mínimo de clientes por folha, e teste valores como
  20, 50 e 100. Qual dá a melhor AUC na validação?
- Compare a AUC de teste da sua árvore com a da regressão logística do tópico anterior. Qual foi
  melhor? Por que uma árvore sozinha, mesmo achando interações, pode perder?

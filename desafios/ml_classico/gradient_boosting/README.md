# Desafio: árvores que corrigem os erros das anteriores

A random forest treina centenas de árvores independentes e tira a média. O gradient boosting faz
diferente: treina árvores pequenas, uma depois da outra, e cada nova árvore tenta corrigir os erros
que as anteriores ainda cometem. É o modelo que mais aparece entre os vencedores de competições com
dados em tabela, mas tem uma diferença importante em relação à floresta: com árvores demais, ele
sobreajusta.

Você vai ver isso acontecer na curva de validação, comparar taxas de aprendizado, usar a parada
antecipada e aproveitar dois recursos do `HistGradientBoostingClassifier`: ele aceita categorias e
valores faltantes sem pré-processamento.

## Os dados

`data/assinaturas.csv`: os mesmos 5 mil clientes dos tópicos anteriores. O alvo é `cancelou`.
Desta vez, plano e canal não viram colunas de 0 e 1: ficam como categorias do pandas.

## O que fazer

Abra o `solucao.py` e implemente as funções, na ordem do arquivo. Cada docstring explica o que a
função recebe e devolve.

## Regras

1. Use pandas, numpy e scikit-learn. Nenhuma função pode alterar o que recebe.
2. Não altere a pasta `tests` nem os arquivos em `data`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 9 testes passam. Os testes treinam vários modelos: rodar todos
leva uns 10 segundos.

## Se travar

1. Rode só um teste: `pytest -v -k curva`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Faça um gráfico da curva de validação, com a iteração no eixo x e a AUC no eixo y, para as
   taxas 0,3 e 0,03. Onde fica o pico de cada uma?
4. Só então consulte o gabarito em `desafios/_gabaritos/ml_classico/gradient_boosting/`.

## Depois de passar

- Treine o boosting com `max_depth=2` e com `max_depth=3`, com parada antecipada. Árvores mais rasas
  precisam de mais iterações? A AUC no teste muda?
- Compare a AUC no teste do boosting, da random forest e da regressão logística, todos no mesmo
  conjunto de teste. Qual você colocaria em produção, e por quê? Pense também em tempo de treino e
  facilidade de explicar.

# Desafio: resumo estatístico de pedidos

Uma loja online exportou os valores de 20 pedidos de um dia (`data/pedidos.csv`). O time comercial
quer saber quanto vale um pedido típico. Antes de responder, você precisa decidir qual medida de
tendência central usar, porque a média pode enganar quando há valores muito fora do comum.

## O que você vai praticar

- Calcular média, mediana e moda sem bibliotecas prontas.
- Detectar valores atípicos pela regra do intervalo interquartil.
- Ler um CSV com pandas.
- Ler a saída de testes automáticos e corrigir o código a partir dela.

## O que fazer

Abra o `solucao.py` e implemente as seis funções. Cada uma tem uma docstring explicando o que
recebe e o que devolve. Sugestão de ordem: `media`, `mediana`, `moda`, `tem_atipico`,
`escolher_medida` e, por último, `resumo_pedidos`.

## Regras

1. Não use o módulo `statistics` nem o `numpy`. O objetivo é entender o cálculo.
2. O pandas só serve para ler o arquivo.
3. Não altere a pasta `tests`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 8 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k test_moda`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Use `print` dentro da função para ver o que ela está calculando.
4. Só então consulte o gabarito em `desafios/_gabaritos/estatistica/tendencia_central/`.

## Depois de passar

Pense na pergunta do time comercial: para esses 20 pedidos, qual é o valor do pedido típico, e por
que a média não é a melhor resposta? Se conseguir explicar em duas frases, você dominou o ponto
central do tópico.

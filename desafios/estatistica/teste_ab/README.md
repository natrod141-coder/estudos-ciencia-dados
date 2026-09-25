# Desafio: o botão novo vende mais?

Uma loja online redesenhou o botão "Finalizar compra" e rodou um teste A/B por duas semanas completas:
metade dos visitantes viu o botão antigo (grupo A) e metade viu o novo (grupo B). A ferramenta de
analytics exportou os resultados por dia (`data/experimento.csv`). O time de produto quer saber se o
botão novo pode ir para todos os clientes. Antes de responder, você precisa conferir se o
experimento foi bem executado, testar a diferença e medir o tamanho do efeito.

## O que você vai praticar

- Calcular taxas de conversão e comparar duas proporções com um teste z.
- Calcular o intervalo de confiança da diferença entre as taxas.
- Calcular o tamanho de amostra necessário antes de começar um teste.
- Detectar uma divisão de tráfego desbalanceada (*sample ratio mismatch*).
- Ver por que olhar o resultado todo dia e parar "quando der significativo" é um erro.

## O que fazer

Abra o `solucao.py` e implemente as oito funções. Cada uma tem uma docstring explicando o que
recebe e o que devolve. Sugestão de ordem: `taxa_conversao`, `teste_duas_proporcoes`,
`intervalo_diferenca`, `tamanho_amostra_por_grupo`, `divisao_balanceada`, `decidir`,
`analisar_experimento` e, por último, `evolucao_do_p`.

## Regras

1. Use `statistics.NormalDist` para a distribuição normal (a constante `NORMAL` já está criada).
2. Não use scipy nem statsmodels. O objetivo é entender cada passo do teste.
3. O pandas só serve para ler e somar os dados do CSV.
4. Não altere a pasta `tests`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 10 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k test_teste_duas_proporcoes`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Atenção à diferença entre o teste e o intervalo: o teste usa a taxa combinada no erro padrão (supõe
   H0), e o intervalo usa a taxa de cada grupo.
4. Só então consulte o gabarito em `desafios/_gabaritos/estatistica/teste_ab/`.

## Depois de passar

1. Rode `evolucao_do_p` e olhe a lista. Quem espiasse no 3º dia teria parado com um resultado
   "significativo". Quem espiasse no 8º teria concluído que não havia diferença. Por que decidir a
   duração antes de começar evita os dois erros?
2. Com `tamanho_amostra_por_grupo(0.10, 0.01)`, quantos visitantes por grupo seriam necessários para
   detectar um aumento de só 1 ponto? Com cerca de 700 visitantes por grupo por dia, quantos dias o
   teste precisaria durar?
3. O intervalo da diferença vai de cerca de 0,3 a 2,0 pontos. Se o botão novo custasse caro para
   manter, esse intervalo mudaria a sua recomendação?

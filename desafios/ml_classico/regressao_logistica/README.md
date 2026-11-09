# Desafio: quem vai cancelar a assinatura

Uma plataforma de cursos por assinatura perde, a cada trimestre, cerca de um em cada quatro
clientes. O time de retenção pode ligar para alguns clientes e oferecer ajuda ou um desconto, mas
não para todos. Ele precisa de uma lista: quem tem mais risco de cancelar?

Você vai treinar uma regressão logística com 5 mil clientes, transformar as probabilidades em
decisões, medir os acertos e os erros, e descobrir por que a acurácia engana neste problema.

## Os dados

`data/assinaturas.csv`, com um cliente por linha. O alvo é `cancelou` (1 se cancelou no
trimestre). As outras colunas: plano (básico, padrão ou premium), canal de aquisição, idade, meses
de assinatura, valor mensal, acessos no último mês, chamados ao suporte, atrasos de pagamento, se
usa o aplicativo e a nota de satisfação, de 1 a 5.

Os mesmos dados aparecem nos próximos tópicos do módulo: árvores, florestas, boosting, validação
cruzada e métricas. Assim, dá para comparar os modelos.

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

O desafio está aprovado quando os 9 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k limiar`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Monte a matriz de confusão à mão para o exemplo do teste: reais 1, 1, 0, 0, 1, 0 e previstos
   1, 0, 1, 0, 1, 0.
4. Só então consulte o gabarito em `desafios/_gabaritos/ml_classico/regressao_logistica/`.

## Depois de passar

- O time de retenção consegue ligar para 300 clientes por trimestre. Que limiar dá uma lista desse
  tamanho? Quantos cancelamentos ela pega?
- Uma ligação custa R$ 15 e um cliente que fica vale R$ 400 no ano. Se metade dos clientes que
  iam cancelar ficar depois da ligação, qual limiar dá mais lucro?
- Escreva, em uma frase, o que significa a razão de chance de `atrasos_pagamento`.

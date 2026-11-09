# Desafio: muitas árvores votando juntas

No tópico anterior, a melhor árvore de decisão chegou perto da regressão logística, mas não passou.
E ela tinha dois problemas: decorava o treino com facilidade e mudava bastante com pequenas mudanças
nos dados. A random forest ataca os dois de uma vez: treina centenas de árvores, cada uma com uma
amostra diferente dos clientes e um sorteio diferente de variáveis, e tira a média.

Você vai comparar a floresta com uma árvore, ver quantas árvores bastam, usar a estimativa fora da
sacola (OOB) no lugar de um conjunto de validação e descobrir que uma das medidas de importância de
variáveis engana.

## Os dados

`data/assinaturas.csv`: os mesmos 5 mil clientes dos tópicos anteriores. O alvo é `cancelou`.

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

O desafio está aprovado quando os 9 testes passam. Os testes treinam várias florestas: rodar todos
leva uns 15 segundos.

## Se travar

1. Rode só um teste: `pytest -v -k oob`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Se `oob_decision_function_` não existir, confira se a floresta foi treinada com
   `oob_score=True`.
4. Só então consulte o gabarito em `desafios/_gabaritos/ml_classico/random_forest/`.

## Depois de passar

- Imprima as duas importâncias lado a lado. Por que a idade aparece no topo de uma e no meio da
  outra?
- Treine a floresta com `min_samples_leaf=1`, o padrão do scikit-learn. A AUC no teste melhora ou
  piora? E a AUC no treino?
- Teste `max_features` com os valores `"sqrt"`, `0.5` e `None`. O que acontece quando cada árvore
  pode olhar todas as variáveis em toda divisão?

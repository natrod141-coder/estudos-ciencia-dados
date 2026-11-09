# Desafio: uma nota que não depende da sorte

Até aqui, todo modelo foi avaliado numa única divisão entre treino e teste. Mas essa divisão é um
sorteio: com outro sorteio, a mesma regressão logística teria outra nota. Quanto outra? E como
escolher entre dois modelos se a diferença entre eles for menor que essa variação?

Você vai medir essa variação, usar a validação cruzada para ter uma estimativa mais firme, ver um
vazamento clássico transformar números sorteados num modelo "ótimo" e escolher os hiperparâmetros
de uma árvore com uma busca em grade, guardando o teste para o fim.

## Os dados

- `data/assinaturas.csv`: os mesmos 5 mil clientes dos tópicos anteriores. A função `preparar` já
  está pronta.
- Para o teste do vazamento, a função `dados_de_ruido`, também pronta, sorteia 300 linhas com 2 mil
  colunas de números e um alvo sorteado: nenhuma coluna tem relação nenhuma com o alvo.

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

1. Rode só um teste: `pytest -v -k selecao`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Depois da busca em grade, olhe `grade.cv_results_` num DataFrame:
   `pd.DataFrame(grade.cv_results_)[["params", "mean_test_score", "std_test_score"]]`.
4. Só então consulte o gabarito em `desafios/_gabaritos/ml_classico/validacao_cruzada/`.

## Depois de passar

- A diferença entre a melhor e a segunda melhor combinação da busca é maior que o desvio padrão
  das notas? Se não for, dá para dizer que uma é melhor que a outra?
- Rode `selecao_antes_de_dividir` com `k=5` e `k=100`. O que acontece com a AUC "inventada"?
- Pense num problema seu, do trabalho ou de estudo: as linhas são independentes, ou há várias
  linhas da mesma pessoa, ou dados ao longo do tempo? Que tipo de divisão ele pede?

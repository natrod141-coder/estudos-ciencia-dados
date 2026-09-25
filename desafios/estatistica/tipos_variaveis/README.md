# Desafio: cada coluna no seu tipo

Uma rede de lojas fez uma pesquisa com 25 clientes (`data/pesquisa.csv`) e pediu um resumo "com a
média de tudo". Só que metade das colunas não aceita média: a cidade é um nome, o CEP é um código e a
satisfação é uma escala de "muito insatisfeito" a "muito satisfeito". Antes de resumir, você precisa
classificar cada variável e ler o arquivo de forma que o pandas trate cada coluna do jeito certo.

## O que você vai praticar

- Classificar variáveis em nominais, ordinais, discretas e contínuas.
- Reconhecer números que não são quantidades, como CEP e códigos.
- Ler um CSV sem perder zeros à esquerda.
- Criar categorias ordenadas no pandas e calcular a mediana de uma variável ordinal.
- Escolher as medidas de resumo que fazem sentido para cada tipo.

## O que fazer

Abra o `solucao.py`, preencha o dicionário `CLASSIFICACAO` e implemente as quatro funções. Cada
função tem uma docstring explicando o que recebe e o que devolve. Sugestão de ordem:
`CLASSIFICACAO`, `medidas_permitidas`, `ler_pesquisa`, `mediana_ordinal` e, por último,
`resumo_central`.

## Regras

1. Use o pandas à vontade: aqui o objetivo é tratar cada tipo de variável do jeito certo.
2. Não altere as listas `ORDEM_ESCOLARIDADE` e `ORDEM_SATISFACAO`.
3. Não altere a pasta `tests`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 8 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k test_ler_pesquisa`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Para ver como o pandas leu cada coluna, rode `print(pesquisa.dtypes)` e `print(pesquisa.head())`.
4. Só então consulte o gabarito em `desafios/_gabaritos/estatistica/tipos_variaveis/`.

## Depois de passar

Na escolaridade, a moda é "médio" e a mediana é "superior". O que cada uma quer dizer para esses 25
clientes? E por que calcular a "média da satisfação" trocando as categorias por 1 a 5 é arriscado?
Se conseguir responder em poucas frases, você dominou o ponto central do tópico.

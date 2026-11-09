# Desafio: do dado cru ao modelo, sem vazamento

Nos tópicos anteriores, a base de assinaturas já vinha pronta: sem vazios, com os meses de
assinatura calculados e poucas categorias. Na vida real, ela chega assim, como em
`data/assinaturas_brutas.csv`:

- a data de início da assinatura, no lugar dos meses de assinatura;
- 8% das idades e 15% das notas de satisfação vazias;
- 47 cidades, sete grandes e quarenta com poucos clientes cada;
- uma coluna `data_cancelamento`, que entrega a resposta.

Você vai encontrar o vazamento, criar as variáveis, montar um pipeline do scikit-learn que prepara
os dados aprendendo só com o treino, e medir o estrago que o vazamento faria se passasse
despercebido.

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

O desafio está aprovado quando os 8 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k preprocessamento`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Depois de treinar o pipeline, explore as etapas: `modelo.named_steps["preparo"]` mostra o
   pré-processamento, e `get_feature_names_out()` mostra as colunas que saem dele.
4. Só então consulte o gabarito em `desafios/_gabaritos/ml_classico/preparacao_variaveis/`.

## Depois de passar

- Imagine que a base tivesse uma coluna `motivo_cancelamento`. Ela seria pega pela função
  `colunas_suspeitas`? E uma coluna `ligacoes_de_retencao`, com o número de ligações que o cliente
  recebeu do time de retenção? Por que essas colunas também vazam?
- Troque o modelo do pipeline por um `HistGradientBoostingClassifier`. Ele precisa do imputador e
  do padronizador? Tire o que não for necessário e compare a AUC.

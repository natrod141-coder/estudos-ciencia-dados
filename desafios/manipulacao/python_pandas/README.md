# Desafio: da base crua à análise

Uma loja online exportou os pedidos do primeiro semestre de 2026 (`data/pedidos.csv`) e o cadastro de
clientes (`data/clientes.csv`). A diretoria quer três respostas: quanto cada estado faturou, como o
faturamento evoluiu mês a mês e quem são os melhores clientes. Antes, você precisa resolver os
problemas da exportação: pedidos repetidos, valores escritos como "n/d", pedidos sem cliente, sem
canal e sem valor.

O desafio tem quatro partes, que seguem o texto do tópico: NumPy, leitura, dados faltantes e
análise.

## O que você vai praticar

- Operações vetorizadas com NumPy: aritmética com arrays, `np.where` e `np.select`.
- Ler CSV com os tipos certos: datas, textos que significam faltante, inteiros com faltantes.
- Diagnosticar dados faltantes e escolher uma regra de tratamento para cada coluna.
- Juntar tabelas com `merge`, agrupar com `groupby` e calcular variações com `pct_change`.

## O que fazer

Abra o `solucao.py` e implemente as doze funções. A `ler_clientes` já está pronta. Siga a ordem do
arquivo: cada parte usa as anteriores.

## Regras

1. Na parte 1, use operações vetorizadas do NumPy: nada de `for` percorrendo os valores.
2. Nas outras partes, evite `for` sobre as linhas do DataFrame: quase sempre existe um método pronto.
3. Nenhuma função pode alterar o DataFrame que recebe: trabalhe numa cópia.
4. Não altere a pasta `tests`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 13 testes passam.

## Se travar

1. Rode só os testes de uma parte: `pytest -v -k faltantes`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Olhe os dados no meio do caminho. Num terminal Python, dentro desta pasta:

   ```python
   import solucao
   pedidos = solucao.ler_pedidos("data/pedidos.csv")
   pedidos.info()
   pedidos.head()
   ```

4. Só então consulte o gabarito em `desafios/_gabaritos/manipulacao/python_pandas/`.

## Depois de passar

Rode `analisar` e leia os resultados como a diretoria leria. O Rio Grande do Sul tem só 2 pedidos:
faz sentido comparar o ticket médio dele com o de São Paulo? Junho caiu 28,6% em relação a maio:
antes de alarmar alguém, o que você verificaria nos dados? Por fim, compare o faturamento total com
e sem os 12 valores imputados. A imputação mudou alguma conclusão?

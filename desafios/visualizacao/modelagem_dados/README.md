# Desafio: da planilha única ao modelo estrela

A rede de lojas guarda as vendas numa planilha única (`data/vendas_planas.csv`): cada linha é um item
vendido, com todos os dados do produto e da loja repetidos em cada venda. Com 853 linhas funciona,
mas o relatório no Power BI está ficando lento, as fórmulas DAX estão confusas, e alguém percebeu que
o Relógio GPS aparece em duas categorias diferentes.

Você vai transformar a planilha num **modelo estrela**: uma tabela fato de vendas, só com chaves e
números, cercada de dimensões de produto, loja e data. É o formato que o Power BI espera, e é a base
do desafio de DAX, a seguir.

```
               dim_produto
                    │ 1
                    │
                    │ *
dim_data ─1───*─ fato_vendas ─*───1─ dim_loja
```

## O que você vai praticar

- Encontrar inconsistências que impedem uma dimensão de ter uma linha por chave.
- Criar dimensões com chaves substitutas.
- Criar uma tabela de calendário completa.
- Separar a tabela fato, só com chaves e medidas numéricas.
- Validar relacionamentos (chave única, linhas órfãs) e a granularidade da fato.

## O que fazer

Abra o `solucao.py` e implemente as oito funções. A `ler_planilha` já está pronta. Sugestão de
ordem: `inconsistencias`, `criar_dim_produto`, `criar_dim_loja`, `criar_calendario`, `criar_fato`,
`validar_relacionamento`, `granularidade_ok` e, por último, `montar_modelo`.

## Regras

1. Use pandas. Nenhuma função pode alterar o DataFrame que recebe.
2. Não altere a pasta `tests` nem o arquivo em `data`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 11 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k calendario`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Olhe o P07 na planilha: `ler_planilha("data/vendas_planas.csv").query("codigo_produto == 'P07'")`.
4. Só então consulte o gabarito em `desafios/_gabaritos/visualizacao/modelagem_dados/`.

## Depois de passar

Exporte as quatro tabelas para CSV e monte o modelo no Power BI Desktop: importe as tabelas, crie os
relacionamentos na exibição de Modelo e marque `dim_data` como tabela de datas. Compare o tamanho do
arquivo `.pbix` com o de um relatório feito sobre a planilha única. Depois, pense no P07: com a
dimensão do tipo 1, o faturamento de 2025 do Relógio GPS aparece em Eletrônicos, embora na época ele
fosse Acessórios. Quando isso seria um problema, e como uma dimensão do tipo 2 resolveria?

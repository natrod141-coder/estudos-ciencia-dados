# Desafio: o Power Query por dentro

Uma rede de lojas de artigos esportivos quer um relatório de vendas contra metas, no Power BI. Todo
mês, o sistema exporta um CSV de vendas para a pasta `data/vendas/`. As metas vêm numa planilha com um
mês por coluna, e o cadastro das lojas fica em outro arquivo. Antes de qualquer gráfico, alguém
precisa preparar esses dados. No Power BI, esse trabalho é feito no **Power Query**.

Neste desafio, você vai fazer em pandas cada etapa que faria no Power Query. O objetivo não é trocar o
Power BI pelo Python: é entender o que cada botão do Power Query faz com os dados, porque é aí que
estão a maior parte do trabalho e a maior parte dos erros de um relatório.

## Os dados

- `data/vendas/vendas_2026_01.csv` a `vendas_2026_03.csv`: uma linha por venda, com data, loja,
  produto, quantidade e valor. Formato brasileiro: ponto e vírgula entre as colunas, vírgula decimal
  e datas dd/mm/aaaa. No arquivo de março, alguns códigos de loja vieram em minúsculas ou com espaços.
- `data/metas.csv`: a meta de faturamento de cada loja, com uma coluna por mês (jan, fev, mar).
- `data/lojas.csv`: código, nome, cidade e região de cada loja.

## O que fazer

Abra o `solucao.py` e implemente as nove funções, na ordem do arquivo. Cada docstring diz a etapa
equivalente no Power Query.

| Função                    | No Power Query                                         |
| ------------------------- | ------------------------------------------------------ |
| `ler_arquivo_vendas`      | Texto/CSV, Alterar Tipo com Localidade                 |
| `combinar_arquivos`       | Obter Dados > Pasta > Combinar; Aparar; MAIÚSCULAS     |
| `despivotar_metas`        | Transformar Outras Colunas em Linhas                   |
| `mesclar_lojas`           | Mesclar Consultas (externa esquerda)                   |
| `adicionar_faixa`         | Coluna Condicional                                     |
| `agrupar_por_loja_e_mes`  | Agrupar Por                                            |
| `realizado_vs_meta`       | Mesclar Consultas e Coluna Personalizada               |
| `cartoes`                 | Os cartões do relatório (no Power BI, medidas DAX)     |
| `montar_relatorio`        | Atualizar                                              |

## Regras

1. Use pandas. Nenhuma função pode alterar o DataFrame que recebe.
2. Não edite os arquivos em `data`.
3. Não altere a pasta `tests`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 10 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k despivotar`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Abra os CSVs num editor de texto para ver o formato exato: separador, decimais, datas.
4. Só então consulte o gabarito em `desafios/_gabaritos/visualizacao/power_bi/`.

## Depois de passar

Faça o mesmo relatório no Power BI Desktop, com os mesmos arquivos: Obter Dados > Pasta, as mesmas
transformações no Power Query, e uma página com os cartões e uma matriz de lojas por mês. Os números
precisam bater com os do seu código. Depois, abra o Editor Avançado do Power Query e compare o código
M gerado pelos cliques com as suas funções em Python: cada etapa do M corresponde a uma linha sua.

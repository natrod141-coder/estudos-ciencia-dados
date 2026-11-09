# Desafio: um projeto dbt para a loja

Os dados brutos do sistema da loja chegaram ao banco: clientes, pedidos e itens de pedido, do jeito
que o sistema exporta. O status dos pedidos foi digitado de vários jeitos, os preços estão em
centavos, e há pedidos de teste da equipe misturados com os de verdade.

Você vai montar o projeto dbt que transforma esses dados em duas tabelas prontas para análise: uma
de pedidos (`fct_pedidos`) e uma de clientes (`dim_clientes`). No caminho, vai escrever modelos de
staging, uma macro e os testes de qualidade que garantem que as tabelas fazem sentido.

## O projeto

```
dbt/
├── carregar_dados.py          carrega os CSVs no banco, no esquema raw (pronto)
├── data/                      os dados brutos, em CSV (pronto)
├── dbt_project.yml            configuração do projeto (pronto)
├── profiles.yml               conexão com o banco DuckDB (pronto)
├── seeds/uf_regiao.csv        região de cada estado (pronto)
├── macros/
│   └── centavos_para_reais.sql    você escreve
├── models/
│   ├── staging/
│   │   ├── _fontes.yml            as fontes de dados brutos (pronto)
│   │   ├── stg_clientes.sql       exemplo pronto
│   │   ├── stg_pedidos.sql        você escreve
│   │   └── stg_itens.sql          você escreve
│   └── marts/
│       ├── fct_pedidos.sql        você escreve
│       ├── dim_clientes.sql       você escreve
│       └── _marts.yml             você acrescenta os testes
├── testes_dbt/                teste singular do dbt (pronto)
└── tests/                     testes do pytest, que conferem o desafio (não altere)
```

Cada arquivo que você escreve começa com um comentário que diz exatamente o que ele precisa ter:
as colunas, a ordem e as regras.

## O que fazer

Todos os comandos rodam no terminal, dentro desta pasta.

1. Carregue os dados brutos no banco. Isso cria o arquivo `loja.duckdb`, com as tabelas no esquema
   `raw`. Num projeto de verdade, quem faz esse papel é uma ferramenta de ingestão.

   ```
   python carregar_dados.py
   ```

2. Leia `models/staging/stg_clientes.sql`, o exemplo pronto, e rode o projeto pela primeira vez.
   Os modelos que você ainda não escreveu vão dar erro, e tudo bem.

   ```
   dbt build
   ```

3. Escreva, nesta ordem: a macro, `stg_pedidos`, `stg_itens`, `fct_pedidos` e `dim_clientes`.
   Depois de cada um, rode `dbt build` de novo e leia o resultado.
4. Acrescente os testes de qualidade em `models/marts/_marts.yml` e rode `dbt build` mais uma vez:
   os testes rodam junto com os modelos.
5. Confira o desafio com o pytest. Ele roda o projeto num banco separado e examina as tabelas:

   ```
   pytest -v
   ```

O desafio está aprovado quando os 10 testes passam.

## Regras

1. Leia outros modelos e o seed sempre com `ref`, e os dados brutos com `source`. Nunca escreva o
   nome de uma tabela direto no SQL.
2. Não altere `dbt_project.yml`, `profiles.yml`, `carregar_dados.py`, os dados, o teste singular nem
   a pasta `tests`.

## Se travar

1. Rode só os testes de uma parte: `pytest -v -k fct`.
2. Veja o SQL que o dbt gerou a partir do seu modelo, com o `ref` e a macro já trocados pelos nomes
   reais: `dbt compile --select fct_pedidos`.
3. Olhe o que ficou numa tabela:

   ```
   python -c "import duckdb; print(duckdb.connect('loja.duckdb').sql('select * from fct_pedidos').df())"
   ```

4. Repare nos detalhes dos dados brutos: o status escrito de jeitos diferentes, o cliente 0, os
   preços em centavos, o pedido 106 sem nenhum item e a cliente 7, que nunca comprou.
5. Só então consulte o gabarito em `desafios/_gabaritos/analytics_eng/dbt/`.

## Sobre as versões do dbt

O `requirements.txt` instala o dbt v1 (o dbt Core, escrito em Python) com o adaptador do DuckDB, e é
com ele que os testes rodam. O mesmo projeto também roda no dbt v2, lançado em setembro de 2026: a
linguagem do projeto (modelos, `ref`, `source`, macros, testes e os arquivos YAML) é a mesma, e os
comandos também.

## Depois de passar

Escreva um teste singular novo em `testes_dbt/`: nenhum pedido aprovado pode ter `valor_total` zero.
Rode `dbt build`. O teste passa? Depois, mude o status do pedido 112 em `data/pedidos.csv` para
`estornado`, rode `python carregar_dados.py` e `dbt build` de novo, e veja qual teste pega o
problema. Desfaça a mudança no fim.

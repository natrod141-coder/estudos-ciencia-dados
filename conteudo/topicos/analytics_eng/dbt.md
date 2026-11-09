---
titulo: "dbt"
modulo: analytics_eng
ordem: 1
horas: 10
estado: publicado
resumo: "Transformar dados com SQL versionado: modelos, camadas, ref e documentação."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Analytics engineering e onde o dbt entra"
    tipo: leitura
    minutos: 12
  - id: a2
    titulo: "Um projeto dbt: modelos, source e ref"
    tipo: leitura
    minutos: 15
  - id: a3
    titulo: "Camadas: staging, intermediate e marts"
    tipo: leitura
    minutos: 12
  - id: a4
    titulo: "Materializações e modelos incrementais"
    tipo: leitura
    minutos: 12
  - id: a5
    titulo: "Testes e documentação"
    tipo: leitura
    minutos: 15
  - id: a6
    titulo: "Jinja, macros e pacotes"
    tipo: leitura
    minutos: 12
  - id: a7
    titulo: "Rodar o projeto: build, seleção e ambientes"
    tipo: leitura
    minutos: 10
  - id: a8
    titulo: "Vídeo de apoio: primeiro projeto com dbt"
    tipo: video
    minutos: 30
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Num fluxo ELT, qual é o papel do dbt?"
    opcoes: ["Extrair os dados dos sistemas de origem", "Carregar arquivos CSV no banco", "Transformar, com SQL, os dados que já estão no banco, criando tabelas e views prontas para análise", "Desenhar os gráficos do painel"]
    correta: 2
    explicacao: "O dbt cuida do T do ELT. A extração e a carga ficam com ferramentas de ingestão. O dbt parte dos dados brutos que já estão no banco e cria, com consultas SELECT, as tabelas e views que o BI e as análises usam."
  - pergunta: "Por que escrever {{ ref('stg_pedidos') }} em vez de main.stg_pedidos no SQL de um modelo?"
    opcoes: ["Porque o ref registra a dependência entre os modelos, o que define a ordem de execução, e troca o nome pelo esquema certo de cada ambiente", "Porque o ref deixa a consulta mais rápida", "Porque o DuckDB não aceita nomes com ponto", "Porque o ref copia a tabela para uma pasta local"]
    correta: 0
    explicacao: "Com o ref, o dbt monta o grafo de dependências: sabe que stg_pedidos precisa rodar antes de fct_pedidos. Também resolve o nome completo da tabela no ambiente em uso, como o seu esquema de desenvolvimento ou o de produção, sem você mudar o código."
  - pergunta: "Para que serve declarar as tabelas brutas como fontes e lê-las com source?"
    opcoes: ["Para o dbt apagar as tabelas brutas depois de usar", "Para converter as tabelas brutas em CSV", "Para deixar as consultas mais curtas", "Para documentar de onde os dados vêm, ligar a linhagem desde a origem e permitir conferir se a fonte está atualizada"]
    correta: 3
    explicacao: "As fontes são as tabelas que outras ferramentas carregaram no banco. Declarando-as em YAML, elas aparecem no grafo e na documentação, ganham testes e podem ter a atualização conferida com dbt source freshness."
  - pergunta: "O que costuma ficar num modelo de staging?"
    opcoes: ["Joins entre várias fontes e as regras de negócio do relatório", "Uma tabela bruta por modelo, com colunas renomeadas, tipos convertidos e limpezas simples", "Só as colunas que o painel usa, já agregadas por mês", "Os gráficos prontos"]
    correta: 1
    explicacao: "Staging é a camada de preparação: um modelo para cada tabela bruta, que padroniza nomes, tipos e valores. Joins e regras de negócio ficam nas camadas seguintes, intermediate e marts."
  - pergunta: "Um modelo recria todo dia uma tabela de 2 bilhões de eventos, e a execução leva horas, embora só entrem alguns milhões de linhas novas por dia. Qual materialização resolve?"
    opcoes: ["view", "ephemeral", "incremental", "seed"]
    correta: 2
    explicacao: "Um modelo incremental processa só as linhas novas, ou alteradas, e as acrescenta à tabela que já existe, em vez de recriar tudo. A view não guarda dados e recalcularia tudo a cada consulta. Seed é para CSVs pequenos."
  - pergunta: "Depois de uma mudança num join, o faturamento da fct_pedidos dobrou. Que teste do dbt teria acusado o problema?"
    opcoes: ["unique na coluna pedido_id, porque uma tabela com uma linha por pedido não pode repetir o pedido", "not_null na coluna status", "accepted_values na coluna regiao", "Nenhum, testes do dbt não olham os dados"]
    correta: 0
    explicacao: "Um join que multiplica linhas repete o mesmo pedido. O teste unique na chave da tabela falha assim que isso acontece, antes de o número dobrado chegar ao painel."
  - pergunta: "O que o teste relationships, aplicado à coluna cliente_id da fct_pedidos e apontando para dim_clientes, confere?"
    opcoes: ["Se cada cliente tem pelo menos um pedido", "Se cliente_id não tem valores vazios", "Se não há clientes repetidos na dim_clientes", "Se todo cliente_id da fct_pedidos existe na dim_clientes"]
    correta: 3
    explicacao: "É o teste de integridade referencial: procura pedidos que apontam para um cliente que não existe. No desafio, ele pega os pedidos do cliente de teste que escaparem do filtro."
  - pergunta: "Vários modelos convertem centavos para reais com a mesma expressão. Qual recurso do dbt evita repetir esse trecho?"
    opcoes: ["Uma macro, escrita uma vez e chamada em cada modelo", "Um seed com os valores convertidos", "Um teste singular", "Uma fonte nova"]
    correta: 0
    explicacao: "Macros são funções em Jinja que geram SQL. A regra fica num lugar só: se mudar, muda em todos os modelos que a usam."
  - pergunta: "Qual é a diferença entre dbt run e dbt build?"
    opcoes: ["Nenhuma, são nomes diferentes para o mesmo comando", "dbt run roda só os testes", "dbt build roda seeds, modelos, snapshots e testes na ordem do grafo, e não constrói o que depende de um modelo cujo teste falhou", "dbt build só compila o SQL, sem rodar"]
    correta: 2
    explicacao: "O dbt run só cria os modelos. O dbt build faz tudo, na ordem do grafo, e testa cada modelo logo depois de criá-lo. Se um teste falhar, o que vem depois não é construído em cima de dados com problema."
  - pergunta: "O dbt v2 foi lançado em setembro de 2026. O que muda para um projeto escrito no dbt v1?"
    opcoes: ["Tudo: os modelos precisam ser reescritos em outra linguagem", "A linguagem do projeto continua a mesma; o v2 é mais rápido e mais rigoroso, e acusa como erro configurações erradas que o v1 deixava passar", "O v2 não aceita mais o ref nem o source", "O v2 só funciona na nuvem, com assinatura"]
    correta: 1
    explicacao: "Modelos, ref, source, macros, testes e YAML continuam iguais. O motor novo valida o projeto com mais rigor: chaves de YAML desconhecidas ou configurações com erro de digitação, que o v1 ignorava em silêncio, viram erro."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Um colega mantém um script SQL de 600 linhas que gera a tabela de pedidos usada no painel, e roda o script à mão toda manhã. Explique como você reorganizaria esse trabalho num projeto dbt e o que o time ganharia com isso."
  rubrica:
    - "Divide o script em camadas ligadas por ref: fontes declaradas, um modelo de staging por tabela bruta (nomes, tipos e limpeza) e modelos de marts com a regra de negócio, como fct_pedidos e dim_clientes."
    - "Acrescenta testes de qualidade, como unique, not_null, relationships e accepted_values, e descrições das colunas, e roda tudo com dbt build, que não constrói o que depende de um teste que falhou."
    - "Cita ganhos concretos: histórico e revisão das mudanças no Git, ordem de execução automática pelo grafo, reaproveitamento com macros e modelos, ambientes separados de desenvolvimento e produção, e execução agendada em vez de manual."
  modelo: "Primeiro, eu declararia as tabelas brutas que o script lê como fontes, num arquivo YAML. Depois quebraria as 600 linhas em modelos pequenos. Na camada de staging, um modelo para cada tabela bruta, só renomeando colunas, convertendo tipos e limpando valores, como o status escrito de vários jeitos. Na camada de marts, a regra de negócio: uma fct_pedidos com uma linha por pedido e uma dim_clientes com uma linha por cliente. Os modelos se ligariam com ref, e o dbt descobriria sozinho a ordem de execução. Trechos repetidos, como a conversão de centavos, virariam macros. Em seguida, eu escreveria testes: unique e not_null na chave de cada tabela, relationships entre pedidos e clientes, accepted_values no status. Junto com os testes, as descrições das colunas, que viram documentação com o grafo de linhagem. Tudo rodaria com dbt build, que testa cada modelo assim que ele é criado e não constrói o que vem depois quando um teste falha. O time ganharia histórico e revisão de cada mudança no Git, um ambiente de desenvolvimento separado do de produção, a execução agendada em vez de manual e, principalmente, a confiança de que um join errado ou um status novo é pego pelos testes antes de chegar ao painel."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Um projeto dbt para a loja"
  descricao: "Os dados brutos da loja chegaram ao banco com o status digitado de vários jeitos, preços em centavos e pedidos de teste misturados aos de verdade. Você vai escrever os modelos de staging, uma macro, a tabela de pedidos e a de clientes, e os testes de qualidade, num projeto dbt de verdade, rodando no DuckDB."
  pasta: "desafios/analytics_eng/dbt"
  testes: 10
  tempo: "3 h"
  ferramentas: "VS Code, Python 3.11 ou superior, dbt com DuckDB e pytest"
  entrega: "Pull Request no GitHub"
  passos:
    - titulo: "Clone o repositório"
      descricao: "Só na primeira vez. Se já clonou, pule para o passo 2."
      comandos:
        - "git clone https://github.com/[seu_usuario]/[repositorio].git"
        - "cd [repositorio]"
    - titulo: "Abra o repositório no VS Code"
      descricao: "Se o VS Code oferecer Reopen in Container, aceite: o ambiente já vem pronto e você pode pular o passo 3."
      comandos:
        - "code ."
    - titulo: "Crie e ative o ambiente virtual"
      descricao: "Abra o terminal do VS Code com Ctrl+` (acento grave). O requirements.txt já instala o dbt e o adaptador do DuckDB. Depois use Ctrl+Shift+P, Python: Select Interpreter, e escolha o .venv."
      comandos:
        - "# Linux ou macOS"
        - "python3 -m venv .venv"
        - "source .venv/bin/activate"
        - "# Windows (PowerShell)"
        - "python -m venv .venv"
        - '.venv\Scripts\Activate.ps1'
        - "pip install -r desafios/requirements.txt"
    - titulo: "Carregue os dados brutos e rode o projeto uma vez"
      descricao: "Leia o README.md da pasta. Os modelos que você ainda não escreveu vão dar erro no primeiro dbt build, e tudo bem."
      comandos:
        - "cd desafios/analytics_eng/dbt"
        - "python carregar_dados.py"
        - "dbt build"
    - titulo: "Escreva a macro, os modelos e os testes"
      descricao: "Cada arquivo começa com um comentário que diz as colunas e as regras. Rode dbt build depois de cada um. Não altere a pasta tests."
      codigo: true
      comandos:
        - "macros/centavos_para_reais.sql"
        - "models/staging/stg_pedidos.sql"
        - "models/staging/stg_itens.sql"
        - "models/marts/fct_pedidos.sql"
        - "models/marts/dim_clientes.sql"
        - "models/marts/_marts.yml"
    - titulo: "Confira com os testes"
      descricao: "O pytest roda o projeto num banco separado e examina as tabelas, o grafo e os testes do dbt."
      comandos:
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/dbt"
        - "git add macros models"
        - 'git commit -m "Resolve o desafio de dbt"'
        - "git push -u origin desafio/dbt"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Engenharia de analytics", en: "analytics engineering" }
  - { pt: "Modelo", en: "model" }
  - { pt: "Fonte", en: "source" }
  - { pt: "Grafo de dependências", en: "DAG (directed acyclic graph)" }
  - { pt: "Linhagem dos dados", en: "data lineage" }
  - { pt: "Materialização", en: "materialization" }
  - { pt: "Modelo incremental", en: "incremental model" }
  - { pt: "Tabela fato", en: "fact table" }
  - { pt: "Tabela dimensão", en: "dimension table" }
  - { pt: "Teste genérico", en: "generic data test" }
  - { pt: "Teste singular", en: "singular data test" }
  - { pt: "Teste unitário", en: "unit test" }
  - { pt: "Macro", en: "macro" }
  - { pt: "Pacote", en: "package" }
  - { pt: "Ambiente de desenvolvimento e de produção", en: "dev and prod targets" }
---

## Analytics engineering e onde o dbt entra

Na maior parte das empresas, os dados chegam ao banco analítico por um caminho chamado **ELT**: *extract*, *load*, *transform*. Ferramentas de ingestão extraem os dados dos sistemas de origem, como o ERP, o site e o CRM, e carregam tudo do jeito que veio num banco como BigQuery, Snowflake, Databricks ou, para projetos locais, DuckDB. Só depois, já dentro do banco, os dados brutos são transformados nas tabelas que os painéis e as análises usam.

Durante muito tempo, essa transformação foi feita com scripts SQL soltos: um arquivo grande, rodado à mão, que alguém precisava lembrar de executar na ordem certa. Sem testes, sem histórico de mudanças, com a mesma regra copiada em vários lugares, e ninguém sabia dizer de onde vinha cada número.

O **dbt** organiza essa etapa, o T do ELT. Cada transformação vira um **modelo**: um arquivo `.sql` com uma consulta SELECT. O dbt descobre a ordem em que os modelos precisam rodar, cria as tabelas e views no banco, roda os testes de qualidade e gera a documentação. E, como tudo é texto, o projeto fica no Git, com revisão de código e histórico, como qualquer software.

Daí vem o nome da função que cuida dessa camada: **analytics engineering**, que fica entre a engenharia de dados, que traz os dados até o banco, e a análise, que usa as tabelas prontas. É quem define, em código testado, o que é um "pedido aprovado" ou o "faturamento do mês".

Um ponto de atualização. Em setembro de 2026, a dbt Labs lançou o **dbt v2**, com um motor novo, bem mais rápido e mais rigoroso na validação do projeto, e ele passou a ser a instalação padrão. A geração anterior, o **dbt v1**, ou dbt Core, escrita em Python, continua com suporte: a versão 1.12 tem suporte ativo até julho de 2027. Para você, o importante é que **a linguagem do projeto é a mesma nas duas**: modelos, `source`, `ref`, macros, testes e arquivos YAML. O desafio deste tópico usa o v1, que o `requirements.txt` instala junto com o resto, e foi testado também no v2. A dbt Labs ainda oferece um serviço pago na nuvem, a dbt platform, antes chamada dbt Cloud, com editor, agendamento e outros recursos.

## Um projeto dbt: modelos, source e ref

Um projeto dbt é uma pasta com alguns arquivos de configuração e pastas de código:

- `dbt_project.yml`: o nome do projeto, onde fica cada tipo de arquivo e as configurações padrão.
- `profiles.yml`: como se conectar ao banco. Costuma ficar fora do projeto, na pasta `~/.dbt/` de cada pessoa, porque guarda credenciais. No desafio, fica na pasta do projeto, porque o DuckDB é só um arquivo local.
- `models/`: os modelos, em SQL, e os arquivos YAML que os descrevem.
- `seeds/`: arquivos CSV pequenos, que o dbt carrega como tabelas.
- `macros/`: trechos de SQL reaproveitáveis, escritos em Jinja.

Um modelo é só uma consulta. Este é o `stg_pedidos` do desafio:

```sql
select
    id as pedido_id,
    id_cliente as cliente_id,
    cast(criado_em as date) as data_pedido,
    lower(trim(status)) as status
from {{ source('loja', 'pedidos') }}
where id_cliente <> 0  -- pedidos de teste da equipe
```

Você não escreve `CREATE TABLE` nem `CREATE VIEW`: o dbt cuida disso. O trecho entre chaves duplas é **Jinja**, a linguagem de modelos que o dbt usa para gerar o SQL final.

A função **`source`** lê uma tabela bruta, carregada no banco por outra ferramenta. As fontes são declaradas em YAML:

```yaml
sources:
  - name: loja
    schema: raw
    tables:
      - name: clientes
      - name: pedidos
      - name: itens_pedido
```

Declarar as fontes documenta de onde os dados vêm, permite testá-las e permite conferir se estão atualizadas, com o comando `dbt source freshness`.

A função **`ref`** lê outro modelo, ou um seed. É a peça mais importante do dbt, e faz duas coisas. Primeiro, registra a dependência: se `fct_pedidos` usa `ref('stg_pedidos')`, o dbt sabe que precisa criar `stg_pedidos` antes. Segundo, troca o nome pelo endereço completo da tabela no ambiente em uso. Compare o que você escreve com o que o dbt envia ao banco, que fica em `target/compiled/`:

```sql
-- o que você escreve
from {{ ref('stg_pedidos') }} as p

-- o que o dbt envia ao banco
from "loja"."main"."stg_pedidos" as p
```

Juntando todos os `source` e `ref`, o dbt monta o **grafo de dependências** do projeto, e roda cada modelo depois dos que ele usa. No desafio, o grafo fica assim:

```text
fontes        staging          marts
pedidos    -> stg_pedidos  ->  fct_pedidos -> dim_clientes
itens      -> stg_itens    ->  fct_pedidos
clientes   -> stg_clientes ->  fct_pedidos e dim_clientes
seed uf_regiao             ->  fct_pedidos e dim_clientes
```

Os **seeds** servem para tabelas pequenas e estáveis, que fazem sentido versionar junto com o código: a região de cada estado, um de-para de categorias, a lista de feriados. Não servem para carregar dados brutos grandes: isso é trabalho da ferramenta de ingestão.

## Camadas: staging, intermediate e marts

Um projeto dbt bem organizado separa os modelos em camadas, cada uma com um papel:

- **Staging** (`stg_`): um modelo para cada tabela bruta. Renomeia colunas, converte tipos, padroniza valores, tira linhas de teste. Não faz joins nem aplica regra de negócio. Costuma ser view.
- **Intermediate** (`int_`): passos de lógica reaproveitáveis entre o staging e os marts, como um join usado por vários modelos. É opcional: projetos pequenos não precisam.
- **Marts**: as tabelas prontas para consumo, organizadas por área de negócio. Seguem a modelagem dimensional que você viu no tópico de modelagem de dados: tabelas **fato** (`fct_`), com um evento por linha, como um pedido, e tabelas **dimensão** (`dim_`), com uma entidade por linha, como um cliente. É nelas que o BI se conecta.

O ponto que mais exige atenção nos marts é a **granularidade**: o que é uma linha de cada tabela. A `fct_pedidos` tem uma linha por pedido, mas os itens têm uma linha por item. Juntar pedidos com itens antes de agregar repete cada pedido uma vez por item, o mesmo erro de fan-out do tópico de conferir código gerado por IA. Por isso, no desafio, os itens são agrupados por pedido antes do join:

```sql
with itens_por_pedido as (
    select
        pedido_id,
        sum(quantidade) as unidades,
        sum(valor_item) as valor_total
    from {{ ref('stg_itens') }}
    group by pedido_id
)

select p.pedido_id, p.status, i.valor_total
from {{ ref('stg_pedidos') }} as p
left join itens_por_pedido as i on i.pedido_id = p.pedido_id
```

Escreva a granularidade na descrição de cada modelo, como "uma linha por pedido". Ela orienta quem usa a tabela e diz qual teste de unicidade a tabela precisa ter.

## Materializações e modelos incrementais

A **materialização** define como o dbt cria o modelo no banco:

- `view`: o padrão. Não guarda dados, roda a consulta a cada uso. Boa para staging.
- `table`: guarda o resultado. Recriada a cada execução. Boa para marts, que são consultados muitas vezes.
- `incremental`: guarda o resultado e, nas execuções seguintes, processa só as linhas novas.
- `ephemeral`: não cria nada no banco; o SQL entra como CTE nos modelos que o usam.

A configuração pode valer para uma pasta inteira, no `dbt_project.yml`, ou para um modelo só, no começo do arquivo:

```yaml
models:
  loja:
    staging:
      +materialized: view
    marts:
      +materialized: table
```

```sql
{{ config(materialized='table') }}
```

Os modelos **incrementais** existem para tabelas grandes que crescem todo dia, como eventos de um site. Recriar 2 bilhões de linhas para acrescentar alguns milhões é desperdício. O modelo incremental processa só o que chegou:

```sql
{{ config(materialized='incremental', unique_key='pedido_id') }}

select pedido_id, cliente_id, data_pedido, status
from {{ ref('stg_pedidos') }}

{% if is_incremental() %}
-- da segunda execução em diante: só o último dia e os novos
where data_pedido >= (select max(data_pedido) from {{ this }})
{% endif %}
```

Na primeira execução, a condição `is_incremental()` é falsa e o dbt cria a tabela inteira. Nas seguintes, o filtro entra, e `{{ this }}` aponta para a própria tabela já existente. Com `unique_key`, o dbt apaga e reinsere as linhas que vieram de novo, em vez de duplicá-las. O filtro com `>=` reprocessa o último dia de propósito, para pegar pedidos que chegaram atrasados. Quando a lógica do modelo muda, rode `dbt build --full-refresh` para recriar a tabela do zero.

Há ainda os **snapshots**, que guardam o histórico de linhas que mudam com o tempo, como o endereço de um cliente: a cada execução, o dbt registra a versão nova e mantém a antiga, com as datas de validade de cada uma.

## Testes e documentação

Os testes do dbt são consultas que procuram problemas nos dados. Os **testes genéricos** são declarados em YAML, coluna por coluna:

```yaml
models:
  - name: fct_pedidos
    description: "Uma linha por pedido."
    columns:
      - name: pedido_id
        data_tests:
          - unique
          - not_null
      - name: cliente_id
        data_tests:
          - relationships:
              arguments:
                to: ref('dim_clientes')
                field: cliente_id
      - name: status
        data_tests:
          - accepted_values:
              arguments:
                values: ["aprovado", "cancelado", "pendente"]
```

Os quatro que vêm com o dbt cobrem os problemas mais comuns:

- `unique`: a coluna não tem valores repetidos. Na chave de uma tabela, pega joins que multiplicam linhas.
- `not_null`: a coluna não tem valores vazios.
- `accepted_values`: a coluna só tem os valores da lista. Pega um status novo que ninguém tratou.
- `relationships`: todo valor da coluna existe na coluna de outra tabela. É a integridade referencial.

Os **testes singulares** são arquivos SQL que devolvem as linhas com problema. O teste passa quando a consulta não devolve nenhuma linha:

```sql
select pedido_id, valor_total
from {{ ref('fct_pedidos') }}
where valor_total < 0
```

Dois detalhes de versão. A chave passou a se chamar `data_tests` no dbt 1.8 (a forma antiga, `tests`, ainda funciona), e os parâmetros dos testes ficam dentro de `arguments`, a forma atual, aceita pelo v1 e pelo v2. Desde a versão 1.8, o dbt também tem **testes unitários**, que conferem a lógica de um modelo com poucas linhas de entrada escritas à mão, antes de rodar sobre os dados de verdade.

As descrições nos arquivos YAML viram **documentação**. O comando `dbt docs generate` monta um site com cada modelo, suas colunas, seus testes e o grafo de linhagem, e `dbt docs serve` abre esse site no navegador. O próximo tópico vai mais fundo em testes de qualidade.

## Jinja, macros e pacotes

O Jinja tem dois tipos de marcação: `{{ ... }}` para inserir um valor e `{% ... %}` para lógica, como condições e laços. Um laço pode gerar colunas repetitivas:

```sql
select
    cliente_id,
    {% for status in ['aprovado', 'cancelado', 'pendente'] %}
    count(case when status = '{{ status }}' then 1 end)
        as pedidos_{{ status }},
    {% endfor %}
    count(*) as pedidos
from {{ ref('fct_pedidos') }}
group by cliente_id
```

Uma **macro** é uma função em Jinja que devolve SQL. A regra fica escrita num lugar só, e todos os modelos que a chamam mudam juntos:

```sql
{% macro centavos_para_reais(expressao) %}
    round(({{ expressao }}) / 100.0, 2)
{% endmacro %}
```

```sql
select
    produto,
    {{ centavos_para_reais('preco_unitario_centavos') }}
        as preco_unitario
from {{ source('loja', 'itens_pedido') }}
```

Os **pacotes** trazem macros e testes prontos, escritos pela comunidade. O mais usado é o `dbt_utils`. Declare o pacote num arquivo `packages.yml` e rode `dbt deps` para instalá-lo:

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: [">=1.3.0", "<2.0.0"]
```

Use o Jinja com moderação: SQL cheio de laços e condições fica difícil de ler e de revisar. Se uma consulta simples resolve, ela é melhor.

## Rodar o projeto: build, seleção e ambientes

Os comandos do dia a dia, sempre de dentro da pasta do projeto:

```bash
dbt build          # seeds, modelos e testes, em ordem
dbt run            # só cria os modelos, sem testar
dbt test           # só roda os testes
dbt compile        # gera o SQL final em target/, sem rodar
dbt docs generate  # gera o site de documentação

dbt build --select fct_pedidos   # um modelo e os testes dele
dbt build --select stg_pedidos+  # o modelo e os descendentes
dbt build --select +fct_pedidos  # o modelo e os ancestrais
```

O `dbt build` é o comando principal: testa cada modelo logo depois de criá-lo e, se um teste falhar, não constrói o que depende daquele modelo. Assim, um problema nos dados para no meio do caminho, em vez de chegar ao painel.

Com o sinal de mais, o `--select` percorre o grafo: depois do nome, pega os descendentes; antes, os ancestrais. Rodar só uma parte do projeto economiza tempo enquanto você desenvolve, desde que os modelos de que ela depende já existam no banco.

Num time, cada pessoa desenvolve no seu próprio **ambiente**, um esquema separado no banco, definido como um `target` no `profiles.yml`. O ambiente de produção é o que os painéis leem, e roda de forma agendada, por um orquestrador como Airflow, Dagster ou GitHub Actions, ou pela dbt platform. Como o `ref` resolve os nomes conforme o ambiente, o mesmo código roda em desenvolvimento e em produção sem nenhuma mudança. E, num Pull Request, a integração contínua pode rodar `dbt build` só nos modelos alterados e nos que dependem deles, para que nada quebrado chegue à produção.

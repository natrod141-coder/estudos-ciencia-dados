---
titulo: "Modelagem de dados"
modulo: visualizacao
ordem: 2
horas: 5
estado: publicado
resumo: "Tabelas fato e dimensão, relacionamentos e esquema estrela."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Por que modelar: o problema da planilha única"
    tipo: leitura
    minutos: 8
  - id: a2
    titulo: "Fatos e dimensões"
    tipo: leitura
    minutos: 12
  - id: a3
    titulo: "Esquema estrela e relacionamentos"
    tipo: leitura
    minutos: 15
  - id: a4
    titulo: "A tabela de calendário"
    tipo: leitura
    minutos: 10
  - id: a5
    titulo: "Granularidade, chaves e dimensões que mudam"
    tipo: leitura
    minutos: 12
  - id: a6
    titulo: "Vídeo de apoio: modelo estrela no Power BI"
    tipo: video
    minutos: 20
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Numa análise de vendas, qual destas tabelas é uma tabela fato?"
    opcoes: ["Produtos, com nome, categoria e marca", "Vendas, com data, chave do produto, chave da loja, quantidade e valor", "Lojas, com nome, cidade e estado", "Calendário, com uma linha por dia"]
    correta: 1
    explicacao: "A tabela fato registra os eventos que se quer medir, no caso as vendas, com as chaves que as ligam às dimensões e os números que serão somados. As dimensões descrevem o contexto: o quê (produto), onde (loja) e quando (calendário)."
  - pergunta: "O que caracteriza um esquema estrela?"
    opcoes: ["Todas as informações numa única tabela larga", "Dimensões ligadas umas às outras em cadeia, sem tabela central", "Uma tabela fato no centro, ligada diretamente a cada dimensão por relacionamentos um-para-muitos", "Uma tabela por mês de dados"]
    correta: 2
    explicacao: "No esquema estrela, cada dimensão se liga direto à fato, e o desenho lembra uma estrela. Quando uma dimensão é quebrada em outras, como produto ligado a categoria, o esquema vira um floco de neve. O Power BI funciona melhor com a estrela: menos relacionamentos, filtros mais previsíveis e DAX mais simples."
  - pergunta: "No Power BI, qual é a direção de filtro recomendada nos relacionamentos entre uma dimensão e a fato?"
    opcoes: ["Bidirecional em todos os relacionamentos", "Da fato para a dimensão", "Nenhuma, os relacionamentos não filtram", "Única, da dimensão para a fato"]
    correta: 3
    explicacao: "Com a direção única, um filtro na dimensão, como uf = 'PR', desce para a fato e filtra as vendas. Filtros bidirecionais fazem a fato filtrar a dimensão também. Isso pode criar ambiguidade quando há vários caminhos entre tabelas e deixa o modelo mais lento. Use bidirecional só quando houver um motivo claro."
  - pergunta: "Por que criar uma tabela de calendário, em vez de usar só a coluna de data da fato?"
    opcoes: ["Porque as funções de inteligência de tempo do DAX precisam de uma tabela de datas contínua, e porque ela concentra atributos como mês, trimestre e dia útil", "Porque a fato não pode ter colunas de data", "Porque o Power BI não aceita datas na fato", "Porque o calendário deixa o modelo menor que a fato"]
    correta: 0
    explicacao: "A coluna de data da fato tem buracos: dias sem venda não aparecem. Funções como TOTALYTD e SAMEPERIODLASTYEAR precisam de todas as datas, em anos completos. O calendário também guarda os atributos de data num lugar só, e pode ser compartilhado por várias fatos."
  - pergunta: "O que é a granularidade de uma tabela fato?"
    opcoes: ["A quantidade de colunas da tabela", "O que uma linha da tabela representa, como um item de um pedido ou o total de um dia por loja", "O nível de detalhe dos gráficos do relatório", "O tamanho do arquivo"]
    correta: 1
    explicacao: "Definir a granularidade é o primeiro passo de qualquer modelo. Ela diz o que pode ser analisado: com uma linha por item de pedido, dá para ver produtos; com o total diário por loja, não. Tabelas de granularidades diferentes, como vendas por item e metas por loja e mês, viram fatos separadas."
  - pergunta: "Um produto mudou de categoria. Para que as vendas antigas continuem na categoria antiga e as novas apareçam na nova, que tipo de dimensão usar?"
    opcoes: ["Tipo 1, sobrescrevendo a categoria", "Tipo 0, ignorando a mudança", "Nenhuma, basta filtrar por data", "Tipo 2, criando uma nova linha para o produto, com nova chave substituta e datas de validade"]
    correta: 3
    explicacao: "Na dimensão do tipo 1, o atributo é sobrescrito, e todo o histórico passa a aparecer na categoria nova. No tipo 2, cada versão do produto vira uma linha, com sua própria chave substituta. As vendas antigas apontam para a versão antiga, e as novas para a nova. O tipo 2 guarda o histórico, mas deixa a dimensão maior e a carga mais complexa."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Um colega importou para o Power BI uma única tabela de vendas com 40 colunas, incluindo nome e cidade do cliente, categoria e marca do produto e a data. Explique por que um modelo estrela seria melhor e descreva as tabelas que você criaria."
  rubrica:
    - "Explica as vantagens do modelo estrela: dados descritivos guardados uma vez só, modelo menor e mais rápido, fórmulas DAX mais simples e filtros previsíveis a partir das dimensões."
    - "Descreve uma tabela fato com chaves e números (data, chave do cliente, chave do produto, quantidade, valor) e dimensões de cliente, produto e calendário, ligadas por relacionamentos um-para-muitos."
    - "Define a granularidade da fato (por exemplo, uma linha por item de pedido) e menciona a tabela de calendário completa, marcada como tabela de datas."
  modelo: "Na tabela única, o nome e a cidade do cliente se repetem em cada venda, assim como a categoria e a marca do produto. O modelo fica maior e mais lento, uma correção de cadastro precisa ser feita em milhares de linhas, e as medidas DAX ficam mais difíceis, porque tudo depende da mesma tabela. Eu criaria uma fato de vendas com uma linha por item de pedido, contendo só a data, o número do pedido, a chave do cliente, a chave do produto, a quantidade e o valor. Em volta dela, uma dimensão de clientes, com nome, cidade e estado, uma dimensão de produtos, com nome, categoria e marca, e uma tabela de calendário com todos os dias dos anos cobertos, com ano, mês, trimestre e dia da semana, marcada como tabela de datas. Cada dimensão se liga à fato por um relacionamento um-para-muitos, com filtro de direção única. Assim, cada informação descritiva fica guardada uma vez, os filtros por cliente, produto ou período descem naturalmente para as vendas, e as funções de tempo do DAX funcionam."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Da planilha única ao modelo estrela"
  descricao: "A rede de lojas guarda as vendas numa planilha única, com os dados de produto e loja repetidos em cada linha. Você vai encontrar inconsistências, criar dimensões com chaves substitutas, montar a tabela de calendário, separar a tabela fato e validar os relacionamentos e a granularidade do modelo estrela."
  pasta: "desafios/visualizacao/modelagem_dados"
  testes: 11
  tempo: "1 h 30 min"
  ferramentas: "VS Code, Python 3.11 ou superior, pandas, pytest e Power BI Desktop para conferir"
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
      descricao: "Abra o terminal do VS Code com Ctrl+` (acento grave). Depois use Ctrl+Shift+P, Python: Select Interpreter, e escolha o .venv."
      comandos:
        - "# Linux ou macOS"
        - "python3 -m venv .venv"
        - "source .venv/bin/activate"
        - "# Windows (PowerShell)"
        - "python -m venv .venv"
        - '.venv\Scripts\Activate.ps1'
        - "pip install -r desafios/requirements.txt"
    - titulo: "Leia o enunciado e conheça os dados"
      descricao: "Abra desafios/visualizacao/modelagem_dados/README.md. Os dados estão em data/vendas_planas.csv: uma linha por item vendido, com os dados do produto e da loja repetidos em cada linha."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "Cada função tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def inconsistencias(plana, chave, atributos):"
        - "def criar_dim_produto(plana):"
        - "def criar_dim_loja(plana):"
        - "def criar_calendario(inicio, fim):"
        - "def criar_fato(plana, dim_produto, dim_loja):"
        - "def validar_relacionamento(fato, dimensao, chave):"
        - "def granularidade_ok(tabela, colunas):"
        - "def montar_modelo(caminho_csv):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/visualizacao/modelagem_dados"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/modelagem_dados"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de modelagem de dados"'
        - "git push -u origin desafio/modelagem_dados"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Tabela fato", en: "fact table" }
  - { pt: "Tabela dimensão", en: "dimension table" }
  - { pt: "Esquema estrela", en: "star schema" }
  - { pt: "Esquema floco de neve", en: "snowflake schema" }
  - { pt: "Granularidade", en: "grain, granularity" }
  - { pt: "Chave substituta", en: "surrogate key" }
  - { pt: "Chave natural", en: "natural key, business key" }
  - { pt: "Cardinalidade", en: "cardinality (one-to-many, 1:*)" }
  - { pt: "Direção do filtro cruzado", en: "cross-filter direction" }
  - { pt: "Tabela de datas", en: "date table" }
  - { pt: "Dimensão de alteração lenta", en: "slowly changing dimension (SCD)" }
  - { pt: "Dimensão degenerada", en: "degenerate dimension" }
  - { pt: "Relacionamento inativo", en: "inactive relationship" }
  - { pt: "Dimensão conformada", en: "conformed dimension" }
---

## Por que modelar: o problema da planilha única

É comum um relatório nascer de uma planilha única: cada linha é uma venda, com a data, o produto, a categoria, a marca, a loja, a cidade, a quantidade e o valor. Funciona no começo, e vai piorando conforme o relatório cresce:

- **Repetição.** O nome, a categoria e a marca do produto se repetem em cada venda. Com milhões de linhas, o modelo fica pesado e lento.
- **Inconsistência.** Se o mesmo produto aparece com duas categorias, os totais por categoria ficam errados, e não há um lugar único para corrigir.
- **Fatos diferentes não cabem juntos.** As vendas são registradas por item, e as metas por loja e mês. Não há como pôr as duas na mesma tabela sem repetir ou dividir valores.
- **DAX complicado.** Várias funções do DAX, principalmente as de tempo, pressupõem tabelas separadas e relacionadas.

A solução é **modelar**: separar os dados em tabelas com papéis diferentes e ligá-las por relacionamentos. Para análise, o formato recomendado pela Microsoft para o Power BI, e pela maior parte dos data warehouses, é o **esquema estrela**.

## Fatos e dimensões

Um modelo estrela tem dois tipos de tabela.

A **tabela fato** registra eventos ou medições: vendas, visitas, pagamentos, movimentações de estoque. Ela tem muitas linhas, e as colunas são de dois tipos: **chaves**, que apontam para as dimensões, e **números**, que serão agregados.

As **tabelas dimensão** descrevem o contexto dos eventos: quem, o quê, onde, quando. Têm menos linhas e muitas colunas de texto, que viram filtros, eixos e agrupamentos no relatório.

| Tabela        | Tipo      | Uma linha é          | Colunas                                                |
| ------------- | --------- | -------------------- | ------------------------------------------------------ |
| `fato_vendas` | Fato      | um item vendido      | data, pedido, id_produto, id_loja, quantidade, preco_unitario, valor |
| `dim_produto` | Dimensão  | um produto           | id_produto, código, nome, categoria, marca, custo      |
| `dim_loja`    | Dimensão  | uma loja             | id_loja, código, nome, cidade, UF                      |
| `dim_data`    | Dimensão  | um dia               | data, ano, mês, nome do mês, trimestre, dia da semana  |

Os números da fato não se comportam todos igual:

- **Aditivos** podem ser somados em qualquer direção: valor e quantidade vendidos.
- **Semiaditivos** podem ser somados em algumas dimensões, mas não no tempo: o saldo do estoque de cada loja soma entre lojas, mas somar o saldo de todos os dias do mês não faz sentido.
- **Não aditivos** nunca podem ser somados: porcentagens, preços unitários, médias. Eles são calculados por medidas, a partir dos aditivos.

## Esquema estrela e relacionamentos

No **esquema estrela**, a fato fica no centro, e cada dimensão se liga diretamente a ela:

```text
                  dim_produto
                       │ 1
                       │
                       │ *
   dim_data ─1─────*─ fato_vendas ─*─────1─ dim_loja
```

Se uma dimensão for quebrada em outras, como produto ligado a subcategoria e subcategoria ligada a categoria, o esquema vira um **floco de neve**. Ele economiza um pouco de espaço, mas no Power BI costuma ser pior: mais relacionamentos para o filtro percorrer e mais tabelas para entender. Prefira dimensões **desnormalizadas**, com todos os atributos do produto numa tabela só.

Cada relacionamento tem três propriedades:

- **As colunas ligadas:** a chave da dimensão e a chave estrangeira na fato.
- **A cardinalidade:** entre dimensão e fato, sempre **um-para-muitos** (1:*). A chave não pode se repetir no lado "um". Relacionamentos muitos-para-muitos existem, mas são sinal de um modelo que precisa de revisão.
- **A direção do filtro cruzado:** o recomendado é **única**, da dimensão para a fato.

É a direção do filtro que faz o modelo funcionar. Quando o usuário escolhe "PR" numa segmentação da coluna `dim_loja[uf]`, o filtro percorre o relacionamento e chega à fato: só as vendas das lojas do Paraná entram nos cálculos. Todo o funcionamento do DAX se apoia nessa propagação. Filtros **bidirecionais**, em que a fato também filtra a dimensão, podem criar ambiguidade quando há mais de um caminho entre duas tabelas, e deixam o modelo mais lento. Use-os só com um motivo claro.

Entre duas tabelas, só um relacionamento pode estar **ativo**. Se a fato tiver duas datas, como a do pedido e a da entrega, as duas podem se ligar ao calendário, mas uma fica **inativa** e só é usada quando uma medida pede, com a função `USERELATIONSHIP`. Uma dimensão usada em papéis diferentes, como o calendário aqui, é chamada de **dimensão com papéis** (*role-playing*).

## A tabela de calendário

Todo modelo com datas precisa de uma **tabela de calendário**, com estas características:

- **Uma linha por dia, sem buracos.** A coluna de data da fato só tem os dias com venda. O calendário tem todos.
- **Anos completos**, de 1º de janeiro do primeiro ano a 31 de dezembro do último. As funções de inteligência de tempo do DAX, como acumulado no ano e mesmo período do ano anterior, dependem disso.
- **Atributos de data:** ano, mês, nome do mês, trimestre, ano e mês, dia da semana, fim de semana, feriado.
- **Marcada como tabela de datas** no Power BI (Ferramentas de tabela > Marcar como tabela de datas).

O calendário pode ser criado na fonte, no Power Query ou em DAX:

```dax
Calendario =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2025, 1, 1 ), DATE ( 2026, 12, 31 ) ),
    "Ano", YEAR ( [Date] ),
    "Mês", MONTH ( [Date] ),
    "Nome do mês", FORMAT ( [Date], "mmmm" ),
    "Trimestre", "T" & QUARTER ( [Date] )
)
```

Dois detalhes práticos. Primeiro, para o nome do mês aparecer na ordem certa, e não em ordem alfabética, use **Classificar por coluna** e ordene "Nome do mês" pela coluna "Mês". Segundo, com um calendário próprio, desative a opção **Data/hora automática** do Power BI, nas opções de carregamento de dados. Ela cria uma tabela de datas escondida para cada coluna de data do modelo, o que aumenta o tamanho sem necessidade.

## Granularidade, chaves e dimensões que mudam

**Granularidade.** Antes de qualquer outra decisão, defina o que uma linha da fato representa. "Uma linha por item de pedido" permite analisar produtos. "O total diário por loja" não permite, mas é bem menor. A granularidade da fato é a menor que as perguntas do negócio exigem. Fatos de granularidades diferentes, como vendas por item e metas por loja e mês, viram **tabelas fato separadas**, ligadas às mesmas dimensões. Dimensões compartilhadas assim são chamadas de **conformadas**, e são elas que permitem comparar vendas com metas no mesmo visual.

**Chaves.** A chave que vem do sistema de origem, como o código "P07", é a **chave natural**. No modelo, é comum criar uma **chave substituta**: um número sem significado, como 1, 2, 3, gerado pelo próprio processo de carga. Ela protege o modelo de mudanças na origem, como um sistema novo com outros códigos, e é necessária para guardar histórico, como se verá abaixo. O número do pedido, que fica na fato sem uma dimensão própria, é uma **dimensão degenerada**.

**Dimensões que mudam.** Produtos mudam de categoria, clientes mudam de cidade, lojas mudam de gerente. As **dimensões de alteração lenta** (*slowly changing dimensions*, SCD) definem o que fazer com o histórico:

| Tipo   | O que faz                                                          | Efeito no relatório                                            |
| ------ | ------------------------------------------------------------------ | -------------------------------------------------------------- |
| Tipo 0 | Mantém o valor original e ignora mudanças                          | O produto fica para sempre na primeira categoria               |
| Tipo 1 | Sobrescreve o valor antigo                                         | Todo o histórico aparece na categoria nova                     |
| Tipo 2 | Cria uma nova linha para cada versão, com nova chave substituta e datas de validade | Vendas antigas ficam na categoria antiga, e as novas na nova |

O tipo 1 é simples e serve quando a mudança corrige um erro ou quando só a situação atual interessa. O tipo 2 é o certo quando a pergunta envolve o histórico, como "quanto a categoria Acessórios vendeu em 2025, com os produtos que ela tinha na época". No desafio, você vai montar a dimensão de produtos do tipo 1 e encontrar o produto que mudou de categoria.

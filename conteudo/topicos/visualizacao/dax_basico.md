---
titulo: "DAX básico"
modulo: visualizacao
ordem: 3
horas: 6
estado: publicado
resumo: "Medidas, colunas calculadas e contexto de filtro."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Medidas e colunas calculadas"
    tipo: leitura
    minutos: 12
  - id: a2
    titulo: "Contexto de filtro e contexto de linha"
    tipo: leitura
    minutos: 20
  - id: a3
    titulo: "CALCULATE: mudando o contexto de filtro"
    tipo: leitura
    minutos: 20
  - id: a4
    titulo: "Iteradores: SUMX e RELATED"
    tipo: leitura
    minutos: 12
  - id: a5
    titulo: "Inteligência de tempo"
    tipo: leitura
    minutos: 15
  - id: a6
    titulo: "Variáveis e boas práticas"
    tipo: leitura
    minutos: 10
  - id: a7
    titulo: "Vídeo de apoio: DAX do zero"
    tipo: video
    minutos: 30
    link: ""
  - id: a8
    titulo: "Vídeo de apoio: CALCULATE e contexto de filtro"
    tipo: video
    minutos: 20
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Qual é a principal diferença entre uma medida e uma coluna calculada?"
    opcoes: ["A coluna calculada é calculada linha a linha na atualização e guardada no modelo; a medida é calculada na hora da consulta, conforme o contexto de filtro de cada visual", "Não há diferença, são dois nomes para a mesma coisa", "A medida só funciona em tabelas de dimensão", "A coluna calculada é sempre mais rápida e deve ser preferida"]
    correta: 0
    explicacao: "A coluna calculada ocupa memória e tem um valor fixo por linha: serve para criar atributos usados em filtros e agrupamentos, embora o ideal seja criá-los no Power Query ou na fonte. A medida não ocupa espaço e se adapta a cada célula do visual: serve para os números que são agregados."
  - pergunta: "Uma matriz tem a UF nas linhas e usa a medida Faturamento = SUM ( fato_vendas[valor] ). Por que cada linha mostra um valor diferente, se a fórmula é a mesma?"
    opcoes: ["Porque o Power BI divide o total pelo número de linhas", "Porque cada linha usa uma medida diferente, criada automaticamente", "Porque cada célula calcula a medida num contexto de filtro diferente: o filtro da UF desce da dim_loja para a fato pelo relacionamento", "Porque a fato tem uma coluna de UF"]
    correta: 2
    explicacao: "A linha 'PR' calcula o SUM com o filtro dim_loja[uf] = 'PR'. O filtro percorre o relacionamento e deixa visíveis só as vendas das lojas do Paraná. A linha de total não tem o filtro de UF, então a medida é recalculada com todas as vendas."
  - pergunta: "O que faz CALCULATE ( [Faturamento], ALL ( dim_loja ) )?"
    opcoes: ["Calcula o faturamento de todas as lojas somadas, e ignora todos os outros filtros também", "Calcula o faturamento ignorando os filtros da tabela dim_loja e mantendo os outros, como os de data e produto", "Filtra só a primeira loja", "Dá erro, porque ALL só funciona com colunas"]
    correta: 1
    explicacao: "O CALCULATE avalia a expressão num contexto de filtro modificado. O ALL ( dim_loja ) remove os filtros vindos da dimensão de lojas, e os demais continuam valendo. É a base de medidas de participação: o faturamento da linha dividido pelo de todas as lojas no mesmo período."
  - pergunta: "Qual fórmula calcula corretamente a receita como a soma de quantidade x preço de cada venda?"
    opcoes: ["SUM ( fato_vendas[quantidade] ) * SUM ( fato_vendas[preco_unitario] )", "SUM ( fato_vendas[quantidade] * fato_vendas[preco_unitario] )", "AVERAGE ( fato_vendas[preco_unitario] ) * COUNT ( fato_vendas[pedido] )", "SUMX ( fato_vendas, fato_vendas[quantidade] * fato_vendas[preco_unitario] )"]
    correta: 3
    explicacao: "O SUMX percorre a tabela, calcula a expressão em cada linha e soma os resultados. Multiplicar as duas somas dá um número sem sentido. O SUM do DAX só aceita uma coluna, então a segunda opção nem funciona. A terceira só daria certo se todas as vendas tivessem a mesma quantidade."
  - pergunta: "Por que usar DIVIDE ( [A], [B] ) em vez de [A] / [B]?"
    opcoes: ["Porque o DIVIDE trata a divisão por zero, devolvendo BLANK ou um valor alternativo em vez de erro", "Porque o operador / não existe no DAX", "Porque o DIVIDE arredonda o resultado", "Porque o DIVIDE converte o resultado em porcentagem"]
    correta: 0
    explicacao: "Num visual, é comum uma célula ter denominador zero ou vazio, como uma loja sem meta num mês. O [A] / [B] mostraria infinito ou erro. O DIVIDE devolve BLANK, e a célula fica vazia, ou devolve o terceiro argumento, se ele for informado."
  - pergunta: "O que as funções de inteligência de tempo, como TOTALYTD e SAMEPERIODLASTYEAR, exigem do modelo?"
    opcoes: ["Uma coluna de data na fato, e nada mais", "Que os dados estejam em DirectQuery", "Uma tabela de datas contínua, com anos completos, relacionada à fato e marcada como tabela de datas", "Uma medida por ano"]
    correta: 2
    explicacao: "Essas funções trabalham deslocando e ampliando o conjunto de datas visíveis no calendário: do início do ano até a última data, ou as mesmas datas um ano antes. Para isso, o calendário precisa ter todos os dias, sem buracos, e estar ligado à fato."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Explique com um exemplo o que é o contexto de filtro e como o CALCULATE o altera. Use como exemplo uma medida de participação de cada loja no faturamento, numa matriz com as lojas nas linhas."
  rubrica:
    - "Explica que o contexto de filtro é o conjunto de filtros ativos numa célula do visual (linha, coluna, segmentações, filtros da página) e que ele desce das dimensões para a fato pelos relacionamentos."
    - "Explica que o CALCULATE avalia uma expressão num contexto de filtro modificado, e que ALL ( dim_loja ) remove o filtro de loja, mantendo os outros."
    - "Escreve a medida com DIVIDE ( [Faturamento], CALCULATE ( [Faturamento], ALL ( dim_loja ) ) ) e explica por que a linha de total mostra 100%."
  modelo: "O contexto de filtro é o conjunto de filtros que vale para uma célula de um visual: o valor da linha e da coluna, as segmentações e os filtros da página. Numa matriz com lojas nas linhas, a célula da Loja Centro calcula as medidas com o filtro dim_loja[loja] = 'Loja Centro', que desce pelo relacionamento e deixa visíveis só as vendas dessa loja. O CALCULATE avalia uma expressão num contexto modificado: CALCULATE ( [Faturamento], ALL ( dim_loja ) ) remove o filtro da loja e calcula o faturamento de todas as lojas, mantendo os outros filtros, como o de período. A participação fica: Participação = DIVIDE ( [Faturamento], CALCULATE ( [Faturamento], ALL ( dim_loja ) ) ). Em cada linha, o numerador é o faturamento da loja e o denominador é o de todas. Na linha de total não há filtro de loja, então numerador e denominador são iguais e o resultado é 100%: o total não soma as participações, ele recalcula a medida."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "O contexto de filtro por dentro"
  descricao: "Sobre o modelo estrela do desafio de modelagem, você vai implementar em Python o que o motor do Power BI faz: propagar o contexto de filtro das dimensões para a fato e calcular medidas equivalentes a SUM, SUMX com RELATED, CALCULATE com ALL, DIVIDE, TOTALYTD e SAMEPERIODLASTYEAR, terminando com uma matriz que mostra por que o total é recalculado, e não somado."
  pasta: "desafios/visualizacao/dax_basico"
  testes: 11
  tempo: "2 h 30 min"
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
    - titulo: "Leia o enunciado e conheça o modelo"
      descricao: "Abra desafios/visualizacao/dax_basico/README.md. Ele mostra as tabelas do modelo e como o contexto de filtro é escrito em Python."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "Comece pelo filtrar_fato: todas as medidas dependem dele. Acima de cada medida está a fórmula DAX equivalente. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def filtrar_fato(modelo, filtros):"
        - "def datas_visiveis(modelo, filtros):"
        - "def faturamento(modelo, filtros):"
        - "def margem(modelo, filtros):"
        - "def faturamento_todas_as_lojas(modelo, filtros):"
        - "def participacao_da_loja(modelo, filtros):"
        - "def faturamento_acumulado_no_ano(modelo, filtros):"
        - "def faturamento_ano_anterior(modelo, filtros):"
        - "def crescimento_anual(modelo, filtros):"
        - "def matriz(modelo, filtros, referencia_linhas, medida):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/visualizacao/dax_basico"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/dax_basico"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de DAX básico"'
        - "git push -u origin desafio/dax_basico"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Medida", en: "measure" }
  - { pt: "Coluna calculada", en: "calculated column" }
  - { pt: "Tabela calculada", en: "calculated table" }
  - { pt: "Contexto de filtro", en: "filter context" }
  - { pt: "Contexto de linha", en: "row context" }
  - { pt: "Transição de contexto", en: "context transition" }
  - { pt: "Iterador (funções X)", en: "iterator (SUMX, AVERAGEX...)" }
  - { pt: "Inteligência de tempo", en: "time intelligence" }
  - { pt: "Acumulado no ano", en: "year-to-date (YTD)" }
  - { pt: "Mesmo período do ano anterior", en: "same period last year (SPLY)" }
  - { pt: "Variável", en: "variable (VAR ... RETURN)" }
  - { pt: "Valor em branco", en: "BLANK" }
---

## Medidas e colunas calculadas

O **DAX** (*Data Analysis Expressions*) é a linguagem de fórmulas do Power BI, do Analysis Services e do Power Pivot do Excel. Ele parece com as fórmulas do Excel, mas trabalha sobre tabelas e colunas, e não sobre células.

Há três lugares onde se escreve DAX:

- **Coluna calculada:** uma coluna nova numa tabela, calculada linha a linha quando os dados são atualizados, e guardada no modelo.
- **Medida:** uma fórmula calculada na hora da consulta, para cada célula de cada visual.
- **Tabela calculada:** uma tabela nova, como um calendário criado com `CALENDAR`.

```dax
-- coluna calculada, na fato_vendas: um valor fixo por linha
Faixa de preço =
IF ( fato_vendas[preco_unitario] >= 500, "Alto", "Normal" )

-- medida: um valor para cada contexto
Faturamento = SUM ( fato_vendas[valor] )
```

A regra prática: **números que serão agregados viram medidas; atributos usados para filtrar e agrupar viram colunas**. E colunas, sempre que possível, devem ser criadas antes, no Power Query ou na fonte, e não em DAX. As colunas calculadas ocupam memória, e as medidas não.

Escreva sempre **medidas explícitas**, como a de faturamento acima, em vez de arrastar a coluna `valor` para o visual e deixar o Power BI somar sozinho. A medida explícita tem nome, formato e pode ser reusada em outras medidas.

A notação é sempre `Tabela[Coluna]` para colunas e `[Medida]` para medidas. Nomear as colunas com a tabela e as medidas sem ela ajuda a distinguir as duas coisas ao ler uma fórmula.

## Contexto de filtro e contexto de linha

Uma medida não tem um valor: ela tem um valor **em cada contexto**. Veja uma matriz com a UF nas linhas e a medida Faturamento:

| UF     | Faturamento |
| ------ | ----------- |
| MG     | 91.249      |
| PR     | 155.516     |
| RS     | 67.092      |
| SP     | 121.676     |
| Total  | 435.533     |

A fórmula é a mesma em todas as células. O que muda é o **contexto de filtro**: o conjunto de filtros ativos naquela célula. Na linha "PR", o filtro `dim_loja[uf] = "PR"` está ativo. Ele percorre o relacionamento entre `dim_loja` e `fato_vendas` e deixa visíveis só as vendas das lojas do Paraná. O `SUM` soma só essas linhas.

O contexto de filtro vem de vários lugares ao mesmo tempo: linhas e colunas do visual, segmentações de dados, filtros do visual, da página e do relatório, e a segurança em nível de linha. Todos se combinam.

A **linha de total** não tem o filtro de UF. Por isso ela não soma as linhas de cima: ela recalcula a medida com todas as vendas. Para uma soma, o resultado é o mesmo. Para uma porcentagem, uma média ou um crescimento, não é, e isso é o esperado.

O **contexto de linha** é outra coisa: é a noção de "linha atual", que existe nas colunas calculadas e nos iteradores. Na coluna calculada Faixa de preço, a fórmula é avaliada uma vez para cada linha, e `fato_vendas[preco_unitario]` é o preço daquela linha. O contexto de linha **não filtra** nada por si só. Para buscar um valor de uma tabela relacionada, do lado "um" do relacionamento, usa-se `RELATED`:

```dax
-- coluna calculada na fato: a categoria do produto de cada venda
Categoria = RELATED ( dim_produto[categoria] )
```

## CALCULATE: mudando o contexto de filtro

O **CALCULATE** é a função mais importante do DAX. Ele avalia uma expressão num contexto de filtro **modificado**:

```dax
Faturamento PR =
CALCULATE ( [Faturamento], dim_loja[uf] = "PR" )

Faturamento todas as lojas =
CALCULATE ( [Faturamento], ALL ( dim_loja ) )

Participação da loja =
DIVIDE ( [Faturamento], [Faturamento todas as lojas] )
```

- Um filtro como `dim_loja[uf] = "PR"` **substitui** o filtro que já existia na mesma coluna. Na matriz por UF, a medida Faturamento PR mostra o valor do Paraná em todas as linhas, inclusive na de MG.
- `ALL ( tabela )` ou `ALL ( tabela[coluna] )` **remove** filtros. `REMOVEFILTERS` faz o mesmo e tem um nome mais claro.
- `ALLEXCEPT ( dim_loja, dim_loja[uf] )` remove os filtros da tabela, menos o de uma coluna.
- `KEEPFILTERS` faz o novo filtro se somar ao existente, em vez de substituí-lo.
- Os filtros que não são tocados continuam valendo: em Faturamento todas as lojas, um filtro de ano no visual continua ativo.

Com a participação na matriz por UF, cada linha mostra a fatia da UF, e o total mostra 100%, porque na linha de total o numerador e o denominador são iguais.

Para condições mais complexas, o `FILTER` percorre uma tabela e mantém as linhas que atendem a uma condição:

```dax
Faturamento de itens caros =
CALCULATE (
    [Faturamento],
    FILTER ( fato_vendas, fato_vendas[preco_unitario] >= 500 )
)
```

Prefira filtros simples em colunas sempre que possível. Filtrar a tabela fato inteira com `FILTER` é mais lento que filtrar uma coluna.

## Iteradores: SUMX e RELATED

As funções terminadas em X, como `SUMX`, `AVERAGEX`, `MAXX` e `COUNTX`, são **iteradores**: percorrem uma tabela, calculam uma expressão em cada linha, num contexto de linha, e agregam os resultados.

```dax
Margem =
SUMX (
    fato_vendas,
    fato_vendas[quantidade]
        * ( fato_vendas[preco_unitario] - RELATED ( dim_produto[custo_unitario] ) )
)
```

Para cada venda visível no contexto de filtro, a fórmula calcula quantidade vezes a diferença entre o preço e o custo do produto, que vem da dimensão pelo `RELATED`. No fim, soma tudo. Multiplicar somas, como `SUM ( quantidade ) * SUM ( preco )`, daria um número sem sentido: a conta precisa ser feita linha a linha, antes de somar.

O `SUM ( coluna )` é, na verdade, um atalho para `SUMX ( tabela, coluna )`.

## Inteligência de tempo

As funções de **inteligência de tempo** mudam o conjunto de datas do contexto: ampliam até o início do ano, deslocam para o ano anterior, voltam um mês. Elas exigem uma tabela de calendário contínua, com anos completos, relacionada à fato e marcada como tabela de datas, como visto no tópico de modelagem.

```dax
Faturamento acumulado no ano =
TOTALYTD ( [Faturamento], dim_data[data] )

Faturamento ano anterior =
CALCULATE ( [Faturamento], SAMEPERIODLASTYEAR ( dim_data[data] ) )

Faturamento mês anterior =
CALCULATE ( [Faturamento], DATEADD ( dim_data[data], -1, MONTH ) )

Crescimento anual =
DIVIDE (
    [Faturamento] - [Faturamento ano anterior],
    [Faturamento ano anterior]
)
```

Como elas funcionam, na célula de março de 2026:

- **TOTALYTD** pega a última data visível, 31/03/2026, e troca o filtro de datas por todas as datas de 1º de janeiro de 2026 até ela.
- **SAMEPERIODLASTYEAR** troca as datas visíveis, de 1º a 31 de março de 2026, pelas mesmas datas um ano antes.
- **DATEADD** desloca as datas visíveis por um intervalo qualquer, para trás ou para a frente.

Os outros filtros, como loja e produto, continuam valendo. No desafio, você vai implementar exatamente esse mecanismo.

## Variáveis e boas práticas

**Variáveis** deixam as medidas mais legíveis e evitam calcular a mesma coisa duas vezes:

```dax
Crescimento anual =
VAR Atual = [Faturamento]
VAR Anterior = [Faturamento ano anterior]
RETURN
    DIVIDE ( Atual - Anterior, Anterior )
```

Uma variável é calculada uma vez, no contexto em que é definida, e o `RETURN` diz o resultado. Para investigar uma medida que dá um número estranho, troque temporariamente o `RETURN` por uma das variáveis e veja o valor dela.

Outras boas práticas:

- **Use `DIVIDE`** em toda divisão. Ele devolve BLANK quando o denominador é zero ou vazio, em vez de erro.
- **Entenda o BLANK.** É o "vazio" do DAX. Visuais escondem as linhas em que todas as medidas são BLANK, o que em geral é o desejado.
- **Construa medidas sobre medidas.** Participação usa Faturamento, Crescimento usa Faturamento e Faturamento ano anterior. Uma correção em Faturamento vale para todas.
- **Guarde as medidas numa tabela própria** e defina o formato de cada uma (moeda, porcentagem) na própria medida.
- **Modele antes de escrever DAX.** Um modelo estrela bem feito deixa quase todas as medidas simples. Medidas muito complicadas costumam ser sinal de um problema no modelo.

A exibição de consulta DAX e o Analisador de desempenho, no Power BI Desktop, ajudam a testar medidas e a encontrar visuais lentos. Temas mais avançados, como a transição de contexto e os grupos de cálculo, aparecem na prova DP-600 e são o próximo passo depois deste tópico.

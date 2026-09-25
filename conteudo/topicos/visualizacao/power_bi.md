---
titulo: "Power BI"
modulo: visualizacao
ordem: 1
horas: 8
estado: publicado
resumo: "Importar dados, montar relatórios e publicar dashboards."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "O que é o Power BI e como é o fluxo de trabalho"
    tipo: leitura
    minutos: 10
  - id: a2
    titulo: "Power Query: obter e transformar dados"
    tipo: leitura
    minutos: 20
  - id: a3
    titulo: "Do modelo ao relatório: medidas e visuais"
    tipo: leitura
    minutos: 15
  - id: a4
    titulo: "Publicar e compartilhar: serviço, atualização e segurança"
    tipo: leitura
    minutos: 15
  - id: a5
    titulo: "Modos de armazenamento: Importação, DirectQuery e Direct Lake"
    tipo: leitura
    minutos: 10
  - id: a6
    titulo: "Vídeo de apoio: primeiro relatório no Power BI Desktop"
    tipo: video
    minutos: 30
    link: ""
  - id: a7
    titulo: "Vídeo de apoio: Power Query na prática"
    tipo: video
    minutos: 20
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "No Power BI Desktop, onde se faz a limpeza e a transformação dos dados antes de eles chegarem ao modelo?"
    opcoes: ["No Power Query", "Nas medidas DAX", "No serviço do Power BI, depois de publicar", "Nos próprios visuais, com filtros"]
    correta: 0
    explicacao: "O Power Query, aberto pelo botão Transformar dados, é a etapa de preparação: tipos, limpeza, junções e formato das tabelas. O DAX calcula sobre os dados já carregados no modelo. Uma regra prática é fazer a limpeza o mais cedo possível, de preferência na fonte ou no Power Query."
  - pergunta: "As metas chegam numa tabela com uma coluna por mês (jan, fev, mar...). Qual transformação do Power Query deixa uma linha por loja e mês?"
    opcoes: ["Transpor", "Transformar Outras Colunas em Linhas, com a coluna da loja selecionada", "Agrupar Por", "Dividir Coluna por delimitador"]
    correta: 1
    explicacao: "Despivotar transforma colunas em pares de atributo e valor: cada loja passa a ter uma linha por mês, com as colunas mes e meta. Selecionar a loja e usar Transformar Outras Colunas em Linhas é a forma mais robusta, porque um mês novo na planilha entra sozinho."
  - pergunta: "Qual é a diferença entre Mesclar Consultas e Acrescentar Consultas no Power Query?"
    opcoes: ["Nenhuma, são nomes diferentes para a mesma coisa", "Mesclar só funciona com arquivos Excel", "Mesclar traz colunas de outra tabela casando por uma chave, como um PROCX ou JOIN; Acrescentar empilha as linhas de tabelas com as mesmas colunas", "Acrescentar remove duplicatas, e Mesclar não"]
    correta: 2
    explicacao: "Mesclar equivale ao merge do pandas e ao JOIN do SQL: acrescenta colunas. Acrescentar equivale ao concat e ao UNION ALL: acrescenta linhas. Juntar vendas com o cadastro de lojas é mesclar; juntar as vendas de janeiro com as de fevereiro é acrescentar."
  - pergunta: "Um CSV brasileiro, com valores como 1.234,56, foi importado num Power BI configurado em inglês, e os valores ficaram errados. O que resolve?"
    opcoes: ["Apagar os pontos com Substituir Valores", "Mudar o tipo da coluna para texto", "Nada, é preciso reexportar o arquivo", "Alterar o tipo usando localidade, com Português (Brasil)"]
    correta: 3
    explicacao: "Com a localidade em inglês, o ponto é lido como separador decimal, e 1.234,56 vira outra coisa. O Alterar Tipo usando localidade diz ao Power Query em que formato o texto está. O mesmo vale para datas como 05/03/2026, que em inglês seriam 3 de maio."
  - pergunta: "Todo mês chega um arquivo novo de vendas. Qual é o jeito de o relatório incluir os meses novos sem refazer nada?"
    opcoes: ["Obter Dados > Pasta e Combinar: ao atualizar, todos os arquivos da pasta entram, inclusive os novos", "Acrescentar uma consulta nova para cada mês", "Copiar os dados novos para o arquivo antigo", "Criar um relatório por mês"]
    correta: 0
    explicacao: "O conector de Pasta lê todos os arquivos de uma pasta e aplica as mesmas etapas a cada um. Basta salvar o arquivo novo na pasta e atualizar. Para isso funcionar, os arquivos precisam ter o mesmo formato."
  - pergunta: "O que são as Etapas Aplicadas do Power Query?"
    opcoes: ["Os filtros aplicados aos visuais do relatório", "A sequência de transformações, gravada em linguagem M e refeita a cada atualização", "As versões salvas do arquivo .pbix", "As permissões de quem pode ver o relatório"]
    correta: 1
    explicacao: "Cada clique no Power Query vira uma etapa, escrita em M, que aparece no painel Etapas Aplicadas e no Editor Avançado. A cada atualização, o Power Query repete todas as etapas sobre os dados novos. É isso que torna o preparo repetível."
  - pergunta: "Qual é a diferença entre os modos de armazenamento Importação e DirectQuery?"
    opcoes: ["Nenhuma, só muda o nome do arquivo", "DirectQuery é sempre mais rápido", "Importação copia os dados para o modelo, com consultas rápidas mas dependentes da atualização; DirectQuery consulta a fonte a cada interação, sempre atual, mas depende do desempenho da fonte", "Importação só funciona com Excel"]
    correta: 2
    explicacao: "Na Importação, os dados ficam comprimidos na memória do modelo e os visuais respondem rápido, mas só mostram o que havia na última atualização. No DirectQuery, cada visual gera consultas na fonte: os dados estão sempre atuais, mas a velocidade e parte das funções DAX dependem da fonte."
  - pergunta: "No Microsoft Fabric, o que o modo de armazenamento Direct Lake oferece?"
    opcoes: ["O modelo lê diretamente as tabelas Delta do OneLake, sem importar uma cópia, com desempenho próximo ao da Importação", "Uma conexão direta com arquivos Excel do computador", "Um modo que dispensa o modelo semântico", "O mesmo que DirectQuery, com outro nome"]
    correta: 0
    explicacao: "No Direct Lake, o modelo semântico carrega na memória, sob demanda, as colunas das tabelas Delta guardadas no OneLake, como as de um lakehouse ou warehouse do Fabric. Não há cópia agendada como na Importação, e as consultas não vão para a fonte a cada clique como no DirectQuery."
  - pergunta: "Um relatório publicado usa dados de um SQL Server dentro da rede da empresa. O que é necessário para a atualização agendada funcionar no serviço?"
    opcoes: ["Nada, o serviço acessa a rede da empresa sozinho", "Tornar o banco público na internet", "Atualizar sempre pelo Power BI Desktop e republicar", "Um gateway de dados local, instalado num computador da rede que alcança o banco"]
    correta: 3
    explicacao: "O serviço do Power BI roda na nuvem e não enxerga a rede interna. O gateway de dados local faz a ponte: ele fica num computador da empresa, busca os dados e os envia para o serviço. Fontes na nuvem, como o OneLake ou um banco na Azure, em geral não precisam de gateway."
  - pergunta: "Como fazer cada gerente regional ver só as vendas da sua região, no mesmo relatório?"
    opcoes: ["Criar um relatório para cada região", "Configurar segurança em nível de linha (RLS), com funções que filtram a tabela de lojas pela região de quem está vendo", "Esconder as páginas das outras regiões", "Usar uma segmentação de dados por região"]
    correta: 1
    explicacao: "Com RLS, o modelo aplica um filtro de acordo com o usuário, e o filtro se propaga pelos relacionamentos. Uma segmentação de dados não é segurança: o usuário pode simplesmente mudar a seleção. E manter um relatório por região multiplica o trabalho."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Você precisa montar no Power BI um relatório de vendas contra metas, com dados que chegam todo mês em CSV numa pasta de rede. Descreva as etapas, do arquivo ao relatório publicado, e explique as decisões que evitam retrabalho a cada mês."
  rubrica:
    - "Descreve as etapas do Power Query: obter da pasta e combinar os arquivos, alterar os tipos com a localidade certa, padronizar as chaves, despivotar as metas e mesclar com o cadastro de lojas."
    - "Menciona o modelo e as medidas: tabelas relacionadas (vendas, metas, lojas, calendário) e medidas DAX para faturamento, meta e atingimento, em vez de números calculados à mão."
    - "Menciona a publicação e a atualização: publicar num workspace, configurar a atualização agendada com gateway, porque a pasta é de rede, e compartilhar por app ou permissão, para que o mês novo entre sem refazer nada."
  modelo: "No Power BI Desktop, eu usaria Obter Dados > Pasta, apontando para a pasta de rede, e combinaria os arquivos: assim, cada CSV novo entra sozinho. No Power Query, alteraria os tipos com a localidade Português (Brasil), por causa da vírgula decimal e das datas dd/mm/aaaa, e padronizaria o código da loja com Aparar e MAIÚSCULAS, para a mesclagem não falhar. As metas, com um mês por coluna, seriam despivotadas com Transformar Outras Colunas em Linhas. No modelo, ligaria vendas e metas às dimensões de loja e de calendário e criaria medidas DAX para faturamento, meta e atingimento. Os visuais usariam essas medidas: cartões no topo, uma matriz de lojas por mês e um gráfico de atingimento. Por fim, publicaria num workspace, configuraria o gateway de dados local, porque a pasta está na rede da empresa, e agendaria a atualização diária. Com isso, basta o arquivo do mês chegar na pasta: ninguém precisa abrir o Desktop nem refazer etapas."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "O Power Query por dentro"
  descricao: "Uma rede de lojas quer um relatório de vendas contra metas. Você vai fazer em pandas cada etapa que faria no Power Query: combinar os arquivos de uma pasta, alterar tipos com a localidade brasileira, padronizar chaves, despivotar as metas, mesclar com o cadastro, criar coluna condicional, agrupar e calcular os cartões do relatório."
  pasta: "desafios/visualizacao/power_bi"
  testes: 10
  tempo: "2 h"
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
      descricao: "Abra desafios/visualizacao/power_bi/README.md e abra os CSVs de data/ num editor de texto, para ver o separador, os decimais e as datas."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "Cada função faz uma etapa do Power Query, e a docstring diz qual. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def ler_arquivo_vendas(caminho_csv):"
        - "def combinar_arquivos(pasta):"
        - "def despivotar_metas(caminho_csv):"
        - "def mesclar_lojas(vendas, lojas):"
        - "def adicionar_faixa(vendas):"
        - "def agrupar_por_loja_e_mes(vendas):"
        - "def realizado_vs_meta(agrupado, metas):"
        - "def cartoes(realizado):"
        - "def montar_relatorio(pasta_dados):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/visualizacao/power_bi"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/power_bi"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de Power BI"'
        - "git push -u origin desafio/power_bi"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Obter dados", en: "get data" }
  - { pt: "Etapas aplicadas", en: "applied steps" }
  - { pt: "Linguagem M", en: "M, Power Query formula language" }
  - { pt: "Mesclar consultas", en: "merge queries" }
  - { pt: "Acrescentar consultas", en: "append queries" }
  - { pt: "Transformar colunas em linhas", en: "unpivot columns" }
  - { pt: "Modelo semântico", en: "semantic model (antes, dataset)" }
  - { pt: "Medida", en: "measure" }
  - { pt: "Segmentação de dados", en: "slicer" }
  - { pt: "Workspace", en: "workspace" }
  - { pt: "Atualização agendada", en: "scheduled refresh" }
  - { pt: "Gateway de dados local", en: "on-premises data gateway" }
  - { pt: "Segurança em nível de linha", en: "row-level security (RLS)" }
  - { pt: "Modo de armazenamento", en: "storage mode (Import, DirectQuery, Direct Lake)" }
---

## O que é o Power BI e como é o fluxo de trabalho

O **Power BI** é a ferramenta de relatórios e painéis da Microsoft. Ele tem duas partes principais:

- **Power BI Desktop:** o programa gratuito, para Windows, em que o relatório é construído.
- **Serviço do Power BI:** o site (app.powerbi.com) onde os relatórios são publicados, compartilhados e atualizados. Hoje ele faz parte do **Microsoft Fabric**, a plataforma de dados da Microsoft.

Um relatório passa sempre pelas mesmas quatro etapas:

1. **Obter e transformar os dados**, no Power Query.
2. **Modelar:** relacionar as tabelas e criar medidas em DAX. O resultado é o **modelo semântico**, que no passado se chamava *dataset*.
3. **Visualizar:** montar as páginas do relatório com gráficos, tabelas e filtros.
4. **Publicar e compartilhar:** enviar ao serviço, agendar a atualização e dar acesso às pessoas.

Este tópico cobre as etapas 1, 3 e 4. A modelagem e o DAX têm tópicos próprios, a seguir. Os nomes em inglês do glossário são os usados na documentação e na prova de certificação DP-600.

## Power Query: obter e transformar dados

O botão **Obter dados** conecta a centenas de fontes: Excel, CSV, pastas, bancos SQL, SharePoint, APIs, lakehouses do Fabric. O botão **Transformar dados** abre o **Editor do Power Query**, onde os dados são preparados antes de chegar ao modelo.

Cada ação feita no editor vira uma **etapa aplicada**, que aparece numa lista no painel lateral. As etapas ficam gravadas e são refeitas, na mesma ordem, a cada atualização. Por isso o preparo no Power Query é repetível: o trabalho é feito uma vez, e os dados novos passam pelas mesmas etapas.

As transformações mais usadas:

| Transformação                          | O que faz                                                    |
| -------------------------------------- | ------------------------------------------------------------ |
| Usar a primeira linha como cabeçalho   | Promove a primeira linha a nomes de coluna                   |
| Alterar tipo (e usando localidade)     | Define texto, número, data; a localidade diz o formato do texto de origem |
| Remover linhas e colunas               | Tira linhas de título, totais, colunas que não serão usadas |
| Substituir valores, Aparar, MAIÚSCULAS | Limpeza de texto                                             |
| Dividir coluna                         | Separa uma coluna em várias, por delimitador ou posição      |
| Transformar outras colunas em linhas   | Despivota: uma coluna por mês vira uma linha por mês         |
| Coluna condicional, coluna personalizada | Cria colunas a partir de regras ou fórmulas               |
| Agrupar por                            | Resume linhas, como o GROUP BY do SQL                        |
| Mesclar consultas                      | Traz colunas de outra tabela casando por chave, como um JOIN |
| Acrescentar consultas                  | Empilha tabelas com as mesmas colunas, como um UNION ALL     |

Duas situações do dia a dia merecem atenção:

- **Arquivos que chegam todo mês.** Use Obter dados > **Pasta** e **Combinar**. O Power Query lê todos os arquivos da pasta e aplica as mesmas etapas a cada um. O mês novo entra só por estar na pasta.
- **Formato brasileiro.** Números como 1.234,56 e datas como 05/03/2026 são lidos errado quando o Power BI está configurado em inglês. Use **Alterar tipo > Usando localidade** e escolha Português (Brasil).

Por trás dos cliques, cada etapa é escrita em **M**, a linguagem do Power Query. O **Editor Avançado** mostra o código completo. Não é preciso escrever M do zero, mas ler ajuda a entender e a corrigir consultas:

```powerquery
let
    Fonte = Csv.Document(File.Contents("C:\dados\metas.csv"),
        [Delimiter = ";", Encoding = 65001]),
    Cabecalhos = Table.PromoteHeaders(Fonte),
    Despivotado = Table.UnpivotOtherColumns(Cabecalhos, {"loja"}, "mes", "meta"),
    Tipos = Table.TransformColumnTypes(Despivotado,
        {{"meta", type number}}, "pt-BR")
in
    Tipos
```

Cada linha do `let` é uma etapa, e cada etapa usa o resultado da anterior. O último argumento de `Table.TransformColumnTypes`, `"pt-BR"`, é a localidade.

Um princípio vale para qualquer transformação: **faça-a o mais perto possível da fonte**. Se o dado pode vir limpo do banco, melhor. Se não, limpe no Power Query. Deixar para limpar com DAX, no modelo, deixa o modelo mais pesado e as fórmulas mais complicadas.

## Do modelo ao relatório: medidas e visuais

Depois de **Fechar e aplicar**, as tabelas vão para o modelo. Os números do relatório vêm de **medidas**, fórmulas em DAX que são calculadas conforme os filtros de cada visual:

```dax
Faturamento = SUM ( Vendas[valor] )

Atingimento % = DIVIDE ( [Faturamento], SUM ( Metas[meta] ) )
```

A mesma medida mostra o total da empresa num cartão, o total de cada loja numa matriz e o total de cada mês num gráfico de linha. O tópico de DAX explica como isso funciona.

Os visuais mais usados num relatório de negócios:

| Visual                         | Para quê                                                   |
| ------------------------------ | ---------------------------------------------------------- |
| Cartão                         | Um número em destaque: faturamento, atingimento            |
| Gráfico de barras ou colunas   | Comparar categorias                                        |
| Gráfico de linhas              | Evolução no tempo                                          |
| Matriz                         | Tabela cruzada, como uma tabela dinâmica, com subtotais    |
| Segmentação de dados           | Filtros que o usuário escolhe na página                    |
| Mapa, dispersão, cascata       | Casos específicos: geografia, relação, composição de uma variação |

As regras do tópico de tipos de gráficos continuam valendo: comece pela pergunta, ordene as barras, comece o eixo no zero, use cor para destacar. Dois recursos próprios do Power BI:

- **Interação entre visuais.** Clicar numa barra filtra os outros visuais da página. Em Formatar > Editar interações, dá para escolher o que cada visual filtra.
- **Detalhamento (drill).** Uma hierarquia, como ano, trimestre e mês, permite descer de nível dentro do mesmo visual.

Uma página boa tem poucos visuais, os números mais importantes no canto superior esquerdo, onde o olho começa, e títulos que dizem o que o visual mostra.

## Publicar e compartilhar: serviço, atualização e segurança

O botão **Publicar** envia o relatório e o modelo semântico para um **workspace** no serviço. Um workspace é uma área compartilhada de trabalho, com papéis de acesso: administrador, membro, colaborador e visualizador.

Para distribuir o relatório a quem só consome, as opções são dar acesso ao workspace com o papel de visualizador, compartilhar o relatório diretamente ou publicar um **aplicativo** (app), que empacota relatórios e painéis para um público maior.

**Atualização.** No modo de Importação, os dados do serviço só mudam quando o modelo é atualizado. A **atualização agendada** é configurada nas opções do modelo semântico, no serviço. Se a fonte estiver dentro da rede da empresa, como um SQL Server local ou uma pasta de rede, é preciso um **gateway de dados local**: um programa instalado num computador da rede, que busca os dados e os envia ao serviço.

**Segurança em nível de linha (RLS).** Para que cada pessoa veja só uma parte dos dados no mesmo relatório, criam-se **funções** no modelo, com um filtro DAX, como `[regiao] = "Sul"`, ou um filtro dinâmico baseado no e-mail de quem está logado, com `USERPRINCIPALNAME()`. No serviço, cada pessoa ou grupo é associado a uma função. O filtro se propaga pelos relacionamentos do modelo. Uma segmentação de dados não é segurança, porque o usuário pode trocar a seleção.

## Modos de armazenamento: Importação, DirectQuery e Direct Lake

O modo de armazenamento define onde os dados ficam e como os visuais os consultam:

| Modo           | Como funciona                                                       | Vantagem                          | Cuidado                                   |
| -------------- | ------------------------------------------------------------------- | --------------------------------- | ----------------------------------------- |
| Importação     | Copia os dados para o modelo, comprimidos na memória                | Visuais muito rápidos, DAX completo | Dados só mudam na atualização; limite de tamanho |
| DirectQuery    | Cada visual gera consultas na fonte, na hora                        | Dados sempre atuais               | Depende da velocidade da fonte; algumas limitações de DAX |
| Direct Lake    | Lê as tabelas Delta do OneLake, carregando as colunas sob demanda   | Desempenho próximo da Importação, sem cópia agendada | Só para dados no OneLake (Fabric)        |
| Composto       | Mistura modos no mesmo modelo, tabela a tabela                      | Equilíbrio entre os dois mundos   | Mais complexo de manter                   |

Para a maioria dos relatórios, a Importação é o ponto de partida. O DirectQuery entra quando os dados precisam estar atualizados ao minuto ou são grandes demais para importar. O **Direct Lake** é o modo nativo do Microsoft Fabric: os dados ficam em tabelas Delta num lakehouse ou warehouse, e o modelo semântico os lê diretamente. É um dos assuntos centrais da prova DP-600.

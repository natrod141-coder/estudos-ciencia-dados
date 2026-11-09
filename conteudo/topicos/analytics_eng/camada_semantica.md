---
titulo: "Métricas e camada semântica"
modulo: analytics_eng
ordem: 3
horas: 6
estado: publicado
resumo: "Definir cada métrica uma vez só, para que pessoas e agentes de IA calculem o mesmo número."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Um número, três valores"
    tipo: leitura
    minutos: 8
  - id: a2
    titulo: "Medidas, dimensões e métricas"
    tipo: leitura
    minutos: 12
  - id: a3
    titulo: "Métricas que não somam"
    tipo: leitura
    minutos: 12
  - id: a4
    titulo: "Ferramentas de camada semântica"
    tipo: leitura
    minutos: 10
  - id: a5
    titulo: "Camada semântica e IA"
    tipo: leitura
    minutos: 10
  - id: a6
    titulo: "Vídeo de apoio: camada semântica e métricas"
    tipo: video
    minutos: 20
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Três painéis mostram três valores diferentes para a receita de março. O que uma camada semântica resolve?"
    opcoes: ["Deixa os painéis mais rápidos", "Escolhe automaticamente o painel mais confiável", "Define a receita uma vez só, em código, e todos os painéis, análises e assistentes pedem a métrica à camada, em vez de reescrever o SQL", "Apaga os painéis antigos"]
    correta: 2
    explicacao: "Os números divergem porque cada painel tem a sua própria definição escrita no seu próprio SQL. Com a camada semântica, a definição fica num lugar só, versionada e revisada, e todo consumidor recebe o mesmo número."
  - pergunta: "No modelo semântico de pedidos, o canal de venda, com os valores site, app e loja, é:"
    opcoes: ["Uma medida", "Uma dimensão", "Uma métrica de razão", "Um grão de tempo"]
    correta: 1
    explicacao: "Dimensões são as colunas pelas quais uma métrica pode ser aberta: receita por canal, por região, por status. Medidas são agregações, como a soma do valor, e métricas são o que se pede, construídas a partir das medidas."
  - pergunta: "O ticket médio de janeiro, fevereiro e março está calculado. Como obter o ticket médio do trimestre?"
    opcoes: ["Tirar a média dos três tickets mensais", "Somar os três tickets mensais", "Pegar a mediana dos três tickets", "Dividir a receita do trimestre pela quantidade de pedidos aprovados do trimestre"]
    correta: 3
    explicacao: "O ticket médio é uma razão, e razões não se agregam por média: um mês com poucos pedidos pesaria tanto quanto um mês cheio. A conta certa recalcula a razão sobre os totais do período pedido."
  - pergunta: "Uma loja teve 21 clientes compradores em janeiro, 23 em fevereiro e 25 em março. Quantos clientes compradores teve no trimestre?"
    opcoes: ["Não dá para saber pela soma: quem comprou em mais de um mês conta uma vez só, então é preciso contar de novo no trimestre inteiro", "69, a soma dos três meses", "23, a média dos três meses", "25, o maior dos três meses"]
    correta: 0
    explicacao: "Contagem distinta não é aditiva. Nos dados do desafio, a soma dos meses dá 69, mas o trimestre teve 38 clientes diferentes, porque muitos compraram em mais de um mês. A camada semântica recalcula a contagem no grão pedido."
  - pergunta: "O saldo em estoque de cada loja é medido no fim de cada mês. O que faz sentido somar?"
    opcoes: ["Os saldos dos três meses, para ter o estoque do trimestre", "Nada, saldo nunca pode ser somado", "Os saldos das lojas num mesmo mês, para ter o estoque da rede naquele mês", "Os saldos de todas as lojas em todos os meses"]
    correta: 2
    explicacao: "Saldo é semiaditivo: soma entre lojas, mas não ao longo do tempo. Janeiro mais fevereiro não é estoque de nada. No tempo, usa-se o último saldo do período ou a média."
  - pergunta: "Por que um assistente de IA erra menos quando consulta uma camada semântica em vez de escrever SQL livre sobre as tabelas?"
    opcoes: ["Porque a camada semântica usa um modelo de IA melhor", "Porque o SQL gerado fica mais curto", "Porque a camada semântica dispensa conferir os resultados", "Porque ele só escolhe métricas, dimensões e filtros de um catálogo com definições fixas, e o SQL é gerado pela camada, com a mesma regra usada no painel"]
    correta: 3
    explicacao: "Escrevendo SQL livre, o modelo precisa adivinhar joins, filtros e definições, como se a receita conta cancelados. Com a camada semântica, essas decisões já estão tomadas e testadas. Sobram menos escolhas, e o número bate com o do painel. Ainda vale conferir se ele escolheu a métrica certa para a pergunta."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Escreva a definição da métrica taxa de conversão do site para uma camada semântica: as medidas e os filtros, a fórmula, as dimensões e os grãos em que ela pode ser aberta, como ela se comporta ao agregar e a descrição que uma pessoa e um assistente de IA vão ler."
  rubrica:
    - "Define as medidas e a fórmula com precisão: o que é uma visita e o que é uma conversão, de que fonte vem cada uma, e quais filtros se aplicam, como excluir visitas de robôs ou pedidos cancelados."
    - "Classifica a métrica como não aditiva e diz como agregar: sempre recalculando a razão sobre os totais do grupo, e nunca pela média das taxas de dias ou de canais."
    - "Escreve uma descrição sem ambiguidade e lista as dimensões e os grãos permitidos, de preferência com um responsável pela definição."
  modelo: "Taxa de conversão do site é uma métrica de razão. O numerador é a medida sessões com compra: a contagem distinta de sessões do site que terminaram em pelo menos um pedido aprovado, sem contar pedidos cancelados nem sessões de robôs. O denominador é a medida sessões: a contagem distinta de sessões do site, também sem robôs. A fórmula é sessões com compra dividido por sessões, protegida contra divisão por zero. Ela pode ser aberta por dia, semana, mês, trimestre e ano, e pelas dimensões canal de aquisição, dispositivo e região do visitante. Não pode ser aberta por produto, porque uma sessão pode comprar vários produtos. A métrica não é aditiva: a taxa de um mês é o total de sessões com compra do mês dividido pelo total de sessões do mês, e nunca a média das taxas diárias, nem a soma das taxas de cada canal. A descrição: porcentagem das sessões do site, sem robôs, que terminaram em pelo menos um pedido aprovado. Não inclui o aplicativo nem as lojas físicas. Responsável: time de produto digital."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Uma camada semântica de bolso"
  descricao: "As métricas da loja já estão definidas num modelo semântico, com medidas, dimensões e métricas simples e de razão. Você vai escrever o compilador que transforma um pedido como receita e ticket médio por região, por mês, só no app, na consulta SQL certa, conferida no DuckDB contra contas feitas em pandas."
  pasta: "desafios/analytics_eng/camada_semantica"
  testes: 10
  tempo: "2 h"
  ferramentas: "VS Code, Python 3.11 ou superior, DuckDB, pandas e pytest"
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
    - titulo: "Leia o enunciado e o modelo semântico"
      descricao: "Abra desafios/analytics_eng/camada_semantica/README.md e depois modelo_semantico.json. Os pedidos estão em data/pedidos.csv."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "As funções ler_modelo, criar_banco e consultar já estão prontas. Cada função tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def sql_da_medida(medida):"
        - "def sql_da_metrica(modelo, nome):"
        - "def expressao_de_tempo(coluna, grao):"
        - "def compilar(modelo, metricas, por=(), grao=None, filtros=()):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "Os testes rodam o SQL gerado no DuckDB e comparam com contas feitas em pandas."
      comandos:
        - "cd desafios/analytics_eng/camada_semantica"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/camada_semantica"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de camada semântica"'
        - "git push -u origin desafio/camada_semantica"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Camada semântica", en: "semantic layer" }
  - { pt: "Modelo semântico", en: "semantic model" }
  - { pt: "Medida", en: "measure" }
  - { pt: "Dimensão", en: "dimension" }
  - { pt: "Métrica", en: "metric" }
  - { pt: "Grão de tempo", en: "time grain" }
  - { pt: "Métrica aditiva", en: "additive metric" }
  - { pt: "Métrica semiaditiva", en: "semi-additive metric" }
  - { pt: "Métrica não aditiva", en: "non-additive metric" }
  - { pt: "Métrica de razão", en: "ratio metric" }
  - { pt: "Contagem distinta", en: "distinct count" }
  - { pt: "Governança de métricas", en: "metric governance" }
  - { pt: "Fonte única da verdade", en: "single source of truth" }
---

## Um número, três valores

Uma cena comum em reunião de resultados: o painel do marketing diz que a receita de março foi de R$ 1,2 milhão, o do financeiro diz R$ 1,05 milhão, e o do comercial, R$ 1,15 milhão. A discussão que se segue não é sobre o negócio, mas sobre qual número está certo.

Na maioria das vezes, todos estão certos, cada um com a sua definição. Um painel conta os pedidos cancelados, outro não. Um usa a data do pedido, outro a do pagamento. Um inclui o frete. Cada painel, cada planilha e cada notebook tem o seu próprio SQL, e cada SQL carrega, escondida, uma definição diferente de receita.

A **camada semântica** ataca o problema na raiz. As métricas são definidas **uma vez só**, em código, versionado e revisado como qualquer modelo do dbt. Quem precisa de um número, seja um painel, uma análise, uma aplicação ou um assistente de IA, não escreve mais o SQL: pede à camada "receita por região, por mês", e ela gera a consulta a partir da definição oficial. Mudou a regra? Muda num lugar, e todos os números mudam juntos.

A camada semântica resolve o "como calcular". O "o que é receita" continua sendo uma decisão de negócio, tomada com as áreas que usam o número. O trabalho de quem cuida da camada é registrar essa decisão sem ambiguidade, com uma descrição que qualquer pessoa entenda.

## Medidas, dimensões e métricas

Uma camada semântica descreve as tabelas com quatro ideias:

- **Dimensões**: as colunas pelas quais um número pode ser aberto, como região, canal e status. A **dimensão de tempo** é especial, porque pode ser vista em vários **grãos**: dia, semana, mês, trimestre, ano.
- **Medidas**: as agregações básicas sobre as colunas: a soma do valor, a contagem de pedidos, a contagem distinta de clientes.
- **Métricas**: o que as pessoas pedem, construído a partir das medidas. Uma métrica **simples** é uma medida, às vezes com um filtro. Uma métrica de **razão** divide uma métrica por outra. Há ainda métricas **derivadas**, que combinam outras, como receita menos devoluções, e **acumuladas**, como a receita acumulada no ano.
- **Entidades e relacionamentos**: as chaves que ligam as tabelas, como o cliente de cada pedido. Com elas, a camada sabe fazer os joins sozinha, no grão certo, sem o fan-out que você já conhece.

No desafio deste tópico, as definições ficam num arquivo JSON. Um trecho:

```json
"receita": {
  "tipo": "simples",
  "medida": "valor_vendido",
  "filtro": "status = 'aprovado'"
},
"ticket_medio": {
  "tipo": "razao",
  "numerador": "receita",
  "denominador": "pedidos_aprovados"
}
```

A partir delas, o pedido "receita e ticket médio por região, por mês, só no app" vira esta consulta:

```sql
SELECT
    date_trunc('month', data_pedido) AS mes,
    regiao,
    SUM(valor) FILTER (WHERE status = 'aprovado') AS receita,
    CAST(SUM(valor) FILTER (WHERE status = 'aprovado') AS DOUBLE)
        / NULLIF(COUNT(*) FILTER (WHERE status = 'aprovado'), 0)
        AS ticket_medio
FROM pedidos
WHERE canal = 'app'
GROUP BY 1, 2
ORDER BY 1, 2
```

Ninguém precisou lembrar que a receita exclui os cancelados, nem como se calcula o ticket médio: as duas regras vieram da definição. O `FILTER (WHERE ...)` faz a agregação considerar só as linhas do filtro, e o `NULLIF` evita a divisão por zero num grupo sem pedidos aprovados.

## Métricas que não somam

O ponto mais delicado de qualquer métrica é o que acontece quando ela é agregada. As métricas se dividem em três grupos:

- **Aditivas** somam em qualquer dimensão: a receita das regiões soma a receita total, e a dos meses soma a do trimestre. Somas e contagens simples são aditivas.
- **Semiaditivas** somam em algumas dimensões, mas não no tempo. O saldo em estoque das lojas soma o estoque da rede, mas o estoque de janeiro mais o de fevereiro não é estoque de nada. No tempo, usa-se o último valor do período ou a média.
- **Não aditivas** não somam em dimensão nenhuma: razões, como ticket médio, taxa de conversão e margem, contagens distintas, médias, medianas e percentis.

Para as não aditivas, a regra é **recalcular no grão pedido**, a partir das medidas. Nos dados do desafio, a taxa de cancelamento por região é esta:

| Região   | Pedidos | Cancelados | Taxa  |
| -------- | ------- | ---------- | ----- |
| Nordeste | 22      | 5          | 22,7% |
| Norte    | 19      | 2          | 10,5% |
| Sudeste  | 62      | 11         | 17,7% |
| Sul      | 24      | 4          | 16,7% |
| Total    | 127     | 22         | 17,3% |

A média das quatro taxas dá 16,9%, mas a taxa da loja é 22 cancelados em 127 pedidos: 17,3%. A média trata o Norte, com 19 pedidos, como se pesasse o mesmo que o Sudeste, com 62. A diferença aqui é pequena, mas com grupos mais desiguais ela cresce, e é o tipo de erro que ninguém percebe olhando o painel.

A contagem distinta engana ainda mais. Nos mesmos dados, a loja teve 21 clientes compradores em janeiro, 23 em fevereiro e 25 em março. A soma dá 69, mas o trimestre teve só 38 clientes diferentes, porque muitos compraram em mais de um mês. Somar contagens distintas conta a mesma pessoa várias vezes.

É aqui que a camada semântica mais ajuda: como ela guarda as medidas, e não os resultados, sempre recalcula a razão e a contagem distinta sobre os totais do grupo pedido. Quem consulta não precisa lembrar dessas regras.

## Ferramentas de camada semântica

Você já usou uma camada semântica sem chamá-la assim: o **modelo semântico do Power BI**. As tabelas, os relacionamentos e as medidas DAX definidas uma vez servem a todos os relatórios construídos sobre o modelo. A diferença das ferramentas abaixo é que elas não ficam presas a uma ferramenta de BI:

- **dbt Semantic Layer e MetricFlow**: modelos semânticos e métricas definidos em YAML, dentro do projeto dbt, ao lado dos modelos que alimentam as métricas. O MetricFlow, o motor que gera o SQL, virou projeto de código aberto em 2025.
- **LookML**, a camada semântica do Looker, e o **Cube**, de código aberto, que expõe as métricas por APIs para painéis e aplicações.
- **Os próprios bancos**: plataformas como Snowflake e Databricks passaram a oferecer camadas semânticas dentro do banco, com definições de métricas guardadas junto com as tabelas.

Com tantas opções, surgiu a necessidade de um formato comum. A especificação Open Semantic Interchange, lançada em 2025 com a participação de empresas como Snowflake, Salesforce, Databricks e dbt Labs, define um formato neutro para métricas, dimensões e relacionamentos. Em 2026, ela foi aceita na incubadora da Apache Software Foundation com o nome de **Apache Ossie**. A ideia é escrever as definições uma vez e usá-las em várias ferramentas.

Seja qual for a ferramenta, as perguntas para definir uma métrica são as mesmas: de quais medidas ela vem, com que filtros, em que dimensões e grãos pode ser aberta, como se comporta ao agregar, e quem responde pela definição.

## Camada semântica e IA

No módulo de fundamentos de IA, você viu que um modelo de linguagem escrevendo SQL livre sobre tabelas brutas precisa adivinhar muita coisa: que tabelas juntar, que filtros aplicar, se a receita conta os cancelados. Cada adivinhação é uma chance de um número plausível e errado.

Com uma camada semântica, o trabalho do assistente muda. Em vez de escrever SQL, ele escolhe, num catálogo de métricas com definições fixas, quais métricas, dimensões, grãos e filtros respondem à pergunta. Algo como:

```json
{"metricas": ["receita", "ticket_medio"], "por": ["regiao"], "grao": "mes"}
```

A camada gera o SQL a partir da definição oficial, e o número que o assistente devolve é o mesmo do painel. Sobram menos escolhas para errar, e as que sobram são fáceis de conferir: basta ler quais métricas ele pediu.

Duas consequências práticas:

- **A descrição faz parte da definição.** O assistente escolhe a métrica lendo o nome e a descrição. "Receita: soma do valor dos pedidos aprovados, sem frete, pela data do pedido" orienta a escolha. "Receita: receita" não ajuda ninguém, nem pessoas nem modelos.
- **A camada vira uma ferramenta do agente.** Camadas semânticas já são oferecidas a assistentes de IA como ferramentas, inclusive por meio do protocolo MCP, que você vai estudar no módulo de IA sobre dados. O assistente lista as métricas disponíveis, escolhe e consulta.

A conferência continua necessária: o assistente pode escolher a métrica errada para a pergunta, ou esquecer um filtro que a pergunta pedia. Mas o erro de definição, que é o mais difícil de perceber, sai de cena.

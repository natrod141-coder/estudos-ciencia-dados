---
titulo: "Tipos de gráficos"
modulo: estatistica
ordem: 5
horas: 4
estado: publicado
resumo: "Barras, linhas, pontos e outros: qual gráfico usar para cada pergunta."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Comece pela pergunta"
    tipo: leitura
    minutos: 6
  - id: a2
    titulo: "Comparação, evolução, distribuição e relação"
    tipo: leitura
    minutos: 15
  - id: a3
    titulo: "Parte de um todo: pizza e barras empilhadas"
    tipo: leitura
    minutos: 8
  - id: a4
    titulo: "Gráficos que enganam"
    tipo: leitura
    minutos: 10
  - id: a5
    titulo: "Primeiros gráficos com matplotlib"
    tipo: leitura
    minutos: 12
  - id: a6
    titulo: "Vídeo de apoio sobre escolha de gráficos"
    tipo: video
    minutos: 15
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Você quer mostrar como o número de usuários ativos mudou semana a semana ao longo de um ano. Qual gráfico é o mais indicado?"
    opcoes: ["Pizza", "Linha", "Histograma", "Dispersão"]
    correta: 1
    explicacao: "Evolução no tempo pede gráfico de linha, com o tempo no eixo horizontal, da esquerda para a direita. A linha liga os pontos e deixa ver tendência, sazonalidade e mudanças bruscas. Com 52 semanas, barras ficariam poluídas, e pizza não mostra ordem no tempo."
  - pergunta: "Qual gráfico mostra melhor a distribuição do tempo de entrega de 5.000 pedidos?"
    opcoes: ["Histograma", "Barras com o tempo de cada pedido", "Pizza", "Linha ligando os pedidos na ordem em que chegaram"]
    correta: 0
    explicacao: "O histograma agrupa os valores em faixas e mostra quantos pedidos caem em cada faixa. Com ele se vê onde os dados se concentram, se há assimetria e se há valores atípicos. Uma barra por pedido daria 5.000 barras sem padrão visível."
  - pergunta: "Um gráfico de barras compara o faturamento de duas lojas: R$ 980 mil e R$ 1,02 milhão. O eixo vertical começa em R$ 950 mil, e a segunda barra fica com mais que o dobro da altura da primeira. Qual é o problema?"
    opcoes: ["Nenhum, o eixo foi ajustado para destacar a diferença", "Deveria ser um gráfico de pizza", "As barras deveriam ser horizontais", "O eixo truncado exagera a diferença: em barras, o comprimento representa o valor, então o eixo precisa começar no zero"]
    correta: 3
    explicacao: "Quem lê um gráfico de barras compara o comprimento das barras. Se o eixo começa em 950 mil, a barra de 1,02 milhão fica com mais que o dobro do comprimento da de 980 mil, embora a diferença real seja de cerca de 4%. Em barras, o eixo dos valores começa sempre no zero."
  - pergunta: "Para investigar se o tempo de uso do app está relacionado ao valor gasto pelo cliente, qual gráfico usar?"
    opcoes: ["Barras empilhadas", "Linha", "Dispersão", "Pizza"]
    correta: 2
    explicacao: "Relação entre duas variáveis quantitativas pede gráfico de dispersão: cada cliente vira um ponto, com o tempo de uso num eixo e o gasto no outro. Se os pontos sobem juntos, há uma relação positiva. O gráfico também mostra grupos e valores atípicos."
  - pergunta: "Em qual situação um gráfico de pizza é aceitável?"
    opcoes: ["Para mostrar a parte de um todo com poucas categorias, como duas ou três, e diferenças grandes entre elas", "Para comparar o faturamento dos 12 meses do ano", "Sempre que os valores forem porcentagens", "Para mostrar a evolução de uma participação ao longo do tempo"]
    correta: 0
    explicacao: "O olho compara mal ângulos e áreas. Com duas ou três fatias bem diferentes, como 70% contra 30%, a pizza funciona. Com muitas fatias, ou fatias de tamanho parecido, fica difícil dizer qual é maior, e um gráfico de barras resolve melhor."
  - pergunta: "Quatro conjuntos de dados têm a mesma média, a mesma variância e a mesma correlação entre x e y. O que se pode concluir sobre a forma deles?"
    opcoes: ["Que os quatro têm a mesma forma", "Que a correlação foi calculada errado", "Nada: conjuntos com as mesmas medidas podem ter formas completamente diferentes, e só o gráfico mostra isso", "Que os quatro seguem uma distribuição normal"]
    correta: 2
    explicacao: "É o quarteto de Anscombe: quatro conjuntos com médias, variâncias e correlação praticamente iguais. Um tem relação linear com ruído, outro é uma curva, e os outros dois têm padrões moldados por um único valor atípico. Medidas resumem, mas escondem a forma. Faça o gráfico antes de concluir."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Um colega apresentou numa reunião um gráfico de pizza em 3D com 9 fatias, uma para o faturamento de cada região. Explique por que esse gráfico dificulta a leitura e proponha uma alternativa."
  rubrica:
    - "Explica que o olho humano compara mal ângulos e áreas, e que com 9 fatias fica difícil dizer qual é maior entre fatias de tamanho parecido."
    - "Aponta que o efeito 3D distorce os tamanhos: as fatias da frente parecem maiores do que são."
    - "Propõe um gráfico de barras, de preferência horizontal e ordenado do maior para o menor, com o eixo dos valores começando no zero."
  modelo: "A pizza obriga a comparar ângulos e áreas, e o olho humano faz isso mal. Com 9 fatias, várias ficam com tamanhos parecidos, e é quase impossível dizer qual região faturou mais entre elas sem ler os números. O 3D piora: a inclinação faz as fatias da frente parecerem maiores do que as de trás, e o gráfico passa uma ideia errada. Eu trocaria por um gráfico de barras horizontais, uma barra por região, ordenadas da que mais faturou para a que menos faturou, com o eixo começando no zero. Assim a comparação vira uma comparação de comprimentos, que é a mais fácil de ler."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "O gráfico certo para cada pergunta"
  descricao: "A gerente de uma loja online quer um relatório do semestre com quatro perguntas. Para cada uma, você vai escolher o tipo de gráfico que responde melhor, preparar os dados com pandas e desenhá-lo com matplotlib, seguindo as regras que evitam gráficos enganosos."
  pasta: "desafios/estatistica/tipos_graficos"
  testes: 8
  tempo: "1 h 30 min"
  ferramentas: "VS Code, Python 3.11 ou superior, pandas, matplotlib e pytest"
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
      descricao: "Abra o terminal do VS Code com Ctrl+` (acento grave). Depois use Ctrl+Shift+P, Python: Select Interpreter, e escolha o .venv. Se o ambiente já existia, rode de novo o pip install: este desafio usa o matplotlib."
      comandos:
        - "# Linux ou macOS"
        - "python3 -m venv .venv"
        - "source .venv/bin/activate"
        - "# Windows (PowerShell)"
        - "python -m venv .venv"
        - '.venv\Scripts\Activate.ps1'
        - "pip install -r desafios/requirements.txt"
    - titulo: "Leia o enunciado e conheça os dados"
      descricao: "Abra desafios/estatistica/tipos_graficos/README.md. Os dados estão em data/vendas.csv: uma linha por pedido, com o número, a data, a categoria, a quantidade de itens e o valor em reais."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "Cada função de gráfico traz a pergunta que o gráfico precisa responder, e escolher o tipo de gráfico é parte do exercício. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def vendas_por_categoria(vendas):"
        - "def vendas_por_mes(vendas):"
        - "def grafico_categorias(vendas):"
        - "def grafico_evolucao(vendas):"
        - "def grafico_distribuicao(vendas):"
        - "def grafico_relacao(vendas):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/estatistica/tipos_graficos"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/tipos_graficos"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de tipos de gráficos"'
        - "git push -u origin desafio/tipos_graficos"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Gráfico de barras", en: "bar chart" }
  - { pt: "Gráfico de linha", en: "line chart" }
  - { pt: "Histograma", en: "histogram" }
  - { pt: "Gráfico de dispersão", en: "scatter plot" }
  - { pt: "Diagrama de caixa", en: "box plot" }
  - { pt: "Gráfico de pizza", en: "pie chart" }
  - { pt: "Barras empilhadas", en: "stacked bar chart" }
  - { pt: "Eixo", en: "axis" }
  - { pt: "Rótulo", en: "label" }
  - { pt: "Legenda", en: "legend" }
  - { pt: "Eixo truncado", en: "truncated axis" }
  - { pt: "Quarteto de Anscombe", en: "Anscombe's quartet" }
---

## Comece pela pergunta

Um gráfico é a resposta visual a uma pergunta. Os mesmos dados de vendas podem responder "qual categoria vendeu mais?", "as vendas estão crescendo?" ou "a maioria dos pedidos é barata ou cara?", e cada pergunta pede um gráfico diferente. Por isso, antes de abrir qualquer ferramenta, escreva a pergunta numa frase.

Quase toda pergunta cai em um destes cinco tipos:

| A pergunta é sobre...     | Exemplo                                          | Gráfico indicado                  |
| ------------------------- | ------------------------------------------------ | --------------------------------- |
| Comparar categorias       | Qual região faturou mais?                        | Barras                            |
| Evolução no tempo         | Como as vendas mudaram mês a mês?                | Linha                             |
| Distribuição de valores   | Os pedidos costumam ser baratos ou caros?        | Histograma ou diagrama de caixa   |
| Relação entre variáveis   | Quem usa mais o app gasta mais?                  | Dispersão                         |
| Parte de um todo          | Quanto cada canal representa das vendas?         | Barras, barras empilhadas ou, com poucas partes, pizza |

Um bom teste para o resultado: alguém que nunca viu os dados precisa entender a resposta em poucos segundos, só olhando o gráfico e o título.

## Comparação, evolução, distribuição e relação

### Comparar categorias: barras

O comprimento da barra representa o valor, e comparar comprimentos é algo que o olho faz muito bem. Três regras:

- **O eixo dos valores começa no zero.** Se começar em outro valor, o comprimento das barras deixa de ser proporcional ao valor e as diferenças parecem maiores do que são.
- **Ordene as barras pelo valor**, do maior para o menor, a não ser que as categorias tenham uma ordem própria, como faixas etárias ou dias da semana.
- **Use barras horizontais** quando os nomes das categorias forem longos ou houver muitas categorias. Os nomes ficam legíveis sem precisar girar o texto.

### Evolução no tempo: linha

O tempo fica no eixo horizontal, da esquerda para a direita, e a linha liga os pontos, mostrando tendência, sazonalidade e mudanças bruscas. Diferente das barras, o eixo de um gráfico de linha não precisa começar no zero, porque o que importa é a variação. Mas cuidado para não ampliar tanto a escala que uma oscilação pequena pareça uma crise. Para comparar séries, use poucas linhas, até quatro ou cinco, e escreva o nome de cada uma perto da própria linha, em vez de depender da legenda.

### Distribuição: histograma e diagrama de caixa

O **histograma** divide os valores em faixas de mesma largura e desenha uma barra para cada faixa, com altura igual à quantidade de valores nela. As barras ficam encostadas, porque as faixas são contínuas. Com ele se vê onde os dados se concentram, se a distribuição é simétrica ou assimétrica e se há valores atípicos. O número de faixas muda a leitura: poucas escondem detalhes, e muitas deixam o desenho serrilhado.

O **diagrama de caixa** (boxplot) resume a distribuição em cinco números: mínimo, primeiro quartil, mediana, terceiro quartil e máximo, e marca os valores atípicos. Ele brilha na comparação de distribuições entre grupos, como o tempo de entrega de cada centro de distribuição lado a lado. O tópico de tabelas de frequência detalha os dois gráficos.

### Relação entre duas variáveis: dispersão

Cada observação vira um ponto, com uma variável no eixo horizontal e outra no vertical. Olhe para a direção (os pontos sobem ou descem juntos?), a forma (reta ou curva?), os grupos e os pontos isolados. Com muitos pontos sobrepostos, use transparência para ver onde eles se acumulam. E lembre: um padrão na dispersão mostra associação, não causa.

## Parte de um todo: pizza e barras empilhadas

O gráfico de pizza é o mais usado e o mais criticado. Um estudo clássico de William Cleveland e Robert McGill, de 1984, mostrou que as pessoas comparam com precisão posições e comprimentos, mas erram bastante ao comparar ângulos e áreas. Numa pizza com fatias de 22% e 25%, é difícil dizer qual é maior.

A pizza funciona quando há **duas ou três partes** com diferenças claras, como 70% das vendas no site e 30% na loja física. Com mais partes, prefira:

- **Barras ordenadas**, uma por parte, mostrando a porcentagem.
- **Barras empilhadas em 100%** para comparar a composição entre grupos ou ao longo do tempo, como a participação de cada canal de venda em cada trimestre.

## Gráficos que enganam

Um gráfico pode ter dados corretos e passar uma conclusão errada. Os erros mais comuns:

- **Eixo truncado em barras.** Duas lojas com R$ 980 mil e R$ 1,02 milhão parecem muito diferentes se o eixo começar em R$ 950 mil.
- **Efeito 3D.** A perspectiva distorce tamanhos: as fatias ou barras da frente parecem maiores.
- **Dois eixos verticais com escalas diferentes.** Ajustando as escalas, dá para fazer quaisquer duas séries parecerem andar juntas.
- **Cores demais.** Use cor para destacar o que importa, e não para decorar. Uma cor de destaque e o resto em cinza costuma funcionar melhor que um arco-íris.
- **Falta de título, rótulos e unidades.** Sem o eixo dizer "Faturamento (R$ mil)", o leitor precisa adivinhar.

O motivo para fazer gráficos, e não só calcular medidas, é o **quarteto de Anscombe**. São quatro conjuntos de dados criados pelo estatístico Francis Anscombe em 1973. Os quatro têm praticamente a mesma média de x (9), a mesma média de y (7,5), as mesmas variâncias e a mesma correlação (0,82). Nos gráficos de dispersão, são completamente diferentes: uma relação linear com ruído, uma curva, uma reta perfeita com um ponto fora e um grupo vertical com um único ponto distante. As medidas escondem a forma, e o gráfico mostra.

## Primeiros gráficos com matplotlib

O matplotlib é a biblioteca de gráficos mais usada em Python. O padrão é sempre o mesmo: criar a figura e o eixo, desenhar, colocar título e rótulos.

```python
import matplotlib.pyplot as plt
import pandas as pd

vendas = pd.read_csv("data/vendas.csv", parse_dates=["data"])

# comparar categorias: barras horizontais, a maior no topo
totais = vendas.groupby("categoria")["valor"].sum()
# o barh desenha de baixo para cima: ordem crescente
totais = totais.sort_values()
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(totais.index, totais.values)
ax.set_title("Faturamento por categoria, 1º semestre")
ax.set_xlabel("Faturamento (R$)")
ax.set_ylabel("Categoria")
fig.savefig("categorias.png", dpi=150, bbox_inches="tight")
```

Os outros tipos trocam só a linha do desenho. Cada um vai num `fig, ax = plt.subplots()` novo:

```python
meses = vendas["data"].dt.strftime("%Y-%m")
mensal = vendas.groupby(meses)["valor"].sum()
por_categoria = vendas.groupby("categoria")["valor"]

ax.plot(mensal.index, mensal.values, marker="o")   # linha
ax.hist(vendas["valor"], bins=20)                  # histograma
ax.scatter(vendas["itens"], vendas["valor"])       # dispersão
ax.boxplot([valores for _, valores in por_categoria])  # caixa
```

O pandas tem um atalho que chama o matplotlib por baixo: `totais.plot.barh()`, `vendas["valor"].plot.hist(bins=20)`. É ótimo para explorar os dados rapidamente. Para um gráfico que vai para um relatório, o controle fino do matplotlib compensa.

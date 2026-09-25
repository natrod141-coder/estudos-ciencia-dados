---
titulo: "Medidas de tendência central"
modulo: estatistica
ordem: 1
horas: 3
estado: publicado
resumo: "Média, mediana e moda: como calcular, o que cada uma diz e quando cada uma engana."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "O que é tendência central"
    tipo: leitura
    minutos: 8
  - id: a2
    titulo: "Média, mediana e moda: como calcular"
    tipo: leitura
    minutos: 12
  - id: a3
    titulo: "Quando a média engana: valores atípicos e assimetria"
    tipo: leitura
    minutos: 10
  - id: a4
    titulo: "Vídeo de apoio sobre medidas de tendência central"
    tipo: video
    minutos: 15
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Cinco contratos fecharam com os valores 10, 12, 12, 15 e 61 (em mil reais). Qual é a mediana?"
    opcoes: ["22", "12", "15", "61"]
    correta: 1
    explicacao: "A mediana é o valor central dos dados em ordem crescente. Com cinco valores, é o terceiro: 12. O número 22 é a média, puxada para cima pelo contrato de 61."
  - pergunta: "Entre as medidas abaixo, qual é a menos afetada por um valor extremo no conjunto de dados?"
    opcoes: ["Média aritmética", "Média ponderada", "Soma dos valores", "Mediana"]
    correta: 3
    explicacao: "A mediana depende só da posição central dos dados ordenados. Mudar o maior valor de 61 para 610 não altera a mediana, mas altera muito a média."
  - pergunta: "Uma pesquisa registrou a cor do carro de 200 clientes (branco, preto, prata e outras). Qual medida de tendência central faz sentido calcular?"
    opcoes: ["Média", "Mediana", "Moda", "Nenhuma, porque a variável não é numérica"]
    correta: 2
    explicacao: "Cor é uma variável qualitativa nominal: não há como somar nem ordenar as cores. A moda, a cor mais frequente, é a única medida de tendência central que se aplica."
  - pergunta: "Em uma distribuição com forte assimetria à direita, com cauda longa de valores altos (como salários), como costumam ficar a média e a mediana?"
    opcoes: ["Média menor que a mediana", "Média maior que a mediana", "Média igual à mediana", "Não dá para saber sem calcular"]
    correta: 1
    explicacao: "Os poucos valores muito altos puxam a média para cima, enquanto a mediana quase não se move. Por isso, na assimetria à direita, a média fica acima da mediana."
  - pergunta: "Quantas modas têm os dados 3, 5, 5, 7, 9, 9?"
    opcoes: ["Uma moda, o 5", "Duas modas, o 5 e o 9", "Nenhuma moda", "Três modas"]
    correta: 1
    explicacao: "O 5 e o 9 aparecem duas vezes cada, mais do que qualquer outro valor. Um conjunto com duas modas é chamado de bimodal."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Numa empresa pequena, o dono ganha muito mais do que os funcionários. Explique com suas palavras por que a mediana dos salários descreve melhor o salário típico do que a média."
  rubrica:
    - "Diz que o salário do dono é um valor atípico (outlier) que puxa a média para cima."
    - "Explica que a mediana depende da posição central dos dados ordenados, e não do tamanho dos valores extremos."
    - "Conclui que a mediana representa melhor o salário de um funcionário comum, enquanto a média mostraria um valor que quase ninguém recebe."
  modelo: "O salário do dono é muito maior que os demais, então é um valor atípico. Como a média soma todos os valores, esse salário alto a puxa para cima, e ela acaba mostrando um valor que quase nenhum funcionário recebe. A mediana é o valor do meio dos salários em ordem: ela olha a posição, e não o tamanho dos extremos. Por isso o salário do dono não a desloca, e ela mostra melhor o que um funcionário comum ganha."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Resumo estatístico de pedidos"
  descricao: "Uma loja online exportou os valores de 20 pedidos de um dia. Você vai calcular média, mediana e moda sem usar bibliotecas prontas, detectar valores atípicos pela regra do intervalo interquartil e decidir qual medida descreve melhor o pedido típico."
  pasta: "desafios/estatistica/tendencia_central"
  testes: 8
  tempo: "1 h 30 min"
  ferramentas: "VS Code, Python 3.11 ou superior, pandas e pytest"
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
      descricao: "Abra desafios/estatistica/tendencia_central/README.md. Os dados estão em data/pedidos.csv: uma linha por pedido, com o número do pedido e o valor em reais."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "Cada função tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def media(valores):"
        - "def mediana(valores):"
        - "def moda(valores):"
        - "def tem_atipico(valores):"
        - "def escolher_medida(valores):"
        - "def resumo_pedidos(caminho_csv):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/estatistica/tendencia_central"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/tendencia_central"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de tendência central"'
        - "git push -u origin desafio/tendencia_central"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Média", en: "mean" }
  - { pt: "Mediana", en: "median" }
  - { pt: "Moda", en: "mode" }
  - { pt: "Valor atípico", en: "outlier" }
  - { pt: "Assimetria", en: "skewness" }
  - { pt: "Distribuição", en: "distribution" }
  - { pt: "Quartil", en: "quartile" }
  - { pt: "Intervalo interquartil", en: "interquartile range (IQR)" }
---

## O que é tendência central

Ao olhar para um conjunto de dados, a primeira pergunta costuma ser: qual é um valor típico? As medidas de tendência central respondem a isso com um único número que indica onde os dados se concentram. As três mais usadas são a média, a mediana e a moda.

Nenhuma delas é a resposta certa em todos os casos. Escolher a medida errada é uma das formas mais comuns de tirar uma conclusão enganosa de dados corretos.

## Média, mediana e moda

A **média aritmética** é a soma dos valores dividida pela quantidade de valores. Para 10, 12, 12, 15 e 61, a soma é 110 e a média é 110 ÷ 5 = 22.

A **mediana** é o valor central depois de ordenar os dados. Com uma quantidade ímpar de valores, é o do meio: nos dados acima, 12. Com uma quantidade par, é a média dos dois valores do meio: para 3, 5, 7 e 9, a mediana é (5 + 7) ÷ 2 = 6.

A **moda** é o valor que mais se repete. Pode haver mais de uma, e o conjunto é chamado de bimodal quando há duas. Também pode não haver nenhuma, quando todos os valores aparecem uma única vez.

| Medida  | Como se calcula                  | Serve para                         | Sofre com valores extremos? |
| ------- | -------------------------------- | ---------------------------------- | --------------------------- |
| Média   | Soma dos valores ÷ quantidade    | Variáveis quantitativas            | Sim                         |
| Mediana | Valor central dos dados ordenados | Quantitativas e ordinais           | Não                         |
| Moda    | Valor mais frequente             | Qualquer tipo, inclusive categorias | Não                         |

## Quando a média engana

Volte aos cinco contratos: 10, 12, 12, 15 e 61. A média é 22, mas quatro dos cinco contratos valem 15 ou menos. O valor 22 não representa nenhum deles, porque o contrato de 61 puxou a média para cima. Um valor muito distante dos demais é chamado de **valor atípico** (em inglês, *outlier*).

Isso acontece sempre que a distribuição é **assimétrica à direita**, com poucos valores muito altos e a maioria concentrada embaixo. Salários, preços de imóveis e tempos de entrega costumam ser assim. Nesses casos, a média fica acima da mediana, e a mediana descreve melhor o caso típico.

Em distribuições simétricas e sem valores atípicos, a média e a mediana ficam próximas. Por isso, um bom hábito é calcular as duas e comparar: se forem muito diferentes, há assimetria ou valores atípicos, e vale investigar antes de tirar conclusões.

**Qual medida usar, conforme o tipo da variável:**

- Qualitativa nominal, como cor ou cidade: a moda.
- Qualitativa ordinal, como satisfação em baixa, média e alta: a mediana ou a moda.
- Quantitativa simétrica e sem valores atípicos: a média.
- Quantitativa com assimetria ou valores atípicos: a mediana.

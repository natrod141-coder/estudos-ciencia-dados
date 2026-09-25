---
titulo: "Tabelas de frequência"
modulo: estatistica
ordem: 6
horas: 3
estado: publicado
resumo: "Frequências, histograma e boxplot para enxergar a distribuição."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Frequência absoluta, relativa e acumulada"
    tipo: leitura
    minutos: 10
  - id: a2
    titulo: "Dados contínuos: classes e histograma"
    tipo: leitura
    minutos: 12
  - id: a3
    titulo: "Resumo de cinco números e diagrama de caixa"
    tipo: leitura
    minutos: 12
  - id: a4
    titulo: "Vídeo de apoio sobre histograma e boxplot"
    tipo: video
    minutos: 15
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Numa pesquisa com 200 clientes, 50 deram nota 4. Qual é a frequência relativa da nota 4?"
    opcoes: ["50", "4%", "25%", "0,4"]
    correta: 2
    explicacao: "A frequência relativa é a frequência absoluta dividida pelo total: 50 ÷ 200 = 0,25, ou 25%. O 50 é a frequência absoluta, a contagem."
  - pergunta: "Numa tabela de notas de 1 a 5, a frequência relativa acumulada da nota 3 é 40%. O que isso significa?"
    opcoes: ["40% dos clientes deram exatamente nota 3", "40% dos clientes deram nota 3 ou menos", "40% dos clientes deram nota maior que 3", "A nota 3 é a mediana"]
    correta: 1
    explicacao: "A frequência acumulada soma tudo até aquele valor: notas 1, 2 e 3. Então 40% deram nota 3 ou menos, e os outros 60% deram 4 ou 5. A nota 3 não é a mediana, porque a mediana é o valor em que a acumulada passa de 50%."
  - pergunta: "Pela regra de Sturges, quantas classes usar num histograma de 200 valores?"
    opcoes: ["14", "5", "9", "200"]
    correta: 2
    explicacao: "A regra de Sturges dá 1 + log₂(n), arredondado para cima. Como log₂(200) ≈ 7,6, o resultado é 1 + 7,6 = 8,6, arredondado para 9 classes. É um ponto de partida: vale testar alguns valores próximos e ver qual mostra melhor a forma dos dados."
  - pergunta: "Num diagrama de caixa (boxplot), o que a caixa representa?"
    opcoes: ["Os 50% centrais dos dados, do primeiro ao terceiro quartil, com a mediana marcada dentro", "A média mais ou menos um desvio padrão", "O intervalo entre o menor e o maior valor", "A faixa onde ficam os valores atípicos"]
    correta: 0
    explicacao: "A caixa vai do primeiro quartil (Q1) ao terceiro (Q3), e a linha dentro dela é a mediana. A altura da caixa é o intervalo interquartil. Os bigodes se estendem até os dados mais extremos que não são atípicos, e os atípicos aparecem como pontos isolados."
  - pergunta: "Os tempos de atendimento de um SAC têm Q1 = 13 min e Q3 = 20 min. Pela regra de 1,5 × IQR, acima de quanto um tempo é considerado atípico?"
    opcoes: ["20 min", "27 min", "33 min", "30,5 min"]
    correta: 3
    explicacao: "O IQR é Q3 − Q1 = 7 min. A cerca superior fica em Q3 + 1,5 × IQR = 20 + 10,5 = 30,5 min. Qualquer atendimento acima disso é marcado como atípico no boxplot."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "O relatório de um SAC diz apenas que o tempo médio de atendimento é de 18 minutos. Explique por que esse número sozinho pode esconder problemas e o que uma tabela por classes e um boxplot revelariam."
  rubrica:
    - "Explica que a média resume tudo em um número e não mostra como os tempos se distribuem: dois SACs com a mesma média podem ter distribuições muito diferentes."
    - "Diz que a tabela por classes, ou o histograma, mostra onde a maioria dos atendimentos se concentra e se há faixas vazias ou uma cauda longa de tempos altos."
    - "Diz que o boxplot mostra a mediana, a faixa dos 50% centrais e os valores atípicos, que são justamente os casos que merecem investigação."
  modelo: "A média de 18 minutos pode vir de atendimentos quase todos entre 15 e 20 minutos, ou de muitos atendimentos rápidos misturados com alguns que levam mais de uma hora. As duas situações têm a mesma média e pedem ações diferentes. Uma tabela por classes, ou o histograma, mostraria onde a maioria dos tempos se concentra e se há uma cauda de atendimentos longos, com faixas vazias no meio. O boxplot resumiria isso na mediana, na caixa com os 50% centrais e nos pontos atípicos. Esses pontos são os chamados que fogem do padrão, e são eles que a coordenação deveria investigar primeiro."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Como se distribuem os atendimentos do SAC"
  descricao: "Um SAC registrou 60 chamados com canal, nota e tempo de atendimento. Você vai montar tabelas de frequência absoluta, relativa e acumulada, agrupar os tempos em classes pela regra de Sturges e calcular o resumo de cinco números e os limites do boxplot para encontrar os atendimentos atípicos."
  pasta: "desafios/estatistica/tabelas_frequencia"
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
      descricao: "Abra desafios/estatistica/tabelas_frequencia/README.md. Os dados estão em data/atendimentos.csv: uma linha por chamado, com o número, o canal, a nota de 1 a 5 e o tempo de atendimento em minutos."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "Cada função tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def tabela_frequencia(serie):"
        - "def numero_de_classes(n):"
        - "def tabela_por_classes(valores, k):"
        - "def cinco_numeros(valores):"
        - "def limites_boxplot(valores):"
        - "def resumo_atendimentos(caminho_csv):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/estatistica/tabelas_frequencia"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/tabelas_frequencia"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de tabelas de frequência"'
        - "git push -u origin desafio/tabelas_frequencia"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Frequência absoluta", en: "frequency, count" }
  - { pt: "Frequência relativa", en: "relative frequency" }
  - { pt: "Frequência acumulada", en: "cumulative frequency" }
  - { pt: "Classe (intervalo)", en: "bin, class interval" }
  - { pt: "Largura da classe", en: "bin width" }
  - { pt: "Regra de Sturges", en: "Sturges' rule" }
  - { pt: "Histograma", en: "histogram" }
  - { pt: "Resumo de cinco números", en: "five-number summary" }
  - { pt: "Diagrama de caixa", en: "box plot, box-and-whisker plot" }
  - { pt: "Bigode", en: "whisker" }
  - { pt: "Cerca", en: "fence" }
---

## Frequência absoluta, relativa e acumulada

Uma **tabela de frequência** conta quantas vezes cada valor aparece. É o primeiro passo para enxergar uma distribuição, ou seja, como os dados se espalham entre os valores possíveis. Estas são as notas de 1 a 5 que 60 clientes deram a um SAC:

| Nota | Frequência | Relativa | Acumulada | Relativa acumulada |
| ---- | ---------- | -------- | --------- | ------------------ |
| 1    | 4          | 6,7%     | 4         | 6,7%               |
| 2    | 6          | 10,0%    | 10        | 16,7%              |
| 3    | 10         | 16,7%    | 20        | 33,3%              |
| 4    | 22         | 36,7%    | 42        | 70,0%              |
| 5    | 18         | 30,0%    | 60        | 100,0%             |

- A **frequência absoluta** é a contagem: 22 clientes deram nota 4.
- A **frequência relativa** é a contagem dividida pelo total: 22 ÷ 60 = 36,7%. Ela permite comparar grupos de tamanhos diferentes.
- A **frequência acumulada** soma as contagens até aquele valor: 20 clientes deram nota 3 ou menos.
- A **relativa acumulada** é a acumulada em porcentagem: 33,3% deram nota 3 ou menos.

A acumulada só faz sentido quando os valores têm ordem, como notas, idades ou faixas de preço. Para uma variável nominal, como o canal de atendimento, "chat ou menos" não significa nada.

A acumulada também mostra a mediana: é o primeiro valor em que a relativa acumulada passa de 50%. Aqui, a nota 4.

No pandas:

```python
import pandas as pd

atendimentos = pd.read_csv("data/atendimentos.csv")
notas = atendimentos["nota"]

# sem o sort_index, as linhas vêm ordenadas pela contagem
frequencia = notas.value_counts().sort_index()
relativa = frequencia / frequencia.sum() * 100
acumulada = frequencia.cumsum()
relativa_acumulada = acumulada / frequencia.sum() * 100
```

Calcule a relativa acumulada a partir da acumulada, como acima, e não somando as relativas já arredondadas. Somando valores arredondados, o erro de arredondamento se acumula, e a última linha pode dar 100,1%.

## Dados contínuos: classes e histograma

Com uma variável contínua, como o tempo de atendimento, quase nenhum valor se repete, e uma tabela com cada valor teria uma linha por atendimento. A solução é agrupar os valores em **classes**, faixas de mesma largura:

1. Calcule a amplitude: maior valor − menor valor. Com tempos de 4 a 74 minutos, dá 70.
2. Escolha o número de classes. A **regra de Sturges** sugere 1 + log₂(n), arredondado para cima. Com 60 valores, dá 7 classes.
3. Divida a amplitude pelo número de classes: 70 ÷ 7 = 10 minutos de largura.
4. Conte quantos valores caem em cada faixa. A convenção mais comum é incluir o início e excluir o fim, com a notação [4, 14), e a última classe inclui também o fim, para o maior valor não ficar de fora.

| Tempo (min) | Frequência | Relativa |
| ----------- | ---------- | -------- |
| [4, 14)     | 21         | 35,0%    |
| [14, 24)    | 32         | 53,3%    |
| [24, 34)    | 4          | 6,7%     |
| [34, 44)    | 1          | 1,7%     |
| [44, 54)    | 0          | 0,0%     |
| [54, 64)    | 0          | 0,0%     |
| [64, 74]    | 2          | 3,3%     |

O **histograma** é o desenho dessa tabela: uma barra por classe, com altura igual à frequência. As barras ficam encostadas, porque as classes cobrem uma faixa contínua. Nesse histograma, 88% dos atendimentos levam menos de 24 minutos, a distribuição é assimétrica à direita, e duas classes vazias separam dois atendimentos muito longos do resto.

O número de classes muda o que se vê. Com poucas classes, detalhes somem. Com muitas, o desenho fica serrilhado e cheio de barras vazias. A regra de Sturges é um ponto de partida: teste alguns valores próximos.

No pandas, `pd.cut` monta as classes:

```python
tempos = atendimentos["tempo_min"]
pd.cut(tempos, bins=7, right=False).value_counts(sort=False)
```

Com `bins=7`, o pandas estica um pouco a última borda para incluir o maior valor. Se você passar as bordas explicitamente, como `bins=[4, 14, ..., 74]`, com `right=False`, o 74 fica de fora sem nenhum aviso. Depois de montar classes, confira sempre se a soma das frequências dá o total de linhas.

## Resumo de cinco números e diagrama de caixa

O **resumo de cinco números** descreve uma distribuição com o mínimo, o primeiro quartil (Q1), a mediana, o terceiro quartil (Q3) e o máximo. Para os 60 tempos de atendimento: 4, 13, 16, 20 e 74 minutos.

O **diagrama de caixa** (boxplot) desenha esse resumo:

- A **caixa** vai de Q1 a Q3 e contém os 50% centrais dos dados. A linha dentro dela é a mediana.
- As **cercas** ficam a 1,5 intervalo interquartil de cada lado da caixa: Q1 − 1,5 × IQR e Q3 + 1,5 × IQR. Elas não são desenhadas, só servem de limite.
- Os **bigodes** vão da caixa até o dado mais extremo que ainda está dentro das cercas.
- Os valores fora das cercas aparecem como pontos isolados: são os **valores atípicos**.

Nos tempos de atendimento, IQR = 20 − 13 = 7, e as cercas ficam em 13 − 10,5 = 2,5 e 20 + 10,5 = 30,5 minutos. O bigode inferior termina no 4, o menor tempo, e o superior no 30, o maior tempo abaixo de 30,5. Os atendimentos de 37, 68 e 74 minutos são atípicos.

Como ler um boxplot:

- **Mediana perto de um lado da caixa**, ou um bigode bem mais longo que o outro: distribuição assimétrica.
- **Caixa estreita:** os valores centrais são parecidos entre si.
- **Muitos pontos atípicos de um lado:** cauda longa, que merece investigação.

| Gráfico     | Mostra bem                                         | Esconde                                        |
| ----------- | -------------------------------------------------- | ---------------------------------------------- |
| Histograma  | A forma: picos, assimetria, lacunas                | Pouco, mas ocupa espaço e depende do número de classes |
| Boxplot     | Mediana, dispersão e atípicos, em pouco espaço     | Picos: uma distribuição com dois picos pode ter o mesmo boxplot de uma com um só |

O boxplot brilha na comparação de grupos, com uma caixa ao lado da outra:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
atendimentos.boxplot(column="tempo_min", by="canal", ax=ax)
ax.set_ylabel("Tempo de atendimento (min)")
```

O matplotlib e o pandas calculam os quartis por interpolação, um método um pouco diferente do método das metades. Em conjuntos pequenos, os limites da caixa podem sair um pouco diferentes dos calculados à mão. A ideia é a mesma, e a diferença some conforme os dados crescem.

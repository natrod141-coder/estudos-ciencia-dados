---
titulo: "Storytelling com dados"
modulo: visualizacao
ordem: 5
horas: 3
estado: publicado
resumo: "Transformar uma análise em uma mensagem clara para quem decide."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Exploratório e explicativo"
    tipo: leitura
    minutos: 6
  - id: a2
    titulo: "Antes do gráfico: público, decisão e ideia central"
    tipo: leitura
    minutos: 8
  - id: a3
    titulo: "Menos é mais: tirando a desordem"
    tipo: leitura
    minutos: 8
  - id: a4
    titulo: "Foco: cor, tamanho e posição"
    tipo: leitura
    minutos: 8
  - id: a5
    titulo: "A estrutura da história e o resumo executivo"
    tipo: leitura
    minutos: 10
  - id: a6
    titulo: "Vídeo de apoio: storytelling com dados na prática"
    tipo: video
    minutos: 15
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Qual é a diferença entre um gráfico exploratório e um gráfico explicativo?"
    opcoes: ["O exploratório usa mais cores", "O exploratório serve para você descobrir o que os dados dizem; o explicativo serve para comunicar uma conclusão específica a outra pessoa", "O explicativo é sempre interativo", "Não há diferença, só o momento em que são feitos"]
    correta: 1
    explicacao: "Na exploração, você faz dezenas de gráficos rápidos para achar o que é interessante. Para apresentar, escolhe uma mensagem e constrói o gráfico em torno dela. O erro mais comum é mostrar à diretoria o gráfico exploratório e esperar que ela encontre a conclusão sozinha."
  - pergunta: "Qual título comunica melhor, num slide para a diretoria?"
    opcoes: ["Faturamento por canal, 2025", "Gráfico 3", "O app cresceu 280% em 2025 e virou o maior canal de vendas", "Evolução mensal do faturamento dos canais de venda da empresa"]
    correta: 2
    explicacao: "Um título que afirma a conclusão diz ao leitor o que olhar, e o gráfico serve de prova. Títulos descritivos, como 'Faturamento por canal', deixam a interpretação para o leitor, que pode não chegar à mesma conclusão ou não ter tempo de procurá-la."
  - pergunta: "Num gráfico de linhas com cinco séries, qual é a melhor forma de destacar a série que importa para a mensagem?"
    opcoes: ["Pintar a série principal com uma cor forte e as outras de cinza", "Usar cinco cores vibrantes, uma para cada série", "Aumentar a fonte da legenda", "Colocar a série principal em 3D"]
    correta: 0
    explicacao: "A cor é percebida antes de qualquer leitura consciente. Com uma cor só de destaque e o resto em cinza, o olho vai direto para a série principal, e as outras continuam lá como contexto. Com cinco cores fortes, nada se destaca."
  - pergunta: "Por que trocar a legenda por rótulos escritos ao lado do fim de cada linha?"
    opcoes: ["Porque o matplotlib não faz legendas", "Porque a legenda ocupa espaço demais em qualquer gráfico", "Porque legendas são proibidas em apresentações", "Porque o leitor não precisa ir e voltar entre a legenda e as linhas para saber quem é quem"]
    correta: 3
    explicacao: "Com a legenda, o leitor precisa associar cores a nomes, ir até a legenda e voltar para a linha. Com o rótulo direto, o nome está onde o olho já está. É um pequeno esforço a menos, e em apresentações cada esforço a menos conta."
  - pergunta: "Antes de montar um gráfico para uma apresentação, o que é preciso definir primeiro?"
    opcoes: ["A paleta de cores e a fonte", "Quem é o público, que decisão ele precisa tomar e qual é a mensagem, numa frase", "Quantos gráficos cabem no slide", "O software que será usado"]
    correta: 1
    explicacao: "Sem saber para quem é e para quê, não há como escolher o que mostrar. A mensagem numa frase, que Cole Nussbaumer Knaflic chama de ideia central, orienta todas as escolhas seguintes: qual gráfico, o que destacar, o que deixar de fora."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Você analisou as vendas por canal e descobriu que o app cresceu 280% no ano, enquanto a loja física ficou estável. Descreva como apresentaria isso num slide para a diretoria: o título, o gráfico e o que você falaria, em três frases."
  rubrica:
    - "Propõe um título que afirma a conclusão, com o número, em vez de um título descritivo."
    - "Descreve um gráfico explicativo: o app destacado em cor e os outros canais em cinza, rótulos diretos em vez de legenda e sem elementos desnecessários."
    - "Organiza a fala em contexto, achado e recomendação, terminando com o que a diretoria deve decidir ou fazer."
  modelo: "O título seria a própria conclusão: 'O app cresceu 280% em 2025 e virou o maior canal de vendas'. O gráfico seria de linhas, com o faturamento mensal dos três canais, a linha do app grossa e na cor de destaque, e a loja física e o site em cinza, como contexto. Cada linha teria o nome e o valor de dezembro escritos no fim, sem legenda, e o gráfico não teria grade pesada nem bordas. Na fala: 'Em 2025, vendemos R$ 3,6 milhões nos três canais. O app, que em janeiro era o menor, cresceu 280%, passou a loja física em outubro e fechou dezembro com 38% das vendas. Proponho aumentar o investimento no app no orçamento de 2026 e entender por que a loja física ficou parada, para decidirmos até março o plano de cada canal.'"

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Do gráfico exploratório ao explicativo"
  descricao: "A diretoria pediu um slide sobre as vendas de 2025 por canal. Você vai calcular a mensagem principal a partir dos dados, escrever um título que afirma a conclusão, construir um gráfico explicativo com cor de destaque, cinza de contexto e rótulos diretos, e redigir o resumo executivo em contexto, achado e recomendação."
  pasta: "desafios/visualizacao/storytelling"
  testes: 7
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
      descricao: "Abra desafios/visualizacao/storytelling/README.md. Os dados estão em data/vendas_por_canal.csv: o faturamento de cada mês de 2025 em cada canal."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "A mensagem vem dos dados: calcule os números, não os escreva à mão. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def tabela_por_canal(vendas):"
        - "def mensagem_principal(vendas):"
        - "def titulo(mensagem):"
        - "def grafico_explicativo(vendas):"
        - "def resumo_executivo(vendas):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/visualizacao/storytelling"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/storytelling"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de storytelling com dados"'
        - "git push -u origin desafio/storytelling"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Storytelling com dados", en: "data storytelling" }
  - { pt: "Gráfico exploratório", en: "exploratory chart" }
  - { pt: "Gráfico explicativo", en: "explanatory chart" }
  - { pt: "Ideia central", en: "big idea" }
  - { pt: "Público", en: "audience" }
  - { pt: "Desordem visual", en: "clutter" }
  - { pt: "Atributos pré-atentivos", en: "preattentive attributes" }
  - { pt: "Rótulo direto", en: "direct label" }
  - { pt: "Chamada para ação", en: "call to action" }
  - { pt: "Resumo executivo", en: "executive summary" }
---

## Exploratório e explicativo

Uma análise tem duas fases, e cada uma pede um tipo de gráfico.

Na **exploração**, você está descobrindo o que os dados dizem. Faz dezenas de gráficos rápidos, com cores automáticas e legendas, olha, descarta, cruza de outro jeito. Esses gráficos servem para você.

Na **explicação**, você já sabe o que os dados dizem e precisa que outra pessoa entenda. Aqui, vale o contrário: poucos gráficos, cada um construído para uma mensagem só. Esses gráficos servem para o outro.

O erro mais comum em apresentações é levar para a reunião os gráficos da fase de exploração e esperar que a diretoria encontre sozinha a conclusão que você levou dias para achar. Ela não vai ter tempo, e pode chegar a outra conclusão.

Este tópico é sobre a segunda fase. Boa parte das técnicas vem do livro *Storytelling com Dados*, de Cole Nussbaumer Knaflic, que vale a leitura completa.

## Antes do gráfico: público, decisão e ideia central

Antes de abrir qualquer ferramenta, responda três perguntas:

1. **Quem é o público?** A diretoria, o time de marketing, um cliente? O que ele já sabe, e que termos entende?
2. **O que ele precisa decidir ou fazer?** Aprovar um orçamento, mudar uma prioridade, investigar um problema. Se a apresentação não ajuda a decidir nada, talvez ela não precise existir.
3. **Qual é a mensagem, numa frase?** É a **ideia central**: uma frase completa, com um ponto de vista e o que está em jogo. "O app cresceu 280% e virou o maior canal: precisa de prioridade no orçamento de 2026" é uma ideia central. "Vendas por canal" é só um assunto.

Um bom teste é a **história de três minutos**: se você tivesse três minutos, sem slides, para explicar a conclusão a alguém da diretoria no elevador, o que diria? Se você não consegue, ainda não está pronto para montar os gráficos.

## Menos é mais: tirando a desordem

Todo elemento num gráfico custa um pouco da atenção de quem lê. Elementos que não ajudam a entender a mensagem são **desordem**, e devem sair:

| Elemento                               | O que fazer                                               |
| -------------------------------------- | --------------------------------------------------------- |
| Bordas do gráfico                      | Tire as de cima e da direita; muitas vezes, todas         |
| Linhas de grade                        | Tire, ou deixe bem claras                                 |
| Legenda                                | Troque por rótulos diretos, ao lado das linhas ou barras  |
| Marcadores em cada ponto               | Tire, a não ser que os pontos importem                    |
| Rótulos de dados em todas as barras    | Deixe só os que sustentam a mensagem                      |
| Cores diferentes sem motivo            | Use cinza para tudo que não é o foco                      |
| Efeitos 3D, sombras, fundos            | Tire sempre                                               |

Os **rótulos diretos** merecem destaque. Com a legenda, o leitor olha a linha, vai até a legenda, descobre a cor e volta. Com o nome escrito ao lado do fim de cada linha, a informação está onde o olho já está.

Depois de limpar, olhe o gráfico e pergunte de cada elemento que sobrou: se eu tirar isto, alguém sentiria falta?

## Foco: cor, tamanho e posição

Alguns atributos visuais são percebidos antes de qualquer leitura consciente, em uma fração de segundo. São os **atributos pré-atentivos**: cor, tamanho, espessura, posição, intensidade. Eles dizem ao leitor onde olhar primeiro.

O uso mais eficaz é o **cinza com uma cor de destaque**: tudo em cinza, e só a série da mensagem numa cor forte. O cinza mantém o contexto visível, sem competir. Se tudo tem cor, nada se destaca.

```python
for canal in tabela.columns:
    destaque = canal == "app"
    ax.plot(tabela.index, tabela[canal],
            color="#0f4c4a" if destaque else "#b0b0b0",
            linewidth=3 if destaque else 1.5)
    ax.text(len(tabela) - 0.8, tabela[canal].iloc[-1], canal,
            color="#0f4c4a" if destaque else "#b0b0b0", va="center")

ax.set_title("O app cresceu 280% em 2025 e virou o maior canal de vendas", loc="left")
ax.spines[["top", "right"]].set_visible(False)
```

Outros cuidados com o foco:

- **Espessura e tamanho** reforçam a cor: a linha principal mais grossa, o número principal maior.
- **Posição:** o leitor começa pelo canto superior esquerdo. É onde vão o título e o número mais importante.
- **Cor com significado:** vermelho para problema e verde para bom resultado só funcionam se forem usados assim no relatório inteiro. Cerca de 1 em cada 12 homens tem alguma dificuldade para distinguir cores, principalmente vermelho e verde. Por isso, não dependa só da cor: use também posição, rótulos e espessura.

## A estrutura da história e o resumo executivo

**O título é a mensagem.** Em vez de "Faturamento por canal, 2025", escreva a conclusão: "O app cresceu 280% em 2025 e virou o maior canal de vendas". O leitor sabe o que procurar, e o gráfico vira a prova. Um teste simples: se alguém ler só os títulos dos slides, em sequência, deve entender a história toda.

**Uma mensagem por slide.** Se um slide tem duas conclusões, vira dois slides.

**Começo, meio e fim.** Uma apresentação de dados funciona como uma história:

1. **Contexto:** a situação que todos conhecem, e por que o assunto importa agora.
2. **Achado:** o que os dados mostram, com os números que sustentam a conclusão.
3. **Recomendação:** o que fazer, e o que você precisa de quem está ouvindo. É a **chamada para ação**, e é a parte mais esquecida.

O mesmo formato serve para o **resumo executivo**, o parágrafo que abre um relatório ou um e-mail para a diretoria:

> Em 2025, as vendas somaram R$ 3,6 milhões nos três canais. O app cresceu 280% no ano e terminou 2025 como o maior canal de vendas, com 38% do faturamento de dezembro. Recomendo priorizar o app no orçamento de 2026 e investigar por que a loja física ficou estável.

Três frases, e quem lê já sabe a situação, a conclusão e o que se espera dele. Os gráficos e as tabelas vêm depois, para quem quiser conferir.

Por fim, uma questão de honestidade: destacar não é distorcer. O cinza deixa o contexto à vista, e o eixo das barras continua começando no zero. Se a mensagem só se sustenta escondendo parte dos dados, o problema está na mensagem.

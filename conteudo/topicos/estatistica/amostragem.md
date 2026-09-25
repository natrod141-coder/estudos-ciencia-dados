---
titulo: "Amostragem"
modulo: estatistica
ordem: 3
horas: 4
estado: publicado
resumo: "Como escolher uma parte dos dados que represente o todo."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "População, amostra e por que amostrar"
    tipo: leitura
    minutos: 8
  - id: a2
    titulo: "Tipos de amostragem"
    tipo: leitura
    minutos: 15
  - id: a3
    titulo: "Viés: quando a amostra não representa a população"
    tipo: leitura
    minutos: 10
  - id: a4
    titulo: "Margem de erro e tamanho da amostra"
    tipo: leitura
    minutos: 12
  - id: a5
    titulo: "Vídeo de apoio sobre amostragem"
    tipo: video
    minutos: 15
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Uma pesquisa com 1.000 eleitores sorteados encontrou 42% de intenção de voto em um candidato. Esse 42% é:"
    opcoes: ["Um parâmetro, porque descreve a população de eleitores", "A margem de erro da pesquisa", "Uma estatística, porque foi calculada a partir da amostra", "O resultado exato da eleição"]
    correta: 2
    explicacao: "Parâmetro é o valor verdadeiro na população, quase sempre desconhecido. Estatística é o valor calculado na amostra e usado para estimar o parâmetro. O 42% vem de 1.000 eleitores, então é uma estatística."
  - pergunta: "Uma empresa tem 70% de clientes no plano básico e 30% no premium. Ela quer uma amostra de 200 clientes com essa mesma proporção garantida. Qual técnica é a mais indicada?"
    opcoes: ["Amostragem estratificada proporcional", "Amostragem por conveniência", "Amostragem por conglomerados", "Amostragem aleatória simples"]
    correta: 0
    explicacao: "Na amostragem estratificada, a população é dividida em grupos (os estratos, aqui os planos) e cada grupo é sorteado separadamente. Com a alocação proporcional, a amostra terá exatamente 140 clientes do básico e 60 do premium. A aleatória simples acerta essa proporção só em média, e não garante."
  - pergunta: "Um app pergunta a satisfação dos usuários por notificação, e só 8% respondem. Qual é o principal risco dessa pesquisa?"
    opcoes: ["A amostra ser pequena demais para qualquer conclusão", "Erro no cálculo da média das notas", "Nenhum, porque a notificação foi enviada para todos os usuários", "Viés de não resposta: quem responde pode ser diferente de quem não responde"]
    correta: 3
    explicacao: "Enviar para todos não garante uma amostra representativa. Quem responde costuma ser quem está muito satisfeito ou muito insatisfeito, e os 92% em silêncio podem pensar diferente. Esse é o viés de não resposta, e ele não diminui com mais respostas."
  - pergunta: "Para reduzir pela metade a margem de erro de uma pesquisa, mantendo o nível de confiança, o que é preciso fazer com o tamanho da amostra?"
    opcoes: ["Dobrar", "Multiplicar por 4", "Multiplicar por 1,5", "Reduzir pela metade"]
    correta: 1
    explicacao: "A margem de erro é proporcional a 1 ÷ √n. Para ela cair pela metade, √n precisa dobrar, e isso exige multiplicar n por 4. É por isso que ganhar precisão fica cada vez mais caro."
  - pergunta: "Uma pesquisa com 1.000 pessoas sorteadas tem margem de erro de cerca de 3 pontos percentuais. Se a população fosse o Brasil inteiro, e não uma cidade de 100 mil habitantes, o que aconteceria com a margem de erro?"
    opcoes: ["Ficaria muito maior, porque a população é maior", "Ficaria menor, porque o país é mais diverso", "Praticamente não mudaria, porque ela depende do tamanho da amostra, e não do tamanho da população", "Não seria possível calcular"]
    correta: 2
    explicacao: "Quando a amostra é uma parte pequena da população, a margem de erro depende quase só do tamanho da amostra. Mil pessoas bem sorteadas dão cerca de 3 pontos de margem, seja numa cidade de 100 mil habitantes, seja num país de 200 milhões."
  - pergunta: "Para estimar o movimento de uma loja, um analista sorteia um dia inicial e depois pega um dia a cada 7. Qual é o problema dessa amostra?"
    opcoes: ["Nenhum, a amostragem sistemática é sempre equivalente ao sorteio", "Todos os dias da amostra caem no mesmo dia da semana, e o movimento varia com o dia da semana", "A amostra fica grande demais", "A amostragem sistemática não pode ser usada com datas"]
    correta: 1
    explicacao: "Com intervalo de 7 dias, todos os dias sorteados caem no mesmo dia da semana. Se o início for um sábado, a amostra só tem sábados e superestima o movimento. A amostragem sistemática falha quando os dados têm um padrão que se repete no mesmo intervalo do salto."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Uma marca publicou uma enquete no Instagram e recebeu 5.000 respostas, com 92% dos clientes satisfeitos. Explique por que esse número pode não representar a satisfação dos clientes e como você montaria uma amostra melhor."
  rubrica:
    - "Identifica que é uma amostra por conveniência, com autosseleção: responde quem segue a marca e decide responder."
    - "Explica que esses respondentes tendem a ser diferentes do cliente comum, por exemplo mais engajados e mais satisfeitos, e que esse viés não diminui com mais respostas."
    - "Propõe sortear clientes a partir da base completa, por amostragem aleatória simples ou estratificada, e contatar os sorteados, cuidando para que a taxa de resposta não crie um novo viés."
  modelo: "As 5.000 respostas vêm de quem segue a marca no Instagram e decidiu responder. É uma amostra por conveniência, com autosseleção. Quem segue a marca e para para responder tende a gostar mais dela do que o cliente comum, e os insatisfeitos provavelmente nem estão ali. Esse viés não diminui com mais respostas: 50 mil respostas do mesmo tipo continuariam enviesadas. Para uma amostra melhor, eu partiria da base completa de clientes e sortearia algumas centenas, de forma aleatória ou estratificada por perfil (região ou plano, por exemplo). Depois entraria em contato com os sorteados e acompanharia quem não respondeu, para que a não resposta não criasse um novo viés."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Uma amostra que represente a base de clientes"
  descricao: "Uma empresa quer entrevistar 100 de seus 1.000 clientes, e a base veio ordenada por região. Você vai montar amostras aleatória simples, sistemática e estratificada, medir o quanto cada uma se afasta da composição real da base e calcular margem de erro e tamanho de amostra."
  pasta: "desafios/estatistica/amostragem"
  testes: 10
  tempo: "2 h"
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
      descricao: "Abra desafios/estatistica/amostragem/README.md. Os dados estão em data/clientes.csv: uma linha por cliente, com o id, a região, o plano (básico ou premium) e o gasto mensal em reais."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "Cada função tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def amostra_aleatoria_simples(populacao, n, semente):"
        - "def amostra_sistematica(populacao, n, inicio=0):"
        - "def tamanhos_por_estrato(populacao, coluna, n):"
        - "def amostra_estratificada(populacao, coluna, n, semente):"
        - "def erro_de_composicao(populacao, amostra, coluna):"
        - "def margem_de_erro(p, n, z=1.96):"
        - "def tamanho_amostra(margem, p=0.5, z=1.96):"
        - "def avaliar_amostras(caminho_csv, n=100, semente=42):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/estatistica/amostragem"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/amostragem"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de amostragem"'
        - "git push -u origin desafio/amostragem"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "População", en: "population" }
  - { pt: "Amostra", en: "sample" }
  - { pt: "Parâmetro", en: "parameter" }
  - { pt: "Estatística (da amostra)", en: "statistic" }
  - { pt: "Amostragem aleatória simples", en: "simple random sampling" }
  - { pt: "Amostragem sistemática", en: "systematic sampling" }
  - { pt: "Amostragem estratificada", en: "stratified sampling" }
  - { pt: "Amostragem por conglomerados", en: "cluster sampling" }
  - { pt: "Amostra por conveniência", en: "convenience sample" }
  - { pt: "Viés de seleção", en: "selection bias" }
  - { pt: "Viés de não resposta", en: "non-response bias" }
  - { pt: "Viés de sobrevivência", en: "survivorship bias" }
  - { pt: "Margem de erro", en: "margin of error" }
  - { pt: "Semente aleatória", en: "random seed" }
---

## População, amostra e por que amostrar

A **população** é o conjunto inteiro sobre o qual você quer tirar conclusões: todos os clientes da empresa, todos os eleitores do país, todas as peças que saem de uma fábrica. A **amostra** é a parte da população que você de fato observa.

Um número que descreve a população, como a porcentagem real de clientes satisfeitos, é um **parâmetro**. Quase sempre ele é desconhecido. O mesmo número calculado na amostra é uma **estatística**, e serve para estimar o parâmetro. Toda a amostragem gira em torno de uma pergunta: quanto dá para confiar que a estatística está perto do parâmetro?

Há bons motivos para trabalhar com amostras:

- **Custo e tempo.** Entrevistar 400 clientes é viável. Entrevistar 200 mil, não.
- **Testes destrutivos.** Para testar a resistência de uma lâmpada, é preciso quebrá-la. Não dá para testar o lote inteiro.
- **Velocidade de análise.** Mesmo com os dados completos no banco, explorar uma amostra de 1% é muito mais rápido, e o resultado costuma ser praticamente o mesmo.

Mesmo quando você acha que tem "todos os dados", muitas vezes tem uma amostra de outra coisa. Os usuários do seu app são uma amostra dos clientes potenciais, e não uma amostra qualquer: são os que já escolheram o seu produto.

## Tipos de amostragem

Nas **amostragens probabilísticas**, cada elemento da população tem uma chance conhecida de ser escolhido. Só elas permitem calcular margem de erro. Para usá-las, é preciso ter a lista da população, chamada de cadastro ou moldura amostral.

**Aleatória simples.** Todos têm a mesma chance, como num sorteio. É a referência: as outras técnicas são variações dela.

**Sistemática.** Escolhe-se um elemento a cada k, a partir de um ponto de partida sorteado. Com 1.000 clientes e uma amostra de 100, k = 10: se o sorteio der 3, entram os clientes nas posições 3, 13, 23 e assim por diante. É prática, mas falha quando a lista tem um padrão que se repete a cada k posições. Um exemplo: pegar um dia a cada 7 produz uma amostra só de segundas-feiras, ou só de sábados.

**Estratificada.** A população é dividida em grupos homogêneos, os **estratos** (região, plano, faixa etária), e sorteia-se dentro de cada um. Na alocação proporcional, cada estrato entra na amostra com o mesmo peso que tem na população. Ela garante que grupos pequenos apareçam e costuma dar estimativas mais precisas que a aleatória simples quando os estratos são diferentes entre si.

**Por conglomerados.** Sorteiam-se grupos inteiros, como escolas, bairros ou lojas, e observam-se todos os elementos dos grupos sorteados. Sai mais barata quando a população está espalhada, mas é menos precisa, porque elementos do mesmo grupo costumam ser parecidos.

Nas **amostragens não probabilísticas**, a escolha não é por sorteio. A mais comum é a **por conveniência**: entra quem é mais fácil de alcançar. Serve para explorar ideias e testar um questionário, mas não para generalizar para a população.

| Técnica            | Como funciona                        | Quando usar                                   |
| ------------------ | ------------------------------------ | --------------------------------------------- |
| Aleatória simples  | Sorteio entre todos                  | Há uma lista completa e a população é homogênea |
| Sistemática        | Um a cada k, com início sorteado     | Lista longa, sem padrão periódico             |
| Estratificada      | Sorteio dentro de cada grupo         | Há grupos diferentes entre si, ou grupos pequenos importantes |
| Por conglomerados  | Sorteio de grupos inteiros           | População espalhada e visitar cada elemento custa caro |
| Por conveniência   | Quem estiver disponível              | Exploração inicial, nunca para generalizar    |

No pandas, as três primeiras são uma linha cada:

```python
import pandas as pd

clientes = pd.read_csv("data/clientes.csv")

# aleatória simples, reproduzível graças ao random_state
aleatoria = clientes.sample(n=100, random_state=42)

# sistemática: uma linha a cada 10, começando na posição 3
sistematica = clientes.iloc[3::10]

# estratificada proporcional: 10% de cada região
por_regiao = clientes.groupby("regiao")
estratificada = por_regiao.sample(frac=0.10, random_state=42)
```

Use sempre uma semente (`random_state`). Sem ela, cada execução sorteia uma amostra diferente, e ninguém consegue reproduzir a sua análise, nem você mesmo.

## Viés: quando a amostra não representa a população

Uma amostra pode errar de dois jeitos.

O **erro amostral** é a diferença que aparece por acaso, porque você observou só uma parte. Ele diminui quando a amostra cresce e pode ser medido pela margem de erro.

O **viés** é um erro sistemático: a forma de escolher a amostra favorece um tipo de elemento. Ele **não diminui** com uma amostra maior. O caso clássico é a revista americana Literary Digest, que em 1936 recebeu cerca de 2,4 milhões de respostas e previu a derrota de Franklin Roosevelt. A lista de envio vinha de assinantes de revista, donos de telefone e de carro, um público mais rico que a média. Roosevelt venceu com folga, e o instituto de George Gallup acertou com uma amostra muito menor e bem escolhida.

Os vieses mais comuns em dados de empresas:

- **Viés de seleção:** a forma de coletar exclui parte da população. Uma pesquisa feita só no site deixa de fora quem compra na loja física.
- **Autosseleção:** as pessoas escolhem participar. Enquetes e avaliações de produtos atraem quem tem opinião forte.
- **Não resposta:** quem não responde é diferente de quem responde. Com 8% de taxa de resposta, os outros 92% podem pensar diferente.
- **Viés de sobrevivência:** só se observa quem "sobreviveu" a um filtro. Estudar apenas os clientes ativos para entender o cancelamento ignora justamente quem cancelou.

A pergunta que evita a maioria desses erros é: **quem ficou de fora da minha amostra, e ele seria diferente de quem entrou?**

## Margem de erro e tamanho da amostra

Numa amostra aleatória, a **margem de erro** de uma proporção, com 95% de confiança, é:

margem = 1,96 × √(p × (1 − p) ÷ n)

Aqui, p é a proporção observada e n é o tamanho da amostra. O 1,96 vem da distribuição normal e corresponde a 95% de confiança. Para 99%, use 2,576.

Exemplo: numa amostra de 1.000 clientes, 50% dizem estar satisfeitos. A margem é 1,96 × √(0,5 × 0,5 ÷ 1.000) ≈ 0,031, ou seja, 3,1 pontos percentuais. A leitura correta é: a satisfação real deve estar entre 46,9% e 53,1%, e esse método de cálculo acerta a faixa em 95% das vezes em que é aplicado.

Invertendo a fórmula, dá para calcular o tamanho de amostra necessário para uma margem desejada:

n = 1,96² × p × (1 − p) ÷ margem²

Sem nenhuma ideia do valor de p, use 0,5: é o caso que exige a maior amostra. Com 95% de confiança, dá 385 para uma margem de 5 pontos e 1.068 para uma margem de 3 pontos.

Três consequências importantes:

1. **A margem cai com a raiz de n.** Para cortar a margem pela metade, é preciso quatro vezes mais amostra.
2. **O tamanho da população quase não importa.** Enquanto a amostra for uma parte pequena da população (menos de uns 5%), 1.000 entrevistas dão cerca de 3 pontos de margem numa cidade ou num país inteiro.
3. **A margem de erro só mede o erro amostral.** Ela não diz nada sobre viés. Uma pesquisa enviesada com margem de 1 ponto continua errada.

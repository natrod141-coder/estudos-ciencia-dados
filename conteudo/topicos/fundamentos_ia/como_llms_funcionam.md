---
titulo: "Como um LLM funciona"
modulo: fundamentos_ia
ordem: 1
horas: 4
estado: publicado
resumo: "Tokens, janela de contexto, previsão do próximo token e temperatura, sem matemática pesada."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "O que um LLM faz: prever o próximo token"
    tipo: leitura
    minutos: 10
  - id: a2
    titulo: "Tokens: as peças que o modelo enxerga"
    tipo: leitura
    minutos: 12
  - id: a3
    titulo: "Janela de contexto e conversas sem memória"
    tipo: leitura
    minutos: 12
  - id: a4
    titulo: "Amostragem: temperatura e por que a resposta varia"
    tipo: leitura
    minutos: 10
  - id: a5
    titulo: "Custo, limites e escolha de modelo"
    tipo: leitura
    minutos: 12
  - id: a6
    titulo: "Vídeo de apoio: como funcionam os modelos de linguagem"
    tipo: video
    minutos: 20
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "O que um LLM faz, no fundo, para gerar uma resposta?"
    opcoes: ["Procura a resposta pronta num banco de dados de textos", "Prevê o próximo token muitas vezes seguidas, a partir de tudo o que veio antes", "Executa um programa escrito especialmente para cada pergunta", "Busca a resposta na internet a cada pergunta"]
    correta: 1
    explicacao: "O modelo calcula a probabilidade de cada próximo token possível, escolhe um, acrescenta ao texto e repete. A resposta inteira sai desse ciclo. Ele não consulta um banco de respostas prontas, e só acessa a internet se tiver uma ferramenta de busca disponível."
  - pergunta: "Por que um LLM pode errar ao contar quantas letras 'r' existem numa palavra?"
    opcoes: ["Porque não conhece o alfabeto", "Porque a palavra é longa demais para a janela de contexto", "Porque enxerga o texto em tokens, que são pedaços de palavras, e não letra por letra", "Porque a temperatura estava alta"]
    correta: 2
    explicacao: "O texto chega ao modelo já quebrado em tokens. Uma palavra pode virar um ou dois pedaços, e as letras de dentro de cada pedaço não aparecem separadas. Contar letras, dígitos ou fazer contas longas são tarefas em que o modelo erra mais, e é melhor deixar para o código."
  - pergunta: "Num chat, o modelo 'lembra' o que você disse cinco mensagens atrás. Como isso funciona numa API como a do Claude?"
    opcoes: ["O aplicativo envia o histórico inteiro de novo a cada mensagem, e ele ocupa a janela de contexto", "O modelo guarda a conversa na memória entre uma chamada e outra", "O modelo é treinado de novo a cada mensagem", "A API guarda as conversas e as recupera pelo nome do usuário"]
    correta: 0
    explicacao: "A API não guarda estado: cada chamada é independente. Quem dá a impressão de memória é o aplicativo, que reenvia todas as mensagens anteriores junto com a nova. Por isso uma conversa longa ocupa cada vez mais tokens, e cada nova mensagem fica mais cara."
  - pergunta: "Uma conversa chegou ao limite da janela de contexto. O que é preciso fazer?"
    opcoes: ["Nada, o modelo resume sozinho o que esqueceu", "Aumentar a temperatura", "Trocar a pergunta por outra mais curta", "Cortar ou resumir parte do histórico: o que ficar de fora, o modelo simplesmente não vê"]
    correta: 3
    explicacao: "A janela é o limite de tokens que o modelo considera numa chamada, somando a entrada e a resposta. Passando dele, a chamada falha, e é preciso tirar mensagens antigas ou trocá-las por um resumo. O modelo não tem acesso a nada que ficou de fora."
  - pergunta: "Para extrair sempre os mesmos campos de notas fiscais, num modelo que permite ajustar a temperatura, que configuração faz mais sentido?"
    opcoes: ["Temperatura alta, para o modelo ser mais criativo", "Temperatura baixa, para concentrar a escolha nos tokens mais prováveis e reduzir a variação entre respostas", "Tanto faz, a temperatura não muda o resultado", "Temperatura alta, com várias tentativas e a escolha da melhor"]
    correta: 1
    explicacao: "A temperatura baixa deixa o modelo escolher quase sempre o token mais provável, e as respostas variam menos, o que é o desejado numa extração. Temperatura alta serve para tarefas criativas. Na API do Claude, a temperatura não é mais ajustável desde outubro de 2026: a consistência vem das instruções e das saídas estruturadas."
  - pergunta: "Uma chamada usou 10.000 tokens de entrada e 1.000 de saída, num modelo que cobra US$ 2 por milhão de tokens de entrada e US$ 10 por milhão de saída. Quanto custou?"
    opcoes: ["US$ 0,03", "US$ 0,12", "US$ 0,30", "US$ 30,00"]
    correta: 0
    explicacao: "Entrada: 10.000 ÷ 1.000.000 x 2 = US$ 0,02. Saída: 1.000 ÷ 1.000.000 x 10 = US$ 0,01. Total: US$ 0,03. Repare que a saída custa cinco vezes mais por token: respostas longas pesam mais na conta."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Explique para alguém do seu time, sem jargão, por que uma ferramenta de IA pode responder de jeitos diferentes à mesma pergunta e por que conversas muito longas ficam mais caras. Use as ideias de próximo token, amostragem e janela de contexto."
  rubrica:
    - "Explica que o modelo gera a resposta token a token, escolhendo entre opções com probabilidades, e que essa escolha tem uma parte de sorteio (amostragem), por isso a resposta pode variar."
    - "Explica que a API não guarda a conversa: o histórico inteiro é enviado de novo a cada mensagem e ocupa a janela de contexto."
    - "Conclui que, como o custo é por token de entrada e de saída, cada mensagem nova numa conversa longa paga de novo por todo o histórico, e sugere uma consequência prática, como começar uma conversa nova, resumir ou enviar só o necessário."
  modelo: "O modelo não busca uma resposta pronta: ele escreve a resposta um pedacinho de cada vez, os tokens. A cada passo, calcula quais pedaços são mais prováveis de vir em seguida e escolhe um deles. Essa escolha tem uma parte de sorteio, a amostragem: o pedaço mais provável sai na maioria das vezes, mas não sempre. Basta uma escolha diferente no começo para o resto da frase seguir outro caminho, e por isso a mesma pergunta pode ter respostas diferentes. Quanto à conversa, a ferramenta não tem memória de verdade: a cada mensagem nova, o aplicativo manda de novo toda a conversa anterior, e tudo isso ocupa o espaço que o modelo consegue ler de uma vez, a janela de contexto. Como a cobrança é por token lido e escrito, cada mensagem numa conversa longa paga de novo por todo o histórico. Na prática, para um assunto novo, vale começar uma conversa nova, e para trabalhos longos, resumir o que importa em vez de arrastar tudo."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Um modelo de linguagem de brinquedo"
  descricao: "Você vai construir em miniatura as peças de um LLM, sem chamar nenhuma API: um tokenizador por subpalavras, a temperatura e o top-p aplicados às probabilidades, um modelo que prevê a próxima palavra a partir de um texto, o corte do histórico para caber na janela de contexto e o cálculo do custo de uma chamada."
  pasta: "desafios/fundamentos_ia/como_llms_funcionam"
  testes: 10
  tempo: "1 h 30 min"
  ferramentas: "VS Code, Python 3.11 ou superior e pytest"
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
      descricao: "Abra desafios/fundamentos_ia/como_llms_funcionam/README.md. O texto de treino do seu modelo de brinquedo está em data/corpus.txt."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "Cada função tem uma docstring com o que recebe, o que devolve e um exemplo. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def tokenizar(texto, vocabulario):"
        - "def aplicar_temperatura(probabilidades, temperatura):"
        - "def filtrar_top_p(probabilidades, p):"
        - "def treinar_bigramas(texto):"
        - "def probabilidades_do_proximo(modelo, palavra):"
        - "def gerar_guloso(modelo, inicio, n):"
        - "def cortar_historico(mensagens, limite):"
        - "def cabe_na_janela(tokens_entrada, max_saida, janela):"
        - "def custo_em_dolares(tokens_entrada, tokens_saida, preco_entrada, preco_saida):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/fundamentos_ia/como_llms_funcionam"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/como_llms_funcionam"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de como um LLM funciona"'
        - "git push -u origin desafio/como_llms_funcionam"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Modelo de linguagem grande", en: "large language model (LLM)" }
  - { pt: "Token", en: "token" }
  - { pt: "Tokenizador", en: "tokenizer" }
  - { pt: "Previsão do próximo token", en: "next-token prediction" }
  - { pt: "Janela de contexto", en: "context window" }
  - { pt: "Instruções de sistema", en: "system prompt" }
  - { pt: "Amostragem", en: "sampling" }
  - { pt: "Temperatura", en: "temperature" }
  - { pt: "Top-p", en: "top-p, nucleus sampling" }
  - { pt: "Pré-treinamento", en: "pretraining" }
  - { pt: "Pós-treinamento", en: "post-training, fine-tuning" }
  - { pt: "Data de corte do conhecimento", en: "knowledge cutoff" }
  - { pt: "Nível de esforço", en: "effort" }
  - { pt: "Cache de prompt", en: "prompt caching" }
---

## O que um LLM faz: prever o próximo token

Um **modelo de linguagem grande** (LLM, do inglês *large language model*) faz uma coisa só, repetida muitas vezes: dado um texto, ele calcula quais pedaços de texto são mais prováveis de vir em seguida. Escolhe um, acrescenta ao final e calcula de novo. Uma resposta de três parágrafos é o resultado de centenas dessas previsões em sequência.

Essa capacidade vem do treinamento, em duas grandes etapas:

1. **Pré-treinamento.** O modelo lê uma quantidade enorme de texto e aprende a prever o próximo pedaço. Para prever bem, ele precisa captar gramática, fatos, estilos de escrita, raciocínios e código. O modelo não guarda esses textos como um banco de dados consultável: o que fica são padrões, distribuídos em bilhões de números, os parâmetros.
2. **Pós-treinamento.** Um modelo que só completa texto ainda não é um bom assistente. Nesta etapa, ele é ajustado com exemplos de conversas e com avaliações de pessoas para seguir instruções, responder de forma útil e recusar pedidos perigosos.

Três consequências importam para quem vai usar LLMs com dados:

- **O modelo produz texto plausível, e não necessariamente verdadeiro.** Ele foi otimizado para escrever o que provavelmente viria a seguir. Quase sempre isso coincide com a verdade, mas não sempre. O próximo tópico trata disso.
- **O modelo tem uma data de corte.** Ele não sabe o que aconteceu depois que os dados de treino foram coletados, a não ser que você forneça a informação na conversa ou dê a ele uma ferramenta de busca.
- **O modelo não conhece os seus dados.** As tabelas da sua empresa, as regras de negócio e o significado de cada coluna só existem para ele se estiverem na conversa.

Os modelos atuais também podem **raciocinar antes de responder**: geram uma etapa de pensamento, que pode ficar escondida, antes da resposta final. Na API do Claude, o nível de esforço (`effort`, de `low` a `max`) controla o quanto o modelo pensa. Mais esforço costuma dar respostas melhores em problemas difíceis, ao custo de mais tokens e mais tempo.

## Tokens: as peças que o modelo enxerga

O modelo não lê letras nem palavras inteiras: lê **tokens**, pedaços de texto definidos por um **tokenizador**. Palavras comuns costumam ser um token só. Palavras raras, longas ou de outros idiomas são quebradas em vários pedaços, como neste exemplo ilustrativo:

```text
"o modelo prevê"  ->  ["o", " modelo", " prev", "ê"]
"desvalorização"  ->  ["des", "valor", "ização"]
```

Os pedaços exatos dependem do tokenizador de cada modelo. Modelos de empresas diferentes quebram o texto de jeitos diferentes, e até modelos da mesma empresa podem ter tokenizadores diferentes. Como regra grosseira, um token tem algo como três ou quatro caracteres de texto em inglês. Português, números e código costumam gerar mais tokens para o mesmo tamanho de texto. Para saber o número exato, use a contagem do próprio provedor:

```python
import anthropic

# a chave vem da variável de ambiente ANTHROPIC_API_KEY
client = anthropic.Anthropic()

pergunta = "Quantos tokens tem esta frase?"
contagem = client.messages.count_tokens(
    model="claude-opus-5-5",
    messages=[{"role": "user", "content": pergunta}],
)
print(contagem.input_tokens)
```

Não use contadores de tokens de outros provedores para estimar o Claude: o resultado pode ficar bem distante.

Entender os tokens explica alguns tropeços conhecidos:

- **Contar letras.** Se "morango" vira dois tokens, o modelo não "vê" cada letra separada, e perguntas como "quantas letras r tem a palavra" ficam mais difíceis do que parecem.
- **Contas com números.** Um número como 1.234.567 vira vários pedaços. Somar uma coluna de cem valores "de cabeça" é exatamente o tipo de tarefa em que o modelo pode errar. Em trabalho com dados, deixe as contas para o código, inclusive o código que o próprio modelo escrever.

## Janela de contexto e conversas sem memória

A **janela de contexto** é o total de tokens que o modelo consegue considerar numa chamada. Ela inclui tudo: as instruções de sistema, o histórico da conversa, os documentos e tabelas colados, os resultados de ferramentas e a própria resposta que está sendo gerada. No fim de 2026, os modelos Claude atuais aceitam até 1 milhão de tokens de contexto, o equivalente a centenas de milhares de palavras.

O ponto que mais surpreende quem começa: **a API não tem memória**. Cada chamada é independente. Num chat, o que parece memória é o aplicativo enviando, a cada mensagem nova, todas as mensagens anteriores:

```python
mensagens = [
    {"role": "user", "content": "Meu time usa a tabela vendas."},
    {"role": "assistant", "content": "Certo. O que quer saber?"},
    {"role": "user", "content": "Que tabela o time usa?"},
]
# as três mensagens vão juntas na mesma chamada:
# sem as duas primeiras, o modelo não saberia responder
```

Disso saem três consequências práticas:

1. **Cada mensagem de uma conversa longa fica mais cara**, porque reenvia o histórico inteiro.
2. **Quando o histórico passa do limite, algo precisa sair.** É preciso cortar as mensagens mais antigas ou trocá-las por um resumo. O que ficou de fora, o modelo simplesmente não vê.
3. **Janela grande não é atenção perfeita.** Despejar documentos inteiros na conversa não garante que o modelo use bem cada detalhe. Instruções claras e só o material relevante, bem organizado, continuam fazendo diferença.

A resposta também ocupa a janela. O parâmetro `max_tokens` define o máximo de tokens que o modelo pode gerar, e a entrada mais esse máximo precisam caber no limite.

## Amostragem: temperatura e por que a resposta varia

A cada passo, o modelo produz uma lista de probabilidades para o próximo token. Por exemplo, depois de "o faturamento do mês":

| Próximo token | Probabilidade |
| ------------- | ------------- |
| " cresceu"    | 0,50          |
| " caiu"       | 0,30          |
| " foi"        | 0,20          |

Escolher sempre o mais provável parece seguro, mas leva a textos repetitivos: o modelo tende a cair em laços, como você vai ver no desafio. Por isso, os modelos **sorteiam** o próximo token segundo essas probabilidades. Esse sorteio é a **amostragem**, e é a razão de a mesma pergunta ter respostas diferentes.

Dois controles clássicos mudam o sorteio:

- **Temperatura.** Abaixo de 1, concentra a chance nos tokens mais prováveis e as respostas variam menos. Acima de 1, espalha a chance e as respostas ficam mais variadas, até perderem o sentido. Com temperatura 0,5, a tabela acima vira mais ou menos 0,66, 0,24 e 0,11.
- **Top-p.** Descarta os tokens menos prováveis e sorteia só entre os que, somados, chegam à probabilidade p. Com p = 0,7, sobram " cresceu" e " caiu".

Onde esses controles existem, a regra prática é temperatura baixa para extração, classificação e código, e mais alta para tarefas criativas. Na **API do Claude**, porém, eles deixaram de ser ajustáveis: desde a versão da API de 21 de outubro de 2026, uma requisição que envia temperatura ou top-p é recusada, em qualquer modelo, e os SDKs atuais nem aceitam mais esses parâmetros. O comportamento passa a ser controlado pelas instruções, pelo nível de esforço e, quando o formato importa, por **saídas estruturadas**, que você vai ver no tópico de prompting. Em outros provedores, e em muito código e documentação mais antigos, os dois parâmetros ainda aparecem, por isso vale entender o que fazem.

A lição para quem trabalha com dados: **uma resposta de LLM é uma amostra, e não um resultado determinístico**. Rodar a mesma análise duas vezes pode dar textos diferentes. Por isso, os números de uma análise devem vir de código que você consegue rodar de novo, e não do texto do modelo.

## Custo, limites e escolha de modelo

As APIs de LLM cobram **por token**, com preços diferentes para a entrada (o que você envia) e a saída (o que o modelo gera). A saída custa mais, porque é gerada token a token. O raciocínio do modelo, quando existe, também conta como tokens de saída. Os preços do Claude em novembro de 2026, em dólares por milhão de tokens:

| Modelo            | Entrada  | Saída    |
| ----------------- | -------- | -------- |
| Claude Opus 5.5   | US$ 4    | US$ 20   |
| Claude Sonnet 5.5 | US$ 2    | US$ 10   |
| Claude Haiku 5.5  | US$ 0,10 | US$ 0,50 |

- **Opus 5.5** (`claude-opus-5-5` na API): para tarefas difíceis, como análise, código e agentes.
- **Sonnet 5.5** (`claude-sonnet-5-5`): bom equilíbrio entre qualidade e custo para uso em volume.
- **Haiku 5.5** (`claude-haiku-5-5`): para tarefas simples e rápidas, como classificação. O preço da tabela vale para entradas de até 100 mil tokens.

Os preços mudam com o tempo, então confira sempre a página oficial antes de estimar um projeto.

A conta de uma chamada é direta. Com 10.000 tokens de entrada e 1.000 de saída no Sonnet 5.5:

```text
entrada: 10.000 ÷ 1.000.000 x US$ 2  = US$ 0,02
saída:    1.000 ÷ 1.000.000 x US$ 10 = US$ 0,01
total:                                 US$ 0,03
```

Parece pouco, e para uma pergunta é. Multiplicado por milhares de linhas de uma tabela, ou por um histórico de conversa reenviado a cada mensagem, vira dinheiro. Cada resposta da API informa quantos tokens foram usados, em `resposta.usage.input_tokens` e `resposta.usage.output_tokens`.

As formas mais comuns de reduzir o custo:

- **Escolher o modelo pelo tamanho da tarefa.** Classificar milhares de comentários em três categorias não precisa do modelo mais caro.
- **Mandar só o necessário.** Em vez da tabela inteira, as colunas e linhas que importam.
- **Cache de prompt.** Quando o começo da chamada se repete, como as mesmas instruções e o mesmo documento, a leitura em cache custa uma fração do preço normal da entrada.
- **Processamento em lote.** Para trabalhos que não precisam de resposta imediata, a API de lotes cobra a metade.
- **Limitar a saída.** Pedir respostas objetivas, e definir `max_tokens`, evita textos longos que ninguém vai ler.

Além do custo, as APIs têm **limites de uso**: quantas chamadas e quantos tokens por minuto cada conta pode fazer. Passando do limite, a chamada é recusada temporariamente e precisa ser repetida depois. O SDK oficial já repete automaticamente algumas vezes, esperando entre as tentativas.

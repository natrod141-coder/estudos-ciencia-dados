---
titulo: "Avaliação de sistemas com LLM"
modulo: ia_documentos
ordem: 3
horas: 10
estado: publicado
resumo: "Montar um conjunto de perguntas com respostas certas e medir quanto o sistema acerta."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Por que avaliar, e não só testar uns exemplos"
    tipo: leitura
    minutos: 8
  - id: a2
    titulo: "Montar o conjunto de avaliação"
    tipo: leitura
    minutos: 12
  - id: a3
    titulo: "Como dar nota a uma resposta"
    tipo: leitura
    minutos: 12
  - id: a4
    titulo: "A média esconde: separar por tipo e olhar item a item"
    tipo: leitura
    minutos: 10
  - id: a5
    titulo: "Quanto confiar numa diferença"
    tipo: leitura
    minutos: 12
  - id: a6
    titulo: "Um modelo como juiz"
    tipo: leitura
    minutos: 15
  - id: a7
    titulo: "Avaliar em produção"
    tipo: leitura
    minutos: 8
  - id: a8
    titulo: "Vídeo de apoio: avaliação de aplicações com LLM"
    tipo: video
    minutos: 30
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Por que montar um conjunto de avaliação antes de trocar o prompt de um assistente?"
    opcoes: ["Porque o modelo exige", "Para treinar o modelo com as perguntas", "Para medir o efeito da mudança em muitos casos, inclusive os difíceis, em vez de confiar em alguns exemplos que foram testados à mão", "Para deixar o assistente mais rápido"]
    correta: 2
    explicacao: "Uma mudança que melhora o exemplo testado pode piorar outros. Só um conjunto fixo, rodado antes e depois, mostra o saldo, e permite repetir a comparação a cada mudança."
  - pergunta: "O que deve entrar num conjunto de avaliação de um assistente de RAG?"
    opcoes: ["Perguntas reais e variadas, com a resposta esperada, incluindo casos difíceis e perguntas que os documentos não respondem", "Só as perguntas mais comuns, que o assistente já acerta", "Perguntas inventadas pelo próprio assistente", "Só perguntas fáceis, para o resultado sair alto"]
    correta: 0
    explicacao: "O conjunto precisa parecer com o uso real, e incluir de propósito os casos que costumam dar errado. Sem perguntas fora do escopo, por exemplo, ninguém mede se o sistema inventa respostas."
  - pergunta: "Quando vale usar uma regra em código, em vez de um modelo juiz, para dar nota às respostas?"
    opcoes: ["Nunca: o modelo juiz é sempre melhor", "Só quando o conjunto é pequeno", "Só para respostas em inglês", "Sempre que o critério puder ser conferido por código, como conter um valor, seguir um formato JSON ou citar só fontes enviadas: é mais barato, mais rápido e dá sempre o mesmo resultado"]
    correta: 3
    explicacao: "Regras em código são reprodutíveis e quase de graça. O modelo juiz entra para o que o código não consegue julgar, como a clareza de um resumo, e mesmo assim precisa ser conferido."
  - pergunta: "A versão nova do prompt subiu o acerto de 80% para 85%. O que olhar antes de aprovar?"
    opcoes: ["Nada, a média subiu", "O resultado por tipo de pergunta e item a item: a média pode esconder uma piora num tipo importante, como perguntas que deveriam ser recusadas", "Só o tempo de resposta", "Só as perguntas que a versão nova acertou"]
    correta: 1
    explicacao: "No desafio, a v2 acertou todas as perguntas factuais, mas passou a inventar respostas para três das cinco perguntas fora do escopo. Na média, ganhou; no risco, piorou muito."
  - pergunta: "Num conjunto de 20 perguntas, a versão nova acertou uma a mais que a antiga, e o intervalo de 95% da diferença, por bootstrap, foi de -0,20 a +0,30. O que concluir?"
    opcoes: ["Que a versão nova é 5 pontos melhor", "Que a versão antiga é melhor", "Que, com esse tamanho de conjunto, não dá para dizer qual é melhor: a diferença pode ser sorte", "Que o bootstrap está errado"]
    correta: 2
    explicacao: "O intervalo inclui o zero e valores negativos. Com poucas perguntas, uma diferença de uma resposta muda muito o percentual. Para decisões com diferenças pequenas, o conjunto precisa ser maior."
  - pergunta: "Qual destes é um viés conhecido de modelos usados como juízes?"
    opcoes: ["Dar notas mais altas a respostas longas e confiantes, mesmo quando trazem informação errada ou inventada", "Dar sempre nota mínima", "Recusar avaliar respostas em português", "Não conseguir ler JSON"]
    correta: 0
    explicacao: "No desafio, o juiz deu notas 3 e 4 a respostas inventadas pela v2, que as pessoas avaliaram com 1. Outros vieses conhecidos: preferir a primeira resposta numa comparação lado a lado e preferir respostas no próprio estilo."
  - pergunta: "Como saber se o modelo juiz é confiável?"
    opcoes: ["Perguntando a ele se as notas estão certas", "Usando o modelo mais caro disponível", "Pedindo notas de 1 a 10 em vez de 1 a 5", "Comparando as notas dele com as de pessoas numa amostra de respostas, e ajustando a rubrica até a concordância ficar boa"]
    correta: 3
    explicacao: "A concordância com pessoas é a calibração do juiz. No desafio, a concordância exata foi de só 50%, com as maiores diferenças justamente nas respostas inventadas: sinal de que a rubrica precisa punir informação sem fonte."
  - pergunta: "Por que incluir no conjunto perguntas cuja resposta não está nos documentos?"
    opcoes: ["Para o resultado sair mais baixo", "Para medir se o sistema admite que não sabe, em vez de inventar uma resposta plausível", "Porque o modelo fica mais rápido", "Para testar o tempo de resposta"]
    correta: 1
    explicacao: "Um assistente que nunca recusa parece ótimo em perguntas que têm resposta e é perigoso nas outras. Sem essas perguntas no conjunto, a alucinação simplesmente não aparece na avaliação."
  - pergunta: "O time ajustou o prompt vinte vezes, sempre olhando o mesmo conjunto de 30 perguntas, até chegar a 100% de acerto. Qual é o risco?"
    opcoes: ["Nenhum, 100% é o objetivo", "O conjunto ficar desatualizado", "Sobreajuste ao conjunto: o prompt foi moldado para aquelas 30 perguntas e pode não ir tão bem em perguntas novas; um segundo conjunto, guardado, mede isso", "O modelo aprender as perguntas"]
    correta: 2
    explicacao: "É o mesmo problema do teste no machine learning clássico. Ajustar muitas vezes olhando o mesmo conjunto faz o resultado nele ficar otimista. Guardar um conjunto separado, usado só para a decisão final, protege contra isso."
  - pergunta: "O assistente já está em produção. Como continuar avaliando?"
    opcoes: ["Não precisa: a avaliação é feita uma vez, antes de publicar", "Esperar reclamações dos usuários", "Rodar o mesmo conjunto todo dia, sem mudar nada", "Acompanhar sinais como a taxa de recusas e de citações erradas, revisar uma amostra de conversas e transformar os erros encontrados em itens novos do conjunto de avaliação"]
    correta: 3
    explicacao: "As perguntas reais mudam, os documentos mudam, e o comportamento dos modelos também. Monitorar e alimentar o conjunto com os erros de produção mantém a avaliação parecida com o uso real."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "O time quer trocar o modelo do assistente de políticas internas por um mais barato. Descreva como você decidiria se a troca é segura: o conjunto de avaliação, as medidas, como compararia as duas versões e o que olharia além da média."
  rubrica:
    - "Monta ou usa um conjunto com perguntas reais, casos difíceis e perguntas fora do escopo, com a resposta esperada, e roda as duas versões nele."
    - "Usa medidas conferidas por código sempre que possível, como fatos presentes, recusa correta e citações válidas, e um juiz calibrado com notas de pessoas para o que o código não julga."
    - "Compara por tipo de pergunta e item a item, considera a incerteza da diferença, por exemplo com bootstrap, e leva em conta custo e tempo de resposta na decisão."
  modelo: "Eu usaria o conjunto de avaliação do assistente, com umas 200 perguntas reais tiradas do histórico, separadas por tipo: factuais, que exigem combinar mais de um documento, e fora do escopo, que devem ser recusadas. Cada pergunta tem os fatos que a resposta precisa conter e o trecho de onde eles vêm. Rodaria as duas versões, com o mesmo prompt, e daria nota com regras em código: a resposta contém os fatos, cita só trechos enviados, recusa quando deve. Para a clareza das respostas, usaria um modelo juiz com uma rubrica escrita, depois de conferir, numa amostra de 30 respostas avaliadas por pessoas, que ele concorda com elas. Na comparação, não ficaria só na média: olharia o acerto por tipo de pergunta, principalmente as recusas, e a lista de perguntas que pioraram, uma por uma. Também calcularia o intervalo de incerteza da diferença, por bootstrap: se o modelo barato for um ponto pior e o intervalo for de menos quatro a mais dois, a diferença pode não existir, ou pode ser grande. A decisão juntaria isso com o custo e o tempo de resposta: se o modelo barato for equivalente no acerto e não piorar nas recusas, a economia justifica a troca. Depois da troca, acompanharia a taxa de recusas e de citações erradas em produção."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Medir o assistente antes de trocar o prompt"
  descricao: "Duas versões do prompt do assistente de políticas internas, 20 perguntas e as respostas gravadas de cada versão. Você vai dar nota com regras em código, descobrir que a versão nova, melhor na média, passou a inventar respostas, medir com bootstrap se a diferença é real e conferir se um modelo usado como juiz concorda com as notas dadas por pessoas."
  pasta: "desafios/ia_documentos/avaliacao_llm"
  testes: 11
  tempo: "2 h"
  ferramentas: "VS Code, Python 3.11 ou superior, numpy e pytest"
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
      descricao: "Abra desafios/ia_documentos/avaliacao_llm/README.md. O conjunto, as respostas, as notas do juiz e as notas humanas estão em data."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "A função carregar já está pronta. Cada função tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def normalizar_texto(texto):"
        - "def cobertura_de_fatos(resposta, fatos):"
        - "def recusou(resposta):"
        - "def avaliar_item(item, resposta):"
        - "def avaliar_versao(conjunto, respostas):"
        - "def comparar(por_item_a, por_item_b):"
        - "def intervalo_bootstrap(diferencas, n_reamostras=2000, semente=0):"
        - "def ler_nota_do_juiz(texto):"
        - "def media_do_juiz(juiz, versao):"
        - "def concordancia(pares):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/ia_documentos/avaliacao_llm"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/avaliacao_llm"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de avaliação de sistemas com LLM"'
        - "git push -u origin desafio/avaliacao_llm"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Conjunto de avaliação", en: "eval set, evaluation dataset" }
  - { pt: "Resposta de referência", en: "reference answer, ground truth" }
  - { pt: "Rubrica", en: "rubric" }
  - { pt: "Modelo como juiz", en: "LLM-as-a-judge" }
  - { pt: "Concordância entre avaliadores", en: "inter-rater agreement" }
  - { pt: "Calibração do juiz", en: "judge calibration" }
  - { pt: "Regressão", en: "regression" }
  - { pt: "Reamostragem bootstrap", en: "bootstrap resampling" }
  - { pt: "Intervalo de confiança", en: "confidence interval" }
  - { pt: "Comparação pareada", en: "paired comparison" }
  - { pt: "Viés de posição", en: "position bias" }
  - { pt: "Viés de tamanho", en: "verbosity bias" }
  - { pt: "Sobreajuste ao conjunto de avaliação", en: "overfitting to the eval set" }
---

## Por que avaliar, e não só testar uns exemplos

O jeito mais comum de "testar" uma mudança num sistema com LLM é perguntar três ou quatro coisas e olhar as respostas. Se parecem boas, a mudança vai para o ar. O problema é que um modelo de linguagem não é determinístico, e uma mudança que melhora um caso pode piorar outros, que ninguém olhou.

**Avaliar** é rodar o sistema num conjunto fixo de casos, com um critério de nota definido antes, e comparar os números. É o mesmo raciocínio do conjunto de teste no machine learning clássico, com uma dificuldade a mais: a resposta é texto, e dar nota a texto exige cuidado. Toda decisão sobre o sistema deveria passar por uma avaliação: trocar o prompt, trocar o modelo, mudar o nível de esforço, mudar o tamanho dos trechos de um RAG.

## Montar o conjunto de avaliação

Um bom conjunto parece com o uso real e inclui, de propósito, os casos que costumam dar errado:

- **Perguntas reais**, tiradas do histórico de uso ou dos chamados, e não só as que o time imagina.
- **Casos difíceis**: perguntas ambíguas, que exigem combinar dois documentos, com números e datas.
- **Perguntas fora do escopo**, cuja resposta não está nos documentos. Sem elas, ninguém mede se o sistema inventa.
- **Casos adversários**, como tentativas de injeção de prompt, se o sistema recebe texto de fora.
- **A resposta esperada** de cada caso: o valor exato, os fatos que precisam aparecer, o trecho de onde eles vêm, ou o comportamento certo, como recusar.

Algumas dezenas de casos servem para começar; algumas centenas, para decidir com segurança. O conjunto fica versionado, como o código, e cresce com o tempo: cada erro encontrado em produção vira um caso novo.

Um cuidado do machine learning clássico vale aqui também: se o time ajusta o prompt vinte vezes olhando o mesmo conjunto, o prompt fica moldado para aqueles casos, e o resultado neles fica otimista. Guarde um segundo conjunto, usado só na decisão final.

## Como dar nota a uma resposta

Do mais barato e confiável para o mais caro:

1. **Regras em código**, sempre que o critério permitir: a resposta contém o valor certo, contém todos os fatos esperados, é um JSON válido no formato combinado, cita só os trechos enviados, recusa quando deveria. São reprodutíveis e quase de graça. No desafio, toda a nota vem delas.
2. **Medidas de etapas intermediárias**, como o acerto nos k primeiros da busca de um RAG, que localizam onde o sistema erra.
3. **Um modelo como juiz**, para o que o código não consegue julgar: a clareza de um resumo, o tom de uma resposta, se uma explicação está correta em essência. Exige uma rubrica escrita e calibração, como na seção sobre o juiz.
4. **Pessoas**, a referência para calibrar tudo o resto. Caras e lentas, por isso usadas em amostras.

## A média esconde: separar por tipo e olhar item a item

No desafio, as duas versões do prompt do assistente de políticas internas são avaliadas em 20 perguntas: 15 factuais e 5 fora do escopo.

| Versão | Acerto geral | Factuais | Fora do escopo |
| ------ | ------------ | -------- | -------------- |
| v1     | 80%          | 73%      | 100%           |
| v2     | 85%          | 100%     | 40%            |

Pela média, a v2 é melhor. Separando por tipo, a história muda: a v2 acerta todas as factuais, mas passou a **inventar respostas** para três das cinco perguntas sem resposta nos documentos, como o valor de um vale-refeição que não existe na política. Para um assistente de RH, isso é pior que deixar de completar uma resposta.

Dois hábitos evitam esse engano: olhar o resultado **por tipo de caso**, e listar **item a item** o que melhorou e o que piorou. Uma comparação pareada, caso a caso, mostra exatamente onde está o ganho e onde está a perda.

## Quanto confiar numa diferença

Mesmo sem a piora escondida, 85% contra 80% em 20 perguntas é uma resposta a mais. Isso é diferença ou sorte? O **bootstrap** dá uma estimativa:

1. Para cada pergunta, calcule a diferença entre as versões: +1 se só a nova acertou, -1 se só a antiga acertou, 0 se empataram.
2. Sorteie, com reposição, um conjunto de 20 diferenças, e calcule a média. Repita milhares de vezes.
3. Os percentis 2,5 e 97,5 dessas médias formam um intervalo de 95% para a diferença.

```python
import numpy as np

gerador = np.random.default_rng(0)
diferencas = np.array(diferencas)
sorteios = gerador.integers(0, len(diferencas), size=(2000, len(diferencas)))
medias = diferencas[sorteios].mean(axis=1)
print(np.percentile(medias, [2.5, 97.5]))  # [-0.2  0.3]
```

No desafio, o intervalo vai de -0,20 a +0,30: inclui o zero e até uma piora considerável. Com 20 perguntas, não dá para dizer que a v2 é melhor. Para diferenças de poucos pontos, o conjunto precisa de centenas de casos. A regra prática: quanto menor a diferença que você quer detectar, maior o conjunto.

## Um modelo como juiz

Para critérios que o código não confere, um modelo de linguagem pode dar a nota, seguindo uma **rubrica**:

```text
Você avalia respostas de um assistente de políticas internas.
Compare a resposta com a resposta de referência e os trechos de origem.

Dê uma nota de 1 a 5:
5 - correta, completa e só com informação dos trechos
3 - correta, mas incompleta
1 - errada, ou com informação que não está nos trechos

Responda só com JSON: {"justificativa": "...", "nota": n}
```

Três práticas melhoram o juiz: pedir a justificativa **antes** da nota, uma rubrica com a descrição de cada nível, e saída estruturada, para a nota poder ser lida por código. Mesmo assim, juízes têm vieses conhecidos: preferem respostas longas e confiantes, preferem a primeira resposta quando comparam duas lado a lado e tendem a gostar de respostas no próprio estilo.

Por isso, o juiz precisa ser **calibrado**: compare as notas dele com as de pessoas numa amostra de respostas. No desafio, a média do juiz é 4,4 para a v1 e 4,8 para a v2. Ele prefere a v2, a versão que inventa. Nas 12 respostas que pessoas também avaliaram, a concordância exata é de só 50%, e as maiores diferenças estão justamente nas respostas inventadas: o juiz deu 3 e 4 a respostas que as pessoas avaliaram com 1. A rubrica precisa punir, de forma explícita, informação que não está nos trechos, e a calibração precisa ser refeita depois do ajuste.

## Avaliar em produção

A avaliação não acaba quando o sistema vai para o ar. As perguntas mudam, os documentos mudam, e o comportamento dos modelos muda a cada versão. Em produção, acompanhe:

- **Sinais automáticos**: a taxa de recusas, a taxa de citações fora do contexto, o tamanho das respostas, o custo e o tempo por resposta.
- **A opinião de quem usa**, com um botão de útil e não útil, sabendo que ela é rara e enviesada.
- **Uma amostra revisada por pessoas**, toda semana.
- **O conjunto de avaliação como teste de regressão**: rodado a cada mudança, como os testes de código, e alimentado com os erros encontrados.

Uma avaliação bem feita é o que permite mudar o sistema com confiança: trocar o modelo por um mais barato, ajustar o prompt, mexer na busca, e saber, com números, o que melhorou e o que piorou.

---
titulo: "Teste A/B"
modulo: estatistica
ordem: 8
horas: 5
estado: publicado
resumo: "Como comparar duas versões de algo e decidir com base em evidência."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "O que é um teste A/B e por que sortear"
    tipo: leitura
    minutos: 10
  - id: a2
    titulo: "Antes de começar: métrica, efeito mínimo e tamanho da amostra"
    tipo: leitura
    minutos: 15
  - id: a3
    titulo: "Analisando o resultado: duas proporções e intervalo de confiança"
    tipo: leitura
    minutos: 15
  - id: a4
    titulo: "Armadilhas: espiar, dividir errado e testar demais"
    tipo: leitura
    minutos: 12
  - id: a5
    titulo: "Vídeo de apoio sobre testes A/B"
    tipo: video
    minutos: 20
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Por que os visitantes de um teste A/B precisam ser sorteados entre os grupos, em vez de, por exemplo, mostrar a versão nova só para quem acessa pelo celular?"
    opcoes: ["Para o teste terminar mais rápido", "Para que a única diferença sistemática entre os grupos seja a versão que eles veem, e a diferença no resultado possa ser atribuída a ela", "Porque o celular não mostra bem a versão nova", "Para ter mais visitantes em cada grupo"]
    correta: 1
    explicacao: "Com o sorteio, os grupos ficam parecidos em tudo, em média: aparelho, região, horário, intenção de compra. A única diferença sistemática passa a ser a versão. Se só o celular vê a versão nova, uma diferença no resultado pode vir do tipo de aparelho, e não da versão."
  - pergunta: "Um analista olha o resultado todo dia e encerra o teste no primeiro dia em que o valor p fica abaixo de 0,05. Qual é o problema?"
    opcoes: ["Nenhum, desde que o valor p fique abaixo de 0,05", "O teste deveria ter usado α = 10%", "O valor p oscila conforme os dados se acumulam, e parar no primeiro momento favorável aumenta muito a chance de falso positivo", "O único problema é olhar antes do fim da primeira semana"]
    correta: 2
    explicacao: "O α de 5% vale para uma única análise, feita no fim. Com uma olhada por dia durante duas semanas, a chance de ver p < 0,05 em algum momento, mesmo sem nenhuma diferença real, passa de 20%. A duração deve ser decidida antes e respeitada."
  - pergunta: "A conversão atual é de 10%. Para detectar um aumento de 2 pontos percentuais, cada grupo precisa de cerca de 3.800 visitantes. Quantos precisaria para detectar um aumento de 1 ponto?"
    opcoes: ["Cerca de 1.900", "Cerca de 3.800", "Cerca de 7.600", "Cerca de 15.000"]
    correta: 3
    explicacao: "O tamanho da amostra cresce com o inverso do quadrado do efeito. Efeito pela metade exige cerca de 4 vezes mais visitantes: 14.749 por grupo. Detectar efeitos pequenos custa caro, e por isso o efeito mínimo precisa ser escolhido com cuidado."
  - pergunta: "Um teste deveria dividir o tráfego meio a meio, mas terminou com 10.000 visitantes em A e 10.500 em B. O que fazer?"
    opcoes: ["Investigar a divisão antes de confiar no resultado: uma diferença desse tamanho é muito improvável por acaso e indica problema técnico", "Nada, 500 visitantes é uma diferença pequena", "Descartar 500 visitantes de B para igualar os grupos", "Usar só os dados do grupo A"]
    correta: 0
    explicacao: "Com 20.500 visitantes e divisão real de 50%, uma diferença assim tem menos de 0,1% de chance de acontecer por acaso. É o chamado sample ratio mismatch (SRM), e indica falha técnica: redirecionamento, erro de registro, robôs. Qualquer que seja a causa, ela pode afetar a conversão, e o resultado não é confiável."
  - pergunta: "Por que um teste A/B costuma durar semanas completas, por exemplo 14 dias, e não 10?"
    opcoes: ["Porque o teste z exige um número par de dias", "Porque a ferramenta de analytics só exporta semanas", "Não há motivo, qualquer duração serve", "Porque o público e o comportamento mudam com o dia da semana, e semanas completas fazem o resultado representar uma semana típica"]
    correta: 3
    explicacao: "Quem compra no sábado pode reagir diferente de quem compra na terça. Com semanas completas, cada dia da semana entra na mesma proporção, e o efeito medido vale para o uso normal do site. Uma duração maior também ajuda a diluir o efeito novidade."
  - pergunta: "Um teste compara 5 versões de uma página com a original, e cada comparação usa α = 5%. Uma das cinco deu p = 0,04. O que considerar?"
    opcoes: ["Que essa versão venceu com certeza", "Que, com 5 comparações, a chance de pelo menos um falso positivo passa de 20%, e o resultado precisa de correção ou de um teste de confirmação", "Que o teste deveria ter usado α = 10%", "Que todas as outras versões são piores que a original"]
    correta: 1
    explicacao: "Cada comparação tem 5% de chance de falso positivo. Com cinco comparações, a chance de ao menos uma dar 'significativa' por acaso é 1 − 0,95⁵ ≈ 23%. Com a correção de Bonferroni, o limite seria 0,05 ÷ 5 = 0,01, e p = 0,04 não passaria."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "O time de produto rodou um teste A/B por 3 dias, viu que a versão nova tinha conversão 15% maior, com p = 0,03, e quer lançá-la para todos os clientes. Aponte os problemas desse teste e diga o que você faria diferente."
  rubrica:
    - "Aponta que 3 dias é pouco: não cobre semanas completas, o comportamento muda entre dias da semana, e o efeito novidade pode inflar o resultado no começo."
    - "Aponta o risco de ter parado cedo por causa de um resultado favorável, o que aumenta a chance de falso positivo, e pergunta se o tamanho da amostra foi calculado antes."
    - "Propõe definir antes a métrica, o efeito mínimo, o tamanho da amostra e a duração em semanas completas, conferir a divisão do tráfego e reportar o intervalo de confiança da diferença."
  modelo: "Três dias não cobrem uma semana completa, e o comportamento de compra muda entre os dias da semana. Além disso, uma versão nova pode chamar atenção só por ser nova, e esse efeito novidade costuma sumir com o tempo. Também não está claro se o teste foi planejado para durar 3 dias ou se parou quando o p ficou abaixo de 0,05. Se parou por isso, a chance de falso positivo é bem maior que 5%. Eu calcularia antes o tamanho da amostra, a partir da conversão atual e do menor aumento que vale a pena detectar, e fixaria a duração em semanas completas, pelo menos duas. No fim, conferiria se o tráfego foi dividido meio a meio e reportaria a diferença com o intervalo de confiança, e não só o valor p. Um aumento de 15% com um intervalo que vai de quase zero a 30% pede cautela."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "O botão novo vende mais?"
  descricao: "Uma loja online testou um novo botão de finalizar compra por duas semanas. Você vai calcular o tamanho de amostra, conferir se o tráfego foi bem dividido, comparar as taxas de conversão com um teste de duas proporções, medir o efeito com um intervalo de confiança e ver o que acontece com o valor p quando alguém espia o resultado todo dia."
  pasta: "desafios/estatistica/teste_ab"
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
      descricao: "Abra desafios/estatistica/teste_ab/README.md. Os dados estão em data/experimento.csv: uma linha por dia e por grupo, com a data, o grupo (A ou B), o número de visitantes e o número de conversões."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "Cada função tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def taxa_conversao(conversoes, visitantes):"
        - "def teste_duas_proporcoes(conv_a, n_a, conv_b, n_b):"
        - "def intervalo_diferenca(conv_a, n_a, conv_b, n_b, confianca=0.95):"
        - "def tamanho_amostra_por_grupo(taxa_base, efeito_minimo, alfa=0.05, poder=0.80):"
        - "def divisao_balanceada(n_a, n_b, limite=0.001):"
        - "def decidir(conv_a, n_a, conv_b, n_b, alfa=0.05):"
        - "def analisar_experimento(caminho_csv, alfa=0.05):"
        - "def evolucao_do_p(caminho_csv):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/estatistica/teste_ab"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/teste_ab"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de teste A/B"'
        - "git push -u origin desafio/teste_ab"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Teste A/B", en: "A/B test, split test" }
  - { pt: "Grupo de controle", en: "control group" }
  - { pt: "Grupo de tratamento (variante)", en: "treatment group, variant" }
  - { pt: "Aleatorização", en: "randomization" }
  - { pt: "Taxa de conversão", en: "conversion rate" }
  - { pt: "Aumento relativo", en: "lift, relative uplift" }
  - { pt: "Efeito mínimo detectável", en: "minimum detectable effect (MDE)" }
  - { pt: "Métrica de proteção", en: "guardrail metric" }
  - { pt: "Divisão desbalanceada", en: "sample ratio mismatch (SRM)" }
  - { pt: "Espiar o resultado", en: "peeking" }
  - { pt: "Efeito novidade", en: "novelty effect" }
  - { pt: "Teste A/A", en: "A/A test" }
---

## O que é um teste A/B e por que sortear

Um **teste A/B** compara duas versões de algo, como uma página, um botão, um e-mail ou um preço, mostrando cada versão a um grupo diferente de pessoas escolhidas por sorteio. A versão atual é o **controle** (A), e a nova é a **variante** (B). No fim, compara-se uma métrica, como a taxa de conversão, entre os dois grupos.

É um teste de hipóteses aplicado a um experimento controlado:

- H0: as duas versões têm a mesma taxa de conversão.
- H1: as taxas são diferentes.

O que faz o teste A/B funcionar é o **sorteio**. Como cada visitante cai em A ou em B por acaso, os dois grupos ficam parecidos em tudo, em média: aparelho, região, horário, intenção de compra. A única diferença sistemática entre eles é a versão que viram. Por isso, uma diferença no resultado pode ser atribuída à versão. Esse é um dos poucos jeitos de medir **causa**, e não só associação.

Compare com a alternativa comum de "mudar o site e comparar com o mês passado". Qualquer diferença pode vir da mudança, mas também da sazonalidade, de uma campanha de marketing, de um concorrente ou da economia. Sem grupo de controle, não há como separar esses efeitos.

Dois cuidados de execução:

- **Sorteie pessoas, e não visitas.** A mesma pessoa deve ver sempre a mesma versão. Se ela alternar entre A e B, os grupos se misturam.
- **Faça um teste A/A antes de confiar na ferramenta.** Mostre a mesma versão para os dois grupos. Se o teste acusar diferença com frequência maior que o α, há algo errado na divisão ou na medição.

## Antes de começar: métrica, efeito mínimo e tamanho da amostra

Quase todos os erros de teste A/B são decisões que deveriam ter sido tomadas antes de o teste começar.

**1. A hipótese e a métrica principal.** Escreva em uma frase: "o botão novo aumenta a taxa de conversão do checkout". Escolha **uma** métrica principal para a decisão. Defina também **métricas de proteção**, que não podem piorar: ticket médio, taxa de cancelamento, tempo de carregamento. Uma variante que converte mais, mas dobra as devoluções, não é uma vitória.

**2. O efeito mínimo detectável (MDE).** É o menor aumento que vale a pena detectar, e é uma decisão de negócio. Se a conversão é 10%, um aumento de 2 pontos percentuais leva a 12%. Repare na diferença entre aumento **absoluto** (+2 pontos percentuais) e **relativo** (+20%, o chamado *lift*). Deixe sempre claro de qual dos dois está falando.

**3. O tamanho da amostra.** Com a conversão atual, o MDE, o α e o poder desejado, calcula-se quantos visitantes cada grupo precisa:

n por grupo = (z do α + z do poder)² × [p₁ × (1 − p₁) + p₂ × (1 − p₂)] ÷ MDE²

Aqui, p₁ é a taxa atual e p₂ = p₁ + MDE. Com α = 5% (bilateral), o z do α é 1,96. Com poder de 80%, o z do poder é 0,84. Para uma conversão atual de 10%:

| Efeito mínimo (pontos percentuais) | Visitantes por grupo |
| ---------------------------------- | -------------------- |
| 1 (de 10% para 11%)                | 14.749               |
| 2 (de 10% para 12%)                | 3.839                |
| 3 (de 10% para 13%)                | 1.772                |
| 5 (de 10% para 15%)                | 683                  |

Efeito pela metade exige cerca de quatro vezes mais visitantes, porque o MDE entra ao quadrado no denominador.

**4. A duração.** Divida o tamanho da amostra pelos visitantes que cada grupo recebe por dia e arredonde para **semanas completas**. O comportamento muda com o dia da semana, e semanas completas fazem o resultado representar uma semana típica. Com 14.749 visitantes por grupo e cerca de 700 por dia em cada grupo, são 22 dias, arredondados para 4 semanas. Rode pelo menos duas semanas, mesmo que a conta dê menos: isso também dilui o **efeito novidade**, a curiosidade inicial que faz qualquer mudança parecer boa nos primeiros dias.

## Analisando o resultado: duas proporções e intervalo de confiança

A loja do desafio testou um botão novo por duas semanas:

| Grupo       | Visitantes | Conversões | Taxa de conversão |
| ----------- | ---------- | ---------- | ----------------- |
| A (antigo)  | 10.051     | 997        | 9,92%             |
| B (novo)    | 10.021     | 1.108      | 11,06%            |

A diferença é de 1,14 ponto percentual, um *lift* de 11,5%. É grande o bastante para não ser acaso?

**Primeiro, confira a divisão.** A divisão planejada era meio a meio, e 10.051 contra 10.021 é compatível com isso. Uma divisão muito desigual, o **sample ratio mismatch**, indica falha técnica. Nesse caso, o resultado não é confiável, por melhor que pareça. A checagem é um teste de proporção: a fração de visitantes em A é compatível com 50%? Por convenção, usa-se um limite rigoroso, p < 0,001, para acusar o problema.

**Depois, o teste de duas proporções.** Sob H0, os dois grupos têm a mesma taxa, então o erro padrão usa a taxa combinada:

taxa combinada = (997 + 1.108) ÷ (10.051 + 10.021) ≈ 10,49%

z = (taxa B − taxa A) ÷ √(combinada × (1 − combinada) × (1/nA + 1/nB)) ≈ 2,63

O valor p bilateral é ≈ 0,0085. Com α = 5%, rejeita-se H0: o botão novo converte mais.

**Por fim, o intervalo de confiança da diferença.** Aqui não se supõe H0, e cada grupo entra com a própria taxa no erro padrão. O intervalo de 95% vai de +0,29 a +1,99 ponto percentual. Essa é a informação mais útil para a decisão: o ganho é quase certamente positivo, mas pode ser modesto, de 0,3 ponto, ou expressivo, de 2 pontos. Se o botão novo tivesse custo alto, valeria pesar o cenário pessimista.

Em Python, com a biblioteca statsmodels (`pip install statsmodels`):

```python
from statsmodels.stats.proportion import proportions_ztest

conversoes = [1108, 997]      # B, A
visitantes = [10021, 10051]
z, p = proportions_ztest(count=conversoes, nobs=visitantes)
print(z, p)   # z ≈ 2,63, p ≈ 0,0085
```

No desafio, você vai implementar esse teste na mão, com `statistics.NormalDist`, para entender cada passo.

## Armadilhas: espiar, dividir errado e testar demais

**Espiar o resultado (peeking).** O valor p oscila conforme os dados se acumulam. Nos dados do desafio, o p acumulado foi 0,024 no terceiro dia, 0,20 no oitavo e 0,0085 no décimo quarto. Quem parasse no terceiro dia "teria resultado". Quem olhasse no oitavo desistiria de uma melhoria real. O α de 5% vale para **uma** análise no fim. Numa simulação de teste A/A, sem nenhuma diferença real, com 700 visitantes por grupo por dia durante 14 dias:

- analisando só no fim, 5% dos testes deram falso positivo;
- olhando todo dia e parando no primeiro p < 0,05, foram 22%.

Acompanhar o teste para detectar falhas técnicas é saudável. Decidir antes da data marcada, não. Quando é preciso decidir no meio do caminho, existem métodos próprios para isso, os testes sequenciais, que ajustam o limite a cada olhada.

**Divisão desbalanceada.** Sempre confira se os grupos têm o tamanho esperado antes de olhar a métrica. Causas comuns: redirecionamento que perde visitantes numa das versões, erro no registro de eventos, robôs caindo mais num grupo.

**Comparações múltiplas.** Testar muitas variantes, muitas métricas ou muitos segmentos multiplica os falsos positivos. Com 5 variantes contra o controle, a chance de pelo menos uma dar "significativa" por acaso é de 23%. Defina a métrica principal antes e corrija o α quando fizer várias comparações. Desconfie de conclusões como "não funcionou no geral, mas funcionou para usuários de iPhone no Nordeste": se o segmento não foi definido antes, é quase certamente acaso, e merece um novo teste.

**Significância estatística não é importância.** Com tráfego enorme, até diferenças irrelevantes dão p pequeno. Decida pelo intervalo de confiança do efeito comparado ao MDE, e não só pelo valor p.

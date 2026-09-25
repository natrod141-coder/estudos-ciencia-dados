---
titulo: "Teste de hipóteses"
modulo: estatistica
ordem: 7
horas: 6
estado: publicado
resumo: "Hipótese nula, valor p e nível de significância."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "A lógica do teste de hipóteses"
    tipo: leitura
    minutos: 10
  - id: a2
    titulo: "Hipótese nula, alternativa e nível de significância"
    tipo: leitura
    minutos: 10
  - id: a3
    titulo: "Estatística de teste e valor p"
    tipo: leitura
    minutos: 15
  - id: a4
    titulo: "Erros tipo I e tipo II, e poder do teste"
    tipo: leitura
    minutos: 12
  - id: a5
    titulo: "Intervalo de confiança e significância prática"
    tipo: leitura
    minutos: 12
  - id: a6
    titulo: "Testes na prática com Python"
    tipo: leitura
    minutos: 12
  - id: a7
    titulo: "Vídeo de apoio sobre valor p e teste de hipóteses"
    tipo: video
    minutos: 20
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Um teste deu valor p = 0,03. Qual interpretação está correta?"
    opcoes: ["Há 3% de chance de a hipótese nula ser verdadeira", "Se a hipótese nula fosse verdadeira, haveria 3% de chance de observar um resultado tão extremo quanto este, ou mais", "Há 97% de chance de a hipótese alternativa ser verdadeira", "O efeito encontrado é pequeno, de 3%"]
    correta: 1
    explicacao: "O valor p é calculado supondo que H0 é verdadeira: ele mede o quanto os dados seriam surpreendentes nesse cenário. Ele não é a probabilidade de H0 ser verdadeira, nem mede o tamanho do efeito. Confundir essas coisas é o erro mais comum com valor p."
  - pergunta: "Com nível de significância de 5%, um teste deu p = 0,12. Qual é a conclusão correta?"
    opcoes: ["Aceitamos a hipótese nula: está provado que não há diferença", "Rejeitamos a hipótese nula", "O teste está errado, porque o valor p deveria ser menor que 0,05", "Não rejeitamos a hipótese nula: os dados não trazem evidência suficiente contra ela"]
    correta: 3
    explicacao: "Como 0,12 é maior que 0,05, não rejeitamos H0. Isso não prova que H0 é verdadeira: a diferença pode existir e o teste não ter tido força para detectá-la. É como num julgamento: 'inocente por falta de provas' não é o mesmo que 'comprovadamente inocente'."
  - pergunta: "Um laboratório conclui que um remédio funciona quando, na verdade, ele não funciona. Que erro é esse?"
    opcoes: ["Erro tipo I, um falso positivo", "Erro tipo II, um falso negativo", "Erro amostral", "Viés de seleção"]
    correta: 0
    explicacao: "Rejeitar H0 ('o remédio não tem efeito') quando ela é verdadeira é o erro tipo I, um falso positivo. A probabilidade de cometê-lo é o nível de significância α. O erro tipo II é o contrário: não detectar um efeito que existe."
  - pergunta: "O que acontece com a chance de erro tipo II quando o nível de significância passa de 5% para 1%, mantendo o tamanho da amostra?"
    opcoes: ["Diminui", "Não muda", "Aumenta", "Vira zero"]
    correta: 2
    explicacao: "Com α menor, fica mais difícil rejeitar H0. Isso reduz os falsos positivos, mas aumenta a chance de não detectar um efeito real, o erro tipo II. Para reduzir os dois ao mesmo tempo, é preciso aumentar a amostra."
  - pergunta: "Um fornecedor garante que no máximo 5% das peças têm defeito. Você desconfia que a taxa real é maior. Qual par de hipóteses usar?"
    opcoes: ["H0: p = 0,05 e H1: p ≠ 0,05", "H0: p ≤ 0,05 e H1: p > 0,05", "H0: p > 0,05 e H1: p ≤ 0,05", "H0: p < 0,05 e H1: p = 0,05"]
    correta: 1
    explicacao: "A hipótese nula é a afirmação do fornecedor, o status quo, e a alternativa é o que você quer demonstrar: que a taxa é maior. Como só interessa um lado, o teste é unilateral. O teste bilateral, com H1: p ≠ 0,05, serviria se uma taxa menor também fosse um problema."
  - pergunta: "Um teste com 2 milhões de usuários mostrou que um novo botão aumenta o tempo no app em 0,2 segundo por sessão, com p = 0,0001. O que concluir?"
    opcoes: ["A mudança é importante, porque o valor p é muito pequeno", "O teste errou, porque 0,2 segundo não pode ser significativo", "É preciso repetir o teste com menos usuários", "A diferença é estatisticamente significativa, mas pode não ter importância prática: com amostras enormes, até efeitos minúsculos dão valor p pequeno"]
    correta: 3
    explicacao: "O valor p diz se o efeito é distinguível do acaso, e não se ele importa. Com 2 milhões de usuários, o teste detecta diferenças minúsculas. Se 0,2 segundo vale o custo da mudança é uma decisão de negócio, e o intervalo de confiança do efeito ajuda mais nessa decisão do que o valor p."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Uma empresa testou um novo roteiro de vendas com 20 vendedores e comparou com outros 20 que usaram o roteiro antigo. O teste deu p = 0,20. O gerente concluiu: 'Está provado que o roteiro novo não funciona.' Explique o erro dessa conclusão e como ela deveria ser escrita."
  rubrica:
    - "Explica que não rejeitar a hipótese nula não prova que ela é verdadeira: falta de evidência de efeito não é evidência de que o efeito não existe."
    - "Aponta que, com poucos vendedores, o teste tem pouco poder e pode ter deixado de detectar um efeito real (erro tipo II)."
    - "Propõe uma conclusão correta, como 'os dados não mostraram diferença significativa entre os roteiros', e sugere olhar o intervalo de confiança do efeito ou repetir o teste com mais vendedores."
  modelo: "O p = 0,20 só diz que os dados não trouxeram evidência suficiente para rejeitar a hipótese nula de que os roteiros dão o mesmo resultado. Não rejeitar H0 é diferente de provar H0. Com 20 vendedores em cada grupo, o teste tem pouco poder: mesmo que o roteiro novo aumentasse as vendas, a variação natural entre vendedores poderia esconder o efeito, e isso seria um erro tipo II. A conclusão correta seria: 'com esta amostra, não encontramos diferença significativa entre os roteiros'. Eu olharia também o intervalo de confiança da diferença: se ele vai de uma pequena queda a um grande aumento, a questão continua em aberto, e vale repetir o teste com mais vendedores ou por mais tempo."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "O pacote tem mesmo 500 gramas?"
  descricao: "Um órgão de fiscalização pesou 40 pacotes de café com 500 g no rótulo, e a média deu um pouco abaixo. Você vai implementar testes z para média e proporção, calcular valores p e intervalos de confiança sem bibliotecas estatísticas prontas e decidir se a máquina de envase está desregulada."
  pasta: "desafios/estatistica/teste_hipoteses"
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
      descricao: "Abra desafios/estatistica/teste_hipoteses/README.md. Os dados estão em data/pacotes.csv: uma linha por pacote, com o número do pacote e o peso medido em gramas."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "Cada função tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - 'def valor_p(z, alternativa="bilateral"):'
        - 'def teste_z_media(amostra, mu0, alternativa="bilateral"):'
        - 'def teste_z_proporcao(sucessos, n, p0, alternativa="bilateral"):'
        - "def rejeita_h0(p, alfa=0.05):"
        - "def intervalo_confianca_media(amostra, confianca=0.95):"
        - "def analisar_pacotes(caminho_csv, peso_rotulo=500, alfa=0.05):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/estatistica/teste_hipoteses"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/teste_hipoteses"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de teste de hipóteses"'
        - "git push -u origin desafio/teste_hipoteses"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Hipótese nula", en: "null hypothesis (H0)" }
  - { pt: "Hipótese alternativa", en: "alternative hypothesis (H1, Ha)" }
  - { pt: "Nível de significância", en: "significance level (α)" }
  - { pt: "Valor p", en: "p-value" }
  - { pt: "Estatística de teste", en: "test statistic" }
  - { pt: "Erro padrão", en: "standard error (SE)" }
  - { pt: "Teste bilateral", en: "two-sided (two-tailed) test" }
  - { pt: "Teste unilateral", en: "one-sided (one-tailed) test" }
  - { pt: "Erro tipo I", en: "type I error, false positive" }
  - { pt: "Erro tipo II", en: "type II error, false negative" }
  - { pt: "Poder do teste", en: "statistical power" }
  - { pt: "Intervalo de confiança", en: "confidence interval (CI)" }
  - { pt: "Teorema central do limite", en: "central limit theorem" }
  - { pt: "Comparações múltiplas", en: "multiple comparisons" }
---

## A lógica do teste de hipóteses

Uma torrefação vende pacotes de café com 500 g no rótulo. Um fiscal pesa 40 pacotes, e a média dá 498,15 g. A máquina de envase está desregulada, ou essa diferença é só a variação natural de um pacote para outro?

Nenhuma amostra dá a média exata da população, então sempre haverá alguma diferença. O **teste de hipóteses** é o método para decidir se uma diferença observada é grande demais para ser atribuída ao acaso.

A lógica é a de um julgamento:

1. Parte-se da presunção de inocência: a máquina está certa, e a média real é 500 g.
2. Olha-se a evidência: a média da amostra, 498,15 g.
3. Pergunta-se: se a máquina estivesse certa, seria muito raro obter uma amostra assim?
4. Se for raro o bastante, a presunção cai e conclui-se que a máquina está desregulada. Se não for, a presunção se mantém por falta de provas.

Repare no último passo. "Não há provas suficientes" é diferente de "está provado que a máquina está certa". Essa assimetria é o ponto mais importante do tópico.

## Hipótese nula, alternativa e nível de significância

A **hipótese nula (H0)** é a afirmação do status quo: não há efeito, não há diferença, o valor é o anunciado. É a hipótese que o teste tenta derrubar. No exemplo, H0: a média é 500 g.

A **hipótese alternativa (H1)** é o que você quer demonstrar. Ela pode ser:

- **Bilateral:** H1: média ≠ 500 g. Interessa qualquer desvio, para mais ou para menos. É a pergunta do controle de qualidade da torrefação: pacotes leves lesam o consumidor, e pacotes pesados dão prejuízo à empresa.
- **Unilateral:** H1: média < 500 g. Só interessa um lado. Um fiscal preocupado apenas com o consumidor poderia usar esta.

Neste tópico e no desafio, o teste dos pacotes é bilateral.

O **nível de significância (α)** é o limite do que se considera raro. O valor mais usado é 5%: se o resultado observado teria menos de 5% de chance de acontecer com H0 verdadeira, rejeita-se H0. Em áreas em que um falso alarme custa caro, como medicina, usa-se 1% ou menos.

As hipóteses, o tipo de teste e o α são escolhidos **antes** de olhar os dados. Escolher depois, conforme o que der o resultado desejado, invalida o teste.

## Estatística de teste e valor p

Para medir o quanto a amostra se afasta de H0, calcula-se uma **estatística de teste**. Para a média de uma amostra grande:

z = (média da amostra − média de H0) ÷ erro padrão, em que erro padrão = desvio padrão da amostra ÷ √n

O **erro padrão** mede o quanto a média da amostra varia de uma amostra para outra. Ele diminui com √n: amostras maiores dão médias mais estáveis. O z diz quantos erros padrão a média observada está distante do valor de H0.

Por que usar a distribuição normal? O **teorema central do limite** garante que a média de uma amostra grande tem distribuição aproximadamente normal, qualquer que seja a forma dos dados originais. A regra prática é n ≥ 30. Assim, se H0 for verdadeira, o z segue a normal padrão, com média 0 e desvio padrão 1.

Com os pacotes: n = 40, média 498,15 g e desvio padrão 5,13 g. O erro padrão é 5,13 ÷ √40 ≈ 0,81 g, e o z é (498,15 − 500) ÷ 0,81 ≈ −2,28. A média observada está 2,28 erros padrão abaixo de 500.

O **valor p** transforma o z numa probabilidade. **Se H0 for verdadeira, qual é a chance de obter um resultado tão extremo quanto o observado, ou mais?** No teste bilateral, isso é a área nas duas caudas da normal, além de 2,28 e aquém de −2,28: p ≈ 0,023, ou 2,3%. No unilateral, com H1: média < 500 g, seria só a cauda da esquerda, metade disso: p ≈ 0,011.

A decisão compara o valor p com o α:

- **p ≤ α:** rejeita-se H0. Com α = 5%, o resultado é considerado estatisticamente significativo: há evidência de que a média é diferente de 500 g.
- **p > α:** não se rejeita H0. Os dados não trazem evidência suficiente.

Com α = 5%, os pacotes reprovam. Com α = 1%, os mesmos dados não bastam para condenar a máquina. Por isso o α precisa ser fixado antes.

O que o valor p **não** é:

- Não é a probabilidade de H0 ser verdadeira.
- Não é a probabilidade de o resultado ter acontecido "por acaso".
- Não mede o tamanho nem a importância do efeito.

O mesmo raciocínio vale para proporções. Um fornecedor garante no máximo 5% de peças com defeito, e numa amostra de 400 peças, 29 tinham defeito (7,25%). Com H0: p = 0,05 e H1: p > 0,05:

z = (0,0725 − 0,05) ÷ √(0,05 × 0,95 ÷ 400) ≈ 2,06, e o valor p unilateral é ≈ 0,019

Com α = 5%, há evidência de que a taxa de defeitos é maior do que a garantida. A aproximação normal para proporções exige que n × p0 e n × (1 − p0) sejam pelo menos 10.

## Erros tipo I e tipo II, e poder do teste

Todo teste pode errar de dois jeitos:

|                        | H0 é verdadeira         | H0 é falsa              |
| ---------------------- | ----------------------- | ----------------------- |
| **Rejeita H0**         | Erro tipo I (falso positivo) | Acerto              |
| **Não rejeita H0**     | Acerto                  | Erro tipo II (falso negativo) |

- **Erro tipo I:** condenar um inocente. Concluir que a máquina está desregulada quando ela está certa. A probabilidade desse erro é o próprio α.
- **Erro tipo II:** absolver um culpado. Não detectar uma máquina que está de fato desregulada. A probabilidade desse erro se chama β.

O **poder do teste** é 1 − β: a chance de detectar um efeito que existe. O poder aumenta quando:

- a amostra é maior;
- o efeito real é maior (um desvio de 10 g é mais fácil de detectar que um de 1 g);
- os dados variam menos;
- o α é maior, o que também aumenta os falsos positivos.

Existe uma troca: com a amostra fixa, reduzir α aumenta β. A única forma de reduzir os dois é aumentar a amostra. Um valor de referência comum é poder de 80%, e o tamanho da amostra é calculado antes do estudo para chegar a ele. Você verá esse cálculo no tópico de teste A/B.

## Intervalo de confiança e significância prática

O **intervalo de confiança** da média é:

média ± z crítico × erro padrão

O z crítico é 1,96 para 95% de confiança e 2,576 para 99%. Para os pacotes, o intervalo de 95% vai de 496,56 g a 499,74 g. O de 99%, mais largo, vai de 496,06 g a 500,24 g.

Há uma ligação direta com o teste: **um teste bilateral com nível α rejeita H0 exatamente quando o valor de H0 fica fora do intervalo de confiança de (1 − α)**. O 500 está fora do intervalo de 95% (rejeita com α = 5%) e dentro do de 99% (não rejeita com α = 1%).

O intervalo informa mais que o valor p, porque mostra o tamanho provável do efeito. "Os pacotes têm, em média, entre 0,3 g e 3,4 g a menos que o rótulo" ajuda muito mais numa decisão do que "p = 0,023".

Isso leva à diferença entre **significância estatística** e **significância prática**. Com amostras enormes, qualquer diferença minúscula dá valor p pequeno. Um teste com milhões de usuários pode concluir, com p = 0,0001, que um botão aumenta o tempo no app em 0,2 segundo. É um efeito real, e provavelmente irrelevante. A pergunta "esse efeito importa?" é respondida pelo tamanho do efeito e pelo contexto do negócio, e não pelo valor p.

## Testes na prática com Python

O teste z usa o desvio padrão da amostra no lugar do desvio padrão da população, o que só é seguro com amostras grandes. Para amostras pequenas, usa-se o **teste t de Student**, que leva em conta a incerteza extra de estimar o desvio padrão. Com n ≥ 30, os dois dão resultados muito próximos. A biblioteca SciPy (`pip install scipy`) tem os testes prontos:

```python
import pandas as pd
from scipy import stats

pesos = pd.read_csv("data/pacotes.csv")["peso_g"]

# teste t de uma amostra: a média é 500?
resultado = stats.ttest_1samp(pesos, popmean=500)
print(resultado.statistic)   # t ≈ -2,28
print(resultado.pvalue)      # p ≈ 0,028

# teste t unilateral: a média é menor que 500?
stats.ttest_1samp(pesos, popmean=500, alternative="less")

# duas amostras independentes, na versão de Welch,
# que não supõe variâncias iguais:
# stats.ttest_ind(grupo_a, grupo_b, equal_var=False)
```

Com n = 40, o teste t dá p ≈ 0,028, e o teste z que você vai implementar no desafio dá p ≈ 0,023. A conclusão com α = 5% é a mesma.

Um roteiro para qualquer teste:

1. Escreva a pergunta e as hipóteses H0 e H1. Escolha bilateral ou unilateral.
2. Fixe o α antes de ver os dados.
3. Confira as condições: amostra aleatória, observações independentes, tamanho suficiente.
4. Calcule a estatística de teste e o valor p.
5. Reporte o tamanho do efeito, o intervalo de confiança e o valor p, e não só "deu significativo".

Um último cuidado são as **comparações múltiplas**. Com α = 5%, cada teste tem 5% de chance de dar um falso positivo. Se você testa 20 hipóteses em que não há efeito nenhum, espera-se que uma dê "significativa" por puro acaso. Testar muitas coisas e reportar só o que deu certo é o chamado *p-hacking*. Quando for fazer vários testes, defina-os antes e corrija o α. A correção mais simples, a de Bonferroni, divide o α pelo número de testes: com 20 testes, use 0,05 ÷ 20 = 0,0025.

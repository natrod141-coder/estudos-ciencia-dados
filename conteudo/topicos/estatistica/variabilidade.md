---
titulo: "Medidas de variabilidade"
modulo: estatistica
ordem: 2
horas: 3
estado: publicado
resumo: "Amplitude, variância e desvio padrão: o quanto os dados se espalham."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Por que a média não basta"
    tipo: leitura
    minutos: 6
  - id: a2
    titulo: "Amplitude, variância e desvio padrão"
    tipo: leitura
    minutos: 15
  - id: a3
    titulo: "Coeficiente de variação e intervalo interquartil"
    tipo: leitura
    minutos: 10
  - id: a4
    titulo: "Vídeo de apoio sobre medidas de variabilidade"
    tipo: video
    minutos: 15
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Os tempos de espera de uma fila, em minutos, foram 2, 4, 4, 4, 5, 5, 7 e 9. A média é 5 e a soma dos quadrados dos desvios é 32. Tratando esses dados como a população inteira, qual é o desvio padrão?"
    opcoes: ["2", "4", "5", "32"]
    correta: 0
    explicacao: "A variância populacional é a soma dos quadrados dos desvios dividida pela quantidade de valores: 32 ÷ 8 = 4. O desvio padrão é a raiz quadrada da variância: √4 = 2. O 4 é a variância, e não o desvio padrão."
  - pergunta: "Por que a variância amostral divide a soma dos quadrados dos desvios por n − 1, e não por n?"
    opcoes: ["Para o resultado ficar na mesma unidade dos dados", "Porque os desvios são medidos até a média da própria amostra, que fica mais perto dos dados do que a média da população, e dividir por n subestimaria a variabilidade", "Para evitar divisão por zero quando só há um valor", "É só uma convenção, sem efeito no resultado"]
    correta: 1
    explicacao: "A média da amostra é calculada com os mesmos dados, então fica mais perto deles do que a média verdadeira da população. Com isso, os desvios saem um pouco menores do que deveriam. Dividir por n − 1 compensa essa diferença. É a chamada correção de Bessel."
  - pergunta: "Um analista mediu a altura de um grupo de pessoas em centímetros e encontrou variância de 64. Em que unidade está esse número?"
    opcoes: ["Centímetros", "Porcentagem", "Centímetros ao quadrado", "Não tem unidade"]
    correta: 2
    explicacao: "Na variância, os desvios são elevados ao quadrado, e a unidade também: cm². Por isso o desvio padrão costuma ser mais fácil de interpretar. Aqui ele é √64 = 8 cm, na mesma unidade dos dados."
  - pergunta: "Qual medida de variabilidade é a mais afetada por um único valor atípico?"
    opcoes: ["Intervalo interquartil", "Amplitude", "Desvio padrão", "Todas são afetadas da mesma forma"]
    correta: 1
    explicacao: "A amplitude depende só do maior e do menor valor, então um único valor atípico muda o resultado inteiro. O desvio padrão também é afetado, mas usa todos os valores. O intervalo interquartil ignora os 25% mais altos e os 25% mais baixos e quase não se move."
  - pergunta: "A ação X custa em média R$ 10, com desvio padrão de R$ 2. A ação Y custa em média R$ 400, com desvio padrão de R$ 20. Qual oscila mais em relação ao próprio preço?"
    opcoes: ["Y, porque o desvio padrão dela é maior", "X, com coeficiente de variação de 20% contra 5% de Y", "As duas oscilam igual", "Não dá para comparar ações de preços tão diferentes"]
    correta: 1
    explicacao: "O coeficiente de variação divide o desvio padrão pela média: 2 ÷ 10 = 20% para X e 20 ÷ 400 = 5% para Y. Em relação ao próprio preço, X oscila quatro vezes mais. O desvio padrão sozinho engana quando as escalas são diferentes."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Dois centros de distribuição entregam, em média, em 5 dias. Em um deles, o desvio padrão é de 0,8 dia. No outro, é de 3 dias. O prazo prometido ao cliente é de 7 dias. Explique qual centro você escolheria e por quê."
  rubrica:
    - "Diz que a média igual não basta para comparar os centros, porque não mostra o quanto os prazos variam."
    - "Interpreta o desvio padrão como a distância típica entre cada entrega e a média, e conclui que as entregas do centro com desvio de 3 dias são bem mais espalhadas."
    - "Liga a variabilidade ao risco: com mais espalhamento, uma parte maior das entregas passa dos 7 dias, e por isso escolhe o centro com desvio de 0,8 dia."
  modelo: "Escolheria o centro com desvio padrão de 0,8 dia. A média dos dois é a mesma, mas a média não mostra o quanto os prazos variam. O desvio padrão mede a distância típica entre cada entrega e a média. No centro de 0,8 dia, a maioria das entregas fica perto dos 5 dias, longe do limite de 7. No centro de 3 dias, as entregas se espalham muito, e uma parte delas passa do prazo. Para cumprir uma promessa ao cliente, o que conta é a consistência, e não só a média."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Qual centro de distribuição é mais confiável"
  descricao: "Dois centros de distribuição entregam, em média, em 5 dias. Você vai calcular amplitude, variância, desvio padrão, coeficiente de variação e intervalo interquartil sem bibliotecas prontas e usar essas medidas para decidir qual centro cumpre melhor um prazo de 7 dias."
  pasta: "desafios/estatistica/variabilidade"
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
      descricao: "Abra desafios/estatistica/variabilidade/README.md. Os dados estão em data/entregas.csv: uma linha por entrega, com o número do pedido, o centro de distribuição e os dias até a entrega."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "Cada função tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def amplitude(valores):"
        - "def variancia(valores, amostral=True):"
        - "def desvio_padrao(valores, amostral=True):"
        - "def coeficiente_variacao(valores):"
        - "def intervalo_interquartil(valores):"
        - "def comparar_centros(caminho_csv, prazo=7):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/estatistica/variabilidade"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/variabilidade"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de variabilidade"'
        - "git push -u origin desafio/variabilidade"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Variabilidade", en: "variability, dispersion" }
  - { pt: "Amplitude", en: "range" }
  - { pt: "Desvio", en: "deviation" }
  - { pt: "Variância", en: "variance" }
  - { pt: "Desvio padrão", en: "standard deviation (SD)" }
  - { pt: "Coeficiente de variação", en: "coefficient of variation (CV)" }
  - { pt: "Intervalo interquartil", en: "interquartile range (IQR)" }
  - { pt: "Correção de Bessel", en: "Bessel's correction" }
  - { pt: "Graus de liberdade", en: "degrees of freedom (ddof)" }
---

## Por que a média não basta

Dois centros de distribuição entregam, em média, em 5 dias. Estes são os prazos de cinco entregas recentes de cada um:

| Centro    | Dias até a entrega | Média |
| --------- | ------------------ | ----- |
| Guarulhos | 4, 5, 5, 5, 6      | 5     |
| Contagem  | 1, 2, 5, 8, 9      | 5     |

Pela média, os dois são iguais. Para quem espera a encomenda, não são. Em Guarulhos, você sabe o que esperar. Em Contagem, a entrega pode chegar amanhã ou daqui a mais de uma semana.

As **medidas de variabilidade** (ou de dispersão) medem o quanto os dados se espalham em torno do centro. A média diz onde os dados estão. A variabilidade diz o quanto dá para confiar nesse valor típico. Um resumo de dados sem nenhuma medida de variabilidade está incompleto.

## Amplitude, variância e desvio padrão

A **amplitude** é o maior valor menos o menor. Em Guarulhos, 6 − 4 = 2 dias. Em Contagem, 9 − 1 = 8 dias. É fácil de calcular, mas depende só dos dois extremos: um único valor atípico muda o resultado inteiro.

A **variância** usa todos os valores. A ideia é medir a distância de cada valor até a média, o **desvio**, e resumir essas distâncias em um número. Veja o cálculo para os dados 2, 4, 4, 4, 5, 5, 7 e 9, cuja média é 5:

| Valor | Desvio (valor − média) | Desvio ao quadrado |
| ----- | ---------------------- | ------------------ |
| 2     | −3                     | 9                  |
| 4     | −1                     | 1                  |
| 4     | −1                     | 1                  |
| 4     | −1                     | 1                  |
| 5     | 0                      | 0                  |
| 5     | 0                      | 0                  |
| 7     | 2                      | 4                  |
| 9     | 4                      | 16                 |
| Soma  | 0                      | 32                 |

Repare que a soma dos desvios é sempre zero: os negativos cancelam os positivos. Por isso os desvios são elevados ao quadrado. O quadrado tira o sinal e ainda pesa mais os valores distantes da média.

A variância é a média desses quadrados. Aqui entra uma escolha importante:

- **Variância populacional:** quando os dados são a população inteira, divide-se por n. Aqui, 32 ÷ 8 = 4.
- **Variância amostral:** quando os dados são uma amostra, divide-se por n − 1. Aqui, 32 ÷ 7 ≈ 4,57.

Por que n − 1? Os desvios são medidos até a média da própria amostra, que foi calculada com esses mesmos dados e por isso fica mais perto deles do que a média verdadeira da população. Os desvios saem um pouco menores do que deveriam, e dividir por n − 1 compensa isso. Na prática, quase sempre os seus dados são uma amostra, então use n − 1.

O problema da variância é a unidade: se os dados estão em dias, a variância está em dias ao quadrado, o que não tem interpretação direta. O **desvio padrão** resolve isso: é a raiz quadrada da variância e volta para a unidade dos dados. Para os valores acima, o desvio padrão amostral é √4,57 ≈ 2,14.

Leia o desvio padrão como a **distância típica entre um valor e a média**. Em distribuições em forma de sino, cerca de 68% dos valores ficam a até um desvio padrão da média, e cerca de 95% ficam a até dois desvios padrão.

## Coeficiente de variação e intervalo interquartil

O desvio padrão está na escala dos dados, e isso atrapalha comparações. Um desvio de R$ 20 é muito para uma ação de R$ 10 e pouco para uma de R$ 400. O **coeficiente de variação (CV)** divide o desvio padrão pela média e mostra o resultado em porcentagem:

- Ação de R$ 10 com desvio padrão de R$ 2: CV = 2 ÷ 10 = 20%.
- Ação de R$ 400 com desvio padrão de R$ 20: CV = 20 ÷ 400 = 5%.

O CV permite comparar a variabilidade de grupos com escalas ou unidades diferentes. Ele só faz sentido para valores sempre positivos, com um zero verdadeiro, como preço, peso ou tempo. Para temperatura em graus Celsius, por exemplo, a média pode ser zero, e o CV perde o sentido.

O **intervalo interquartil (IQR)** é Q3 − Q1: a largura da faixa que contém os 50% centrais dos dados. Como ignora os 25% mais baixos e os 25% mais altos, quase não se move quando aparece um valor atípico. Ele é para a mediana o que o desvio padrão é para a média: se os dados têm valores atípicos e você resume o centro pela mediana, resuma a variabilidade pelo IQR.

| Medida                  | O que mede                         | Unidade           | Sofre com valores atípicos? |
| ----------------------- | ---------------------------------- | ----------------- | --------------------------- |
| Amplitude               | Distância entre os extremos        | A dos dados       | Muito                       |
| Variância               | Média dos quadrados dos desvios    | A dos dados ao quadrado | Sim                   |
| Desvio padrão           | Distância típica até a média       | A dos dados       | Sim                         |
| Coeficiente de variação | Desvio padrão em relação à média   | Porcentagem       | Sim                         |
| Intervalo interquartil  | Largura dos 50% centrais           | A dos dados       | Não                         |

No pandas, cada medida é uma linha:

```python
import pandas as pd

entregas = pd.read_csv("data/entregas.csv")
dias = entregas["dias"]

# amplitude
dias.max() - dias.min()

# variância e desvio padrão amostrais (dividem por n - 1)
dias.var()
dias.std()

# coeficiente de variação, em %
dias.std() / dias.mean() * 100

# intervalo interquartil
dias.quantile(0.75) - dias.quantile(0.25)
```

Dois cuidados com as bibliotecas. Primeiro, o pandas divide por n − 1 por padrão, mas o NumPy (`np.std`, `np.var`) divide por n. Para o NumPy usar n − 1, passe `ddof=1`. Segundo, existem vários métodos para calcular quartis. O `quantile` do pandas interpola entre os valores e pode dar um resultado um pouco diferente do método das metades que você vai usar no desafio. Os dois estão corretos, e a diferença diminui quanto mais dados houver.

**Qual medida usar:**

- Para descrever dados sem valores atípicos: média e desvio padrão.
- Para dados assimétricos ou com valores atípicos: mediana e intervalo interquartil.
- Para comparar grupos em escalas diferentes: coeficiente de variação.
- A amplitude serve para uma primeira olhada, mas não deve ser a única medida.

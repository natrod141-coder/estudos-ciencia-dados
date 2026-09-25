---
titulo: "Tipos de variáveis"
modulo: estatistica
ordem: 4
horas: 2
estado: publicado
resumo: "Variáveis quantitativas e qualitativas, e o que se pode calcular com cada uma."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Qualitativas e quantitativas"
    tipo: leitura
    minutos: 6
  - id: a2
    titulo: "Nominal, ordinal, discreta e contínua"
    tipo: leitura
    minutos: 10
  - id: a3
    titulo: "Tipos de variáveis no pandas"
    tipo: leitura
    minutos: 10
  - id: a4
    titulo: "Vídeo de apoio sobre tipos de variáveis"
    tipo: video
    minutos: 10
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Qual destas variáveis é qualitativa ordinal?"
    opcoes: ["CEP", "Número de filhos", "Nível de satisfação: baixo, médio ou alto", "Peso em quilos"]
    correta: 2
    explicacao: "O nível de satisfação é uma categoria, e as categorias têm uma ordem natural: baixo, médio e alto. O CEP é qualitativo nominal, porque identifica um lugar sem ordem de grandeza. Número de filhos é quantitativa discreta, e peso é quantitativa contínua."
  - pergunta: "O número de reclamações recebidas por dia em um SAC é uma variável:"
    opcoes: ["Quantitativa contínua", "Quantitativa discreta", "Qualitativa ordinal", "Qualitativa nominal"]
    correta: 1
    explicacao: "É uma contagem: 0, 1, 2, 3 reclamações. Não existe 2,7 reclamações. Variáveis que vêm de contagens são quantitativas discretas. As contínuas vêm de medições, como tempo, peso ou distância."
  - pergunta: "Uma base de clientes tem a coluna CEP, com valores como 01310100. Por que calcular a média dessa coluna não faz sentido?"
    opcoes: ["Porque os números do CEP são grandes demais", "Porque o CEP tem zeros à esquerda", "Faz sentido, desde que se use a mediana em vez da média", "Porque o CEP é um código que identifica um lugar, e os dígitos não medem nenhuma quantidade"]
    correta: 3
    explicacao: "O CEP é escrito com dígitos, mas é um rótulo, como um nome. A média de dois CEPs não corresponde a nenhum lugar entre eles. O mesmo vale para CPF, telefone e número de pedido: são variáveis qualitativas nominais."
  - pergunta: "Uma pesquisa pergunta a renda em faixas: até R$ 2 mil, de R$ 2 mil a R$ 5 mil e acima de R$ 5 mil. Como fica classificada essa variável?"
    opcoes: ["Qualitativa ordinal, porque as faixas têm ordem, mas não são valores exatos", "Quantitativa contínua, porque renda é dinheiro", "Qualitativa nominal, porque as faixas são textos", "Quantitativa discreta, porque há só três opções"]
    correta: 0
    explicacao: "O tipo depende de como a variável foi medida. A renda exata em reais seria quantitativa contínua. Agrupada em faixas, vira qualitativa ordinal: dá para ordenar as faixas, mas não calcular a média das respostas."
  - pergunta: "Uma escala de satisfação vai de 1 (muito insatisfeito) a 5 (muito satisfeito). Qual é o problema de calcular a média dessas notas?"
    opcoes: ["Nenhum, porque as notas são números", "A média de números inteiros não pode ter casas decimais", "A média supõe que a distância entre 1 e 2 é igual à distância entre 4 e 5, e numa escala ordinal isso não é garantido", "A média só funciona com mais de 100 respostas"]
    correta: 2
    explicacao: "Os números de 1 a 5 só representam a ordem das respostas. Nada garante que o salto de 'insatisfeito' para 'neutro' vale o mesmo que o de 'satisfeito' para 'muito satisfeito'. Muitas empresas calculam essa média mesmo assim, como aproximação, mas a mediana e a porcentagem de cada resposta são mais seguras."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Uma planilha de vendas tem as colunas: número do pedido, cidade, tamanho da camiseta (P, M, G ou GG), quantidade de itens e valor pago. Classifique cada coluna e explique como essa classificação muda o que você pode calcular com ela."
  rubrica:
    - "Classifica corretamente: número do pedido e cidade como qualitativas nominais, tamanho como qualitativa ordinal, quantidade de itens como quantitativa discreta e valor pago como quantitativa contínua."
    - "Explica que o número do pedido, apesar de ter dígitos, é um identificador, e que fazer contas com ele não tem significado."
    - "Liga os tipos às medidas possíveis: moda para as nominais, moda e mediana para as ordinais, e média e mediana para as quantitativas."
  modelo: "Número do pedido e cidade são qualitativas nominais. O número do pedido tem dígitos, mas é só um identificador: a média dos números de pedido não significa nada. Tamanho da camiseta é qualitativa ordinal, porque P, M, G e GG têm uma ordem, mas a distância entre eles não é uma medida. Quantidade de itens é quantitativa discreta, porque vem de uma contagem. Valor pago é quantitativa contínua, porque é uma medida em reais. Para as nominais, só a moda faz sentido, por exemplo a cidade com mais pedidos. Para o tamanho, dá para usar moda e mediana. Para quantidade de itens e valor pago, dá para calcular média, mediana e medidas de variabilidade."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Cada coluna no seu tipo"
  descricao: "Uma rede de lojas quer um resumo de uma pesquisa com clientes, mas metade das colunas não aceita média. Você vai classificar cada variável, ler o CSV sem perder o zero à esquerda do CEP, criar categorias ordenadas no pandas e calcular só as medidas que fazem sentido para cada tipo."
  pasta: "desafios/estatistica/tipos_variaveis"
  testes: 8
  tempo: "1 h"
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
      descricao: "Abra desafios/estatistica/tipos_variaveis/README.md. Os dados estão em data/pesquisa.csv: uma linha por cliente, com cidade, CEP, escolaridade, satisfação, número de dependentes, compras no ano e renda mensal."
    - titulo: "Classifique as colunas e implemente as funções em solucao.py"
      descricao: "Troque cada None do dicionário CLASSIFICACAO pelo tipo da coluna. Depois implemente as funções: cada uma tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - "CLASSIFICACAO = {...}"
        - "def medidas_permitidas(tipo):"
        - "def ler_pesquisa(caminho_csv):"
        - "def mediana_ordinal(serie):"
        - "def resumo_central(pesquisa):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/estatistica/tipos_variaveis"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/tipos_variaveis"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de tipos de variáveis"'
        - "git push -u origin desafio/tipos_variaveis"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Variável", en: "variable" }
  - { pt: "Qualitativa (categórica)", en: "qualitative (categorical)" }
  - { pt: "Quantitativa (numérica)", en: "quantitative (numerical)" }
  - { pt: "Nominal", en: "nominal" }
  - { pt: "Ordinal", en: "ordinal" }
  - { pt: "Discreta", en: "discrete" }
  - { pt: "Contínua", en: "continuous" }
  - { pt: "Escala Likert", en: "Likert scale" }
  - { pt: "Identificador", en: "identifier (ID)" }
  - { pt: "Tipo de dado", en: "data type (dtype)" }
---

## Qualitativas e quantitativas

Uma **variável** é uma característica que muda de um elemento para outro: cada cliente tem uma cidade, uma idade e um gasto mensal. Antes de calcular qualquer coisa, é preciso saber de que tipo é cada variável, porque o tipo define quais contas fazem sentido.

A primeira divisão é entre dois grandes grupos:

- **Qualitativas** (ou categóricas): os valores são categorias, como cidade, meio de pagamento ou nível de escolaridade.
- **Quantitativas** (ou numéricas): os valores são números que medem ou contam alguma coisa, como idade, número de itens ou valor da compra.

Cuidado com números que não são quantidades. CEP, CPF, telefone e número do pedido são escritos com dígitos, mas são rótulos que identificam algo. Um teste simples: **faz sentido somar ou tirar a média?** A média de dois CEPs não é um lugar entre eles, e somar números de pedido não resulta em nada. Se a resposta for não, a variável é qualitativa, mesmo que o valor seja feito só de dígitos.

## Nominal, ordinal, discreta e contínua

Cada grupo se divide em dois tipos:

| Tipo     | Grupo        | O que é                         | Exemplos                                   | O que dá para fazer             |
| -------- | ------------ | ------------------------------- | ------------------------------------------ | ------------------------------- |
| Nominal  | Qualitativa  | Categorias sem ordem            | Cidade, cor, meio de pagamento, CEP        | Contar e comparar igualdade     |
| Ordinal  | Qualitativa  | Categorias com ordem natural    | Escolaridade, tamanho P/M/G, satisfação    | Contar e ordenar                |
| Discreta | Quantitativa | Contagens, valores separados    | Número de filhos, itens no carrinho        | Contar, ordenar e fazer contas  |
| Contínua | Quantitativa | Medições, qualquer valor numa faixa | Peso, tempo de entrega, renda, temperatura | Contar, ordenar e fazer contas |

Numa variável **ordinal**, dá para dizer que "superior" vem depois de "médio", mas não quanto depois. A distância entre as categorias não é uma medida. Numa **discreta**, os valores vêm de contagens: 0, 1, 2 filhos, nunca 1,5. Numa **contínua**, os valores vêm de medições e podem ter tantas casas decimais quanto o instrumento permitir. Dinheiro, na prática, é tratado como contínuo, mesmo sendo contado em centavos.

O tipo depende de **como a variável foi medida**, e não do assunto. A renda em reais é contínua. A mesma renda perguntada em faixas ("até R$ 2 mil", "de R$ 2 mil a R$ 5 mil") vira ordinal. A idade em anos é quantitativa, e a faixa etária é ordinal. Quando você agrupa uma variável quantitativa em faixas, perde informação e perde operações: não dá mais para calcular a média.

O tipo define as medidas de tendência central possíveis:

- **Nominal:** só a moda.
- **Ordinal:** moda e mediana. A mediana precisa só de ordem.
- **Discreta:** moda, mediana e média.
- **Contínua:** mediana e média. A moda existe, mas os valores quase nunca se repetem, então a moda dos valores brutos não diz nada. Nesse caso, olha-se a faixa mais frequente de um histograma.

Um caso que gera discussão é a **escala Likert**, como a satisfação de 1 a 5. Ela é ordinal, então a rigor não admite média. Na prática, muitas empresas calculam a média mesmo assim, como aproximação. Se fizer isso, saiba que está supondo distâncias iguais entre as respostas. Quase sempre é mais claro reportar a porcentagem de cada resposta ou a porcentagem de satisfeitos.

## Tipos de variáveis no pandas

O pandas tem os seus próprios tipos de dado, os **dtypes**, e eles não correspondem sozinhos aos tipos estatísticos. Ao ler um CSV, o pandas adivinha o dtype pelo conteúdo: qualquer coluna só com dígitos vira número, inclusive o CEP. Quem decide o tipo estatístico é você.

| Tipo estatístico | dtype recomendado no pandas              | Cuidado                                                                |
| ---------------- | ---------------------------------------- | ---------------------------------------------------------------------- |
| Nominal          | `str` (ou `object`) ou `category`        | Códigos com dígitos (CEP, CPF, id) precisam ser lidos como texto       |
| Ordinal          | `category` com `ordered=True`            | Sem a ordem definida, o pandas ordena as categorias em ordem alfabética |
| Discreta         | `int64`                                  | Com algum valor faltante, a coluna vira `float64`. Use `Int64` para manter inteiros |
| Contínua         | `float64`                                | Nenhum em especial                                                     |

Na prática:

```python
import pandas as pd

# dtype impede que o CEP "01310100" vire o número 1310100
pesquisa = pd.read_csv("data/pesquisa.csv",
                       dtype={"cep": str})
print(pesquisa.dtypes)

# categoria ordenada: "neutro" vem antes de "satisfeito"
ordem = ["muito insatisfeito", "insatisfeito", "neutro",
         "satisfeito", "muito satisfeito"]
satisfacao = pd.Categorical(pesquisa["satisfacao"],
                            categories=ordem, ordered=True)
pesquisa["satisfacao"] = satisfacao

# contagem na ordem da escala
pesquisa["satisfacao"].value_counts(sort=False)

# proporção de satisfeitos ou mais
(pesquisa["satisfacao"] >= "satisfeito").mean()

# códigos de 0 a 4, na ordem da escala
pesquisa["satisfacao"].cat.codes
```

Sem a categoria ordenada, a coluna é só texto. A comparação `>= "satisfeito"` passa a seguir a ordem alfabética e devolve um resultado errado sem nenhum aviso, e ordenar a coluna coloca "insatisfeito" antes de "muito insatisfeito". O tipo `category` também economiza memória em colunas com poucos valores diferentes e muitas linhas, como UF ou meio de pagamento.

Um bom hábito, antes de qualquer análise: rode `df.dtypes` e `df.head()` e pergunte, para cada coluna, se o tipo que o pandas escolheu é o tipo que a variável realmente tem.

---
titulo: "Excel"
modulo: manipulacao
ordem: 1
horas: 8
estado: publicado
resumo: "Tabelas dinâmicas, fórmulas e limpeza de dados."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Tabelas, tipos de dado e referências"
    tipo: leitura
    minutos: 12
  - id: a2
    titulo: "Fórmulas essenciais: SE, SOMASES, CONT.SES e PROCX"
    tipo: leitura
    minutos: 20
  - id: a3
    titulo: "Limpeza de dados no Excel"
    tipo: leitura
    minutos: 15
  - id: a4
    titulo: "Tabela dinâmica"
    tipo: leitura
    minutos: 15
  - id: a5
    titulo: "Do Excel para o Python"
    tipo: leitura
    minutos: 10
  - id: a6
    titulo: "Vídeo de apoio: tabela dinâmica do zero"
    tipo: video
    minutos: 20
    link: ""
  - id: a7
    titulo: "Vídeo de apoio: PROCX e SOMASES na prática"
    tipo: video
    minutos: 15
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "A célula C2 tem a fórmula =A2*$B$1. Ao copiar a fórmula para C3, como ela fica?"
    opcoes: ["=A3*$B$1", "=A3*$B$2", "=A2*$B$1", "=A3*B2"]
    correta: 0
    explicacao: "A referência A2 é relativa e acompanha a cópia: uma linha abaixo, vira A3. A referência $B$1 é absoluta, porque o cifrão trava a coluna e a linha, então continua $B$1. É assim que se usa uma célula fixa, como uma taxa, em todas as linhas."
  - pergunta: "Qual fórmula soma o valor das vendas da vendedora Ana na região Sul?"
    opcoes: ["=SOMA(Valor; \"Ana\"; \"Sul\")", "=SOMASE(Vendedor; \"Ana\"; Valor)", "=SOMASES(Valor; Vendedor; \"Ana\"; Região; \"Sul\")", "=CONT.SES(Vendedor; \"Ana\"; Região; \"Sul\")"]
    correta: 2
    explicacao: "O SOMASES soma com vários critérios. O primeiro argumento é o intervalo a somar, seguido de pares de intervalo e critério. O SOMASE aceita um critério só, e o CONT.SES conta as linhas em vez de somar os valores."
  - pergunta: "Por que o PROCX costuma ser preferido ao PROCV?"
    opcoes: ["Porque é mais curto de digitar", "Porque procura em qualquer direção, não quebra quando uma coluna é inserida, usa correspondência exata por padrão e tem um argumento para o caso de não encontrar", "Porque funciona em qualquer versão antiga do Excel", "Porque soma os valores encontrados"]
    correta: 1
    explicacao: "O PROCV só procura na primeira coluna e devolve colunas à direita, depende do número da coluna, que muda quando alguém insere uma coluna, e usa correspondência aproximada se o último argumento for omitido. Esse último ponto causa resultados errados sem nenhum aviso. O PROCX resolve os três problemas. O único porém é que ele não existe em versões antigas do Excel."
  - pergunta: "Uma coluna de valores está alinhada à esquerda, e a SOMA dela dá zero. Qual é a causa mais provável?"
    opcoes: ["A coluna está oculta", "A função SOMA só funciona dentro de Tabelas", "Os valores são negativos e se cancelam", "Os números estão armazenados como texto"]
    correta: 3
    explicacao: "O Excel alinha números à direita e texto à esquerda. Números guardados como texto, comuns em exportações de sistemas, são ignorados pela SOMA. O Excel costuma marcar essas células com um triângulo verde, que oferece a opção 'Converter em número'. A função VALOR também resolve."
  - pergunta: "A célula A2 contém o nome Ana Souza com dois espaços antes, três espaços entre o nome e o sobrenome e um espaço depois. O que =ARRUMAR(A2) devolve?"
    opcoes: ["AnaSouza, sem nenhum espaço", "ANA SOUZA, em maiúsculas", "Ana Souza, sem espaços nas pontas e com um espaço só entre as palavras", "O mesmo texto, porque o ARRUMAR só tira os espaços do fim"]
    correta: 2
    explicacao: "O ARRUMAR tira os espaços do começo e do fim e reduz os espaços repetidos entre as palavras a um só. Ele não muda maiúsculas e minúsculas: para isso existem MAIÚSCULA, MINÚSCULA e PRI.MAIÚSCULA."
  - pergunta: "Numa tabela dinâmica, você quer ver o faturamento de cada vendedor nas linhas e de cada mês nas colunas. Onde vai o campo Valor?"
    opcoes: ["Em Filtros", "Em Linhas", "Em Colunas", "Em Valores, resumido por Soma"]
    correta: 3
    explicacao: "Linhas e Colunas definem os grupos, e Valores define o que é calculado para cada grupo. Vendedor vai em Linhas, a data agrupada por mês vai em Colunas, e Valor vai em Valores com o resumo Soma."
  - pergunta: "Você acrescentou 200 linhas novas na base de uma tabela dinâmica. O que é preciso fazer para ela mostrar os dados novos?"
    opcoes: ["Nada, ela se atualiza sozinha", "Atualizar a tabela dinâmica e, se a base não for uma Tabela (Ctrl+T), ajustar também o intervalo de origem", "Criar uma nova tabela dinâmica", "Salvar e reabrir o arquivo"]
    correta: 1
    explicacao: "A tabela dinâmica guarda um resumo e só recalcula quando é atualizada. Se a base for um intervalo comum, como A1:E500, as linhas novas ficam de fora até o intervalo ser ajustado. Com a base formatada como Tabela, o intervalo cresce sozinho, e basta atualizar."
  - pergunta: "Qual é o limite de linhas de uma planilha nas versões atuais do Excel?"
    opcoes: ["65.536", "1.048.576", "10 milhões", "Não há limite"]
    correta: 1
    explicacao: "Desde o Excel 2007, cada planilha tem no máximo 1.048.576 linhas e 16.384 colunas. Muito antes disso, a planilha já fica lenta. Bases maiores pedem banco de dados, Power Query ou Python."
  - pergunta: "Uma célula que deveria mostrar uma data mostra o número 45658. O que aconteceu?"
    opcoes: ["A célula está com formato de número: o Excel guarda datas como a quantidade de dias desde 1900, e 45658 é 01/01/2025", "A data foi corrompida e precisa ser digitada de novo", "O Excel não reconheceu o ano", "A célula tem uma fórmula errada"]
    correta: 0
    explicacao: "Para o Excel, uma data é um número: os dias contados a partir de 1900. Por isso dá para subtrair datas e somar dias a elas. Basta mudar o formato da célula para Data. No Python, células com formato de data já chegam como data, e um número como 45658 vira data com pd.to_datetime(45658, unit='D', origin='1899-12-30')."
  - pergunta: "Qual é a principal vantagem de fazer a limpeza de uma planilha mensal em Python, e não à mão no Excel?"
    opcoes: ["O Python deixa os gráficos mais bonitos", "O Excel não consegue remover duplicatas", "O processo fica registrado e repetível: roda igual todo mês, sem erro manual, e com qualquer quantidade de linhas", "O Python não precisa de dados limpos"]
    correta: 2
    explicacao: "Cada passo feito à mão pode ser esquecido ou feito diferente no mês seguinte, e não deixa registro. Em código, os passos ficam escritos, podem ser revisados e rodam iguais toda vez. O Power Query, dentro do próprio Excel, oferece uma vantagem parecida."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Todo mês, um colega monta o mesmo relatório no Excel: copia a exportação do sistema, apaga as linhas de título, corrige os nomes à mão, usa PROCV para trazer a categoria dos produtos e monta a tabela dinâmica. Explique os riscos desse processo e o que você mudaria."
  rubrica:
    - "Aponta os riscos do trabalho manual repetido: esquecer um passo, arrastar a fórmula até a linha errada, apagar dados sem querer e não deixar registro do que foi feito."
    - "Aponta os riscos do PROCV: correspondência aproximada quando o último argumento é omitido, e códigos não encontrados que viram #N/D e podem sumir dos totais."
    - "Propõe tornar o processo repetível: base como Tabela e PROCX com valor para não encontrado, ou levar a limpeza para o Power Query ou para Python, de modo que o relatório seja refeito igual a cada mês."
  modelo: "O processo depende de alguém repetir os mesmos passos à mão todo mês, e cada passo é uma chance de erro: apagar uma linha a mais, esquecer de corrigir um nome, arrastar a fórmula até a linha errada. Não fica registro do que foi feito, então um erro pode passar despercebido. O PROCV tem riscos próprios: se o último argumento for omitido, ele faz correspondência aproximada e pode trazer a categoria errada sem avisar, e códigos que não estão no cadastro viram #N/D, que podem ser filtrados ou ignorados e sumir do total. Eu formataria a base como Tabela, trocaria o PROCV pelo PROCX com um valor para não encontrado, como 'Sem cadastro', e levaria a limpeza para o Power Query ou para um script em Python. Assim, o relatório é refeito do mesmo jeito todo mês, com um clique ou um comando."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Da planilha bagunçada ao relatório"
  descricao: "Uma filial manda todo mês uma planilha exportada do sistema, com título em cima do cabeçalho, valores guardados como texto, nomes escritos de jeitos diferentes, linhas repetidas e códigos sem cadastro. Você vai refazer em Python o que faria no Excel, de ARRUMAR a PROCX, SOMASES e tabela dinâmica, e gerar o relatório em .xlsx."
  pasta: "desafios/manipulacao/excel"
  testes: 10
  tempo: "2 h"
  ferramentas: "VS Code, Python 3.11 ou superior, pandas, openpyxl, pytest e Excel ou LibreOffice para conferir"
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
      descricao: "Abra o terminal do VS Code com Ctrl+` (acento grave). Depois use Ctrl+Shift+P, Python: Select Interpreter, e escolha o .venv. Se o ambiente já existia, rode de novo o pip install: este desafio usa o openpyxl."
      comandos:
        - "# Linux ou macOS"
        - "python3 -m venv .venv"
        - "source .venv/bin/activate"
        - "# Windows (PowerShell)"
        - "python -m venv .venv"
        - '.venv\Scripts\Activate.ps1'
        - "pip install -r desafios/requirements.txt"
    - titulo: "Leia o enunciado e abra a planilha"
      descricao: "Abra desafios/manipulacao/excel/README.md. Depois abra data/vendas_filial.xlsx no Excel ou no LibreOffice e procure os problemas antes de programar: o enunciado lista o que procurar."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "Cada função tem uma docstring com o que recebe, o que devolve e o equivalente no Excel. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def ler_vendas(caminho_xlsx):"
        - "def texto_para_numero(valor):"
        - "def limpar_vendas(vendas):"
        - "def procx(vendas, produtos):"
        - "def somases(vendas, vendedor, mes):"
        - "def tabela_dinamica(vendas):"
        - "def exportar_relatorio(caminho_entrada, caminho_saida):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/manipulacao/excel"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/excel"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de Excel"'
        - "git push -u origin desafio/excel"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Tabela (Ctrl+T)", en: "table" }
  - { pt: "Referência absoluta ($A$1)", en: "absolute reference" }
  - { pt: "SE / SES", en: "IF / IFS" }
  - { pt: "SOMASES", en: "SUMIFS" }
  - { pt: "CONT.SES", en: "COUNTIFS" }
  - { pt: "MÉDIASES", en: "AVERAGEIFS" }
  - { pt: "PROCV", en: "VLOOKUP" }
  - { pt: "PROCX", en: "XLOOKUP" }
  - { pt: "SEERRO", en: "IFERROR" }
  - { pt: "ARRUMAR", en: "TRIM" }
  - { pt: "PRI.MAIÚSCULA", en: "PROPER" }
  - { pt: "SUBSTITUIR", en: "SUBSTITUTE" }
  - { pt: "VALOR", en: "VALUE" }
  - { pt: "Tabela dinâmica", en: "pivot table" }
  - { pt: "Texto para colunas", en: "text to columns" }
---

## Tabelas, tipos de dado e referências

Antes de qualquer fórmula, a base de dados precisa estar num formato que o Excel e qualquer outra ferramenta consigam usar:

- uma linha por registro, como uma venda ou um cliente;
- uma coluna por informação, com o cabeçalho numa única linha;
- nenhuma célula mesclada, linha de total ou linha em branco no meio dos dados;
- cada coluna com um só tipo de dado.

Com a base assim, selecione uma célula dela e use **Ctrl+T** para formatá-la como **Tabela** (em inglês, *table*). Dê um nome à tabela, como Vendas, em Design da Tabela. Isso traz três vantagens: a tabela cresce sozinha quando você acrescenta linhas, as fórmulas copiam para a coluna inteira, e as fórmulas passam a usar nomes, como `=SOMA(Vendas[Valor])` e `=[@Quantidade]*[@Preço]`, que são muito mais fáceis de ler que `=SOMA(E2:E5000)`.

**Tipos de dado.** Cada célula guarda um número, um texto, uma data ou um valor lógico (VERDADEIRO ou FALSO). Dois detalhes causam muitos erros:

- **Números guardados como texto.** Aparecem alinhados à esquerda, às vezes com um triângulo verde no canto, e são ignorados por SOMA e MÉDIA. São comuns em exportações de sistemas, como "R$ 1.234,50".
- **Datas são números.** O Excel conta os dias desde 1900: 01/01/2025 é o número 45658 com formato de data. Por isso dá para subtrair datas e somar dias. Uma data que aparece como número só está com o formato errado. Uma data que aparece alinhada à esquerda é texto, e não funciona em filtros de período.

**Referências.** Ao copiar uma fórmula, as referências mudam junto:

| Referência | Ao copiar para baixo | Ao copiar para a direita | Uso típico                   |
| ---------- | -------------------- | ------------------------ | ---------------------------- |
| `A2`       | vira `A3`            | vira `B2`                | O valor da própria linha     |
| `$A$2`     | continua `$A$2`      | continua `$A$2`          | Uma célula fixa, como a taxa de câmbio |
| `$A2`      | vira `$A3`           | continua `$A2`           | Coluna fixa, linha variável  |
| `A$2`      | continua `A$2`       | vira `B$2`               | Linha fixa, coluna variável  |

A tecla **F4** alterna entre os quatro tipos enquanto você edita a fórmula.

## Fórmulas essenciais: SE, SOMASES, CONT.SES e PROCX

No Excel em português, os argumentos são separados por ponto e vírgula, e as funções têm nomes em português. O glossário do tópico traz os nomes em inglês, que aparecem em tutoriais e na documentação.

**SE e SES.** `=SE(teste; valor_se_verdadeiro; valor_se_falso)` escolhe entre dois resultados. Para mais de duas faixas, o SES evita SEs aninhados:

```
=SE([@Valor]>=1000; "Grande"; "Pequeno")
=SES([@Valor]>=5000; "A"; [@Valor]>=1000; "B"; VERDADEIRO; "C")
```

Para combinar condições, use `E(...)` e `OU(...)` dentro do teste.

**SOMASES, CONT.SES e MÉDIASES.** Somam, contam ou tiram a média das linhas que atendem a um ou mais critérios. No SOMASES, o primeiro argumento é o intervalo a somar, e depois vêm pares de intervalo e critério:

```
=SOMASES(Vendas[Valor]; Vendas[Vendedor]; "Ana Souza"; Vendas[Região]; "Sul")
=CONT.SES(Vendas[Região]; "Sul"; Vendas[Valor]; ">1000")
=MÉDIASES(Vendas[Valor]; Vendas[Data]; ">="&DATA(2026;3;1))
```

Critérios com operadores vão entre aspas, e para juntar um operador com uma célula ou função usa-se o `&`.

**PROCX.** Busca um valor numa coluna e devolve o valor correspondente de outra:

```
=PROCX([@Código]; Produtos[Código]; Produtos[Categoria]; "Sem cadastro")
```

Os argumentos são: o que procurar, onde procurar, o que devolver e, opcionalmente, o que mostrar se não encontrar. Por padrão, a correspondência é exata.

O **PROCV** é a versão antiga, e ainda aparece em muitas planilhas: `=PROCV(A2; Produtos!A:D; 3; FALSO)`. Ele tem três armadilhas:

1. Se o último argumento for omitido, a correspondência é **aproximada**. Com códigos fora de ordem, ele devolve o valor errado sem avisar. Use sempre FALSO.
2. O número da coluna é fixo: se alguém inserir uma coluna na tabela de produtos, o 3 passa a apontar para outra informação.
3. Ele só procura na primeira coluna e só devolve colunas à direita dela.

Quando o valor não é encontrado, PROCV e PROCX sem o quarto argumento devolvem `#N/D`. O `SEERRO(fórmula; valor)` troca qualquer erro por outro valor. Use com cuidado: ele esconde também os erros que você gostaria de ver.

## Limpeza de dados no Excel

Dados de sistemas raramente chegam prontos. As ferramentas mais usadas:

| Problema                            | Ferramenta                                                   |
| ----------------------------------- | ------------------------------------------------------------ |
| Espaços sobrando                    | `=ARRUMAR(A2)`: tira espaços das pontas e repetidos no meio  |
| Maiúsculas e minúsculas misturadas  | `MAIÚSCULA`, `MINÚSCULA` e `PRI.MAIÚSCULA`                   |
| Trocar um trecho de texto           | `=SUBSTITUIR(A2; "R$ "; "")` ou Localizar e Substituir       |
| Número guardado como texto          | `=VALOR(...)`, ou o triângulo verde > Converter em número    |
| Várias informações numa coluna      | Dados > Texto para Colunas, ou `ESQUERDA`, `DIREITA` e `EXT.TEXTO` |
| Linhas repetidas                    | Dados > Remover Duplicatas                                   |
| Células vazias                      | Filtro na coluna, opção (Vazias)                             |

Um exemplo que junta várias funções, convertendo "R$ 1.234,50" em número:

```
=VALOR(SUBSTITUIR(SUBSTITUIR(A2; "R$ "; ""); "."; ""))
```

A fórmula de dentro tira o "R$ ", a do meio tira o ponto dos milhares, e o VALOR converte "1234,50" em número. Ela funciona num Excel configurado em português, em que a vírgula é o separador decimal. Num Excel em inglês, seria preciso também trocar a vírgula por ponto. Essa diferença de configuração regional aparece de novo ao abrir arquivos CSV: um CSV brasileiro costuma usar ponto e vírgula entre as colunas e vírgula nos decimais, e um CSV americano usa vírgula entre as colunas e ponto nos decimais.

Faça a limpeza em colunas novas, mantendo a coluna original, e só apague a original depois de conferir o resultado. Para limpezas que se repetem todo mês, o **Power Query** (Dados > Obter Dados) grava cada passo e refaz tudo com um clique em Atualizar.

## Tabela dinâmica

A **tabela dinâmica** resume milhares de linhas em poucos cliques, sem fórmulas. Com a base selecionada, use Inserir > Tabela Dinâmica e arraste os campos para as quatro áreas:

- **Linhas:** os grupos que aparecem de cima para baixo, como Vendedor.
- **Colunas:** os grupos que aparecem da esquerda para a direita, como Categoria ou Mês.
- **Valores:** o que é calculado para cada combinação, como a Soma de Valor.
- **Filtros:** um recorte aplicado à tabela inteira, como a Região.

O resultado é uma grade, com totais nas bordas:

| Vendedor     | Informática | Móveis  | Papelaria | Total geral |
| ------------ | ----------- | ------- | --------- | ----------- |
| Ana Souza    | 46.822      | 12.509  | 196       | 59.527      |
| Bruno Lima   | 25.060      | 15.539  | 923       | 41.522      |
| Total geral  | 71.882      | 28.048  | 1.119     | 101.049     |

Recursos que valem a pena conhecer:

- **Resumir valores por:** trocar Soma por Contagem, Média, Máximo.
- **Mostrar valores como:** % do total geral, % da linha, diferença em relação ao mês anterior.
- **Agrupar datas:** clique com o botão direito numa data em Linhas ou Colunas e agrupe por mês, trimestre ou ano.
- **Segmentação de dados:** botões para filtrar a tabela, bons para painéis.
- **Atualizar:** a tabela dinâmica não recalcula sozinha. Depois de mudar a base, use Dados > Atualizar Tudo. Com a base formatada como Tabela, as linhas novas entram automaticamente.

## Do Excel para o Python

O Excel é ótimo para explorar, conferir e apresentar. Ele começa a atrapalhar quando:

- a base passa de algumas centenas de milhares de linhas, porque o limite é 1.048.576 linhas e a planilha fica lenta muito antes disso;
- o mesmo trabalho manual se repete toda semana ou todo mês;
- outra pessoa precisa revisar ou refazer o que foi feito.

O pandas lê e grava arquivos `.xlsx` com a biblioteca openpyxl, e cada operação do Excel tem um equivalente:

| No Excel                              | No pandas                                              |
| ------------------------------------- | ------------------------------------------------------ |
| Abrir a aba Vendas, pular o título    | `pd.read_excel(arquivo, sheet_name="Vendas", skiprows=3)` |
| `ARRUMAR` e `PRI.MAIÚSCULA`           | `.str.split().str.join(" ").str.title()`               |
| Remover Duplicatas                    | `.drop_duplicates()`                                   |
| Filtro                                | `vendas[vendas["Região"] == "Sul"]`                    |
| `PROCX`                               | `vendas.merge(produtos, on="Código", how="left")`      |
| `SOMASES`                             | `vendas.loc[filtro, "Valor"].sum()`                    |
| Tabela dinâmica                       | `pd.pivot_table(vendas, index=..., columns=..., values=..., aggfunc="sum")` |
| Salvar como `.xlsx`                   | `tabela.to_excel("relatorio.xlsx")`                    |

O caminho mais comum na prática é combinar os dois: o Python prepara e resume os dados de forma repetível, e o Excel, ou o Power BI, fica com a conferência e a apresentação. No desafio, você vai fazer exatamente isso.

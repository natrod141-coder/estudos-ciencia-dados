---
titulo: "Visualização em Python"
modulo: visualizacao
ordem: 4
horas: 3
estado: publicado
resumo: "Gráficos com matplotlib, seaborn e plotly."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Anatomia de uma figura no matplotlib"
    tipo: leitura
    minutos: 12
  - id: a2
    titulo: "Seaborn: gráficos estatísticos com pouco código"
    tipo: leitura
    minutos: 10
  - id: a3
    titulo: "Plotly: gráficos interativos"
    tipo: leitura
    minutos: 10
  - id: a4
    titulo: "Qual biblioteca usar"
    tipo: leitura
    minutos: 5
  - id: a5
    titulo: "Vídeo de apoio: matplotlib, seaborn e plotly lado a lado"
    tipo: video
    minutos: 20
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "No matplotlib, qual é a diferença entre Figure e Axes?"
    opcoes: ["Figure é a imagem inteira, que pode conter vários gráficos; cada Axes é um gráfico, com seus eixos, título e dados", "São sinônimos", "Axes é a imagem inteira, e Figure é cada gráfico", "Figure guarda os dados, e Axes guarda as cores"]
    correta: 0
    explicacao: "O plt.subplots devolve os dois: fig, ax = plt.subplots(). A figura é a tela onde tudo é desenhado e o que é salvo com savefig. Cada Axes é uma área de gráfico, e é nele que se chamam plot, bar, set_title e set_xlabel."
  - pergunta: "Num painel de pequenos múltiplos, por que usar a mesma escala no eixo y em todos os gráficos?"
    opcoes: ["Porque o matplotlib exige", "Para o painel ocupar menos espaço", "Para a altura das linhas ser comparável entre os gráficos: com escalas diferentes, uma loja pequena parece tão grande quanto uma grande", "Para as cores ficarem iguais"]
    correta: 2
    explicacao: "Cada gráfico, sozinho, ajusta a escala aos próprios dados. Uma loja que vende R$ 5 mil por mês e outra que vende R$ 50 mil ficariam com linhas do mesmo tamanho. Com sharey=True, a comparação entre os gráficos passa a ser justa."
  - pergunta: "Em que formato o seaborn espera os dados, num gráfico como sns.boxplot(data=vendas, x='categoria', y='valor')?"
    opcoes: ["Formato largo, com uma coluna para cada categoria", "Formato longo (tidy): uma linha por observação e uma coluna para cada variável", "Uma lista de listas", "Um dicionário com as médias de cada categoria"]
    correta: 1
    explicacao: "O seaborn trabalha com dados longos: cada linha é uma venda, e as colunas dizem a categoria, o valor, a UF. Os argumentos x, y, hue e col apontam para essas colunas, e o seaborn agrupa sozinho. Dados largos costumam precisar de um melt antes."
  - pergunta: "Qual é a principal vantagem do plotly em relação ao matplotlib?"
    opcoes: ["É o único que faz gráficos de barras", "Gera imagens com melhor resolução para impressão", "Não precisa de dados", "Gráficos interativos, com zoom, valores ao passar o mouse e filtro pela legenda, que podem ser salvos em HTML"]
    correta: 3
    explicacao: "O plotly desenha no navegador. Quem recebe o HTML explora o gráfico sem ter Python instalado. Para imagens estáticas em relatórios e artigos, o matplotlib dá mais controle sobre cada detalhe."
  - pergunta: "Um gráfico do matplotlib saiu com o título cortado e a imagem borrada no relatório. O que ajuda?"
    opcoes: ["Salvar com fig.savefig('grafico.png', dpi=200, bbox_inches='tight')", "Usar plt.show() antes de salvar", "Trocar para gráfico de pizza", "Diminuir o tamanho da fonte para 4"]
    correta: 0
    explicacao: "O dpi define a resolução da imagem, e 150 a 200 costuma bastar para relatórios. O bbox_inches='tight' ajusta a área salva ao que foi desenhado, sem cortar títulos e rótulos. O fig.tight_layout() também evita sobreposição entre gráficos da mesma figura."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Você precisa mostrar a evolução mensal do faturamento de 12 lojas. Compare duas opções: um gráfico de linhas com as 12 lojas juntas ou um painel de pequenos múltiplos. Qual você escolheria, por quê, e que cuidados tomaria?"
  rubrica:
    - "Explica que 12 linhas no mesmo gráfico viram um emaranhado, com cores difíceis de distinguir e uma legenda longa que obriga o leitor a ir e voltar."
    - "Justifica os pequenos múltiplos: cada loja num gráfico pequeno, lado a lado, o que facilita ver o padrão de cada uma e comparar entre elas."
    - "Cita cuidados: a mesma escala no eixo y para comparar níveis, o nome da loja como título de cada gráfico, uma ordem que faça sentido (por faturamento ou região) e, se útil, a média de todas em cinza como referência."
  modelo: "Escolheria os pequenos múltiplos. Com 12 linhas no mesmo gráfico, elas se cruzam o tempo todo, as cores ficam parecidas e o leitor precisa consultar a legenda a cada linha: na prática, ninguém consegue acompanhar uma loja. Nos pequenos múltiplos, cada loja tem o seu gráfico, pequeno, e todos ficam lado a lado numa grade. Dá para ver o padrão de cada loja de relance e comparar o formato das curvas. Os cuidados: usar a mesma escala no eixo y em todos os gráficos, senão uma loja pequena parece tão grande quanto uma grande; pôr o nome da loja como título de cada gráfico; ordenar a grade de um jeito que ajude, como do maior para o menor faturamento ou agrupando por região; e, se fizer sentido, desenhar em cinza, em cada gráfico, a média de todas as lojas, como referência para ver quem está acima ou abaixo."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Três bibliotecas, três gráficos"
  descricao: "Com as vendas de 18 meses de uma rede de lojas, você vai fazer pequenos múltiplos com matplotlib, um mapa de calor com seaborn e um gráfico de barras empilhadas interativo com plotly, exportado em HTML para quem não tem Python."
  pasta: "desafios/visualizacao/visualizacao_python"
  testes: 7
  tempo: "1 h 30 min"
  ferramentas: "VS Code, Python 3.11 ou superior, pandas, matplotlib, seaborn, plotly e pytest"
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
      descricao: "Abra o terminal do VS Code com Ctrl+` (acento grave). Depois use Ctrl+Shift+P, Python: Select Interpreter, e escolha o .venv. Se o ambiente já existia, rode de novo o pip install: este desafio usa o seaborn e o plotly."
      comandos:
        - "# Linux ou macOS"
        - "python3 -m venv .venv"
        - "source .venv/bin/activate"
        - "# Windows (PowerShell)"
        - "python -m venv .venv"
        - '.venv\Scripts\Activate.ps1'
        - "pip install -r desafios/requirements.txt"
    - titulo: "Leia o enunciado e conheça os dados"
      descricao: "Abra desafios/visualizacao/visualizacao_python/README.md. Os dados estão em data/vendas.csv: uma linha por item vendido, com data, UF, categoria, quantidade e valor."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "Cada função de gráfico usa uma biblioteca diferente, e a docstring diz qual. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def faturamento_mensal_por_uf(vendas):"
        - "def pequenos_multiplos(vendas):"
        - "def mapa_de_calor(vendas):"
        - "def grafico_interativo(vendas):"
        - "def salvar_html(fig, caminho):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/visualizacao/visualizacao_python"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/visualizacao_python"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de visualização em Python"'
        - "git push -u origin desafio/visualizacao_python"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Figura", en: "figure" }
  - { pt: "Área do gráfico", en: "axes" }
  - { pt: "Pequenos múltiplos", en: "small multiples" }
  - { pt: "Eixo compartilhado", en: "shared axis (sharex, sharey)" }
  - { pt: "Mapa de calor", en: "heatmap" }
  - { pt: "Barra de cores", en: "colorbar" }
  - { pt: "Dados longos", en: "long (tidy) data" }
  - { pt: "Facetas", en: "facets" }
  - { pt: "Anotação", en: "annotation" }
  - { pt: "Resolução", en: "dpi (dots per inch)" }
---

## Anatomia de uma figura no matplotlib

O matplotlib é a base da visualização em Python: o seaborn e os gráficos do pandas desenham por meio dele. Uma imagem do matplotlib tem duas camadas:

- a **figura** (`Figure`), que é a tela inteira, o que é salvo em arquivo;
- uma ou mais **áreas de gráfico** (`Axes`), cada uma com seus eixos, título, rótulos e dados.

A forma recomendada de trabalhar é criar os dois de uma vez e chamar os métodos do `ax`:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(meses, faturamento, color="#0f4c4a", marker="o")
ax.set_title("Faturamento mensal")
ax.set_xlabel("Mês")
ax.set_ylabel("Faturamento (R$)")
# tira as bordas de cima e da direita
ax.spines[["top", "right"]].set_visible(False)
fig.savefig("faturamento.png", dpi=200, bbox_inches="tight")
```

Você vai encontrar muito código com `plt.plot(...)` e `plt.title(...)` direto, sem `ax`. Funciona para um gráfico só, mas atrapalha quando há vários. Prefira sempre o `fig, ax`.

**Vários gráficos na mesma figura.** `plt.subplots(2, 2)` cria uma grade de 2 x 2 áreas, devolvidas num array:

```python
fig, eixos = plt.subplots(2, 2, figsize=(10, 6), sharex=True, sharey=True)
for ax, uf in zip(eixos.flat, ["MG", "PR", "RS", "SP"]):
    ax.plot(mensal.index, mensal[uf])
    ax.set_title(uf)
fig.suptitle("Faturamento mensal por UF")
fig.tight_layout()
```

Isso se chama **pequenos múltiplos**: o mesmo gráfico repetido para cada grupo. É a melhor alternativa a um gráfico com muitas linhas emboladas. O `sharey=True` é essencial: dá a todos os gráficos a mesma escala no eixo y, e só assim a comparação entre eles é justa.

Outros ajustes frequentes:

| Para                                 | Use                                                    |
| ------------------------------------ | ------------------------------------------------------ |
| Destacar um ponto com texto e seta   | `ax.annotate("Black Friday", xy=(x, y), xytext=(x2, y2), arrowprops={"arrowstyle": "->"})` |
| Formatar o eixo como moeda, com ponto nos milhares | `ax.yaxis.set_major_formatter(lambda x, _: f"R$ {x:,.0f}".replace(",", "."))` |
| Girar os rótulos do eixo x           | `ax.tick_params(axis="x", labelrotation=45)`           |
| Uma linha de referência              | `ax.axhline(meta, color="gray", linestyle="--")`       |
| Evitar sobreposição                  | `fig.tight_layout()`                                   |

## Seaborn: gráficos estatísticos com pouco código

O **seaborn** é construído sobre o matplotlib e é especializado em gráficos estatísticos. Ele trabalha com **dados longos** (*tidy*): uma linha por observação e uma coluna por variável. Você diz quais colunas vão em cada papel, e ele agrupa, calcula e desenha:

```python
import seaborn as sns

fig, ax = plt.subplots()

# distribuição por grupo
sns.boxplot(data=vendas, x="categoria", y="valor", ax=ax)

# histogramas sobrepostos, um por UF
sns.histplot(data=vendas, x="valor", hue="uf", ax=ax)

# mapa de calor
tabela = vendas.pivot_table(index="categoria", columns="mes",
                            values="valor", aggfunc="sum")
sns.heatmap(tabela, cmap="Greens", ax=ax)
```

- `hue` separa os dados por cor, conforme uma coluna.
- As funções de figura, como `sns.relplot` e `sns.catplot`, aceitam `col` e `row` e fazem pequenos múltiplos sozinhas: `sns.relplot(data=vendas, x="data", y="valor", col="uf", kind="line")`.
- Como tudo é matplotlib por baixo, os ajustes finos (título, rótulos, `savefig`) continuam iguais.

O **mapa de calor** é uma tabela em que a cor substitui o número. Ele é ótimo para achar padrões em duas dimensões, como categoria e mês, e ruim para ler valores exatos. Use uma escala de uma cor só, do claro ao escuro, e diga a unidade na barra de cores.

## Plotly: gráficos interativos

O **plotly** desenha gráficos no navegador. O leitor pode passar o mouse para ver os valores, dar zoom e esconder séries clicando na legenda. O módulo `plotly.express` faz a maioria dos gráficos numa linha, também com dados longos:

```python
import plotly.express as px

fig = px.bar(
    resumo, x="uf", y="valor", color="categoria",
    barmode="stack", title="Faturamento por UF e categoria",
    labels={"uf": "UF", "valor": "Faturamento (R$)"},
)
fig.write_html("faturamento.html", include_plotlyjs="cdn")
```

O arquivo HTML abre em qualquer navegador, e quem recebe não precisa ter Python. Com `include_plotlyjs="cdn"`, o arquivo fica com alguns KB, e a biblioteca é carregada da internet ao abrir. Sem essa opção, a biblioteca inteira, com alguns MB, vai dentro do arquivo, que funciona mesmo sem internet.

O plotly também é a base de ferramentas para construir painéis em Python, como o Dash. O Streamlit, outra opção muito usada, aceita gráficos de todas essas bibliotecas.

## Qual biblioteca usar

| Situação                                               | Biblioteca                        |
| ------------------------------------------------------ | --------------------------------- |
| Imagem para relatório, artigo ou apresentação, com controle de cada detalhe | matplotlib |
| Explorar distribuições e relações, com pouco código    | seaborn                           |
| Gráfico para o leitor explorar, ou para um painel web  | plotly                            |
| Uma olhada rápida nos dados, durante a análise         | `df.plot()` do pandas             |

As regras de bom gráfico dos tópicos de tipos de gráficos e de storytelling valem para todas: comece pela pergunta, escolha o gráfico certo para ela, dê título e rótulos com unidade, e use a cor para destacar, e não para decorar.

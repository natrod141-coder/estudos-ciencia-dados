# Tópicos ainda em rascunho

Dos 35 tópicos que começaram em rascunho, 18 já foram escritos (toda a Fase 1: estatística,
manipulação de dados e visualização de dados, marcados com [x] abaixo). Os 17 restantes têm só o
cabeçalho (título, módulo, horas). Falta escrever o texto de leitura, as aulas, o quiz, a pergunta
aberta e o desafio. Use `conteudo/topicos/estatistica/tendencia_central.md` como modelo do formato
completo.

Todo tópico tem desafio prático em Python com testes, mesmo os de ferramentas que não são Python:
o desafio de Excel lê e gera planilhas, o de BigQuery usa o DuckDB, o de Git roda os comandos em
repositórios temporários, o de Power BI refaz as etapas do Power Query em pandas, e o de DAX
implementa o contexto de filtro e as medidas em Python.

Um tópico em rascunho já aparece no mapa da trilha e aceita registro de horas, mas nunca
chega a "dominado" porque não tem como cumprir os critérios.

## Como tirar um tópico do rascunho

1. Abra o arquivo em `conteudo/topicos/<modulo>/<id>.md`.
2. Preencha `aulas`, `quiz`, `aberta` e `desafio` conforme o formato do tópico piloto.
3. Escreva o texto de leitura no corpo do arquivo, depois do cabeçalho.
4. Mude `estado: rascunho` para `estado: publicado`.
5. Se o tópico tiver desafio, crie a pasta em `desafios/<modulo>/<id>/` (veja `desafios/README.md`)
   e rode `python scripts/verificar_desafios.py` para confirmar que o arquivo inicial falha
   nos testes e o gabarito passa.

## Lista

### Estatística descritiva
- [x] variabilidade — Medidas de variabilidade
- [x] amostragem — Amostragem
- [x] tipos_variaveis — Tipos de variáveis
- [x] tipos_graficos — Tipos de gráficos
- [x] tabelas_frequencia — Tabelas de frequência
- [x] teste_hipoteses — Teste de hipóteses
- [x] teste_ab — Teste A/B (vem depois de teste de hipóteses, porque usa valor p e significância)

### Manipulação de dados
- [x] excel — Excel
- [x] python_pandas — Python e pandas, com NumPy e dados faltantes (16 h)
- [x] sql_basico — SQL básico
- [x] sql_avancado — SQL avançado
- [x] bigquery — BigQuery
- [x] git_github — Git e GitHub

### Visualização de dados
- [x] power_bi — Power BI
- [x] modelagem_dados — Modelagem de dados (vem antes de DAX, porque o DAX depende do modelo)
- [x] dax_basico — DAX básico
- [x] visualizacao_python — Visualização em Python
- [x] storytelling — Storytelling com dados

### Machine learning clássico
- [ ] regressao_linear — Regressão linear
- [ ] regressao_logistica — Regressão logística
- [ ] arvores_decisao — Árvores de decisão
- [ ] random_forest — Random Forest
- [ ] gradient_boosting — Gradient Boosting
- [ ] validacao_cruzada — Validação cruzada
- [ ] metricas — Métricas de classificação (considere incluir feature engineering em um tópico próprio deste módulo)

### IA aplicada
- [ ] apis_llm — APIs de LLM
- [ ] prompting — Prompting e saídas estruturadas
- [ ] embeddings — Embeddings e bancos vetoriais
- [ ] rag — RAG
- [ ] fastapi — FastAPI
- [ ] docker — Docker

### Aprofundamento
- [ ] clusterizacao_pca — Clusterização e PCA
- [ ] series_temporais — Séries temporais
- [ ] deep_learning — Deep Learning
- [ ] cloud — Cloud

## Pendências de conteúdo, além dos tópicos acima

- NumPy e tratamento de dados faltantes: incorporados ao tópico `python_pandas`, que passou de
  12 h para 16 h (2 h para cada assunto). O desafio do tópico tem uma parte de NumPy e uma de
  dados faltantes.
- Feature engineering não tem tópico próprio. Sugestão: incorporar a `metricas` ou criar um
  tópico novo no módulo `ml_classico`, antes de `validacao_cruzada`.

Falta decidir só o feature engineering. Se decidir incorporar a um tópico existente, ajuste
o campo `horas` do arquivo para refletir o tempo extra.

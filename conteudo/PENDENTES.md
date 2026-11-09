# Tópicos ainda em rascunho

A trilha tem 42 tópicos. 22 já foram escritos (estatística, manipulação de dados, visualização
de dados e fundamentos de IA generativa, marcados com [x] abaixo). Os 20 restantes têm só o
cabeçalho (título, módulo, horas).
Falta escrever o texto de leitura, as aulas, o quiz, a pergunta aberta e o desafio. Use
`conteudo/topicos/estatistica/tendencia_central.md` como modelo do formato completo.

Todo tópico tem desafio prático em Python com testes, mesmo os de ferramentas que não são Python:
o desafio de Excel lê e gera planilhas, o de BigQuery usa o DuckDB, o de Git roda os comandos em
repositórios temporários, o de Power BI refaz as etapas do Power Query em pandas, e o de DAX
implementa o contexto de filtro e as medidas em Python. Os tópicos novos seguem a mesma ideia: o
de dbt pode usar o dbt com DuckDB, e os de IA podem testar a lógica com respostas de modelo
gravadas em arquivo, para que os testes rodem sem chave de API e sem custo.

Um tópico em rascunho já aparece no mapa da trilha e aceita registro de horas, mas nunca
chega a "dominado" porque não tem como cumprir os critérios.

## Prioridade de escrita

A ordem abaixo segue o calendário: escreva primeiro o que será estudado primeiro.

1. Fundamentos de IA generativa (Fase 1, estudado em paralelo com estatística e manipulação): escrito
2. Analytics engineering e APIs de LLM (Fase 2)
3. Machine learning clássico e Busca, RAG e avaliação (Fase 3)
4. IA sobre dados e Colocar em produção (Fase 4)

## Como tirar um tópico do rascunho

1. Abra o arquivo em `conteudo/topicos/<modulo>/<id>.md`.
2. Preencha `aulas`, `quiz`, `aberta` e `desafio` conforme o formato do tópico piloto.
3. Escreva o texto de leitura no corpo do arquivo, depois do cabeçalho.
4. Mude `estado: rascunho` para `estado: publicado`.
5. Se o tópico tiver desafio, crie a pasta em `desafios/<modulo>/<id>/` (veja `desafios/README.md`)
   e rode `python scripts/verificar_desafios.py` para confirmar que o arquivo inicial falha
   nos testes e o gabarito passa.

## Lista

### Fase 1, trilha de dados: Estatística descritiva
- [x] tendencia_central: Medidas de tendência central
- [x] variabilidade: Medidas de variabilidade
- [x] amostragem: Amostragem
- [x] tipos_variaveis: Tipos de variáveis
- [x] tipos_graficos: Tipos de gráficos
- [x] tabelas_frequencia: Tabelas de frequência
- [x] teste_hipoteses: Teste de hipóteses
- [x] teste_ab: Teste A/B (vem depois de teste de hipóteses, porque usa valor p e significância)

### Fase 1, trilha de dados: Manipulação de dados
- [x] excel: Excel
- [x] python_pandas: Python e pandas, com NumPy e dados faltantes (16 h)
- [x] sql_basico: SQL básico
- [x] sql_avancado: SQL avançado
- [x] bigquery: BigQuery
- [x] git_github: Git e GitHub

### Fase 1, trilha de IA: Fundamentos de IA generativa
- [x] como_llms_funcionam: Como um LLM funciona
- [x] limites_alucinacao: Limites e alucinação
- [x] conferir_codigo_gerado: Conferir código gerado por IA

### Fase 2, trilha de dados: Visualização de dados
- [x] power_bi: Power BI
- [x] modelagem_dados: Modelagem de dados (vem antes de DAX, porque o DAX depende do modelo)
- [x] dax_basico: DAX básico
- [x] visualizacao_python: Visualização em Python
- [x] storytelling: Storytelling com dados

### Fase 2, trilha de dados: Analytics engineering
- [ ] dbt: dbt (depende de modelagem de dados e SQL avançado)
- [ ] qualidade_dados: Testes de qualidade de dados
- [ ] camada_semantica: Métricas e camada semântica

### Fase 2, trilha de IA: APIs de LLM
- [ ] apis_llm: APIs de LLM
- [ ] prompting: Prompting e saídas estruturadas

### Fase 3, trilha de dados: Machine learning clássico
- [ ] regressao_linear: Regressão linear
- [ ] regressao_logistica: Regressão logística
- [ ] arvores_decisao: Árvores de decisão
- [ ] random_forest: Random Forest
- [ ] gradient_boosting: Gradient Boosting
- [ ] validacao_cruzada: Validação cruzada
- [ ] metricas: Métricas de classificação (considere incluir feature engineering em um tópico próprio deste módulo)

### Fase 3, trilha de IA: Busca, RAG e avaliação
- [ ] embeddings: Embeddings e bancos vetoriais
- [ ] rag: RAG
- [ ] avaliacao_llm: Avaliação de sistemas com LLM

### Fase 4, trilha de dados: Colocar em produção
- [ ] fastapi: FastAPI
- [ ] docker: Docker
- [ ] deploy_nuvem: Publicar na nuvem

### Fase 4, trilha de IA: IA sobre dados
- [ ] text_to_sql: Text-to-SQL (usa o modelo da Fase 2 e a avaliação da Fase 3)
- [ ] agentes_mcp: Agentes, ferramentas e MCP

## Pendências de conteúdo, além dos tópicos acima

- Feature engineering não tem tópico próprio. Sugestão: incorporar a `metricas` ou criar um
  tópico novo no módulo `ml_classico`, antes de `validacao_cruzada`. Se decidir incorporar a um
  tópico existente, ajuste o campo `horas` do arquivo para refletir o tempo extra.
- Clusterização e PCA, séries temporais e deep learning saíram da trilha na reestruturação de
  novembro de 2026, por pesarem pouco para vagas júnior de dados. Se quiser de volta, recrie com
  `npm run novo -- ml_classico "Clusterização e PCA" --horas 15`.

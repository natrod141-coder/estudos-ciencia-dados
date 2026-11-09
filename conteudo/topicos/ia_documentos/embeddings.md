---
titulo: "Embeddings e bancos vetoriais"
modulo: ia_documentos
ordem: 1
horas: 10
estado: publicado
resumo: "Representar textos como vetores e buscar por significado."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Buscar por palavras e buscar por significado"
    tipo: leitura
    minutos: 10
  - id: a2
    titulo: "O que é um embedding"
    tipo: leitura
    minutos: 12
  - id: a3
    titulo: "Medir a proximidade: a similaridade de cosseno"
    tipo: leitura
    minutos: 10
  - id: a4
    titulo: "Gerar embeddings de verdade"
    tipo: leitura
    minutos: 15
  - id: a5
    titulo: "Bancos vetoriais"
    tipo: leitura
    minutos: 12
  - id: a6
    titulo: "Busca híbrida e reordenação"
    tipo: leitura
    minutos: 12
  - id: a7
    titulo: "Medir a qualidade da busca"
    tipo: leitura
    minutos: 10
  - id: a8
    titulo: "Vídeo de apoio: embeddings e busca semântica"
    tipo: video
    minutos: 25
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "O que é um embedding de um texto?"
    opcoes: ["Um resumo do texto escrito pelo modelo", "Uma lista de números que representa o significado do texto, de modo que textos parecidos ficam com vetores próximos", "A contagem de palavras do texto", "O texto traduzido para o inglês"]
    correta: 1
    explicacao: "Um modelo de embeddings transforma o texto num vetor, em geral com mais de mil números. Textos com significado parecido, mesmo com palavras diferentes, ganham vetores que apontam em direções parecidas."
  - pergunta: "Por que a busca por significado encontra o artigo 'Como pedir reembolso' para a consulta 'quero meu dinheiro de volta', e a busca por palavras não?"
    opcoes: ["Porque a busca por significado procura mais palavras", "Porque o artigo tem a palavra dinheiro", "Porque a busca por palavras ignora textos curtos", "Porque as duas frases não têm palavras em comum, mas têm significado parecido, e os vetores delas ficam próximos"]
    correta: 3
    explicacao: "A busca por palavras só encontra o que tem palavras em comum com a consulta. Os embeddings captam o significado: dinheiro de volta, estorno e reembolso falam do mesmo assunto."
  - pergunta: "Se os vetores já estão normalizados, com comprimento 1, a similaridade de cosseno entre dois deles é igual a:"
    opcoes: ["O produto escalar dos dois", "A soma dos dois", "A distância entre eles", "O maior valor de cada um"]
    correta: 0
    explicacao: "O cosseno é o produto escalar dividido pelo produto dos comprimentos. Com comprimento 1, a divisão some, e o produto escalar, mais rápido de calcular, dá o mesmo resultado. Os embeddings da Voyage AI, por exemplo, já vêm normalizados."
  - pergunta: "Em que tipo de consulta a busca por palavras costuma ganhar da busca por significado?"
    opcoes: ["Em perguntas escritas com sinônimos", "Em perguntas longas e vagas", "Em consultas com códigos, números de pedido, nomes próprios ou termos raros, como 'erro E-403'", "Em perguntas em outro idioma"]
    correta: 2
    explicacao: "O vetor capta o assunto, aplicativo com erro, mas não a sequência exata E-403. A busca por palavras acha o código na hora. Por isso as duas abordagens se complementam."
  - pergunta: "Para que serve o parâmetro input_type, com os valores query e document, na API de embeddings da Voyage AI?"
    opcoes: ["Para escolher o idioma", "Para dizer se o texto é uma consulta ou um documento a ser encontrado, o que melhora a qualidade da busca", "Para definir o número de dimensões", "Para escolher entre texto e imagem"]
    correta: 1
    explicacao: "Consultas e documentos têm formas diferentes: uma pergunta curta e um parágrafo explicativo. Indicando o tipo, o modelo gera vetores mais adequados para a busca. Os artigos são indexados como document; a pergunta do cliente, como query."
  - pergunta: "A empresa decidiu trocar de modelo de embeddings. O que é preciso fazer com os vetores já guardados?"
    opcoes: ["Nada, os vetores de qualquer modelo são compatíveis", "Só normalizar de novo", "Só gerar os vetores das consultas novas com o modelo novo", "Gerar de novo os vetores de todos os documentos com o modelo novo: vetores de modelos diferentes não são comparáveis"]
    correta: 3
    explicacao: "Cada modelo organiza o espaço de vetores do seu jeito. Comparar a consulta de um modelo com documentos de outro dá resultados sem sentido. Por isso, guarde junto com cada vetor o nome do modelo que o gerou."
  - pergunta: "Qual é o papel de um banco vetorial?"
    opcoes: ["Guardar vetores com metadados e encontrar rapidamente os mais próximos de um vetor de consulta, com filtros, mesmo com milhões de itens", "Gerar os embeddings dos textos", "Substituir o modelo de linguagem", "Corrigir os erros de digitação das consultas"]
    correta: 0
    explicacao: "Com poucos milhares de vetores, comparar a consulta com todos, como no desafio, é rápido. Com milhões, os bancos vetoriais usam índices aproximados, como o HNSW, que encontram os vizinhos mais próximos sem comparar com todos."
  - pergunta: "Como a fusão por posição recíproca (RRF) junta o resultado da busca por palavras com o da busca por significado?"
    opcoes: ["Somando as notas de similaridade das duas buscas", "Usando só a busca que tiver a maior nota", "Dando a cada documento, em cada ranking, um valor que diminui com a posição, e somando os valores dos dois rankings", "Sorteando qual busca usar em cada consulta"]
    correta: 2
    explicacao: "As notas das duas buscas estão em escalas diferentes e não podem ser somadas direto. A RRF usa só as posições: quem aparece bem colocado nas duas sobe. No desafio, a busca híbrida acertou o primeiro resultado de todas as 10 consultas."
  - pergunta: "Numa avaliação, o acerto nos 3 primeiros resultados da busca foi de 0,9. O que isso quer dizer?"
    opcoes: ["Que 90% dos resultados são relevantes", "Que, em 90% das consultas, o documento certo apareceu entre os 3 primeiros resultados", "Que a busca leva 0,9 segundo para 3 resultados", "Que 3 em cada 10 consultas falham"]
    correta: 1
    explicacao: "O acerto em k, ou recall em k, mede se o que importa aparece entre os k primeiros. Numa aplicação de RAG, em que os k primeiros trechos vão para o modelo, é a medida mais direta da qualidade da busca."
  - pergunta: "O que faz um modelo de reordenação (reranker)?"
    opcoes: ["Gera embeddings menores", "Corrige a ortografia da consulta", "Ordena os documentos pela data", "Recebe a consulta e os primeiros candidatos da busca e os reordena com um modelo mais preciso, que lê a consulta e cada documento juntos"]
    correta: 3
    explicacao: "A busca vetorial é rápida porque compara vetores calculados separadamente. O reranker é mais lento e mais preciso, por isso entra só no fim: a busca traz, por exemplo, 50 candidatos, e ele escolhe os 5 melhores."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "A busca da central de ajuda da sua empresa só encontra artigos com as mesmas palavras da consulta. Proponha uma busca melhor: como funcionaria, que componentes teria e como você mostraria que ela é de fato melhor que a atual."
  rubrica:
    - "Propõe embeddings para os artigos e para as consultas, com o mesmo modelo, e explica que a busca por significado resolve sinônimos e frases diferentes."
    - "Mantém a busca por palavras numa busca híbrida, para códigos, nomes e termos exatos, e combina os dois resultados, por exemplo com RRF, possivelmente com filtros por metadados ou um reranker."
    - "Define uma avaliação: um conjunto de consultas reais com o artigo certo de cada uma, medindo o acerto nos k primeiros resultados da busca atual e da nova."
  modelo: "Eu geraria um embedding para cada artigo, com um modelo como o voyage-4, indicando que são documentos, e guardaria os vetores num banco vetorial junto com o título, a categoria e o nome do modelo. A cada busca, a consulta do cliente também viraria um vetor, com o mesmo modelo, indicando que é uma consulta, e o banco traria os artigos mais próximos pela similaridade de cosseno. Isso resolve o problema principal: 'quero meu dinheiro de volta' encontra 'Como pedir reembolso'. Mas eu não jogaria fora a busca por palavras, porque ela é melhor para códigos de erro, números de pedido e nomes de produto, que o vetor capta mal. As duas buscas rodariam juntas, e os resultados seriam combinados pela posição, com a fusão RRF. Se ainda houver erros, um reranker reordena os 20 primeiros candidatos. Para mostrar que é melhor, eu montaria um conjunto de umas 100 consultas reais, tiradas do histórico do site, com o artigo certo de cada uma marcado por alguém do atendimento. Mediria, para a busca atual e para a nova, em quantas consultas o artigo certo aparece em primeiro e entre os três primeiros. A busca nova só entra no ar se ganhar nessas medidas, e o conjunto de consultas fica guardado para avaliar qualquer mudança futura."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Busca por significado na central de ajuda"
  descricao: "Com 16 artigos de uma central de ajuda e 10 buscas reais de clientes, você vai comparar a busca por palavras com a busca por significado, com vetores, ver em que cada uma erra, juntar as duas numa busca híbrida que acerta todas as consultas, medir os acertos e montar um pequeno banco vetorial com filtro por categoria."
  pasta: "desafios/ia_documentos/embeddings"
  testes: 11
  tempo: "2 h"
  ferramentas: "VS Code, Python 3.11 ou superior, numpy, scikit-learn e pytest"
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
      descricao: "Abra desafios/ia_documentos/embeddings/README.md. Os artigos e as consultas estão em data."
    - titulo: "Implemente as funções e a classe em solucao.py"
      descricao: "A função carregar já está pronta. Cada função tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def normalizar(vetor):"
        - "def similaridade_cosseno(a, b):"
        - "def buscar(consulta, matriz, k=3):"
        - "def buscar_por_palavras(consulta, textos, k=3):"
        - "def acertos_em_k(rankings, relevantes, k):"
        - "def fusao_rrf(rankings, k_rrf=60):"
        - "class IndiceVetorial:"
    - titulo: "Rode os testes a cada parte pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/ia_documentos/embeddings"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/embeddings"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de embeddings"'
        - "git push -u origin desafio/embeddings"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Vetor de representação", en: "embedding" }
  - { pt: "Busca semântica", en: "semantic search" }
  - { pt: "Busca por palavras", en: "lexical search, keyword search" }
  - { pt: "Similaridade de cosseno", en: "cosine similarity" }
  - { pt: "Produto escalar", en: "dot product" }
  - { pt: "Normalização", en: "normalization" }
  - { pt: "Vizinhos mais próximos", en: "nearest neighbors" }
  - { pt: "Busca aproximada", en: "approximate nearest neighbor (ANN)" }
  - { pt: "Banco vetorial", en: "vector database" }
  - { pt: "Busca híbrida", en: "hybrid search" }
  - { pt: "Fusão por posição recíproca", en: "reciprocal rank fusion (RRF)" }
  - { pt: "Reordenação", en: "reranking" }
  - { pt: "Acerto nos k primeiros", en: "recall at k" }
---

## Buscar por palavras e buscar por significado

A busca da maioria dos sites procura pelas **palavras** digitadas. Ela funciona bem quando a pessoa usa os mesmos termos dos documentos, e mal quando não usa. No desafio deste tópico, a central de ajuda de uma loja tem o artigo "Como pedir reembolso". Um cliente digita "quero meu dinheiro de volta". As duas frases não têm uma única palavra em comum, e a busca por palavras não devolve nada.

As técnicas clássicas de busca por palavras, como o TF-IDF e o BM25, dão mais peso às palavras raras e à frequência delas em cada documento. São rápidas, previsíveis e excelentes para termos exatos. Mas não sabem que "dinheiro de volta", "estorno" e "reembolso" falam da mesma coisa.

A **busca por significado**, ou busca semântica, resolve esse problema com **embeddings**. É também a primeira peça do RAG, o assunto do próximo tópico: para responder com base nos seus documentos, o sistema precisa primeiro encontrar os trechos certos.

## O que é um embedding

Um **embedding** é uma lista de números, um vetor, que representa o significado de um texto. Um **modelo de embeddings** recebe o texto e devolve o vetor, e foi treinado para que textos com significado parecido ganhem vetores que apontam em direções parecidas.

Para dar para entender, o desafio usa vetores de brinquedo, com 8 dimensões, uma para cada assunto da central de ajuda:

```text
dimensão       "Como pedir reembolso"   "quero meu dinheiro de volta"
pagamento      0,35                     0,40
entrega        0,06                     0,04
assinatura     0,02                     0,02
conta          0,05                     0,00
devolução      0,90                     0,80
aplicativo     0,02                     0,04
nota fiscal    0,03                     0,05
promoção       0,02                     0,06
```

Os dois vetores são quase iguais, apesar de as frases não terem palavras em comum. Os vetores de um modelo de verdade funcionam do mesmo jeito, com duas diferenças: têm de centenas a milhares de dimensões, e nenhuma delas tem um significado que dê para nomear. O que importa é a posição de um vetor em relação aos outros.

## Medir a proximidade: a similaridade de cosseno

Para saber se dois vetores apontam para o mesmo lado, usa-se a **similaridade de cosseno**: o produto escalar dos dois, dividido pelo produto dos comprimentos. Ela vai de -1, direções opostas, a 1, mesma direção, e não depende do tamanho dos vetores, só da direção.

```python
import numpy as np

def similaridade_cosseno(a, b):
    a, b = np.asarray(a), np.asarray(b)
    return a @ b / (np.linalg.norm(a) * np.linalg.norm(b))
```

Se os vetores estiverem **normalizados**, com comprimento 1, a divisão some, e o cosseno é só o produto escalar. Isso permite comparar uma consulta com uma matriz inteira de documentos de uma vez:

```python
documentos = np.array(vetores_dos_artigos)
documentos = documentos / np.linalg.norm(documentos, axis=1, keepdims=True)
consulta = vetor_da_consulta / np.linalg.norm(vetor_da_consulta)

notas = documentos @ consulta  # um cosseno por artigo
melhores = np.argsort(-notas)[:3]  # os 3 mais parecidos
```

Com alguns milhares de documentos, essa conta leva milissegundos. É a busca exata, que compara a consulta com todos.

## Gerar embeddings de verdade

A Anthropic não oferece um modelo de embeddings próprio, e indica a **Voyage AI**, empresa que hoje faz parte do MongoDB. Os modelos de uso geral mais recentes, de 2026, são o `voyage-4-large`, o de melhor qualidade, o `voyage-4`, equilibrado, e o `voyage-4-lite`, mais rápido e barato. Há também modelos especializados, para código, finanças e direito, e um modelo aberto, o `voyage-4-nano`, que pode rodar no seu próprio computador. A chave de API é criada no MongoDB Atlas, e a biblioteca Python é a `voyageai`:

```python
import voyageai

vo = voyageai.Client()  # lê a chave de VOYAGE_API_KEY

artigos = ["Como pedir reembolso. O estorno é feito...", "..."]
resultado = vo.embed(artigos, model="voyage-4", input_type="document")
vetores = resultado.embeddings  # uma lista de 1.024 números por artigo

consulta = vo.embed(
    ["quero meu dinheiro de volta"], model="voyage-4", input_type="query"
).embeddings[0]
```

O `input_type` diz se o texto é um documento, que vai ser encontrado, ou uma consulta. Indicar o tipo melhora a qualidade da busca. Os vetores da Voyage AI já vêm normalizados.

Outros provedores de modelos de linguagem também oferecem embeddings, e há modelos abertos, que rodam localmente. Algumas regras valem para todos:

- **O mesmo modelo para documentos e consultas.** Vetores de modelos diferentes não são comparáveis.
- **Trocar de modelo exige gerar de novo todos os vetores.** Guarde, junto com cada vetor, o nome do modelo que o gerou.
- **Os embeddings custam por token**, como as chamadas aos modelos de linguagem, mas bem menos. Os vetores dos documentos são gerados uma vez e guardados; só as consultas são geradas a cada busca.
- **Avalie antes de escolher.** O melhor modelo para os seus documentos, em português e com o seu vocabulário, é o que acerta mais nas suas consultas, como você vai medir no fim deste tópico.

## Bancos vetoriais

Um **banco vetorial** guarda os vetores junto com metadados, como o título, a categoria, a data e o documento de origem, e encontra os mais próximos de um vetor de consulta. Três recursos fazem diferença:

- **Busca aproximada.** Com milhões de vetores, comparar a consulta com todos fica lento. Índices como o HNSW organizam os vetores num grafo e encontram vizinhos muito próximos dos melhores, sem olhar todos. A troca é aceitar, de vez em quando, perder um resultado que a busca exata acharia.
- **Filtros por metadados.** "Os artigos mais parecidos, mas só da categoria pagamento" ou "só documentos que este usuário pode ver". O filtro de permissão é essencial em sistemas com documentos internos.
- **Atualização.** Documentos novos entram, documentos apagados saem, sem reconstruir tudo.

As opções vão de extensões de bancos que você já conhece, como o **pgvector** no PostgreSQL e a extensão de busca vetorial do DuckDB, a bancos dedicados, como Qdrant, Chroma, Milvus e Pinecone, e à busca vetorial de plataformas como MongoDB Atlas, BigQuery e Databricks. Com o pgvector, por exemplo, a busca é uma consulta SQL, em que `<=>` é a distância de cosseno:

```sql
SELECT titulo
FROM artigos
WHERE categoria = 'pagamento'
ORDER BY embedding <=> '[0.12, -0.03, ...]'
LIMIT 5;
```

Para poucos milhares de documentos, como uma central de ajuda, um array do numpy e a conta da seção anterior bastam. O banco vetorial passa a valer a pena com volume, atualização frequente e filtros.

## Busca híbrida e reordenação

A busca por significado também erra. No desafio, a consulta "apareceu o código E-403" tem um vetor que capta o assunto, um erro no aplicativo, mas não o código exato. O primeiro resultado é "Aplicativo lento ou travando", e não "Erro E-403 no aplicativo". A busca por palavras acha o código na hora.

A **busca híbrida** roda as duas e junta os resultados. Como as notas das duas estão em escalas diferentes, a forma mais usada de juntar é pela posição, com a **fusão por posição recíproca** (RRF): cada documento ganha, de cada ranking em que aparece, 1 / (60 + posição), e os valores são somados. Quem aparece bem colocado nas duas listas sobe. No desafio:

| Busca                | Acertos na 1ª posição | Acertos nas 3 primeiras |
| -------------------- | --------------------- | ----------------------- |
| Por palavras         | 6 de 10               | 7 de 10                 |
| Por significado      | 8 de 10               | 10 de 10                |
| Híbrida (RRF)        | 10 de 10              | 10 de 10                |

Um passo a mais, comum em sistemas de produção, é a **reordenação**: a busca traz, digamos, 50 candidatos, e um modelo de reordenação, como o `rerank-3` da Voyage AI, lê a consulta junto com cada candidato e escolhe os melhores. Ele é mais lento e mais preciso que a comparação de vetores, por isso só entra no fim, com poucos candidatos.

## Medir a qualidade da busca

Como saber se uma busca é melhor que outra? Com um **conjunto de avaliação**: consultas reais, cada uma com o documento certo marcado por alguém que conhece o assunto. A medida mais usada é o **acerto nos k primeiros**, ou *recall at k*: em quantas consultas o documento certo aparece entre os k primeiros resultados. Num sistema de RAG, em que os k primeiros trechos vão para o modelo de linguagem, é a medida mais direta: se o trecho certo não está entre eles, o modelo não tem como responder bem.

Dez consultas, como no desafio, servem para aprender. Para decidir de verdade, use algumas centenas, tiradas do histórico de buscas, e inclua os casos difíceis: sinônimos, códigos, erros de digitação, perguntas que não têm resposta nos documentos. O último tópico deste módulo aprofunda a avaliação de sistemas com LLM.

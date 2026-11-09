# Desafio: um assistente que responde com base nas políticas da empresa

O time de pessoas recebe todo dia as mesmas perguntas: qual o limite de reembolso de alimentação,
em quantos períodos dá para dividir as férias, quantos dias de home office são permitidos. As
respostas estão em quatro documentos internos, mas ninguém lê os documentos.

A ideia é um assistente que responde a essas perguntas **com base nos documentos**, citando de onde
tirou cada informação, e que diz "não encontrei" quando a resposta não está lá. Você vai montar o
caminho completo de um RAG: dividir os documentos em trechos, buscar os trechos certos, montar o
prompt com as fontes, chamar o modelo e conferir as citações da resposta.

## Os dados

- `data/documentos/`: as quatro políticas, em Markdown: reembolso de despesas, home office, férias e
  segurança da informação. Cada uma tem um título e algumas seções.
- `data/perguntas.json`: oito perguntas de pessoas da empresa, cada uma com o trecho que tem a
  resposta (ou nenhum, se a resposta não está nos documentos) e a resposta que um modelo deu,
  gravada.

O `modelo_gravado.py` tem um `ModeloGravado`, com a mesma cara do cliente do SDK da Anthropic, que
devolve as respostas gravadas: o desafio roda sem chave de API e sem custo. Algumas respostas
gravadas têm problemas de propósito. Descobrir quais é parte do desafio.

## O que fazer

Abra o `solucao.py` e implemente as funções, na ordem do arquivo. A função `ler_documentos` já está
pronta. Cada docstring explica o que a função recebe e devolve.

## Regras

1. Use `re`, `unicodedata`, numpy e scikit-learn. Nenhuma função pode alterar o que recebe.
2. Não altere `modelo_gravado.py`, a pasta `tests` nem os arquivos em `data`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 11 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k trechos`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Imprima os trechos de um documento e confira um por um: o id, a seção e o texto.
4. Só então consulte o gabarito em `desafios/_gabaritos/ia_documentos/rag/`.

## Depois de passar

- Leia as respostas gravadas das perguntas `p6` e `p8`. O que o modelo fez de errado em cada uma?
  Qual das duas é mais perigosa?
- A resposta da `p7` está certa, mas não cita a fonte. Por que isso é um problema, mesmo com a
  informação correta?
- Se tiver uma chave de API, troque o `ModeloGravado()` por `anthropic.Anthropic()` e rode
  `avaliar`. As respostas de um modelo atual têm os mesmos problemas?

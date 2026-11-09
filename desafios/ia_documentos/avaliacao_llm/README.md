# Desafio: medir o assistente antes de trocar o prompt

O assistente de políticas internas, do tópico de RAG, tem uma versão nova do prompt, a v2. Quem
escreveu testou algumas perguntas e achou as respostas melhores: mais completas, mais diretas. Antes
de trocar, o time quer números.

Você vai avaliar as duas versões num conjunto de 20 perguntas, com regras que o código consegue
conferir, separar o resultado por tipo de pergunta, comparar item a item, medir o quanto a
diferença pode ser sorte, e ler as notas de um modelo usado como juiz, conferindo se ele concorda
com as notas dadas por pessoas.

## Os dados

- `data/conjunto.json`: as 20 perguntas. As do tipo `factual` têm a resposta nos documentos e uma
  lista de fatos que a resposta precisa conter. As do tipo `fora_do_escopo` não têm resposta nos
  documentos: o certo é o assistente dizer que não encontrou.
- `data/respostas_v1.json` e `data/respostas_v2.json`: as respostas das duas versões, gravadas.
- `data/juiz.json`: as notas, de 1 a 5, que um modelo juiz deu a cada resposta, no texto em que
  ele respondeu.
- `data/notas_humanas.json`: as notas que pessoas do time deram a uma amostra de 12 respostas.

## O que fazer

Abra o `solucao.py` e implemente as funções, na ordem do arquivo. A função `carregar` já está
pronta. Cada docstring explica o que a função recebe e devolve.

## Regras

1. Use `json`, `re`, `unicodedata` e numpy. Nenhuma função pode alterar o que recebe.
2. Não altere a pasta `tests` nem os arquivos em `data`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 11 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k bootstrap`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Abra as respostas das duas versões lado a lado, item a item. Onde a v2 melhorou? Onde piorou?
4. Só então consulte o gabarito em `desafios/_gabaritos/ia_documentos/avaliacao_llm/`.

## Depois de passar

- Escreva a recomendação para o time, em três frases: a v2 deve substituir a v1? O que precisa
  mudar nela antes?
- Quantas perguntas o conjunto precisaria ter para que uma melhora de 5 pontos ficasse fora do
  intervalo de incerteza? Experimente repetir as diferenças 5 e 10 vezes e rodar o bootstrap.
- Reescreva a rubrica do juiz para que ele dê nota baixa a respostas que trazem informação que não
  está nos documentos.

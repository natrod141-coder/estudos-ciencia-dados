# Desafio: busca por significado na central de ajuda

A central de ajuda de uma loja online tem 16 artigos, e a busca do site procura pelas palavras
digitadas. O problema: os clientes escrevem do jeito deles. Quem digita "quero meu dinheiro de
volta" não encontra o artigo "Como pedir reembolso", porque as duas frases não têm nenhuma palavra
em comum.

Você vai comparar a busca por palavras com a busca por significado, com vetores, descobrir em que
cada uma erra, juntar as duas numa busca híbrida, medir os acertos de cada abordagem e montar um
pequeno banco vetorial com filtro por categoria.

## Os dados

- `data/artigos.json`: os 16 artigos, com título, texto, categoria e um vetor.
- `data/consultas.json`: 10 buscas reais de clientes, cada uma com o vetor e o artigo certo.

Os vetores são **de brinquedo**: têm 8 dimensões, uma para cada assunto da central (pagamento,
entrega, assinatura, conta, devolução, aplicativo, nota fiscal e promoção), para dar para entender
o que cada número quer dizer. Um modelo de embeddings de verdade, como os da Voyage AI, gera
vetores com mais de mil dimensões, que ninguém consegue interpretar uma a uma. As contas, porém,
são exatamente as mesmas.

## O que fazer

Abra o `solucao.py` e implemente as funções e a classe `IndiceVetorial`, na ordem do arquivo. Cada
docstring explica o que recebe e devolve.

## Regras

1. Use numpy e scikit-learn. Nenhuma função pode alterar o que recebe.
2. Não altere a pasta `tests` nem os arquivos em `data`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 11 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k hibrida`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Calcule à mão o cosseno entre `[1, 2]` e `[2, 4]`. Por que dá 1?
4. Só então consulte o gabarito em `desafios/_gabaritos/ia_documentos/embeddings/`.

## Depois de passar

- Para cada consulta, imprima o primeiro resultado das três buscas. Em que tipo de pergunta a busca
  por palavras ganha? E a por significado?
- Escreva uma consulta nova, invente o vetor dela pelos assuntos e teste. Que vetor você daria para
  "comprei com cupom e quero devolver"?
- Se tiver uma chave da Voyage AI, gere os vetores de verdade dos 16 artigos e das 10 consultas com
  `voyage-4`, e refaça a comparação.

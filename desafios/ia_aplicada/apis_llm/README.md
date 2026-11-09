# Desafio: classificar avaliações pela API, sem desperdício

O time de atendimento quer saber, toda semana, quantas avaliações de clientes foram positivas,
negativas ou neutras. Ler uma por uma não escala, e um modelo de linguagem resolve bem esse tipo de
classificação. Mas, numa chamada de API de verdade, aparecem problemas que o chat esconde:

- a resposta pode vir com espaços, maiúsculas, ponto final, ou com um rótulo que não foi pedido;
- a resposta pode ser cortada no meio, se o teto de tokens for pequeno demais;
- a API pode recusar a chamada por um instante, por limite de uso ou sobrecarga;
- avaliações repetidas não devem ser pagas duas vezes.

Você vai escrever o código que lida com tudo isso.

## Sem chave de API e sem custo

O arquivo `cliente_gravado.py` tem um `ClienteGravado`, com a mesma cara do cliente do SDK da
Anthropic: `cliente.messages.create(...)` devolve uma resposta com `content`, `stop_reason` e
`usage`, igual à de verdade. A diferença é que as respostas vêm de `data/respostas_gravadas.json`,
gravadas antes. O cliente gravado também consegue simular erros da API, para testar as
retentativas.

Quando quiser rodar com a API de verdade, troque `ClienteGravado()` por `anthropic.Anthropic()`, com
a sua chave na variável de ambiente `ANTHROPIC_API_KEY`. O resto do código continua igual, a não ser
o tipo de erro: no SDK, os erros da API são `anthropic.APIStatusError`, também com `status_code`.

## Os dados

- `data/avaliacoes.csv`: 12 avaliações, com duas repetidas.
- `data/respostas_gravadas.json`: a resposta gravada para cada avaliação diferente. Abra e repare
  nos blocos de raciocínio vazios, nos rótulos escritos de jeitos diferentes e na resposta cortada.

## O que fazer

Abra o `solucao.py` e implemente as funções, na ordem do arquivo. Cada docstring explica o que a
função recebe e devolve.

## Regras

1. Nenhuma função pode alterar o que recebe, a não ser o cache em `classificar`.
2. Não altere `cliente_gravado.py`, a pasta `tests` nem os arquivos em `data`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 12 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k retentativa`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Experimente o cliente gravado no terminal, digitando `python` dentro desta pasta:

   ```python
   from cliente_gravado import ClienteGravado
   cliente = ClienteGravado()
   r = cliente.messages.create(model="claude-haiku-5-5", max_tokens=256,
                               messages=[{"role": "user", "content": "Recebi o pedido."}])
   print(r.content, r.stop_reason, r.usage)
   ```

4. Só então consulte o gabarito em `desafios/_gabaritos/ia_aplicada/apis_llm/`.

## Depois de passar

- Calcule quanto custaria classificar 1 milhão de avaliações com os preços do teste. E com o Claude
  Opus 5.5, a US$ 4 e US$ 20 por milhão de tokens? E pela API de lotes, com metade do preço?
- Uma das avaliações foi classificada como "misto". Isso é erro do modelo ou da instrução? Como você
  mudaria o prompt: acrescentaria o rótulo "misto" ou diria o que fazer com avaliações que têm as
  duas coisas?
- Se você tiver uma chave de API, rode `classificar` com o cliente de verdade numa amostra pequena e
  compare com os rótulos gravados.

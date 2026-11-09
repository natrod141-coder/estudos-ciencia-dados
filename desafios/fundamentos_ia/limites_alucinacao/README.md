# Desafio: conferir as respostas do assistente

O time comercial começou a usar um assistente de IA para tirar dúvidas sobre o relatório de vendas.
Ele respondeu a dez perguntas. Nas perguntas sobre números, mostrou a consulta SQL que usou. Nas
perguntas sobre as regras do relatório, citou trechos do documento de regras. O texto das respostas
é fluente e confiante em todos os casos, mas nem todas estão certas.

Antes de as respostas irem para a reunião, você vai escrever um verificador que confere cada uma
contra o banco de vendas e contra o documento, e separa as respostas em cinco categorias:

| Categoria           | Quando                                                                 |
| ------------------- | ---------------------------------------------------------------------- |
| `correta`           | O número confere com a consulta, ou todas as citações existem         |
| `valor_errado`      | A consulta roda, mas o número do texto não confere com o resultado    |
| `sql_invalida`      | O banco recusa a consulta (por exemplo, uma coluna que não existe)    |
| `citacao_inventada` | Pelo menos uma citação não aparece no documento                       |
| `sem_fonte`         | A resposta não traz nem consulta nem citação: não há como conferir    |

## Os dados

- `data/vendas.csv`: faturamento por mês e região, de janeiro a junho. Colunas `mes`, `regiao` e
  `faturamento`.
- `data/regras_relatorio.txt`: o documento com as regras do relatório.
- `data/respostas_modelo.json`: as dez respostas do assistente, gravadas. Cada uma tem `id`,
  `pergunta` e `resposta`, e às vezes `sql` ou `citacoes`.

As respostas foram gravadas para você trabalhar sem chave de API e sem custo. O verificador que você
escrever funciona igual com respostas novas, vindas de uma chamada de verdade.

## O que fazer

Abra o `solucao.py` e implemente as funções, na ordem do arquivo. A função `criar_banco` já está
pronta: ela carrega o CSV num banco SQLite em memória. Cada docstring explica o que a função recebe
e devolve.

## Regras

1. Use só a biblioteca padrão do Python (`re`, `sqlite3`, `csv`, `json`).
2. Nenhuma função pode alterar o que recebe.
3. Não altere a pasta `tests` nem os arquivos em `data`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 10 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k extrair`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Para `extrair_numeros`, uma expressão regular ajuda. Teste a sua com "R$ 4.180.000,00." e com
   "Foram 7." antes de seguir.
4. Para entender uma resposta, rode a consulta dela à mão. Digite `python` no terminal, dentro
   desta pasta, e depois:

   ```python
   from solucao import criar_banco
   banco = criar_banco("data/vendas.csv")
   banco.execute("SELECT SUM(faturamento) FROM vendas").fetchone()
   ```

5. Só então consulte o gabarito em `desafios/_gabaritos/fundamentos_ia/limites_alucinacao/`.

## Depois de passar

Olhe as respostas classificadas como erradas e pense em como cada erro aconteceu:

- r02: o assistente "somou de cabeça" e chegou perto, mas errou por quase 2%.
- r03: inventou uma coluna `ticket_medio`, que não existe na tabela.
- r06: deu um número para o Centro-Oeste, que nem está na base. O que o documento de regras diz sobre
  essa região?
- r07: citou um trecho que não existe, e o trecho verdadeiro diz o contrário da resposta.
- r08: respondeu sem fonte. Procure no documento: a resposta está certa?

Para cada uma, escreva que instrução você colocaria no prompt para reduzir esse tipo de erro.

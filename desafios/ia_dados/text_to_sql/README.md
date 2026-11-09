# Desafio: perguntas em português, respostas em SQL

O time comercial vive pedindo números ao time de dados: a receita de março, as vendas por região,
os produtos que mais venderam. A ideia é um assistente que transforma a pergunta em SQL, executa e
devolve o resultado. Parece simples, até aparecerem os problemas: o modelo esquece uma regra do
negócio, inventa uma coluna, escreve o valor de uma categoria do jeito errado, ou alguém pede para
apagar dados.

Você vai montar o caminho completo: descrever o banco para o modelo, montar o prompt com o esquema e
as regras, extrair o SQL da resposta, barrar comandos perigosos, executar num banco somente leitura
e medir se o resultado bate com o de uma consulta escrita por uma pessoa.

## Os dados

- `data/produtos.csv`, `data/lojas.csv` e `data/vendas.csv`: um pequeno modelo estrela, com 259
  vendas de janeiro a março de 2026. A função `criar_banco` carrega tudo num arquivo do DuckDB.
- `data/perguntas.json`: oito perguntas do time comercial, cada uma com a consulta de referência,
  escrita por uma pessoa, e a resposta que um modelo deu, gravada.

O `modelo_gravado.py` tem um `ModeloGravado`, com a mesma cara do cliente do SDK da Anthropic, que
devolve as respostas gravadas: o desafio roda sem chave de API e sem custo.

## O que fazer

Abra o `solucao.py` e implemente as funções, na ordem do arquivo. As funções `criar_banco` e
`abrir_somente_leitura` já estão prontas. Cada docstring explica o que a função recebe e devolve.

## Regras

1. Use `re` e duckdb. Nenhuma função pode alterar o que recebe.
2. Não altere `modelo_gravado.py`, a pasta `tests` nem os arquivos em `data`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 10 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k segura`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Para explorar o banco, digite `python` dentro desta pasta:

   ```python
   from solucao import criar_banco, abrir_somente_leitura
   conexao = abrir_somente_leitura(criar_banco("loja.duckdb"))
   conexao.execute("select * from information_schema.columns").fetchall()
   ```

4. Só então consulte o gabarito em `desafios/_gabaritos/ia_dados/text_to_sql/`.

## Depois de passar

- Para cada pergunta que deu errado, leia o SQL gravado e diga que informação do prompt teria
  evitado o erro.
- A pergunta t8 pede para rodar um `DROP TABLE`. Se a sua função `consulta_segura` tivesse um
  defeito e deixasse o comando passar, o que aconteceria? Teste executando o comando direto na
  conexão somente leitura.
- Escreva mais três perguntas com a consulta de referência, incluindo uma ambígua, como "vendas do
  mês passado". Que resposta você esperaria do assistente para ela?

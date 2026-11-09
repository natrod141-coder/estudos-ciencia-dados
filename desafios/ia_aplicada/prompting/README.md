# Desafio: extrair dados de notas fiscais com saída estruturada

O financeiro recebe notas de serviço por e-mail, cada uma num formato: uma com tabela, outra num
parágrafo, outra num recibo de pessoa física, sem CNPJ. A ideia é usar um modelo de linguagem para
extrair, de cada e-mail, o fornecedor, o CNPJ, a data de emissão, o valor total e a categoria do
gasto, e lançar tudo numa planilha.

Antes de existir a saída estruturada, um modelo devolveu respostas em texto livre para oito
e-mails. Elas estão gravadas, e têm de tudo: JSON limpo, JSON com uma frase antes e cercas de
código, data no formato brasileiro, valor como texto, categoria fora da lista, campo a mais, um
e-mail que nem era uma nota, e um CNPJ que o modelo inventou.

Você vai:

1. Definir o formato da saída com uma classe do **pydantic**, a mesma que serviria para pedir a
   saída estruturada à API com `client.messages.parse(..., output_format=Nota)`.
2. Montar o prompt com exemplos e com o documento delimitado e protegido contra injeção.
3. Conferir as respostas gravadas: extrair o JSON, validar campo a campo, preparar o pedido de
   correção e pegar o CNPJ inventado, que passa na validação de formato.

## Os dados

- `data/documentos.json`: os oito e-mails, pelo identificador, de `n01` a `n08`.
- `data/exemplos.json`: dois exemplos de documento e saída esperada, para o prompt.
- `data/respostas_gravadas.json`: o texto que o modelo devolveu para cada e-mail.

## O que fazer

Abra o `solucao.py`. Comece pela classe `Nota`, que hoje é `None`: o comentário acima dela diz os
campos. Depois implemente as funções, na ordem do arquivo. Cada docstring explica o que a função
recebe e devolve.

## Regras

1. Use `json`, `re` e `pydantic`. Nenhuma função pode alterar o que recebe.
2. Não altere a pasta `tests` nem os arquivos em `data`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 15 testes passam.

## Se travar

1. Rode só os testes de uma parte: `pytest -v -k nota`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Para entender os erros do pydantic, rode no terminal, digitando `python` dentro desta pasta:

   ```python
   from solucao import Nota
   Nota.model_validate({"fornecedor": "x", "cnpj": None, "data_emissao": "15/03/2026",
                        "valor_total": 10, "categoria": "outros"})
   ```

4. Só então consulte o gabarito em `desafios/_gabaritos/ia_aplicada/prompting/`.

## Depois de passar

- Abra o e-mail `n07` e a resposta gravada para ele. De onde veio o CNPJ? Que instrução do prompt
  deveria ter evitado isso?
- O e-mail `n05` é de hospedagem de site. Em que categoria ele deveria entrar? Se a resposta não
  for óbvia nem para você, as categorias precisam de uma definição melhor nas instruções.
- Se você tiver uma chave de API, rode a extração de verdade com `client.messages.parse`, usando a
  sua classe `Nota` e as mensagens de `montar_mensagens`, e compare com as respostas gravadas.

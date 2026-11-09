# Desafio: revisar o código que a IA escreveu

Você pediu a um assistente de IA seis funções para o relatório de vendas. Ele entregou o arquivo
`codigo_da_ia.py`, testou cada função num exemplo simples, e todas rodaram sem erro. O código está
limpo, bem nomeado e com docstrings. Mesmo assim, cada função tem um problema, que só aparece em
algum caso.

O seu trabalho é o de quem revisa: encontrar o caso em que cada função erra, provar o erro com um
exemplo e entregar a versão corrigida.

## O que você vai praticar

- Ler código conferindo se ele faz o que foi pedido, e não só se parece certo.
- Montar exemplos pequenos, à mão, em que você sabe a resposta.
- Procurar os casos de borda: zero, valor vazio, último dia do mês, formato brasileiro.
- Reconhecer erros clássicos de dados: média de razões, duplicação depois de um merge e `NOT IN`
  com valor nulo.

## O que fazer

Para cada uma das seis funções de `codigo_da_ia.py`:

1. Leia o código e a docstring. A docstring é o pedido que foi feito ao assistente.
2. Descubra um caso em que o código não faz o que foi pedido. Rode a função da IA com exemplos
   pequenos até encontrar.
3. Registre esse caso em `CONTRAEXEMPLOS`, no `solucao.py`: os argumentos de uma chamada em que a
   versão da IA levanta um erro ou devolve um resultado diferente do certo.
4. Escreva a versão corrigida no `solucao.py`, com o mesmo nome e os mesmos parâmetros.

Para rodar a função da IA num exemplo, digite `python` no terminal, dentro desta pasta, e depois:

```python
from codigo_da_ia import limpar_valor
limpar_valor("R$ 59,90")
```

## Regras

1. Não altere `codigo_da_ia.py` nem a pasta `tests`.
2. Nenhuma função pode alterar o que recebe.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

São 12 testes: seis conferem as suas versões corrigidas, e seis conferem se cada contraexemplo
realmente mostra o erro da IA. O desafio está aprovado quando os 12 passam.

## Se travar

1. Rode só os testes de uma função: `pytest -v -k limpar`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Para cada função, pergunte: e se o valor for zero? E se tiver separador de milhar? E se o mesmo
   pedido aparecer em mais de uma linha? E se a venda for às 23h do último dia? E se a coluna
   tiver um valor vazio?
4. Só então consulte o gabarito em `desafios/_gabaritos/fundamentos_ia/conferir_codigo_gerado/`.

## Depois de passar

Escolha uma das funções e peça a um assistente de IA para revisá-la, sem dizer qual é o problema.
Ele encontrou o erro? Depois peça que ele escreva testes para a função. Os testes que ele escreveu
pegariam o erro? Compare com os seus contraexemplos.

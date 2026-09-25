# Desafio: da planilha bagunçada ao relatório

Todo mês, a Filial Centro manda para a matriz a planilha `data/vendas_filial.xlsx`, exportada do
sistema de vendas. E todo mês alguém gasta uma tarde arrumando a planilha no Excel antes de montar a
tabela dinâmica do faturamento. Você vai automatizar esse trabalho em Python: cada passo que seria
feito à mão no Excel vira uma função, e o relatório sai pronto, igual toda vez.

Abra a planilha no Excel ou no LibreOffice antes de começar e procure os problemas: título em cima do
cabeçalho, datas e valores guardados como texto, nomes escritos de jeitos diferentes, linhas
repetidas, uma linha de total no meio dos dados e um código de produto que não existe no cadastro.

## O que você vai praticar

- Ler planilhas com cabeçalho fora do lugar e várias abas.
- Converter texto em número e em data, no formato brasileiro.
- Fazer em pandas o equivalente a ARRUMAR, PRI.MAIÚSCULA, PROCX, SOMASES e tabela dinâmica.
- Gravar um relatório em `.xlsx` com várias abas.

## O que fazer

Abra o `solucao.py` e implemente as sete funções. A `ler_produtos` já está pronta. Sugestão de
ordem: `ler_vendas`, `texto_para_numero`, `limpar_vendas`, `procx`, `somases`, `tabela_dinamica`
e, por último, `exportar_relatorio`.

| Função              | O que faria no Excel                                          |
| ------------------- | ------------------------------------------------------------- |
| `ler_vendas`        | Apagar as linhas de título e a linha de total                 |
| `texto_para_numero` | `=VALOR(SUBSTITUIR(SUBSTITUIR(...)))`                         |
| `limpar_vendas`     | `ARRUMAR`, `PRI.MAIÚSCULA`, texto para data, remover duplicatas |
| `procx`             | `=PROCX(código; Produtos[Código]; Produtos[Produto]; "Não encontrado")` |
| `somases`           | `=SOMASES(valor; vendedor; "Ana Souza"; mês; 2)`              |
| `tabela_dinamica`   | Inserir > Tabela Dinâmica, com totais gerais                  |
| `exportar_relatorio`| Salvar como `.xlsx` com as abas Dados e Resumo                |

## Regras

1. Use pandas para ler, limpar e resumir, e deixe o pandas gravar o `.xlsx`.
2. Não edite a planilha de entrada à mão: o relatório precisa sair igual toda vez que rodar.
3. Não altere a pasta `tests`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 10 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k test_limpar_vendas`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Olhe os dados enquanto trabalha: `print(ler_vendas("data/vendas_filial.xlsx").head(10))`.
4. Só então consulte o gabarito em `desafios/_gabaritos/manipulacao/excel/`.

## Depois de passar

Gere o relatório e abra no Excel:

```
python -c "import solucao; solucao.exportar_relatorio('data/vendas_filial.xlsx', 'relatorio.xlsx')"
```

Monte a mesma tabela dinâmica à mão no Excel, a partir da aba Dados, e compare os totais. Depois
pense: se no mês que vem a planilha chegar com 100 mil linhas, quanto tempo cada caminho leva? E o
que o código de produto "P-099" diz sobre o cadastro da filial?

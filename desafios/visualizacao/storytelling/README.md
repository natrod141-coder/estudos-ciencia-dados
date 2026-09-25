# Desafio: do gráfico exploratório ao explicativo

A diretoria pediu um slide sobre as vendas de 2025 por canal: loja física, site e app. Os dados estão
em `data/vendas_por_canal.csv`. Um gráfico de linhas com as três séries, cores automáticas, legenda e
o título "Faturamento por canal" mostraria os dados, mas deixaria o trabalho de achar a mensagem para
quem está olhando. Numa reunião, ninguém faz esse trabalho.

Você vai transformar esse gráfico **exploratório**, que serve para você entender os dados, num
gráfico **explicativo**, que serve para o outro entender a sua conclusão em cinco segundos. E vai
escrever o resumo que acompanha o slide.

## O que você vai praticar

- Encontrar nos dados a mensagem principal e calculá-la, sem escrever números à mão.
- Escrever um título que afirma a conclusão.
- Usar cor para destacar a mensagem e cinza para o contexto.
- Trocar a legenda por rótulos diretos e tirar os elementos que não carregam informação.
- Resumir a análise em contexto, achado e recomendação.

## O que fazer

Abra o `solucao.py` e implemente as seis funções, na ordem do arquivo. A `ler_vendas` já está
pronta.

## Regras

1. Use pandas e matplotlib.
2. A mensagem vem dos dados: nada de escrever números à mão no título ou no resumo.
3. A função de gráfico devolve a figura e não chama `plt.show()`.
4. Não altere a pasta `tests` nem o arquivo em `data`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 7 testes passam.

Para ver o gráfico enquanto trabalha:

```
python -c "import solucao as s; s.grafico_explicativo(s.ler_vendas('data/vendas_por_canal.csv')).savefig('grafico.png')"
```

## Se travar

1. Rode só um teste: `pytest -v -k titulo`.
2. Leia as linhas que começam com `E`: elas dizem o que o teste esperava.
3. Antes de caprichar no visual, faça primeiro o gráfico padrão, com as três linhas, e olhe para ele.
   Qual é a mensagem? Só então comece a tirar e destacar coisas.
4. Só então consulte o gabarito em `desafios/_gabaritos/visualizacao/storytelling/`.

## Depois de passar

Ponha lado a lado o gráfico padrão e o seu gráfico explicativo e mostre os dois a alguém que não
conhece os dados, por cinco segundos cada. Pergunte o que a pessoa entendeu de cada um. Depois,
pense: em que situação a mensagem principal não seria o canal que mais cresceu, mas o que mais
faturou? O mesmo conjunto de dados pode contar histórias diferentes, e escolher qual contar depende
de quem vai decidir o quê.

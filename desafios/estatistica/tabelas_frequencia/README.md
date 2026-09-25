# Desafio: como se distribuem os atendimentos do SAC

O SAC de uma empresa registrou 60 chamados de uma semana (`data/atendimentos.csv`): o canal (chat,
e-mail ou telefone), a nota de 1 a 5 que o cliente deu e o tempo de atendimento em minutos. A
coordenadora quer saber três coisas: por qual canal chega a maioria dos chamados, quantos clientes
deram nota 3 ou menos, e como se distribui o tempo de atendimento, incluindo os casos que fogem do
padrão. Você vai responder com tabelas de frequência e com os números que formam um boxplot.

## O que você vai praticar

- Montar tabelas de frequência absoluta, relativa e acumulada.
- Agrupar uma variável contínua em classes, com o número de classes dado pela regra de Sturges.
- Calcular o resumo de cinco números e os limites de um boxplot.
- Identificar valores atípicos pela regra de 1,5 vez o intervalo interquartil.

## O que fazer

Abra o `solucao.py` e implemente as seis funções. Cada uma tem uma docstring explicando o que
recebe e o que devolve. Sugestão de ordem: `tabela_frequencia`, `numero_de_classes`,
`tabela_por_classes`, `cinco_numeros`, `limites_boxplot` e, por último, `resumo_atendimentos`.

## Regras

1. Na tabela de frequência, use o pandas (`value_counts`, `cumsum`).
2. Monte as classes, os quartis e os limites do boxplot na mão: sem numpy, sem o módulo `statistics`
   e sem `pd.cut` ou `quantile`. O módulo `math` pode.
3. Não altere a pasta `tests`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 8 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k test_tabela_por_classes`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Para as classes, desenhe no papel a reta de 10 a 50 com as divisões de 10 em 10 e marque onde cai
   cada valor. Onde fica o 20? E o 50?
4. Só então consulte o gabarito em `desafios/_gabaritos/estatistica/tabelas_frequencia/`.

## Depois de passar

Desenhe o histograma e o boxplot dos tempos para ver o que você calculou:

```python
import matplotlib.pyplot as plt
import pandas as pd

tempos = pd.read_csv("data/atendimentos.csv")["tempo_min"]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
ax1.hist(tempos, bins=7)
ax2.boxplot(tempos)
fig.savefig("tempos.png")
```

As duas classes vazias no histograma e os pontos isolados no boxplot contam a mesma história. O que
você diria à coordenadora sobre os três chamados atípicos? O boxplot do matplotlib calcula os quartis
por interpolação, então em outros dados os bigodes podem sair um pouco diferentes dos seus.

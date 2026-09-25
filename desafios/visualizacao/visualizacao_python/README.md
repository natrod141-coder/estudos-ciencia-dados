# Desafio: três bibliotecas, três gráficos

A rede de lojas quer um material de análise das vendas de janeiro de 2025 a junho de 2026
(`data/vendas.csv`). Três perguntas, três gráficos, cada um feito com a biblioteca que resolve
melhor:

1. **Como o faturamento evoluiu em cada UF?** Pequenos múltiplos com **matplotlib**: um gráfico por UF,
   todos com a mesma escala.
2. **Em que meses cada categoria vende mais?** Um mapa de calor com **seaborn**.
3. **Quanto cada UF fatura, e com quais categorias?** Barras empilhadas interativas com **plotly**,
   salvas em HTML para mandar a quem não tem Python.

## O que você vai praticar

- Preparar os dados de cada gráfico com `pivot_table` e `groupby`.
- Montar figuras com vários gráficos e eixos compartilhados no matplotlib.
- Usar o seaborn para gráficos estatísticos com pouco código.
- Criar gráficos interativos com o plotly e exportá-los em HTML.

## O que fazer

Abra o `solucao.py` e implemente as cinco funções. A `ler_vendas` já está pronta. Sugestão de ordem:
`faturamento_mensal_por_uf`, `pequenos_multiplos`, `mapa_de_calor`, `grafico_interativo` e
`salvar_html`.

## Regras

1. Use matplotlib nos pequenos múltiplos, seaborn no mapa de calor e plotly no gráfico interativo.
2. As funções de gráfico devolvem a figura e não chamam `plt.show()` nem `fig.show()`.
3. Não altere a pasta `tests` nem o arquivo em `data`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 7 testes passam.

Para ver os gráficos enquanto trabalha:

```
python -c "import solucao as s; s.mapa_de_calor(s.ler_vendas('data/vendas.csv')).savefig('mapa.png')"
python -c "import solucao as s; s.salvar_html(s.grafico_interativo(s.ler_vendas('data/vendas.csv')), 'grafico.html')"
```

## Se travar

1. Rode só um teste: `pytest -v -k mapa`.
2. Leia as linhas que começam com `E`: elas dizem o que o teste esperava do gráfico.
3. Prepare e imprima a tabela antes de desenhar: a maioria dos problemas está nos dados, e não no
   gráfico.
4. Só então consulte o gabarito em `desafios/_gabaritos/visualizacao/visualizacao_python/`.

## Depois de passar

Abra o `grafico.html` no navegador e explore: passe o mouse, clique nas categorias da legenda para
escondê-las, dê zoom. Depois, olhe o mapa de calor: Eletrônicos fica bem mais forte a partir de
novembro de 2025. Quanto disso é a sazonalidade do fim de ano, e quanto é o Relógio GPS, que mudou de
Acessórios para Eletrônicos em outubro? A resposta está no desafio de modelagem.

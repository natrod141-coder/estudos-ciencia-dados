# Desafio: qual centro de distribuição é mais confiável

Uma loja online despacha pedidos de dois centros de distribuição, Guarulhos e Contagem. Os dois
entregam, em média, em 5 dias. O time de logística precisa escolher um deles para uma campanha em
que o prazo prometido ao cliente é de 7 dias. Olhando só a média, os dois parecem iguais. Os dados de
30 entregas recentes (`data/entregas.csv`) mostram outra coisa.

## O que você vai praticar

- Calcular amplitude, variância e desvio padrão sem bibliotecas prontas.
- Entender a diferença entre variância populacional (divide por n) e amostral (divide por n - 1).
- Comparar a variabilidade de grupos com o coeficiente de variação.
- Calcular o intervalo interquartil, a medida de variabilidade que resiste a valores atípicos.
- Separar os dados por grupo com pandas.

## O que fazer

Abra o `solucao.py` e implemente as seis funções. Cada uma tem uma docstring explicando o que
recebe e o que devolve. Sugestão de ordem: `amplitude`, `variancia`, `desvio_padrao`,
`coeficiente_variacao`, `intervalo_interquartil` e, por último, `comparar_centros`.

## Regras

1. Não use o módulo `statistics` nem o `numpy`. O módulo `math` pode (para a raiz quadrada).
2. O pandas só serve para ler o arquivo e separar os dados de cada centro.
3. Não altere a pasta `tests`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 8 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k test_variancia`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Faça a conta de um exemplo pequeno no papel, como `[2, 4, 4, 4, 5, 5, 7, 9]`, e compare com o que
   a função devolve.
4. Só então consulte o gabarito em `desafios/_gabaritos/estatistica/variabilidade/`.

## Depois de passar

Os dois centros têm a mesma média. Com base no resultado de `comparar_centros`, qual você escolheria
para a campanha com prazo de 7 dias, e por quê? Se conseguir explicar em duas frases usando o desvio
padrão e o percentual de atrasos, você dominou o ponto central do tópico.

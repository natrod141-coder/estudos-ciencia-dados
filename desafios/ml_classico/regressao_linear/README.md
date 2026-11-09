# Desafio: quanto tempo leva uma entrega

A empresa de entregas quer mostrar ao cliente, na hora da compra, quanto tempo o pedido vai levar.
Hoje o site mostra sempre "até 60 minutos", e as reclamações de atraso não param. Você tem 600
entregas passadas, com a distância, o peso, a quantidade de itens, se chovia, se era horário de
pico, a região e o tempo que a entrega levou.

Você vai treinar uma regressão linear, medir o erro em entregas que o modelo nunca viu, comparar
com uma previsão ingênua e ler o que os coeficientes dizem sobre o negócio.

## Os dados

`data/entregas.csv`, com uma linha por entrega:

| Coluna         | O que é                                    |
| -------------- | ------------------------------------------ |
| `pedido_id`    | Identificador do pedido                    |
| `distancia_km` | Distância da loja ao cliente               |
| `peso_kg`      | Peso do pacote                             |
| `itens`        | Quantidade de itens                        |
| `chuva`        | 1 se chovia, 0 se não                      |
| `horario_pico` | 1 se a entrega foi em horário de pico      |
| `regiao`       | centro, norte ou sul                       |
| `tempo_min`    | Tempo da entrega, em minutos: o alvo       |

## O que fazer

Abra o `solucao.py` e implemente as funções, na ordem do arquivo. Cada docstring explica o que a
função recebe e devolve.

## Regras

1. Use pandas, numpy e scikit-learn. Nenhuma função pode alterar o que recebe.
2. Não altere a pasta `tests` nem os arquivos em `data`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 9 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k baseline`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Para o R², faça a conta à mão com o exemplo do teste: reais 10, 20, 30, 40; previstos 12, 18,
   33, 37.
4. Só então consulte o gabarito em `desafios/_gabaritos/ml_classico/regressao_linear/`.

## Depois de passar

- Escreva, em uma frase cada, o que significam os coeficientes de `chuva` e de `regiao_norte`.
- Olhe as piores previsões. Elas têm algo em comum? O erro do modelo é parecido para entregas
  curtas e longas?
- O que o modelo prevê para uma entrega de 80 km? Os dados de treino vão até 25 km: em quanto você
  confiaria nesse número?

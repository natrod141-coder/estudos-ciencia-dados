# Desafio: um portão de qualidade para a carga diária

Todo dia, a carga com os pedidos do dia chega num CSV e, depois de conferida, alimenta o painel de
vendas. Hoje, a carga veio com problemas: um pedido repetido, um pedido sem cliente, um cliente que
não existe no cadastro, um status que ninguém conhece e valores impossíveis.

Você vai escrever as verificações de qualidade e o **portão** que decide o que fazer com a carga:

| Decisão                 | Quando                                                                  |
| ----------------------- | ----------------------------------------------------------------------- |
| `publicar`              | Nenhuma regra falhou                                                    |
| `publicar_com_aviso`    | Só regras de aviso falharam                                             |
| `publicar_sem_as_ruins` | Regras de erro falharam em poucos pedidos: eles vão para a quarentena  |
| `bloquear`              | Regras de erro falharam em pedidos demais: nada é publicado             |

## Os dados

- `data/carga_pedidos.csv`: a carga do dia, com 40 linhas.
- `data/clientes.csv`: o cadastro de clientes, para conferir se cada pedido aponta para um cliente
  que existe.
- `data/regras.json`: as seis regras de qualidade da carga, cada uma com tipo e severidade.
- `data/historico_volume.csv`: quantas linhas chegaram em cada um dos 14 dias anteriores.

## O que fazer

Abra o `solucao.py` e implemente as funções, na ordem do arquivo. As funções `ler_carga` e
`ler_regras` já estão prontas. As verificações de linha devolvem uma Series de booleanos, em que
True marca a linha com problema. Assim, `df[mascara]` mostra as linhas que falharam.

## Regras

1. Use pandas. Nenhuma função pode alterar o que recebe.
2. Não altere a pasta `tests` nem os arquivos em `data`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 11 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k intervalo`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Abra o CSV da carga e procure os problemas à mão antes de programar: os pedidos 5012, 5020,
   5027, 5031, 5035 e 5038 têm alguma coisa errada. E o 5016?
4. Só então consulte o gabarito em `desafios/_gabaritos/analytics_eng/qualidade_dados/`.

## Depois de passar

Pense no portão como parte do processo do time:

- O que você colocaria na mensagem de alerta quando a carga for bloqueada? Para quem ela iria?
- Escreva a regra que faltou: `criado_em` precisa ser do dia da carga. Que tipo de regra é essa?
- Rode `volume_anormal` com o tamanho da carga de hoje. E se amanhã chegarem 400 linhas por causa
  de uma promoção? O portão deveria bloquear?

# Desafio: uma amostra que represente a base de clientes

Uma empresa de assinaturas tem 1.000 clientes (`data/clientes.csv`) e quer entrevistar 100 deles
para entender por que alguns trocam do plano básico para o premium. Entrevistar todos custa caro
demais, então é preciso escolher uma amostra. Quem exportou a base mandou o arquivo ordenado por
região, e a primeira ideia do time foi "pegar os 100 primeiros". Você vai mostrar por que essa ideia
é ruim e montar amostras melhores.

## O que você vai praticar

- Sortear amostras aleatórias simples de forma reproduzível, com semente.
- Montar amostras sistemáticas e estratificadas proporcionais.
- Medir o quanto a composição de uma amostra se afasta da população.
- Calcular a margem de erro de uma proporção e o tamanho de amostra necessário.

## O que fazer

Abra o `solucao.py` e implemente as oito funções. Cada uma tem uma docstring explicando o que
recebe e o que devolve. Sugestão de ordem: `amostra_aleatoria_simples`, `amostra_sistematica`,
`tamanhos_por_estrato`, `amostra_estratificada`, `erro_de_composicao`, `margem_de_erro`,
`tamanho_amostra` e, por último, `avaliar_amostras`.

## Regras

1. Use o pandas para ler e sortear (`.sample`) e o módulo `math` para as contas.
2. Não use bibliotecas de amostragem prontas, como o scikit-learn.
3. Não altere a pasta `tests`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 10 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k test_tamanhos_por_estrato`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Para `tamanhos_por_estrato`, faça a conta de n = 30 no papel antes de programar: cota, parte
   inteira e resto de cada região.
4. Só então consulte o gabarito em `desafios/_gabaritos/estatistica/amostragem/`.

## Depois de passar

Rode `avaliar_amostras` e compare os quatro erros. Depois, compare a porcentagem de clientes premium
em cada amostra com a da população (19,1%). Por que a amostra sistemática acertou a composição por
região em cheio, mesmo sem sorteio? Dica: pense na ordem das linhas do arquivo. E o que aconteceria
com ela se, por algum motivo, o arquivo tivesse um cliente premium exatamente a cada 10 linhas?

# Desafio: o pacote tem mesmo 500 gramas?

Uma torrefação vende café em pacotes com 500 g no rótulo. Um órgão de fiscalização pesou 40 pacotes
comprados no mercado (`data/pacotes.csv`), e a média deu um pouco abaixo de 500 g. Pode ser só a
variação natural da máquina de envase, ou pode ser que ela esteja desregulada e o consumidor esteja
levando menos café do que paga. Você vai fazer o teste de hipóteses que responde a essa pergunta e
ver como a conclusão depende do nível de significância escolhido.

## O que você vai praticar

- Transformar uma pergunta em hipótese nula e hipótese alternativa.
- Calcular a estatística z e o valor p, em testes bilaterais e unilaterais.
- Testar uma média e uma proporção.
- Calcular um intervalo de confiança e ver a ligação dele com o teste.
- Decidir com um nível de significância e escrever a conclusão do jeito certo.

## O que fazer

Abra o `solucao.py` e implemente as seis funções. Cada uma tem uma docstring explicando o que
recebe e o que devolve. Sugestão de ordem: `valor_p`, `teste_z_media`, `teste_z_proporcao`,
`rejeita_h0`, `intervalo_confianca_media` e, por último, `analisar_pacotes`.

## Regras

1. Pode usar o módulo `statistics`: `mean` e `stdev` para média e desvio padrão, e `NormalDist` para
   a distribuição normal.
2. Não use scipy nem statsmodels. O objetivo é entender cada passo do teste.
3. Não altere a pasta `tests`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 10 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k test_valor_p`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Para entender o valor p, desenhe a curva normal e pinte a área que ele representa. No bilateral,
   são as duas caudas, além de z e aquém de -z.
4. Só então consulte o gabarito em `desafios/_gabaritos/estatistica/teste_hipoteses/`.

## Depois de passar

Rode `analisar_pacotes` com `alfa=0.05` e com `alfa=0.01`. Os dados são os mesmos, mas as conclusões
são diferentes. Escreva, em duas ou três frases, o que você diria ao órgão de fiscalização em cada
caso, sem usar a palavra "provado". Depois, pense: por que o α precisa ser escolhido antes de olhar
os dados?

# Desafio: escolher o limiar pelo dinheiro

O modelo de cancelamento está pronto, e o time de retenção quer começar a campanha: cada cliente da
lista recebe uma ligação e uma oferta, que custam juntas R$ 40. Um cliente que fica vale R$ 400 no
ano, e, dos clientes que iam cancelar e recebem o contato, 30% ficam. A pergunta do time é simples:
para quem ligar?

Você vai calcular as métricas à mão, comparar com o scikit-learn, montar a tabela de limiares,
escolher o limiar que dá mais lucro, avaliar uma lista de tamanho fixo e conferir se as
probabilidades do modelo são confiáveis.

## Os dados

A função `probabilidades_de_teste`, já pronta, treina a regressão logística do tópico de regressão
logística com `data/assinaturas.csv` e devolve, para os 1.250 clientes de teste, se cada um cancelou
e a probabilidade que o modelo deu.

## O que fazer

Abra o `solucao.py` e implemente as funções, na ordem do arquivo. Faça as contas das métricas você
mesmo, com numpy: os testes comparam o seu resultado com o do scikit-learn.

## Regras

1. Use numpy e pandas. Nenhuma função pode alterar o que recebe.
2. Não altere a pasta `tests` nem os arquivos em `data`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 9 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k lucro`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Para a AUC por pares, comece pelo exemplo pequeno do teste e conte os pares à mão. Com numpy,
   `positivos[:, None] > negativos[None, :]` compara todos os pares de uma vez.
4. Só então consulte o gabarito em `desafios/_gabaritos/ml_classico/metricas/`.

## Depois de passar

- Monte um gráfico do lucro por limiar. Onde ele cruza o zero? Por que limiares muito baixos dão
  prejuízo?
- O time só consegue fazer 300 ligações por trimestre. A lista dos 300 clientes de maior risco dá
  mais ou menos lucro que o limiar ótimo? Qual você recomendaria?
- Escreva, em três frases, o resultado para a diretoria, sem usar as palavras precisão, recall e
  AUC.

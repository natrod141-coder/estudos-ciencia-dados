# Desafio: pronta para a nuvem

A API de cancelamento já tem imagem Docker e está quase pronta para o Cloud Run. Quase: na nuvem,
ninguém vai olhar o terminal, a configuração chega por variáveis de ambiente, cada requisição
custa dinheiro e uma versão com defeito pode chegar a todos os usuários de uma vez.

Você vai escrever as peças que cuidam disso: a configuração conferida quando a API sobe, os
registros num formato que a plataforma entende, a conta do custo antes da fatura, o
acompanhamento do orçamento e a decisão de promover ou reverter uma versão nova.

## Os arquivos

- `data/precos_cloud_run.json`: os preços do Cloud Run e a cota gratuita, conferidos na página
  oficial em novembro de 2026.
- `solucao.py`: a classe de configuração e as funções que você vai escrever.

O desafio não publica nada e não precisa de conta na nuvem. As contas de custo são uma estimativa
simplificada; para decidir de verdade, use a calculadora oficial do Google Cloud.

## O que fazer

Complete o `solucao.py`, na ordem do arquivo: a classe `Configuracao` e as funções `linha_de_log`,
`custo_mensal`, `acompanhar_orcamento` e `decidir_lancamento`. Cada docstring explica o que fazer.

## Regras

1. Use `json`, `datetime` e as bibliotecas `pydantic` e `pydantic-settings`, que vêm com o FastAPI.
2. Nenhuma função pode alterar o que recebe.
3. Não altere a pasta `tests` nem os arquivos em `data`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 15 testes passam.

## Se travar

1. Rode só um grupo de testes: `pytest -v -k configuracao`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que o seu código devolveu.
3. Para a configuração, experimente no terminal. No PowerShell, defina as duas variáveis
   obrigatórias, `$env:CHAVE_API = "uma-chave-com-16-letras"` e `$env:ANTHROPIC_API_KEY = "teste"`;
   depois, no `python`, rode `from solucao import Configuracao; Configuracao()`.
4. Só então consulte o gabarito em `desafios/_gabaritos/producao/deploy_nuvem/`.

## Depois de passar

- Use a `Configuracao` no ciclo de vida da API do desafio de FastAPI. Sem a `ANTHROPIC_API_KEY`, o
  que acontece agora, e quando?
- Refaça a conta do custo com a região de São Paulo, que está no nível 2 de preço, consultando a
  página oficial. Quanto muda?
- Com os números do teste de custo, quantas requisições por mês cabem na cota gratuita com uma
  instância de 1 vCPU e 512 MiB, respondendo em 200 ms, uma requisição por vez?

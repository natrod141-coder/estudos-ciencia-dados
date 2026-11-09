# Desafio: uma API para o modelo de cancelamento

O modelo de cancelamento do módulo de machine learning ficou bom, e agora o time de relacionamento
quer usá-lo no sistema de atendimento. O sistema não roda Python nem lê notebooks: ele faz
requisições HTTP. Você vai escrever a API que recebe os dados de um cliente e devolve a
probabilidade de ele cancelar, com tudo o que uma API de verdade precisa: validação da entrada,
chave de acesso, documentação, previsões em lote, o modelo carregado uma vez só e uma resposta
clara quando um serviço de fora falha.

## Os arquivos

- `data/modelo.json`: a regressão logística do módulo de machine learning, treinada com
  `data/assinaturas.csv` e gravada em JSON por `treinar_modelo.py`.
- `modelo.py`: lê o modelo e calcula as probabilidades. Já está pronto.
- `data/clientes_exemplo.json`: três clientes, um de cada faixa de risco, para testar na mão.
- `llm_gravado.py`: um cliente com a mesma cara do SDK da Anthropic e uma resposta gravada. Ele
  também imita as falhas da API, levantando os mesmos erros do SDK. O desafio roda sem chave de API
  e sem custo.

## O que fazer

Abra o `solucao.py` e complete, na ordem do arquivo: a função `faixa_de_risco`, os modelos do
Pydantic, o ciclo de vida, a dependência `exigir_chave` e as quatro rotas. Cada docstring explica
o que fazer.

## Regras

1. Não altere `modelo.py`, `llm_gravado.py`, a pasta `tests` nem os arquivos em `data`.
2. Mantenha os nomes e os caminhos das rotas.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 12 testes passam.

## Para ver a API funcionando

Defina a chave e suba o servidor de desenvolvimento, que reinicia a cada mudança no código:

```
# Linux ou macOS
export CHAVE_API=minha-chave-local
# Windows (PowerShell)
$env:CHAVE_API = "minha-chave-local"

fastapi dev solucao.py
```

Abra http://127.0.0.1:8000/docs. Clique em Authorize, informe a chave e experimente a rota
`/previsoes` com um dos clientes de `data/clientes_exemplo.json`.

## Se travar

1. Rode só um teste: `pytest -v -k chave`.
2. Leia as linhas que começam com `E`: mostram o valor esperado e o que a API devolveu.
3. Um 422 inesperado traz, no corpo da resposta, o campo e o motivo. Imprima `resposta.json()`.
4. Só então consulte o gabarito em `desafios/_gabaritos/producao/fastapi/`.

## Depois de passar

- Sem a variável `ANTHROPIC_API_KEY`, chame `/previsoes/explicacao` pelo `/docs`. O que acontece? E
  por que é melhor descobrir isso quando o servidor sobe, e não na primeira requisição? O tópico
  de publicar na nuvem volta a esse ponto.
- Troque a rota de explicação para `async def`, com o `anthropic.AsyncAnthropic`. O que muda no
  código e por quê?
- Treine o modelo de novo com `python treinar_modelo.py`, mudando a versão. Como o sistema de
  atendimento saberia qual versão respondeu cada previsão?

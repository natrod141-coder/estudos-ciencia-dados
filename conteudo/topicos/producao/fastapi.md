---
titulo: "FastAPI"
modulo: producao
ordem: 1
horas: 10
estado: publicado
resumo: "Expor um modelo ou uma aplicação de IA como uma API."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Do notebook ao serviço"
    tipo: leitura
    minutos: 8
  - id: a2
    titulo: "HTTP em poucas palavras"
    tipo: leitura
    minutos: 12
  - id: a3
    titulo: "A primeira API"
    tipo: leitura
    minutos: 12
  - id: a4
    titulo: "Validar a entrada com Pydantic"
    tipo: leitura
    minutos: 15
  - id: a5
    titulo: "Servir um modelo de machine learning"
    tipo: leitura
    minutos: 15
  - id: a6
    titulo: "Dependências e chave de acesso"
    tipo: leitura
    minutos: 12
  - id: a7
    titulo: "Chamar um LLM de dentro da API"
    tipo: leitura
    minutos: 12
  - id: a8
    titulo: "Testar a API"
    tipo: leitura
    minutos: 10
  - id: a9
    titulo: "Vídeo de apoio: FastAPI do zero"
    tipo: video
    minutos: 40
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "O sistema de atendimento mandou idade igual a 'trinta' e a API respondeu 422. O que aconteceu?"
    opcoes: ["O servidor caiu", "O Pydantic recusou a entrada antes de ela chegar à sua função, e a resposta diz o campo e o motivo", "A chave da API estava errada", "O modelo de machine learning não conseguiu prever"]
    correta: 1
    explicacao: "Com o tipo declarado no modelo do Pydantic, o FastAPI valida o corpo da requisição e devolve 422 com a lista de erros, cada um com o campo e o motivo. A sua função só roda com dados válidos."
  - pergunta: "Por que carregar o modelo de machine learning no ciclo de vida da API, e não dentro da rota de previsão?"
    opcoes: ["Porque a rota não consegue abrir arquivos", "Porque o ciclo de vida deixa o modelo mais preciso", "É indiferente", "Porque carregar o modelo é lento: feito uma vez, quando o servidor sobe, cada requisição só faz a conta"]
    correta: 3
    explicacao: "Ler um modelo do disco pode levar segundos. Dentro da rota, esse tempo se repete em toda requisição. No ciclo de vida, o modelo fica na memória e é usado por todas as requisições."
  - pergunta: "Um cliente enviou a chave da API errada. Que código de status a API deve devolver?"
    opcoes: ["401", "404", "422", "500"]
    correta: 0
    explicacao: "401 quer dizer que a requisição não está autenticada: chave ausente ou inválida. 403 é para quem está autenticado mas não tem permissão para aquela ação. 404 é recurso inexistente, 422 é entrada inválida e 500 é erro do servidor."
  - pergunta: "O campo usa_app tem valor padrão False. Um sistema manda usaApp, com outra grafia, e a API ignora o campo calada. Qual é o problema?"
    opcoes: ["Nenhum, o valor padrão resolve", "A API fica mais lenta", "A previsão sai com usa_app falso sem ninguém perceber; recusar campos desconhecidos, com extra igual a forbid, faz o erro aparecer", "O modelo dá erro de execução"]
    correta: 2
    explicacao: "Por padrão, o Pydantic ignora campos que não conhece. Com um valor padrão, o erro de grafia vira uma previsão errada e silenciosa. Recusar campos extras transforma o problema num 422, que quem chama a API vê na hora."
  - pergunta: "Onde a chave que protege a API deve ficar?"
    opcoes: ["Escrita no código, para não se perder", "Numa variável de ambiente ou num gerenciador de segredos, fora do código e do Git", "No README do projeto", "No corpo de cada resposta"]
    correta: 1
    explicacao: "Segredo no código vai para o Git, e do Git para qualquer pessoa com acesso ao repositório, para sempre no histórico. A API lê a chave do ambiente; em produção, o valor vem de um gerenciador de segredos."
  - pergunta: "Na rota de previsão, por que é importante aplicar exatamente o mesmo pré-processamento usado no treino?"
    opcoes: ["Porque o modelo aprendeu com os dados transformados de um jeito; transformados de outro, as previsões ficam erradas sem nenhum erro aparecer", "Porque o FastAPI exige", "Porque deixa a API mais rápida", "Não é importante: o modelo se adapta"]
    correta: 0
    explicacao: "É o desvio entre treino e produção: uma padronização com outra média ou uma categoria codificada em outra ordem e o modelo responde com confiança, mas errado. Salvar o pré-processamento junto com o modelo, num pipeline, evita reescrever a transformação."
  - pergunta: "A rota de explicação chama a API do Claude, que responde com erro de sobrecarga. O que a sua API deve devolver?"
    opcoes: ["500, com a mensagem original do erro", "200, com a explicação vazia", "Repetir a chamada até funcionar, sem limite", "503, com uma mensagem clara, e registrar o detalhe no servidor"]
    correta: 3
    explicacao: "503 diz a quem chama que o serviço está indisponível agora e que vale tentar de novo. A mensagem original fica no registro: ela pode revelar detalhes internos. O SDK já tenta de novo algumas vezes antes de levantar o erro."
  - pergunta: "Uma rota usa o cliente síncrono do SDK da Anthropic, que espera a resposta da rede. Como declarar a função?"
    opcoes: ["Com async def, sempre", "Tanto faz", "Com def: o FastAPI roda a função num conjunto de threads e o servidor segue atendendo outras requisições", "Não é possível usar o SDK numa API"]
    correta: 2
    explicacao: "Uma chamada que bloqueia dentro de async def trava o laço de eventos, e o servidor inteiro espera. Com def, o FastAPI usa threads. Para usar async def, troque pelo cliente assíncrono, o AsyncAnthropic, com await."
  - pergunta: "Como testar a rota que chama o LLM sem gastar com a API e sem depender da rede?"
    opcoes: ["Trocando a dependência que cria o cliente por um cliente gravado, com app.dependency_overrides", "Não é possível testar", "Desligando a internet durante o teste", "Usando sempre o modelo mais barato"]
    correta: 0
    explicacao: "Quando o cliente do LLM chega à rota por uma dependência, o teste troca a dependência por um objeto com a mesma cara e respostas conhecidas. O teste fica rápido, sem custo e sempre igual, e ainda simula falhas."
  - pergunta: "De onde vem a documentação interativa que o FastAPI publica em /docs?"
    opcoes: ["De um arquivo escrito à mão", "Do esquema OpenAPI, gerado a partir das rotas, dos tipos e dos modelos do Pydantic, com as descrições dos campos", "De um serviço pago", "Dos testes"]
    correta: 1
    explicacao: "O FastAPI monta o esquema OpenAPI com o que você já declarou no código. Por isso a documentação nunca fica desatualizada, e as descrições escritas em Field aparecem para quem vai usar a API."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "O time de produto quer que o aplicativo mostre, para cada cliente, o risco de cancelamento e uma explicação escrita por IA. Descreva a API que você construiria: as rotas, a validação, a segurança, o que fazer quando o LLM falha e como você testaria."
  rubrica:
    - "Descreve rotas com entradas e saídas definidas por modelos do Pydantic, com tipos, limites, valores permitidos e recusa de campos desconhecidos, e uma rota de saúde."
    - "Descreve o modelo carregado uma vez, com o mesmo pré-processamento do treino e a versão na resposta, e a chave de acesso lida do ambiente, com 401 para chave ausente ou errada."
    - "Descreve o tratamento da falha do LLM, com 503 e registro do erro, a previsão funcionando sem o LLM, e os testes com o cliente de teste e a troca das dependências."
  modelo: "Eu faria três rotas: /saude, sem chave, para a plataforma conferir se a API está de pé; /previsoes, que recebe os dados de um cliente e devolve a probabilidade, a faixa de risco e a versão do modelo; e /previsoes/explicacao, que devolve a mesma previsão e um texto gerado pelo LLM. A entrada é um modelo do Pydantic com cada campo tipado, limites como idade de 18 a 100, valores permitidos para plano e canal e recusa de campos desconhecidos, para que um erro de grafia vire um 422 e não uma previsão errada. O modelo de machine learning é carregado uma vez, no ciclo de vida, como um pipeline com o pré-processamento do treino, e a versão volta em toda resposta. As rotas de previsão exigem uma chave no cabeçalho, comparada com o valor de uma variável de ambiente; chave ausente ou errada é 401. Na explicação, o cliente do LLM chega por uma dependência; se a API do modelo falhar, devolvo 503 com uma mensagem clara e registro o detalhe no servidor, e a rota de previsão continua funcionando. Para testar, uso o TestClient do FastAPI e troco a dependência do LLM por um cliente gravado: testo entradas válidas e inválidas, a chave, o lote, o modelo carregado uma vez e as falhas do LLM, sem custo e sem rede."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Uma API para o modelo de cancelamento"
  descricao: "Você vai expor o modelo de cancelamento do módulo de machine learning como uma API com FastAPI: modelos do Pydantic que validam a entrada e recusam campos desconhecidos, chave de acesso lida do ambiente, previsões em lote, o modelo carregado uma vez no ciclo de vida e uma rota que pede ao Claude uma explicação da previsão e devolve 503 quando ele falha. Os testes usam o cliente de teste do FastAPI e um cliente do Claude com respostas gravadas, sem chave de API e sem custo."
  pasta: "desafios/producao/fastapi"
  testes: 12
  tempo: "3 h"
  ferramentas: "VS Code, Python 3.11 ou superior, FastAPI e pytest"
  entrega: "Pull Request no GitHub"
  passos:
    - titulo: "Clone o repositório"
      descricao: "Só na primeira vez. Se já clonou, pule para o passo 2."
      comandos:
        - "git clone https://github.com/[seu_usuario]/[repositorio].git"
        - "cd [repositorio]"
    - titulo: "Abra o repositório no VS Code"
      descricao: "Se o VS Code oferecer Reopen in Container, aceite: o ambiente já vem pronto e você pode pular o passo 3."
      comandos:
        - "code ."
    - titulo: "Crie e ative o ambiente virtual"
      descricao: "Abra o terminal do VS Code com Ctrl+` (acento grave). Depois use Ctrl+Shift+P, Python: Select Interpreter, e escolha o .venv. O requirements.txt já inclui o FastAPI com o servidor e o cliente de testes."
      comandos:
        - "# Linux ou macOS"
        - "python3 -m venv .venv"
        - "source .venv/bin/activate"
        - "# Windows (PowerShell)"
        - "python -m venv .venv"
        - '.venv\Scripts\Activate.ps1'
        - "pip install -r desafios/requirements.txt"
    - titulo: "Leia o enunciado e conheça o modelo"
      descricao: "Abra desafios/producao/fastapi/README.md. O modelo está em data/modelo.json, e data/clientes_exemplo.json tem um cliente de cada faixa de risco."
    - titulo: "Complete o solucao.py"
      descricao: "Siga a ordem do arquivo. Cada classe e cada função tem uma docstring com o que fazer. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def faixa_de_risco(probabilidade):"
        - "class Cliente(BaseModel):"
        - "class Previsao(BaseModel):"
        - "async def ciclo_de_vida(app):"
        - "def exigir_chave(chave: str | None = Security(chave_api)):"
        - "def saude(request: Request):"
        - "def prever(cliente: Cliente, request: Request):"
        - "def prever_lote(pedido: PedidoLote, request: Request):"
        - "def explicar(cliente: Cliente, request: Request, llm=Depends(obter_cliente_llm)):"
    - titulo: "Rode os testes e veja a API funcionando"
      descricao: "O pytest mostra qual teste falhou e por quê. Para usar a API pelo navegador, defina a variável CHAVE_API, rode fastapi dev solucao.py e abra http://127.0.0.1:8000/docs."
      comandos:
        - "cd desafios/producao/fastapi"
        - "pytest -v"
        - "fastapi dev solucao.py"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/fastapi"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de FastAPI"'
        - "git push -u origin desafio/fastapi"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Interface de programação", en: "API (application programming interface)" }
  - { pt: "Rota", en: "route, endpoint, path operation" }
  - { pt: "Método HTTP", en: "HTTP method (GET, POST, PUT, DELETE)" }
  - { pt: "Código de status", en: "status code" }
  - { pt: "Corpo da requisição", en: "request body" }
  - { pt: "Cabeçalho", en: "header" }
  - { pt: "Validação de dados", en: "data validation" }
  - { pt: "Esquema OpenAPI", en: "OpenAPI schema" }
  - { pt: "Injeção de dependências", en: "dependency injection" }
  - { pt: "Ciclo de vida", en: "lifespan" }
  - { pt: "Chave de API", en: "API key" }
  - { pt: "Servir um modelo", en: "model serving" }
  - { pt: "Desvio entre treino e produção", en: "training-serving skew" }
  - { pt: "Cliente de teste", en: "test client" }
---

## Do notebook ao serviço

Um modelo que só roda no seu notebook não ajuda ninguém. O sistema de atendimento, o aplicativo e o painel de outro time precisam pedir uma previsão e receber a resposta na hora, sem abrir Python. O jeito mais comum de oferecer isso é uma **API**: um serviço que recebe requisições pela rede, faz o trabalho e devolve o resultado em JSON.

O mesmo vale para uma aplicação de IA. O código que chama o Claude, monta o prompt e confere a resposta vira uma API, e qualquer sistema da empresa passa a usá-lo sem conhecer os detalhes.

O **FastAPI** é o framework de Python mais usado para isso. Você declara as rotas como funções comuns e os dados com tipos do Python, e ele cuida do resto: lê a requisição, valida os dados, converte a resposta para JSON e ainda gera a documentação.

## HTTP em poucas palavras

Uma API web conversa por **HTTP**. Cada requisição tem um **método**, um **caminho**, **cabeçalhos** e, às vezes, um **corpo**:

```text
POST /previsoes HTTP/1.1
Content-Type: application/json
X-API-Key: minha-chave

{"plano": "padrao", "canal": "organico", "idade": 29, ...}
```

Os métodos dizem a intenção: **GET** lê sem mudar nada, **POST** envia dados para processar ou criar algo, **PUT** e **PATCH** alteram, **DELETE** apaga. Uma previsão usa POST, porque os dados do cliente vão no corpo.

A resposta traz um **código de status**, que diz o que aconteceu antes mesmo de alguém ler o corpo:

| Código | Quer dizer                                       |
| ------ | ------------------------------------------------ |
| 200    | Deu certo                                        |
| 201    | Criado                                           |
| 401    | Sem autenticação: chave ausente ou errada        |
| 403    | Autenticado, mas sem permissão                   |
| 404    | Caminho ou recurso que não existe                |
| 422    | Dados inválidos                                  |
| 429    | Requisições demais                               |
| 500    | Erro inesperado no servidor                      |
| 503    | Indisponível agora, tente de novo                |

A regra geral: os 4xx são problemas de quem chamou, que precisa mudar o pedido; os 5xx são problemas do servidor.

## A primeira API

Com o FastAPI instalado (`pip install "fastapi[standard]"`), uma API cabe em poucas linhas:

```python
from fastapi import FastAPI

app = FastAPI(title="API de cancelamento")


@app.get("/saude")
def saude():
    return {"status": "ok"}


@app.get("/clientes/{cliente_id}")
def buscar_cliente(cliente_id: int, detalhado: bool = False):
    return {"cliente_id": cliente_id, "detalhado": detalhado}
```

O decorador diz o método e o caminho. Na segunda rota, `cliente_id` vem do caminho e `detalhado` vem da consulta, como em `/clientes/42?detalhado=true`. Os tipos não são enfeite: o FastAPI converte o texto da URL para `int` e `bool` e recusa `/clientes/abc` com um 422.

Para rodar, no terminal:

```bash
fastapi dev main.py
```

O servidor sobe em http://127.0.0.1:8000 e reinicia sozinho a cada mudança no código. Em http://127.0.0.1:8000/docs fica a **documentação interativa**, gerada a partir do código, onde dá para chamar cada rota pelo navegador. Em produção, o comando é `fastapi run`, sem o reinício automático.

## Validar a entrada com Pydantic

O corpo de uma requisição é descrito por um modelo do **Pydantic**, a mesma biblioteca que você usou para as saídas estruturadas do LLM:

```python
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Cliente(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plano: Literal["basico", "padrao", "premium"] = Field(description="Plano contratado.")
    idade: int = Field(ge=18, le=100, description="Idade, em anos.")
    valor_mensal: float = Field(gt=0, description="Valor da mensalidade, em reais.")
    usa_app: bool = Field(description="Se o cliente usa o aplicativo.")


@app.post("/previsoes")
def prever(cliente: Cliente):
    ...
```

Com isso, a função só roda com dados válidos. Uma idade de 10 anos, um plano "ouro" ou um campo faltando viram um **422**, com o campo e o motivo:

```json
{"detail": [{"type": "less_than_equal", "loc": ["body", "idade"],
             "msg": "Input should be less than or equal to 100",
             "input": 140, "ctx": {"le": 100}}]}
```

Três detalhes fazem diferença:

- **`Literal`** limita o campo a uma lista de valores. É o mesmo cuidado que você teve no text-to-SQL com os valores das categorias.
- **`extra="forbid"`** recusa campos desconhecidos. Sem isso, o Pydantic ignora o que não conhece, e um campo com outra grafia, como `usaApp`, some calado.
- **`description`** vai para a documentação, que é o que a pessoa do outro time vai ler para usar a sua API.

A resposta também pode ter um modelo, declarado com `response_model`. O FastAPI confere o que a rota devolve e mostra o formato no `/docs`.

## Servir um modelo de machine learning

Servir um modelo tem três cuidados próprios.

**Carregar uma vez.** Ler um modelo do disco é lento. O lugar certo é o **ciclo de vida** da API, uma função que roda quando o servidor sobe:

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request


@asynccontextmanager
async def ciclo_de_vida(app):
    app.state.modelo = carregar_modelo("modelo.json")  # roda uma vez, na subida
    yield  # daqui em diante, o servidor atende as requisições


app = FastAPI(lifespan=ciclo_de_vida)


@app.post("/previsoes")
def prever(cliente: Cliente, request: Request):
    probabilidade = request.app.state.modelo.prever([cliente.model_dump()])[0]
    return {"probabilidade_cancelamento": round(probabilidade, 4)}
```

**O mesmo pré-processamento do treino.** O modelo aprendeu com dados padronizados e categorias codificadas de um jeito. Se a API transformar de outro jeito, as previsões saem erradas sem nenhum erro aparecer: é o **desvio entre treino e produção**. A defesa é salvar o pré-processamento junto com o modelo, num pipeline do scikit-learn, como no módulo de machine learning.

**Um formato de arquivo que você controla.** O jeito mais comum de salvar um modelo do scikit-learn é o `joblib`. Ele é prático, mas tem duas armadilhas: o arquivo só abre com a mesma versão da biblioteca, e abrir um arquivo de origem desconhecida pode executar código. Fixe as versões no `requirements.txt` e só carregue arquivos que você mesmo gerou. No desafio, a regressão logística foi gravada em JSON, com as médias, os desvios e os coeficientes: qualquer código lê, e a previsão é uma conta simples.

Duas boas práticas completam o quadro: devolver a **versão do modelo** em toda resposta, para saber qual modelo fez cada previsão, e oferecer uma rota de **previsão em lote**, que atende muitos clientes numa requisição só, com um limite de tamanho.

## Dependências e chave de acesso

Uma API aberta na internet recebe requisições de qualquer um. O mínimo é exigir uma **chave de acesso** num cabeçalho. No FastAPI, isso é uma **dependência**: uma função que roda antes da rota e pode barrar a requisição.

```python
import os
import secrets

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader

chave_api = APIKeyHeader(name="X-API-Key", auto_error=False)


def exigir_chave(chave: str | None = Security(chave_api)):
    esperada = os.environ.get("CHAVE_API")
    if not esperada or not chave or not secrets.compare_digest(chave, esperada):
        raise HTTPException(status_code=401, detail="Chave da API ausente ou inválida.")


@app.post("/previsoes", dependencies=[Depends(exigir_chave)])
def prever(cliente: Cliente):
    ...
```

Repare em quatro escolhas. A chave certa vem de uma **variável de ambiente**, nunca do código, que vai para o Git. Sem a variável, nenhuma chave vale: o erro fica do lado seguro. O `secrets.compare_digest` compara em tempo constante, sem dar pistas de quantas letras acertaram. E o `APIKeyHeader` faz o `/docs` ganhar um botão Authorize, para testar com a chave.

A rota de saúde fica sem chave, porque é a plataforma de nuvem que vai chamá-la para saber se a API está de pé. Chaves de acesso servem para uma API entre sistemas; para pessoas, com login, o caminho é OAuth2, que o FastAPI também oferece. E tudo isso só protege de verdade com HTTPS, que a plataforma de nuvem cuida no próximo tópico.

As dependências servem para muito mais que segurança: qualquer coisa que a rota precisa receber pronta, como uma conexão com o banco ou o cliente de um LLM, pode chegar por uma dependência. E o que chega por dependência, o teste consegue trocar.

## Chamar um LLM de dentro da API

Uma rota que chama o Claude é uma rota como as outras, com dois cuidados a mais: o cliente do SDK chega por uma dependência e as falhas do serviço de fora viram uma resposta clara.

```python
import logging
from functools import lru_cache

import anthropic

registro = logging.getLogger("api")


@lru_cache
def obter_cliente_llm():
    return anthropic.Anthropic()  # criado uma vez; lê ANTHROPIC_API_KEY do ambiente


@app.post("/previsoes/explicacao", dependencies=[Depends(exigir_chave)])
def explicar(cliente: Cliente, llm=Depends(obter_cliente_llm)):
    try:
        resposta = llm.messages.create(
            model="claude-haiku-5-5",
            max_tokens=1024,
            system="Explique em até três frases por que o cliente tem esse risco.",
            messages=[{"role": "user", "content": str(cliente.model_dump())}],
        )
    except anthropic.APIError as erro:
        registro.warning("Falha ao chamar a API do Claude: %s", erro)
        raise HTTPException(status_code=503, detail="Explicação indisponível. Tente de novo em instantes.")
    return {"explicacao": "".join(b.text for b in resposta.content if b.type == "text")}
```

O SDK já tenta de novo, sozinho, em erros temporários como 429 e 529. Se mesmo assim falhar, a API devolve **503**, que diz a quem chamou que vale tentar mais tarde, e guarda o detalhe no registro do servidor, em vez de repassar uma mensagem interna. A previsão do modelo continua funcionando sem o LLM.

A escolha do modelo também é de produção: uma explicação curta não precisa do modelo mais caro. O Claude Haiku 5.5 custa uma fração do Opus 5.5, e cada requisição da API é uma chamada paga.

E uma pergunta que sempre aparece: `def` ou `async def`? O cliente `anthropic.Anthropic` espera a resposta da rede **bloqueando** a função. Com `def`, o FastAPI roda a função num conjunto de threads, e o servidor segue atendendo outras requisições. Uma chamada que bloqueia dentro de `async def` trava o servidor inteiro. Para usar `async def`, troque pelo `anthropic.AsyncAnthropic` e use `await`. Na dúvida, `def` é o seguro.

## Testar a API

O FastAPI traz um **cliente de teste**, que faz requisições à API sem subir um servidor:

```python
from fastapi.testclient import TestClient

from main import app, obter_cliente_llm


def test_entrada_invalida(monkeypatch):
    monkeypatch.setenv("CHAVE_API", "teste")  # a chave que a API espera, só durante o teste
    with TestClient(app) as api:  # o "with" roda o ciclo de vida
        resposta = api.post("/previsoes", json={"plano": "ouro"}, headers={"X-API-Key": "teste"})
    assert resposta.status_code == 422


def test_explicacao_sem_gastar(monkeypatch):
    monkeypatch.setenv("CHAVE_API", "teste")
    app.dependency_overrides[obter_cliente_llm] = lambda: ClienteGravado()
    try:
        with TestClient(app) as api:
            resposta = api.post("/previsoes/explicacao", json=CLIENTE, headers={"X-API-Key": "teste"})
    finally:
        app.dependency_overrides.clear()
    assert resposta.status_code == 200
```

O `app.dependency_overrides` troca uma dependência por outra durante o teste. É assim que o desafio testa a rota do LLM com um cliente gravado: sem chave, sem rede, sem custo e simulando até as falhas. Teste o caminho feliz e também os outros: entrada inválida, chave errada, lote grande demais, serviço de fora indisponível. São eles que aparecem às três da manhã.

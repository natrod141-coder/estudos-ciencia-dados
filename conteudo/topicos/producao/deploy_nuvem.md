---
titulo: "Publicar na nuvem"
modulo: producao
ordem: 3
horas: 8
estado: publicado
resumo: "Colocar a API no ar em um serviço de nuvem, com variáveis de ambiente e custo sob controle."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Onde rodar a API"
    tipo: leitura
    minutos: 8
  - id: a2
    titulo: "Publicar no Cloud Run"
    tipo: leitura
    minutos: 12
  - id: a3
    titulo: "Configuração e segredos"
    tipo: leitura
    minutos: 12
  - id: a4
    titulo: "Escala, partida a frio e custo"
    tipo: leitura
    minutos: 15
  - id: a5
    titulo: "Registros e saúde"
    tipo: leitura
    minutos: 10
  - id: a6
    titulo: "Lançar com segurança: revisões e reversão"
    tipo: leitura
    minutos: 10
  - id: a7
    titulo: "Publicar a cada push"
    tipo: leitura
    minutos: 10
  - id: a8
    titulo: "Vídeo de apoio: Cloud Run do zero"
    tipo: video
    minutos: 30
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "A API ficou uma hora sem acessos, e a primeira requisição depois disso demorou 4 segundos. As seguintes foram rápidas. O que aconteceu?"
    opcoes: ["A internet estava lenta", "Uma partida a frio: sem tráfego, o Cloud Run desligou as instâncias, e a primeira requisição esperou um contêiner novo subir e carregar o modelo", "O modelo de machine learning errou", "A chave da API expirou"]
    correta: 1
    explicacao: "Escalar a zero é o que deixa o serviço barato quando ninguém usa. O preço é a partida a frio. Manter uma instância mínima ligada evita a espera, e essa instância é cobrada mesmo parada, pela tarifa de ociosidade."
  - pergunta: "Onde a ANTHROPIC_API_KEY da API deve ficar no Cloud Run?"
    opcoes: ["No Dockerfile, com ENV", "No código, numa constante", "Num arquivo .env dentro da imagem", "No Secret Manager, ligada ao serviço com --set-secrets, que a entrega como variável de ambiente"]
    correta: 3
    explicacao: "O gerenciador de segredos guarda o valor com controle de acesso, histórico de versões e registro de quem leu. A imagem continua sem segredo nenhum, e trocar a chave não exige um build novo."
  - pergunta: "Por que conferir a configuração quando a API sobe, e não na primeira requisição que precisa dela?"
    opcoes: ["Porque uma revisão sem a configuração certa falha na subida, não recebe tráfego, e a versão anterior continua atendendo", "Porque deixa a API mais rápida", "Porque o Cloud Run exige", "Não faz diferença"]
    correta: 0
    explicacao: "Falhar cedo transforma um erro escondido, que apareceria para um usuário horas depois, num erro de publicação, visto na hora por quem publicou. Com o pydantic-settings, a configuração inválida levanta um erro claro, sem mostrar os valores."
  - pergunta: "Para que serve o --max-instances?"
    opcoes: ["Para a API responder mais rápido", "Para aumentar a cota gratuita", "Para limitar quantas instâncias podem rodar ao mesmo tempo, o que segura o custo num pico ou num ataque e protege os serviços que a API chama", "Para escolher a região"]
    correta: 2
    explicacao: "Sem limite, um pico de tráfego, legítimo ou não, vira centenas de instâncias e uma fatura grande. O limite também protege o que vem depois: o banco de dados, que aceita um número de conexões, e a API do LLM, que tem limite de requisições."
  - pergunta: "Um orçamento de 50 dólares por mês tem alerta em 100%. O que acontece quando o gasto chega a 50 dólares?"
    opcoes: ["O Google Cloud desliga o serviço", "A conta é bloqueada", "Nada muda na cobrança", "O alerta avisa por e-mail, mas o gasto continua; para limitar de verdade, use --max-instances, cotas ou uma automação que reage ao alerta"]
    correta: 3
    explicacao: "Alertas de orçamento avisam, não cortam. Configure alertas também pela previsão do mês, para saber antes de acontecer, e combine com limites técnicos, como o número máximo de instâncias."
  - pergunta: "Por que a API deve escrever os registros como uma linha de JSON com o campo severity, em vez de um print com texto livre?"
    opcoes: ["Porque JSON é mais bonito", "Porque a plataforma entende o nível de cada registro e os campos, e dá para filtrar, por exemplo, só os erros de uma rota", "Porque print não funciona em contêineres", "Porque ocupa menos espaço"]
    correta: 1
    explicacao: "O Cloud Run envia tudo o que a aplicação escreve na saída padrão para o Cloud Logging. Numa linha de JSON, severity vira o nível do registro e os outros campos ficam pesquisáveis. Texto livre vira uma linha só, sem estrutura."
  - pergunta: "Uma versão nova foi publicada e a taxa de erro subiu. Qual é o jeito mais rápido de voltar ao normal?"
    opcoes: ["Mandar todo o tráfego de volta para a revisão anterior, que continua existindo", "Corrigir o código e esperar o próximo build", "Apagar o serviço e publicar de novo", "Esperar o erro passar sozinho"]
    correta: 0
    explicacao: "Cada publicação cria uma revisão nova, e as antigas continuam lá, prontas. Mudar o tráfego leva segundos e não depende de build. Depois, com calma, você corrige o código."
  - pergunta: "Num lançamento gradual, você publicou a revisão nova sem tráfego e mandou 10% para ela. O que decide se ela recebe os outros 90%?"
    opcoes: ["A opinião de quem escreveu o código", "O horário do dia", "O tamanho da imagem", "As métricas da nova comparadas com as da atual, como taxa de erro e latência, com um número mínimo de requisições para a comparação valer"]
    correta: 3
    explicacao: "É a mesma lógica do teste A/B: comparar dois grupos com dados suficientes. Com poucas requisições, qualquer diferença pode ser acaso. Se a nova errar mais ou ficar mais lenta, o tráfego volta para a atual."
  - pergunta: "Como o GitHub Actions deve se autenticar no Google Cloud para publicar a API?"
    opcoes: ["Com a senha da sua conta Google num segredo do repositório", "Com a federação de identidade de carga de trabalho: o Google Cloud confia em tokens de curta duração que o GitHub emite para aquele repositório, sem chave guardada", "Com uma chave JSON de conta de serviço escrita no workflow", "Não precisa de autenticação"]
    correta: 1
    explicacao: "Uma chave JSON vale até alguém apagá-la e, se vazar, dá acesso de longe. Com a federação, cada execução recebe um token que vale por pouco tempo e só para o repositório autorizado. Não há segredo para vazar."
  - pergunta: "A API responde em 400 ms e cada instância atende até 80 requisições ao mesmo tempo. Se você mudar a concorrência para 1, o que acontece com o custo?"
    opcoes: ["Diminui, porque cada instância trabalha menos", "Não muda", "Aumenta: cada requisição passa a ocupar uma instância sozinha, e o tempo de instância cobrado se multiplica", "A API para de funcionar"]
    correta: 2
    explicacao: "Com concorrência alta, várias requisições dividem o mesmo tempo de instância. Concorrência 1 só faz sentido para código que não aguenta duas requisições ao mesmo tempo. No desafio, a mesma carga custa 98,98 dólares com uma requisição por instância e 18,18 com cinco."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "O time de atendimento vai usar a API de cancelamento todos os dias. Descreva como você a publicaria no Cloud Run: configuração e segredos, custo, observação e como lançar uma versão nova sem risco."
  rubrica:
    - "Descreve a publicação com a mesma imagem em todos os ambientes, a configuração por variáveis de ambiente, os segredos no Secret Manager e a configuração conferida na subida."
    - "Descreve o controle de custo: a estimativa antes de publicar, escala a zero ou instâncias mínimas conforme a necessidade, número máximo de instâncias, concorrência e alertas de orçamento, lembrando que alertas não cortam o gasto."
    - "Descreve registros estruturados sem segredos nem dados pessoais, o acompanhamento de erros e latência e o lançamento gradual com revisões, decisão por métricas e reversão pelo tráfego."
  modelo: "Eu publicaria a imagem do tópico de Docker no Cloud Run, na região de São Paulo, perto dos usuários, sabendo que ela custa mais que as regiões do nível 1. A configuração vem do ambiente: o nível de registro por variável comum e as chaves, CHAVE_API e ANTHROPIC_API_KEY, pelo Secret Manager, com --set-secrets. Na subida, uma classe do pydantic-settings confere tudo; se faltar algo, a revisão não sobe e a anterior continua atendendo. Antes de publicar, faria a conta do custo: com o volume do atendimento, de dia útil, escala a zero basta, aceitando uma partida a frio de manhã; se a espera incomodar, uma instância mínima custa uns 13 dólares por mês. Limitaria o máximo de instâncias, para um pico não virar uma fatura e para não estourar o limite da API do LLM, e criaria um orçamento com alertas em 50, 90 e 100%, real e previsto, sabendo que eles só avisam. A API escreve registros em JSON, com severity, rota, duração e versão do modelo, sem chaves e sem dados pessoais, e eu acompanharia a taxa de 5xx e a latência p95 com alertas. Para cada versão nova, publicaria sem tráfego e com uma etiqueta, testaria pelo endereço da etiqueta, mandaria 10% do tráfego e compararia erros e latência com a atual, com um mínimo de requisições; se piorar, o tráfego volta todo para a revisão anterior em segundos. Por fim, o GitHub Actions rodaria os testes e publicaria a cada push na main, autenticado pela federação de identidade, sem chave guardada."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Pronta para a nuvem"
  descricao: "Você vai escrever as peças que preparam a API para a nuvem: a configuração lida do ambiente com o pydantic-settings, que impede a subida com valores inválidos sem mostrar segredos; registros em JSON no formato do Cloud Logging; a estimativa do custo mensal no Cloud Run, com a cota gratuita, a concorrência e as instâncias mínimas; o acompanhamento do orçamento; e a decisão de promover ou reverter uma revisão nova. Nada é publicado: o desafio roda no seu computador, sem conta na nuvem."
  pasta: "desafios/producao/deploy_nuvem"
  testes: 15
  tempo: "2 h 30 min"
  ferramentas: "VS Code, Python 3.11 ou superior, pydantic-settings e pytest"
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
      descricao: "Abra o terminal do VS Code com Ctrl+` (acento grave). Depois use Ctrl+Shift+P, Python: Select Interpreter, e escolha o .venv. O pydantic-settings vem junto com o FastAPI."
      comandos:
        - "# Linux ou macOS"
        - "python3 -m venv .venv"
        - "source .venv/bin/activate"
        - "# Windows (PowerShell)"
        - "python -m venv .venv"
        - '.venv\Scripts\Activate.ps1'
        - "pip install -r desafios/requirements.txt"
    - titulo: "Leia o enunciado e os preços"
      descricao: "Abra desafios/producao/deploy_nuvem/README.md. Os preços do Cloud Run estão em data/precos_cloud_run.json, com a data em que foram conferidos."
    - titulo: "Complete o solucao.py"
      descricao: "Siga a ordem do arquivo. Cada classe e cada função tem uma docstring com o que fazer. Não altere a pasta tests."
      codigo: true
      comandos:
        - "class Configuracao(BaseSettings):"
        - "def linha_de_log(nivel, mensagem, momento, **campos):"
        - "def custo_mensal(uso, precos):"
        - "def acompanhar_orcamento(gastos_diarios, orcamento, dias_no_mes, limites=(0.5, 0.9, 1.0)):"
        - "def decidir_lancamento(atual, nova, minimo_de_requisicoes=500, tolerancia_erro=0.01, fator_latencia=1.2):"
    - titulo: "Rode os testes a cada parte pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/producao/deploy_nuvem"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/deploy_nuvem"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de publicar na nuvem"'
        - "git push -u origin desafio/deploy_nuvem"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Contêiner sem servidor", en: "serverless container" }
  - { pt: "Revisão", en: "revision" }
  - { pt: "Escala a zero", en: "scale to zero" }
  - { pt: "Partida a frio", en: "cold start" }
  - { pt: "Instâncias mínimas e máximas", en: "min instances, max instances" }
  - { pt: "Concorrência", en: "concurrency" }
  - { pt: "Gerenciador de segredos", en: "secret manager" }
  - { pt: "Registro estruturado", en: "structured logging" }
  - { pt: "Verificação de saúde", en: "health check, startup probe" }
  - { pt: "Lançamento gradual", en: "canary release, gradual rollout" }
  - { pt: "Divisão de tráfego", en: "traffic splitting" }
  - { pt: "Reversão", en: "rollback" }
  - { pt: "Orçamento e alertas", en: "budget, budget alerts" }
  - { pt: "Federação de identidade", en: "workload identity federation" }
  - { pt: "Integração e entrega contínuas", en: "CI/CD" }
---

## Onde rodar a API

A API tem imagem Docker. Agora ela precisa de um lugar na internet, com HTTPS, que fique de pé sem você e cresça quando o uso crescer. As opções se dividem em quatro grupos:

| Tipo                    | Exemplos                                   | Quando faz sentido                  |
| ----------------------- | ------------------------------------------ | ----------------------------------- |
| Contêiner sem servidor  | Google Cloud Run, Azure Container Apps, AWS ECS com Fargate | APIs com uso variável; paga pelo uso |
| Plataforma simplificada | Render, Railway, Fly.io, Hugging Face Spaces | Protótipos e portfólio            |
| Máquina virtual         | Compute Engine, Amazon EC2                 | Controle total; você cuida de tudo  |
| Kubernetes              | GKE, Amazon EKS, Azure AKS                 | Muitos serviços e um time de plataforma |

Para uma API de dados, o **contêiner sem servidor** costuma ser o melhor ponto de partida: você entrega a imagem, e a plataforma cuida de servidores, HTTPS, escala e atualizações. Este tópico usa o **Cloud Run**, do Google Cloud, a mesma nuvem do BigQuery. Ele roda qualquer contêiner, desliga tudo quando não há uso e tem uma cota gratuita mensal. As ideias valem para as outras plataformas, com outros nomes. O próprio time do FastAPI tem um serviço, o FastAPI Cloud, em beta pública desde 2026, que publica com o comando `fastapi deploy`.

## Publicar no Cloud Run

Você precisa de uma conta no Google Cloud com faturamento ativo, mesmo para ficar na cota gratuita, e da **Google Cloud CLI**, o comando `gcloud`. Depois de `gcloud init`, que escolhe a conta e o projeto, ative os serviços usados e publique, de dentro da pasta da API:

```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com

gcloud run deploy api-cancelamento \
  --source . \
  --region southamerica-east1 \
  --allow-unauthenticated \
  --memory 512Mi --cpu 1 \
  --max-instances 3
```

O `--source .` envia a pasta para o Google Cloud, que constrói a imagem com o seu Dockerfile, guarda no Artifact Registry e cria uma **revisão** do serviço. Em poucos minutos, a API está no ar, com HTTPS, num endereço terminado em `run.app`. Para mandar a imagem já pronta, use `--image` no lugar de `--source`.

O `--allow-unauthenticated` deixa qualquer pessoa na internet chamar o endereço. Para a API de cancelamento, tudo bem: ela exige a própria chave em cada rota de previsão, e a rota de saúde não mostra nada sensível. Para um serviço que só outros serviços da empresa chamam, o certo é o contrário, `--no-allow-unauthenticated`, e liberar o acesso por permissões do Google Cloud.

A **região** pesa em três coisas: a distância até os usuários, o preço e onde os dados ficam. São Paulo, `southamerica-east1`, deixa a API perto de quem está no Brasil, mas está no nível 2 de preço do Cloud Run, mais caro que regiões do nível 1, como Iowa, `us-central1`.

## Configuração e segredos

A mesma imagem roda no seu computador, no ambiente de testes e em produção. O que muda entre eles é a **configuração**, que chega por variáveis de ambiente. Valores comuns vão direto:

```bash
gcloud run deploy api-cancelamento --source . --region southamerica-east1 \
  --set-env-vars NIVEL_LOG=INFO
```

Segredos, não. Eles ficam no **Secret Manager**, que guarda o valor com controle de acesso, versões e registro de quem leu, e chegam à API como variáveis de ambiente:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32), end='')" | gcloud secrets create chave-api --data-file=-

gcloud run deploy api-cancelamento --source . --region southamerica-east1 \
  --set-secrets=CHAVE_API=chave-api:latest,ANTHROPIC_API_KEY=anthropic-api-key:latest
```

O primeiro comando gera uma chave aleatória e guarda direto no segredo, sem passar pela tela; crie do mesmo jeito o segredo `anthropic-api-key`, com a sua chave da Anthropic. Para entregar a chave da API a quem vai chamá-la, leia com `gcloud secrets versions access latest --secret=chave-api`. A conta de serviço que roda a API precisa do papel de leitura de segredos (Secret Manager Secret Accessor). Trocar uma chave vira criar uma versão nova do segredo, sem build.

Do lado da API, a configuração deve ser conferida **na subida**, e não na primeira requisição que precisa dela. O FastAPI recomenda o `pydantic-settings`, que lê as variáveis de ambiente para dentro de uma classe e valida como o Pydantic valida o corpo de uma requisição:

```python
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracao(BaseSettings):
    model_config = SettingsConfigDict(hide_input_in_errors=True)

    chave_api: SecretStr = Field(min_length=16)  # lida de CHAVE_API
    anthropic_api_key: SecretStr                 # lida de ANTHROPIC_API_KEY
    port: int = 8080                             # lida de PORT, que o Cloud Run preenche
```

No ciclo de vida da API, `Configuracao()` roda antes de qualquer requisição. Se faltar a chave ou a porta não for um número, a API não sobe. Parece ruim, mas é o melhor que pode acontecer: o Cloud Run percebe que a revisão nova não subiu, não manda tráfego para ela, e a anterior continua atendendo. O erro aparece para quem publicou, na hora, e não para um usuário, horas depois.

Dois detalhes de segurança: o `SecretStr` mostra `**********` quando alguém imprime a configuração, e o `hide_input_in_errors` tira da mensagem de erro o valor recebido, que pode ser justamente uma chave escrita errado.

## Escala, partida a frio e custo

O Cloud Run sobe instâncias da API conforme as requisições chegam e desliga todas depois de um tempo sem uso. É a **escala a zero**: sem tráfego, sem custo de computação. O preço disso é a **partida a frio**: a primeira requisição depois de um tempo parado espera um contêiner subir, o Python iniciar e o modelo carregar. Por padrão, o Cloud Run dá CPU extra na subida para encurtar essa espera. Se nem assim for aceitável, `--min-instances 1` mantém uma instância sempre ligada, cobrada pela tarifa de ociosidade enquanto não atende.

Três controles definem o custo:

- **`--max-instances`** limita quantas instâncias rodam ao mesmo tempo. Segura a fatura num pico, legítimo ou não, e protege o que a API chama: o banco, que aceita um número de conexões, e a API do LLM, que tem limite de requisições.
- **`--concurrency`**, por padrão até 80, diz quantas requisições uma instância atende ao mesmo tempo. Requisições simultâneas dividem o mesmo tempo de instância, e o custo cai.
- **`--memory` e `--cpu`**, o tamanho de cada instância.

Com a cobrança por requisição, você paga a CPU e a memória enquanto a instância atende, mais as requisições. Em novembro de 2026, nas regiões do nível 1: 0,000024 dólar por vCPU-segundo, 0,0000025 por GiB-segundo e 0,40 por milhão de requisições, com uma cota gratuita mensal de 180 mil vCPU-segundos, 360 mil GiB-segundos e 2 milhões de requisições, somada por conta de faturamento. Na estimativa simplificada do desafio, com 1 vCPU e 512 MiB:

| Situação                                               | Custo por mês |
| ------------------------------------------------------ | ------------- |
| 300 mil requisições de 200 ms                          | 0 (cota gratuita) |
| 10 milhões de requisições de 400 ms, uma por instância | US$ 98,98     |
| As mesmas, cinco por instância                         | US$ 18,18     |
| Uma instância mínima, 1 vCPU e 1 GiB, quase sem uso    | US$ 12,66     |

E não esqueça o LLM: numa rota que chama o Claude Haiku 5.5, a 0,10 dólar por milhão de tokens de entrada e 0,50 por milhão de saída, uma explicação com 180 tokens de entrada e 60 de saída custa uns 0,00005 dólar. Um milhão de explicações: perto de 50 dólares, mais que a própria hospedagem.

Por fim, crie um **orçamento** no faturamento do Google Cloud, com alertas em 50%, 90% e 100%, tanto do gasto real quanto do previsto para o mês. Atenção: os alertas **avisam, não cortam**. Para limitar de verdade, valem o `--max-instances`, as cotas e uma automação que reage ao alerta.

## Registros e saúde

Na nuvem, ninguém olha o terminal. Tudo o que a API escreve na saída padrão vai para o **Cloud Logging**, e o formato importa. Uma linha de JSON com os campos `severity` e `message` vira um **registro estruturado**: a plataforma entende o nível, e os outros campos ficam pesquisáveis.

```json
{"severity": "WARNING", "message": "Falha ao chamar a API do Claude", "time": "2026-11-09T14:30:00.250Z", "rota": "/previsoes/explicacao", "revisao": "api-cancelamento-00007-xyz"}
```

Com o módulo `logging` do Python, basta um formatador:

```python
import json
import logging
import sys


class FormatoJson(logging.Formatter):
    def format(self, registro):
        return json.dumps(
            {"severity": registro.levelname, "message": registro.getMessage(), "origem": registro.name},
            ensure_ascii=False,
        )


saida = logging.StreamHandler(sys.stdout)
saida.setFormatter(FormatoJson())
logging.basicConfig(level=logging.INFO, handlers=[saida])
```

Registre o que ajuda a investigar: a rota, a duração, o código de status, a versão do modelo e a revisão, que o Cloud Run informa na variável `K_REVISION`. E nunca registre segredos nem dados pessoais: chaves, CPF, e-mail ou o corpo inteiro das requisições. Registro também é dado, e a LGPD vale para ele.

Para a **saúde**, o Cloud Run confere se o contêiner subiu antes de mandar tráfego. Por padrão, ele só testa se a porta abriu; uma verificação de subida por HTTP, apontada para a rota `/saude`, confirma que a API está mesmo pronta. No painel do serviço ficam as métricas que importam no dia a dia: requisições por segundo, latência (p50, p95 e p99), respostas com erro 5xx e número de instâncias. Crie alertas para a taxa de erro e para a latência.

## Lançar com segurança: revisões e reversão

Cada publicação cria uma **revisão** nova e imutável, como `api-cancelamento-00007-xyz`, e as anteriores continuam lá, prontas para receber tráfego de novo. Isso permite um **lançamento gradual**:

```bash
# publica a revisão nova sem tráfego, com uma etiqueta que ganha um endereço próprio
gcloud run deploy api-cancelamento --source . --region southamerica-east1 --no-traffic --tag candidata

# manda 10% do tráfego para ela
gcloud run services update-traffic api-cancelamento --region southamerica-east1 --to-tags candidata=10

# se as métricas forem boas, tudo para a revisão mais nova
gcloud run services update-traffic api-cancelamento --region southamerica-east1 --to-latest

# se piorarem, tudo de volta para a revisão anterior
gcloud run services update-traffic api-cancelamento --region southamerica-east1 --to-revisions api-cancelamento-00006-abc=100
```

Antes de mandar qualquer tráfego, dá para testar a revisão nova pelo endereço da etiqueta. Com os 10%, compare as duas revisões, com um número mínimo de requisições para a comparação valer, como num teste A/B. Se a taxa de erro ou a latência piorar, o tráfego volta para a revisão anterior em segundos, sem build. No desafio, você vai escrever essa decisão.

## Publicar a cada push

Publicar na mão funciona, mas depende de alguém lembrar de rodar os testes antes. Com o **GitHub Actions**, cada push na `main` roda os testes e, se passarem, publica:

```yaml
name: Publicar a API

on:
  push:
    branches: [main]

jobs:
  publicar:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write  # permite pedir um token de identidade ao GitHub
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: "3.14"
      - run: pip install -r requirements.txt pytest && pytest
      - uses: google-github-actions/auth@v3
        with:
          workload_identity_provider: ${{ vars.PROVEDOR_DE_IDENTIDADE }}
          service_account: ${{ vars.CONTA_DE_SERVICO }}
      - uses: google-github-actions/deploy-cloudrun@v3
        with:
          service: api-cancelamento
          region: southamerica-east1
          source: .
```

O detalhe importante é a autenticação. O jeito antigo era criar uma chave JSON de conta de serviço e guardar nos segredos do repositório: uma chave que vale até alguém apagá-la e que, se vazar, dá acesso de qualquer lugar. O jeito recomendado é a **federação de identidade de carga de trabalho**: o Google Cloud passa a confiar nos tokens que o GitHub emite para aquele repositório, e cada execução recebe uma credencial que vale por pouco tempo. Não há chave para guardar nem para vazar. A configuração, feita uma vez, está na documentação da action `google-github-actions/auth`.

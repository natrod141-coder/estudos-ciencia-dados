---
titulo: "Docker"
modulo: producao
ordem: 2
horas: 8
estado: publicado
resumo: "Empacotar a aplicação para rodar igual em qualquer máquina."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Na minha máquina funciona"
    tipo: leitura
    minutos: 8
  - id: a2
    titulo: "Imagem, contêiner e registro"
    tipo: leitura
    minutos: 10
  - id: a3
    titulo: "Escrever um Dockerfile"
    tipo: leitura
    minutos: 15
  - id: a4
    titulo: "Camadas e cache: a ordem importa"
    tipo: leitura
    minutos: 10
  - id: a5
    titulo: "Imagens menores e mais seguras"
    tipo: leitura
    minutos: 15
  - id: a6
    titulo: "Rodar e investigar contêineres"
    tipo: leitura
    minutos: 12
  - id: a7
    titulo: "Vários serviços com o Docker Compose"
    tipo: leitura
    minutos: 10
  - id: a8
    titulo: "Vídeo de apoio: Docker para quem trabalha com dados"
    tipo: video
    minutos: 40
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Qual é a diferença entre uma imagem e um contêiner?"
    opcoes: ["São a mesma coisa", "A imagem roda e o contêiner fica guardado", "A imagem é o pacote pronto e imutável; o contêiner é uma execução dessa imagem, e uma imagem pode ter vários contêineres", "O contêiner é a versão da imagem na nuvem"]
    correta: 2
    explicacao: "A imagem é como um programa instalado, pronto e sem mudanças. O contêiner é esse programa rodando, com o seu próprio processo e os seus próprios arquivos temporários. Da mesma imagem saem quantos contêineres você precisar."
  - pergunta: "Por que copiar o requirements.txt e instalar as dependências antes de copiar o resto do código?"
    opcoes: ["Porque o código muda muito mais que as dependências: assim, uma mudança no código reaproveita a camada da instalação, que é a mais demorada", "Porque o pip não acha o código se ele já estiver na imagem", "Porque a imagem fica mais segura", "Não faz diferença"]
    correta: 0
    explicacao: "Cada instrução vira uma camada, guardada em cache. Quando um arquivo copiado muda, o Docker refaz a partir daquela cópia. Com o código copiado depois da instalação, mudar uma linha refaz só a cópia do código, em segundos."
  - pergunta: "Por que colocar o arquivo .env no .dockerignore?"
    opcoes: ["Para a imagem ficar mais rápida", "Porque o Docker não lê arquivos .env", "Não precisa: o .env não é copiado", "Para os segredos que estão nele não irem parar dentro da imagem, onde qualquer pessoa com acesso a ela consegue ler"]
    correta: 3
    explicacao: "Um COPY . . leva tudo o que está na pasta, inclusive o .env com as chaves. Uma imagem é distribuída, guardada em registros e reaproveitada: o segredo vai junto. O .dockerignore tira o arquivo do contexto do build."
  - pergunta: "O Dockerfile tem ENV ANTHROPIC_API_KEY=sk-ant-... Qual é o problema?"
    opcoes: ["Nenhum, desde que o repositório seja privado", "A chave fica gravada na imagem e aparece para quem rodar docker history ou docker inspect; ela deve ser passada só na hora de rodar", "O Docker não aceita variáveis com números", "A chave expira mais rápido"]
    correta: 1
    explicacao: "ENV e ARG ficam registrados na configuração e no histórico da imagem. O certo é passar o segredo quando o contêiner roda, com -e ou --env-file no seu computador e com um gerenciador de segredos na nuvem. O docker build --check avisa desse erro."
  - pergunta: "Por que preferir CMD [\"fastapi\", \"run\", \"app/main.py\"], a forma exec, a CMD fastapi run app/main.py?"
    opcoes: ["Porque é mais curta", "Porque a forma shell não funciona com Python", "Porque, na forma exec, o servidor é o processo principal do contêiner e recebe o aviso de desligamento, podendo encerrar com calma", "Por nenhum motivo técnico"]
    correta: 2
    explicacao: "Na forma shell, quem roda é um /bin/sh, que nem sempre repassa o sinal SIGTERM. Aí o servidor é morto à força, sem terminar as requisições em andamento nem rodar o fim do ciclo de vida. A documentação do FastAPI recomenda a forma exec."
  - pergunta: "O que pode dar errado com FROM python:latest?"
    opcoes: ["A imagem fica maior", "Nada, é o recomendado", "O Docker não aceita latest", "O latest muda sem aviso: um build de amanhã pode vir com outra versão do Python e quebrar o que funcionava hoje"]
    correta: 3
    explicacao: "Uma imagem reproduzível depende de versões fixas, tanto da imagem base quanto das bibliotecas no requirements.txt. Com python:3.14-slim, a versão do Python só muda quando você decidir, e as correções da 3.14 chegam quando você baixa a base de novo, com docker build --pull."
  - pergunta: "A API, dentro do contêiner, escuta em 127.0.0.1:8080. Você roda com -p 8080:8080 e não consegue acessar. Por quê?"
    opcoes: ["Porque 127.0.0.1, dentro do contêiner, é o próprio contêiner; o servidor precisa escutar em 0.0.0.0 para aceitar conexões de fora", "Porque a porta 8080 é proibida", "Porque falta o EXPOSE", "Porque o Docker bloqueia APIs"]
    correta: 0
    explicacao: "Cada contêiner tem a sua própria rede. Escutando em 127.0.0.1, o servidor só aceita conexões vindas de dentro dele. O fastapi run já escuta em 0.0.0.0; o fastapi dev, pensado para o seu computador, escuta em 127.0.0.1."
  - pergunta: "O que quer dizer -p 8000:8080 no docker run?"
    opcoes: ["Que o contêiner usa 8000 MB de memória", "Que a porta 8000 do seu computador leva à porta 8080 do contêiner", "Que a porta 8080 do seu computador leva à porta 8000 do contêiner", "Que o contêiner roda por 8000 segundos"]
    correta: 1
    explicacao: "A ordem é sempre porta do computador, dois-pontos, porta do contêiner. Com -p 8000:8080, você acessa http://localhost:8000 e a requisição chega à API, que escuta na 8080 lá dentro."
  - pergunta: "Por que rodar a aplicação com um usuário que não seja o root?"
    opcoes: ["Porque o root deixa a aplicação mais lenta", "Porque o Docker exige", "Para limitar o estrago se alguém explorar uma falha da aplicação: sem privilégios, o invasor não altera o sistema do contêiner", "Para economizar memória"]
    correta: 2
    explicacao: "É o mesmo princípio do privilégio mínimo do agente de dados. A API não precisa instalar pacotes nem mexer no sistema para responder previsões; quem tomar o controle dela herda só o que ela pode fazer."
  - pergunta: "A API grava um arquivo de registro dentro do contêiner. O que acontece com ele quando o contêiner é removido?"
    opcoes: ["Some junto com o contêiner; para guardar dados, use um volume, um banco ou um serviço de armazenamento", "Vai para a imagem automaticamente", "Fica guardado para sempre no Docker Hub", "É enviado por e-mail"]
    correta: 0
    explicacao: "Os arquivos criados dentro de um contêiner são temporários. Volumes guardam dados entre execuções no seu computador; na nuvem, o certo é um banco ou um serviço de armazenamento. No Cloud Run, o sistema de arquivos fica até na memória."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "A API de cancelamento funciona no computador de quem a escreveu, mas não no seu: dá erro de versão de biblioteca. Explique como o Docker resolve esse problema e descreva o Dockerfile que você escreveria para a API, justificando cada escolha."
  rubrica:
    - "Explica que a imagem empacota sistema, Python, dependências com versões fixas e código, e que o contêiner roda igual em qualquer máquina com Docker."
    - "Descreve um Dockerfile com imagem base slim e versão fixa, dependências instaladas antes do código por causa do cache, pip sem cache, só os arquivos necessários e .dockerignore."
    - "Inclui segurança e execução: usuário sem privilégios, nenhum segredo na imagem, segredos passados na execução, CMD na forma exec com o servidor escutando em 0.0.0.0 na porta certa."
  modelo: "O problema é que cada máquina tem o seu Python e as suas bibliotecas. Uma imagem Docker leva junto tudo de que a API precisa: o sistema base, o Python, as dependências com versões fixas e o código. Qualquer máquina com Docker roda a mesma imagem do mesmo jeito, inclusive a nuvem. O Dockerfile partiria de python:3.14-slim, com a versão fixa, para o Python não mudar sem aviso, e na variante slim, bem menor que a completa. Eu copiaria primeiro só o requirements.txt, com as versões fixas, e instalaria com pip install --no-cache-dir; só depois copiaria a pasta app. Assim, mudar o código não refaz a instalação, que é a etapa mais demorada. O .dockerignore deixaria de fora .env, .git, .venv, __pycache__ e os testes, para a imagem ficar menor e nenhum segredo entrar por acidente. Criaria um usuário sem privilégios e terminaria com USER, para limitar o estrago de uma possível invasão. Por fim, EXPOSE 8080 e CMD na forma exec com fastapi run na porta 8080, que escuta em 0.0.0.0 e recebe o aviso de desligamento. As chaves, como CHAVE_API, entram só na hora de rodar, com -e ou --env-file, e nunca no Dockerfile. Antes de publicar, rodaria docker build --check."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Uma imagem Docker para a API"
  descricao: "Você vai escrever um pequeno verificador de Dockerfile, que lê as instruções, aponta os erros mais comuns, entende o .dockerignore e descobre qual etapa do build é refeita quando um arquivo muda. Depois, vai escrever o Dockerfile e o .dockerignore da API de cancelamento, conferidos pelo seu verificador. Os testes não precisam do Docker; com ele instalado, você constrói a imagem e roda a API num contêiner."
  pasta: "desafios/producao/docker"
  testes: 10
  tempo: "2 h 30 min"
  ferramentas: "VS Code, Python 3.11 ou superior, pytest e, para construir a imagem, Docker Desktop"
  entrega: "Pull Request no GitHub"
  passos:
    - titulo: "Clone o repositório"
      descricao: "Só na primeira vez. Se já clonou, pule para o passo 2."
      comandos:
        - "git clone https://github.com/[seu_usuario]/[repositorio].git"
        - "cd [repositorio]"
    - titulo: "Abra o repositório no VS Code"
      descricao: "Se o VS Code oferecer Reopen in Container, aceite: o ambiente já vem pronto e você pode pular o passo 3. Esse contêiner de desenvolvimento também é Docker."
      comandos:
        - "code ."
    - titulo: "Crie e ative o ambiente virtual"
      descricao: "Abra o terminal do VS Code com Ctrl+` (acento grave). Depois use Ctrl+Shift+P, Python: Select Interpreter, e escolha o .venv."
      comandos:
        - "# Linux ou macOS"
        - "python3 -m venv .venv"
        - "source .venv/bin/activate"
        - "# Windows (PowerShell)"
        - "python -m venv .venv"
        - '.venv\Scripts\Activate.ps1'
        - "pip install -r desafios/requirements.txt"
    - titulo: "Leia o enunciado"
      descricao: "Abra desafios/producao/docker/README.md. A API pronta está na pasta app."
    - titulo: "Implemente o verificador e escreva o Dockerfile"
      descricao: "As funções estão em solucao.py, cada uma com uma docstring do que fazer. O Dockerfile e o .dockerignore ficam na mesma pasta. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def ler_instrucoes(texto):"
        - "def problemas(instrucoes):"
        - "def ignorado(caminho, padroes):"
        - "def primeira_etapa_refeita(instrucoes, alterados, padroes_ignorados=()):"
    - titulo: "Rode os testes e construa a imagem"
      descricao: "Os testes não precisam do Docker. Com o Docker Desktop aberto, construa a imagem e rode a API em http://localhost:8080/docs."
      comandos:
        - "cd desafios/producao/docker"
        - "pytest -v"
        - "docker build -t api-cancelamento ."
        - "docker run --rm -p 8080:8080 -e CHAVE_API=minha-chave-local api-cancelamento"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/docker"
        - "git add solucao.py Dockerfile .dockerignore"
        - 'git commit -m "Resolve o desafio de Docker"'
        - "git push -u origin desafio/docker"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Imagem", en: "image" }
  - { pt: "Contêiner", en: "container" }
  - { pt: "Registro de imagens", en: "container registry" }
  - { pt: "Camada", en: "layer" }
  - { pt: "Cache do build", en: "build cache" }
  - { pt: "Contexto do build", en: "build context" }
  - { pt: "Imagem base", en: "base image" }
  - { pt: "Etiqueta", en: "tag" }
  - { pt: "Forma exec e forma shell", en: "exec form, shell form" }
  - { pt: "Mapeamento de portas", en: "port mapping" }
  - { pt: "Volume", en: "volume" }
  - { pt: "Build em várias etapas", en: "multi-stage build" }
  - { pt: "Orquestração de serviços", en: "Docker Compose" }
---

## Na minha máquina funciona

A API de cancelamento roda no seu computador. No do colega, dá erro: ele tem outra versão do Python, o pandas é mais novo, falta uma biblioteca do sistema. Na nuvem, é pior: o servidor não tem nada do que você instalou ao longo dos meses.

O **Docker** resolve isso empacotando a aplicação com tudo de que ela precisa: o sistema base, o Python, as bibliotecas com as versões certas e o código. O pacote roda igual em qualquer máquina com Docker, seja o seu notebook, o servidor da empresa ou um serviço de nuvem. Você já usa isso: o "Reopen in Container" dos desafios abre o repositório dentro de um contêiner Docker.

Para usar no seu computador, instale o **Docker Desktop**, gratuito para uso pessoal e estudo. No Windows, ele roda sobre o WSL 2.

## Imagem, contêiner e registro

Três palavras organizam tudo:

- A **imagem** é o pacote pronto: um sistema de arquivos com tudo instalado e a instrução de como iniciar. Ela não muda depois de construída.
- O **contêiner** é uma imagem rodando, com o seu próprio processo, a sua rede e os seus arquivos temporários. Da mesma imagem saem quantos contêineres você quiser.
- O **registro** guarda e distribui imagens, como o GitHub faz com código. O Docker Hub é o registro público, de onde vem a imagem oficial do Python; na nuvem, cada provedor tem o seu, como o Artifact Registry do Google Cloud.

Uma imagem é identificada por nome e **etiqueta**: em `python:3.14-slim`, `python` é o nome e `3.14-slim` é a etiqueta, que diz a versão do Python e a variante.

Diferente de uma máquina virtual, um contêiner não carrega um sistema operacional inteiro: ele usa o núcleo do sistema da máquina e isola só o resto. Por isso sobe em segundos e ocupa pouco.

## Escrever um Dockerfile

A receita de uma imagem é o **Dockerfile**, um arquivo de texto com uma instrução por linha. O da API de cancelamento:

```dockerfile
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

RUN useradd --create-home api
USER api

EXPOSE 8080
CMD ["fastapi", "run", "app/main.py", "--port", "8080"]
```

Linha a linha:

- **`FROM`** escolhe a imagem base: a oficial do Python, com a versão fixa e na variante **slim**, que traz só o essencial do Debian.
- **`ENV`** define variáveis de ambiente. Estas duas são de Python: sem arquivos `.pyc` e com a saída sem buffer, para os registros aparecerem na hora.
- **`WORKDIR`** é a pasta de trabalho dentro da imagem.
- **`COPY`** leva arquivos do seu computador para a imagem. **`RUN`** executa um comando durante a construção, como instalar as dependências.
- **`USER`** troca o usuário que roda a aplicação.
- **`EXPOSE`** documenta a porta em que a aplicação escuta.
- **`CMD`** é o comando que roda quando o contêiner inicia.

Para construir a imagem e rodar um contêiner, dentro da pasta do Dockerfile:

```bash
docker build -t api-cancelamento .
docker run --rm -p 8080:8080 -e CHAVE_API=minha-chave-local api-cancelamento
```

O ponto no fim do `docker build` é o **contexto**: a pasta cujos arquivos o `COPY` pode usar. O `-p 8080:8080` liga a porta 8080 do seu computador à 8080 do contêiner, na ordem computador:contêiner, e o `-e` passa uma variável de ambiente. A API fica em http://localhost:8080/docs.

## Camadas e cache: a ordem importa

Cada instrução do Dockerfile vira uma **camada**, e o Docker guarda as camadas em cache. No próximo build, ele reaproveita tudo o que não mudou e refaz a partir da primeira instrução afetada. Para um `COPY`, "afetada" quer dizer que algum arquivo copiado mudou.

Daí a ordem do Dockerfile acima. As dependências mudam pouco, e instalar é a etapa mais demorada. O código muda toda hora. Com o `requirements.txt` copiado e instalado antes do código, mudar uma linha da API refaz só a cópia da pasta `app`:

```text
#7 [3/6] COPY requirements.txt .
#7 CACHED
#8 [4/6] RUN pip install --no-cache-dir -r requirements.txt
#8 CACHED
#9 [5/6] COPY app ./app
#9 DONE 0.0s
```

Com um `COPY . .` antes do `pip install`, qualquer mudança no código invalida a cópia, e a instalação inteira roda de novo a cada build. No desafio, você vai escrever a função que descobre qual etapa o Docker refaz para cada arquivo alterado.

## Imagens menores e mais seguras

Uma imagem boa é pequena, reproduzível e não carrega nada que não deveria:

**Versões fixas.** `python:latest` muda sem aviso: o build de amanhã pode vir com outro Python. Fixe a imagem base e fixe as bibliotecas no `requirements.txt`, como `fastapi[standard]==0.162.2`.

**Variante slim.** Para baixar, a `python:3.14-slim` tem uns 44 MB; a completa, a `python:3.14`, passa de 400 MB, com compiladores e ferramentas que a API não usa. Imagem menor sobe mais rápido na nuvem e tem menos programas com falhas de segurança.

**Sem cache do pip.** O `--no-cache-dir` evita guardar na imagem os pacotes baixados, que já foram instalados.

**Um `.dockerignore`.** Ele diz o que fica fora do contexto do build:

```text
.git
.venv
.env
**/__pycache__
tests
*.md
```

Sem ele, um `COPY . .` leva o `.git`, o ambiente virtual e, pior, o `.env` com as suas chaves. As regras parecem as do `.gitignore`, com uma diferença: `*.md` vale só na raiz, e `**/` é o jeito de dizer "em qualquer pasta".

**Nenhum segredo na imagem.** `ENV` e `ARG` ficam gravados na configuração da imagem, e qualquer pessoa com acesso a ela lê com `docker history` ou `docker inspect`. Segredos entram só na hora de rodar: com `-e` ou `--env-file .env` no seu computador e com um gerenciador de segredos na nuvem, como você vai ver no próximo tópico.

**Um usuário sem privilégios.** Por padrão, o contêiner roda como root. Se alguém explorar uma falha da API, herda esse poder. Com `USER api`, a aplicação só faz o que precisa.

**`CMD` na forma exec.** Com a lista entre colchetes, o servidor é o processo principal do contêiner e recebe o aviso de desligamento (o sinal SIGTERM), podendo terminar as requisições em andamento. Na forma shell, quem recebe é um `/bin/sh`, que nem sempre repassa o aviso.

O próprio Docker confere parte disso:

```bash
docker build --check .
```

Para um Dockerfile com `ENV ANTHROPIC_API_KEY=...` e um `CMD` na forma shell, ele avisa `SecretsUsedInArgOrEnv` e `JSONArgsRecommended`. Ferramentas como o hadolint vão além e apontam, por exemplo, o pip sem `--no-cache-dir`.

Quando a instalação precisa de compiladores, um **build em várias etapas** ajuda: uma primeira etapa, com a imagem completa, compila; a etapa final, slim, copia só o resultado.

## Rodar e investigar contêineres

Os comandos do dia a dia:

```bash
docker run -d --name api -p 8080:8080 --env-file .env api-cancelamento  # roda em segundo plano
docker ps                    # lista os contêineres rodando
docker logs -f api           # acompanha a saída da aplicação
docker exec -it api bash     # abre um terminal dentro do contêiner
docker stop api              # pede para encerrar, com o aviso de desligamento
docker rm api                # remove o contêiner parado
docker images                # lista as imagens
docker history api-cancelamento  # mostra as camadas e o tamanho de cada uma
```

Dois erros aparecem muito. O primeiro: a API escuta em `127.0.0.1` dentro do contêiner e ninguém consegue acessá-la de fora, porque `127.0.0.1` lá dentro é o próprio contêiner. O servidor precisa escutar em `0.0.0.0`; o `fastapi run` já faz isso, e o `fastapi dev`, pensado para o seu computador, não. O segundo: guardar dados dentro do contêiner. O que ele grava some quando é removido. Para guardar dados, use um **volume** no seu computador e, na nuvem, um banco ou um serviço de armazenamento.

## Vários serviços com o Docker Compose

Projetos reais costumam ter mais de um serviço: a API e um banco de dados, por exemplo. O **Docker Compose** descreve todos num arquivo `compose.yaml`:

```yaml
services:
  api:
    build: .
    ports:
      - "8080:8080"
    env_file: .env
    depends_on:
      - banco
  banco:
    image: postgres:17
    environment:
      POSTGRES_PASSWORD: ${SENHA_BANCO}
    volumes:
      - dados:/var/lib/postgresql/data

volumes:
  dados:
```

Com `docker compose up`, os dois sobem juntos, numa rede em que a API acessa o banco pelo nome `banco`. Com `docker compose down`, param; o volume `dados` guarda o banco entre uma execução e outra. A senha vem de uma variável de ambiente, e não do arquivo. O Compose é ótimo no seu computador e em servidores simples; na nuvem, cada serviço costuma rodar separado, gerenciado pela plataforma.

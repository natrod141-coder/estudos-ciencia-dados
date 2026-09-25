---
titulo: "Git e GitHub"
modulo: manipulacao
ordem: 6
horas: 4
estado: publicado
resumo: "Versionar código, criar branches e abrir Pull Requests."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Por que versionar: Git e GitHub"
    tipo: leitura
    minutos: 8
  - id: a2
    titulo: "O ciclo básico: status, add e commit"
    tipo: leitura
    minutos: 12
  - id: a3
    titulo: "O que não vai para o repositório: .gitignore"
    tipo: leitura
    minutos: 8
  - id: a4
    titulo: "Branches e merge"
    tipo: leitura
    minutos: 12
  - id: a5
    titulo: "Conflitos e como desfazer"
    tipo: leitura
    minutos: 12
  - id: a6
    titulo: "Remoto, Pull Request e revisão"
    tipo: leitura
    minutos: 12
  - id: a7
    titulo: "Vídeo de apoio: Git e GitHub para iniciantes"
    tipo: video
    minutos: 25
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Qual é a diferença entre Git e GitHub?"
    opcoes: ["São nomes diferentes para a mesma ferramenta", "Git é a ferramenta de controle de versões que roda no seu computador; GitHub é um serviço na internet que hospeda repositórios Git e acrescenta colaboração, como Pull Requests", "Git serve para código e GitHub serve para dados", "GitHub é a versão paga do Git"]
    correta: 1
    explicacao: "O Git funciona sozinho, sem internet: o histórico inteiro fica na pasta .git do projeto. O GitHub, assim como o GitLab e o Bitbucket, guarda uma cópia do repositório na nuvem e oferece revisão de código, Pull Requests, issues e automações."
  - pergunta: "Para que serve o git add?"
    opcoes: ["Envia os arquivos para o GitHub", "Cria um repositório novo", "Coloca alterações na área de preparação, escolhendo o que vai entrar no próximo commit", "Adiciona um colaborador ao projeto"]
    correta: 2
    explicacao: "O commit grava o que está na área de preparação (staging). O git add escolhe o que entra nela, e isso permite fazer commits com só parte das alterações. Quem envia para o GitHub é o git push."
  - pergunta: "Você fez um commit com um arquivo de senha e já enviou para um repositório público no GitHub. O que fazer?"
    opcoes: ["git reset HEAD~1 resolve", "Apagar o arquivo e fazer um novo commit resolve", "Tornar o repositório privado resolve", "Considerar a senha vazada e trocá-la imediatamente; limpar o histórico ajuda, mas não desfaz a exposição"]
    correta: 3
    explicacao: "Um novo commit apaga o arquivo da versão atual, mas ele continua no histórico. Mesmo reescrevendo o histórico, qualquer pessoa ou robô pode ter copiado o repositório nesse intervalo, e há robôs que procuram senhas em repositórios públicos. A senha precisa ser trocada. Para evitar o problema, o .env vai no .gitignore desde o primeiro commit."
  - pergunta: "Por que criar uma branch para cada funcionalidade nova?"
    opcoes: ["Para trabalhar isolado do main, que continua funcionando, e juntar as mudanças só depois de revisadas", "Porque o Git não permite commits no main", "Para o repositório ocupar menos espaço", "Porque cada branch é um repositório separado"]
    correta: 0
    explicacao: "A branch é uma linha de trabalho paralela. Os commits nela não afetam o main até o merge. Com isso, várias pessoas trabalham ao mesmo tempo, cada mudança pode ser revisada num Pull Request, e o main continua sempre utilizável."
  - pergunta: "Quando acontece um conflito de merge?"
    opcoes: ["Sempre que duas branches são juntadas", "Quando as duas branches alteraram as mesmas linhas de um arquivo, e o Git não sabe qual versão manter", "Quando uma das branches tem arquivos novos", "Quando o remoto está desatualizado"]
    correta: 1
    explicacao: "Na maioria dos merges, o Git junta as mudanças sozinho, mesmo no mesmo arquivo, se forem em partes diferentes. O conflito acontece quando as duas branches mudaram o mesmo trecho. O Git marca o trecho com <<<<<<<, ======= e >>>>>>>, e você decide o resultado."
  - pergunta: "Um commit com erro já está no main do GitHub, e colegas já baixaram. Qual é o jeito seguro de desfazê-lo?"
    opcoes: ["git reset --hard seguido de git push --force", "git commit --amend", "git revert, que cria um commit novo desfazendo as mudanças, sem reescrever o histórico", "Apagar o repositório e criar outro"]
    correta: 2
    explicacao: "O reset reescreve o histórico: quem já baixou o commit fica com um histórico diferente do remoto, e o push forçado pode apagar trabalho dos colegas. O revert acrescenta um commit que desfaz o anterior, e todo mundo continua com o mesmo histórico. Regra prática: reset só no que ainda não foi enviado."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Descreva o fluxo que você seguiria, do começo ao fim, para acrescentar uma análise nova a um repositório compartilhado com o time, usando branch e Pull Request. Por que não fazer o commit direto no main?"
  rubrica:
    - "Descreve os passos em ordem: atualizar o main local (pull), criar uma branch, fazer commits pequenos com mensagens claras, enviar a branch (push) e abrir um Pull Request."
    - "Explica o papel do Pull Request: outra pessoa revisa, há espaço para discussão e ajustes, e testes automáticos podem rodar antes de juntar ao main."
    - "Justifica não commitar direto no main: o main fica sempre funcionando, toda mudança passa por revisão e fica registrada com contexto, e é mais fácil desfazer uma mudança isolada."
  modelo: "Primeiro eu atualizaria o main local com git pull, para partir da versão mais recente. Depois criaria uma branch com um nome que diga o que ela faz, como analise/churn-marco, e trabalharia nela, com commits pequenos e mensagens que expliquem o que mudou. Quando a análise estivesse pronta, enviaria a branch com git push -u origin e abriria um Pull Request no GitHub, explicando o objetivo, como conferir o resultado e o que ainda está em aberto. Uma colega revisaria o código e os números, os testes automáticos rodariam, eu ajustaria o que fosse pedido com novos commits na mesma branch, e só então a branch seria juntada ao main. Commitar direto no main pula tudo isso: um erro chega direto à versão que todo mundo usa, ninguém revisa, e a mudança fica misturada com as dos outros. Com a branch e o Pull Request, o main continua sempre funcionando, e cada mudança fica registrada junto com a discussão que a justificou."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Git na prática"
  descricao: "Nove situações do dia a dia de um time de dados: começar um repositório, escrever o .gitignore, trabalhar numa branch, fazer um commit seletivo, descartar e desfazer mudanças, resolver um conflito de merge, e enviar e receber commits de um remoto. Você responde com os comandos git, e os testes rodam os comandos em repositórios temporários e conferem o resultado."
  pasta: "desafios/manipulacao/git_github"
  testes: 9
  tempo: "1 h 30 min"
  ferramentas: "VS Code, Git 2.32 ou superior, Python 3.11 ou superior e pytest"
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
      descricao: "Abra o terminal do VS Code com Ctrl+` (acento grave). Depois use Ctrl+Shift+P, Python: Select Interpreter, e escolha o .venv. Confira também a versão do Git com git --version."
      comandos:
        - "# Linux ou macOS"
        - "python3 -m venv .venv"
        - "source .venv/bin/activate"
        - "# Windows (PowerShell)"
        - "python -m venv .venv"
        - '.venv\Scripts\Activate.ps1'
        - "pip install -r desafios/requirements.txt"
        - "git --version"
    - titulo: "Leia o enunciado"
      descricao: "Abra desafios/manipulacao/git_github/README.md. Ele explica como as respostas são testadas. As nove situações estão descritas no solucao.py."
    - titulo: "Escreva os comandos em solucao.py"
      descricao: "Cada situação tem uma variável, e a resposta é a lista de comandos git, na ordem, um por item. Antes, experimente os comandos num repositório de teste, fora do projeto. Não altere a pasta tests."
      codigo: true
      comandos:
        - "PRIMEIRO_COMMIT = [\"git ...\", \"git ...\"]"
        - "GITIGNORE = \"\"\" ... \"\"\""
        - "CRIAR_BRANCH = [\"git ...\"]"
        - "..."
        - "ATUALIZAR_MAIN = [\"git ...\"]"
    - titulo: "Rode os testes a cada resposta"
      descricao: "Quando um teste falha, a mensagem mostra os comandos que rodaram e a saída de cada um."
      comandos:
        - "cd desafios/manipulacao/git_github"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Use o próprio fluxo que o desafio ensina: branch, commit, push e Pull Request."
      comandos:
        - "git checkout -b desafio/git_github"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de Git e GitHub"'
        - "git push -u origin desafio/git_github"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Repositório", en: "repository" }
  - { pt: "Área de preparação", en: "staging area, index" }
  - { pt: "Ramo", en: "branch" }
  - { pt: "Mesclar", en: "merge" }
  - { pt: "Conflito de merge", en: "merge conflict" }
  - { pt: "Repositório remoto", en: "remote" }
  - { pt: "Enviar", en: "push" }
  - { pt: "Puxar", en: "pull" }
  - { pt: "Buscar", en: "fetch" }
  - { pt: "Clonar", en: "clone" }
  - { pt: "Bifurcação", en: "fork" }
  - { pt: "Pedido de integração", en: "pull request (PR)" }
  - { pt: "Rastreamento do remoto", en: "upstream" }
  - { pt: "Integração contínua", en: "continuous integration (CI)" }
---

## Por que versionar: Git e GitHub

Todo projeto de dados passa por versões: `analise_final.py`, `analise_final_v2.py`, `analise_final_agora_vai.py`. O **Git** resolve isso: ele guarda o histórico completo do projeto, com cada mudança registrada, datada e explicada. Dá para ver o que mudou, voltar a qualquer versão anterior e trabalhar em várias coisas ao mesmo tempo sem misturá-las.

O Git roda no seu computador. O histórico fica numa pasta oculta, `.git`, dentro do projeto. O **GitHub** é um serviço na internet que guarda uma cópia do repositório e acrescenta colaboração: revisão de código com Pull Requests, discussões, automações que rodam testes a cada mudança. GitLab e Bitbucket fazem o mesmo papel.

Para quem trabalha com dados, o Git serve para três coisas:

- **Histórico:** saber quando e por que uma regra de cálculo mudou.
- **Colaboração:** várias pessoas mexendo no mesmo projeto sem sobrescrever o trabalho umas das outras.
- **Portfólio:** um perfil no GitHub com projetos bem organizados é uma das melhores formas de mostrar o que você sabe fazer. Por isso os desafios deste site são entregues como Pull Requests.

## O ciclo básico: status, add e commit

Um arquivo passa por três lugares:

1. **Pasta de trabalho:** onde você edita os arquivos.
2. **Área de preparação** (*staging*): onde você separa as mudanças que vão entrar no próximo commit.
3. **Repositório:** onde os commits ficam guardados para sempre.

```bash
# transforma a pasta num repositório (uma vez só)
git init

# o que mudou e o que está preparado
git status

# prepara um arquivo, ou tudo o que mudou na pasta
git add analise.py
git add .

git commit -m "Calcula ticket médio por estado"

# o histórico, um commit por linha
git log --oneline

# o que mudou e ainda não foi preparado
git diff
```

Um **commit** é uma fotografia do projeto, com autor, data e mensagem. Duas boas práticas:

- **Commits pequenos, com um assunto só.** "Corrige filtro de data" e "Adiciona gráfico mensal" são dois commits, e não um.
- **Mensagens que dizem o que muda**, no imperativo e com contexto: "Remove pedidos cancelados do faturamento" é útil daqui a seis meses. "ajustes" não é.

A área de preparação existe para permitir commits seletivos: você alterou três arquivos, mas só dois estão prontos? Faça `git add` só nos dois.

Antes do primeiro commit numa máquina nova, configure o seu nome e e-mail, que aparecem em cada commit:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "voce@exemplo.com"
```

## O que não vai para o repositório: .gitignore

O arquivo `.gitignore`, na raiz do projeto, lista o que o Git deve ignorar. Num projeto de dados, quatro tipos de arquivo ficam de fora:

| O quê                     | Por quê                                         | No .gitignore             |
| ------------------------- | ----------------------------------------------- | ------------------------- |
| Segredos                  | Senhas e chaves de API vazam com o repositório  | `.env`                    |
| Ambiente virtual          | É recriado com `pip install -r requirements.txt` | `.venv/`                 |
| Arquivos gerados          | São recriados ao rodar o código                 | `__pycache__/`, `*.pyc`, `.ipynb_checkpoints/` |
| Dados grandes ou sensíveis | O Git não foi feito para arquivos grandes, e dados de clientes não podem ir para o GitHub | `dados/brutos/` |

Os padrões funcionam assim: `nome` ignora o arquivo ou pasta com esse nome em qualquer lugar, `pasta/` ignora a pasta inteira, `*.pyc` ignora todos os arquivos com essa extensão, e `!arquivo` abre uma exceção. Um `.env.exemplo`, com os nomes das variáveis e sem os valores, costuma ir para o repositório para mostrar o formato esperado.

O `.gitignore` só vale para arquivos que ainda não estão no repositório. Um arquivo já commitado continua sendo rastreado até ser removido com `git rm --cached arquivo`. E um segredo que já foi enviado para o GitHub deve ser considerado vazado: troque a senha, porque o histórico guarda o arquivo.

## Branches e merge

Uma **branch** é uma linha de trabalho paralela. O projeto começa com a branch `main`, que deve conter sempre a versão que funciona. Para uma mudança nova, crie uma branch, trabalhe nela e junte ao main quando estiver pronta:

```bash
# cria a branch e passa para ela
git switch -c feature/grafico-mensal

# ... edita, add, commit, quantas vezes precisar ...

# volta para o main e junta a branch nele
git switch main
git merge feature/grafico-mensal

# apaga a branch já juntada
git branch -d feature/grafico-mensal
```

O `git switch -c` é a forma atual. Em tutoriais antigos, aparece `git checkout -b`, que faz o mesmo.

Para ver as branches e como elas se juntam, use `git log --oneline --graph --all`.

## Conflitos e como desfazer

**Conflitos.** No merge, o Git junta sozinho as mudanças em partes diferentes dos arquivos. Quando as duas branches mudaram as mesmas linhas, ele para e marca o trecho:

```text
<<<<<<< HEAD
    return df.dropna(how='all')
=======
    return df.dropna().drop_duplicates()
>>>>>>> feature/limpeza
```

A parte de cima é a versão da branch em que você está, e a de baixo é a da branch que está chegando. Para resolver: edite o arquivo, deixando o código como deve ficar e apagando as marcas, depois `git add` no arquivo e `git commit` para concluir o merge. Quando uma das versões deve ficar inteira, `git checkout --ours arquivo` ou `git checkout --theirs arquivo` escolhe a versão de um dos lados. O VS Code mostra botões para aceitar uma versão, a outra ou as duas. Para desistir do merge, use `git merge --abort`.

**Desfazer.** Cada situação tem o seu comando:

| Situação                                              | Comando                     |
| ----------------------------------------------------- | --------------------------- |
| Descartar alterações não commitadas de um arquivo     | `git restore arquivo`       |
| Tirar um arquivo da área de preparação                | `git restore --staged arquivo` |
| Corrigir a mensagem do último commit, ainda não enviado | `git commit --amend -m "..."` |
| Desfazer o último commit, ainda não enviado, mantendo os arquivos | `git reset HEAD~1` |
| Desfazer um commit que já foi enviado                 | `git revert <commit>`       |

A regra mais importante: **não reescreva o histórico que já foi enviado**. `reset` e `commit --amend` mudam commits existentes. Se alguém já baixou esses commits, o seu histórico e o dele deixam de bater. Para o que já está no remoto, use `revert`, que desfaz criando um commit novo. E cuidado com `git reset --hard` e `git restore`: eles descartam alterações sem volta.

## Remoto, Pull Request e revisão

O **remoto** é a cópia do repositório no GitHub, que por convenção se chama `origin`.

```bash
# baixa um repositório existente
git clone https://github.com/usuario/projeto.git

# envia a branch e configura o upstream
git push -u origin feature/grafico-mensal

# depois do -u, basta isso
git push

# traz as mudanças do remoto e junta; o fetch só traz
git pull
git fetch
```

O `-u` no primeiro push liga a branch local à branch remota, o que se chama **upstream**. Depois disso, `git push` e `git pull` sabem para onde ir sem precisar dos nomes.

O **Pull Request** (PR) é o pedido para juntar uma branch no main, feito na página do GitHub. É onde a colaboração acontece:

1. Você envia a branch e abre o PR, explicando o que muda, por que e como conferir.
2. Outra pessoa revisa: lê as mudanças, comenta linhas específicas, pede ajustes.
3. Testes automáticos rodam. É a **integração contínua** (CI): no GitHub, o GitHub Actions pode rodar o pytest a cada push, como faz o repositório deste site.
4. Você ajusta com novos commits na mesma branch, e o PR se atualiza sozinho.
5. Aprovado, o PR é juntado ao main.

O fluxo completo de uma mudança, do jeito que os desafios deste site são entregues:

```bash
# parte da versão mais recente
git switch main
git pull

# uma branch para a mudança
git switch -c desafio/excel

# ... trabalho, add, commit ...

# envia e abre o Pull Request na página do GitHub
git push -u origin desafio/excel
```

Para contribuir com um projeto de outra pessoa, em que você não tem permissão de escrita, faz-se antes um **fork**: uma cópia do repositório na sua conta. Você trabalha no fork e abre o PR dele para o original.

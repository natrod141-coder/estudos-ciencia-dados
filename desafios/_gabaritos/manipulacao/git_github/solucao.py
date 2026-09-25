"""Gabarito do desafio "Git na prática".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela mostra os comandos que rodaram e a saída de cada um.

Há outros comandos que também passam nos testes: por exemplo, git checkout -b no lugar de
git switch -c, git checkout -- no lugar de git restore, ou git merge -X theirs no conflito.
"""

PRIMEIRO_COMMIT = [
    "git init",
    "git add analise.py README.md",
    'git commit -m "Primeiro commit"',
]

GITIGNORE = """
# segredos: nunca vão para o repositório
.env

# ambiente virtual e arquivos gerados pelo Python
.venv/
__pycache__/
*.pyc

# dados brutos, grandes demais para o Git
dados/brutos/

# cópias automáticas do Jupyter
.ipynb_checkpoints/
"""

CRIAR_BRANCH = [
    "git switch -c feature/grafico",
]

COMMIT_SELETIVO = [
    "git add grafico.py",
    'git commit -m "Adiciona gráfico de vendas"',
]

DESCARTAR_ALTERACOES = [
    "git restore analise.py",
]

DESFAZER_COMMIT = [
    "git reset HEAD~1",
]

MERGE_COM_CONFLITO = [
    "git merge feature/limpeza",
    "git checkout --theirs limpeza.py",
    "git add limpeza.py",
    "git commit --no-edit",
]

ENVIAR_BRANCH = [
    "git push -u origin feature/grafico",
]

ATUALIZAR_MAIN = [
    "git pull origin main",
]

import json
import re
from pathlib import Path

from solucao import ignorado, ler_instrucoes, primeira_etapa_refeita, problemas

PASTA = Path(__file__).parent.parent

BOM = """\
# Um Dockerfile sem problemas
FROM python:3.14-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir \\
    -r requirements.txt
COPY app ./app
RUN useradd --create-home api
USER api
CMD ["fastapi", "run", "app/main.py", "--port", "8080"]
"""

RUIM = """\
FROM python:latest
ENV ANTHROPIC_API_KEY=sk-ant-0000
WORKDIR /code
COPY . .
RUN pip install -r requirements.txt
CMD fastapi run app/main.py
"""


def problemas_de(texto):
    return problemas(ler_instrucoes(texto))


def test_ler_instrucoes():
    assert ler_instrucoes(BOM) == [
        ("FROM", "python:3.14-slim"),
        ("ENV", "PYTHONUNBUFFERED=1"),
        ("WORKDIR", "/code"),
        ("COPY", "requirements.txt ."),
        ("RUN", "pip install --no-cache-dir -r requirements.txt"),
        ("COPY", "app ./app"),
        ("RUN", "useradd --create-home api"),
        ("USER", "api"),
        ("CMD", '["fastapi", "run", "app/main.py", "--port", "8080"]'),
    ]


def test_ler_instrucoes_minusculas_e_comentarios_no_meio():
    texto = "from python:3.14-slim AS base\n\nrun apt-get update && \\\n    # comentário no meio\n    apt-get install -y curl\n"
    assert ler_instrucoes(texto) == [
        ("FROM", "python:3.14-slim AS base"),
        ("RUN", "apt-get update && apt-get install -y curl"),
    ]


def test_dockerfile_bom_e_dockerfile_ruim():
    assert problemas_de(BOM) == []
    assert problemas_de(RUIM) == [
        "imagem-sem-versao", "pip-com-cache", "usuario-root", "cmd-forma-shell",
        "segredo-no-dockerfile", "copia-tudo-antes-de-instalar",
    ]


def test_imagem_e_pip():
    final = "USER api\nCMD [\"python\", \"app.py\"]\n"
    assert problemas_de("FROM python\n" + final) == ["imagem-sem-versao"]
    assert problemas_de("FROM python:3.14-slim AS construcao\nFROM construcao\n" + final) == [], (
        "FROM construcao usa uma etapa anterior do próprio Dockerfile, e não uma imagem sem versão."
    )
    assert problemas_de("FROM python:3.14-slim\nRUN pip install pandas\n" + final) == ["pip-com-cache"]


def test_usuario_e_forma_do_cmd():
    cmd = 'CMD ["python", "app.py"]\n'
    assert problemas_de("FROM python:3.14-slim\n" + cmd) == ["usuario-root"]
    assert problemas_de("FROM python:3.14-slim\nUSER api\nUSER root\n" + cmd) == ["usuario-root"]
    assert problemas_de("FROM python:3.14-slim AS a\nUSER api\nFROM python:3.14-slim\n" + cmd) == ["usuario-root"], (
        "Só vale o USER da última etapa: é ela que vira a imagem final."
    )
    assert problemas_de("FROM python:3.14-slim\nUSER api\nENTRYPOINT python app.py\n") == ["cmd-forma-shell"]


def test_segredos_e_ordem_das_copias():
    base = "FROM python:3.14-slim\nUSER api\n"
    assert problemas_de(base + "ARG GITHUB_TOKEN\n") == ["segredo-no-dockerfile"]
    assert problemas_de(base + "ENV MODO=producao CHAVE_SECRETA=abc\n") == ["segredo-no-dockerfile"]
    assert problemas_de(base + "ENV PORTA=8080\n") == []
    copia_depois = base + "COPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\n"
    assert problemas_de(copia_depois) == []


def test_dockerignore():
    padroes = ["# comentário", ".git", ".venv", "**/__pycache__", "*.md", "!README.md", "data/*.csv"]
    ignorados = [".git/HEAD", ".venv/lib/site.py", "app/__pycache__/main.pyc", "__pycache__/x.pyc", "notas.md", "data/vendas.csv"]
    mantidos = ["README.md", "docs/guia.md", "data/2026/vendas.csv", "app/main.py", "requirements.txt"]
    assert [c for c in ignorados if not ignorado(c, padroes)] == []
    assert [c for c in mantidos if ignorado(c, padroes)] == [], "* não atravessa pastas; ** atravessa; ! abre exceção."


def test_primeira_etapa_refeita():
    instrucoes = ler_instrucoes(BOM)
    assert primeira_etapa_refeita(instrucoes, ["app/main.py"]) == 5
    assert primeira_etapa_refeita(instrucoes, ["requirements.txt"]) == 3
    assert primeira_etapa_refeita(instrucoes, ["app/main.py", "requirements.txt"]) == 3
    assert primeira_etapa_refeita(instrucoes, ["README.md"], ["*.md"]) is None
    assert primeira_etapa_refeita(ler_instrucoes(RUIM), ["app/main.py"]) == 3, (
        "Com COPY . . antes do pip install, mudar uma linha do código refaz a instalação."
    )


def test_seu_dockerfile():
    instrucoes = ler_instrucoes((PASTA / "Dockerfile").read_text(encoding="utf-8"))
    assert problemas(instrucoes) == []
    imagem = [a for n, a in instrucoes if n == "FROM"][-1]
    assert re.fullmatch(r"python:3\.\d+-slim", imagem.split()[0]), "Use a imagem oficial do Python, slim, com a versão."
    assert ("EXPOSE", "8080") in instrucoes
    comando = json.loads([a for n, a in instrucoes if n == "CMD"][-1])
    assert "8080" in comando and ("fastapi" in comando or "uvicorn" in comando)
    padroes = (PASTA / ".dockerignore").read_text(encoding="utf-8").splitlines()
    codigo = primeira_etapa_refeita(instrucoes, ["app/main.py"], padroes)
    assert not any("pip install" in a for _, a in instrucoes[codigo:]), "Mudar o código não pode refazer a instalação."
    assert primeira_etapa_refeita(instrucoes, ["requirements.txt"], padroes) is not None


def test_seu_dockerignore():
    padroes = (PASTA / ".dockerignore").read_text(encoding="utf-8").splitlines()
    fora = [".env", ".git/HEAD", ".venv/Lib/site.py", "app/__pycache__/main.cpython-314.pyc", "tests/test_docker.py"]
    dentro = ["app/main.py", "app/modelo.py", "app/modelo.json", "requirements.txt"]
    assert [c for c in fora if not ignorado(c, padroes)] == [], "Estes não podem ir para a imagem."
    assert [c for c in dentro if ignorado(c, padroes)] == [], "A API precisa destes arquivos."

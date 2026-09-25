"""Cada teste monta um repositório temporário numa situação, roda os seus comandos e confere
o resultado. Os repositórios são criados numa pasta temporária: nada acontece no seu projeto.

Os testes ignoram a sua configuração do Git (nome, e-mail, editor) para que o resultado seja
o mesmo em qualquer computador.
"""

import os
import shlex
import subprocess

import pytest

import solucao

ORIGINAL_ANALISE = "import pandas as pd\n\nvendas = pd.read_csv('vendas.csv')\n"
LIMPEZA_BASE = "def limpar(df):\n    return df.dropna()\n"
LIMPEZA_MAIN = "def limpar(df):\n    return df.dropna(how='all')\n"
LIMPEZA_FEATURE = "def limpar(df):\n    return df.dropna().drop_duplicates()\n"


@pytest.fixture
def ambiente(tmp_path):
    config_vazia = tmp_path / "gitconfig_vazio"
    config_vazia.write_text("", encoding="utf-8")
    return {
        **os.environ,
        "GIT_CONFIG_GLOBAL": str(config_vazia),
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_COUNT": "2",
        "GIT_CONFIG_KEY_0": "init.defaultBranch",
        "GIT_CONFIG_VALUE_0": "main",
        "GIT_CONFIG_KEY_1": "core.autocrlf",
        "GIT_CONFIG_VALUE_1": "false",
        "GIT_AUTHOR_NAME": "Estudante",
        "GIT_AUTHOR_EMAIL": "estudante@exemplo.com",
        "GIT_COMMITTER_NAME": "Estudante",
        "GIT_COMMITTER_EMAIL": "estudante@exemplo.com",
        "GIT_EDITOR": "true",  # um commit sem -m falha em vez de abrir um editor
        "GIT_MERGE_AUTOEDIT": "no",
        "GIT_TERMINAL_PROMPT": "0",
    }


def git(pasta, ambiente, *argumentos):
    """Roda um comando git para montar a situação do teste."""
    resultado = subprocess.run(
        ["git", *argumentos], cwd=pasta, env=ambiente, capture_output=True, text=True, encoding="utf-8"
    )
    assert resultado.returncode == 0, f"Falha ao preparar o teste: git {' '.join(argumentos)}\n{resultado.stderr}"
    return resultado.stdout.strip()


def escrever(pasta, nome, conteudo):
    caminho = pasta / nome
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(conteudo, encoding="utf-8", newline="\n")


def rodar(comandos, pasta, ambiente):
    """Roda os seus comandos, um por um, e devolve tudo o que eles imprimiram."""
    assert comandos, "Preencha a lista de comandos no solucao.py."
    saidas = []
    for comando in comandos:
        partes = shlex.split(comando)
        assert partes and partes[0] == "git", f"Use só comandos git, um por item da lista: {comando!r}"
        resultado = subprocess.run(
            partes, cwd=pasta, env=ambiente, capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        saidas.append(f"$ {comando}\n{resultado.stdout}{resultado.stderr}")
    return "\n".join(saidas)


def repositorio_com_um_commit(pasta, ambiente):
    pasta.mkdir()
    git(pasta, ambiente, "init")
    escrever(pasta, "analise.py", ORIGINAL_ANALISE)
    escrever(pasta, "README.md", "# Análise de vendas\n")
    git(pasta, ambiente, "add", ".")
    git(pasta, ambiente, "commit", "-m", "Primeiro commit")


def test_primeiro_commit(tmp_path, ambiente):
    projeto = tmp_path / "projeto"
    projeto.mkdir()
    escrever(projeto, "analise.py", ORIGINAL_ANALISE)
    escrever(projeto, "README.md", "# Análise de vendas\n")

    saida = rodar(solucao.PRIMEIRO_COMMIT, projeto, ambiente)

    assert (projeto / ".git").is_dir(), "A pasta ainda não é um repositório.\n" + saida
    assert git(projeto, ambiente, "log", "--format=%s").splitlines() == ["Primeiro commit"], (
        'Esperava um único commit, com a mensagem "Primeiro commit".\n' + saida
    )
    assert git(projeto, ambiente, "ls-files").splitlines() == ["README.md", "analise.py"], (
        "O commit precisa ter os dois arquivos.\n" + saida
    )
    assert git(projeto, ambiente, "status", "--porcelain") == "", "Sobrou alteração fora do commit.\n" + saida


def test_gitignore(tmp_path, ambiente):
    projeto = tmp_path / "projeto"
    projeto.mkdir()
    git(projeto, ambiente, "init")
    escrever(projeto, ".gitignore", solucao.GITIGNORE)

    def ignorado(caminho):
        resultado = subprocess.run(["git", "check-ignore", "-q", caminho], cwd=projeto, env=ambiente)
        return resultado.returncode == 0

    for caminho in [".env", ".venv/Lib/site-packages/pandas.py", "__pycache__/analise.cpython-312.pyc",
                    "modelo.pyc", "dados/brutos/clientes.csv", ".ipynb_checkpoints/relatorio-checkpoint.ipynb"]:
        assert ignorado(caminho), f"{caminho} deveria ser ignorado."
    for caminho in [".env.exemplo", "analise.py", "dados/README.md", "relatorio.ipynb", ".gitignore"]:
        assert not ignorado(caminho), f"{caminho} não pode ser ignorado."


def test_criar_branch(tmp_path, ambiente):
    projeto = tmp_path / "projeto"
    repositorio_com_um_commit(projeto, ambiente)
    commit_do_main = git(projeto, ambiente, "rev-parse", "main")

    saida = rodar(solucao.CRIAR_BRANCH, projeto, ambiente)

    assert git(projeto, ambiente, "branch", "--show-current") == "feature/grafico", saida
    assert git(projeto, ambiente, "rev-parse", "HEAD") == commit_do_main, "A branch nova deve partir do main.\n" + saida


def test_commit_seletivo(tmp_path, ambiente):
    projeto = tmp_path / "projeto"
    repositorio_com_um_commit(projeto, ambiente)
    git(projeto, ambiente, "switch", "-c", "feature/grafico")
    escrever(projeto, "grafico.py", "import matplotlib.pyplot as plt\n")
    escrever(projeto, "rascunho.txt", "ideias soltas\n")

    saida = rodar(solucao.COMMIT_SELETIVO, projeto, ambiente)

    assert git(projeto, ambiente, "log", "-1", "--format=%s") == "Adiciona gráfico de vendas", saida
    assert git(projeto, ambiente, "show", "--name-only", "--format=", "HEAD") == "grafico.py", (
        "O commit deve ter só o grafico.py.\n" + saida
    )
    assert git(projeto, ambiente, "status", "--porcelain") == "?? rascunho.txt", saida


def test_descartar_alteracoes_de_um_arquivo(tmp_path, ambiente):
    projeto = tmp_path / "projeto"
    repositorio_com_um_commit(projeto, ambiente)
    escrever(projeto, "analise.py", "codigo quebrado\n")
    escrever(projeto, "README.md", "# Análise de vendas\n\nComo rodar: python analise.py\n")

    saida = rodar(solucao.DESCARTAR_ALTERACOES, projeto, ambiente)

    assert (projeto / "analise.py").read_text(encoding="utf-8") == ORIGINAL_ANALISE, saida
    assert git(projeto, ambiente, "status", "--porcelain") == "M README.md", (
        "A alteração do README.md precisa continuar lá.\n" + saida
    )


def test_desfazer_ultimo_commit_mantendo_os_arquivos(tmp_path, ambiente):
    projeto = tmp_path / "projeto"
    repositorio_com_um_commit(projeto, ambiente)
    primeiro = git(projeto, ambiente, "rev-parse", "HEAD")
    escrever(projeto, "config.py", "PASTA = 'dados'\n")
    escrever(projeto, "senha.txt", "123456\n")
    git(projeto, ambiente, "add", ".")
    git(projeto, ambiente, "commit", "-m", "Adiciona configuração")

    saida = rodar(solucao.DESFAZER_COMMIT, projeto, ambiente)

    assert git(projeto, ambiente, "rev-parse", "HEAD") == primeiro, "O último commit continua no histórico.\n" + saida
    assert (projeto / "config.py").exists() and (projeto / "senha.txt").exists(), (
        "Os arquivos precisam continuar no disco: desfaça o commit, não o trabalho.\n" + saida
    )


def test_merge_com_conflito(tmp_path, ambiente):
    projeto = tmp_path / "projeto"
    projeto.mkdir()
    git(projeto, ambiente, "init")
    escrever(projeto, "limpeza.py", LIMPEZA_BASE)
    git(projeto, ambiente, "add", ".")
    git(projeto, ambiente, "commit", "-m", "Função de limpeza")
    git(projeto, ambiente, "switch", "-c", "feature/limpeza")
    escrever(projeto, "limpeza.py", LIMPEZA_FEATURE)
    git(projeto, ambiente, "commit", "-am", "Remove duplicatas na limpeza")
    git(projeto, ambiente, "switch", "main")
    escrever(projeto, "limpeza.py", LIMPEZA_MAIN)
    git(projeto, ambiente, "commit", "-am", "Só remove linhas totalmente vazias")

    saida = rodar(solucao.MERGE_COM_CONFLITO, projeto, ambiente)

    assert git(projeto, ambiente, "branch", "--show-current") == "main", saida
    pais = git(projeto, ambiente, "log", "-1", "--format=%P").split()
    assert len(pais) == 2, "O merge não foi concluído com um commit de merge.\n" + saida
    conteudo = (projeto / "limpeza.py").read_text(encoding="utf-8")
    assert "<<<<<<<" not in conteudo, "Ficaram marcas de conflito no arquivo.\n" + saida
    assert conteudo == LIMPEZA_FEATURE, "Fique com a versão da feature/limpeza.\n" + saida
    assert git(projeto, ambiente, "status", "--porcelain") == "", saida


def test_enviar_branch_para_o_remoto(tmp_path, ambiente):
    remoto = tmp_path / "remoto.git"
    git(tmp_path, ambiente, "init", "--bare", str(remoto))
    projeto = tmp_path / "projeto"
    repositorio_com_um_commit(projeto, ambiente)
    git(projeto, ambiente, "remote", "add", "origin", str(remoto))
    git(projeto, ambiente, "push", "origin", "main")
    git(projeto, ambiente, "switch", "-c", "feature/grafico")
    escrever(projeto, "grafico.py", "import matplotlib.pyplot as plt\n")
    git(projeto, ambiente, "add", ".")
    git(projeto, ambiente, "commit", "-m", "Adiciona gráfico de vendas")

    saida = rodar(solucao.ENVIAR_BRANCH, projeto, ambiente)

    no_remoto = subprocess.run(
        ["git", "rev-parse", "feature/grafico"], cwd=remoto, env=ambiente, capture_output=True, text=True
    ).stdout.strip()
    assert no_remoto == git(projeto, ambiente, "rev-parse", "HEAD"), "A branch não chegou ao remoto.\n" + saida
    upstream = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "feature/grafico@{upstream}"],
        cwd=projeto, env=ambiente, capture_output=True, text=True,
    ).stdout.strip()
    assert upstream == "origin/feature/grafico", (
        "A branch chegou ao remoto, mas sem upstream. Configure o upstream (-u), para os próximos "
        "git push e git pull saberem para onde ir.\n" + saida
    )


def test_atualizar_o_main_local(tmp_path, ambiente):
    remoto = tmp_path / "remoto.git"
    git(tmp_path, ambiente, "init", "--bare", str(remoto))
    projeto = tmp_path / "projeto"
    repositorio_com_um_commit(projeto, ambiente)
    git(projeto, ambiente, "remote", "add", "origin", str(remoto))
    git(projeto, ambiente, "push", "-u", "origin", "main")
    # uma colega envia um commit novo para o main do remoto
    colega = tmp_path / "colega"
    git(tmp_path, ambiente, "clone", str(remoto), str(colega))
    escrever(colega, "relatorio.md", "# Relatório de março\n")
    git(colega, ambiente, "add", ".")
    git(colega, ambiente, "commit", "-m", "Adiciona relatório de março")
    git(colega, ambiente, "push", "origin", "main")

    saida = rodar(solucao.ATUALIZAR_MAIN, projeto, ambiente)

    assert git(projeto, ambiente, "rev-parse", "main") == git(colega, ambiente, "rev-parse", "main"), (
        "O main local não está igual ao do remoto.\n" + saida
    )
    assert (projeto / "relatorio.md").exists(), "O arquivo novo não apareceu na pasta.\n" + saida

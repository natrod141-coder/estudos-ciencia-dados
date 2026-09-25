"""Confere se cada desafio está bem construído.

Para cada desafio que tem gabarito em desafios/_gabaritos/, verifica três coisas:

1. Com o arquivo inicial (solucao.py que você recebe), todos os testes precisam falhar.
   Se algum passar sem nenhum código escrito, esse teste não está testando nada.
2. Com o gabarito no lugar do solucao.py, todos os testes precisam passar.
3. A quantidade de testes é a mesma do campo "testes" do tópico que aponta para o desafio.
   Se for diferente, o critério "desafio aprovado" do painel nunca é cumprido.

Uso, na raiz do repositório:
    python scripts/verificar_desafios.py
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESAFIOS = RAIZ / "desafios"
GABARITOS = DESAFIOS / "_gabaritos"
TOPICOS = RAIZ / "conteudo" / "topicos"


def rodar_pytest(pasta: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
        cwd=pasta,
        capture_output=True,
        text=True,
    )


def contar(saida: str, situacao: str) -> int:
    """Lê do resumo do pytest ("3 failed, 5 passed in 0.4s") quantos testes tiveram a situação."""
    encontrado = re.search(rf"(\d+) {situacao}", saida)
    return int(encontrado.group(1)) if encontrado else 0


def testes_por_pasta() -> dict:
    """Devolve {pasta do desafio: número de testes} lendo o cabeçalho de cada tópico."""
    resultado = {}
    for arquivo in TOPICOS.rglob("*.md"):
        cabecalho = arquivo.read_text(encoding="utf-8").split("---")[1]
        pasta = re.search(r'^\s+pasta:\s*"?([^"\n]+?)"?\s*$', cabecalho, re.M)
        testes = re.search(r"^\s+testes:\s*(\d+)", cabecalho, re.M)
        if pasta and testes:
            resultado[pasta.group(1)] = int(testes.group(1))
    return resultado


def listar_desafios():
    for gabarito in sorted(GABARITOS.rglob("solucao.py")):
        relativo = gabarito.parent.relative_to(GABARITOS)
        pasta = DESAFIOS / relativo
        if pasta.is_dir():
            yield relativo, pasta, gabarito


def main() -> int:
    problemas = []
    total = 0
    esperados = testes_por_pasta()
    for relativo, pasta, gabarito in listar_desafios():
        total += 1
        print(f"Desafio {relativo}")

        with tempfile.TemporaryDirectory() as tmp:
            copia = Path(tmp) / "desafio"
            shutil.copytree(pasta, copia, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))

            inicial = rodar_pytest(copia)
            passaram_sem_solucao = contar(inicial.stdout, "passed")
            erros_sem_solucao = contar(inicial.stdout, "error")
            if inicial.returncode == 0 or passaram_sem_solucao > 0:
                problemas.append(
                    f"{relativo}: {passaram_sem_solucao} teste(s) passam com o arquivo inicial, sem nenhuma solução"
                )
                print("  arquivo inicial: PROBLEMA (há testes passando sem solução)")
            elif erros_sem_solucao > 0:
                # "ERROR at setup" confunde quem está aprendendo: cada teste deve aparecer como FAILED
                problemas.append(
                    f"{relativo}: {erros_sem_solucao} teste(s) dão erro de preparação (fixture) em vez de falhar"
                )
                print("  arquivo inicial: PROBLEMA (há testes com ERROR em vez de FAILED)")
            else:
                print("  arquivo inicial: todos os testes falham, como esperado")

            shutil.copyfile(gabarito, copia / "solucao.py")
            com_gabarito = rodar_pytest(copia)
            passaram = contar(com_gabarito.stdout, "passed")
            if com_gabarito.returncode != 0:
                problemas.append(f"{relativo}: o gabarito não passa nos testes")
                print("  gabarito: PROBLEMA\n" + com_gabarito.stdout[-1500:])
            else:
                print(f"  gabarito: todos os {passaram} testes passam")

            chave = f"desafios/{relativo.as_posix()}"
            if chave not in esperados:
                problemas.append(f"{relativo}: nenhum tópico aponta para este desafio no campo desafio.pasta")
                print("  tópico: PROBLEMA (nenhum tópico aponta para esta pasta)")
            elif com_gabarito.returncode == 0 and esperados[chave] != passaram:
                problemas.append(
                    f"{relativo}: o tópico diz testes: {esperados[chave]}, mas o desafio tem {passaram} testes"
                )
                print(f"  tópico: PROBLEMA (testes: {esperados[chave]} no tópico, {passaram} no desafio)")
            else:
                print(f"  tópico: campo testes confere ({esperados[chave]})")

    if total == 0:
        print("Nenhum desafio com gabarito encontrado.")
        return 1
    if problemas:
        print("\nProblemas encontrados:")
        for problema in problemas:
            print(f"  * {problema}")
        return 1
    print(f"\n{total} desafio(s) verificado(s) sem problemas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

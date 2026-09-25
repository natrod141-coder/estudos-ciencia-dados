"""Desafio: Git na prática.

Cada situação abaixo descreve um repositório e o que você precisa fazer nele. A resposta é a
lista de comandos git, na ordem em que você os digitaria no terminal, um comando por item.
O .gitignore é a exceção: a resposta é o conteúdo do arquivo.

Os testes criam cada repositório numa pasta temporária, rodam os seus comandos dentro dela
e conferem o resultado. Nada acontece no seu projeto.

Regras:
- Só comandos git, um por item da lista. Nada de cd, &&, | ou outros programas.
- Os comandos rodam na pasta raiz do repositório.
- Commits precisam de mensagem (-m): os testes não abrem editor.
- Não altere a pasta tests.

Para treinar antes, crie um repositório de teste numa pasta qualquer e experimente os comandos.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

# 1. A pasta tem os arquivos analise.py e README.md e ainda não é um repositório Git.
#    Transforme a pasta em repositório e faça um commit com os dois arquivos, com a mensagem
#    "Primeiro commit".
PRIMEIRO_COMMIT = None

# 2. Escreva o conteúdo do .gitignore de um projeto de dados. Ele precisa ignorar:
#    - o arquivo .env, que guarda senhas (mas não o .env.exemplo, que mostra o formato);
#    - o ambiente virtual, na pasta .venv/;
#    - os arquivos gerados pelo Python: a pasta __pycache__/ e qualquer arquivo .pyc;
#    - os dados brutos, na pasta dados/brutos/ (mas não o dados/README.md);
#    - a pasta .ipynb_checkpoints/, criada pelo Jupyter.
#    Os notebooks (.ipynb) e o código (.py) precisam continuar versionados.
GITIGNORE = """
"""

# 3. Você está na branch main, com tudo commitado. Crie a branch feature/grafico e passe a
#    trabalhar nela.
CRIAR_BRANCH = None

# 4. Na branch feature/grafico, você criou dois arquivos: grafico.py, que está pronto, e
#    rascunho.txt, com anotações que não devem ir para o repositório. Faça um commit só com o
#    grafico.py, com a mensagem "Adiciona gráfico de vendas".
COMMIT_SELETIVO = None

# 5. Você alterou analise.py e README.md, sem commitar. A alteração em analise.py quebrou o
#    código: descarte-a, voltando o arquivo à versão do último commit. A alteração no README.md
#    está boa e precisa continuar.
DESCARTAR_ALTERACOES = None

# 6. O último commit ("Adiciona configuração") incluiu por engano o arquivo senha.txt, junto
#    com config.py. O commit ainda não foi enviado para o remoto. Desfaça o commit, mas
#    mantenha os dois arquivos na pasta, para você corrigir antes de commitar de novo.
DESFAZER_COMMIT = None

# 7. Você está no main. O main e a branch feature/limpeza alteraram a mesma linha de
#    limpeza.py. Junte a feature/limpeza no main e, no conflito, fique com a versão da
#    feature/limpeza. Termine com o merge concluído e nada pendente.
MERGE_COM_CONFLITO = None

# 8. O repositório tem um remoto chamado origin. Você está na branch feature/grafico, com um
#    commit que só existe no seu computador. Envie a branch para o origin e configure o
#    upstream, para que os próximos git push e git pull saibam para onde ir.
ENVIAR_BRANCH = None

# 9. Você está no main. Uma colega enviou commits novos para o main do origin. Traga esses
#    commits para o seu main.
ATUALIZAR_MAIN = None

"""Desafio: um portão de qualidade para a carga diária.

Todo dia, a carga de pedidos do dia chega num CSV e, depois de conferida, vai para o painel de
vendas. Você vai escrever as verificações de qualidade e o portão que decide o que fazer com a
carga: publicar, publicar com aviso, publicar sem as linhas ruins ou bloquear.

As verificações de linha devolvem uma Series de booleanos, alinhada com o DataFrame recebido:
True marca a linha que falhou. Assim, df[mascara] mostra as linhas com problema.

Regras:
- Use pandas. Nenhuma função pode alterar o que recebe.
- Não altere a pasta tests nem os arquivos em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import json

import pandas as pd


def ler_carga(caminho):
    """Já está pronta: lê a carga de pedidos, com as datas convertidas e cliente_id inteiro."""
    return pd.read_csv(caminho, dtype={"cliente_id": "Int64"}, parse_dates=["criado_em", "atualizado_em"])


def ler_regras(caminho):
    """Já está pronta: lê a lista de regras de qualidade do arquivo JSON."""
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def linhas_duplicadas(df, coluna):
    """Marca todas as linhas cujo valor na coluna aparece mais de uma vez (todas as cópias)."""
    raise NotImplementedError("Implemente a função linhas_duplicadas")


def linhas_nulas(df, coluna):
    """Marca as linhas em que a coluna está vazia."""
    raise NotImplementedError("Implemente a função linhas_nulas")


def linhas_fora_da_lista(df, coluna, valores):
    """Marca as linhas cujo valor na coluna não está na lista de valores aceitos.

    Valores vazios não contam como falha: isso é trabalho de linhas_nulas.
    """
    raise NotImplementedError("Implemente a função linhas_fora_da_lista")


def linhas_fora_do_intervalo(df, coluna, minimo=None, maximo=None):
    """Marca as linhas com valor menor que o mínimo ou maior que o máximo.

    Os limites valem como permitidos: um valor igual ao mínimo ou ao máximo passa. Se o mínimo
    ou o máximo for None, aquele lado não tem limite. Valores vazios não contam como falha.
    """
    raise NotImplementedError("Implemente a função linhas_fora_do_intervalo")


def linhas_orfas(df, coluna, chaves_validas):
    """Marca as linhas cujo valor na coluna não existe entre as chaves válidas.

    É a integridade referencial: um pedido que aponta para um cliente que não está no cadastro.
    Valores vazios não contam como falha.
    """
    raise NotImplementedError("Implemente a função linhas_orfas")


def atraso_em_horas(df, coluna, agora):
    """Horas entre o registro mais recente da coluna de data e hora e o momento agora."""
    raise NotImplementedError("Implemente a função atraso_em_horas")


def volume_anormal(historico, linhas_hoje, desvios=3):
    """Devolve True se a quantidade de linhas de hoje foge do padrão do histórico.

    historico é a lista de quantidades de linhas dos dias anteriores. Hoje é anormal quando
    fica a mais de `desvios` desvios padrão (amostral) da média do histórico, para cima ou
    para baixo.
    """
    raise NotImplementedError("Implemente a função volume_anormal")


def aplicar_regras(carga, regras, tabelas, chave="pedido_id"):
    """Aplica cada regra à carga e devolve a lista de resultados, na ordem das regras.

    Cada regra é um dicionário com "nome", "tipo", "coluna", "severidade" ("erro" ou "aviso")
    e os parâmetros do tipo:
    - "unico" e "nao_nulo": nenhum parâmetro a mais.
    - "valores_aceitos": "valores", a lista de valores aceitos.
    - "intervalo": "minimo" e "maximo", e qualquer um dos dois pode faltar.
    - "relacao": "tabela" e "coluna_referencia". A tabela de referência vem do dicionário
      tabelas, pelo nome. Ex.: tabelas["clientes"]["cliente_id"] são as chaves válidas.
    Cada resultado é {"regra": nome, "severidade": severidade, "falhas": ids}, em que ids é a
    lista dos valores da coluna chave das linhas que falharam, sem repetição e em ordem crescente.
    """
    raise NotImplementedError("Implemente a função aplicar_regras")


def separar_quarentena(carga, resultados, chave="pedido_id"):
    """Separa a carga em (aprovadas, quarentena).

    Vão para a quarentena todas as linhas cuja chave falhou em alguma regra de severidade
    "erro", inclusive todas as cópias de uma chave repetida. Falhas de "aviso" não mandam
    ninguém para a quarentena. Devolve dois DataFrames, com as linhas na ordem original.
    """
    raise NotImplementedError("Implemente a função separar_quarentena")


def decidir(resultados, total_pedidos, limite=0.05):
    """Decide o que fazer com a carga, a partir dos resultados das regras.

    - "publicar": nenhuma regra falhou.
    - "publicar_com_aviso": só regras de "aviso" falharam.
    - "publicar_sem_as_ruins": alguma regra de "erro" falhou, mas os pedidos com falha de erro,
      contados sem repetição, são no máximo `limite` do total de pedidos. As linhas ruins vão
      para a quarentena e o resto é publicado.
    - "bloquear": os pedidos com falha de erro passam do limite. Nada é publicado.
    """
    raise NotImplementedError("Implemente a função decidir")

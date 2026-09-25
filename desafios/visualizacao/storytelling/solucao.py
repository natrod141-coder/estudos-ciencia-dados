"""Desafio: do gráfico exploratório ao explicativo.

Implemente cada função abaixo. Leia a docstring de cada uma antes de começar.
A mensagem vem dos dados: nada de escrever números à mão no título ou no resumo.

Regras:
- Use pandas e matplotlib.
- A função de gráfico devolve a figura e não chama plt.show().
- Não altere a pasta tests nem o arquivo em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v

Para ver o gráfico enquanto trabalha:
    python -c "import solucao as s; s.grafico_explicativo(s.ler_vendas('data/vendas_por_canal.csv')).savefig('grafico.png')"
"""

import matplotlib.pyplot as plt  # noqa: F401  (será usado em grafico_explicativo)
import pandas as pd

COR_DESTAQUE = "#0f4c4a"  # a cor da mensagem
COR_CONTEXTO = "#b0b0b0"  # cinza, para o resto


def ler_vendas(caminho_csv):
    """Já está pronta: lê o faturamento mensal de cada canal (colunas mes, canal, faturamento)."""
    return pd.read_csv(caminho_csv)


def tabela_por_canal(vendas):
    """Devolve uma tabela com o mês no índice (em ordem), um canal por coluna (em ordem
    alfabética) e o faturamento em cada célula.
    """
    raise NotImplementedError("Implemente a função tabela_por_canal")


def mensagem_principal(vendas):
    """Encontra a mensagem principal dos dados: o canal que mais cresceu no ano.

    Compare o primeiro mês com o último. Devolve um dicionário com:
    - "canal": o canal com o maior crescimento percentual entre o primeiro e o último mês;
    - "crescimento_pct": esse crescimento, em %, arredondado para inteiro (um int);
    - "participacao_final_pct": a participação do canal no faturamento do último mês, em %,
      arredondada para 1 casa;
    - "virou_lider": True se o canal é o de maior faturamento no último mês (um bool).
    """
    raise NotImplementedError("Implemente a função mensagem_principal")


def titulo(mensagem):
    """Escreve o título do gráfico: uma frase que afirma a conclusão.

    Recebe o dicionário de mensagem_principal. Formatos:
    - se virou_lider: "O {canal} cresceu {crescimento_pct}% em 2025 e virou o maior canal de vendas"
    - senão: "O {canal} cresceu {crescimento_pct}% em 2025 e já responde por {participacao}% das vendas",
      com a participação escrita com vírgula decimal, como 38,5.
    """
    raise NotImplementedError("Implemente a função titulo")


def grafico_explicativo(vendas):
    """Gráfico de linhas que conta a história, e não só mostra os dados.

    - Uma linha por canal, com o faturamento mensal (em reais ou em milhares de reais).
    - Só a linha do canal da mensagem principal usa COR_DESTAQUE. As outras usam COR_CONTEXTO.
    - Sem legenda. No lugar dela, escreva o nome de cada canal ao lado do fim da sua linha,
      com ax.text(x, y, texto, color=...).
    - O título é a frase de titulo(mensagem_principal(vendas)).
    - Sem as bordas de cima e da direita: ax.spines[["top", "right"]].set_visible(False).
    - O eixo y diz a unidade, com "R$".
    Devolve a figura.
    """
    raise NotImplementedError("Implemente a função grafico_explicativo")


def resumo_executivo(vendas):
    """Escreve o resumo para quem decide, em três partes. Devolve um dicionário com:

    - "contexto": "Em 2025, as vendas somaram R$ {total} milhões nos três canais.", com o total
      de todos os meses e canais em milhões, arredondado para 1 casa e com vírgula decimal;
    - "achado": o título do gráfico, seguido de ponto final;
    - "recomendacao": uma frase sua, de até 200 caracteres, dizendo o que fazer com esse achado.
    """
    raise NotImplementedError("Implemente a função resumo_executivo")

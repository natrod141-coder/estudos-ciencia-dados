"""Desafio: um assistente que responde com base nas políticas da empresa.

As políticas internas estão em quatro documentos, em data/documentos: reembolso de despesas, home
office, férias e segurança da informação. Você vai montar o caminho completo de um RAG: dividir os
documentos em trechos, buscar os trechos certos para cada pergunta, montar o prompt com as fontes,
chamar o modelo e conferir se a resposta cita só o que foi enviado a ele.

O modelo é o ModeloGravado, de modelo_gravado.py, com a mesma cara do cliente do SDK da Anthropic e
respostas gravadas: o desafio roda sem chave de API e sem custo.

Regras:
- Use re, unicodedata, numpy e scikit-learn. Nenhuma função pode alterar o que recebe.
- Não altere modelo_gravado.py, a pasta tests nem os arquivos em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import re
import unicodedata
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

PASTA_DOCUMENTOS = Path(__file__).parent / "data" / "documentos"
NAO_ENCONTREI = "Não encontrei essa informação nos documentos."
PALAVRAS_VAZIAS = [
    "ao", "as", "até", "com", "como", "da", "das", "de", "do", "dos", "em", "na", "nas", "no", "nos", "não",
    "numa", "num", "os", "ou", "para", "pela", "pelo", "por", "posso", "qual", "que", "se", "uma", "um",
]


def ler_documentos():
    """Já está pronta: devolve {id do documento: texto}, um por arquivo .md em data/documentos."""
    return {arquivo.stem: arquivo.read_text(encoding="utf-8") for arquivo in sorted(PASTA_DOCUMENTOS.glob("*.md"))}


def criar_slug(texto):
    """Transforma um título em identificador: sem acentos, em minúsculas, com hífen no lugar de
    tudo o que não for letra ou número, e sem hífen nas pontas.
    Ex.: "Divisão em períodos" vira "divisao-em-periodos"."""
    raise NotImplementedError("Implemente a função criar_slug")


def dividir_em_trechos(doc_id, texto, max_caracteres=600):
    """Divide um documento em trechos, um por seção.

    O documento tem um título, numa linha que começa com "# ", e seções, que começam com "## ".
    Cada trecho é um dicionário com:
    - "id": f"{doc_id}#{slug da seção}";
    - "documento": doc_id; "titulo": o título do documento; "secao": o nome da seção;
    - "texto": os parágrafos da seção, sem o título, cada parágrafo numa linha só (troque as
      quebras de linha de dentro do parágrafo por espaço) e os parágrafos separados por "\\n\\n".
    Se o texto de uma seção passar de max_caracteres, divida a seção em vários trechos, juntando
    parágrafos inteiros enquanto couberem no limite, e acrescente "-1", "-2"... ao id.
    """
    raise NotImplementedError("Implemente a função dividir_em_trechos")


def indexar(trechos):
    """Prepara a busca por palavras nos trechos e devolve o índice, no formato que preferir.

    Use TfidfVectorizer(stop_words=PALAVRAS_VAZIAS) sobre o texto de cada trecho com o título e a
    seção na frente: f"{titulo}. {secao}. {texto}". O índice precisa guardar os trechos.
    """
    raise NotImplementedError("Implemente a função indexar")


def recuperar(indice, pergunta, k=3):
    """Devolve até k trechos (os dicionários) mais parecidos com a pergunta, pelo cosseno do
    TF-IDF, do mais parecido para o menos. Trechos com nota zero não entram."""
    raise NotImplementedError("Implemente a função recuperar")


def montar_mensagens(pergunta, trechos):
    """Devolve (system, messages) para a chamada ao modelo.

    system: as instruções. Diga para usar só os documentos, citar o id de onde veio cada
    informação entre colchetes, como [ferias#como-marcar], e, se a resposta não estiver nos
    documentos, responder exatamente o texto de NAO_ENCONTREI.
    messages: uma mensagem só, do usuário, neste formato:
        <documentos>
        <documento id="(id do trecho)">
        (título) > (seção)
        (texto)
        </documento>
        ... um bloco por trecho, na ordem recebida ...
        </documentos>

        <pergunta>
        (a pergunta)
        </pergunta>
    """
    raise NotImplementedError("Implemente a função montar_mensagens")


def extrair_citacoes(resposta):
    """Lista os ids citados entre colchetes na resposta, como [ferias#como-marcar], sem repetição
    e na ordem em que aparecem."""
    raise NotImplementedError("Implemente a função extrair_citacoes")


def checar_resposta(resposta, ids_enviados):
    """Confere a resposta. Devolve um dicionário com:
    - "citacoes": os ids citados;
    - "fora_do_contexto": os citados que não estão em ids_enviados (inventados, ou de trechos que
      o modelo não recebeu);
    - "sem_citacao": True se a resposta não cita nada e não é a recusa NAO_ENCONTREI;
    - "recusou": True se a resposta, sem os espaços das pontas, é exatamente NAO_ENCONTREI.
    """
    raise NotImplementedError("Implemente a função checar_resposta")


def responder(cliente, indice, pergunta, k=3, modelo="claude-opus-5-5"):
    """O caminho completo: recupera os trechos, monta as mensagens, chama
    cliente.messages.create(model=modelo, max_tokens=1024, system=..., messages=...), junta o
    texto dos blocos de tipo "text" e confere a resposta.

    Devolve {"resposta": texto, "trechos": ids dos trechos enviados, "checagem": checar_resposta}.
    Se a busca não encontrar nenhum trecho, não chame o modelo: a resposta é NAO_ENCONTREI.
    """
    raise NotImplementedError("Implemente a função responder")


def avaliar(cliente, indice, perguntas, k=3):
    """Roda responder para cada pergunta de data/perguntas.json e resume o resultado:
    - "recuperacao": entre as perguntas com trecho_relevante, a proporção em que esse trecho
      estava entre os enviados ao modelo;
    - "recusas", "sem_citacao", "fora_do_contexto" e "ok": os ids das perguntas, separados nesta
      ordem de prioridade: recusou; senão, sem citação; senão, com citação fora do contexto;
      senão, ok.
    """
    raise NotImplementedError("Implemente a função avaliar")

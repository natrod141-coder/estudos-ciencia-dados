"""Desafio: classificar avaliações de clientes pela API, sem desperdício.

Você vai escrever o código que manda cada avaliação para um modelo, lê a resposta, repete a
chamada quando a API está temporariamente indisponível, calcula o custo e evita pagar duas vezes
pela mesma avaliação.

Os testes usam o ClienteGravado, de cliente_gravado.py, que tem a mesma cara do cliente do SDK
da Anthropic, mas devolve respostas gravadas. O seu código não precisa saber a diferença.

Regras:
- Nenhuma função pode alterar o que recebe, a não ser o cache em classificar.
- Não altere cliente_gravado.py, a pasta tests nem os arquivos em data.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v
"""

import time

from cliente_gravado import ErroDaApi

ROTULOS = ("positivo", "negativo", "neutro")


def montar_requisicao(texto, modelo="claude-haiku-5-5"):
    """Monta os parâmetros da chamada a messages.create, como um dicionário.

    - "model": o modelo recebido.
    - "max_tokens": um teto pequeno, porque a resposta é uma palavra. Lembre que o raciocínio
      do modelo também gasta tokens de saída: 256 é um bom valor.
    - "output_config": {"effort": "low"}, porque a tarefa é simples.
    - "system": as instruções. Diga que a resposta é só uma palavra, entre positivo, negativo
      e neutro.
    - "messages": uma mensagem só, do usuário, com a avaliação entre <avaliacao> e </avaliacao>.
    Não envie temperature, top_p nem top_k: a API atual recusa esses parâmetros.
    """
    raise NotImplementedError("Implemente a função montar_requisicao")


def extrair_texto(resposta):
    """Junta o texto dos blocos de tipo "text" da resposta, na ordem.

    A resposta pode ter outros blocos, como os de raciocínio (tipo "thinking"), que não entram.
    Se não houver nenhum bloco de texto, devolve "".
    """
    raise NotImplementedError("Implemente a função extrair_texto")


def normalizar_rotulo(texto, stop_reason):
    """Transforma o texto da resposta num dos ROTULOS, ou em "invalido".

    - Se stop_reason não for "end_turn", a resposta não terminou direito: "invalido".
    - Tire os espaços e quebras de linha das pontas, passe para minúsculas e tire um ponto ou
      ponto de exclamação do final. Se sobrar um dos ROTULOS, devolva-o; senão, "invalido".
    """
    raise NotImplementedError("Implemente a função normalizar_rotulo")


def chamar_com_retentativas(cliente, requisicao, tentativas=4, espera_base=1.0, dormir=time.sleep):
    """Chama cliente.messages.create(**requisicao) e repete a chamada em erros temporários.

    Os erros da API são ErroDaApi, com o código HTTP em status_code, como em
    anthropic.APIStatusError. São temporários o 429 (limite de uso) e os códigos a partir de 500,
    como o 529 (API sobrecarregada). Qualquer outro erro, como o 400, sobe na hora: repetir não
    adianta. Depois da tentativa número i que falhou (contando do 0), espere
    espera_base * 2 ** i segundos chamando dormir. Se todas as tentativas falharem, deixe o
    último erro subir.
    """
    raise NotImplementedError("Implemente a função chamar_com_retentativas")


def custo_em_dolares(uso, precos):
    """Custo de uma chamada, a partir do usage da resposta e dos preços em dólares por milhão de tokens.

    precos tem as chaves "entrada", "saida", "escrita_cache" e "leitura_cache", que valem para
    os campos input_tokens, output_tokens, cache_creation_input_tokens e
    cache_read_input_tokens do uso. Campos ausentes ou com valor None contam como zero.
    """
    raise NotImplementedError("Implemente a função custo_em_dolares")


def classificar(cliente, textos, cache, precos, dormir=time.sleep):
    """Classifica cada texto e devolve (rotulos, custo_total).

    - Se o texto já está no cache (um dicionário texto -> rótulo), use o rótulo de lá, sem
      chamar a API.
    - Senão, monte a requisição, chame com retentativas (passando dormir adiante), some o custo,
      extraia e normalize o rótulo e guarde no cache. Rótulos "invalido" não vão para o cache:
      da próxima vez, vale a pena tentar de novo.
    rotulos tem um rótulo por texto, na mesma ordem.
    """
    raise NotImplementedError("Implemente a função classificar")

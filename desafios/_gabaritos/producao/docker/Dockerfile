# A imagem oficial do Python, na variante slim: só o essencial, bem menor que a completa.
# A versão fica fixa: python:latest mudaria de Python sem aviso.
FROM python:3.14-slim

# Sem arquivos .pyc e com a saída sem buffer, para os registros aparecerem na hora
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

# Primeiro só a lista de dependências: enquanto ela não mudar, o Docker reaproveita a camada
# da instalação, que é a mais demorada
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Depois o código, que muda toda hora
COPY app ./app

# Um usuário sem privilégios para rodar a API
RUN useradd --create-home api
USER api

# A porta padrão do Cloud Run; a forma exec do CMD deixa o servidor receber o aviso de
# desligamento e encerrar com calma
EXPOSE 8080
CMD ["fastapi", "run", "app/main.py", "--port", "8080"]

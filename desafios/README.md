# Desafios práticos

Cada desafio é uma pasta com o mesmo formato:

```
estatistica/tendencia_central/
  README.md            enunciado
  solucao.py           o arquivo que você edita
  data/                os dados do exercício
  tests/               testes automáticos (não altere)
  pytest.ini           configuração dos testes
```

## Como fazer um desafio

O passo a passo completo, com os comandos, aparece na página do tópico no site. Em resumo:

1. Prepare o ambiente uma vez só (na raiz do repositório):

   ```
   python -m venv .venv
   source .venv/bin/activate        # no Windows: .venv\Scripts\Activate.ps1
   pip install -r desafios/requirements.txt
   ```

2. Entre na pasta do desafio e rode os testes. No começo, todos falham. É o esperado.

   ```
   cd desafios/estatistica/tendencia_central
   pytest -v
   ```

3. Edite o `solucao.py` e rode os testes de novo a cada função pronta.
4. Quando todos passarem, registre o resultado na página do tópico. Isso cumpre o critério
   "desafio aprovado" do painel.

## A pasta `_gabaritos`

Guarda uma solução de referência de cada desafio. Consulte só depois de tentar. Se travar, leia com
calma a mensagem de erro do pytest antes de abrir o gabarito: ela mostra o valor esperado e o valor
que o seu código devolveu.

## Como criar um desafio novo

Copie a pasta de um desafio existente, troque o enunciado, os dados, o `solucao.py` e os testes, e
coloque a solução de referência em `_gabaritos/`. Depois aponte o tópico para a pasta do desafio, no
campo `desafio` do arquivo em `conteudo/topicos/`, e rode `python scripts/verificar_desafios.py`. Ele
confere três coisas: o `solucao.py` inicial faz todos os testes falharem, o gabarito faz todos
passarem, e a quantidade de testes é a mesma do campo `testes` do tópico. O gabarito pode ter mais
de um arquivo: o script copia a pasta inteira do gabarito por cima de uma cópia do desafio, como no
desafio de dbt, em que a solução são os modelos SQL e o YAML.

Dois cuidados que já apareceram:

- **Nomes de função que começam com "test".** Por padrão, o pytest trata como teste qualquer
  função cujo nome comece com "test", inclusive as importadas do `solucao.py`, como
  `teste_z_media`. Nesse caso, acrescente `python_functions = test_*` ao `pytest.ini` do desafio,
  como em `estatistica/teste_hipoteses/`.
- **Testes que aceitam mais de uma solução certa.** Teste o resultado, e não o caminho. Por
  exemplo, o desafio de gráficos aceita barras verticais ou horizontais, matplotlib direto ou o
  `.plot` do pandas. Antes de publicar, rode os testes também contra uma solução alternativa e contra
  uma solução com erros comuns, para ver se as mensagens de falha ajudam.

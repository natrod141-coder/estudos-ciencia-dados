---
titulo: "Conferir código gerado por IA"
modulo: fundamentos_ia
ordem: 3
horas: 3
estado: publicado
resumo: "Ler, testar e corrigir SQL e Python escritos pela IA antes de confiar no resultado."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Código que roda não é código certo"
    tipo: leitura
    minutos: 8
  - id: a2
    titulo: "Ler antes de rodar: o que procurar"
    tipo: leitura
    minutos: 12
  - id: a3
    titulo: "Testar com exemplos pequenos e contraexemplos"
    tipo: leitura
    minutos: 12
  - id: a4
    titulo: "Armadilhas comuns em SQL gerado por IA"
    tipo: leitura
    minutos: 12
  - id: a5
    titulo: "Pedir ajuda à IA do jeito certo"
    tipo: leitura
    minutos: 8
  - id: a6
    titulo: "Vídeo de apoio: revisão de código gerado por IA"
    tipo: video
    minutos: 15
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Para a taxa de conversão do mês, a IA escreveu (df['pedidos'] / df['visitas']).mean(), com uma linha por dia. Qual é o problema?"
    opcoes: ["Nenhum, a média das taxas diárias é igual à taxa do mês", "A média das taxas diárias dá o mesmo peso a um dia com 100 visitas e a um dia com 10.000; a taxa do mês é o total de pedidos dividido pelo total de visitas", "Falta arredondar o resultado para duas casas", "O código deveria usar a mediana em vez da média"]
    correta: 1
    explicacao: "Média de razões não é razão de totais. Com 10 pedidos em 100 visitas num dia e 20 em 1.000 no outro, a média das taxas dá 6%, mas o mês teve 30 pedidos em 1.100 visitas: 2,7%. O código roda, o número parece razoável, e está errado."
  - pergunta: "Depois que a IA juntou a tabela de pedidos com a de itens usando merge, o faturamento total ficou maior do que o do relatório oficial. Qual é a causa mais provável?"
    opcoes: ["O merge arredondou os valores para cima", "A tabela de itens tem valores negativos", "O pandas soma errado em tabelas grandes", "Cada pedido com vários itens apareceu em várias linhas, e o valor do pedido foi somado mais de uma vez"]
    correta: 3
    explicacao: "Ao juntar uma tabela com uma linha por pedido a uma tabela com uma linha por item, cada pedido se repete uma vez para cada item. Somar ou tirar a média do valor do pedido depois disso conta o mesmo pedido várias vezes. Comparar a quantidade de linhas antes e depois do merge revela o problema."
  - pergunta: "A consulta SELECT nome FROM clientes WHERE cliente_id NOT IN (SELECT cliente_id FROM pedidos) não devolveu nenhuma linha, mas você sabe que há clientes sem pedido. O que explica isso?"
    opcoes: ["Algum pedido tem cliente_id nulo, e um NOT IN com um nulo na lista nunca dá verdadeiro", "Faltou um ORDER BY na consulta", "O NOT IN só funciona com textos", "A tabela de clientes está vazia"]
    correta: 0
    explicacao: "Com um NULL na lista, o banco não consegue afirmar que um valor não está nela, e a condição fica desconhecida para todas as linhas. NOT EXISTS ou um LEFT JOIN com IS NULL não têm esse problema."
  - pergunta: "A IA escreveu uma função que soma as vendas de um mês. Qual é o melhor jeito de testá-la antes de usar?"
    opcoes: ["Rodar com a base inteira e ver se não deu erro", "Perguntar à IA se o código está correto", "Montar à mão uma tabela pequena, com casos de borda como uma venda às 23h do último dia, e comparar o resultado com a soma feita por você", "Ler a docstring e conferir se ela descreve bem a função"]
    correta: 2
    explicacao: "Rodar sem erro não prova nada, e a IA pode confirmar um código errado com a mesma segurança. Um exemplo pequeno, em que você sabe a resposta, com os casos que costumam quebrar, mostra o erro na hora."
  - pergunta: "A IA montou a consulta colando, com um f-string, o nome da região digitado pelo usuário dentro do texto do SQL. Qual é o risco?"
    opcoes: ["Nenhum, o f-string deixa a consulta mais rápida", "O texto digitado vira parte do SQL: um apóstrofo quebra a consulta, e um texto malicioso pode mudar o que ela faz; o certo é passar o valor como parâmetro", "A consulta só funciona com regiões em maiúsculas", "O SQLite não aceita f-strings"]
    correta: 1
    explicacao: "Montar SQL colando texto de fora é a porta da injeção de SQL. Com parâmetros, como WHERE regiao = ? e o valor passado separado, o banco trata o texto sempre como valor, e nunca como parte do comando."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Você pediu à IA uma função que calcula o ticket médio por categoria de produto, a partir das tabelas de pedidos e de itens, e ela entregou um código que roda sem erro. Descreva, passo a passo, como você conferiria esse código antes de usar o resultado num relatório."
  rubrica:
    - "Lê o código conferindo a granularidade: se juntar pedidos com itens repete cada pedido, e se a média é calculada com uma linha por pedido."
    - "Monta um exemplo pequeno, à mão, com resposta conhecida e com casos de borda, como um pedido com dois itens da mesma categoria ou uma categoria sem pedidos, e compara com o resultado da função."
    - "Confere por outro caminho, como uma consulta SQL ou uma conta independente, ou com um invariante, como a quantidade de linhas antes e depois do merge, e guarda os exemplos como testes."
  modelo: "Primeiro, eu leria o código pensando na granularidade. A tabela de pedidos tem uma linha por pedido e a de itens tem uma linha por item. Se o código junta as duas e tira a média do valor do pedido, um pedido com três itens da categoria entra três vezes na média. Eu conferiria se o código tira as repetições antes de calcular. Depois, montaria um exemplo pequeno à mão: dois pedidos de livros, um de 100 reais com dois livros e outro de 300 com um livro. O ticket médio certo é 200. Se a função devolver 166,67, ela está contando o primeiro pedido duas vezes. Também testaria uma categoria sem nenhum pedido, para ver se a função quebra ou devolve algo que faça sentido. Em seguida, calcularia o mesmo número por outro caminho, por exemplo com uma consulta SQL no banco, e compararia. Durante a conferência, olharia a quantidade de linhas antes e depois do merge. Por fim, guardaria esses exemplos como testes com pytest, para que uma mudança futura no código não traga o erro de volta."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Revisar o código que a IA escreveu"
  descricao: "Um assistente de IA escreveu seis funções para o relatório de vendas. Todas rodam sem erro no exemplo que ele testou, e todas têm um problema. Para cada função, você vai encontrar o caso em que ela erra, registrar esse caso como contraexemplo e escrever a versão corrigida."
  pasta: "desafios/fundamentos_ia/conferir_codigo_gerado"
  testes: 12
  tempo: "1 h 30 min"
  ferramentas: "VS Code, Python 3.11 ou superior, pandas e pytest"
  entrega: "Pull Request no GitHub"
  passos:
    - titulo: "Clone o repositório"
      descricao: "Só na primeira vez. Se já clonou, pule para o passo 2."
      comandos:
        - "git clone https://github.com/[seu_usuario]/[repositorio].git"
        - "cd [repositorio]"
    - titulo: "Abra o repositório no VS Code"
      descricao: "Se o VS Code oferecer Reopen in Container, aceite: o ambiente já vem pronto e você pode pular o passo 3."
      comandos:
        - "code ."
    - titulo: "Crie e ative o ambiente virtual"
      descricao: "Abra o terminal do VS Code com Ctrl+` (acento grave). Depois use Ctrl+Shift+P, Python: Select Interpreter, e escolha o .venv."
      comandos:
        - "# Linux ou macOS"
        - "python3 -m venv .venv"
        - "source .venv/bin/activate"
        - "# Windows (PowerShell)"
        - "python -m venv .venv"
        - '.venv\Scripts\Activate.ps1'
        - "pip install -r desafios/requirements.txt"
    - titulo: "Leia o enunciado e o código da IA"
      descricao: "Abra desafios/fundamentos_ia/conferir_codigo_gerado/README.md e depois codigo_da_ia.py. A docstring de cada função é o pedido feito ao assistente. Não altere esse arquivo."
    - titulo: "Registre os contraexemplos e corrija as funções em solucao.py"
      descricao: "Para cada função, um caso em que a versão da IA erra, em CONTRAEXEMPLOS, e a versão corrigida, com o mesmo nome e os mesmos parâmetros. Não altere a pasta tests."
      codigo: true
      comandos:
        - "CONTRAEXEMPLOS = {...}"
        - "def taxa_de_conversao(diario):"
        - "def ticket_medio_categoria(pedidos, itens, categoria):"
        - "def limpar_valor(texto):"
        - "def variacao_percentual(atual, anterior):"
        - "def vendas_do_mes(vendas, ano, mes):"
        - "def clientes_sem_pedido(clientes, pedidos):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "Seis testes conferem as suas versões corrigidas, e seis conferem se cada contraexemplo mostra o erro da IA."
      comandos:
        - "cd desafios/fundamentos_ia/conferir_codigo_gerado"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/conferir_codigo_gerado"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de conferir código gerado por IA"'
        - "git push -u origin desafio/conferir_codigo_gerado"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Revisão de código", en: "code review" }
  - { pt: "Caso de borda", en: "edge case" }
  - { pt: "Contraexemplo", en: "counterexample" }
  - { pt: "Teste unitário", en: "unit test" }
  - { pt: "Asserção", en: "assertion" }
  - { pt: "Granularidade", en: "grain" }
  - { pt: "Duplicação de linhas no join", en: "join fan-out" }
  - { pt: "Valor nulo", en: "null value" }
  - { pt: "Divisão inteira", en: "integer division" }
  - { pt: "Injeção de SQL", en: "SQL injection" }
  - { pt: "Consulta parametrizada", en: "parameterized query" }
  - { pt: "Invariante", en: "invariant" }
---

## Código que roda não é código certo

Pedir código a um assistente de IA virou rotina em análise de dados: uma consulta SQL, uma limpeza em pandas, um gráfico. Na maioria das vezes, o código vem bem escrito, com nomes claros e comentários, e roda de primeira. É justamente aí que mora o risco.

Os erros que mais importam em dados **não levantam exceção**. Uma média calculada do jeito errado devolve um número. Um merge que duplica linhas devolve uma tabela. Um filtro de data que perde o último dia do mês devolve um total. Todos com cara de resultado certo. Um erro que quebra o programa é o caso bom, porque você percebe na hora.

O código gerado por IA tem alguns pontos fracos conhecidos. O modelo não conhece os seus dados, então supõe a granularidade das tabelas, os formatos e as regras de negócio. Ele tende a escrever o caso comum e esquecer os casos de borda. E, quando testa, testa com o exemplo simples que ele mesmo imaginou.

Por isso, vale uma regra simples: **quem assina a análise é você**. O código da IA é um rascunho de um colega rápido e pouco cuidadoso, e precisa de revisão antes de virar número em relatório.

## Ler antes de rodar: o que procurar

Ler o código com uma lista de perguntas em mente pega a maior parte dos problemas:

1. **Faz o que foi pedido?** Compare o pedido com o código, linha a linha. "Taxa do mês" é total de pedidos dividido por total de visitas, e não a média das taxas diárias.
2. **As colunas existem e significam o que o código supõe?** Uma coluna `valor` pode ser o valor do item ou o valor do pedido.
3. **Qual é a granularidade de cada tabela?** Uma linha por pedido, por item, por dia, por cliente? Juntar tabelas de granularidades diferentes multiplica linhas.
4. **As agregações fazem sentido?** Média de médias, média de razões e soma de percentuais quase sempre estão erradas.
5. **Os filtros pegam tudo o que deveriam?** Datas com horário, intervalos que incluem ou não o último dia, valores nulos nas condições.
6. **E nos casos de borda?** Divisão por zero, tabela vazia, valor faltando, número escrito no formato brasileiro, como `R$ 1.234,56`.
7. **As bibliotecas e funções existem?** O modelo pode usar uma função que não existe, ou que mudou de nome na versão instalada. Antes de instalar um pacote sugerido pela IA, confira se ele existe e se é o pacote certo: há quem publique pacotes maliciosos com os nomes que os modelos costumam inventar.
8. **É seguro?** SQL montado colando texto de fora, chaves de API escritas no código, comandos que apagam arquivos ou tabelas.

O exemplo mais comum do item 4, em código:

```python
import pandas as pd

diario = pd.DataFrame({"visitas": [100, 1000], "pedidos": [10, 20]})

taxas = diario["pedidos"] / diario["visitas"]
print(round(taxas.mean(), 4))  # 0.06: média das taxas, errado

total = diario["pedidos"].sum() / diario["visitas"].sum()
print(round(total, 4))  # 0.0273: taxa do período, certo
```

## Testar com exemplos pequenos e contraexemplos

Ler encontra muita coisa, mas a prova vem de rodar o código num caso em que você **já sabe a resposta**. A técnica é simples:

1. Monte à mão uma tabela pequena, com três a cinco linhas.
2. Inclua de propósito os casos que costumam quebrar: o pedido com dois itens, a venda às 23h do último dia, o valor zero, a célula vazia.
3. Calcule a resposta certa no papel.
4. Rode o código e compare.

Um caso em que o código erra é um **contraexemplo**. Ele vale mais que qualquer explicação: mostra o erro de forma que ninguém discute. No desafio, você vai registrar um contraexemplo para cada função da IA.

Outra ferramenta é o **invariante**: algo que precisa ser verdade se o código estiver certo. Depois de juntar pedidos com itens, cada pedido deveria aparecer quantas vezes? A soma das partes bate com o total? Os percentuais somam 100%? No pandas, o merge confere a granularidade sozinho, se você pedir:

```python
# cada item aponta para exatamente um pedido; se um pedido
# estiver repetido na tabela de pedidos, o merge dá erro
juntos = itens.merge(pedidos, on="pedido_id", validate="many_to_one")

print(len(itens), len(juntos))  # devem ser iguais
```

Por fim, transforme os exemplos em **testes**. Com pytest, cada exemplo vira uma função curta, que roda de novo sempre que o código mudar:

```python
def test_limpar_valor_com_separador_de_milhar():
    assert limpar_valor("R$ 1.234,56") == 1234.56
```

Também ajuda calcular o mesmo número por outro caminho, por exemplo com SQL e com pandas, e comparar. Dois caminhos independentes que chegam ao mesmo resultado dão bem mais confiança do que um só.

## Armadilhas comuns em SQL gerado por IA

Alguns erros aparecem com tanta frequência em SQL que vale procurá-los sempre.

**NOT IN com valor nulo.** Se a subconsulta tiver um único NULL, o `NOT IN` não devolve nenhuma linha. Prefira `NOT EXISTS`:

```sql
-- se algum cliente_id em pedidos for NULL, não devolve nada
SELECT nome
FROM clientes
WHERE cliente_id NOT IN (SELECT cliente_id FROM pedidos);

-- NOT EXISTS não tem esse problema
SELECT c.nome
FROM clientes AS c
WHERE NOT EXISTS (
    SELECT 1 FROM pedidos AS p WHERE p.cliente_id = c.cliente_id
);
```

**`COUNT(coluna)` e `COUNT(*)`.** `COUNT(email)` conta só as linhas com e-mail preenchido. `COUNT(*)` conta todas.

**Divisão inteira.** Em bancos como SQLite e PostgreSQL, `7 / 2` dá 3, porque os dois números são inteiros. Para a divisão com decimais, multiplique por `1.0` antes de dividir.

**Intervalos de data com horário.** `WHERE data <= '2026-03-31'` deixa de fora as vendas de 31 de março depois da meia-noite, quando a coluna tem data e hora. O filtro seguro é `WHERE data >= '2026-03-01' AND data < '2026-04-01'`.

**Soma depois de um JOIN.** A mesma duplicação do merge do pandas: juntar pedidos com itens e somar o valor do pedido conta cada pedido uma vez por item.

**SQL montado com texto de fora.** Colar no SQL um valor digitado pelo usuário abre espaço para a injeção de SQL, e um simples apóstrofo, como em "Pau d'Arco", já quebra a consulta. Passe o valor como parâmetro:

```python
# perigoso: o texto digitado vira parte do comando
sql = f"SELECT * FROM vendas WHERE regiao = '{regiao}'"

# seguro: o valor vai separado, como parâmetro
sql = "SELECT * FROM vendas WHERE regiao = ?"
linhas = conexao.execute(sql, (regiao,)).fetchall()
```

E, como no tópico anterior: SQL escrito por IA roda com um usuário **só de leitura**.

## Pedir ajuda à IA do jeito certo

A IA continua sendo uma ótima parceira para escrever e revisar código, desde que você use do jeito certo:

- **Dê o contexto antes de pedir.** O esquema das tabelas, a granularidade de cada uma, algumas linhas de exemplo e as regras de negócio. Boa parte dos erros acima vem de suposições que o contexto evita.
- **Peça em partes pequenas.** Uma função por vez é mais fácil de revisar do que um script de duzentas linhas.
- **Peça as suposições.** "Liste as suposições que você fez sobre os dados" costuma revelar o problema antes de você rodar qualquer coisa.
- **Peça testes, e revise os testes.** Testes escritos pela IA tendem a cobrir só o caso simples, e às vezes copiam como "esperado" o resultado do próprio código, o que não testa nada.
- **Peça uma revisão, mas não pare nela.** Uma segunda conversa revisando o código encontra erros, mas também deixa passar. Os seus exemplos à mão continuam sendo a prova.

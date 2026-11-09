---
titulo: "Limites e alucinação"
modulo: fundamentos_ia
ordem: 2
horas: 3
estado: publicado
resumo: "Por que o modelo erra com confiança e em que tipo de tarefa de dados isso costuma acontecer."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "O que é alucinação e por que acontece"
    tipo: leitura
    minutos: 12
  - id: a2
    titulo: "Onde o modelo mais erra em tarefas de dados"
    tipo: leitura
    minutos: 12
  - id: a3
    titulo: "Como reduzir o risco"
    tipo: leitura
    minutos: 12
  - id: a4
    titulo: "Conferir antes de usar"
    tipo: leitura
    minutos: 10
  - id: a5
    titulo: "Vídeo de apoio: alucinação em modelos de linguagem"
    tipo: video
    minutos: 15
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "O que é uma alucinação de um LLM?"
    opcoes: ["Uma resposta que o modelo se recusa a dar", "Um erro de digitação na pergunta do usuário", "Uma resposta fluente e confiante, mas falsa ou sem base nos dados", "Uma resposta lenta, por causa de um modelo sobrecarregado"]
    correta: 2
    explicacao: "Alucinação é quando o modelo produz algo que parece certo, com boa redação e tom seguro, mas que é falso ou não tem base: um número inventado, uma coluna que não existe, uma citação que ninguém escreveu."
  - pergunta: "Por que o tom confiante de uma resposta não indica que ela está certa?"
    opcoes: ["Porque o modelo escreve com o mesmo tom quando acerta e quando inventa: ele gera o texto mais plausível, e o tom faz parte do texto", "Porque os modelos são treinados para errar de propósito", "Porque o tom confiante só aparece quando a temperatura está alta", "Porque respostas confiantes sempre vêm de dados desatualizados"]
    correta: 0
    explicacao: "O modelo aprendeu a escrever como textos bem escritos, e textos bem escritos costumam ter tom seguro. Uma frase inventada sai com a mesma fluência de uma frase verdadeira. O que dá confiança é a fonte conferida, e não o jeito de escrever."
  - pergunta: "Qual destas tarefas tem mais risco de erro se o modelo responder direto no texto, sem rodar código?"
    opcoes: ["Explicar a diferença entre WHERE e HAVING", "Sugerir nomes mais claros para as colunas de uma tabela", "Reescrever um e-mail em tom mais formal", "Somar os 300 valores de uma coluna colada na conversa"]
    correta: 3
    explicacao: "Contas longas são um ponto fraco: os números viram vários tokens, e o modelo não faz a soma como uma calculadora. O resultado pode sair perto do certo, mas errado. Para contas, peça o código ou a consulta e rode você mesmo."
  - pergunta: "O assistente respondeu que o Centro-Oeste faturou R$ 96.300,00 em junho e mostrou a consulta. Você rodou a consulta e ela devolveu NULL. O que isso indica?"
    opcoes: ["Que o banco está com defeito, e a resposta do modelo deve estar certa", "Que não existe nenhuma linha dessa região no período: o número da resposta foi inventado", "Que o modelo arredondou o valor", "Que faltou um ORDER BY na consulta"]
    correta: 1
    explicacao: "SUM sobre nenhuma linha devolve NULL. Se a base não tem vendas dessa região, qualquer número na resposta foi inventado. É um caso típico: em vez de dizer que o dado não existe, o modelo preencheu a lacuna com um valor plausível."
  - pergunta: "Qual destas instruções no prompt mais ajuda a reduzir respostas inventadas sobre um documento interno?"
    opcoes: ["Pedir que seja criativo e completo na resposta", "Pedir que responda sempre, mesmo sem certeza", "Pedir que use só o documento, copie o trecho que sustenta cada afirmação e diga quando a resposta não estiver nele", "Pedir que responda em no máximo uma frase"]
    correta: 2
    explicacao: "Limitar a resposta ao documento, exigir o trecho literal e dar permissão para dizer que não encontrou atacam as três causas mais comuns: falta de contexto, falta de fonte e a pressão para responder de qualquer jeito. E o trecho citado pode ser conferido depois."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Seu gestor quer usar um assistente de IA para responder às perguntas do time comercial sobre faturamento. Descreva três riscos de alucinação nesse uso e, para cada um, uma forma de reduzir o risco ou de detectar o erro."
  rubrica:
    - "Cita pelo menos um risco ligado a números, como contas feitas de cabeça ou um valor inventado para um dado que não existe, e propõe que os números venham de consultas executadas e conferidas no banco."
    - "Cita pelo menos um risco ligado a fontes ou regras de negócio, como uma citação inventada ou uma definição de faturamento suposta, e propõe exigir o trecho literal da fonte e conferi-lo."
    - "Propõe pelo menos uma salvaguarda de processo: permitir que o modelo diga que não sabe, dar acesso só de leitura ao banco ou revisar os números antes de irem para um relatório."
  modelo: "Primeiro risco: números errados. O modelo pode somar de cabeça e errar, ou inventar um valor para uma região ou um período que nem estão na base. Para reduzir, o assistente deve escrever a consulta SQL em vez de calcular, a consulta deve rodar no banco, e o número da resposta deve vir do resultado. Uma consulta que devolve NULL é sinal de que o dado não existe. Segundo risco: regras de negócio inventadas. Sem o documento de regras, o modelo supõe a definição mais comum, por exemplo que o frete entra no faturamento, e pode até citar um trecho que não existe. Para reduzir, o documento de regras vai junto na conversa, e o assistente precisa copiar o trecho que sustenta cada resposta. Esse trecho é procurado no documento antes de a resposta ser usada. Terceiro risco: responder o que não sabe. Se o prompt não der saída, o modelo tende a responder qualquer coisa. Para reduzir, a instrução diz explicitamente que ele pode responder que não encontrou a informação. Por segurança, o assistente acessa o banco com um usuário só de leitura, e números que vão para a diretoria passam por uma pessoa antes."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Conferir as respostas do assistente"
  descricao: "Um assistente de IA respondeu a dez perguntas do time comercial, mostrando a consulta SQL que usou ou citando o documento de regras. Você vai escrever um verificador que roda cada consulta, compara o número do texto com o resultado, procura cada citação no documento e separa as respostas em corretas, com valor errado, com SQL inválida, com citação inventada e sem fonte."
  pasta: "desafios/fundamentos_ia/limites_alucinacao"
  testes: 10
  tempo: "1 h 30 min"
  ferramentas: "VS Code, Python 3.11 ou superior e pytest"
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
    - titulo: "Leia o enunciado e conheça os dados"
      descricao: "Abra desafios/fundamentos_ia/limites_alucinacao/README.md. Em data estão o CSV de vendas, o documento de regras e as respostas gravadas do assistente."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "A função criar_banco já está pronta. Cada função tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def extrair_numeros(texto):"
        - "def valores_conferem(afirmado, real, tolerancia=0.01):"
        - "def executar_consulta(conexao, sql):"
        - "def citacao_existe(citacao, documento):"
        - "def classificar_resposta(resposta, conexao, documento):"
        - "def relatorio(respostas, conexao, documento):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/fundamentos_ia/limites_alucinacao"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/limites_alucinacao"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de limites e alucinação"'
        - "git push -u origin desafio/limites_alucinacao"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Alucinação", en: "hallucination" }
  - { pt: "Fundamentação em fontes", en: "grounding" }
  - { pt: "Citação", en: "citation" }
  - { pt: "Data de corte do conhecimento", en: "knowledge cutoff" }
  - { pt: "Verificação de fatos", en: "fact-checking" }
  - { pt: "Uso de ferramentas", en: "tool use" }
  - { pt: "Execução de código", en: "code execution" }
  - { pt: "Saída estruturada", en: "structured output" }
  - { pt: "Esquema da tabela", en: "table schema" }
  - { pt: "Acesso só de leitura", en: "read-only access" }
  - { pt: "Revisão humana", en: "human in the loop" }
---

## O que é alucinação e por que acontece

**Alucinação** é o nome dado a uma resposta fluente, confiante e errada. O modelo inventa um número, uma coluna que não existe na tabela, uma função de biblioteca, uma referência, uma citação "entre aspas" que ninguém escreveu. O texto em volta está bem escrito, o tom é seguro, e nada na resposta avisa que aquele trecho foi inventado.

Para entender por que isso acontece, lembre do tópico anterior: o modelo gera o texto **mais plausível** para continuar a conversa. Na grande maioria das vezes, o texto plausível também é o verdadeiro. Mas, quando a informação não está na conversa e o modelo não a aprendeu bem no treino, a continuação plausível ainda existe: tem o formato certo, o vocabulário certo, a ordem de grandeza certa. Só não é verdade.

Algumas situações aumentam muito a chance de alucinação:

- **Falta de contexto.** O modelo não conhece as suas tabelas, as suas regras de negócio nem os seus documentos, a não ser que estejam na conversa.
- **Informação rara ou recente.** Assuntos pouco presentes no treino, ou posteriores à data de corte, viram terreno para palpite.
- **Pressão para responder.** Os modelos são treinados para serem úteis. Se a pergunta pressupõe que a resposta existe, como "qual foi o faturamento do Centro-Oeste?", o modelo tende a responder, mesmo quando o certo seria dizer que o dado não existe.
- **Tarefas que exigem precisão mecânica.** Contas longas, contagem de itens, cópia exata de textos grandes.

O ponto mais importante: **o tom não diz nada sobre a correção**. O modelo escreve "o faturamento foi de R$ 4.180.000,00" com a mesma segurança quando acerta e quando erra, porque o tom também faz parte do texto plausível. Os modelos atuais alucinam bem menos do que os primeiros e são treinados para admitir quando não sabem, mas o risco não chega a zero. Em trabalho com dados, o que dá confiança é uma fonte que você conferiu.

## Onde o modelo mais erra em tarefas de dados

Alguns erros aparecem com tanta frequência em análise de dados que vale conhecer cada um pelo nome.

**Contas feitas "de cabeça".** Peça para o modelo somar uma coluna colada na conversa, e ele pode chegar perto, mas errar. No desafio deste tópico, o assistente afirma que o semestre faturou R$ 4.180.000,00. A consulta no banco dá R$ 4.104.084,05: quase 2% de diferença, com cara de número certo.

**Esquema inventado.** Sem ver a estrutura da tabela, o modelo escreve SQL com nomes prováveis: `data_venda` em vez de `dt_pedido`, `ticket_medio` numa tabela que não tem essa coluna, `clientes` quando a tabela se chama `cadastro_cliente`. Às vezes a consulta falha, o que é o caso bom, porque você percebe. O caso ruim é quando a coluna inventada existe com outro significado.

**Dado que não existe.** Pergunte sobre uma região, um produto ou um período que não está na base, e o modelo pode dar um número mesmo assim. Uma consulta ajuda a desmascarar esse caso:

```sql
SELECT SUM(faturamento)
FROM vendas
WHERE regiao = 'Centro-Oeste';
-- devolve NULL: não existe nenhuma linha dessa região
```

**Citações e referências.** Trechos "copiados" de um documento que não estão nele, links que levam a lugar nenhum, artigos que nunca foram publicados, funções de biblioteca com nomes plausíveis que não existem ou mudaram de nome em versões recentes.

**Regras de negócio supostas.** "Faturamento" inclui o frete? Pedido cancelado sai do mês em que foi feito ou do mês do cancelamento? Sem o documento da empresa, o modelo usa a definição mais comum, que pode não ser a sua.

**Detalhes perdidos em contexto longo.** Mesmo com uma janela de contexto grande, uma informação no meio de um documento extenso pode ser ignorada ou misturada com outra parecida.

## Como reduzir o risco

Nenhuma técnica elimina a alucinação, mas várias reduzem bastante a chance, e todas seguem a mesma ideia: **trocar a memória do modelo por fontes que você controla**.

**Dar o contexto.** Para perguntas sobre dados, envie o esquema das tabelas, os valores possíveis das colunas de categoria e algumas linhas de exemplo. Para perguntas sobre regras, envie o documento.

**Separar o raciocínio da conta.** Em vez de pedir o número, peça a consulta ou o código, e rode você mesmo, ou dê ao modelo uma ferramenta que execute a consulta. O número passa a vir do banco, e não da memória do modelo. Você vai fazer isso nos módulos de APIs de LLM e de IA sobre dados.

```text
Esquema da tabela:
CREATE TABLE vendas (mes TEXT, regiao TEXT, faturamento REAL)
-- mes no formato 'AAAA-MM'; regiões: Norte, Nordeste, Sudeste, Sul

Escreva a consulta SQL que responde à pergunta. Não calcule o
resultado: eu vou rodar a consulta. Se a pergunta pedir um dado
que não existe no esquema, diga isso em vez de inventar.
```

**Exigir a fonte e permitir o "não sei".** Peça que cada afirmação venha com o trecho literal que a sustenta, e diga explicitamente que o modelo pode responder que não encontrou a informação. Sem essa saída, a pressão para responder fala mais alto.

```text
Responda usando apenas o documento entre as marcações <documento>.
Para cada afirmação, copie entre aspas o trecho do documento que
a sustenta. Se o documento não responder à pergunta, escreva
"não encontrei essa informação no documento" e não tente adivinhar.

<documento>
(o texto das regras do relatório)
</documento>

Pergunta: um pedido cancelado depois de duas semanas
sai do faturamento?
```

Algumas APIs ajudam nessa parte. A do Claude, por exemplo, tem um recurso de **citações**: você envia o documento, e a resposta vem com os trechos exatos que a sustentam, apontando para o próprio documento.

**Pedir respostas estruturadas.** Uma resposta em formato fixo, com campos como `valor`, `consulta_sql` e `trecho_citado`, pode ser conferida por código, como você vai fazer no desafio.

**Buscar antes de responder.** Quando o material é grande demais para caber na conversa, um sistema busca os trechos relevantes e envia só eles ao modelo. Essa técnica, a RAG, tem um módulo inteiro mais adiante.

## Conferir antes de usar

Mesmo com tudo isso, a regra é conferir antes de usar, com mais cuidado quanto maior o impacto da resposta. Uma dúvida durante uma exploração pede pouca conferência. Um número que vai para a diretoria pede muita.

Um roteiro para conferir respostas sobre dados:

1. **Números: rode a consulta você mesmo.** Compare o resultado com o número do texto. Um arredondamento pequeno é normal. Uma diferença de alguns por cento não é.
2. **Citações: procure o trecho na fonte.** Com Ctrl+F no documento, ou com código, como no desafio. Uma citação inventada é motivo para desconfiar da resposta inteira.
3. **Esquema: confira se as colunas e tabelas existem** e se significam o que a resposta supõe.
4. **Ordem de grandeza: compare com um número que você conhece.** O total do mês bate com o relatório oficial? As partes somam o todo? Os percentuais somam 100%?
5. **Respostas sem fonte: trate como hipótese.** Não estão necessariamente erradas, mas ainda não foram conferidas.

A primeira conferência cabe em poucas linhas de Python:

```python
import sqlite3

conexao = sqlite3.connect("vendas.db")
sql = "SELECT SUM(faturamento) FROM vendas WHERE regiao = 'Sul'"
real = conexao.execute(sql).fetchone()[0]

afirmado = 1_200_000.00  # o número que o modelo escreveu
diferenca = abs(afirmado - real) / real
print(f"diferença de {diferenca:.1%}")  # diferença de 11.4%
```

Uma última precaução, de segurança: SQL escrito por um modelo deve rodar com um **usuário só de leitura**. Uma consulta mal interpretada que apaga ou altera dados é um erro bem mais caro do que um número errado num rascunho.

---
titulo: "Testes de qualidade de dados"
modulo: analytics_eng
ordem: 2
horas: 6
estado: publicado
resumo: "Garantir unicidade, chaves válidas e valores esperados antes que o número chegue ao painel."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Por que testar os dados, e não só o código"
    tipo: leitura
    minutos: 8
  - id: a2
    titulo: "As dimensões da qualidade"
    tipo: leitura
    minutos: 12
  - id: a3
    titulo: "Onde e quando testar"
    tipo: leitura
    minutos: 12
  - id: a4
    titulo: "Ferramentas"
    tipo: leitura
    minutos: 10
  - id: a5
    titulo: "Quando um teste falha"
    tipo: leitura
    minutos: 10
  - id: a6
    titulo: "Vídeo de apoio: qualidade de dados na prática"
    tipo: video
    minutos: 20
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "O painel de vendas mostra o mesmo número há três dias, e ninguém percebeu que a carga diária parou de chegar. Que tipo de teste teria avisado?"
    opcoes: ["Atualidade: conferir se o registro mais recente é de menos de um dia atrás", "Unicidade da chave dos pedidos", "Valores aceitos na coluna de status", "Integridade entre pedidos e clientes"]
    correta: 0
    explicacao: "Os dados velhos continuam válidos, únicos e íntegros, então os testes de coluna passam. Só um teste de atualidade, que mede há quanto tempo chegou o último registro, percebe que a carga parou."
  - pergunta: "Numa tabela com uma linha por pedido, o mesmo pedido aparece duas vezes, porque o sistema reenviou o evento. Que dimensão da qualidade foi violada?"
    opcoes: ["Atualidade", "Unicidade", "Completude", "Volume"]
    correta: 1
    explicacao: "Cada pedido deveria aparecer uma vez só. Um teste de unicidade na chave da tabela pega o reenvio antes que o faturamento seja contado em dobro."
  - pergunta: "Ontem a carga trouxe 40 mil linhas; hoje, 9 mil. Todos os testes de coluna passaram. Que verificação pega esse problema?"
    opcoes: ["Valores aceitos no status", "Não nulo no cliente", "Volume: comparar a quantidade de linhas com o padrão dos dias anteriores", "Unicidade da chave"]
    correta: 2
    explicacao: "As 9 mil linhas que chegaram podem estar perfeitas, e o problema é o que não chegou. Testes de volume comparam o tamanho da carga com o histórico e avisam quando ela foge muito do normal."
  - pergunta: "Qual destas regras faz mais sentido como aviso, e não como erro que bloqueia a carga?"
    opcoes: ["Pedido com o mesmo identificador de outro", "Pedido que aponta para um cliente que não existe", "Pedido com status desconhecido", "Pedido acima de R$ 10 mil, que é raro mas possível"]
    correta: 3
    explicacao: "Um valor alto e raro pode ser legítimo, como uma compra corporativa: merece um aviso para alguém olhar, mas não deve travar a carga. Chave repetida, cliente inexistente e status desconhecido são dados errados de verdade."
  - pergunta: "Numa carga de 1 milhão de pedidos, 3 têm um status desconhecido. O que costuma ser a melhor reação?"
    opcoes: ["Bloquear a carga inteira até o sistema de origem ser corrigido", "Separar os 3 pedidos numa quarentena, publicar o resto e avisar o time responsável", "Apagar os 3 pedidos e não contar a ninguém", "Trocar o status desconhecido por aprovado"]
    correta: 1
    explicacao: "Bloquear tudo por 3 linhas em 1 milhão deixa o painel sem dados novos por um problema mínimo. A quarentena publica o que está bom, guarda o que está ruim para investigação e não esconde nada. Quando a proporção de linhas ruins é grande, aí sim vale bloquear."
  - pergunta: "Por que testar os dados já na camada de staging, e não só nas tabelas finais?"
    opcoes: ["Porque o staging é mais rápido de testar", "Porque nas tabelas finais não é possível testar", "Porque o problema é pego perto da causa, antes de se espalhar pelos modelos que dependem dele", "Porque o dbt só aceita testes no staging"]
    correta: 2
    explicacao: "Um erro na fonte que só é pego no fim já passou por joins e agregações, e fica mais difícil achar a origem. Testar cedo aponta direto para a tabela e a coluna com problema, e impede que o erro chegue aos modelos seguintes."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Escreva o plano de testes de qualidade da tabela de pedidos que alimenta o painel de vendas: quais verificações você faria, com que severidade, e o que acontece quando cada uma falha."
  rubrica:
    - "Cobre várias dimensões: unicidade da chave, campos obrigatórios preenchidos, valores aceitos e faixas válidas, integridade com a tabela de clientes, e pelo menos um teste de tabela, de atualidade ou de volume."
    - "Separa as regras por severidade, com justificativa: erro para dados que não podem estar errados e aviso para casos raros mas possíveis."
    - "Define a reação a cada falha: quem recebe o alerta, quando a carga é bloqueada e quando as linhas ruins vão para a quarentena, e como o painel comunica que os dados estão atrasados ou incompletos."
  modelo: "Na chave, pedido_id, eu testaria unicidade e não nulo, com severidade de erro: um pedido repetido dobra o faturamento. O cliente_id seria obrigatório e teria um teste de integridade contra o cadastro de clientes, também como erro. O status só poderia ter os valores conhecidos, aprovado, cancelado e pendente, porque um status novo, que ninguém tratou, some das contas. O valor teria uma faixa válida, de zero a 50 mil reais, como erro, e um aviso para pedidos acima de 10 mil, que são raros mas possíveis. Na tabela inteira, um teste de atualidade com erro se a última atualização tiver mais de 24 horas, e um teste de volume com aviso se a quantidade de linhas fugir muito da média das últimas semanas. Quando uma regra de erro falha em poucos pedidos, até 5% da carga, essas linhas vão para uma tabela de quarentena, o resto é publicado, e o time de dados recebe um alerta com as regras que falharam, a quantidade de linhas e exemplos. Acima disso, a carga é bloqueada, o painel continua com os dados do dia anterior e mostra a data da última atualização, e o alerta vai também para o time do sistema de origem. Avisos geram só uma mensagem para alguém conferir, sem travar nada."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Um portão de qualidade para a carga diária"
  descricao: "A carga de pedidos do dia chegou com um pedido repetido, um pedido sem cliente, um cliente inexistente, um status desconhecido e valores impossíveis. Você vai escrever as verificações de qualidade em pandas, aplicar as regras de um arquivo de configuração, separar as linhas ruins numa quarentena e decidir se a carga é publicada ou bloqueada."
  pasta: "desafios/analytics_eng/qualidade_dados"
  testes: 11
  tempo: "2 h"
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
    - titulo: "Leia o enunciado e conheça os dados"
      descricao: "Abra desafios/analytics_eng/qualidade_dados/README.md. Em data estão a carga do dia, o cadastro de clientes, as regras e o histórico de volume."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "As funções ler_carga e ler_regras já estão prontas. Cada função tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def linhas_duplicadas(df, coluna):"
        - "def linhas_nulas(df, coluna):"
        - "def linhas_fora_da_lista(df, coluna, valores):"
        - "def linhas_fora_do_intervalo(df, coluna, minimo=None, maximo=None):"
        - "def linhas_orfas(df, coluna, chaves_validas):"
        - "def atraso_em_horas(df, coluna, agora):"
        - "def volume_anormal(historico, linhas_hoje, desvios=3):"
        - "def aplicar_regras(carga, regras, tabelas, chave='pedido_id'):"
        - "def separar_quarentena(carga, resultados, chave='pedido_id'):"
        - "def decidir(resultados, total_pedidos, limite=0.05):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/analytics_eng/qualidade_dados"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/qualidade_dados"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de qualidade de dados"'
        - "git push -u origin desafio/qualidade_dados"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Qualidade de dados", en: "data quality" }
  - { pt: "Unicidade", en: "uniqueness" }
  - { pt: "Completude", en: "completeness" }
  - { pt: "Validade", en: "validity" }
  - { pt: "Integridade referencial", en: "referential integrity" }
  - { pt: "Consistência", en: "consistency" }
  - { pt: "Atualidade dos dados", en: "freshness, timeliness" }
  - { pt: "Volume", en: "volume" }
  - { pt: "Severidade", en: "severity" }
  - { pt: "Quarentena", en: "quarantine" }
  - { pt: "Gravar, auditar e publicar", en: "write-audit-publish (WAP)" }
  - { pt: "Contrato de dados", en: "data contract" }
  - { pt: "Observabilidade de dados", en: "data observability" }
  - { pt: "Detecção de anomalias", en: "anomaly detection" }
---

## Por que testar os dados, e não só o código

No tópico de conferir código gerado por IA, você testou a **lógica**: dado um exemplo pequeno, o código devolve o resultado certo? Isso é necessário, mas não basta para quem trabalha com dados. O código pode estar perfeito e o número do painel sair errado, porque **os dados mudam todo dia**, e mudam sem avisar:

- o sistema de origem reenvia um evento, e um pedido aparece duas vezes;
- alguém cria um status novo, "estornado", que nenhuma regra trata;
- um campo obrigatório começa a chegar vazio depois de uma atualização do site;
- a carga da madrugada falha, e o painel continua mostrando os números de ontem como se fossem de hoje.

Os **testes de qualidade de dados** são afirmações sobre os dados que rodam a cada carga: "o pedido_id não se repete", "todo pedido aponta para um cliente que existe", "a última atualização tem menos de 24 horas". Quando uma afirmação deixa de ser verdade, alguém fica sabendo antes que o número errado chegue a uma reunião.

Vale lembrar o que está em jogo. Um painel que diz "os dados de hoje ainda não chegaram" é um incômodo. Um painel que mostra o faturamento em dobro, sem nenhum aviso, leva a decisões erradas e acaba com a confiança no time de dados, e confiança perdida demora a voltar.

## As dimensões da qualidade

É útil pensar na qualidade em dimensões, cada uma com uma pergunta e um tipo de teste:

| Dimensão     | A pergunta                                  | Exemplo de teste                        |
| ------------ | ------------------------------------------- | --------------------------------------- |
| Unicidade    | Cada coisa aparece uma vez só?              | pedido_id sem repetição                 |
| Completude   | O que é obrigatório está preenchido?        | cliente_id não vazio                    |
| Validade     | Os valores fazem sentido?                   | status na lista; valor entre 0 e 50 mil |
| Integridade  | As referências apontam para algo que existe? | todo cliente_id está no cadastro        |
| Consistência | Os números batem entre si?                  | soma dos itens igual ao valor do pedido |
| Atualidade   | Os dados chegaram a tempo?                  | última atualização há menos de 24 h     |
| Volume       | Chegou a quantidade esperada?               | linhas do dia dentro do padrão          |

As cinco primeiras são **testes de linha**: olham cada registro e apontam quais estão com problema. As duas últimas são **testes de tabela**: olham o conjunto. Os testes de tabela são os mais esquecidos, e pegam justamente os problemas que os de linha não veem. Se a carga parou, os dados velhos continuam únicos, completos e válidos.

Quase todos os testes de linha cabem numa consulta que devolve as linhas com problema. Se a consulta não devolve nada, o teste passou:

```sql
-- unicidade: pedidos que aparecem mais de uma vez
select pedido_id, count(*) as vezes
from pedidos
group by pedido_id
having count(*) > 1;

-- integridade: pedidos que apontam para um cliente inexistente
select p.pedido_id, p.cliente_id
from pedidos as p
left join clientes as c on c.cliente_id = p.cliente_id
where p.cliente_id is not null
  and c.cliente_id is null;
```

Em pandas, a mesma ideia vira uma máscara de booleanos, com True nas linhas com problema:

```python
import pandas as pd

pedidos = pd.read_csv("carga_pedidos.csv")

repetidos = pedidos["pedido_id"].duplicated(keep=False)
sem_cliente = pedidos["cliente_id"].isna()
aceitos = ["aprovado", "cancelado", "pendente"]
status_novo = (
    pedidos["status"].notna() & ~pedidos["status"].isin(aceitos)
)

print(pedidos[repetidos | sem_cliente | status_novo])
```

Repare em dois detalhes. O `keep=False` marca **todas** as cópias de um pedido repetido, e não só a segunda: não dá para saber qual delas é a certa. E o teste de valores aceitos ignora os vazios de propósito. Cada teste cuida de uma pergunta só, e a pergunta "está vazio?" é do teste de completude. Assim, cada falha aponta para um problema só.

Para o volume, uma forma simples é comparar a carga de hoje com a média e o desvio padrão dos dias anteriores: se ficar a mais de três desvios padrão da média, para cima ou para baixo, algo mudou. Promoções, feriados e sazonalidade geram falsos alarmes, então esse teste costuma ser um aviso, e não um erro.

## Onde e quando testar

Os testes rendem mais em pontos diferentes do caminho dos dados:

- **Na entrada.** Os **contratos de dados** são acordos com o time que produz os dados: quais colunas vêm, com que tipos, o que cada uma significa e o que pode mudar sem aviso. Testar o contrato na ingestão pega o problema na porta.
- **No staging.** Testes das suposições sobre os dados brutos: chaves únicas, campos obrigatórios, valores conhecidos. Pegam o erro perto da causa, antes de ele passar por joins e agregações.
- **Nos marts.** Testes da regra de negócio e da granularidade: a chave da tabela fato é única, toda linha da fato aponta para uma dimensão que existe, o total bate com o do sistema financeiro.
- **Antes de publicar.** O padrão **gravar, auditar e publicar** (*write-audit-publish*) grava os dados novos numa área de preparação, roda os testes ali e só então os torna visíveis para o painel. O `dbt build` segue uma versão dessa ideia: testa cada modelo logo depois de criá-lo e não constrói o que depende de um teste que falhou.

Nem toda falha merece a mesma reação. A **severidade** separa os dois casos: **erro** para dados que não podem estar errados, como uma chave repetida, e **aviso** para o que é raro mas possível, como um pedido de valor muito alto. No dbt, a severidade é uma configuração do teste. Neste teste singular, um pedido acima de 10 mil reais gera um aviso, sem travar o build:

```sql
{{ config(severity='warn') }}

select pedido_id, valor_total
from {{ ref('fct_pedidos') }}
where valor_total > 10000
```

Nos testes declarados em YAML, a mesma configuração entra em `config`, ao lado de `arguments`.

E, quando uma regra de erro falha, ainda há uma escolha: **bloquear** a carga inteira ou mandar só as linhas ruins para uma **quarentena** e publicar o resto. Bloquear tudo por 3 linhas em 1 milhão deixa o painel parado por um problema mínimo. Publicar com 30% das linhas ruins espalha o erro. Uma regra comum é decidir pela proporção: até um limite, quarentena; acima dele, bloqueio. É o portão que você vai construir no desafio.

## Ferramentas

Dá para testar dados com SQL e pandas puros, como nos exemplos acima. Conforme o projeto cresce, ferramentas próprias ajudam a organizar os testes, rodar tudo de forma padronizada e guardar os resultados:

- **Testes do dbt**, que você viu no tópico anterior, com pacotes como o `dbt_utils` para testes prontos além dos quatro básicos. A configuração `store_failures` guarda as linhas que falharam numa tabela, para investigação. Os **contratos de modelo** do dbt conferem, no momento do build, se as colunas e os tipos de uma tabela são os combinados.
- **Bibliotecas em Python**, como Great Expectations, pandera e Soda, que descrevem as regras em código ou em YAML e geram relatórios dos resultados.
- **Ferramentas de observabilidade de dados**, que acompanham atualidade, volume e distribuição das tabelas automaticamente e usam detecção de anomalias para avisar quando algo foge do padrão, sem que alguém precise escrever cada regra.

A ferramenta importa menos do que as regras. Comece pelas que protegem as decisões mais importantes: a chave da tabela fato, os relacionamentos, os valores que entram nas contas e a atualidade das fontes.

## Quando um teste falha

Um teste que falha e ninguém vê não serve para nada. Alguns cuidados fazem a diferença:

- **O alerta vai para alguém responsável**, com o que falhou, quantas linhas, alguns exemplos e o que fazer. "Teste falhou" sozinho não ajuda ninguém.
- **Avisos demais viram ruído.** Se o time recebe vinte avisos por dia, para de ler, e o vigésimo primeiro, o importante, passa batido. Teste que vive falhando precisa ser corrigido ou removido. E teste que nunca falhou também merece desconfiança: ele está testando alguma coisa? Rode-o uma vez com um dado errado de propósito.
- **Cada incidente vira um teste.** Quando um problema escapar e chegar ao painel, depois de corrigir, escreva o teste que o teria pegado.
- **A causa costuma estar na origem.** Uma quarentena que enche todo dia com o mesmo problema pede uma conversa com o time do sistema de origem, e não mais um filtro no staging.
- **O painel diz de quando são os dados.** Mostrar a data e a hora da última atualização ajuda quem lê a perceber um atraso, mesmo quando nenhum alerta disparou.

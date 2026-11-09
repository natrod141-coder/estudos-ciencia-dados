---
titulo: "Métricas de classificação"
modulo: ml_classico
ordem: 8
horas: 7
estado: publicado
resumo: "AUC, acurácia, recall e precisão: o que cada uma mede."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Tudo começa na matriz de confusão"
    tipo: leitura
    minutos: 8
  - id: a2
    titulo: "Precisão, recall e F1"
    tipo: leitura
    minutos: 12
  - id: a3
    titulo: "AUC e precisão média: medidas que não dependem do limiar"
    tipo: leitura
    minutos: 15
  - id: a4
    titulo: "Escolher o limiar pelo negócio"
    tipo: leitura
    minutos: 12
  - id: a5
    titulo: "Probabilidades confiáveis: calibração"
    tipo: leitura
    minutos: 10
  - id: a6
    titulo: "Vídeo de apoio: precisão, recall e curva ROC"
    tipo: video
    minutos: 25
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Na campanha de retenção, o que mede a precisão do modelo?"
    opcoes: ["Dos clientes que cancelaram, quantos o modelo encontrou", "Dos clientes que o modelo colocou na lista, quantos de fato iam cancelar", "A proporção de acertos entre todos os clientes", "O quanto as probabilidades estão perto da taxa real"]
    correta: 1
    explicacao: "Precisão olha para a lista: dos contatados, quantos eram mesmo de risco. Ela mede o desperdício com alarmes falsos. A primeira opção descreve o recall."
  - pergunta: "Num sistema de detecção de fraude, deixar passar uma fraude custa muito mais que bloquear por engano uma compra legítima, que o cliente desbloqueia com uma mensagem. Que medida priorizar?"
    opcoes: ["O recall: encontrar a maior parte das fraudes, aceitando mais bloqueios por engano", "A precisão: bloquear só quando tiver certeza", "A acurácia, que resume tudo", "Nenhuma: nesse caso, o limiar deve ficar em 0,5"]
    correta: 0
    explicacao: "Quando o falso negativo é muito mais caro que o falso positivo, vale um limiar mais baixo, que aumenta o recall à custa de alguns alarmes falsos. No caso contrário, como um alarme que exige uma visita cara, a precisão pesa mais."
  - pergunta: "O modelo de cancelamento tem AUC de 0,71. O que isso significa?"
    opcoes: ["Que 71% das previsões estão certas", "Que o modelo encontra 71% dos cancelamentos", "Que, sorteando um cliente que cancelou e um que ficou, o modelo dá probabilidade maior ao que cancelou em 71% das vezes", "Que 71% dos clientes da lista cancelam"]
    correta: 2
    explicacao: "A AUC mede a capacidade de ordenar, sem depender de limiar. 0,5 é o mesmo que sortear; 1 é ordenar perfeitamente. No desafio, você calcula a AUC exatamente assim, contando pares."
  - pergunta: "Por que a curva de precisão e recall, e a precisão média, costumam ser mais informativas que a curva ROC quando a classe de interesse é rara?"
    opcoes: ["Porque são mais fáceis de calcular", "Porque não dependem das probabilidades", "Porque a curva ROC só funciona com classes balanceadas", "Porque a precisão mostra diretamente o custo dos alarmes falsos: com muitos negativos, a curva ROC pode parecer ótima mesmo quando a maior parte da lista é alarme falso"]
    correta: 3
    explicacao: "Com 1% de fraudes, uma taxa de falso positivo de 2% parece pequena na curva ROC, mas são o dobro de alarmes falsos em relação às fraudes. A precisão média tem como referência a taxa da classe, e não 0,5: no desafio, 0,48 contra 0,27 de uma lista sorteada."
  - pergunta: "Cada contato custa R$ 40, e um cliente que ia cancelar e recebe o contato fica com probabilidade 0,3, valendo R$ 400. A partir de que probabilidade de cancelar vale a pena contatar?"
    opcoes: ["A partir de 0,5", "A partir de 40 / (0,3 x 400), cerca de 0,33, se as probabilidades forem confiáveis", "A partir de 0,1", "Sempre vale a pena contatar"]
    correta: 1
    explicacao: "O ganho esperado de contatar um cliente é a probabilidade de cancelar vezes 0,3 vezes R$ 400; o custo é R$ 40. Vale quando o ganho passa do custo. No desafio, o melhor limiar da tabela foi 0,30, perto da conta teórica, porque o modelo está bem calibrado."
  - pergunta: "Como conferir se as probabilidades de um modelo são confiáveis?"
    opcoes: ["Olhando a AUC: se for alta, as probabilidades estão certas", "Conferindo se todas as probabilidades estão entre 0 e 1", "Agrupando os clientes por faixa de probabilidade e comparando, em cada faixa, a probabilidade média com a proporção real de cancelamentos", "Comparando a acurácia no treino e no teste"]
    correta: 2
    explicacao: "Um modelo pode ordenar bem, com AUC alta, e ainda assim errar o nível das probabilidades, dizendo 0,8 para um grupo em que só 50% cancelam. A tabela de calibração mostra isso. No desafio, a regressão logística está bem calibrada."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "A diretoria pergunta: 'o modelo de cancelamento é bom?'. Responda com as métricas certas para a decisão que a empresa vai tomar, explicando cada número em linguagem de negócio, e diga como você escolheria quem entra na campanha."
  rubrica:
    - "Explica por que a acurácia não serve como resposta e usa medidas ligadas à decisão: quanto da lista cancela de fato e quanto dos cancelamentos a lista pega, comparando com uma lista sorteada."
    - "Escolhe o limiar ou o tamanho da lista pelos custos e ganhos da campanha, ou pela capacidade do time, e traduz o resultado em dinheiro ou em clientes."
    - "Menciona a capacidade de ordenar o risco, como a AUC, e a confiabilidade das probabilidades, como a calibração, ou o acompanhamento do modelo depois que a campanha começar."
  modelo: "O modelo serve para decidir para quem ligar, então a pergunta certa é quanto ele melhora essa decisão. Hoje, 27% dos clientes cancelam por trimestre. Se o time ligasse para 300 clientes sorteados, uns 80 seriam de risco. Com o modelo, a lista dos 300 de maior risco tem 143 clientes que iam cancelar, quase metade, e pega 43% de todos os cancelamentos. Eu não usaria a acurácia, porque um modelo que diz que ninguém cancela já acerta 73% e não ajuda em nada. Para escolher quem entra, pus na conta o custo de R$ 40 por contato e o ganho de R$ 400 por cliente que fica, com 30% de sucesso entre os que iam cancelar. O lucro é maior ligando para quem tem 30% ou mais de risco: uma lista de 412 clientes, com lucro estimado de R$ 5,5 mil no trimestre, contra R$ 3,4 mil se usássemos o corte padrão de 50%. Isso só vale porque as probabilidades do modelo são confiáveis: quando ele diz 50%, cerca de metade cancela de fato. Por fim, a taxa de sucesso de 30% é uma suposição: na primeira campanha, eu separaria um grupo de controle, que não recebe ligação, para medir o efeito real e refazer a conta."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Escolher o limiar pelo dinheiro"
  descricao: "Com as probabilidades de um modelo de cancelamento, você vai calcular à mão a matriz de confusão, a precisão, o recall, o F1 e a AUC, montar a tabela de limiares, escolher o limiar que dá mais lucro para uma campanha de retenção, avaliar uma lista de tamanho fixo e conferir se as probabilidades são confiáveis."
  pasta: "desafios/ml_classico/metricas"
  testes: 9
  tempo: "1 h 30 min"
  ferramentas: "VS Code, Python 3.11 ou superior, numpy, pandas e pytest"
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
      descricao: "Abra desafios/ml_classico/metricas/README.md. A função probabilidades_de_teste, já pronta, entrega os dados."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "Faça as contas das métricas com numpy. Cada função tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def contar(y, probs, limiar):"
        - "def precisao_recall_f1(contagem):"
        - "def auc_por_pares(y, probs):"
        - "def tabela_de_limiares(y, probs, limiares):"
        - "def lucro(contagem, valor_cliente=400, custo_contato=40, taxa_sucesso=0.3):"
        - "def melhor_limiar(y, probs, limiares, valor_cliente=400, custo_contato=40, taxa_sucesso=0.3):"
        - "def precisao_no_topo(y, probs, k):"
        - "def calibracao(y, probs, faixas=5):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/ml_classico/metricas"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/metricas"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de métricas de classificação"'
        - "git push -u origin desafio/metricas"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Precisão", en: "precision" }
  - { pt: "Revocação, sensibilidade", en: "recall, sensitivity, true positive rate" }
  - { pt: "Especificidade", en: "specificity" }
  - { pt: "Taxa de falsos positivos", en: "false positive rate" }
  - { pt: "Medida F1", en: "F1 score" }
  - { pt: "Curva ROC", en: "ROC curve" }
  - { pt: "Área sob a curva", en: "AUC (area under the curve)" }
  - { pt: "Curva de precisão e recall", en: "precision-recall curve" }
  - { pt: "Precisão média", en: "average precision" }
  - { pt: "Precisão no topo", en: "precision at k" }
  - { pt: "Calibração", en: "calibration" }
  - { pt: "Ponto de equilíbrio", en: "break-even point" }
  - { pt: "Grupo de controle", en: "control group" }
---

## Tudo começa na matriz de confusão

No tópico de regressão logística, você viu que a acurácia engana quando uma classe é bem maior que a outra. Este tópico organiza as medidas que olham para o que importa. Quase todas saem das quatro contagens da **matriz de confusão**, para um limiar escolhido:

- **Verdadeiros positivos (VP):** cancelaram, e o modelo apontou.
- **Falsos positivos (FP):** ficaram, mas o modelo apontou. Os alarmes falsos.
- **Falsos negativos (FN):** cancelaram, mas o modelo não apontou. Os que escaparam.
- **Verdadeiros negativos (VN):** ficaram, e o modelo não apontou.

Cada medida combina essas contagens de um jeito, e cada uma responde a uma pergunta diferente. Escolher a medida é escolher a pergunta.

## Precisão, recall e F1

- **Precisão** = VP / (VP + FP). Dos clientes que o modelo apontou, quantos de fato iam cancelar? Mede o desperdício com alarmes falsos.
- **Recall**, ou sensibilidade, = VP / (VP + FN). Dos clientes que cancelaram, quantos o modelo encontrou? Mede o que escapou.
- **F1** = 2 x precisão x recall / (precisão + recall). A média harmônica das duas: só é alta se as duas forem.

As duas primeiras puxam para lados opostos. Baixar o limiar aumenta o recall e diminui a precisão; subir, o contrário. Nos dados do desafio:

| Limiar | Lista | Precisão | Recall |
| ------ | ----- | -------- | ------ |
| 0,10   | 1.100 | 0,29     | 0,97   |
| 0,30   | 412   | 0,44     | 0,55   |
| 0,50   | 115   | 0,58     | 0,20   |

Qual priorizar depende do custo de cada erro. Em detecção de fraude, deixar passar uma fraude costuma custar mais que bloquear uma compra legítima: o recall pesa mais. Num alarme que exige uma visita técnica cara, cada falso positivo custa caro: a precisão pesa mais. O F1 é útil quando os dois erros têm custos parecidos, ou como resumo rápido, mas não diz nada sobre dinheiro.

## AUC e precisão média: medidas que não dependem do limiar

Para comparar modelos antes de escolher o limiar, usam-se medidas que olham para todas as ordenações possíveis.

A **curva ROC** mostra, para cada limiar, o recall contra a taxa de falsos positivos, FP / (FP + VN). A **AUC**, a área sob essa curva, tem uma leitura direta: sorteando um cliente que cancelou e um que ficou, é a probabilidade de o modelo dar risco maior ao que cancelou. AUC de 0,5 é o mesmo que sortear; de 1, uma ordenação perfeita. O modelo do desafio tem 0,71. No desafio, você calcula a AUC exatamente pela definição, contando os pares.

Com classes muito desbalanceadas, a curva ROC pode enganar. Com 1% de fraudes, uma taxa de falsos positivos de 2% parece pequena no gráfico, mas são o dobro de alarmes falsos em relação às fraudes. A **curva de precisão e recall** mostra o problema diretamente, e a **precisão média**, a área sob ela, resume a curva. A referência dela não é 0,5, e sim a taxa da classe: no desafio, a precisão média é 0,48, contra 0,27 de uma ordenação ao acaso.

```python
from sklearn.metrics import average_precision_score, roc_auc_score

print(roc_auc_score(y_teste, probs))  # 0.71
print(average_precision_score(y_teste, probs))  # 0.48
```

Quando a capacidade de atendimento é fixa, uma medida mais direta é a **precisão no topo**: das k pessoas de maior risco, quantas são positivas. Se o time de retenção só faz 300 ligações, a pergunta é quantos dos 300 primeiros iam cancelar. No desafio, 48%, e essa lista pega 43% de todos os cancelamentos.

## Escolher o limiar pelo negócio

As medidas acima comparam modelos. Para **decidir**, é preciso pôr a decisão em números. Na campanha do desafio, cada contato custa R$ 40, um cliente que fica vale R$ 400 no ano, e 30% dos clientes que iam cancelar ficam depois do contato. O lucro de uma lista é:

```text
lucro = VP x 0,3 x 400 - (VP + FP) x 40
```

| Limiar | Lista | Cancelamentos na lista | Lucro       |
| ------ | ----- | ---------------------- | ----------- |
| 0,10   | 1.100 | 322                    | -R$ 5.360   |
| 0,20   | 700   | 251                    | R$ 2.120    |
| 0,30   | 412   | 183                    | R$ 5.480    |
| 0,40   | 217   | 113                    | R$ 4.880    |
| 0,50   | 115   | 67                     | R$ 3.440    |

O melhor limiar é 0,30, e não o padrão de 0,5. Há uma forma de chegar perto disso sem a tabela: vale contatar um cliente quando o ganho esperado passa do custo, ou seja, quando a probabilidade de cancelar vezes 0,3 vezes R$ 400 passa de R$ 40. O **ponto de equilíbrio** é 40 / 120, cerca de 0,33. A conta só funciona se as probabilidades forem confiáveis, o assunto da próxima seção.

Mude a economia, e o limiar muda junto. Se o contato custasse R$ 15, um e-mail com cupom, por exemplo, o melhor limiar cairia para 0,10: valeria falar com quase todo mundo. Por isso, o limiar é uma decisão de negócio, que precisa ser revista quando os custos mudam.

Um cuidado final: a taxa de sucesso de 30% é uma suposição. Na primeira campanha, separe um **grupo de controle**, de clientes de risco que não recebem contato, e compare as taxas de cancelamento dos dois grupos. É um teste A/B, e é a única forma de medir o efeito real da campanha.

## Probabilidades confiáveis: calibração

Um modelo pode ordenar bem, com AUC alta, e ainda assim errar o **nível** das probabilidades: dizer 0,8 para um grupo em que só metade cancela. Para conferir, agrupe os clientes em faixas de probabilidade e compare, em cada faixa, a probabilidade média com a taxa real:

| Faixa | Probabilidade média | Taxa real de cancelamento |
| ----- | ------------------- | ------------------------- |
| 1ª    | 0,09                | 0,10                      |
| 2ª    | 0,16                | 0,19                      |
| 3ª    | 0,22                | 0,20                      |
| 4ª    | 0,32                | 0,34                      |
| 5ª    | 0,52                | 0,50                      |

A regressão logística do desafio está bem **calibrada**: em cada faixa, os dois números ficam próximos. Modelos de árvore, florestas e boosting costumam ser menos calibrados, com probabilidades espremidas para o meio ou exageradas nas pontas. O `CalibratedClassifierCV` do scikit-learn corrige isso, ajustando as probabilidades com validação cruzada.

A calibração importa sempre que a probabilidade é usada como número, e não só para ordenar: na conta do lucro, numa previsão de quantos clientes vão cancelar no trimestre, num preço de seguro. Se a decisão for só "ligar para os 300 de maior risco", basta a ordenação.

Este é o fim do módulo de machine learning clássico. O roteiro completo que você percorreu vale para quase todo projeto de dados tabulares: preparar as variáveis sem vazamento, comparar modelos simples e complexos com validação cruzada, guardar o teste para o fim, e escolher o limiar e as métricas pela decisão que o modelo vai apoiar.

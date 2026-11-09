# Estudos: ciência de dados e IA

Site de estudo com painel de progresso para a trilha de ciência de dados e IA. Cada tópico
tem material de leitura, aulas, quiz, uma pergunta aberta e um desafio prático em Python. O
painel acompanha as horas estudadas e quando cada tópico foi dominado.

## Como a trilha está organizada

São duas trilhas estudadas **em paralelo**, e não uma depois da outra: a de dados dá a base
(SQL, Python, estatística, modelagem, ML) e a de IA ensina a usar e a construir sistemas com
LLMs em cima dessa base. O plano vai de novembro de 2026 a dezembro de 2027, com meta de 5 h
por semana (cerca de 296 h), e termina junto com a graduação em ADS.

| Fase | Período | Trilha de dados | Trilha de IA | Projeto da fase |
|---|---|---|---|---|
| 1 | nov/2026 a mar/2027 | Estatística, manipulação de dados | Fundamentos de IA generativa | Análise exploratória com SQL e pandas |
| 2 | mar a jun/2027 | Visualização, analytics engineering | APIs de LLM | Modelo dimensional em dbt com testes |
| 3 | jun a out/2027 | Machine learning clássico | Busca, RAG e avaliação | Assistente de RAG com avaliação |
| 4 | out a dez/2027 | Colocar em produção | IA sobre dados | Agente text-to-SQL avaliado e publicado |

Fases, módulos, marcos e projetos ficam em `conteudo/trilhas.json`. O que ainda falta escrever
está em `conteudo/PENDENTES.md`.

## Como rodar

Pré-requisito: Node.js 22 ou superior.

```
npm install
npm run dev
```

Abra http://localhost:4321. O site também pode ser gerado como arquivos estáticos:

```
npm run build      # gera a pasta dist/
npm run preview    # serve a pasta dist/ para conferir o resultado do build
```

## Onde fica cada coisa

```
src/dados/        regras do painel (progresso, critérios, datas), com testes
src/scripts/      código que roda no navegador (estado, quiz, formulários)
src/pages/        as páginas do site
src/layouts/      layout comum a todas as páginas
src/styles/       o CSS
conteudo/         os tópicos, em Markdown, e trilhas.json (trilhas, módulos, fases, marcos)
desafios/         os exercícios práticos de Python, com testes automáticos
scripts/          scripts de linha de comando (criar tópico, verificar desafios)
tests/            testes automáticos de src/dados/
```

## Como o progresso é calculado

Um tópico fica **dominado** quando cumpre os critérios que se aplicam a ele:

1. **Quiz com 80% ou mais.** Pode ser refeito quantas vezes for preciso.
2. **Desafio prático aprovado**, ou seja, todos os testes automáticos passando.
3. **Revisão bem sucedida**, feita 7 dias ou mais depois de cumprir os dois critérios acima.

Um tópico sem quiz nem desafio (ainda em rascunho) nunca chega a dominado, porque não há
como comprovar. As regras completas, com todos os casos, estão em `src/dados/dominio.js` e
têm testes em `tests/dominio.test.js`.

O progresso de um módulo é a média do progresso dos seus tópicos (não iniciado = 0,
estudando = 0,25, praticando = 0,6, dominado = 1). O progresso de uma trilha e o progresso
geral ponderam os módulos pelas horas estimadas de cada um.

## Onde o progresso fica guardado

No `localStorage` do navegador de quem está estudando. Não há login nem servidor: cada
navegador guarda o seu próprio progresso. Por isso:

- O rodapé do site mostra a data do último backup e avisa depois de 14 dias sem exportar.
- Os botões "Exportar progresso" e "Importar progresso" fazem o backup em um arquivo JSON.
- Se o conteúdo salvo estiver corrompido, o site começa do zero sozinho e guarda uma cópia
  do que havia antes, para não travar a navegação.

## Escrever um tópico novo

```
npm run novo -- <modulo> "<Título do tópico>" --horas 4
```

Isso cria o arquivo em `conteudo/topicos/<modulo>/` já com o cabeçalho preenchido, como
rascunho. Depois, edite o arquivo seguindo o modelo completo em
`conteudo/topicos/estatistica/tendencia_central.md`: aulas, quiz, pergunta aberta, desafio e
o texto de leitura. A lista de tópicos que ainda faltam escrever está em
`conteudo/PENDENTES.md`, junto com o que falta decidir sobre NumPy, dados faltantes
e feature engineering.

O formato de cada arquivo é validado no build por `src/content.config.js`: se algo estiver
fora do formato, o build para e diz qual arquivo e qual campo corrigir.

## Criar um desafio prático

Veja `desafios/README.md`. Depois de criar um desafio, rode:

```
python scripts/verificar_desafios.py
```

Esse script confere, para cada desafio com gabarito, que o arquivo inicial (sem nenhuma
solução) falha em todos os testes e que o gabarito passa em todos. Pré-requisito: Python
3.11 ou superior e `pip install -r desafios/requirements.txt`.

## Rodar os testes

```
npm test
```

Roda os testes de `src/dados/` com o executor de testes nativo do Node (58 testes, sem
dependências extras).

## Publicar o site

O site é estático e pode ser hospedado em qualquer serviço de páginas estáticas (GitHub
Pages, Netlify, Vercel). Para o GitHub Pages, defina `site` e `base` em `astro.config.mjs`
com o endereço do repositório antes de gerar o build, por exemplo:

```js
export default defineConfig({
  site: 'https://SEU_USUARIO.github.io',
  base: '/NOME_DO_REPOSITORIO',
});
```

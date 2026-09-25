// Cria o arquivo de um tópico novo em conteudo/topicos/<modulo>/.
//
// Uso:
//   npm run novo -- <modulo> "<título>" [--id nome_do_arquivo] [--horas 3] [--resumo "frase"]
//
// Exemplo:
//   npm run novo -- estatistica "Correlação" --horas 4
//
// O número de ordem é o próximo da fila do módulo.

import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const raiz = join(dirname(fileURLToPath(import.meta.url)), '..');

function falhar(mensagem) {
  console.error(`Erro: ${mensagem}`);
  process.exit(1);
}

/** "Medidas de tendência central" vira "medidas_de_tendencia_central". */
export function criarId(texto) {
  return texto
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '');
}

function lerArgumentos(argv) {
  const posicionais = [];
  const opcoes = {};
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i].startsWith('--')) {
      opcoes[argv[i].slice(2)] = argv[i + 1];
      i += 1;
    } else {
      posicionais.push(argv[i]);
    }
  }
  return { posicionais, opcoes };
}

function proximaOrdem(pasta) {
  if (!existsSync(pasta)) return 1;
  let maior = 0;
  for (const arquivo of readdirSync(pasta)) {
    if (!arquivo.endsWith('.md')) continue;
    const encontrado = /^ordem:\s*(\d+)/m.exec(readFileSync(join(pasta, arquivo), 'utf8'));
    if (encontrado) maior = Math.max(maior, Number(encontrado[1]));
  }
  return maior + 1;
}

export function montarArquivo({ titulo, modulo, ordem, horas, resumo }) {
  return `---
titulo: ${JSON.stringify(titulo)}
modulo: ${modulo}
ordem: ${ordem}
horas: ${horas}
estado: rascunho
resumo: ${JSON.stringify(resumo)}
---

<!-- Escreva o material de leitura aqui. Para o formato completo (aulas, quiz, pergunta
     aberta e desafio), veja conteudo/topicos/estatistica/tendencia_central.md. -->
`;
}

function principal() {
  const { posicionais, opcoes } = lerArgumentos(process.argv.slice(2));
  const [modulo, titulo] = posicionais;
  if (!modulo || !titulo) {
    falhar('Uso: npm run novo -- <modulo> "<título>" [--id nome] [--horas 3] [--resumo "frase"]');
  }

  const config = JSON.parse(readFileSync(join(raiz, 'conteudo', 'trilhas.json'), 'utf8'));
  if (!config.modulos.some((m) => m.id === modulo)) {
    const validos = config.modulos.map((m) => m.id).join(', ');
    falhar(`O módulo "${modulo}" não existe. Módulos disponíveis: ${validos}.`);
  }

  const id = opcoes.id ?? criarId(titulo);
  if (!/^[a-z0-9_]+$/.test(id)) falhar(`O id "${id}" só pode ter letras minúsculas, números e "_".`);

  const horas = opcoes.horas === undefined ? 3 : Number(opcoes.horas);
  if (!Number.isFinite(horas) || horas <= 0) falhar('--horas precisa ser um número maior que zero.');

  const pasta = join(raiz, 'conteudo', 'topicos', modulo);
  const caminho = join(pasta, `${id}.md`);
  if (existsSync(caminho)) falhar(`Já existe um tópico em ${caminho}.`);

  mkdirSync(pasta, { recursive: true });
  const ordem = proximaOrdem(pasta);
  writeFileSync(caminho, montarArquivo({ titulo, modulo, ordem, horas, resumo: opcoes.resumo ?? '' }));
  console.log(`Criado: conteudo/topicos/${modulo}/${id}.md (ordem ${ordem}, ${horas} h)`);
}

// só executa quando chamado direto, e não quando importado pelos testes
if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) principal();

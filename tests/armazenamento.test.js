import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  estadoInicial, lerEstado, carregarEstado, salvarEstado, exportarTexto, importarTexto,
  registrarBackup, ultimoBackup, sessaoValida,
} from '../src/dados/armazenamento.js';
import {
  CHAVE_ESTADO, CHAVE_ESTADO_CORROMPIDO, VERSAO_ESTADO,
} from '../src/dados/constantes.js';

function storageDeMentira(inicial = {}) {
  const dados = { ...inicial };
  return {
    dados,
    getItem: (k) => (k in dados ? dados[k] : null),
    setItem: (k, v) => { dados[k] = String(v); },
  };
}

const sessao = { id: 's1', data: '2026-09-20', horas: 1.5, topico: 'estatistica/teste_ab', nota: '' };

test('sem nada salvo começa com o estado inicial e sem aviso', () => {
  const r = carregarEstado(storageDeMentira());
  assert.deepEqual(r.estado, estadoInicial());
  assert.equal(r.aviso, null);
});

test('salvar e carregar devolvem o mesmo progresso', () => {
  const storage = storageDeMentira();
  const estado = estadoInicial();
  estado.sessoes.push(sessao);
  estado.topicos['estatistica/teste_ab'] = {
    aulasConcluidas: ['a1'],
    tentativasQuiz: [{ data: '2026-09-21', nota: 60, acertos: 3, total: 5 }],
    aberta: { rascunho: 'texto', rubricaMarcada: [0], enviadaEm: null },
    desafio: { testesPassando: 6, testesTotal: 8, tentativas: 2, aprovadoEm: null },
    revisoes: [],
  };
  assert.deepEqual(salvarEstado(estado, storage), { ok: true });
  const r = carregarEstado(storage);
  assert.deepEqual(r.estado, estado);
  assert.equal(r.aviso, null);
});

test('JSON ilegível não derruba o site: guarda uma cópia e começa do zero', () => {
  const storage = storageDeMentira({ [CHAVE_ESTADO]: '{isso não é json' });
  const r = carregarEstado(storage);
  assert.deepEqual(r.estado, estadoInicial());
  assert.match(r.aviso, /ilegível/);
  assert.equal(storage.dados[CHAVE_ESTADO_CORROMPIDO], '{isso não é json');
});

test('estrutura inválida também é tratada como corrompida', () => {
  const storage = storageDeMentira({ [CHAVE_ESTADO]: JSON.stringify({ versao: 1, topicos: [], sessoes: [] }) });
  const r = carregarEstado(storage);
  assert.deepEqual(r.estado, estadoInicial());
  assert.ok(r.aviso);
});

test('storage que lança erro na leitura não derruba o site', () => {
  const bloqueado = { getItem() { throw new Error('bloqueado'); }, setItem() { throw new Error('bloqueado'); } };
  const r = carregarEstado(bloqueado);
  assert.deepEqual(r.estado, estadoInicial());
  assert.match(r.aviso, /não permite guardar/);
  const s = salvarEstado(estadoInicial(), bloqueado);
  assert.equal(s.ok, false);
  assert.match(s.erro, /Exporte/);
});

test('sessões inválidas são descartadas com aviso, as válidas ficam', () => {
  const storage = storageDeMentira({
    [CHAVE_ESTADO]: JSON.stringify({
      versao: 1, topicos: {},
      sessoes: [sessao, { id: 's2', data: '2026-09-20', horas: -1, topico: null, nota: '' }, 'lixo'],
    }),
  });
  const r = carregarEstado(storage);
  assert.equal(r.estado.sessoes.length, 1);
  assert.match(r.aviso, /2 sessão/);
});

test('lerEstado rejeita versão mais nova e formatos errados', () => {
  assert.equal(lerEstado(null).ok, false);
  assert.equal(lerEstado([]).ok, false);
  assert.equal(lerEstado({ topicos: {}, sessoes: [] }).ok, false);
  const nova = lerEstado({ versao: VERSAO_ESTADO + 1, topicos: {}, sessoes: [] });
  assert.equal(nova.ok, false);
  assert.match(nova.erro, /mais nova/);
  assert.equal(lerEstado({ versao: 1, topicos: {} }).ok, false);
});

test('sessaoValida confere cada campo', () => {
  assert.equal(sessaoValida(sessao), true);
  assert.equal(sessaoValida({ ...sessao, horas: 0 }), false);
  assert.equal(sessaoValida({ ...sessao, horas: 25 }), false);
  assert.equal(sessaoValida({ ...sessao, data: '20/09/2026' }), false);
  assert.equal(sessaoValida({ ...sessao, id: '' }), false);
  assert.equal(sessaoValida({ ...sessao, topico: null }), true);
  assert.equal(sessaoValida({ ...sessao, topico: 5 }), false);
});

test('exportar e importar fazem o caminho de ida e volta', () => {
  const estado = estadoInicial();
  estado.sessoes.push(sessao);
  const texto = exportarTexto(estado, new Date('2026-09-24T12:00:00Z'));
  const dentro = JSON.parse(texto);
  assert.equal(dentro.app, 'estudos');
  assert.equal(dentro.exportadoEm, '2026-09-24T12:00:00.000Z');

  const r = importarTexto(texto);
  assert.equal(r.ok, true);
  assert.deepEqual(r.estado, estado);
});

test('importar aceita o progresso puro e recusa arquivos que não servem', () => {
  const estado = estadoInicial();
  assert.equal(importarTexto(JSON.stringify(estado)).ok, true);
  assert.equal(importarTexto('não é json').ok, false);
  assert.match(importarTexto('não é json').erro, /JSON/);
  assert.equal(importarTexto(JSON.stringify({ app: 'estudos', estado: { versao: 1 } })).ok, false);
  assert.equal(importarTexto('42').ok, false);
});

test('data do último backup', () => {
  const storage = storageDeMentira();
  assert.equal(ultimoBackup(storage), null);
  registrarBackup(storage, '2026-09-24');
  assert.equal(ultimoBackup(storage), '2026-09-24');
  assert.equal(ultimoBackup(storageDeMentira({ 'estudos:ultimo_backup': 'lixo' })), null);
});

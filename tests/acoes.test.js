import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  comProgresso, alternarAula, registrarQuiz, salvarRascunho, marcarRubrica, enviarAberta,
  registrarDesafio, registrarRevisao, registrarSessao, removerSessao,
} from '../src/dados/acoes.js';
import { estadoInicial } from '../src/dados/armazenamento.js';
import { progressoVazio } from '../src/dados/dominio.js';

const HOJE = '2026-09-24';

test('comProgresso não altera o estado original', () => {
  const original = estadoInicial();
  const novo = comProgresso(original, 'a/b', (p) => alternarAula(p, 'a1', true));
  assert.deepEqual(original.topicos, {});
  assert.deepEqual(novo.topicos['a/b'].aulasConcluidas, ['a1']);
});

test('alternar aula marca e desmarca sem duplicar', () => {
  let p = progressoVazio();
  p = alternarAula(p, 'a1', true);
  p = alternarAula(p, 'a1', true);
  p = alternarAula(p, 'a2', true);
  assert.deepEqual(p.aulasConcluidas, ['a1', 'a2']);
  p = alternarAula(p, 'a1', false);
  assert.deepEqual(p.aulasConcluidas, ['a2']);
});

test('registrar quiz guarda a tentativa com a data de hoje e no máximo 50', () => {
  let p = progressoVazio();
  p = registrarQuiz(p, { nota: 60, acertos: 3, total: 5 }, HOJE);
  assert.deepEqual(p.tentativasQuiz[0], { data: HOJE, nota: 60, acertos: 3, total: 5 });
  for (let i = 0; i < 60; i += 1) p = registrarQuiz(p, { nota: i, acertos: 0, total: 5 }, HOJE);
  assert.equal(p.tentativasQuiz.length, 50);
  assert.equal(p.tentativasQuiz.at(-1).nota, 59);
});

test('rubrica marcada fica ordenada e sem repetição', () => {
  let p = progressoVazio();
  p = marcarRubrica(p, 2, true);
  p = marcarRubrica(p, 0, true);
  p = marcarRubrica(p, 2, true);
  assert.deepEqual(p.aberta.rubricaMarcada, [0, 2]);
  p = marcarRubrica(p, 0, false);
  assert.deepEqual(p.aberta.rubricaMarcada, [2]);
});

test('rascunho é limitado e o envio guarda a data', () => {
  let p = salvarRascunho(progressoVazio(), 'x'.repeat(6000));
  assert.equal(p.aberta.rascunho.length, 5000);
  p = enviarAberta(p, HOJE);
  assert.equal(p.aberta.enviadaEm, HOJE);
  assert.equal(p.aberta.rascunho.length, 5000);
});

test('registrar desafio valida os números', () => {
  const p = progressoVazio();
  assert.equal(registrarDesafio(p, { passando: 3, total: 0 }, HOJE).ok, false);
  assert.equal(registrarDesafio(p, { passando: 9, total: 8 }, HOJE).ok, false);
  assert.equal(registrarDesafio(p, { passando: -1, total: 8 }, HOJE).ok, false);
  assert.equal(registrarDesafio(p, { passando: 2.5, total: 8 }, HOJE).ok, false);
  assert.match(registrarDesafio(p, { passando: 9, total: 8 }, HOJE).erro, /entre 0 e 8/);
});

test('desafio só é aprovado com todos os testes e a aprovação não se perde', () => {
  let r = registrarDesafio(progressoVazio(), { passando: 6, total: 8 }, '2026-09-20');
  assert.equal(r.ok, true);
  assert.equal(r.progresso.desafio.aprovadoEm, null);
  assert.equal(r.progresso.desafio.tentativas, 1);

  r = registrarDesafio(r.progresso, { passando: 8, total: 8 }, '2026-09-22');
  assert.equal(r.progresso.desafio.aprovadoEm, '2026-09-22');
  assert.equal(r.progresso.desafio.tentativas, 2);

  // uma rodada pior depois não desfaz a aprovação nem muda a data
  r = registrarDesafio(r.progresso, { passando: 5, total: 8 }, '2026-09-30');
  assert.equal(r.progresso.desafio.aprovadoEm, '2026-09-22');
  assert.equal(r.progresso.desafio.testesPassando, 5);
});

test('registrar revisão guarda o resultado', () => {
  let p = registrarRevisao(progressoVazio(), true, HOJE);
  p = registrarRevisao(p, false, '2026-09-25');
  assert.deepEqual(p.revisoes, [{ data: HOJE, ok: true }, { data: '2026-09-25', ok: false }]);
});

test('registrar sessão aceita dados válidos e mantém a ordem por data', () => {
  let estado = estadoInicial();
  let r = registrarSessao(estado, { data: '2026-09-22', horas: '1,5'.replace(',', '.'), topico: 'a/b', nota: '  leitura  ' }, { hoje: HOJE, id: 's1' });
  assert.equal(r.ok, true);
  estado = r.estado;
  r = registrarSessao(estado, { data: '2026-09-20', horas: 2, topico: '', nota: undefined }, { hoje: HOJE, id: 's2' });
  estado = r.estado;
  assert.deepEqual(estado.sessoes.map((s) => s.id), ['s2', 's1']);
  assert.equal(estado.sessoes[1].nota, 'leitura');
  assert.equal(estado.sessoes[0].topico, null);
  assert.equal(estado.sessoes[1].horas, 1.5);
});

test('registrar sessão recusa entradas inválidas com mensagem clara', () => {
  const estado = estadoInicial();
  const tenta = (entrada) => registrarSessao(estado, entrada, { hoje: HOJE, id: 'x' });
  assert.match(tenta({ data: HOJE, horas: 0 }).erro, /maior que zero/);
  assert.match(tenta({ data: HOJE, horas: 'abc' }).erro, /maior que zero/);
  assert.match(tenta({ data: HOJE, horas: 25 }).erro, /24 horas/);
  assert.match(tenta({ data: '2026-02-30', horas: 1 }).erro, /data válida/);
  assert.match(tenta({ data: '2026-09-25', horas: 1 }).erro, /futura/);
  assert.equal(estado.sessoes.length, 0);
});

test('remover sessão só tira a escolhida e não altera o original', () => {
  let estado = estadoInicial();
  estado = registrarSessao(estado, { data: HOJE, horas: 1 }, { hoje: HOJE, id: 's1' }).estado;
  estado = registrarSessao(estado, { data: HOJE, horas: 2 }, { hoje: HOJE, id: 's2' }).estado;
  const depois = removerSessao(estado, 's1');
  assert.deepEqual(depois.sessoes.map((s) => s.id), ['s2']);
  assert.equal(estado.sessoes.length, 2);
});

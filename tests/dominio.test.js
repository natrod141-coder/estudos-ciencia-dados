import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  progressoVazio, normalizarProgresso, avaliarTopico, corrigirQuiz, resumirProgresso,
  horasPorSemana, sequenciaDeSemanas, revisoesPendentes, proximoMarco, horasPorTopico,
} from '../src/dados/dominio.js';
import { estadoInicial } from '../src/dados/armazenamento.js';

const HOJE = '2026-09-24';
const completo = { temQuiz: true, temDesafio: true };

function progresso(parcial) {
  return { ...progressoVazio(), ...parcial };
}
function desafioAprovado(data) {
  return { testesPassando: 8, testesTotal: 8, tentativas: 2, aprovadoEm: data };
}
function av(topico, parcial, extra = {}) {
  return avaliarTopico(topico, progresso(parcial), { hoje: HOJE, ...extra });
}

// ---------------------------------------------------------------------------
// avaliarTopico
// ---------------------------------------------------------------------------

test('sem progresso o tópico não foi iniciado', () => {
  const r = avaliarTopico(completo, undefined, { hoje: HOJE });
  assert.equal(r.estado, 'nao_iniciado');
  assert.equal(r.criteriosCumpridos, 0);
  assert.equal(r.criteriosTotal, 3);
});

test('aula concluída, horas ou rascunho colocam o tópico em estudando', () => {
  assert.equal(av(completo, { aulasConcluidas: ['a1'] }).estado, 'estudando');
  assert.equal(av(completo, {}, { horasNoTopico: 0.5 }).estado, 'estudando');
  const comRascunho = progresso({ aberta: { rascunho: 'meu texto', rubricaMarcada: [], enviadaEm: null } });
  assert.equal(avaliarTopico(completo, comRascunho, { hoje: HOJE }).estado, 'estudando');
});

test('tentar o quiz ou o desafio coloca o tópico em praticando', () => {
  const quiz = av(completo, { tentativasQuiz: [{ data: '2026-09-20', nota: 60, acertos: 3, total: 5 }] });
  assert.equal(quiz.estado, 'praticando');
  assert.equal(quiz.criterios.quiz.melhorNota, 60);
  assert.equal(quiz.criterios.quiz.cumprido, false);

  const desafio = av(completo, { desafio: { testesPassando: 6, testesTotal: 8, tentativas: 1, aprovadoEm: null } });
  assert.equal(desafio.estado, 'praticando');
  assert.equal(desafio.criterios.desafio.cumprido, false);
});

test('a nota mínima do quiz é 80, inclusive', () => {
  const t79 = av({ temQuiz: true, temDesafio: false }, { tentativasQuiz: [{ data: '2026-09-20', nota: 79, acertos: 4, total: 5 }] });
  const t80 = av({ temQuiz: true, temDesafio: false }, { tentativasQuiz: [{ data: '2026-09-20', nota: 80, acertos: 4, total: 5 }] });
  assert.equal(t79.criterios.quiz.cumprido, false);
  assert.equal(t80.criterios.quiz.cumprido, true);
});

test('a data do critério do quiz é a da primeira tentativa que passou', () => {
  const r = av(completo, {
    tentativasQuiz: [
      { data: '2026-09-01', nota: 40, acertos: 2, total: 5 },
      { data: '2026-09-05', nota: 80, acertos: 4, total: 5 },
      { data: '2026-09-10', nota: 100, acertos: 5, total: 5 },
    ],
  });
  assert.equal(r.criterios.quiz.cumpridoEm, '2026-09-05');
  assert.equal(r.criterios.quiz.melhorNota, 100);
  assert.equal(r.criterios.quiz.tentativas, 3);
});

test('a revisão só é liberada quando quiz e desafio estão cumpridos', () => {
  const soQuiz = av(completo, { tentativasQuiz: [{ data: '2026-09-10', nota: 90, acertos: 5, total: 5 }] });
  assert.equal(soQuiz.criterios.revisao.liberaEm, null);
  assert.equal(soQuiz.criterios.revisao.liberada, false);

  const soDesafio = av(completo, { desafio: desafioAprovado('2026-09-10') });
  assert.equal(soDesafio.criterios.revisao.liberaEm, null);
});

test('a revisão libera 7 dias depois do último dos dois critérios', () => {
  const r = av(completo, {
    tentativasQuiz: [{ data: '2026-09-10', nota: 90, acertos: 5, total: 5 }],
    desafio: desafioAprovado('2026-09-15'),
  });
  assert.equal(r.criterios.revisao.liberaEm, '2026-09-22');
  assert.equal(r.criterios.revisao.liberada, true); // hoje é 24/9
  assert.equal(r.estado, 'praticando');
  assert.equal(r.criteriosCumpridos, 2);
});

test('revisão antes da data liberada ou com ok falso não conta', () => {
  const base = {
    tentativasQuiz: [{ data: '2026-09-10', nota: 90, acertos: 5, total: 5 }],
    desafio: desafioAprovado('2026-09-15'),
  };
  const cedo = av(completo, { ...base, revisoes: [{ data: '2026-09-20', ok: true }] });
  assert.equal(cedo.criterios.revisao.cumprido, false);
  assert.notEqual(cedo.estado, 'dominado');

  const falhou = av(completo, { ...base, revisoes: [{ data: '2026-09-23', ok: false }] });
  assert.equal(falhou.criterios.revisao.cumprido, false);
});

test('com os três critérios cumpridos o tópico está dominado', () => {
  const r = av(completo, {
    tentativasQuiz: [{ data: '2026-09-10', nota: 90, acertos: 5, total: 5 }],
    desafio: desafioAprovado('2026-09-15'),
    revisoes: [{ data: '2026-09-23', ok: false }, { data: '2026-09-24', ok: true }],
  });
  assert.equal(r.estado, 'dominado');
  assert.equal(r.criterios.revisao.cumpridoEm, '2026-09-24');
  assert.equal(r.criteriosCumpridos, 3);
});

test('tópico só com quiz exige quiz e revisão', () => {
  const soQuiz = { temQuiz: true, temDesafio: false };
  const r = av(soQuiz, {
    tentativasQuiz: [{ data: '2026-09-10', nota: 100, acertos: 5, total: 5 }],
    revisoes: [{ data: '2026-09-18', ok: true }],
  });
  assert.equal(r.criteriosTotal, 2);
  assert.equal(r.criterios.desafio.aplica, false);
  assert.equal(r.estado, 'dominado');
});

test('tópico sem quiz e sem desafio nunca chega a dominado', () => {
  const rascunho = { temQuiz: false, temDesafio: false };
  const r = av(rascunho, { aulasConcluidas: ['a1'], revisoes: [{ data: '2026-09-24', ok: true }] });
  assert.equal(r.estado, 'estudando');
  assert.equal(r.criteriosTotal, 0);
  assert.equal(r.criterios.revisao.aplica, false);
});

test('normalizarProgresso descarta dados inválidos sem lançar erro', () => {
  const r = normalizarProgresso({
    aulasConcluidas: ['a1', 5, null],
    tentativasQuiz: [{ data: '2026-09-01', nota: 150 }, { data: 'ontem', nota: 50 }, { data: '2026-09-02', nota: 50, acertos: 1, total: 2 }],
    aberta: { rascunho: 42, rubricaMarcada: [0, -1, 'x', 2], enviadaEm: 'nunca' },
    desafio: { testesPassando: -3, testesTotal: 'oito', tentativas: 2, aprovadoEm: '2026-02-31' },
    revisoes: [{ data: '2026-09-01', ok: 'sim' }, { data: '2026-09-01', ok: true }],
  });
  assert.deepEqual(r.aulasConcluidas, ['a1']);
  assert.equal(r.tentativasQuiz.length, 1);
  assert.equal(r.aberta.rascunho, '');
  assert.deepEqual(r.aberta.rubricaMarcada, [0, 2]);
  assert.equal(r.aberta.enviadaEm, null);
  assert.equal(r.desafio.testesPassando, 0);
  assert.equal(r.desafio.testesTotal, 0);
  assert.equal(r.desafio.aprovadoEm, null);
  assert.equal(r.revisoes.length, 1);
  assert.deepEqual(normalizarProgresso(null), progressoVazio());
  assert.deepEqual(normalizarProgresso('lixo'), progressoVazio());
});

// ---------------------------------------------------------------------------
// corrigirQuiz
// ---------------------------------------------------------------------------

test('corrigirQuiz conta acertos e arredonda a nota', () => {
  const quiz = [{ correta: 1 }, { correta: 0 }, { correta: 2 }];
  const r = corrigirQuiz(quiz, [1, 0, 0]);
  assert.equal(r.acertos, 2);
  assert.equal(r.total, 3);
  assert.equal(r.nota, 67);
  assert.deepEqual(r.detalhes.map((d) => d.acertou), [true, true, false]);
});

test('corrigirQuiz trata resposta em branco como erro', () => {
  const r = corrigirQuiz([{ correta: 0 }, { correta: 1 }], [null, undefined]);
  assert.equal(r.acertos, 0);
  assert.equal(r.nota, 0);
  assert.equal(r.detalhes[0].escolhida, null);
});

test('corrigirQuiz de um quiz vazio dá nota zero', () => {
  assert.equal(corrigirQuiz([], []).nota, 0);
});

// ---------------------------------------------------------------------------
// resumirProgresso
// ---------------------------------------------------------------------------

const trilhaDeTeste = {
  trilhas: [
    {
      id: 'dados',
      nome: 'Dados',
      modulos: [
        {
          id: 'm1', nome: 'M1', horas: 10,
          topicos: [
            { id: 'm1/a', titulo: 'A', temQuiz: true, temDesafio: false },
            { id: 'm1/b', titulo: 'B', temQuiz: true, temDesafio: false },
          ],
        },
        {
          id: 'm2', nome: 'M2', horas: 30,
          topicos: [{ id: 'm2/c', titulo: 'C', temQuiz: false, temDesafio: false }],
        },
      ],
    },
    { id: 'ia', nome: 'IA', modulos: [{ id: 'm3', nome: 'M3', horas: 10, topicos: [] }] },
  ],
};

test('progresso pondera os tópicos no módulo e os módulos pelas horas', () => {
  const estado = estadoInicial();
  estado.topicos['m1/a'] = progresso({
    tentativasQuiz: [{ data: '2026-09-01', nota: 100, acertos: 5, total: 5 }],
    revisoes: [{ data: '2026-09-10', ok: true }],
  });
  estado.topicos['m2/c'] = progresso({ aulasConcluidas: ['x'] });

  const r = resumirProgresso(trilhaDeTeste, estado, HOJE);
  assert.equal(r.porTopico['m1/a'].estado, 'dominado');
  assert.equal(r.porTopico['m1/b'].estado, 'nao_iniciado');
  assert.equal(r.porTopico['m2/c'].estado, 'estudando');

  assert.equal(r.porModulo.m1.pontuacao, 0.5);
  assert.equal(r.porModulo.m1.dominados, 1);
  assert.equal(r.porModulo.m1.horasEquivalentes, 5);
  assert.equal(r.porModulo.m2.pontuacao, 0.25);
  assert.equal(r.porModulo.m2.horasEquivalentes, 7.5);

  assert.equal(r.porTrilha.dados.horas, 40);
  assert.equal(r.porTrilha.dados.pontuacao, 12.5 / 40);
  assert.equal(r.porTrilha.ia.pontuacao, 0);
  assert.equal(r.geral.horas, 50);
  assert.equal(r.geral.pontuacao, 12.5 / 50);
});

test('progresso geral é zero quando nada foi feito e não divide por zero', () => {
  const r = resumirProgresso(trilhaDeTeste, estadoInicial(), HOJE);
  assert.equal(r.geral.pontuacao, 0);
  const vazio = resumirProgresso({ trilhas: [] }, estadoInicial(), HOJE);
  assert.equal(vazio.geral.pontuacao, 0);
});

test('horas registradas em um tópico contam como estudando', () => {
  const estado = estadoInicial();
  estado.sessoes.push({ id: 's1', data: '2026-09-20', horas: 1.5, topico: 'm1/b', nota: '' });
  const r = resumirProgresso(trilhaDeTeste, estado, HOJE);
  assert.equal(r.porTopico['m1/b'].estado, 'estudando');
  assert.deepEqual(horasPorTopico(estado.sessoes), { 'm1/b': 1.5 });
});

// ---------------------------------------------------------------------------
// Horas por semana
// ---------------------------------------------------------------------------

test('horasPorSemana agrupa de segunda a domingo e marca a semana atual', () => {
  const sessoes = [
    { data: '2026-09-21', horas: 1 }, // segunda da semana atual
    { data: '2026-09-24', horas: 2.5 }, // quinta, atual
    { data: '2026-09-20', horas: 3 }, // domingo, semana anterior
    { data: '2026-09-14', horas: 1.25 }, // segunda da semana anterior
    { data: '2026-01-01', horas: 9 }, // fora da janela
  ];
  const semanas = horasPorSemana(sessoes, HOJE, 3);
  assert.deepEqual(semanas.map((s) => s.inicio), ['2026-09-07', '2026-09-14', '2026-09-21']);
  assert.deepEqual(semanas.map((s) => s.horas), [0, 4.25, 3.5]);
  assert.deepEqual(semanas.map((s) => s.atual), [false, false, true]);
});

test('horasPorSemana devolve a quantidade pedida mesmo sem sessões', () => {
  const semanas = horasPorSemana([], HOJE, 8);
  assert.equal(semanas.length, 8);
  assert.ok(semanas.every((s) => s.horas === 0));
});

test('horasPorSemana não acumula erro de ponto flutuante', () => {
  const sessoes = [0.1, 0.2, 0.3].map((horas) => ({ data: HOJE, horas }));
  assert.equal(horasPorSemana(sessoes, HOJE, 1)[0].horas, 0.6);
});

test('sequência de semanas cumprindo a meta', () => {
  const semana = (horas, atual = false) => ({ inicio: 'x', horas, atual });
  // as três últimas semanas fechadas cumpriram; a atual ainda não
  assert.equal(sequenciaDeSemanas([semana(2), semana(5), semana(6), semana(5.5), semana(1, true)], 5), 3);
  // a atual já cumpriu e entra na conta
  assert.equal(sequenciaDeSemanas([semana(2), semana(5), semana(6), semana(5, true)], 5), 3);
  // uma semana fechada abaixo da meta quebra a sequência
  assert.equal(sequenciaDeSemanas([semana(6), semana(4.9), semana(6), semana(1, true)], 5), 1);
  assert.equal(sequenciaDeSemanas([semana(1), semana(1, true)], 5), 0);
  assert.equal(sequenciaDeSemanas([], 5), 0);
});

// ---------------------------------------------------------------------------
// Revisões e marcos
// ---------------------------------------------------------------------------

test('revisões pendentes separam o que já pode ser revisado do que ainda espera', () => {
  const estado = estadoInicial();
  // liberada em 17/9 (quiz em 10/9), portanto já disponível e atrasada
  estado.topicos['m1/a'] = progresso({ tentativasQuiz: [{ data: '2026-09-10', nota: 90, acertos: 5, total: 5 }] });
  // liberada em 27/9, ainda espera
  estado.topicos['m1/b'] = progresso({ tentativasQuiz: [{ data: '2026-09-20', nota: 90, acertos: 5, total: 5 }] });
  const resumo = resumirProgresso(trilhaDeTeste, estado, HOJE);
  const r = revisoesPendentes(trilhaDeTeste, resumo, HOJE);

  assert.equal(r.disponiveis.length, 1);
  assert.equal(r.disponiveis[0].id, 'm1/a');
  assert.equal(r.disponiveis[0].atrasoDias, 7);
  assert.equal(r.proximas.length, 1);
  assert.equal(r.proximas[0].id, 'm1/b');
  assert.equal(r.proximas[0].diasParaLiberar, 3);
});

test('revisão já feita sai da lista de pendentes', () => {
  const estado = estadoInicial();
  estado.topicos['m1/a'] = progresso({
    tentativasQuiz: [{ data: '2026-09-10', nota: 90, acertos: 5, total: 5 }],
    revisoes: [{ data: '2026-09-18', ok: true }],
  });
  const resumo = resumirProgresso(trilhaDeTeste, estado, HOJE);
  const r = revisoesPendentes(trilhaDeTeste, resumo, HOJE);
  assert.equal(r.disponiveis.length + r.proximas.length, 0);
});

test('próximo marco ignora os que já passaram', () => {
  const marcos = [
    { id: 'a', titulo: 'Passado', data: '2026-09-01' },
    { id: 'c', titulo: 'Depois', data: '2026-12-01' },
    { id: 'b', titulo: 'Prova', data: '2026-10-03' },
  ];
  const m = proximoMarco(marcos, HOJE);
  assert.equal(m.id, 'b');
  assert.equal(m.dias, 9);
  assert.equal(proximoMarco(marcos, '2027-01-01'), null);
  assert.equal(proximoMarco([], HOJE), null);
  assert.equal(proximoMarco(marcos, '2026-10-03').dias, 0);
});

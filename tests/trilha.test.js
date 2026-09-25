import { test } from 'node:test';
import assert from 'node:assert/strict';
import { montarTrilha, vizinhosDoTopico } from '../src/dados/trilha.js';

const config = {
  trilhas: [{ id: 'dados', nome: 'Trilha de dados' }, { id: 'ia', nome: 'Trilha de IA' }],
  modulos: [
    { id: 'estatistica', nome: 'Estatística', trilha: 'dados', fase: 1 },
    { id: 'rag', nome: 'RAG', trilha: 'ia', fase: 3 },
  ],
};

function topico(id, modulo, ordem, horas, extra = {}) {
  return { id, data: { titulo: id.toUpperCase(), modulo, ordem, horas, estado: 'publicado', ...extra } };
}

test('monta trilhas, módulos e tópicos em ordem, com as horas somadas', () => {
  const trilha = montarTrilha(config, [
    topico('estatistica/b', 'estatistica', 2, 3),
    topico('estatistica/a', 'estatistica', 1, 4, {
      aulas: [{ id: 'a1' }, { id: 'a2' }], quiz: [{ correta: 0 }], desafio: { testes: 8 },
    }),
    topico('rag/x', 'rag', 1, 6, { estado: 'rascunho' }),
  ]);

  assert.equal(trilha.trilhas.length, 2);
  const [dados, ia] = trilha.trilhas;
  assert.equal(dados.horas, 7);
  assert.equal(ia.horas, 6);

  const modulo = dados.modulos[0];
  assert.deepEqual(modulo.topicos.map((t) => t.id), ['estatistica/a', 'estatistica/b']);
  assert.equal(modulo.horas, 7);

  const a = trilha.topicosPorId['estatistica/a'];
  assert.equal(a.temQuiz, true);
  assert.equal(a.temDesafio, true);
  assert.deepEqual(a.aulas, ['a1', 'a2']);
  assert.equal(a.rascunho, false);
  assert.equal(a.trilha, 'dados');
  assert.equal(a.moduloNome, 'Estatística');

  const x = trilha.topicosPorId['rag/x'];
  assert.equal(x.temQuiz, false);
  assert.equal(x.temDesafio, false);
  assert.equal(x.rascunho, true);
});

test('módulo sem tópicos continua existindo, com zero horas', () => {
  const trilha = montarTrilha(config, [topico('estatistica/a', 'estatistica', 1, 2)]);
  assert.equal(trilha.trilhas[1].modulos[0].topicos.length, 0);
  assert.equal(trilha.trilhas[1].horas, 0);
});

test('erros de configuração dizem o que corrigir', () => {
  assert.throws(
    () => montarTrilha(config, [topico('x/y', 'inexistente', 1, 1)]),
    /módulo "inexistente", que não existe/,
  );
  assert.throws(
    () => montarTrilha({ ...config, modulos: [...config.modulos, { id: 'estatistica', nome: 'E', trilha: 'dados', fase: 1 }] }, []),
    /aparece duas vezes/,
  );
  assert.throws(
    () => montarTrilha({ ...config, modulos: [{ id: 'm', nome: 'M', trilha: 'nada', fase: 1 }] }, []),
    /trilha "nada", que não existe/,
  );
  assert.throws(
    () => montarTrilha(config, [topico('estatistica/a', 'estatistica', 1, 1), topico('estatistica/a', 'estatistica', 2, 1)]),
    /duplicado/,
  );
  assert.throws(
    () => montarTrilha(config, [topico('estatistica/a', 'estatistica', 1, 1, { aulas: [{ id: 'x' }, { id: 'x' }] })]),
    /mesmo id/,
  );
  assert.throws(() => montarTrilha({}, []), /trilhas.json/);
});

test('vizinhos do tópico dentro do módulo', () => {
  const trilha = montarTrilha(config, [
    topico('estatistica/a', 'estatistica', 1, 1),
    topico('estatistica/b', 'estatistica', 2, 1),
    topico('estatistica/c', 'estatistica', 3, 1),
  ]);
  assert.equal(vizinhosDoTopico(trilha, 'estatistica/b').anterior.id, 'estatistica/a');
  assert.equal(vizinhosDoTopico(trilha, 'estatistica/b').proximo.id, 'estatistica/c');
  assert.equal(vizinhosDoTopico(trilha, 'estatistica/a').anterior, null);
  assert.equal(vizinhosDoTopico(trilha, 'estatistica/c').proximo, null);
  assert.deepEqual(vizinhosDoTopico(trilha, 'nao/existe'), { anterior: null, proximo: null });
});

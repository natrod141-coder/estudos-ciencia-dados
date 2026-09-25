import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  somarDias, diasEntre, segundaDaSemana, formatarDiaMes, formatarPorExtenso,
  dataValida, hojeISO, maiorData,
} from '../src/dados/datas.js';

test('somarDias atravessa meses e anos', () => {
  assert.equal(somarDias('2026-09-24', 7), '2026-10-01');
  assert.equal(somarDias('2026-12-30', 3), '2027-01-02');
  assert.equal(somarDias('2026-03-01', -1), '2026-02-28');
  assert.equal(somarDias('2028-02-28', 1), '2028-02-29'); // ano bissexto
});

test('diasEntre conta em ambos os sentidos', () => {
  assert.equal(diasEntre('2026-09-24', '2026-10-03'), 9);
  assert.equal(diasEntre('2026-10-03', '2026-09-24'), -9);
  assert.equal(diasEntre('2026-09-24', '2026-09-24'), 0);
});

test('segundaDaSemana: a semana começa na segunda', () => {
  assert.equal(segundaDaSemana('2026-09-24'), '2026-09-21'); // quinta
  assert.equal(segundaDaSemana('2026-09-21'), '2026-09-21'); // segunda
  assert.equal(segundaDaSemana('2026-09-27'), '2026-09-21'); // domingo
  assert.equal(segundaDaSemana('2026-09-28'), '2026-09-28'); // próxima segunda
});

test('datas inválidas são rejeitadas', () => {
  assert.equal(dataValida('2026-09-24'), true);
  assert.equal(dataValida('2026-02-30'), false);
  assert.equal(dataValida('24/09/2026'), false);
  assert.equal(dataValida(null), false);
  assert.throws(() => somarDias('ontem', 1), /Data inválida/);
  assert.throws(() => diasEntre('2026-13-01', '2026-01-01'), /inexistente/);
});

test('formatação em português', () => {
  assert.equal(formatarDiaMes('2026-09-05'), '5/9');
  assert.equal(formatarPorExtenso('2026-09-24'), 'Quinta, 24 de setembro de 2026');
  assert.equal(formatarPorExtenso('2026-10-03'), 'Sábado, 3 de outubro de 2026');
});

test('hojeISO usa o fuso local', () => {
  assert.equal(hojeISO(new Date(2026, 8, 24, 23, 59)), '2026-09-24');
  assert.equal(hojeISO(new Date(2026, 0, 2, 0, 1)), '2026-01-02');
});

test('maiorData', () => {
  assert.equal(maiorData(['2026-09-01', '2026-10-01', '2026-09-30']), '2026-10-01');
});

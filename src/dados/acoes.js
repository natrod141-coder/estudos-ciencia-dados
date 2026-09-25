// Ações que mudam o progresso. Cada uma devolve uma cópia nova, sem alterar a original,
// e valida o que a pessoa digitou antes de aceitar.

import { normalizarProgresso } from './dominio.js';
import { dataValida } from './datas.js';

const MAX_TENTATIVAS_GUARDADAS = 50;

function clonar(valor) {
  return structuredClone(valor);
}

export function gerarId() {
  if (globalThis.crypto && typeof globalThis.crypto.randomUUID === 'function') {
    return globalThis.crypto.randomUUID();
  }
  return `s${Date.now().toString(36)}${Math.random().toString(36).slice(2, 8)}`;
}

/** Aplica `alterar` ao progresso de um tópico e devolve o estado novo. */
export function comProgresso(estado, topicoId, alterar) {
  const copia = clonar(estado);
  const atual = normalizarProgresso(copia.topicos[topicoId]);
  copia.topicos[topicoId] = alterar(atual) ?? atual;
  return copia;
}

// Cada função abaixo recebe o progresso de UM tópico e devolve o progresso novo.

export function alternarAula(progresso, aulaId, concluida) {
  const restantes = progresso.aulasConcluidas.filter((id) => id !== aulaId);
  return { ...progresso, aulasConcluidas: concluida ? [...restantes, aulaId] : restantes };
}

export function registrarQuiz(progresso, { nota, acertos, total }, hoje) {
  const tentativas = [...progresso.tentativasQuiz, { data: hoje, nota, acertos, total }];
  return { ...progresso, tentativasQuiz: tentativas.slice(-MAX_TENTATIVAS_GUARDADAS) };
}

export function salvarRascunho(progresso, texto) {
  return { ...progresso, aberta: { ...progresso.aberta, rascunho: String(texto).slice(0, 5000) } };
}

export function marcarRubrica(progresso, indice, marcado) {
  const restantes = progresso.aberta.rubricaMarcada.filter((n) => n !== indice);
  const rubricaMarcada = marcado ? [...restantes, indice].sort((a, b) => a - b) : restantes;
  return { ...progresso, aberta: { ...progresso.aberta, rubricaMarcada } };
}

export function enviarAberta(progresso, hoje) {
  return { ...progresso, aberta: { ...progresso.aberta, enviadaEm: hoje } };
}

/**
 * Registra o resultado de uma rodada de testes do desafio.
 * Devolve { ok: true, progresso } ou { ok: false, erro }.
 */
export function registrarDesafio(progresso, { passando, total }, hoje) {
  if (!Number.isInteger(total) || total <= 0) {
    return { ok: false, erro: 'O desafio precisa ter ao menos um teste.' };
  }
  if (!Number.isInteger(passando) || passando < 0 || passando > total) {
    return { ok: false, erro: `Informe um número de testes entre 0 e ${total}.` };
  }
  const aprovadoEm = progresso.desafio.aprovadoEm ?? (passando === total ? hoje : null);
  return {
    ok: true,
    progresso: {
      ...progresso,
      desafio: {
        testesPassando: passando,
        testesTotal: total,
        tentativas: progresso.desafio.tentativas + 1,
        aprovadoEm,
      },
    },
  };
}

export function registrarRevisao(progresso, ok, hoje) {
  return { ...progresso, revisoes: [...progresso.revisoes, { data: hoje, ok: Boolean(ok) }] };
}

// Sessões de estudo (horas registradas)

/**
 * Registra horas estudadas. Devolve { ok: true, estado } ou { ok: false, erro }.
 */
export function registrarSessao(estado, entrada, { hoje, id = gerarId() }) {
  const horas = Number(entrada.horas);
  if (!Number.isFinite(horas) || horas <= 0) {
    return { ok: false, erro: 'Informe quantas horas você estudou, com um número maior que zero.' };
  }
  if (horas > 24) {
    return { ok: false, erro: 'Um dia tem 24 horas. Confira o valor informado.' };
  }
  if (!dataValida(entrada.data)) {
    return { ok: false, erro: 'Informe uma data válida.' };
  }
  if (entrada.data > hoje) {
    return { ok: false, erro: 'Não dá para registrar horas em uma data futura.' };
  }
  const topico = entrada.topico ? String(entrada.topico) : null;
  const nota = String(entrada.nota ?? '').trim().slice(0, 200);

  const copia = clonar(estado);
  copia.sessoes.push({ id, data: entrada.data, horas: Math.round(horas * 100) / 100, topico, nota });
  copia.sessoes.sort((a, b) => (a.data < b.data ? -1 : a.data > b.data ? 1 : 0));
  return { ok: true, estado: copia };
}

export function removerSessao(estado, id) {
  const copia = clonar(estado);
  copia.sessoes = copia.sessoes.filter((s) => s.id !== id);
  return copia;
}

// Regras do painel. Nenhuma função aqui mexe na tela ou no navegador:
// todas recebem dados e devolvem resultados, o que permite testar tudo com `npm test`.

import { META_QUIZ, DIAS_ATE_REVISAO, PESO_ESTADO } from './constantes.js';
import { somarDias, diasEntre, segundaDaSemana, maiorData, dataValida } from './datas.js';

// ---------------------------------------------------------------------------
// Progresso de um tópico
// ---------------------------------------------------------------------------

export function progressoVazio() {
  return {
    aulasConcluidas: [],
    tentativasQuiz: [], // { data, nota, acertos, total }
    aberta: { rascunho: '', rubricaMarcada: [], enviadaEm: null },
    desafio: { testesPassando: 0, testesTotal: 0, tentativas: 0, aprovadoEm: null },
    revisoes: [], // { data, ok }
  };
}

function tentativaValida(t) {
  return (
    t && typeof t === 'object' && dataValida(t.data) &&
    Number.isFinite(t.nota) && t.nota >= 0 && t.nota <= 100
  );
}

function revisaoValida(r) {
  return r && typeof r === 'object' && dataValida(r.data) && typeof r.ok === 'boolean';
}

/** Completa o que faltar e descarta o que estiver inválido (dados vindos do navegador). */
export function normalizarProgresso(bruto) {
  const base = progressoVazio();
  if (!bruto || typeof bruto !== 'object') return base;
  const aberta = bruto.aberta && typeof bruto.aberta === 'object' ? bruto.aberta : {};
  const desafio = bruto.desafio && typeof bruto.desafio === 'object' ? bruto.desafio : {};
  const numero = (v) => (Number.isFinite(v) && v >= 0 ? v : 0);
  return {
    aulasConcluidas: Array.isArray(bruto.aulasConcluidas)
      ? bruto.aulasConcluidas.filter((id) => typeof id === 'string')
      : base.aulasConcluidas,
    tentativasQuiz: Array.isArray(bruto.tentativasQuiz)
      ? bruto.tentativasQuiz.filter(tentativaValida)
      : base.tentativasQuiz,
    aberta: {
      rascunho: typeof aberta.rascunho === 'string' ? aberta.rascunho : '',
      rubricaMarcada: Array.isArray(aberta.rubricaMarcada)
        ? aberta.rubricaMarcada.filter((n) => Number.isInteger(n) && n >= 0)
        : [],
      enviadaEm: dataValida(aberta.enviadaEm) ? aberta.enviadaEm : null,
    },
    desafio: {
      testesPassando: numero(desafio.testesPassando),
      testesTotal: numero(desafio.testesTotal),
      tentativas: numero(desafio.tentativas),
      aprovadoEm: dataValida(desafio.aprovadoEm) ? desafio.aprovadoEm : null,
    },
    revisoes: Array.isArray(bruto.revisoes) ? bruto.revisoes.filter(revisaoValida) : base.revisoes,
  };
}

/**
 * Calcula o estado de um tópico e o cumprimento dos três critérios de domínio:
 *   1. quiz com nota mínima (META_QUIZ)
 *   2. desafio prático aprovado (todos os testes passando)
 *   3. revisão bem sucedida, liberada DIAS_ATE_REVISAO dias depois dos critérios 1 e 2
 *
 * `topico` diz o que existe no tópico: { temQuiz, temDesafio }.
 * Um critério que o tópico não tem não é exigido. Sem quiz e sem desafio,
 * o tópico não pode ser dominado (ainda não há como comprovar).
 */
export function avaliarTopico(topico, progresso, { hoje, horasNoTopico = 0 }) {
  const p = normalizarProgresso(progresso);

  const aprovacao = p.tentativasQuiz.find((t) => t.nota >= META_QUIZ);
  const quiz = {
    aplica: Boolean(topico.temQuiz),
    cumprido: Boolean(aprovacao),
    cumpridoEm: aprovacao ? aprovacao.data : null,
    melhorNota: p.tentativasQuiz.length ? Math.max(...p.tentativasQuiz.map((t) => t.nota)) : null,
    tentativas: p.tentativasQuiz.length,
  };

  const desafio = {
    aplica: Boolean(topico.temDesafio),
    cumprido: p.desafio.aprovadoEm !== null,
    cumpridoEm: p.desafio.aprovadoEm,
    testesPassando: p.desafio.testesPassando,
    testesTotal: p.desafio.testesTotal,
    tentativas: p.desafio.tentativas,
  };

  const exigidosBase = [quiz, desafio].filter((c) => c.aplica);
  const algumCriterio = exigidosBase.length > 0;
  const baseCumprida = algumCriterio && exigidosBase.every((c) => c.cumprido);

  const dataBase = baseCumprida ? maiorData(exigidosBase.map((c) => c.cumpridoEm)) : null;
  const liberaEm = dataBase ? somarDias(dataBase, DIAS_ATE_REVISAO) : null;
  const revisaoOk = liberaEm ? p.revisoes.find((r) => r.ok && r.data >= liberaEm) : undefined;
  const revisao = {
    aplica: algumCriterio,
    liberaEm,
    liberada: liberaEm !== null && hoje >= liberaEm,
    cumprido: Boolean(revisaoOk),
    cumpridoEm: revisaoOk ? revisaoOk.data : null,
  };

  const exigidos = [quiz, desafio, revisao].filter((c) => c.aplica);
  const dominado = algumCriterio && exigidos.every((c) => c.cumprido);
  const praticou =
    p.tentativasQuiz.length > 0 || p.desafio.tentativas > 0 ||
    p.desafio.testesPassando > 0 || p.aberta.enviadaEm !== null;
  const estudou =
    p.aulasConcluidas.length > 0 || horasNoTopico > 0 || p.aberta.rascunho.trim() !== '';

  let estado = 'nao_iniciado';
  if (dominado) estado = 'dominado';
  else if (praticou) estado = 'praticando';
  else if (estudou) estado = 'estudando';

  return { estado, criterios: { quiz, desafio, revisao }, criteriosCumpridos: exigidos.filter((c) => c.cumprido).length, criteriosTotal: exigidos.length };
}

/**
 * Corrige um quiz. `quiz` é a lista de perguntas ({ correta: indice }) e
 * `respostas` é a lista de índices escolhidos (null quando ficou em branco).
 */
export function corrigirQuiz(quiz, respostas) {
  const detalhes = quiz.map((pergunta, i) => {
    const escolhida = Number.isInteger(respostas[i]) ? respostas[i] : null;
    return { escolhida, certa: pergunta.correta, acertou: escolhida === pergunta.correta };
  });
  const acertos = detalhes.filter((d) => d.acertou).length;
  const total = quiz.length;
  const nota = total === 0 ? 0 : Math.round((acertos / total) * 100);
  return { acertos, total, nota, detalhes };
}

// ---------------------------------------------------------------------------
// Progresso de módulos, trilhas e geral
// ---------------------------------------------------------------------------

export function horasPorTopico(sessoes) {
  const soma = {};
  for (const s of sessoes) {
    if (s.topico) soma[s.topico] = arredondar((soma[s.topico] ?? 0) + s.horas);
  }
  return soma;
}

/**
 * Resume o progresso de tudo. `trilha` vem de montarTrilha() e `estado` do armazenamento.
 * Cada tópico vale igual dentro do módulo, e cada módulo pesa pelas suas horas estimadas.
 */
export function resumirProgresso(trilha, estado, hoje) {
  const horasNoTopico = horasPorTopico(estado.sessoes);
  const porTopico = {};
  const porModulo = {};
  const porTrilha = {};
  let horasTotais = 0;
  let horasEquivalentes = 0;

  for (const t of trilha.trilhas) {
    let horasDaTrilha = 0;
    let equivalentesDaTrilha = 0;
    for (const m of t.modulos) {
      let soma = 0;
      let dominados = 0;
      for (const topico of m.topicos) {
        const avaliacao = avaliarTopico(topico, estado.topicos[topico.id], {
          hoje,
          horasNoTopico: horasNoTopico[topico.id] ?? 0,
        });
        porTopico[topico.id] = avaliacao;
        soma += PESO_ESTADO[avaliacao.estado];
        if (avaliacao.estado === 'dominado') dominados += 1;
      }
      const pontuacao = m.topicos.length ? soma / m.topicos.length : 0;
      porModulo[m.id] = {
        pontuacao, dominados, total: m.topicos.length,
        horas: m.horas, horasEquivalentes: pontuacao * m.horas,
      };
      horasDaTrilha += m.horas;
      equivalentesDaTrilha += pontuacao * m.horas;
    }
    porTrilha[t.id] = {
      pontuacao: horasDaTrilha ? equivalentesDaTrilha / horasDaTrilha : 0,
      horas: horasDaTrilha, horasEquivalentes: equivalentesDaTrilha,
    };
    horasTotais += horasDaTrilha;
    horasEquivalentes += equivalentesDaTrilha;
  }

  return {
    porTopico, porModulo, porTrilha,
    geral: {
      pontuacao: horasTotais ? horasEquivalentes / horasTotais : 0,
      horas: horasTotais, horasEquivalentes,
    },
  };
}

// ---------------------------------------------------------------------------
// Horas por semana e sequência
// ---------------------------------------------------------------------------

export function arredondar(valor, casas = 2) {
  const fator = 10 ** casas;
  return Math.round(valor * fator) / fator;
}

/** Horas das últimas `quantidade` semanas (segunda a domingo), da mais antiga à atual. */
export function horasPorSemana(sessoes, hoje, quantidade = 8) {
  const segundaAtual = segundaDaSemana(hoje);
  const semanas = [];
  for (let i = quantidade - 1; i >= 0; i -= 1) {
    semanas.push({ inicio: somarDias(segundaAtual, -7 * i), horas: 0, atual: i === 0 });
  }
  const porInicio = new Map(semanas.map((s) => [s.inicio, s]));
  for (const sessao of sessoes) {
    const semana = porInicio.get(segundaDaSemana(sessao.data));
    if (semana) semana.horas += sessao.horas;
  }
  return semanas.map((s) => ({ ...s, horas: arredondar(s.horas) }));
}

/**
 * Semanas seguidas cumprindo a meta. A semana atual só entra na conta se já
 * cumpriu a meta; se ainda não cumpriu, ela não quebra a sequência antes de terminar.
 */
export function sequenciaDeSemanas(semanas, meta) {
  let i = semanas.length - 1;
  if (i >= 0 && semanas[i].horas < meta) i -= 1;
  let total = 0;
  while (i >= 0 && semanas[i].horas >= meta) {
    total += 1;
    i -= 1;
  }
  return total;
}

// ---------------------------------------------------------------------------
// Revisões
// ---------------------------------------------------------------------------

/**
 * Tópicos com revisão a fazer. `disponiveis` já podem ser revisados;
 * `proximas` ainda estão esperando os 7 dias.
 */
export function revisoesPendentes(trilha, resumo, hoje) {
  const disponiveis = [];
  const proximas = [];
  for (const t of trilha.trilhas) {
    for (const m of t.modulos) {
      for (const topico of m.topicos) {
        const revisao = resumo.porTopico[topico.id].criterios.revisao;
        if (!revisao.aplica || revisao.liberaEm === null || revisao.cumprido) continue;
        const item = {
          id: topico.id,
          titulo: topico.titulo,
          liberaEm: revisao.liberaEm,
          atrasoDias: Math.max(0, diasEntre(revisao.liberaEm, hoje)),
          diasParaLiberar: Math.max(0, diasEntre(hoje, revisao.liberaEm)),
        };
        (revisao.liberada ? disponiveis : proximas).push(item);
      }
    }
  }
  const porData = (a, b) => (a.liberaEm < b.liberaEm ? -1 : a.liberaEm > b.liberaEm ? 1 : 0);
  return { disponiveis: disponiveis.sort(porData), proximas: proximas.sort(porData) };
}

// ---------------------------------------------------------------------------
// Marcos (provas, entregas)
// ---------------------------------------------------------------------------

/** O próximo marco que ainda não passou, com quantos dias faltam. */
export function proximoMarco(marcos, hoje) {
  const futuros = marcos
    .filter((m) => m.data >= hoje)
    .sort((a, b) => (a.data < b.data ? -1 : 1));
  if (futuros.length === 0) return null;
  return { ...futuros[0], dias: diasEntre(hoje, futuros[0].data) };
}

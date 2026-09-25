// Torna a página de um tópico interativa. O HTML (conteúdo, perguntas, passos) vem pronto
// do build; aqui só lemos o progresso guardado no navegador e reagimos aos cliques.
// Toda a regra de domínio fica em src/dados/, que tem testes automáticos.

import { atualizarEstado, mostrarMensagem, obterEstado } from './estado.js';
import {
  alternarAula, comProgresso, enviarAberta, marcarRubrica, registrarDesafio,
  registrarQuiz, registrarRevisao, salvarRascunho,
} from '../dados/acoes.js';
import { avaliarTopico, corrigirQuiz, horasPorTopico, normalizarProgresso } from '../dados/dominio.js';
import { formatarDiaMes, hojeISO, diasEntre } from '../dados/datas.js';
import { ROTULO_ESTADO } from '../dados/constantes.js';
import { formatarHoras, plural } from './formato.js';

const dados = JSON.parse(document.getElementById('dados-topico').textContent);
const topicoParaAvaliar = { temQuiz: dados.temQuiz, temDesafio: dados.temDesafio };

const $ = (seletor, raiz = document) => raiz.querySelector(seletor);
const $$ = (seletor, raiz = document) => [...raiz.querySelectorAll(seletor)];

function progressoAtual() {
  return normalizarProgresso(obterEstado().topicos[dados.id]);
}

/** Aplica uma mudança ao progresso deste tópico. */
function mudarProgresso(alterar) {
  return atualizarEstado((estado) => comProgresso(estado, dados.id, alterar));
}

// ---------------------------------------------------------------------------
// Critérios de domínio
// ---------------------------------------------------------------------------

function descreverQuiz(c) {
  if (!c.aplica) return { situacao: 'nao_se_aplica', rotulo: 'Sem quiz', detalhe: 'Este tópico ainda não tem quiz.', fracao: 0 };
  if (c.cumprido) {
    return {
      situacao: 'cumprido', rotulo: 'Cumprido', fracao: c.melhorNota / 100,
      detalhe: `Aprovado em ${formatarDiaMes(c.cumpridoEm)}. Melhor nota: ${c.melhorNota}%.`,
    };
  }
  if (c.tentativas > 0) {
    return {
      situacao: 'refazer', rotulo: 'Refazer', fracao: c.melhorNota / 100,
      detalhe: `Melhor nota: ${c.melhorNota}%, em ${c.tentativas} ${plural(c.tentativas, 'tentativa', 'tentativas')}. A meta é ${dados.meta}%.`,
    };
  }
  return { situacao: 'pendente', rotulo: 'Não feito', detalhe: `Faça o quiz abaixo. A meta é ${dados.meta}%.`, fracao: 0 };
}

function descreverDesafio(c) {
  if (!c.aplica) return { situacao: 'nao_se_aplica', rotulo: 'Sem desafio', detalhe: 'Este tópico ainda não tem desafio.', fracao: 0 };
  const total = c.testesTotal || dados.desafioTotal;
  if (c.cumprido) {
    return {
      situacao: 'cumprido', rotulo: 'Cumprido', fracao: 1,
      detalhe: `Todos os ${total} testes passaram. Aprovado em ${formatarDiaMes(c.cumpridoEm)}.`,
    };
  }
  if (c.tentativas > 0) {
    return {
      situacao: 'andamento', rotulo: 'Em andamento', fracao: total ? c.testesPassando / total : 0,
      detalhe: `${c.testesPassando} de ${total} testes passando na última rodada.`,
    };
  }
  return { situacao: 'pendente', rotulo: 'Não iniciado', detalhe: 'Siga o passo a passo do desafio, mais abaixo.', fracao: 0 };
}

function descreverRevisao(c, hoje) {
  if (!c.aplica) return { situacao: 'nao_se_aplica', rotulo: 'Não se aplica', detalhe: 'Depende de o tópico ter quiz ou desafio.', fracao: 0 };
  if (c.cumprido) {
    return { situacao: 'cumprido', rotulo: 'Cumprido', detalhe: `Revisão feita em ${formatarDiaMes(c.cumpridoEm)}.`, fracao: 1 };
  }
  if (c.liberaEm === null) {
    return {
      situacao: 'pendente', rotulo: 'Bloqueada', fracao: 0,
      detalhe: `Libera ${dados.diasRevisao} dias depois de cumprir os critérios anteriores.`,
    };
  }
  if (c.liberada) {
    return {
      situacao: 'disponivel', rotulo: 'Disponível', fracao: 0,
      detalhe: `Liberada em ${formatarDiaMes(c.liberaEm)}. Tente refazer o tópico de memória e registre como foi.`,
    };
  }
  const dias = diasEntre(hoje, c.liberaEm);
  return {
    situacao: 'pendente', rotulo: `Libera em ${formatarDiaMes(c.liberaEm)}`, fracao: 0,
    detalhe: `Faltam ${dias} ${plural(dias, 'dia', 'dias')} para a revisão.`,
  };
}

function desenharCriterios(avaliacao, hoje) {
  const total = $('[data-campo="criterios-total"]');
  if (total) total.textContent = `${avaliacao.criteriosCumpridos} de ${avaliacao.criteriosTotal}`;

  const descricoes = {
    quiz: descreverQuiz(avaliacao.criterios.quiz),
    desafio: descreverDesafio(avaliacao.criterios.desafio),
    revisao: descreverRevisao(avaliacao.criterios.revisao, hoje),
  };
  for (const cartao of $$('[data-criterio]')) {
    const d = descricoes[cartao.dataset.criterio];
    cartao.dataset.situacao = d.situacao;
    $('[data-campo="situacao"]', cartao).textContent = d.rotulo;
    $('[data-campo="detalhe"]', cartao).textContent = d.detalhe;
    $('[data-campo="barra"]', cartao).style.width = `${Math.round(Math.min(1, d.fracao) * 100)}%`;
  }
  const acoes = $('[data-campo="acoes-revisao"]');
  if (acoes) acoes.hidden = descricoes.revisao.situacao !== 'disponivel';
}

// ---------------------------------------------------------------------------
// Cabeçalho, aulas e lateral
// ---------------------------------------------------------------------------

function desenharCabecalho(avaliacao) {
  const chip = $('[data-estado-topico]');
  if (chip) chip.dataset.estado = avaliacao.estado;
  const rotulo = $('[data-rotulo-topico]');
  if (rotulo) rotulo.textContent = ROTULO_ESTADO[avaliacao.estado];
}

function desenharAulas(progresso) {
  for (const caixa of $$('[data-aula]')) {
    caixa.checked = progresso.aulasConcluidas.includes(caixa.dataset.aula);
  }
  const concluidas = dados.aulas.filter((id) => progresso.aulasConcluidas.includes(id)).length;
  const resumo = $('[data-campo="aulas-progresso"]');
  if (resumo) resumo.textContent = `${concluidas} de ${dados.aulas.length} aulas concluídas`;
  const total = $('[data-campo="aulas-total"]');
  if (total) total.textContent = `${concluidas} de ${dados.aulas.length}`;
}

function desenharLateral(progresso, horas) {
  const campoHoras = $('[data-campo="horas-topico"]');
  if (campoHoras) campoHoras.textContent = formatarHoras(horas);
  const tentativas = $('[data-campo="tentativas-quiz"]');
  if (tentativas) tentativas.textContent = String(progresso.tentativasQuiz.length);
}

// ---------------------------------------------------------------------------
// Quiz
// ---------------------------------------------------------------------------

const formQuiz = $('#form-quiz');
const painelResultado = $('#resultado-quiz');
const botaoCorrigir = $('#corrigir-quiz');
const botaoRefazer = $('#refazer-quiz');

function respostasEscolhidas() {
  return dados.quiz.map((_, i) => {
    const marcada = $(`input[name="q${i}"]:checked`, formQuiz);
    return marcada ? Number(marcada.value) : null;
  });
}

function mostrarCorrecao(resultado) {
  resultado.detalhes.forEach((detalhe, i) => {
    const pergunta = $(`[data-pergunta="${i}"]`, formQuiz);
    $$('.opcao', pergunta).forEach((opcao, j) => {
      const etiqueta = $('[data-campo="etiqueta"]', opcao);
      opcao.dataset.bloqueada = 'true';
      $('input', opcao).disabled = true;
      delete opcao.dataset.resultado;
      etiqueta.textContent = '';
      if (j === detalhe.certa) {
        opcao.dataset.resultado = 'certa';
        etiqueta.textContent = j === detalhe.escolhida ? 'Sua resposta, certa' : 'Resposta certa';
      } else if (j === detalhe.escolhida) {
        opcao.dataset.resultado = 'errada';
        etiqueta.textContent = 'Sua resposta, errada';
      }
    });
    $('.explicacao', pergunta).hidden = false;
  });

  const aprovado = resultado.nota >= dados.meta;
  painelResultado.replaceChildren();
  const titulo = document.createElement('strong');
  titulo.textContent = `Você acertou ${resultado.acertos} de ${resultado.total} (${resultado.nota}%).`;
  const complemento = document.createElement('p');
  complemento.textContent = aprovado
    ? `A nota atingiu a meta de ${dados.meta}%. O critério 1 está cumprido.`
    : `A meta é ${dados.meta}%. Leia as explicações abaixo de cada pergunta e tente de novo.`;
  painelResultado.append(titulo, complemento);
  painelResultado.hidden = false;
  botaoCorrigir.hidden = true;
  botaoRefazer.hidden = false;
  painelResultado.focus();
}

function refazerQuiz() {
  formQuiz.reset();
  $$('.opcao', formQuiz).forEach((opcao) => {
    delete opcao.dataset.resultado;
    delete opcao.dataset.bloqueada;
    $('input', opcao).disabled = false;
    $('[data-campo="etiqueta"]', opcao).textContent = '';
  });
  $$('.explicacao', formQuiz).forEach((e) => { e.hidden = true; });
  painelResultado.hidden = true;
  botaoCorrigir.hidden = false;
  botaoRefazer.hidden = true;
  $('input', formQuiz)?.focus();
}

formQuiz?.addEventListener('submit', (evento) => {
  evento.preventDefault();
  const respostas = respostasEscolhidas();
  const primeiraEmBranco = respostas.indexOf(null);
  if (primeiraEmBranco !== -1) {
    mostrarMensagem('Responda todas as perguntas antes de corrigir.', 'aviso');
    $(`input[name="q${primeiraEmBranco}"]`, formQuiz).focus();
    return;
  }
  const resultado = corrigirQuiz(dados.quiz, respostas);
  mostrarCorrecao(resultado);
  mudarProgresso((p) => registrarQuiz(p, resultado, hojeISO()));
});

botaoRefazer?.addEventListener('click', refazerQuiz);

function desenharHistoricoQuiz(progresso) {
  const container = $('[data-campo="historico-quiz"]');
  if (!container) return;
  const recentes = progresso.tentativasQuiz.slice(-4);
  container.replaceChildren(
    ...recentes.map((t) => {
      const selo = document.createElement('span');
      selo.className = 'selo';
      selo.textContent = `${t.nota}% em ${formatarDiaMes(t.data)}`;
      if (t.nota >= dados.meta) selo.dataset.tom = 'ok';
      return selo;
    }),
  );
}

// ---------------------------------------------------------------------------
// Pergunta aberta
// ---------------------------------------------------------------------------

const areaAberta = $('#resposta-aberta');
const botaoEnviar = $('#enviar-aberta');
let temporizadorRascunho = null;

function guardarRascunho() {
  if (!areaAberta) return;
  window.clearTimeout(temporizadorRascunho);
  const texto = areaAberta.value;
  atualizarEstado((estado) => {
    if (normalizarProgresso(estado.topicos[dados.id]).aberta.rascunho === texto) return null;
    return comProgresso(estado, dados.id, (p) => salvarRascunho(p, texto));
  });
}

areaAberta?.addEventListener('input', () => {
  window.clearTimeout(temporizadorRascunho);
  temporizadorRascunho = window.setTimeout(guardarRascunho, 500);
});
areaAberta?.addEventListener('blur', guardarRascunho);

botaoEnviar?.addEventListener('click', () => {
  const texto = areaAberta.value.trim();
  if (texto.length < 10) {
    mostrarMensagem('Escreva ao menos uma frase antes de enviar.', 'aviso');
    areaAberta.focus();
    return;
  }
  window.clearTimeout(temporizadorRascunho);
  mudarProgresso((p) => enviarAberta(salvarRascunho(p, areaAberta.value), hojeISO()));
});

for (const caixa of $$('[data-rubrica]')) {
  caixa.addEventListener('change', () => {
    mudarProgresso((p) => marcarRubrica(p, Number(caixa.dataset.rubrica), caixa.checked));
  });
}

function desenharAberta(progresso) {
  if (!areaAberta) return;
  const { rascunho, enviadaEm, rubricaMarcada } = progresso.aberta;
  if (document.activeElement !== areaAberta && areaAberta.value !== rascunho) areaAberta.value = rascunho;

  const enviada = enviadaEm !== null;
  const estado = $('[data-campo="aberta-estado"]');
  estado.textContent = enviada ? `Enviada em ${formatarDiaMes(enviadaEm)}` : 'Não enviada';
  estado.dataset.tom = enviada ? 'ok' : '';
  const modelo = $('#modelo-aberta');
  if (modelo) modelo.hidden = !enviada;
  botaoEnviar.textContent = enviada ? 'Enviar de novo' : 'Enviar resposta';
  const dica = $('[data-campo="aberta-dica"]');
  if (dica) dica.hidden = enviada;

  for (const caixa of $$('[data-rubrica]')) {
    caixa.disabled = !enviada;
    caixa.checked = rubricaMarcada.includes(Number(caixa.dataset.rubrica));
  }
}

// ---------------------------------------------------------------------------
// Desafio e revisão
// ---------------------------------------------------------------------------

const formDesafio = $('#form-desafio');

formDesafio?.addEventListener('submit', (evento) => {
  evento.preventDefault();
  const campo = $('#testes-passando');
  if (campo.value.trim() === '') {
    mostrarMensagem('Informe quantos testes passaram na última rodada.', 'aviso');
    campo.focus();
    return;
  }
  const passando = Number(campo.value);
  let erro = null;
  const gravou = atualizarEstado((estado) => {
    const resultado = registrarDesafio(
      normalizarProgresso(estado.topicos[dados.id]),
      { passando, total: dados.desafioTotal },
      hojeISO(),
    );
    if (!resultado.ok) {
      erro = resultado.erro;
      return null;
    }
    return comProgresso(estado, dados.id, () => resultado.progresso);
  });
  if (!gravou) {
    mostrarMensagem(erro ?? 'Não foi possível registrar o resultado.', 'erro');
    campo.focus();
    return;
  }
  campo.value = '';
  mostrarMensagem('Resultado do desafio registrado.', 'ok');
});

function desenharDesafio(avaliacao) {
  const selo = $('[data-campo="desafio-estado"]');
  if (!selo) return;
  const c = avaliacao.criterios.desafio;
  const total = c.testesTotal || dados.desafioTotal;
  selo.textContent = c.cumprido ? 'Aprovado' : c.tentativas > 0 ? 'Em andamento' : 'Não iniciado';
  selo.dataset.tom = c.cumprido ? 'ok' : '';
  const detalhe = $('[data-campo="desafio-detalhe"]');
  detalhe.textContent = c.tentativas > 0
    ? `Última rodada: ${c.testesPassando} de ${total} testes. ${c.tentativas} ${plural(c.tentativas, 'rodada registrada', 'rodadas registradas')}.`
    : 'Nenhuma rodada registrada ainda.';
}

document.addEventListener('click', async (evento) => {
  const botao = evento.target.closest('[data-acao]');
  if (botao?.dataset.acao === 'revisao-ok' || botao?.dataset.acao === 'revisao-nao') {
    const deuCerto = botao.dataset.acao === 'revisao-ok';
    mudarProgresso((p) => registrarRevisao(p, deuCerto, hojeISO()));
    mostrarMensagem(
      deuCerto ? 'Revisão registrada como cumprida.' : 'Anotado. Revise o tópico e tente de novo mais tarde.',
      deuCerto ? 'ok' : 'aviso',
    );
  }

  const copiar = evento.target.closest('[data-copiar]');
  if (copiar) {
    try {
      await navigator.clipboard.writeText(copiar.dataset.copiar);
      const original = copiar.textContent;
      copiar.textContent = 'Copiado';
      window.setTimeout(() => { copiar.textContent = original; }, 2000);
    } catch {
      mostrarMensagem('Não foi possível copiar. Selecione o texto e copie manualmente.', 'aviso');
    }
  }
});

for (const caixa of $$('[data-aula]')) {
  caixa.addEventListener('change', () => {
    mudarProgresso((p) => alternarAula(p, caixa.dataset.aula, caixa.checked));
  });
}

// ---------------------------------------------------------------------------

function renderizar() {
  const estado = obterEstado();
  const hoje = hojeISO();
  const progresso = progressoAtual();
  const horas = horasPorTopico(estado.sessoes)[dados.id] ?? 0;
  const avaliacao = avaliarTopico(topicoParaAvaliar, progresso, { hoje, horasNoTopico: horas });

  desenharCabecalho(avaliacao);
  desenharCriterios(avaliacao, hoje);
  desenharAulas(progresso);
  desenharLateral(progresso, horas);
  desenharHistoricoQuiz(progresso);
  desenharAberta(progresso);
  desenharDesafio(avaliacao);
}

renderizar();
window.addEventListener('estudos:atualizado', renderizar);

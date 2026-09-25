// Preenche com o progresso tudo o que a página tiver de painel: números, barras, chips do
// mapa, gráfico de horas, revisões e sessões recentes. Cada parte é opcional: se a página
// não tem o elemento, a função simplesmente não faz nada. Por isso o mesmo script serve
// ao painel, às páginas de trilha e à página de revisões.

import { atualizarEstado, obterEstado } from './estado.js';
import { removerSessao } from '../dados/acoes.js';
import {
  arredondar, horasPorSemana, proximoMarco, resumirProgresso, revisoesPendentes, sequenciaDeSemanas,
} from '../dados/dominio.js';
import { formatarDiaMes, formatarPorExtenso, hojeISO } from '../dados/datas.js';
import { ROTULO_ESTADO } from '../dados/constantes.js';
import { formatarHoras, formatarNumero, plural } from './formato.js';
import { url } from './url.js';

const dados = JSON.parse(document.getElementById('dados-pagina').textContent);
const { trilha, meta, marcos } = dados;
const SEMANAS = 8;

function cadaElemento(atributo, funcao) {
  document.querySelectorAll(`[${atributo}]`).forEach((el) => funcao(el, el.getAttribute(atributo)));
}

function texto(seletor, valor) {
  const el = document.querySelector(seletor);
  if (el) el.textContent = valor;
}

function largura(seletor, fracao) {
  const el = document.querySelector(seletor);
  if (el) el.style.width = `${Math.round(Math.min(1, Math.max(0, fracao)) * 100)}%`;
}

function porcentagem(pontuacao) {
  return Math.round(pontuacao * 100);
}

function criar(tag, classe, conteudo) {
  const el = document.createElement(tag);
  if (classe) el.className = classe;
  if (conteudo !== undefined) el.textContent = conteudo;
  return el;
}

// ---------------------------------------------------------------------------
// Partes do painel
// ---------------------------------------------------------------------------

function desenharProgresso(resumo) {
  cadaElemento('data-chip', (el, id) => {
    const avaliacao = resumo.porTopico[id];
    if (!avaliacao) return;
    el.dataset.estado = avaliacao.estado;
    const rotulo = el.querySelector('[data-rotulo-estado]');
    if (rotulo) rotulo.textContent = `, ${ROTULO_ESTADO[avaliacao.estado]}`;
  });

  cadaElemento('data-modulo-contagem', (el, id) => {
    const modulo = resumo.porModulo[id];
    if (modulo) el.textContent = `${modulo.dominados} de ${modulo.total} dominados`;
  });
  cadaElemento('data-modulo-barra', (el, id) => {
    const modulo = resumo.porModulo[id];
    if (modulo) el.style.width = `${porcentagem(modulo.pontuacao)}%`;
  });
  cadaElemento('data-modulo-pct', (el, id) => {
    const modulo = resumo.porModulo[id];
    if (modulo) el.textContent = `${porcentagem(modulo.pontuacao)}%`;
  });
  cadaElemento('data-trilha-barra', (el, id) => {
    const t = resumo.porTrilha[id];
    if (t) el.style.width = `${porcentagem(t.pontuacao)}%`;
  });
  cadaElemento('data-trilha-pct', (el, id) => {
    const t = resumo.porTrilha[id];
    if (t) el.textContent = String(porcentagem(t.pontuacao));
  });
  cadaElemento('data-trilha-horas', (el, id) => {
    const t = resumo.porTrilha[id];
    if (t) el.textContent = `${formatarNumero(arredondar(t.horasEquivalentes, 1))} h de ${formatarNumero(t.horas)} h`;
  });

  const geral = resumo.geral;
  texto('[data-kpi="progresso-valor"]', String(porcentagem(geral.pontuacao)));
  largura('[data-kpi="progresso-barra"]', geral.pontuacao);
  texto(
    '[data-kpi="progresso-detalhe"]',
    `Equivale a ${formatarHoras(arredondar(geral.horasEquivalentes, 1))} de ${formatarHoras(geral.horas)} do plano`,
  );
}

function desenharSemanas(estado, hoje) {
  const semanas = horasPorSemana(estado.sessoes, hoje, SEMANAS);
  const atual = semanas[semanas.length - 1];

  texto('[data-kpi="horas-valor"]', formatarNumero(atual.horas));
  largura('[data-kpi="horas-barra"]', meta > 0 ? atual.horas / meta : 0);
  const faltam = arredondar(Math.max(0, meta - atual.horas));
  texto(
    '[data-kpi="horas-detalhe"]',
    faltam === 0 ? `Meta de ${formatarHoras(meta)} cumprida nesta semana` : `Faltam ${formatarHoras(faltam)} para a meta de ${formatarHoras(meta)}`,
  );

  const sequencia = sequenciaDeSemanas(semanas, meta);
  texto('[data-kpi="sequencia-valor"]', String(sequencia));
  texto('[data-kpi="sequencia-unidade"]', plural(sequencia, 'semana', 'semanas'));
  texto('[data-kpi="sequencia-detalhe"]', `Semanas seguidas com ${formatarHoras(meta)} ou mais`);
  const mini = document.querySelector('[data-kpi="sequencia-semanas"]');
  if (mini) {
    mini.replaceChildren(
      ...semanas.map((s) => {
        const bloco = criar('span');
        bloco.dataset.tipo = s.atual ? 'atual' : s.horas >= meta ? 'meta' : 'abaixo';
        return bloco;
      }),
    );
  }

  desenharGrafico(semanas);
}

function desenharGrafico(semanas) {
  const grafico = document.getElementById('grafico');
  if (!grafico) return;

  const maximo = Math.max(meta, ...semanas.map((s) => s.horas), 1);
  const escala = 150 / maximo;
  const colunas = semanas.map((s) => {
    const coluna = criar('div', 'coluna-semana');
    const barra = criar('div', 'barra-semana');
    barra.dataset.tipo = s.atual ? 'atual' : s.horas >= meta ? 'meta' : 'abaixo';
    barra.style.setProperty('--h', `${Math.round(s.horas * escala)}px`);
    coluna.append(barra);
    return coluna;
  });
  const linhaMeta = criar('div', 'linha-meta');
  const rotuloMeta = criar('span', 'rotulo-meta', `Meta ${formatarHoras(meta)}`);
  grafico.style.setProperty('--meta', `${Math.round(meta * escala)}px`);
  grafico.replaceChildren(...colunas, linhaMeta, rotuloMeta);

  const resumoAcessivel = semanas
    .map((s) => `semana de ${formatarDiaMes(s.inicio)}: ${formatarHoras(s.horas)}`)
    .join('; ');
  grafico.setAttribute('aria-label', `Horas por semana. ${resumoAcessivel}. Meta de ${formatarHoras(meta)}.`);

  const rotulos = document.getElementById('rotulos-semanas');
  if (rotulos) {
    rotulos.replaceChildren(
      ...semanas.map((s) => {
        const item = criar('div');
        item.append(criar('span', '', formatarDiaMes(s.inicio)), criar('strong', '', formatarHoras(s.horas)));
        return item;
      }),
    );
  }

  const total = arredondar(semanas.reduce((soma, s) => soma + s.horas, 0));
  texto('[data-campo="total-semanas"]', formatarHoras(total));
  const vazio = document.getElementById('grafico-vazio');
  if (vazio) vazio.hidden = total > 0;
}

function desenharMarco(hoje) {
  const marco = proximoMarco(marcos, hoje);
  if (!marco) {
    texto('[data-kpi="marco-valor"]', '-');
    texto('[data-kpi="marco-unidade"]', '');
    texto('[data-kpi="marco-detalhe"]', 'Nenhum marco cadastrado. Edite conteudo/trilhas.json.');
    return;
  }
  texto('[data-kpi="marco-valor"]', String(marco.dias));
  texto('[data-kpi="marco-unidade"]', plural(marco.dias, 'dia', 'dias'));
  texto('[data-kpi="marco-titulo"]', marco.titulo);
  texto('[data-kpi="marco-detalhe"]', marco.detalhe ? `${formatarDiaMes(marco.data)}. ${marco.detalhe}` : formatarDiaMes(marco.data));
}

function linhaRevisao(item, disponivel) {
  const li = criar('li');
  const bloco = criar('div');
  const link = criar('a', 'titulo-item', item.titulo);
  link.href = url(`topicos/${item.id}/`);
  bloco.append(link, criar('p', 'detalhe-item', `Liberada em ${formatarDiaMes(item.liberaEm)}`));
  const selo = criar('span', 'selo');
  if (disponivel) {
    selo.dataset.tom = item.atrasoDias > 0 ? 'atraso' : 'ok';
    selo.textContent = item.atrasoDias > 0
      ? `${item.atrasoDias} ${plural(item.atrasoDias, 'dia', 'dias')} de atraso`
      : 'Disponível hoje';
  } else {
    selo.dataset.tom = 'espera';
    selo.textContent = `Em ${item.diasParaLiberar} ${plural(item.diasParaLiberar, 'dia', 'dias')}`;
  }
  li.append(bloco, selo);
  return li;
}

function desenharRevisoes(resumo, hoje) {
  const container = document.getElementById('lista-revisoes');
  if (!container) return;
  const { disponiveis, proximas } = revisoesPendentes(trilha, resumo, hoje);
  texto('[data-campo="contagem-revisoes"]', String(disponiveis.length));
  const limite = Number(container.dataset.limite) || Infinity;
  const itens = [
    ...disponiveis.map((i) => linhaRevisao(i, true)),
    ...proximas.map((i) => linhaRevisao(i, false)),
  ].slice(0, limite);

  if (itens.length === 0) {
    container.replaceChildren(
      criar(
        'p',
        'vazio',
        'Nenhuma revisão pendente. Quando você cumprir o quiz e o desafio de um tópico, a revisão aparece aqui 7 dias depois.',
      ),
    );
    return;
  }
  const lista = criar('ul', 'lista');
  lista.append(...itens);
  container.replaceChildren(lista);
}

function desenharSessoes(estado) {
  const container = document.getElementById('lista-sessoes');
  if (!container) return;
  const recentes = [...estado.sessoes].reverse().slice(0, 5);
  if (recentes.length === 0) {
    container.replaceChildren(
      criar('p', 'vazio', 'Nenhuma sessão registrada ainda. Use o botão "Registrar horas" depois de estudar.'),
    );
    return;
  }
  const lista = criar('ul', 'lista');
  for (const sessao of recentes) {
    const topico = sessao.topico ? trilha.topicosPorId[sessao.topico] : null;
    const li = criar('li');
    const bloco = criar('div');
    const partes = [`${formatarDiaMes(sessao.data)}`, formatarHoras(sessao.horas)];
    if (sessao.nota) partes.push(sessao.nota);
    bloco.append(
      criar('p', 'titulo-item', topico ? topico.titulo : 'Sem tópico específico'),
      criar('p', 'detalhe-item', partes.join(', ')),
    );
    const remover = criar('button', 'botao-pequeno', 'Remover');
    remover.type = 'button';
    remover.dataset.removerSessao = sessao.id;
    remover.setAttribute('aria-label', `Remover a sessão de ${formatarDiaMes(sessao.data)}, ${formatarHoras(sessao.horas)}`);
    li.append(bloco, remover);
    lista.append(li);
  }
  container.replaceChildren(lista);
}

document.addEventListener('click', (evento) => {
  const botao = evento.target.closest('[data-remover-sessao]');
  if (!botao) return;
  if (!window.confirm('Remover esta sessão de estudo? As horas deixam de contar no painel.')) return;
  atualizarEstado((estado) => removerSessao(estado, botao.dataset.removerSessao));
});

// ---------------------------------------------------------------------------

function renderizar() {
  const estado = obterEstado();
  const hoje = hojeISO();
  const resumo = resumirProgresso(trilha, estado, hoje);
  texto('[data-campo="data-hoje"]', formatarPorExtenso(hoje));
  desenharProgresso(resumo);
  desenharSemanas(estado, hoje);
  desenharMarco(hoje);
  desenharRevisoes(resumo, hoje);
  desenharSessoes(estado);
}

renderizar();
window.addEventListener('estudos:atualizado', renderizar);

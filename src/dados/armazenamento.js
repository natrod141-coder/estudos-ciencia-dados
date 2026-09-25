// Guarda o progresso no navegador (localStorage) e permite exportar e importar um arquivo.
//
// O "storage" é sempre passado como parâmetro. No navegador é o `localStorage`;
// nos testes é um objeto de mentira com os mesmos métodos.

import {
  CHAVE_ESTADO, CHAVE_ESTADO_CORROMPIDO, CHAVE_ULTIMO_BACKUP, VERSAO_ESTADO,
} from './constantes.js';
import { dataValida } from './datas.js';
import { normalizarProgresso } from './dominio.js';

export function estadoInicial() {
  return { versao: VERSAO_ESTADO, topicos: {}, sessoes: [] };
}

export function sessaoValida(s) {
  return (
    s !== null && typeof s === 'object' &&
    typeof s.id === 'string' && s.id !== '' &&
    dataValida(s.data) &&
    Number.isFinite(s.horas) && s.horas > 0 && s.horas <= 24 &&
    (s.topico === null || typeof s.topico === 'string') &&
    typeof s.nota === 'string'
  );
}

/**
 * Valida um estado vindo de fora (navegador ou arquivo) e devolve uma cópia limpa.
 * Aceita perder partes inválidas, mas avisa quantas sessões foram descartadas.
 */
export function lerEstado(bruto) {
  if (bruto === null || typeof bruto !== 'object' || Array.isArray(bruto)) {
    return { ok: false, erro: 'O conteúdo não é um progresso válido.' };
  }
  if (!Number.isInteger(bruto.versao)) {
    return { ok: false, erro: 'O arquivo não tem a versão do progresso.' };
  }
  if (bruto.versao > VERSAO_ESTADO) {
    return { ok: false, erro: 'Este progresso foi salvo por uma versão mais nova do site.' };
  }
  if (bruto.topicos === null || typeof bruto.topicos !== 'object' || Array.isArray(bruto.topicos)) {
    return { ok: false, erro: 'O progresso não tem a lista de tópicos.' };
  }
  if (!Array.isArray(bruto.sessoes)) {
    return { ok: false, erro: 'O progresso não tem a lista de sessões de estudo.' };
  }

  const topicos = {};
  for (const [id, progresso] of Object.entries(bruto.topicos)) {
    topicos[id] = normalizarProgresso(progresso);
  }
  const sessoes = bruto.sessoes.filter(sessaoValida).map((s) => ({
    id: s.id, data: s.data, horas: s.horas, topico: s.topico, nota: s.nota,
  }));

  return {
    ok: true,
    estado: { versao: VERSAO_ESTADO, topicos, sessoes },
    descartadas: bruto.sessoes.length - sessoes.length,
  };
}

/** Lê o progresso salvo. Nunca lança erro: no pior caso começa do zero e avisa. */
export function carregarEstado(storage) {
  let texto;
  try {
    texto = storage.getItem(CHAVE_ESTADO);
  } catch {
    return {
      estado: estadoInicial(),
      aviso: 'Este navegador não permite guardar o progresso. Ele só valerá até fechar a página.',
    };
  }
  if (texto === null) return { estado: estadoInicial(), aviso: null };

  let bruto;
  try {
    bruto = JSON.parse(texto);
  } catch {
    return recuperar(storage, texto);
  }
  const lido = lerEstado(bruto);
  if (!lido.ok) return recuperar(storage, texto);

  const aviso = lido.descartadas > 0
    ? `${lido.descartadas} sessão(ões) de estudo com dados inválidos foram ignoradas.`
    : null;
  return { estado: lido.estado, aviso };
}

function recuperar(storage, texto) {
  try {
    storage.setItem(CHAVE_ESTADO_CORROMPIDO, texto);
  } catch {
    // sem espaço para a cópia: segue sem ela
  }
  return {
    estado: estadoInicial(),
    aviso:
      'O progresso salvo estava ilegível, então o painel começou do zero. ' +
      'Uma cópia do conteúdo antigo foi guardada no navegador.',
  };
}

/** Grava o progresso. Devolve { ok } ou { ok: false, erro }. */
export function salvarEstado(estado, storage) {
  try {
    storage.setItem(CHAVE_ESTADO, JSON.stringify(estado));
    return { ok: true };
  } catch {
    return {
      ok: false,
      erro: 'Não foi possível salvar. Exporte o progresso para não perder o que fez nesta sessão.',
    };
  }
}

/** Texto do arquivo de backup. */
export function exportarTexto(estado, agora = new Date()) {
  return JSON.stringify(
    { app: 'estudos', exportadoEm: agora.toISOString(), estado },
    null,
    2,
  );
}

/** Lê um arquivo de backup. Aceita o formato exportado ou o progresso puro. */
export function importarTexto(texto) {
  let bruto;
  try {
    bruto = JSON.parse(texto);
  } catch {
    return { ok: false, erro: 'O arquivo não é um JSON válido.' };
  }
  const candidato =
    bruto && typeof bruto === 'object' && bruto.app === 'estudos' ? bruto.estado : bruto;
  return lerEstado(candidato);
}

export function registrarBackup(storage, hoje) {
  try {
    storage.setItem(CHAVE_ULTIMO_BACKUP, hoje);
  } catch {
    // o backup em si já foi feito; só não lembramos a data
  }
}

export function ultimoBackup(storage) {
  try {
    const valor = storage.getItem(CHAVE_ULTIMO_BACKUP);
    return dataValida(valor) ? valor : null;
  } catch {
    return null;
  }
}

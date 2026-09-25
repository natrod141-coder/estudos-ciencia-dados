// Guarda o progresso em memória, grava no navegador a cada mudança e avisa a página
// (evento "estudos:atualizado") para redesenhar o que depende dele.

import { carregarEstado, salvarEstado } from '../dados/armazenamento.js';
import { CHAVE_ESTADO } from '../dados/constantes.js';

let storage = null;
let atual = null;
let avisoAtual = null;

function criarStorage() {
  try {
    const teste = '__estudos_teste__';
    window.localStorage.setItem(teste, '1');
    window.localStorage.removeItem(teste);
    return window.localStorage;
  } catch {
    // Navegação privada ou permissão negada: guarda só na memória desta página.
    const memoria = new Map();
    return {
      semPersistencia: true,
      getItem: (chave) => (memoria.has(chave) ? memoria.get(chave) : null),
      setItem: (chave, valor) => { memoria.set(chave, String(valor)); },
      removeItem: (chave) => { memoria.delete(chave); },
    };
  }
}

export function obterStorage() {
  if (!storage) storage = criarStorage();
  return storage;
}

function carregar() {
  const resultado = carregarEstado(obterStorage());
  atual = resultado.estado;
  avisoAtual = resultado.aviso;
  if (obterStorage().semPersistencia && !avisoAtual) {
    avisoAtual = 'Este navegador não permite guardar o progresso. Ele só vale até fechar a página.';
  }
}

export function obterEstado() {
  if (!atual) carregar();
  return atual;
}

/** Aviso sobre a leitura do progresso (dados corrompidos, storage bloqueado), ou null. */
export function obterAviso() {
  if (!atual) carregar();
  return avisoAtual;
}

function notificar() {
  window.dispatchEvent(new CustomEvent('estudos:atualizado'));
}

export function mostrarMensagem(texto, tipo = 'aviso') {
  window.dispatchEvent(new CustomEvent('estudos:mensagem', { detail: { texto, tipo } }));
}

/**
 * Aplica uma mudança ao progresso. `mudanca` recebe o estado atual e devolve o novo
 * (ou null para não mudar nada).
 */
export function atualizarEstado(mudanca) {
  const novo = mudanca(obterEstado());
  if (!novo) return false;
  atual = novo;
  const resultado = salvarEstado(atual, obterStorage());
  if (!resultado.ok) mostrarMensagem(resultado.erro, 'erro');
  notificar();
  return true;
}

/** Troca todo o progresso, por exemplo depois de importar um backup. */
export function substituirEstado(novo) {
  return atualizarEstado(() => novo);
}

// Se o progresso mudar em outra aba, recarrega e redesenha.
window.addEventListener('storage', (evento) => {
  if (evento.key === CHAVE_ESTADO || evento.key === null) {
    atual = null;
    notificar();
  }
});

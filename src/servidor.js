// Funções usadas só na hora de gerar as páginas (no build), nunca no navegador.

import { getCollection } from 'astro:content';
import config from '../conteudo/trilhas.json';
import { montarTrilha } from './dados/trilha.js';

let guardado;

/** Monta a trilha completa a partir de trilhas.json e dos arquivos de tópicos. */
export async function obterTrilha() {
  if (!guardado) {
    const entradas = await getCollection('topicos');
    guardado = montarTrilha(config, entradas);
  }
  return guardado;
}

export { config };

/** Prepara um objeto para ir dentro de <script type="application/json">. */
export function paraJson(objeto) {
  return JSON.stringify(objeto).replace(/</g, '\\u003c');
}

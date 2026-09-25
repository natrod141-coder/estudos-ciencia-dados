// Formatação de números para a tela, no padrão brasileiro.

const numero = new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 2 });

export function formatarNumero(valor) {
  return numero.format(valor);
}

export function formatarHoras(valor) {
  return `${numero.format(valor)} h`;
}

export function formatarPorcentagem(pontuacao) {
  return `${Math.round(pontuacao * 100)}%`;
}

export function plural(quantidade, singular, pluralTexto) {
  return quantidade === 1 ? singular : pluralTexto;
}

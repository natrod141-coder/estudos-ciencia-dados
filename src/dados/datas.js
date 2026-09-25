// Datas no formato "AAAA-MM-DD" (texto), sempre no fuso local de quem usa.
// Trabalhar com texto evita erros de fuso horário e de horário de verão.

const ISO = /^(\d{4})-(\d{2})-(\d{2})$/;
const DIA_MS = 86400000;

export function paraUTC(iso) {
  const partes = ISO.exec(iso);
  if (!partes) throw new Error(`Data inválida: "${iso}". Use o formato AAAA-MM-DD.`);
  const ms = Date.UTC(Number(partes[1]), Number(partes[2]) - 1, Number(partes[3]));
  if (deUTC(ms) !== iso) throw new Error(`Data inexistente: "${iso}".`);
  return ms;
}

export function deUTC(ms) {
  const d = new Date(ms);
  const mes = String(d.getUTCMonth() + 1).padStart(2, '0');
  const dia = String(d.getUTCDate()).padStart(2, '0');
  return `${d.getUTCFullYear()}-${mes}-${dia}`;
}

export function dataValida(iso) {
  if (typeof iso !== 'string') return false;
  try {
    paraUTC(iso);
    return true;
  } catch {
    return false;
  }
}

/** Data de hoje no fuso local, como "AAAA-MM-DD". */
export function hojeISO(agora = new Date()) {
  const mes = String(agora.getMonth() + 1).padStart(2, '0');
  const dia = String(agora.getDate()).padStart(2, '0');
  return `${agora.getFullYear()}-${mes}-${dia}`;
}

export function somarDias(iso, dias) {
  return deUTC(paraUTC(iso) + dias * DIA_MS);
}

/** Quantos dias de `a` até `b` (negativo se `b` vier antes). */
export function diasEntre(a, b) {
  return Math.round((paraUTC(b) - paraUTC(a)) / DIA_MS);
}

/** A semana começa na segunda-feira. */
export function segundaDaSemana(iso) {
  const diaDaSemana = new Date(paraUTC(iso)).getUTCDay(); // 0 = domingo
  return somarDias(iso, -((diaDaSemana + 6) % 7));
}

/** "2026-09-22" vira "22/9". */
export function formatarDiaMes(iso) {
  const partes = ISO.exec(iso);
  if (!partes) return iso;
  return `${Number(partes[3])}/${Number(partes[2])}`;
}

const DIAS_SEMANA = ['domingo', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado'];
const MESES = [
  'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
  'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro',
];

/** "2026-09-24" vira "Quinta, 24 de setembro de 2026". */
export function formatarPorExtenso(iso) {
  const d = new Date(paraUTC(iso));
  const dia = DIAS_SEMANA[d.getUTCDay()];
  return `${dia[0].toUpperCase()}${dia.slice(1)}, ${d.getUTCDate()} de ${MESES[d.getUTCMonth()]} de ${d.getUTCFullYear()}`;
}

export function maiorData(datas) {
  return datas.reduce((maior, atual) => (atual > maior ? atual : maior));
}

// Junta conteudo/trilhas.json (trilhas e módulos) com os arquivos de conteudo/topicos/
// e monta a estrutura que o painel usa. Se algo estiver inconsistente, para o build
// com uma mensagem que diz o que corrigir.

function erro(mensagem) {
  return new Error(`[conteudo] ${mensagem}`);
}

/**
 * @param config  o conteúdo de conteudo/trilhas.json
 * @param entradas lista de tópicos: cada um com `id` e `data` (o cabeçalho do arquivo .md)
 */
export function montarTrilha(config, entradas) {
  if (!Array.isArray(config.trilhas) || !Array.isArray(config.modulos)) {
    throw erro('trilhas.json precisa ter as listas "trilhas" e "modulos".');
  }

  const idsTrilhas = new Set();
  for (const t of config.trilhas) {
    if (idsTrilhas.has(t.id)) throw erro(`A trilha "${t.id}" aparece duas vezes em trilhas.json.`);
    idsTrilhas.add(t.id);
  }

  const modulos = {};
  for (const m of config.modulos) {
    if (modulos[m.id]) throw erro(`O módulo "${m.id}" aparece duas vezes em trilhas.json.`);
    if (!idsTrilhas.has(m.trilha)) {
      throw erro(`O módulo "${m.id}" aponta para a trilha "${m.trilha}", que não existe.`);
    }
    modulos[m.id] = { id: m.id, nome: m.nome, fase: m.fase, trilha: m.trilha, horas: 0, topicos: [] };
  }

  const topicosPorId = {};
  for (const entrada of entradas) {
    const d = entrada.data;
    const modulo = modulos[d.modulo];
    if (!modulo) {
      throw erro(`O tópico "${entrada.id}" usa o módulo "${d.modulo}", que não existe em trilhas.json.`);
    }
    if (topicosPorId[entrada.id]) throw erro(`O tópico "${entrada.id}" está duplicado.`);

    const ids = (d.aulas ?? []).map((a) => a.id);
    if (new Set(ids).size !== ids.length) {
      throw erro(`O tópico "${entrada.id}" tem duas aulas com o mesmo id.`);
    }

    const topico = {
      id: entrada.id,
      titulo: d.titulo,
      ordem: d.ordem,
      horas: d.horas,
      modulo: modulo.id,
      moduloNome: modulo.nome,
      trilha: modulo.trilha,
      rascunho: d.estado === 'rascunho',
      temQuiz: (d.quiz ?? []).length > 0,
      temDesafio: Boolean(d.desafio),
      aulas: ids,
    };
    modulo.topicos.push(topico);
    topicosPorId[entrada.id] = topico;
  }

  for (const modulo of Object.values(modulos)) {
    modulo.topicos.sort((a, b) => a.ordem - b.ordem || (a.id < b.id ? -1 : 1));
    modulo.horas = modulo.topicos.reduce((soma, t) => soma + t.horas, 0);
  }

  const trilhas = config.trilhas.map((t) => {
    const daTrilha = config.modulos.map((m) => modulos[m.id]).filter((m) => m.trilha === t.id);
    return {
      id: t.id,
      nome: t.nome,
      horas: daTrilha.reduce((soma, m) => soma + m.horas, 0),
      modulos: daTrilha,
    };
  });

  return { trilhas, modulosPorId: modulos, topicosPorId };
}

/** Tópico anterior e seguinte dentro do mesmo módulo. */
export function vizinhosDoTopico(trilha, id) {
  const topico = trilha.topicosPorId[id];
  if (!topico) return { anterior: null, proximo: null };
  const lista = trilha.modulosPorId[topico.modulo].topicos;
  const i = lista.findIndex((t) => t.id === id);
  return { anterior: lista[i - 1] ?? null, proximo: lista[i + 1] ?? null };
}

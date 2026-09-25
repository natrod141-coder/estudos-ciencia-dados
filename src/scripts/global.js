// Comportamento presente em todas as páginas:
// caixa "Registrar horas", exportar e importar progresso e faixa de mensagens.

import {
  atualizarEstado, obterAviso, obterEstado, obterStorage, substituirEstado, mostrarMensagem,
} from './estado.js';
import { registrarSessao } from '../dados/acoes.js';
import {
  exportarTexto, importarTexto, registrarBackup, ultimoBackup,
} from '../dados/armazenamento.js';
import { diasEntre, formatarDiaMes, hojeISO } from '../dados/datas.js';

const DIAS_PARA_LEMBRAR_BACKUP = 14;

// ---------------------------------------------------------------------------
// Faixa de mensagens
// ---------------------------------------------------------------------------

const faixa = document.getElementById('faixa-mensagem');
const textoFaixa = document.getElementById('texto-mensagem');

function exibirMensagem(texto, tipo) {
  if (!faixa || !textoFaixa) return;
  textoFaixa.textContent = texto;
  faixa.dataset.tipo = tipo;
  faixa.hidden = false;
}

window.addEventListener('estudos:mensagem', (evento) => {
  exibirMensagem(evento.detail.texto, evento.detail.tipo);
});

document.getElementById('fechar-mensagem')?.addEventListener('click', () => {
  if (faixa) faixa.hidden = true;
});

const avisoInicial = obterAviso();
if (avisoInicial) mostrarMensagem(avisoInicial, 'aviso');

// ---------------------------------------------------------------------------
// Registrar horas
// ---------------------------------------------------------------------------

const dialogo = document.getElementById('dialogo-horas');
const formulario = document.getElementById('form-horas');
const erroHoras = document.getElementById('erro-horas');

function mostrarErroHoras(texto) {
  if (!erroHoras) return;
  erroHoras.textContent = texto;
  erroHoras.hidden = texto === '';
}

function abrirDialogo(topicoId) {
  if (!dialogo || !formulario) return;
  formulario.reset();
  mostrarErroHoras('');
  const hoje = hojeISO();
  formulario.elements.data.value = hoje;
  formulario.elements.data.max = hoje;
  formulario.elements.topico.value = topicoId ?? '';
  if (typeof dialogo.showModal === 'function') dialogo.showModal();
  else dialogo.setAttribute('open', '');
  formulario.elements.horas.focus();
}

document.addEventListener('click', (evento) => {
  const gatilho = evento.target.closest('[data-abrir-horas]');
  if (gatilho) abrirDialogo(gatilho.dataset.topico ?? '');
  if (evento.target.closest('[data-fechar-horas]')) dialogo?.close();
});

formulario?.addEventListener('submit', (evento) => {
  evento.preventDefault();
  const dados = new FormData(formulario);
  const entrada = {
    data: String(dados.get('data')),
    horas: String(dados.get('horas')).replace(',', '.'),
    topico: String(dados.get('topico') ?? ''),
    nota: String(dados.get('nota') ?? ''),
  };
  let erro = null;
  const gravou = atualizarEstado((estado) => {
    const resultado = registrarSessao(estado, entrada, { hoje: hojeISO() });
    if (!resultado.ok) {
      erro = resultado.erro;
      return null;
    }
    return resultado.estado;
  });
  if (!gravou) {
    mostrarErroHoras(erro ?? 'Não foi possível registrar as horas.');
    return;
  }
  dialogo.close();
  mostrarMensagem('Horas registradas.', 'ok');
});

// ---------------------------------------------------------------------------
// Backup
// ---------------------------------------------------------------------------

const statusBackup = document.getElementById('backup-status');
const botaoExportar = document.getElementById('btn-exportar');
const botaoImportar = document.getElementById('btn-importar');
const arquivoImportar = document.getElementById('arq-importar');

function atualizarStatusBackup() {
  if (!statusBackup) return;
  const hoje = hojeISO();
  const ultimo = ultimoBackup(obterStorage());
  if (!ultimo) {
    statusBackup.textContent = 'Você ainda não fez backup do progresso.';
    statusBackup.dataset.alerta = 'true';
    return;
  }
  const dias = diasEntre(ultimo, hoje);
  statusBackup.textContent = dias === 0
    ? 'Último backup: hoje.'
    : `Último backup: ${formatarDiaMes(ultimo)}, há ${dias} dia${dias === 1 ? '' : 's'}.`;
  statusBackup.dataset.alerta = dias > DIAS_PARA_LEMBRAR_BACKUP ? 'true' : 'false';
}

botaoExportar?.addEventListener('click', () => {
  const texto = exportarTexto(obterEstado());
  const arquivo = new Blob([texto], { type: 'application/json' });
  const ancora = document.createElement('a');
  ancora.href = URL.createObjectURL(arquivo);
  ancora.download = `estudos_progresso_${hojeISO()}.json`;
  document.body.append(ancora);
  ancora.click();
  ancora.remove();
  URL.revokeObjectURL(ancora.href);
  registrarBackup(obterStorage(), hojeISO());
  atualizarStatusBackup();
  mostrarMensagem('Backup exportado. Guarde o arquivo em um lugar seguro.', 'ok');
});

botaoImportar?.addEventListener('click', () => arquivoImportar?.click());

arquivoImportar?.addEventListener('change', async () => {
  const arquivo = arquivoImportar.files?.[0];
  arquivoImportar.value = '';
  if (!arquivo) return;
  const resultado = importarTexto(await arquivo.text());
  if (!resultado.ok) {
    mostrarMensagem(`Não foi possível importar: ${resultado.erro}`, 'erro');
    return;
  }
  const confirmou = window.confirm(
    'Importar substitui o progresso atual deste navegador pelo conteúdo do arquivo. Continuar?',
  );
  if (!confirmou) return;
  substituirEstado(resultado.estado);
  mostrarMensagem('Progresso importado.', 'ok');
});

atualizarStatusBackup();

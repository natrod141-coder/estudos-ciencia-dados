// Valores fixos que definem as regras do painel.
// Se quiser mudar uma regra (por exemplo, a nota mínima do quiz), é aqui.

export const ESTADOS = ['nao_iniciado', 'estudando', 'praticando', 'dominado'];

export const ROTULO_ESTADO = {
  nao_iniciado: 'Não iniciado',
  estudando: 'Estudando',
  praticando: 'Praticando',
  dominado: 'Dominado',
};

// Quanto cada estado conta no cálculo do progresso de um módulo.
export const PESO_ESTADO = {
  nao_iniciado: 0,
  estudando: 0.25,
  praticando: 0.6,
  dominado: 1,
};

// Critérios para um tópico virar "dominado".
export const META_QUIZ = 80; // nota mínima do quiz, em porcentagem
export const DIAS_ATE_REVISAO = 7; // a revisão libera 7 dias depois dos critérios 1 e 2

// Onde o progresso fica guardado no navegador.
export const CHAVE_ESTADO = 'estudos:progresso';
export const CHAVE_ESTADO_CORROMPIDO = 'estudos:progresso:corrompido';
export const CHAVE_ULTIMO_BACKUP = 'estudos:ultimo_backup';
export const VERSAO_ESTADO = 1;

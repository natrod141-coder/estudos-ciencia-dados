// Define o formato dos arquivos em conteudo/topicos/. Se algum arquivo estiver fora do
// formato, o build para e diz qual arquivo e qual campo estão errados.

import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const aula = z.object({
  id: z.string().regex(/^[a-z0-9_]+$/, 'Use só letras minúsculas, números e "_".'),
  titulo: z.string(),
  tipo: z.enum(['leitura', 'video']),
  minutos: z.number().int().positive(),
  link: z.string().default(''),
});

const pergunta = z
  .object({
    pergunta: z.string(),
    opcoes: z.array(z.string()).min(2).max(6),
    correta: z.number().int().min(0),
    explicacao: z.string(),
  })
  .refine((q) => q.correta < q.opcoes.length, {
    message: 'O campo "correta" aponta para uma opção que não existe.',
  });

const aberta = z.object({
  pergunta: z.string(),
  rubrica: z.array(z.string()).min(1),
  modelo: z.string(),
});

const passo = z.object({
  titulo: z.string(),
  descricao: z.string(),
  comandos: z.array(z.string()).default([]),
  codigo: z.boolean().default(false), // true: as linhas são código, e não comandos de terminal
});

const desafio = z.object({
  titulo: z.string(),
  descricao: z.string(),
  pasta: z.string(),
  testes: z.number().int().positive(),
  tempo: z.string(),
  ferramentas: z.string(),
  entrega: z.string(),
  passos: z.array(passo).min(1),
});

const topicos = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './conteudo/topicos' }),
  schema: z.object({
    titulo: z.string(),
    modulo: z.string(),
    ordem: z.number().int().positive(),
    horas: z.number().positive(),
    estado: z.enum(['rascunho', 'publicado']).default('rascunho'),
    resumo: z.string().default(''),
    aulas: z.array(aula).default([]),
    quiz: z.array(pergunta).default([]),
    aberta: aberta.optional(),
    desafio: desafio.optional(),
    glossario: z.array(z.object({ pt: z.string(), en: z.string() })).default([]),
  }),
});

export const collections = { topicos };

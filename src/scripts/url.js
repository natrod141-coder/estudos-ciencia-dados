// Monta endereços respeitando o "base" do astro.config.mjs (útil no GitHub Pages).

export function url(caminho = '') {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  return `${base}/${String(caminho).replace(/^\//, '')}`;
}

import { defineConfig } from 'astro/config';

// O site publicado fica em https://natrod141-coder.github.io/estudos-ciencia-dados/.
// O workflow .github/workflows/publicar.yml define PUBLICAR_NO_PAGES=1 para gerar os links
// com esse caminho. No seu computador, sem a variável, o site continua em http://localhost:4321/.
const noPages = process.env.PUBLICAR_NO_PAGES === '1';

export default defineConfig({
  site: 'https://natrod141-coder.github.io',
  base: noPages ? '/estudos-ciencia-dados' : '/',
});

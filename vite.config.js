import { defineConfig } from 'vite';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const root = import.meta.dirname;
const pages = ['index', 'services/index', 'work/index', 'about/index', 'privacy/index', 'terms/index'];

// Injects shared partials so every page has the same header and footer in its HTML.
// Use <!-- @header --> and <!-- @footer --> in a page.
function partials() {
  return {
    name: 'partials',
    transformIndexHtml: {
      order: 'pre',
      handler(html) {
        return html.replace(/<!--\s*@(\w+)\s*-->/g, (_, name) =>
          readFileSync(resolve(root, 'partials', `${name}.html`), 'utf8'),
        );
      },
    },
  };
}

export default defineConfig({
  plugins: [partials()],
  server: { watch: { ignored: ['!**/partials/**'] } },
  build: {
    rollupOptions: {
      input: Object.fromEntries(pages.map(p => [p, resolve(root, `${p}.html`)])),
    },
  },
});

import { defineConfig } from 'vite';
import volto from '@plone/volto/node_modules/@plone/volto/vite-plugin';

export default defineConfig({
  plugins: [volto()],
});

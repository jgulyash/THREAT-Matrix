import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: './',
  build: {
    outDir: 'docs',
    emptyOutDir: false,
    assetsDir: 'assets',
    sourcemap: false,
    // Keep font files as files; nothing is inlined as a data URI.
    assetsInlineLimit: 0,
    rollupOptions: {
      output: {
        // Every emitted file starts with "index-", so the documented rebuild
        // (rm -f docs/assets/index-* && bun run build) clears all of them and
        // stale chunks or fonts cannot accumulate.
        entryFileNames: 'assets/index-[hash].js',
        chunkFileNames: 'assets/index-[name]-[hash].js',
        assetFileNames: (info) =>
          info.names?.some((n) => n.endsWith('.css'))
            ? 'assets/index-[hash][extname]'
            : 'assets/index-[name]-[hash][extname]',
      },
    },
  },
  server: {
    port: 5173,
    strictPort: true,
    open: false,
  },
});

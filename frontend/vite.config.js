import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Fully static build: the curriculum ships as JSON in the bundle and grading
// runs in the browser, so there is no API to proxy and no server to deploy.
//
// Dev server binds 0.0.0.0 so the host's preview proxy can reach it.
export default defineConfig({
  plugins: [react()],
  base: '/',
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    allowedHosts: true,
    hmr: { protocol: 'wss', clientPort: 443 },
  },
  preview: {
    host: '0.0.0.0',
    port: 4173,
    strictPort: true,
    allowedHosts: true,
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    sourcemap: false,
    chunkSizeWarningLimit: 1200,
  },
})

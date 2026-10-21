import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Dev server is bound to 0.0.0.0 so the Arena live preview proxy can reach it.
// /api is proxied to the FastAPI backend on port 8000 (same origin for the browser).
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    allowedHosts: true,
    hmr: { protocol: 'wss', clientPort: 443 },
    proxy: {
      '/api': { target: 'http://127.0.0.1:8000', changeOrigin: true },
    },
  },
  build: {
    outDir: '../backend/static_app',
    emptyOutDir: true,
  },
})

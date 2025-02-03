import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  css: {
    modules: {
      localsConvention: 'camelCase'
    }
  },
  server: {
    host: true,
    port: 3000,
    strictPort: true,
    cors: true,
    allowedHosts: ['all'],
    proxy: {
      '/agents': {
        target: process.env.VITE_API_URL || 'https://localhost:8000',
        changeOrigin: true,
        secure: true,
        rewrite: (path) => path.replace(/^\/agents/, '/agents'),
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq, req) => {
            proxyReq.setHeader('x-api-key', process.env.VITE_BING_API_KEY || '');
            proxyReq.setHeader('x-api-version', process.env.VITE_API_VERSION || 'v1');
            proxyReq.setHeader('x-azure-endpoint', process.env.VITE_AZURE_ENDPOINT || '');
            proxyReq.setHeader('x-azure-model', process.env.VITE_AZURE_MODEL || '');
            proxyReq.setHeader('Accept', 'application/json');
            proxyReq.setHeader('Content-Type', 'application/json');
            proxyReq.setHeader('Origin', req.headers.origin || 'http://localhost:3000');
          });
          proxy.on('error', (err) => {
            console.error('proxy error', err);
          });
        }
      }
    }
  },
  preview: {
    host: true,
    port: 5173,
    strictPort: true,
    allowedHosts: ['all']
  },
  base: '/',
  build: {
    cssMinify: true,
    rollupOptions: {
      output: {
        manualChunks: undefined
      }
    },
    sourcemap: true,
    chunkSizeWarningLimit: 1000
  }
})

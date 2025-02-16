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
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, ''),
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq, req) => {
            proxyReq.setHeader('x-api-version', process.env.VITE_API_VERSION || 'v1');
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

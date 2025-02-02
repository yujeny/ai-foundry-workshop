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
    postcss: true,
  },
  build: {
    cssMinify: true,
  },
  server: {
    host: true,
    port: 5173,
    strictPort: true,
    allowedHosts: ['.devinapps.com']
  },
  preview: {
    host: true,
    port: 5173,
    strictPort: true,
    allowedHosts: ['.devinapps.com']
  }
})

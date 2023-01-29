// Plugins
import { fileURLToPath, URL } from 'node:url'

// Utilities
import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'
import { chunkSplitPlugin } from 'vite-plugin-chunk-split'
import eslint from 'vite-plugin-eslint'
import vuetify from 'vite-plugin-vuetify'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    chunkSplitPlugin({
      strategy: 'all-in-one',
      customSplitting: {
        '@vendor/vue': ['vue', 'vue-router', 'vue3-treeview', 'vee-validate', '@vue/test-utils', '@vue/tsconfig'],
        '@vendor/vuetify': ['vuetify'],
        '@vendor/eslint': [
          'eslint',
          'eslint-plugin-vue',
          'eslint-plugin-import',
          'eslint-plugin-promise',
          'eslint-plugin-n',
          'eslint-config-standard',
          '@rushstack/eslint-patch',
          '@vue/eslint-config-typescript'
        ],
        '@vendor/typescript': [
          '@typescript-eslint/eslint-plugin',
          '@typescript-eslint/parser',
          'vue-tsc',
          'typescript'
        ],
        '@vendor/vite': [
          'vite',
          'vite-plugin-chunk-split',
          'vite-plugin-eslint',
          'vite-plugin-vuetify',
          '@vitejs/plugin-vue',
          'vitest'
        ],
        '@vendor/revogrid': ['@revolist/revogrid', '@revolist/vue3-datagrid'],
        '@vendor/axios': ['axios'],
        '@vendor/pinia': ['pinia'],
        '@vendor/sweealert2': ['sweetalert2', 'vue-sweetalert2', '@sweetalert2/theme-dark'],
        '@vendor/prettier': ['prettier', 'eslint-plugin-prettier', '@vue/eslint-config-prettier']
      }
    }),
    vue(),
    vuetify({ autoImport: true }),
    eslint({
      include: ['src/**/*.ts', 'src/**/*.vue', 'src/*.ts', 'src/*.vue']
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 80,
    proxy: {
      '^/api/.*': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, ''),
        configure: (proxy, _options) => {
          proxy.on('error', (err, _req, _res) => {
            console.info('proxy error', err)
          })
          proxy.on('proxyReq', (proxyReq, req, _res) => {
            console.info('Sending Request to the Target:', req.method, req.url)
          })
          proxy.on('proxyRes', (proxyRes, req, _res) => {
            console.info('Received Response from the Target:', proxyRes.statusCode, req.url)
          })
        }
      }
    }
  }
})

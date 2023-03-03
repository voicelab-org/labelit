import { defineConfig } from 'vite';
import { fileURLToPath, URL } from 'url';
import vue from '@vitejs/plugin-vue2';
import VitePluginHtmlEnv from 'vite-plugin-html-env';
import VueI18nPlugin from '@intlify/unplugin-vue-i18n/vite';
import * as path from 'path';
// import eslintPlugin from 'vite-plugin-eslint';

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    port: 8080,
    proxy: {
      '^/api': {
        target: 'http://127.0.0.1:8000/',
        //target: 'https://labelit.staging.hosting.call.watch/',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  plugins: [
    vue(),
    VueI18nPlugin({
      include: path.resolve(
        path.dirname(fileURLToPath(import.meta.url)),
        './src/plugins/locales/**'
      ),
    }),
    VitePluginHtmlEnv({
      compiler: true,
    }),
    // eslintPlugin({
    //   lintOnStart: false,
    //   failOnError: false,
    //   failOnWarning: false,
    // }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
});

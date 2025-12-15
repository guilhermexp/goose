import { defineConfig } from 'vite';

// https://vitejs.dev/config
export default defineConfig({
  build: {
    rollupOptions: {
      external: [
        '@johnlindquist/node-window-manager',
      ],
    },
  },
});

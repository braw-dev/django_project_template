import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
export default defineConfig({
  base: "/static/",
  build: {
    manifest: "manifest.json",
    outDir: "dist",
    rollupOptions: {
      input: {
        tailwind: "src/tailwind.css",
      }
    }
  },
  plugins: [react()],
})

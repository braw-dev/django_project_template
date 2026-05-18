import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  base: "/static/",
  build: {
    manifest: "manifest.json",
    outDir: "dist",
    rollupOptions: {
      input: {
        tailwind: "src/tailwind.css",
        main: "src/main.tsx",
      }
    }
  },
  plugins: [react(), tailwindcss()],
})

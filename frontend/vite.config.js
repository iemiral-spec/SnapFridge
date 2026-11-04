import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Geliştirmede /api istekleri FastAPI'ye (8000) yönlenir.
export default defineConfig({
  plugins: [react()],
  server: { proxy: { "/api": "http://localhost:8000" } },
});

import tailwindcss from "@tailwindcss/vite";
export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  css: ['./app/assets/css/main.css'],
  modules: ['@nuxt/image', '@nuxt/fonts', '@nuxt/eslint', '@pinia/nuxt', 'pinia-plugin-persistedstate/nuxt'],

  // Runtime configuration for environment variables
  runtimeConfig: {
    // Private keys (server-side only) - not used in this app
    // apiSecret: '',

    // Public keys (client-side accessible)
    public: {
      apiUrl: process.env.NUXT_PUBLIC_API_URL || 'http://localhost:8000',
      googleClientId: process.env.NUXT_PUBLIC_GOOGLE_CLIENT_ID || '',
      env: process.env.NUXT_PUBLIC_ENV || 'development',
    }
  },

  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
});
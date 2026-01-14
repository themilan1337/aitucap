/**
 * Google OAuth Plugin
 * Initializes Google OAuth library globally
 * Only runs on client-side (.client.ts suffix)
 */

import { googleSdkLoaded } from 'vue3-google-login'

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()

  // Wait for Google SDK to load
  googleSdkLoaded((google) => {
    // Initialize Google OAuth
    google.accounts.id.initialize({
      client_id: config.public.googleClientId as string,
      callback: () => {
        // Callback handled in individual components
        // This is just for global initialization
      },
    })
  })
})

/**
 * Google OAuth Plugin
 * Initializes Google OAuth library globally
 * Only runs on client-side (.client.ts suffix)
 */

import { googleSdkLoaded } from 'vue3-google-login'

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const clientId = config.public.googleClientId as string

  // Only initialize if client_id is provided
  if (!clientId || clientId.trim() === '') {
    console.warn('Google OAuth client ID not configured. Please set NUXT_PUBLIC_GOOGLE_CLIENT_ID in your .env file.')
    return
  }

  // Wait for Google SDK to load
  googleSdkLoaded((google) => {
    // Initialize Google OAuth
    google.accounts.id.initialize({
      client_id: clientId,
      callback: () => {
        // Callback handled in individual components
        // This is just for global initialization
      },
    })
  })
})

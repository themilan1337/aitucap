<script setup lang="ts">
import { Icon } from '@iconify/vue'
import PrimaryButton from '~/components/ui/PrimaryButton.vue'
import { googleSdkLoaded } from 'vue3-google-login'

definePageMeta({
  layout: 'auth'
})

const config = useRuntimeConfig()
const authStore = useAuthStore()
const router = useRouter()

const isLoading = ref(false)
const errorMessage = ref<string | null>(null)
const rememberMe = ref(true) // Always remember user for 30 days

/**
 * Handle Google OAuth login
 * Uses Google OAuth2 popup flow to get authorization code
 * Exchanges it for ID token and sends to backend
 */
const handleGoogleLogin = () => {
  isLoading.value = true
  errorMessage.value = null

  const clientId = config.public.googleClientId as string

  // Check if client ID is configured
  if (!clientId || clientId.trim() === '') {
    errorMessage.value = 'Google OAuth is not configured. Please set NUXT_PUBLIC_GOOGLE_CLIENT_ID in your .env file.'
    isLoading.value = false
    return
  }

  // Use Google OAuth2 with popup
  googleSdkLoaded((google) => {
    const client = google.accounts.oauth2.initTokenClient({
      client_id: clientId,
      scope: 'openid email profile',
      callback: handleOAuthResponse,
    })

    // Request access token (which includes ID token in response)
    client.requestAccessToken()
  })
}

/**
 * Handle OAuth response
 * Extract ID token and login to backend
 */
const handleOAuthResponse = async (response: any) => {
  try {
    if (response.error) {
      throw new Error(response.error)
    }

    // For OAuth2, we need to get the ID token separately
    // The access_token can be used to fetch user info from Google
    // But our backend expects ID token, so we'll use the access token
    // to make a request to Google's tokeninfo endpoint to get the ID token

    // Alternative: Use the access_token to get user info and create our own session
    // Let's try sending the access_token to our backend and let it handle verification
    const accessToken = response.access_token

    if (!accessToken) {
      throw new Error('Failed to get access token from Google')
    }

    // Login with backend using access token
    // Backend will need to be updated to accept access token and fetch user info
    const success = await authStore.loginWithGoogle(
      accessToken,
      rememberMe.value
    )

    if (!success) {
      throw new Error(authStore.error || 'Login failed')
    }

    // Check if user has completed onboarding
    if (!authStore.hasCompletedProfile) {
      await router.push('/onboarding/')
    } else {
      await router.push('/home')
    }
  } catch (error: any) {
    console.error('Google login error:', error)
    errorMessage.value = error.message || 'Failed to login with Google. Please try again.'
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex flex-col items-center justify-center px-6 py-8">
    <!-- Login Card -->
    <div class="w-full max-w-md">
        <h2 class="text-2xl font-bold mb-2 mt-8 text-center">Войти в аккаунт</h2>
        <p class="text-gray-400 text-sm mb-8 text-center">
          Войдите, чтобы начать тренировки
        </p>

        <!-- Error Message -->
        <div v-if="errorMessage" class="px-6 mb-4">
          <div class="bg-red-500/10 border border-red-500/50 rounded-lg p-3 text-red-500 text-sm">
            {{ errorMessage }}
          </div>
        </div>

        <!-- Google Login Button -->
        <div class="px-6">
          <PrimaryButton
            @click="handleGoogleLogin"
            :disabled="isLoading"
            class="py-6 mb-6"
          >
          <svg v-if="!isLoading" class="w-6 h-6" viewBox="0 0 24 24">
            <path
              fill="#4285F4"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            />
            <path
              fill="#34A853"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path
              fill="#FBBC05"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
            />
            <path
              fill="#EA4335"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
            />
          </svg>
          <svg v-else class="animate-spin h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{{ isLoading ? 'Вход...' : 'Продолжить с Google' }}</span>
          </PrimaryButton>
        </div>

      <p class="text-center text-xs text-gray-500 mt-8 px-4">
        Продолжая, вы соглашаетесь с
        <a href="#" class="text-neon hover:underline">Условиями использования</a>
        и
        <a href="#" class="text-neon hover:underline">Политикой конфиденциальности</a>
      </p>
    </div>
  </div>
</template>

<style scoped>
.bg-neon {
  background-color: var(--color-neon);
}
.text-neon {
  color: var(--color-neon);
}
</style>
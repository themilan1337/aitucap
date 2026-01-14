/**
 * App Initialization Plugin
 * Runs on client-side app startup
 *
 * Responsibilities:
 * 1. Attempt to restore user session from cookies
 * 2. Fetch current user if access_token cookie exists
 * 3. Silent token refresh if needed
 *
 * This ensures users stay logged in across page refreshes
 */

export default defineNuxtPlugin(async () => {
  const authStore = useAuthStore()

  // Only attempt session restore if we think we're authenticated
  // (based on persisted state from previous session)
  if (authStore.isAuthenticated) {
    try {
      // Try to fetch current user
      // If access_token is valid, this will succeed
      // If expired, will attempt token refresh
      await authStore.fetchCurrentUser()
    } catch (error) {
      console.error('Session restore failed:', error)
      // Session expired or invalid, user will be redirected to login by middleware
    }
  }
})

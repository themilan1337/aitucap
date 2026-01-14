/**
 * Authentication Middleware
 * Protects routes and enforces authentication
 *
 * Flow:
 * 1. Check if route requires authentication
 * 2. If yes, check if user is authenticated
 * 3. If not authenticated, redirect to login
 * 4. If authenticated, allow access
 *
 * Public routes (no auth required):
 * - /login
 */

export default defineNuxtRouteMiddleware(async (to) => {
  const authStore = useAuthStore()

  // Define public routes that don't require authentication
  const publicRoutes = ['/login']

  // Check if the route is public
  const isPublicRoute = publicRoutes.some(route => to.path === route)

  // If route is public, allow access
  if (isPublicRoute) {
    // If already authenticated and trying to access login, redirect to home/onboarding
    if (authStore.isAuthenticated && to.path === '/login') {
      const onboardingStore = useOnboardingStore()
      return navigateTo(onboardingStore.completed ? '/home' : '/onboarding/')
    }
    return
  }

  // For protected routes, check authentication
  // If not authenticated, redirect to login
  if (!authStore.isAuthenticated) {
    return navigateTo('/login')
  }

  // User is authenticated, allow access
  // (Onboarding middleware will handle onboarding flow separately)
})

import { useOnboardingStore } from '../stores/onboarding'

export default defineNuxtRouteMiddleware((to) => {
  const store = useOnboardingStore()

  // If completed and trying to access onboarding, redirect to dashboard
  if (store.completed && to.path.startsWith('/onboarding')) {
    return navigateTo('/dashboard')
  }

  // If NOT completed and trying to access dashboard, redirect to onboarding start
  if (!store.completed && to.path === '/dashboard') {
    return navigateTo('/onboarding/')
  }
  
  // If at root, redirect to onboarding or dashboard
  if (to.path === '/') {
    return store.completed ? navigateTo('/dashboard') : navigateTo('/onboarding/')
  }
})

/**
 * Authentication Store
 * Manages user authentication state, login/logout, and token refresh
 *
 * Security features:
 * - HttpOnly cookies for token storage (managed by backend)
 * - Automatic token refresh before expiry
 * - CSRF token handling
 * - Secure logout (revokes tokens)
 */

import { defineStore } from 'pinia'

// User type matching backend UserResponse schema
interface User {
  id: string  // UUID converted to string in JSON
  email: string
  full_name: string | null
  avatar_url: string | null
  oauth_provider: string
  created_at: string
  profile?: UserProfile
}

interface UserProfile {
  age: number | null
  weight: number | null
  height: number | null
  fitness_goal: string | null
  fitness_level: string | null
  preferred_units: string
  language: string
  notifications_enabled: boolean
}

// Login request matching backend schema
interface LoginOAuthRequest {
  id_token: string
  provider: 'google'
  csrf_token: string
  remember_me?: boolean
}

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    isAuthenticated: false,
    isLoading: false,
    error: null,
  }),

  getters: {
    /**
     * Check if user is authenticated
     */
    isLoggedIn: (state) => state.isAuthenticated && state.user !== null,

    /**
     * Get user display name
     */
    userName: (state) => state.user?.full_name || state.user?.email || 'User',

    /**
     * Get user avatar URL
     */
    userAvatar: (state) => state.user?.avatar_url || null,

    /**
     * Check if user has completed profile setup
     */
    hasCompletedProfile: (state) => {
      if (!state.user?.profile) return false
      const profile = state.user.profile
      return !!(
        profile.age &&
        profile.weight &&
        profile.height &&
        profile.fitness_goal &&
        profile.fitness_level
      )
    },
  },

  actions: {
    /**
     * Login with Google OAuth
     * @param idToken - Google ID token from OAuth flow
     * @param rememberMe - Extended session (30 days vs 7 days)
     */
    async loginWithGoogle(idToken: string, rememberMe = false): Promise<boolean> {
      this.isLoading = true
      this.error = null

      try {
        const api = useApi()

        // 1. Get CSRF token
        const csrfToken = await api.getCsrfToken()

        // 2. Send login request to backend
        const loginData: LoginOAuthRequest = {
          id_token: idToken,
          provider: 'google',
          csrf_token: csrfToken,
          remember_me: rememberMe,
        }

        const user = await api.post<User>('/api/v1/auth/login/oauth', loginData)

        // 3. Update store state
        this.user = user
        this.isAuthenticated = true
        this.isLoading = false

        return true
      } catch (error: any) {
        console.error('Login failed:', error)
        this.error = error.message || 'Login failed. Please try again.'
        this.isLoading = false
        this.user = null
        this.isAuthenticated = false
        return false
      }
    },

    /**
     * Logout current user
     * Revokes refresh token and clears cookies
     */
    async logout(): Promise<void> {
      try {
        const api = useApi()

        // Call backend logout endpoint (revokes refresh token)
        await api.post('/api/v1/auth/logout')
      } catch (error) {
        console.error('Logout error:', error)
        // Continue with local logout even if backend call fails
      } finally {
        // Clear local state
        this.user = null
        this.isAuthenticated = false
        this.error = null

        // Clear CSRF token
        const api = useApi()
        api.clearCsrfToken()

        // Redirect to login page
        await navigateTo('/login')
      }
    },

    /**
     * Logout from all devices
     * Revokes all refresh tokens for the user
     */
    async logoutAllDevices(): Promise<void> {
      try {
        const api = useApi()

        // Call backend logout-all endpoint
        await api.post('/api/v1/auth/logout-all')
      } catch (error) {
        console.error('Logout all devices error:', error)
      } finally {
        // Clear local state
        this.user = null
        this.isAuthenticated = false
        this.error = null

        // Clear CSRF token
        const api = useApi()
        api.clearCsrfToken()

        // Redirect to login page
        await navigateTo('/login')
      }
    },

    /**
     * Refresh access token using refresh token cookie
     * Called automatically by API client on 401 errors
     * @returns true if refresh successful, false otherwise
     */
    async refreshToken(): Promise<boolean> {
      try {
        const api = useApi()

        // Backend reads refresh_token from HttpOnly cookie
        // and returns updated user data
        const user = await api.post<User>('/api/v1/auth/refresh')

        // Update user data
        this.user = user
        this.isAuthenticated = true

        return true
      } catch (error) {
        console.error('Token refresh failed:', error)

        // Clear auth state on refresh failure
        this.user = null
        this.isAuthenticated = false

        return false
      }
    },

    /**
     * Fetch current authenticated user
     * Used to restore session on app load
     */
    async fetchCurrentUser(): Promise<boolean> {
      this.isLoading = true

      try {
        const api = useApi()

        // Try to get current user (requires valid access_token cookie)
        const user = await api.get<User>('/api/v1/auth/me')

        this.user = user
        this.isAuthenticated = true
        this.isLoading = false

        return true
      } catch (error: any) {
        // If 401, try to refresh token
        if (error.message?.includes('401')) {
          const refreshed = await this.refreshToken()
          if (refreshed) {
            this.isLoading = false
            return true
          }
        }

        // Not authenticated
        this.user = null
        this.isAuthenticated = false
        this.isLoading = false

        return false
      }
    },

    /**
     * Update user profile
     * @param profileData - Partial profile data to update
     */
    async updateProfile(profileData: Partial<UserProfile>): Promise<boolean> {
      try {
        const api = useApi()

        const updatedUser = await api.patch<User>('/api/v1/users/profile', profileData)

        // Update local user data
        this.user = updatedUser

        return true
      } catch (error) {
        console.error('Profile update failed:', error)
        this.error = 'Failed to update profile'
        return false
      }
    },

    /**
     * Clear error message
     */
    clearError(): void {
      this.error = null
    },
  },

  // Persist auth state to localStorage
  // Note: We only persist the authentication flag, not tokens
  // Tokens are stored in HttpOnly cookies by backend
  persist: {
    paths: ['isAuthenticated'], // Only persist auth status, not user data
  },
})

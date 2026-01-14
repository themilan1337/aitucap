/**
 * API Client Composable
 * Provides a configured API client with CSRF protection, error handling, and automatic token refresh
 *
 * Security features:
 * - CSRF token management (fetch, store, send in headers)
 * - Credentials included (sends HttpOnly cookies)
 * - Automatic 401 handling (redirects to login)
 * - Automatic token refresh on 401 errors
 */

interface ApiOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'
  body?: any
  requiresCsrf?: boolean
}

interface CsrfResponse {
  csrf_token: string
}

export const useApi = () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiUrl as string

  // Store CSRF token in memory (not localStorage for security)
  let csrfToken: string | null = null

  /**
   * Fetch CSRF token from backend
   * Backend returns token in both response body and X-CSRF-Token header
   */
  const fetchCsrfToken = async (): Promise<string> => {
    try {
      const response = await fetch(`${baseURL}/api/v1/auth/csrf-token`, {
        method: 'GET',
        credentials: 'include', // Include cookies
      })

      if (!response.ok) {
        throw new Error('Failed to fetch CSRF token')
      }

      // Try to get from header first (as per backend implementation)
      const headerToken = response.headers.get('X-CSRF-Token')
      if (headerToken) {
        csrfToken = headerToken
        return headerToken
      }

      // Fallback to response body
      const data: CsrfResponse = await response.json()
      csrfToken = data.csrf_token
      return csrfToken
    } catch (error) {
      console.error('Error fetching CSRF token:', error)
      throw error
    }
  }

  /**
   * Get current CSRF token, fetch new one if not available
   */
  const getCsrfToken = async (): Promise<string> => {
    if (!csrfToken) {
      return await fetchCsrfToken()
    }
    return csrfToken
  }

  /**
   * Clear stored CSRF token (used after failed requests)
   */
  const clearCsrfToken = () => {
    csrfToken = null
  }

  /**
   * Main API request function
   * @param endpoint - API endpoint (e.g., '/api/v1/users/profile')
   * @param options - Request options
   */
  const request = async <T = any>(
    endpoint: string,
    options: ApiOptions = {}
  ): Promise<T> => {
    const {
      method = 'GET',
      body = null,
      requiresCsrf = ['POST', 'PUT', 'PATCH', 'DELETE'].includes(method),
    } = options

    // Build headers
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    }

    // Add CSRF token for state-changing operations
    if (requiresCsrf) {
      try {
        const token = await getCsrfToken()
        headers['X-CSRF-Token'] = token
      } catch (error) {
        console.error('Failed to get CSRF token:', error)
        throw new Error('Authentication error: Unable to get CSRF token')
      }
    }

    // Make request
    try {
      const response = await fetch(`${baseURL}${endpoint}`, {
        method,
        headers,
        credentials: 'include', // CRITICAL: Send HttpOnly cookies
        body: body ? JSON.stringify(body) : null,
      })

      // Handle CSRF token errors (403) - fetch new token and retry once
      if (response.status === 403 && requiresCsrf) {
        console.warn('CSRF token invalid, fetching new token and retrying...')
        clearCsrfToken()
        const newToken = await fetchCsrfToken()
        headers['X-CSRF-Token'] = newToken

        // Retry request with new CSRF token
        const retryResponse = await fetch(`${baseURL}${endpoint}`, {
          method,
          headers,
          credentials: 'include',
          body: body ? JSON.stringify(body) : null,
        })

        if (!retryResponse.ok) {
          throw new Error(`API Error: ${retryResponse.status}`)
        }

        return await retryResponse.json()
      }

      // Handle unauthorized (401) - token expired or invalid
      if (response.status === 401) {
        // Try to refresh token first (handled by auth store)
        // If refresh fails, redirect to login
        const authStore = useAuthStore()
        const refreshed = await authStore.refreshToken()

        if (!refreshed) {
          // Redirect to login
          clearCsrfToken()
          await navigateTo('/login')
          throw new Error('Session expired. Please login again.')
        }

        // Retry original request after successful refresh
        const retryResponse = await fetch(`${baseURL}${endpoint}`, {
          method,
          headers,
          credentials: 'include',
          body: body ? JSON.stringify(body) : null,
        })

        if (!retryResponse.ok) {
          throw new Error(`API Error: ${retryResponse.status}`)
        }

        return await retryResponse.json()
      }

      // Handle other errors
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(
          errorData.detail || `API Error: ${response.status} ${response.statusText}`
        )
      }

      // Parse and return response
      const data = await response.json()
      return data
    } catch (error) {
      console.error('API Request Error:', error)
      throw error
    }
  }

  /**
   * Convenience methods for different HTTP verbs
   */
  const get = <T = any>(endpoint: string) =>
    request<T>(endpoint, { method: 'GET' })

  const post = <T = any>(endpoint: string, body?: any) =>
    request<T>(endpoint, { method: 'POST', body })

  const put = <T = any>(endpoint: string, body?: any) =>
    request<T>(endpoint, { method: 'PUT', body })

  const patch = <T = any>(endpoint: string, body?: any) =>
    request<T>(endpoint, { method: 'PATCH', body })

  const del = <T = any>(endpoint: string) =>
    request<T>(endpoint, { method: 'DELETE' })

  return {
    request,
    get,
    post,
    put,
    patch,
    delete: del,
    fetchCsrfToken,
    getCsrfToken,
    clearCsrfToken,
  }
}

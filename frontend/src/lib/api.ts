import axios from 'axios'

export const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api',
    headers: {
        'Content-Type': 'application/json',
    },
})

// Interceptor para agregar token JWT a todas las requests
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config

        // Si es 401 y no es un retry, intentar refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true
            const refreshToken = localStorage.getItem('refreshToken')

            if (refreshToken) {
                try {
                    const res = await api.post('/auth/refresh', { refreshToken })
                    const { token, refreshToken: newRefresh } = res.data
                    localStorage.setItem('token', token)
                    localStorage.setItem('refreshToken', newRefresh)
                    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
                    originalRequest.headers['Authorization'] = `Bearer ${token}`
                    return api(originalRequest)
                } catch {
                    // Refresh falló, limpiar sesión
                }
            }

            localStorage.removeItem('token')
            localStorage.removeItem('refreshToken')
            localStorage.removeItem('userId')
            localStorage.removeItem('userName')
            localStorage.removeItem('userEmail')
            localStorage.removeItem('userRole')

            if (!window.location.pathname.startsWith('/auth')) {
                window.location.href = '/auth/login'
            }
        }
        return Promise.reject(error)
    }
)

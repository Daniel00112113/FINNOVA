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
    (error) => {
        if (error.response?.status === 401) {
            // Token inválido o expirado
            localStorage.removeItem('token')
            localStorage.removeItem('userId')
            localStorage.removeItem('userName')
            localStorage.removeItem('userEmail')

            // Redirigir a login solo si no estamos ya en una página de auth
            if (!window.location.pathname.startsWith('/auth')) {
                window.location.href = '/auth/login'
            }
        }
        return Promise.reject(error)
    }
)

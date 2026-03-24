import { api } from './api'

export interface AuthResponse {
    token: string
    userId: string
    name: string
    email: string
}

export interface RegisterData {
    name: string
    email: string
    password: string
}

export interface LoginData {
    email: string
    password: string
}

// Registrar nuevo usuario
export const register = async (data: RegisterData): Promise<AuthResponse> => {
    const response = await api.post('/auth/register', data)
    const authData = response.data

    localStorage.setItem('token', authData.token)
    localStorage.setItem('refreshToken', authData.refreshToken)
    localStorage.setItem('userId', authData.userId)
    localStorage.setItem('userName', authData.name)
    localStorage.setItem('userEmail', authData.email)
    localStorage.setItem('userRole', authData.role || 'user')

    api.defaults.headers.common['Authorization'] = `Bearer ${authData.token}`
    return authData
}

// Login de usuario
export const login = async (data: LoginData): Promise<AuthResponse> => {
    const response = await api.post('/auth/login', data)
    const authData = response.data

    localStorage.setItem('token', authData.token)
    localStorage.setItem('refreshToken', authData.refreshToken)
    localStorage.setItem('userId', authData.userId)
    localStorage.setItem('userName', authData.name)
    localStorage.setItem('userEmail', authData.email)
    localStorage.setItem('userRole', authData.role || 'user')

    api.defaults.headers.common['Authorization'] = `Bearer ${authData.token}`
    return authData
}

// Logout
export const logout = () => {
    const refreshToken = localStorage.getItem('refreshToken')
    if (refreshToken) {
        api.post('/auth/logout', { refreshToken }).catch(() => { })
    }
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('userId')
    localStorage.removeItem('userName')
    localStorage.removeItem('userEmail')
    localStorage.removeItem('userRole')
    delete api.defaults.headers.common['Authorization']
    window.location.href = '/auth/login'
}

// Verificar si está autenticado
export const isAuthenticated = (): boolean => {
    if (typeof window === 'undefined') return false
    return !!localStorage.getItem('token')
}

// Obtener token actual
export const getToken = (): string | null => {
    if (typeof window === 'undefined') return null
    return localStorage.getItem('token')
}

// Obtener userId actual
export const getUserId = (): string | null => {
    if (typeof window === 'undefined') return null
    return localStorage.getItem('userId')
}

// Obtener datos del usuario
export const getUserData = () => {
    if (typeof window === 'undefined') {
        return { userId: null, name: null, email: null }
    }
    return {
        userId: localStorage.getItem('userId'),
        name: localStorage.getItem('userName'),
        email: localStorage.getItem('userEmail')
    }
}

// Inicializar auth (llamar al inicio de la app)
export const initializeAuth = () => {
    const token = getToken()
    if (token) {
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`
    }
}

// Validar token con el servidor
export const validateToken = async (): Promise<boolean> => {
    try {
        const token = getToken()
        if (!token) return false

        const response = await api.post('/auth/validate', { token })
        return response.data.valid
    } catch (error) {
        logout()
        return false
    }
}

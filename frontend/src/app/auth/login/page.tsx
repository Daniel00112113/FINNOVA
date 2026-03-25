'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { login } from '@/lib/auth'
import Logo from '@/components/Logo'

export default function LoginPage() {
    const router = useRouter()
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [showPassword, setShowPassword] = useState(false)
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError('')
        setLoading(true)
        try {
            await login({ email, password })
            router.push('/dashboard')
        } catch (err: any) {
            const msg = err.response?.data?.message || 'Error al iniciar sesión'
            setError(msg.includes('bloqueada') ? `🔒 ${msg}` : msg)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-[#030712] flex items-center justify-center px-4 relative overflow-hidden">
            <style>{`
                @keyframes glow { 0%,100%{opacity:.4}50%{opacity:.8} }
                @keyframes float { from{transform:translateY(0) rotate(0)}to{transform:translateY(-16px) rotate(180deg)} }
                @keyframes slideUp { from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:translateY(0)} }
                .glass { background:rgba(255,255,255,0.04); backdrop-filter:blur(20px); border:1px solid rgba(255,255,255,0.08); }
                .input-dark { background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); color:white; transition:all .2s; }
                .input-dark:focus { outline:none; border-color:rgba(16,185,129,0.6); box-shadow:0 0 0 3px rgba(16,185,129,0.1); background:rgba(255,255,255,0.07); }
                .input-dark::placeholder { color:rgba(255,255,255,0.25); }
                .animate-slide-up { animation:slideUp .6s ease forwards; }
                .shimmer { background:linear-gradient(90deg,#10b981,#34d399,#10b981);background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 3s linear infinite; }
                @keyframes shimmer { 0%{background-position:-200% center}100%{background-position:200% center} }
            `}</style>

            {/* Orbes de fondo */}
            <div className="absolute top-1/4 left-1/3 w-72 h-72 rounded-full pointer-events-none"
                style={{ background: 'radial-gradient(circle,rgba(16,185,129,0.1) 0%,transparent 70%)', animation: 'glow 4s ease-in-out infinite' }} />
            <div className="absolute bottom-1/4 right-1/3 w-56 h-56 rounded-full pointer-events-none"
                style={{ background: 'radial-gradient(circle,rgba(52,211,153,0.07) 0%,transparent 70%)', animation: 'glow 6s ease-in-out 2s infinite' }} />

            {/* Grid de fondo */}
            <div className="absolute inset-0 pointer-events-none"
                style={{ backgroundImage: 'linear-gradient(rgba(16,185,129,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(16,185,129,0.04) 1px,transparent 1px)', backgroundSize: '60px 60px' }} />

            <div className="relative z-10 w-full max-w-md animate-slide-up">
                {/* Logo */}
                <div className="text-center mb-8">
                    <Link href="/" className="inline-flex items-center gap-2 mb-4">
                        <Logo width={44} height={44} />
                        <span className="text-2xl font-black shimmer">FINNOVA</span>
                    </Link>
                    <h1 className="text-2xl font-black text-white">Bienvenido de vuelta</h1>
                    <p className="text-gray-500 text-sm mt-1">Inicia sesión en tu cuenta</p>
                </div>

                {/* Card */}
                <div className="glass rounded-2xl p-8">
                    {error && (
                        <div className="mb-5 px-4 py-3 rounded-xl text-sm font-medium"
                            style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', color: '#fca5a5' }}>
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-5">
                        <div>
                            <label className="block text-xs font-semibold text-gray-400 mb-2 uppercase tracking-wider">Email</label>
                            <input
                                type="email" required autoComplete="email"
                                value={email} onChange={e => setEmail(e.target.value)}
                                placeholder="tu@email.com"
                                className="input-dark w-full px-4 py-3 rounded-xl text-sm"
                            />
                        </div>

                        <div>
                            <label className="block text-xs font-semibold text-gray-400 mb-2 uppercase tracking-wider">Contraseña</label>
                            <div className="relative">
                                <input
                                    type={showPassword ? 'text' : 'password'} required autoComplete="current-password"
                                    value={password} onChange={e => setPassword(e.target.value)}
                                    placeholder="••••••••"
                                    className="input-dark w-full px-4 py-3 pr-12 rounded-xl text-sm"
                                />
                                <button type="button" onClick={() => setShowPassword(!showPassword)}
                                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300 transition-colors text-lg">
                                    {showPassword ? '🙈' : '👁️'}
                                </button>
                            </div>
                        </div>

                        <button type="submit" disabled={loading}
                            className="w-full py-3.5 rounded-xl font-bold text-sm text-white transition-all disabled:opacity-50 relative overflow-hidden group"
                            style={{ background: 'linear-gradient(135deg,#10b981,#059669)', boxShadow: loading ? 'none' : '0 0 30px rgba(16,185,129,0.3)' }}>
                            <span className="relative z-10">
                                {loading ? (
                                    <span className="flex items-center justify-center gap-2">
                                        <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                        </svg>
                                        Iniciando sesión...
                                    </span>
                                ) : 'Iniciar Sesión →'}
                            </span>
                            <div className="absolute inset-0 bg-white opacity-0 group-hover:opacity-10 transition-opacity" />
                        </button>
                    </form>

                    <div className="mt-6 pt-6 text-center" style={{ borderTop: '1px solid rgba(255,255,255,0.06)' }}>
                        <p className="text-gray-500 text-sm">
                            ¿No tienes cuenta?{' '}
                            <Link href="/auth/register" className="text-emerald-400 hover:text-emerald-300 font-semibold transition-colors">
                                Regístrate gratis
                            </Link>
                        </p>
                    </div>
                </div>

                <p className="text-center text-gray-600 text-xs mt-6">
                    🇨🇴 Hecho en Colombia • 100% Seguro
                </p>
            </div>
        </div>
    )
}

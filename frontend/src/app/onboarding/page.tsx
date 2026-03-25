'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Logo from '@/components/Logo'

const steps = [
    {
        icon: '🎉',
        title: 'Bienvenido a FINNOVA',
        subtitle: 'Tu copiloto financiero impulsado por IA',
        features: [
            { icon: '📊', label: 'Analiza tus finanzas', desc: 'Identifica patrones automáticamente' },
            { icon: '🔮', label: 'Predice tu futuro', desc: 'Proyecciones precisas con IA' },
            { icon: '🎯', label: 'Simula escenarios', desc: 'Decide antes de actuar' },
            { icon: '🏆', label: 'Gana logros', desc: 'Gamificación financiera' },
        ]
    },
    {
        icon: '💳',
        title: 'Registra tus Transacciones',
        subtitle: 'La base de todo — ingresos y gastos',
        demo: 'transactions'
    },
    {
        icon: '🔮',
        title: 'Predicciones con IA',
        subtitle: 'La IA aprende de tus patrones',
        demo: 'predictions'
    },
    {
        icon: '🎯',
        title: 'Simulador de Escenarios',
        subtitle: 'Compara 5 futuros posibles',
        demo: 'simulator'
    },
    {
        icon: '🚀',
        title: '¡Todo Listo!',
        subtitle: 'Ahora te mostramos un tour del dashboard',
        final: true
    },
]

export default function OnboardingPage() {
    const router = useRouter()
    const [step, setStep] = useState(0)
    const [userName, setUserName] = useState('Usuario')
    const [animating, setAnimating] = useState(false)

    useEffect(() => {
        const name = localStorage.getItem('userName') || 'Usuario'
        setUserName(name.split(' ')[0])
    }, [])

    const goTo = (next: number) => {
        setAnimating(true)
        setTimeout(() => { setStep(next); setAnimating(false) }, 250)
    }

    const handleNext = () => {
        if (step < steps.length - 1) goTo(step + 1)
        else finish(true)
    }

    const finish = (withTour: boolean) => {
        localStorage.removeItem('isNewUser')
        if (withTour) {
            localStorage.setItem('startTour', 'true')
        }
        router.push('/dashboard')
    }

    const progress = ((step + 1) / steps.length) * 100
    const current = steps[step]

    return (
        <div className="min-h-screen bg-[#030712] flex items-center justify-center p-4 relative overflow-hidden">
            <style>{`
                @keyframes glow { 0%,100%{opacity:.4}50%{opacity:.9} }
                @keyframes slideIn { from{opacity:0;transform:translateX(30px)}to{opacity:1;transform:translateX(0)} }
                @keyframes fadeUp { from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)} }
                .glass { background:rgba(255,255,255,0.04); backdrop-filter:blur(20px); border:1px solid rgba(255,255,255,0.08); }
                .step-in { animation: slideIn .25s ease forwards; }
                .shimmer { background:linear-gradient(90deg,#10b981,#34d399,#10b981);background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 3s linear infinite; }
                @keyframes shimmer { 0%{background-position:-200% center}100%{background-position:200% center} }
                .dot-active { background:#10b981; width:2rem; }
                .dot { background:rgba(255,255,255,0.15); width:.5rem; }
            `}</style>

            {/* Orbes */}
            <div className="absolute top-1/4 left-1/4 w-80 h-80 rounded-full pointer-events-none"
                style={{ background: 'radial-gradient(circle,rgba(16,185,129,0.1) 0%,transparent 70%)', animation: 'glow 4s ease-in-out infinite' }} />
            <div className="absolute bottom-1/4 right-1/4 w-64 h-64 rounded-full pointer-events-none"
                style={{ background: 'radial-gradient(circle,rgba(52,211,153,0.07) 0%,transparent 70%)', animation: 'glow 6s ease-in-out 2s infinite' }} />
            <div className="absolute inset-0 pointer-events-none"
                style={{ backgroundImage: 'linear-gradient(rgba(16,185,129,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(16,185,129,0.03) 1px,transparent 1px)', backgroundSize: '60px 60px' }} />

            <div className="relative z-10 w-full max-w-2xl">
                {/* Header */}
                <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-2">
                        <Logo width={32} height={32} />
                        <span className="font-black shimmer text-lg">FINNOVA</span>
                    </div>
                    <button onClick={() => finish(false)}
                        className="text-gray-600 hover:text-gray-400 text-sm transition-colors">
                        Saltar →
                    </button>
                </div>

                {/* Barra de progreso */}
                <div className="mb-6">
                    <div className="flex justify-between text-xs text-gray-600 mb-2">
                        <span>Paso {step + 1} de {steps.length}</span>
                        <span>{Math.round(progress)}%</span>
                    </div>
                    <div className="w-full rounded-full h-1.5" style={{ background: 'rgba(255,255,255,0.06)' }}>
                        <div className="h-1.5 rounded-full transition-all duration-500"
                            style={{ width: `${progress}%`, background: 'linear-gradient(90deg,#10b981,#34d399)' }} />
                    </div>
                </div>

                {/* Card principal */}
                <div className={`glass rounded-3xl p-8 md:p-10 ${animating ? 'opacity-0' : 'step-in'}`}>
                    {/* Icono y título */}
                    <div className="text-center mb-8">
                        <div className="text-6xl mb-4" style={{ filter: 'drop-shadow(0 0 20px rgba(16,185,129,0.4))' }}>
                            {current.icon}
                        </div>
                        <h2 className="text-2xl md:text-3xl font-black text-white mb-2">
                            {step === 0 ? `¡Hola, ${userName}! 👋` : current.title}
                        </h2>
                        <p className="text-gray-400">{current.subtitle}</p>
                    </div>

                    {/* Contenido por paso */}
                    {step === 0 && (
                        <div className="grid grid-cols-2 gap-3">
                            {current.features!.map((f, i) => (
                                <div key={i} className="rounded-2xl p-4 transition-all hover:scale-105"
                                    style={{ background: 'rgba(16,185,129,0.06)', border: '1px solid rgba(16,185,129,0.15)', animationDelay: `${i * 0.1}s` }}>
                                    <div className="text-2xl mb-2">{f.icon}</div>
                                    <div className="font-semibold text-white text-sm">{f.label}</div>
                                    <div className="text-gray-500 text-xs mt-0.5">{f.desc}</div>
                                </div>
                            ))}
                        </div>
                    )}

                    {current.demo === 'transactions' && (
                        <div className="space-y-4">
                            <div className="rounded-2xl p-5" style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.07)' }}>
                                <div className="flex items-center justify-between mb-4">
                                    <span className="text-sm font-semibold text-gray-300">Transacciones recientes</span>
                                    <span className="text-xs text-emerald-400">+ Agregar</span>
                                </div>
                                {[
                                    { icon: '💰', label: 'Salario', amount: '+$3,000,000', color: 'text-emerald-400' },
                                    { icon: '🛒', label: 'Supermercado', amount: '-$180,000', color: 'text-red-400' },
                                    { icon: '🚗', label: 'Transporte', amount: '-$50,000', color: 'text-red-400' },
                                ].map((t, i) => (
                                    <div key={i} className="flex items-center justify-between py-3 border-b last:border-0"
                                        style={{ borderColor: 'rgba(255,255,255,0.05)' }}>
                                        <div className="flex items-center gap-3">
                                            <span className="text-xl">{t.icon}</span>
                                            <span className="text-sm text-gray-300">{t.label}</span>
                                        </div>
                                        <span className={`text-sm font-bold ${t.color}`}>{t.amount}</span>
                                    </div>
                                ))}
                            </div>
                            <div className="flex gap-2 text-xs text-gray-500">
                                <span className="px-3 py-1 rounded-full" style={{ background: 'rgba(16,185,129,0.1)', color: '#10b981' }}>✓ Categorías automáticas</span>
                                <span className="px-3 py-1 rounded-full" style={{ background: 'rgba(16,185,129,0.1)', color: '#10b981' }}>✓ Etiquetas y ubicación</span>
                            </div>
                        </div>
                    )}

                    {current.demo === 'predictions' && (
                        <div className="space-y-4">
                            <div className="rounded-2xl p-5" style={{ background: 'linear-gradient(135deg,rgba(139,92,246,0.15),rgba(59,130,246,0.15))', border: '1px solid rgba(139,92,246,0.2)' }}>
                                <div className="flex items-center gap-3 mb-4">
                                    <span className="text-2xl">🤖</span>
                                    <div>
                                        <div className="text-sm font-bold text-white">Predicción IA — 3 meses</div>
                                        <div className="text-xs text-gray-400">Basado en tus patrones</div>
                                    </div>
                                    <span className="ml-auto text-xs px-2 py-1 rounded-full" style={{ background: 'rgba(16,185,129,0.2)', color: '#10b981' }}>85% confianza</span>
                                </div>
                                <div className="flex items-end gap-1 h-16">
                                    {[40, 55, 48, 70, 62, 80, 75, 90, 85, 95, 88, 100].map((h, i) => (
                                        <div key={i} className="flex-1 rounded-t transition-all"
                                            style={{ height: `${h}%`, background: `rgba(139,92,246,${0.2 + (i / 12) * 0.6})` }} />
                                    ))}
                                </div>
                                <div className="mt-3 flex justify-between text-xs text-gray-500">
                                    <span>Hoy</span>
                                    <span className="text-violet-400 font-bold">Balance proyectado: $2,700,000</span>
                                </div>
                            </div>
                            <div className="grid grid-cols-3 gap-2 text-xs text-center">
                                {[
                                    { label: 'Tendencia', value: '📈 Creciente', color: 'text-emerald-400' },
                                    { label: 'Riesgo', value: '🟢 Bajo', color: 'text-emerald-400' },
                                    { label: 'Ahorro/mes', value: '$450,000', color: 'text-blue-400' },
                                ].map(s => (
                                    <div key={s.label} className="rounded-xl p-3" style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.07)' }}>
                                        <div className="text-gray-500 mb-1">{s.label}</div>
                                        <div className={`font-bold ${s.color}`}>{s.value}</div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {current.demo === 'simulator' && (
                        <div className="space-y-3">
                            {[
                                { icon: '📊', label: 'Situación actual', balance: '$900,000', badge: '', color: 'rgba(255,255,255,0.04)' },
                                { icon: '✂️', label: 'Reducir gastos 20%', balance: '$1,620,000', badge: '🏆 Recomendado', color: 'rgba(16,185,129,0.08)' },
                                { icon: '📈', label: 'Aumentar ingresos 15%', balance: '$1,485,000', badge: '', color: 'rgba(255,255,255,0.04)' },
                                { icon: '💳', label: 'Pago agresivo deuda', balance: '$1,200,000', badge: '', color: 'rgba(255,255,255,0.04)' },
                            ].map((s, i) => (
                                <div key={i} className="flex items-center justify-between rounded-xl px-4 py-3 transition-all"
                                    style={{ background: s.color, border: `1px solid ${s.badge ? 'rgba(16,185,129,0.3)' : 'rgba(255,255,255,0.07)'}` }}>
                                    <div className="flex items-center gap-3">
                                        <span>{s.icon}</span>
                                        <div>
                                            <div className="text-sm text-white font-medium">{s.label}</div>
                                            {s.badge && <span className="text-xs text-emerald-400">{s.badge}</span>}
                                        </div>
                                    </div>
                                    <span className={`text-sm font-bold ${s.badge ? 'text-emerald-400' : 'text-gray-300'}`}>{s.balance}</span>
                                </div>
                            ))}
                            <p className="text-xs text-gray-600 text-center">Proyección a 12 meses</p>
                        </div>
                    )}

                    {current.final && (
                        <div className="text-center space-y-6">
                            <div className="rounded-2xl p-6" style={{ background: 'linear-gradient(135deg,rgba(16,185,129,0.1),rgba(52,211,153,0.05))', border: '1px solid rgba(16,185,129,0.2)' }}>
                                <div className="text-4xl mb-3">🗺️</div>
                                <h3 className="text-white font-bold text-lg mb-2">Tour Interactivo del Dashboard</h3>
                                <p className="text-gray-400 text-sm leading-relaxed">
                                    Te mostraremos cada sección del dashboard con explicaciones en tiempo real.
                                    Puedes pausarlo cuando quieras.
                                </p>
                            </div>
                            <div className="grid grid-cols-2 gap-3 text-xs">
                                {['Dashboard', 'Gamificación', 'Predicciones', 'Simulador', 'Análisis', 'Alertas'].map(f => (
                                    <div key={f} className="flex items-center gap-2 text-gray-400">
                                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                                        {f}
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Botones */}
                    <div className="flex gap-3 mt-8">
                        {step > 0 && (
                            <button onClick={() => goTo(step - 1)}
                                className="px-5 py-3 rounded-xl text-sm font-semibold text-gray-400 hover:text-white transition-colors"
                                style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.08)' }}>
                                ← Anterior
                            </button>
                        )}
                        <button onClick={handleNext}
                            className="flex-1 py-3.5 rounded-xl font-bold text-sm text-white relative overflow-hidden group transition-all"
                            style={{ background: 'linear-gradient(135deg,#10b981,#059669)', boxShadow: '0 0 30px rgba(16,185,129,0.3)' }}>
                            <span className="relative z-10">
                                {step === steps.length - 1 ? '🗺️ Iniciar Tour del Dashboard' : 'Siguiente →'}
                            </span>
                            <div className="absolute inset-0 bg-white opacity-0 group-hover:opacity-10 transition-opacity" />
                        </button>
                        {step === steps.length - 1 && (
                            <button onClick={() => finish(false)}
                                className="px-5 py-3 rounded-xl text-sm font-semibold text-gray-500 hover:text-gray-300 transition-colors"
                                style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)' }}>
                                Sin tour
                            </button>
                        )}
                    </div>
                </div>

                {/* Dots */}
                <div className="flex justify-center gap-2 mt-5">
                    {steps.map((_, i) => (
                        <button key={i} onClick={() => goTo(i)}
                            className="h-1.5 rounded-full transition-all duration-300"
                            style={{ width: i === step ? '2rem' : '0.5rem', background: i === step ? '#10b981' : 'rgba(255,255,255,0.15)' }} />
                    ))}
                </div>
            </div>
        </div>
    )
}

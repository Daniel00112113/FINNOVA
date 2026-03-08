'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import Logo from '@/components/Logo'

export default function LandingPage() {
    const router = useRouter()

    const handleGetStarted = () => {
        router.push('/auth/register')
    }

    const features = [
        {
            icon: (
                <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
            ),
            title: 'IA Predictiva',
            description: 'Predicciones inteligentes de tu futuro financiero basadas en tus patrones de gasto'
        },
        {
            icon: (
                <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
            ),
            title: 'Análisis Automático',
            description: 'Identifica automáticamente tus hábitos de gasto y recibe recomendaciones personalizadas'
        },
        {
            icon: (
                <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
                </svg>
            ),
            title: 'Simulador de Escenarios',
            description: 'Visualiza diferentes escenarios financieros antes de tomar decisiones importantes'
        },
        {
            icon: (
                <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                </svg>
            ),
            title: 'Gestión de Deudas',
            description: 'Controla tus deudas, calcula intereses y recibe planes de pago optimizados'
        },
        {
            icon: (
                <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
            ),
            title: 'Alertas Inteligentes',
            description: 'Recibe notificaciones automáticas sobre gastos elevados y riesgos financieros'
        },
        {
            icon: (
                <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
            ),
            title: 'Reportes Visuales',
            description: 'Gráficas interactivas y reportes detallados de tu situación financiera'
        }
    ]

    const testimonials = [
        {
            name: 'María González',
            role: 'Profesional Independiente',
            initials: 'MG',
            text: 'Gracias a FINNOVA logré reducir mis gastos en 30% y pagar mi tarjeta de crédito en 6 meses.'
        },
        {
            name: 'Carlos Rodríguez',
            role: 'Emprendedor',
            initials: 'CR',
            text: 'Las predicciones de IA me ayudaron a planificar mejor mi flujo de caja. Increíble herramienta.'
        },
        {
            name: 'Ana Martínez',
            role: 'Estudiante',
            initials: 'AM',
            text: 'Finalmente entiendo a dónde va mi dinero. La app es súper fácil de usar y me ha ayudado a ahorrar.'
        }
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-emerald-50">
            {/* Navbar */}
            <nav className="bg-white/80 backdrop-blur-md shadow-sm sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-20">
                        <div className="flex items-center gap-2">
                            <Logo width={70} height={70} priority />
                            <span className="text-4xl font-black bg-gradient-to-r from-gray-900 via-green-600 to-gray-900 bg-clip-text text-transparent tracking-tight">
                                FINNOVA
                            </span>
                        </div>
                        <div className="flex items-center gap-4">
                            <Link
                                href="/auth/login"
                                className="text-gray-700 hover:text-emerald-600 font-medium transition"
                            >
                                Iniciar Sesión
                            </Link>
                            <button
                                onClick={handleGetStarted}
                                className="bg-gradient-to-r from-emerald-600 to-green-600 text-white px-6 py-2 rounded-lg font-semibold hover:shadow-lg transition-all transform hover:scale-105"
                            >
                                Comenzar Gratis
                            </button>
                        </div>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
                <div className="text-center">
                    <div className="inline-block mb-4">
                        <span className="bg-emerald-100 text-emerald-700 px-4 py-2 rounded-full text-sm font-semibold">
                            Powered by Artificial Intelligence
                        </span>
                    </div>

                    <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
                        Tu Copiloto Financiero
                        <br />
                        <span className="bg-gradient-to-r from-emerald-600 to-green-600 bg-clip-text text-transparent">
                            Impulsado por IA
                        </span>
                    </h1>
                    <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
                        Toma el control de tus finanzas con inteligencia artificial.
                        Predicciones precisas, análisis automático y recomendaciones personalizadas
                        para alcanzar tus metas financieras.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                        <button
                            onClick={handleGetStarted}
                            className="bg-gradient-to-r from-emerald-600 to-green-600 text-white px-8 py-4 rounded-xl font-bold text-lg hover:shadow-2xl transition-all transform hover:scale-105"
                        >
                            Comenzar Gratis →
                        </button>
                        <Link
                            href="#features"
                            className="text-gray-700 px-8 py-4 rounded-xl font-semibold border-2 border-gray-300 hover:border-emerald-600 transition"
                        >
                            Ver Características
                        </Link>
                    </div>
                    <p className="text-sm text-gray-500 mt-4">
                        No requiere tarjeta de crédito • 100% Seguro • Hecho en Colombia
                    </p>
                </div>

                {/* Hero Image/Demo */}
                <div className="mt-16 relative">
                    <div className="bg-white rounded-2xl p-8 shadow-xl border border-gray-200">
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-xl border border-green-200">
                                <svg className="w-8 h-8 text-green-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                <div className="text-sm text-gray-600">Balance Total</div>
                                <div className="text-2xl font-bold text-green-600">$8,450,000</div>
                                <div className="text-xs text-green-600 mt-1">↑ +12% este mes</div>
                            </div>
                            <div className="bg-gradient-to-br from-emerald-50 to-emerald-100 p-6 rounded-xl border border-emerald-200">
                                <svg className="w-8 h-8 text-emerald-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                                </svg>
                                <div className="text-sm text-gray-600">Predicción IA</div>
                                <div className="text-2xl font-bold text-gray-900">$9,200,000</div>
                                <div className="text-xs text-emerald-600 mt-1">En 3 meses</div>
                            </div>
                            <div className="bg-gradient-to-br from-emerald-50 to-emerald-100 p-6 rounded-xl border border-emerald-200">
                                <svg className="w-8 h-8 text-emerald-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                                </svg>
                                <div className="text-sm text-gray-600">Ahorro Sugerido</div>
                                <div className="text-2xl font-bold text-emerald-600">$750,000</div>
                                <div className="text-xs text-emerald-600 mt-1">Por mes</div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section id="features" className="bg-white py-20">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-16">
                        <h2 className="text-4xl font-bold text-gray-900 mb-4">
                            Características Poderosas
                        </h2>
                        <p className="text-xl text-gray-600">
                            Todo lo que necesitas para dominar tus finanzas personales
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {features.map((feature, index) => (
                            <div
                                key={index}
                                className="bg-gradient-to-br from-gray-50 to-white p-8 rounded-2xl border border-gray-200 hover:shadow-xl transition-all transform hover:scale-105"
                            >
                                <div className="text-emerald-600 mb-4">{feature.icon}</div>
                                <h3 className="text-xl font-bold text-gray-900 mb-3">
                                    {feature.title}
                                </h3>
                                <p className="text-gray-600">
                                    {feature.description}
                                </p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* How It Works */}
            <section className="py-20 bg-gradient-to-br from-gray-50 to-emerald-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-16">
                        <h2 className="text-4xl font-bold text-gray-900 mb-4">
                            ¿Cómo Funciona?
                        </h2>
                        <p className="text-xl text-gray-600">
                            Comienza en 3 simples pasos
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        <div className="text-center">
                            <div className="bg-gradient-to-r from-emerald-600 to-green-600 text-white w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6">
                                1
                            </div>
                            <h3 className="text-xl font-bold text-gray-900 mb-3">
                                Crea tu Cuenta
                            </h3>
                            <p className="text-gray-600">
                                Regístrate gratis en menos de 1 minuto. No necesitas tarjeta de crédito.
                            </p>
                        </div>

                        <div className="text-center">
                            <div className="bg-gradient-to-r from-emerald-600 to-green-600 text-white w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6">
                                2
                            </div>
                            <h3 className="text-xl font-bold text-gray-900 mb-3">
                                Registra tus Transacciones
                            </h3>
                            <p className="text-gray-600">
                                Agrega tus ingresos, gastos y deudas. La IA comenzará a aprender tus patrones.
                            </p>
                        </div>

                        <div className="text-center">
                            <div className="bg-gradient-to-r from-emerald-600 to-green-600 text-white w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6">
                                3
                            </div>
                            <h3 className="text-xl font-bold text-gray-900 mb-3">
                                Recibe Insights
                            </h3>
                            <p className="text-gray-600">
                                Obtén predicciones, alertas y recomendaciones personalizadas automáticamente.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Testimonials */}
            <section className="bg-white py-20">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-16">
                        <h2 className="text-4xl font-bold text-gray-900 mb-4">
                            Lo Que Dicen Nuestros Usuarios
                        </h2>
                        <p className="text-xl text-gray-600">
                            Miles de personas ya están mejorando sus finanzas
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {testimonials.map((testimonial, index) => (
                            <div
                                key={index}
                                className="bg-gradient-to-br from-gray-50 to-white p-8 rounded-2xl border border-gray-200 hover:shadow-xl transition-all"
                            >
                                <div className="flex items-center gap-4 mb-4">
                                    <div className="w-16 h-16 rounded-full bg-gradient-to-r from-emerald-600 to-green-600 flex items-center justify-center text-white font-bold text-xl">
                                        {testimonial.initials}
                                    </div>
                                    <div>
                                        <div className="font-bold text-gray-900">{testimonial.name}</div>
                                        <div className="text-sm text-gray-600">{testimonial.role}</div>
                                    </div>
                                </div>
                                <p className="text-gray-700 italic">"{testimonial.text}"</p>
                                <div className="mt-4 flex gap-1">
                                    {[...Array(5)].map((_, i) => (
                                        <svg key={i} className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                        </svg>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="bg-gradient-to-r from-gray-900 to-emerald-900 py-20">
                <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <h2 className="text-4xl font-bold text-white mb-6">
                        ¿Listo para Transformar tus Finanzas?
                    </h2>
                    <p className="text-xl text-emerald-100 mb-8">
                        Únete a miles de usuarios que ya están tomando mejores decisiones financieras con IA
                    </p>
                    <button
                        onClick={handleGetStarted}
                        className="bg-white text-emerald-600 px-8 py-4 rounded-xl font-bold text-lg hover:shadow-2xl transition-all transform hover:scale-105"
                    >
                        Comenzar Gratis Ahora →
                    </button>
                    <p className="text-sm text-emerald-100 mt-4">
                        Sin compromisos • Cancela cuando quieras
                    </p>
                </div>
            </section>

            {/* Footer */}
            <footer className="bg-gray-900 text-white py-12">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                        <div>
                            <Logo width={60} height={60} showText className="mb-4" />
                            <p className="text-gray-400">
                                Tu copiloto financiero impulsado por inteligencia artificial.
                            </p>
                        </div>

                        <div>
                            <h4 className="font-bold mb-4">Producto</h4>
                            <ul className="space-y-2 text-gray-400">
                                <li><a href="#features" className="hover:text-white transition">Características</a></li>
                                <li><a href="#" className="hover:text-white transition">Precios</a></li>
                                <li><a href="#" className="hover:text-white transition">Demo</a></li>
                            </ul>
                        </div>

                        <div>
                            <h4 className="font-bold mb-4">Empresa</h4>
                            <ul className="space-y-2 text-gray-400">
                                <li><a href="#" className="hover:text-white transition">Sobre Nosotros</a></li>
                                <li><a href="#" className="hover:text-white transition">Blog</a></li>
                                <li><a href="#" className="hover:text-white transition">Contacto</a></li>
                            </ul>
                        </div>

                        <div>
                            <h4 className="font-bold mb-4">Legal</h4>
                            <ul className="space-y-2 text-gray-400">
                                <li><a href="#" className="hover:text-white transition">Privacidad</a></li>
                                <li><a href="#" className="hover:text-white transition">Términos</a></li>
                                <li><a href="#" className="hover:text-white transition">Seguridad</a></li>
                            </ul>
                        </div>
                    </div>

                    <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
                        <p>© 2024 FINNOVA. Todos los derechos reservados. Hecho con pasión en Colombia</p>
                    </div>
                </div>
            </footer>
        </div>
    )
}

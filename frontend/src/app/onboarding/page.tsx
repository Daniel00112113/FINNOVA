'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function OnboardingPage() {
    const router = useRouter()
    const [currentStep, setCurrentStep] = useState(0)
    const [userName, setUserName] = useState('')

    useEffect(() => {
        const name = localStorage.getItem('userName') || 'Usuario'
        setUserName(name.split(' ')[0]) // Solo primer nombre
    }, [])

    const steps = [
        {
            title: '¡Bienvenido a FINNOVA!',
            subtitle: `Hola ${userName}, estamos emocionados de tenerte aquí`,
            icon: '🎉',
            content: (
                <div className="space-y-6">
                    <p className="text-lg text-gray-700">
                        Tu copiloto financiero impulsado por inteligencia artificial está listo para ayudarte a:
                    </p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="flex items-start gap-3 p-4 bg-emerald-50 rounded-lg">
                            <span className="text-2xl">📊</span>
                            <div>
                                <h4 className="font-semibold text-gray-900">Analizar tus Finanzas</h4>
                                <p className="text-sm text-gray-600">Identifica patrones y oportunidades</p>
                            </div>
                        </div>
                        <div className="flex items-start gap-3 p-4 bg-green-50 rounded-lg">
                            <span className="text-2xl">🔮</span>
                            <div>
                                <h4 className="font-semibold text-gray-900">Predecir tu Futuro</h4>
                                <p className="text-sm text-gray-600">Proyecciones precisas con IA</p>
                            </div>
                        </div>
                        <div className="flex items-start gap-3 p-4 bg-green-50 rounded-lg">
                            <span className="text-2xl">💡</span>
                            <div>
                                <h4 className="font-semibold text-gray-900">Recibir Recomendaciones</h4>
                                <p className="text-sm text-gray-600">Consejos personalizados</p>
                            </div>
                        </div>
                        <div className="flex items-start gap-3 p-4 bg-orange-50 rounded-lg">
                            <span className="text-2xl">🎯</span>
                            <div>
                                <h4 className="font-semibold text-gray-900">Alcanzar tus Metas</h4>
                                <p className="text-sm text-gray-600">Planifica tu éxito financiero</p>
                            </div>
                        </div>
                    </div>
                </div>
            )
        },
        {
            title: 'Dashboard: Tu Centro de Control',
            subtitle: 'Visualiza toda tu información financiera en un solo lugar',
            icon: '📊',
            content: (
                <div className="space-y-6">
                    <div className="bg-gradient-to-r from-emerald-500 to-green-600 rounded-xl p-1">
                        <div className="bg-white rounded-lg p-6">
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                <div className="text-center p-4 bg-green-50 rounded-lg">
                                    <div className="text-2xl mb-2">💰</div>
                                    <div className="text-xs text-gray-600">Ingresos</div>
                                    <div className="text-lg font-bold text-green-600">$3,000,000</div>
                                </div>
                                <div className="text-center p-4 bg-red-50 rounded-lg">
                                    <div className="text-2xl mb-2">💸</div>
                                    <div className="text-xs text-gray-600">Gastos</div>
                                    <div className="text-lg font-bold text-red-600">$2,100,000</div>
                                </div>
                                <div className="text-center p-4 bg-emerald-50 rounded-lg">
                                    <div className="text-2xl mb-2">💳</div>
                                    <div className="text-xs text-gray-600">Balance</div>
                                    <div className="text-lg font-bold text-emerald-600">$900,000</div>
                                </div>
                                <div className="text-center p-4 bg-orange-50 rounded-lg">
                                    <div className="text-2xl mb-2">📊</div>
                                    <div className="text-xs text-gray-600">Ahorro</div>
                                    <div className="text-lg font-bold text-orange-600">30%</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="space-y-3">
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-emerald-100 rounded-full flex items-center justify-center text-emerald-600 font-bold">✓</div>
                            <p className="text-gray-700">Ve tus métricas financieras en tiempo real</p>
                        </div>
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-emerald-100 rounded-full flex items-center justify-center text-emerald-600 font-bold">✓</div>
                            <p className="text-gray-700">Accesos rápidos a todas las funciones</p>
                        </div>
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-emerald-100 rounded-full flex items-center justify-center text-emerald-600 font-bold">✓</div>
                            <p className="text-gray-700">Alertas importantes destacadas</p>
                        </div>
                    </div>
                </div>
            )
        },
        {
            title: 'Registra tus Transacciones',
            subtitle: 'Mantén un registro completo de ingresos y gastos',
            icon: '💳',
            content: (
                <div className="space-y-6">
                    <div className="bg-gray-50 rounded-xl p-6 border-2 border-dashed border-gray-300">
                        <div className="text-center mb-4">
                            <div className="text-4xl mb-2">💰</div>
                            <h4 className="font-bold text-gray-900">Registrar Ingreso</h4>
                        </div>
                        <div className="space-y-3 text-sm">
                            <div className="flex justify-between">
                                <span className="text-gray-600">Monto:</span>
                                <span className="font-semibold">$3,000,000</span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-gray-600">Tipo:</span>
                                <span className="font-semibold">Salario</span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-gray-600">Fecha:</span>
                                <span className="font-semibold">01/03/2024</span>
                            </div>
                        </div>
                    </div>
                    <div className="space-y-3">
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center text-green-600 font-bold">✓</div>
                            <p className="text-gray-700">Agrega ubicación, etiquetas y recurrencia</p>
                        </div>
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center text-green-600 font-bold">✓</div>
                            <p className="text-gray-700">Filtra y busca transacciones fácilmente</p>
                        </div>
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center text-green-600 font-bold">✓</div>
                            <p className="text-gray-700">Categoriza automáticamente tus gastos</p>
                        </div>
                    </div>
                </div>
            )
        },
        {
            title: 'Predicciones con IA',
            subtitle: 'Descubre qué te depara el futuro financiero',
            icon: '🔮',
            content: (
                <div className="space-y-6">
                    <div className="bg-gradient-to-r from-green-500 to-pink-600 rounded-xl p-6 text-white">
                        <div className="flex items-center gap-4 mb-4">
                            <div className="text-4xl">🤖</div>
                            <div>
                                <h4 className="font-bold text-lg">Predicción IA</h4>
                                <p className="text-sm opacity-90">Basado en tus patrones</p>
                            </div>
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <div className="text-sm opacity-90">Balance en 3 meses</div>
                                <div className="text-2xl font-bold">$2,700,000</div>
                            </div>
                            <div>
                                <div className="text-sm opacity-90">Confianza</div>
                                <div className="text-2xl font-bold">85%</div>
                            </div>
                        </div>
                    </div>
                    <div className="space-y-3">
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center text-green-600 font-bold">✓</div>
                            <p className="text-gray-700">Predicciones de balance futuro</p>
                        </div>
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center text-green-600 font-bold">✓</div>
                            <p className="text-gray-700">Análisis de riesgo financiero</p>
                        </div>
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center text-green-600 font-bold">✓</div>
                            <p className="text-gray-700">Recomendaciones personalizadas</p>
                        </div>
                    </div>
                </div>
            )
        },
        {
            title: 'Simulador de Escenarios',
            subtitle: 'Visualiza diferentes futuros antes de decidir',
            icon: '🎯',
            content: (
                <div className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="bg-emerald-50 p-4 rounded-lg border border-emerald-200">
                            <div className="text-2xl mb-2">📈</div>
                            <h4 className="font-semibold text-gray-900 mb-1">Situación Actual</h4>
                            <p className="text-sm text-gray-600 mb-2">Mantener hábitos actuales</p>
                            <div className="text-lg font-bold text-emerald-600">$900,000</div>
                            <p className="text-xs text-gray-500">En 12 meses</p>
                        </div>
                        <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                            <div className="text-2xl mb-2">🚀</div>
                            <h4 className="font-semibold text-gray-900 mb-1">Optimizado</h4>
                            <p className="text-sm text-gray-600 mb-2">Reducir gastos 10%</p>
                            <div className="text-lg font-bold text-green-600">$1,800,000</div>
                            <p className="text-xs text-gray-500">En 12 meses</p>
                        </div>
                    </div>
                    <div className="space-y-3">
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center text-orange-600 font-bold">✓</div>
                            <p className="text-gray-700">Compara 5 escenarios diferentes</p>
                        </div>
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center text-orange-600 font-bold">✓</div>
                            <p className="text-gray-700">Ve el impacto de tus decisiones</p>
                        </div>
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center text-orange-600 font-bold">✓</div>
                            <p className="text-gray-700">Recibe el mejor escenario recomendado</p>
                        </div>
                    </div>
                </div>
            )
        },
        {
            title: '¡Estás Listo para Comenzar!',
            subtitle: 'Empieza tu viaje hacia la libertad financiera',
            icon: '🚀',
            content: (
                <div className="space-y-6">
                    <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-xl p-8 text-white text-center">
                        <div className="text-6xl mb-4">🎉</div>
                        <h3 className="text-2xl font-bold mb-2">¡Todo Listo!</h3>
                        <p className="text-lg opacity-90">
                            Ya conoces las funciones principales de FINNOVA
                        </p>
                    </div>
                    <div className="bg-emerald-50 rounded-xl p-6 border border-emerald-200">
                        <h4 className="font-bold text-gray-900 mb-4">Próximos Pasos:</h4>
                        <div className="space-y-3">
                            <div className="flex items-center gap-3">
                                <div className="w-8 h-8 bg-emerald-600 text-white rounded-full flex items-center justify-center font-bold">1</div>
                                <p className="text-gray-700">Registra tus primeras transacciones</p>
                            </div>
                            <div className="flex items-center gap-3">
                                <div className="w-8 h-8 bg-emerald-600 text-white rounded-full flex items-center justify-center font-bold">2</div>
                                <p className="text-gray-700">Explora el dashboard y análisis</p>
                            </div>
                            <div className="flex items-center gap-3">
                                <div className="w-8 h-8 bg-emerald-600 text-white rounded-full flex items-center justify-center font-bold">3</div>
                                <p className="text-gray-700">Revisa tus predicciones y simulaciones</p>
                            </div>
                        </div>
                    </div>
                    <div className="text-center text-gray-600">
                        <p className="text-sm">
                            💡 Tip: Mientras más datos registres, más precisas serán las predicciones de la IA
                        </p>
                    </div>
                </div>
            )
        }
    ]

    const handleNext = () => {
        if (currentStep < steps.length - 1) {
            setCurrentStep(currentStep + 1)
        } else {
            localStorage.removeItem('isNewUser')
            router.push('/dashboard')
        }
    }

    const handleSkip = () => {
        localStorage.removeItem('isNewUser')
        router.push('/dashboard')
    }

    const handlePrevious = () => {
        if (currentStep > 0) {
            setCurrentStep(currentStep - 1)
        }
    }

    const progress = ((currentStep + 1) / steps.length) * 100

    return (
        <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-white to-green-50 flex items-center justify-center p-4">
            <div className="max-w-4xl w-full">
                {/* Progress Bar */}
                <div className="mb-8">
                    <div className="flex justify-between items-center mb-2">
                        <span className="text-sm font-medium text-gray-600">
                            Paso {currentStep + 1} de {steps.length}
                        </span>
                        <button
                            onClick={handleSkip}
                            className="text-sm text-gray-500 hover:text-gray-700 font-medium"
                        >
                            Saltar tutorial →
                        </button>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                            className="bg-gradient-to-r from-emerald-600 to-green-600 h-2 rounded-full transition-all duration-300"
                            style={{ width: `${progress}%` }}
                        />
                    </div>
                </div>

                {/* Content Card */}
                <div className="bg-white rounded-2xl shadow-2xl p-8 md:p-12 border border-gray-200">
                    <div className="text-center mb-8">
                        <div className="text-7xl mb-4">{steps[currentStep].icon}</div>
                        <h2 className="text-3xl font-bold text-gray-900 mb-2">
                            {steps[currentStep].title}
                        </h2>
                        <p className="text-lg text-gray-600">
                            {steps[currentStep].subtitle}
                        </p>
                    </div>

                    <div className="mb-8">
                        {steps[currentStep].content}
                    </div>

                    {/* Navigation Buttons */}
                    <div className="flex gap-4">
                        {currentStep > 0 && (
                            <button
                                onClick={handlePrevious}
                                className="px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:border-gray-400 transition"
                            >
                                ← Anterior
                            </button>
                        )}
                        <button
                            onClick={handleNext}
                            className="flex-1 bg-gradient-to-r from-emerald-600 to-green-600 text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-all transform hover:scale-105"
                        >
                            {currentStep === steps.length - 1 ? '¡Comenzar! 🚀' : 'Siguiente →'}
                        </button>
                    </div>
                </div>

                {/* Dots Indicator */}
                <div className="flex justify-center gap-2 mt-6">
                    {steps.map((_, index) => (
                        <button
                            key={index}
                            onClick={() => setCurrentStep(index)}
                            className={`w-2 h-2 rounded-full transition-all ${index === currentStep
                                ? 'bg-emerald-600 w-8'
                                : 'bg-gray-300 hover:bg-gray-400'
                                }`}
                        />
                    ))}
                </div>
            </div>
        </div>
    )
}

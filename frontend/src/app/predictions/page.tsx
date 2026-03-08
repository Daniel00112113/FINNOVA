'use client'

import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import ProtectedRoute from '@/components/ProtectedRoute'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

// Formato de moneda colombiana
const formatCOP = (amount: number) => {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount)
}

interface BalancePrediction {
    predictions: MonthlyPrediction[]
    confidence: number
    trend: string
    riskLevel: string
    recommendations: string[]
    currentBalance: number
}

interface MonthlyPrediction {
    month: string
    predictedBalance: number
    confidence: number
}

interface RiskAnalysis {
    riskScore: number
    riskLevel: string
    factors: string[]
    recommendations: string[]
    metrics: {
        expenseRatio: number
        volatility: number
        balance: number
    }
}

interface ExpensePrediction {
    predictions: CategoryPrediction[]
    totalPredicted: number
    confidence: number
    recommendations: string[]
}

interface CategoryPrediction {
    category: string
    predictedAmount: number
    confidence: number
    trend: string
}

export default function PredictionsPage() {
    const [prediction, setPrediction] = useState<BalancePrediction | null>(null)
    const [risk, setRisk] = useState<RiskAnalysis | null>(null)
    const [expensePrediction, setExpensePrediction] = useState<ExpensePrediction | null>(null)
    const [loading, setLoading] = useState(true)
    const [userId, setUserId] = useState<string>('')
    const [monthsAhead, setMonthsAhead] = useState(3)

    useEffect(() => {
        const id = localStorage.getItem('userId')
        if (id) {
            setUserId(id)
            loadPredictions(id, monthsAhead)
        }
    }, [monthsAhead])

    const loadPredictions = async (id: string, months: number) => {
        try {
            setLoading(true)
            const [predResponse, riskResponse, expenseResponse] = await Promise.all([
                api.get(`/users/${id}/predictions/balance?monthsAhead=${months}`),
                api.get(`/users/${id}/predictions/risk`),
                api.get(`/users/${id}/predictions/expenses?monthsAhead=${months}`)
            ])
            setPrediction(predResponse.data)
            setRisk(riskResponse.data)
            setExpensePrediction(expenseResponse.data)
        } catch (error) {
            console.error('Error loading predictions:', error)
        } finally {
            setLoading(false)
        }
    }

    if (loading) return <div className="p-8">Generando predicciones...</div>

    // Verificar si hay datos suficientes
    const hasLimitedData = !prediction || prediction.confidence < 0.7 || !risk || risk.riskScore === 0

    const getRiskColor = (level: string) => {
        switch (level) {
            case 'high': return 'text-red-600 bg-red-100'
            case 'medium': return 'text-yellow-600 bg-yellow-100'
            case 'low': return 'text-green-600 bg-green-100'
            default: return 'text-gray-600 bg-gray-100'
        }
    }

    const chartData = prediction?.predictions.map(p => ({
        month: p.month,
        balance: p.predictedBalance
    })) || []

    return (
        <ProtectedRoute>
            <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-4 md:p-8">
                <div className="w-full px-8">
                    <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
                        <div>
                            <h1 className="text-3xl md:text-4xl font-bold text-gray-800 mb-2">🔮 Predicciones Financieras</h1>
                            <p className="text-gray-600">Proyecciones inteligentes basadas en IA</p>
                        </div>
                        <select
                            value={monthsAhead}
                            onChange={(e) => setMonthsAhead(Number(e.target.value))}
                            className="px-6 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-green-500 focus:border-transparent font-semibold"
                        >
                            <option value={3}>📅 3 meses</option>
                            <option value={6}>📅 6 meses</option>
                            <option value={12}>📅 12 meses</option>
                        </select>
                    </div>

                    {/* Cómo funciona */}
                    <div className="bg-gradient-to-r from-green-500 to-pink-600 text-white p-6 rounded-lg shadow-lg mb-8">
                        <h2 className="text-2xl font-bold mb-4">🤖 ¿Cómo funciona la IA de predicción?</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                            <div className="flex items-start gap-3">
                                <span className="text-2xl">📊</span>
                                <div>
                                    <p className="font-bold mb-1">Análisis de patrones históricos</p>
                                    <p className="opacity-90">La IA analiza tus transacciones pasadas para identificar tendencias en ingresos y gastos</p>
                                </div>
                            </div>
                            <div className="flex items-start gap-3">
                                <span className="text-2xl">🧮</span>
                                <div>
                                    <p className="font-bold mb-1">Regresión lineal</p>
                                    <p className="opacity-90">Usa un modelo matemático para proyectar tu balance futuro basado en tu comportamiento</p>
                                </div>
                            </div>
                            <div className="flex items-start gap-3">
                                <span className="text-2xl">⚠️</span>
                                <div>
                                    <p className="font-bold mb-1">Análisis de riesgo</p>
                                    <p className="opacity-90">Evalúa tu ratio gastos/ingresos, volatilidad y balance para calcular tu nivel de riesgo financiero</p>
                                </div>
                            </div>
                            <div className="flex items-start gap-3">
                                <span className="text-2xl">🎯</span>
                                <div>
                                    <p className="font-bold mb-1">Confianza adaptativa</p>
                                    <p className="opacity-90">Más transacciones = mayor confianza. Con 6+ meses de datos alcanzamos 90% de confianza</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Alerta de datos limitados */}
                    {hasLimitedData && (
                        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-6 rounded-xl shadow-lg mb-8">
                            <div className="flex items-start gap-4">
                                <span className="text-5xl">⚠️</span>
                                <div className="flex-1">
                                    <h3 className="text-xl font-bold text-yellow-800 mb-3">Datos Limitados Detectados</h3>
                                    <p className="text-yellow-700 mb-4">
                                        Las predicciones actuales tienen baja confianza porque:
                                    </p>
                                    <ul className="list-disc list-inside text-yellow-700 space-y-2 mb-4">
                                        <li>Todas tus transacciones son del mismo mes</li>
                                        <li>El modelo necesita al menos 2-3 meses de historial para identificar patrones</li>
                                        <li>Sin datos temporales, las predicciones son estimaciones básicas</li>
                                    </ul>
                                    <div className="bg-white p-5 rounded-xl shadow-sm">
                                        <p className="font-bold text-gray-800 mb-3">💡 Para mejorar las predicciones:</p>
                                        <ol className="list-decimal list-inside text-gray-700 space-y-2">
                                            <li>Registra transacciones de meses anteriores (enero, febrero, etc.)</li>
                                            <li>Mantén un registro constante de ingresos y gastos cada mes</li>
                                            <li>Con 3+ meses de datos, la confianza subirá a 70%</li>
                                            <li>Con 6+ meses de datos, alcanzarás 90% de confianza</li>
                                        </ol>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {risk && (
                        <>
                            <div className="bg-white p-6 rounded-xl shadow-lg mb-8 border border-gray-200">
                                <h2 className="text-2xl font-bold mb-6 text-gray-800">📈 Métricas de Riesgo Financiero</h2>
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                    <div className="p-6 bg-gradient-to-br from-red-50 to-orange-50 rounded-xl border border-red-200">
                                        <h3 className="text-gray-700 text-sm mb-3 font-semibold">Score de Riesgo</h3>
                                        <div className="flex items-center gap-4 mb-3">
                                            <div className="text-5xl font-bold">{risk.riskScore}</div>
                                            <div className="flex-1">
                                                <div className="w-full bg-gray-200 rounded-full h-4">
                                                    <div
                                                        className={`h-4 rounded-full transition-all ${risk.riskScore >= 70 ? 'bg-red-500' :
                                                            risk.riskScore >= 40 ? 'bg-yellow-500' :
                                                                'bg-green-500'
                                                            }`}
                                                        style={{ width: `${risk.riskScore}%` }}
                                                    />
                                                </div>
                                            </div>
                                        </div>
                                        <p className="text-xs text-gray-600">
                                            0-39: Bajo riesgo | 40-69: Riesgo medio | 70-100: Alto riesgo
                                        </p>
                                    </div>

                                    <div className="p-6 bg-gradient-to-br from-yellow-50 to-amber-50 rounded-xl border border-yellow-200">
                                        <h3 className="text-gray-700 text-sm mb-3 font-semibold">Nivel de Riesgo</h3>
                                        <span className={`inline-block px-4 py-2 rounded-full text-lg font-bold ${getRiskColor(risk.riskLevel)}`}>
                                            {risk.riskLevel === 'high' ? '🔴 ALTO' : risk.riskLevel === 'medium' ? '🟡 MEDIO' : '🟢 BAJO'}
                                        </span>
                                        <p className="text-xs text-gray-600 mt-3">
                                            {risk.riskLevel === 'high' && 'Requiere atención inmediata'}
                                            {risk.riskLevel === 'medium' && 'Monitorea y ajusta tus hábitos'}
                                            {risk.riskLevel === 'low' && 'Situación financiera saludable'}
                                        </p>
                                    </div>

                                    <div className="p-6 bg-gradient-to-br from-emerald-50 to-indigo-50 rounded-xl border border-emerald-200">
                                        <h3 className="text-gray-700 text-sm mb-3 font-semibold">Ratio Gastos/Ingresos</h3>
                                        <p className="text-4xl font-bold mb-2">
                                            {(risk.metrics.expenseRatio * 100).toFixed(1)}%
                                        </p>
                                        <p className="text-xs text-gray-600">
                                            Ideal: &lt;70% | Aceptable: 70-80% | Riesgoso: &gt;80%
                                        </p>
                                        <div className="mt-2 text-xs">
                                            {risk.metrics.expenseRatio > 0.8 ? '⚠️ Gastas demasiado' :
                                                risk.metrics.expenseRatio > 0.7 ? '⚡ Ajusta un poco' :
                                                    '✅ Excelente control'}
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div className="bg-white p-6 rounded-xl shadow-lg mb-8 border border-gray-200">
                                <h2 className="text-2xl font-bold mb-6 text-gray-800">📊 Métricas Adicionales</h2>
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                    <div className="p-5 bg-gradient-to-br from-green-50 to-green-100 rounded-xl border border-green-200">
                                        <p className="text-sm text-gray-600 mb-1">Volatilidad de Gastos</p>
                                        <p className="text-2xl font-bold text-green-600">
                                            {(risk.metrics.volatility * 100).toFixed(1)}%
                                        </p>
                                        <p className="text-xs text-gray-500 mt-1">
                                            Qué tan variables son tus gastos mes a mes
                                        </p>
                                    </div>
                                    <div className="p-5 bg-gradient-to-br from-green-50 to-green-100 rounded-xl border border-green-200">
                                        <p className="text-sm text-gray-600 mb-2 font-medium">Balance Neto</p>
                                        <p className="text-2xl font-bold text-green-600">
                                            {formatCOP(risk.metrics.balance)}
                                        </p>
                                        <p className="text-xs text-gray-500 mt-1">
                                            Total de ingresos menos gastos
                                        </p>
                                    </div>
                                    <div className="p-5 bg-gradient-to-br from-emerald-50 to-emerald-100 rounded-xl border border-emerald-200">
                                        <p className="text-sm text-gray-600 mb-2 font-medium">Confianza de Predicción</p>
                                        <p className="text-2xl font-bold text-emerald-600">
                                            {prediction ? (prediction.confidence * 100).toFixed(0) : 0}%
                                        </p>
                                        <p className="text-xs text-gray-500 mt-1">
                                            Basado en cantidad de datos históricos
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </>
                    )}

                    {prediction && (
                        <>
                            <div className="bg-white p-6 rounded-xl shadow-lg mb-8 border border-gray-200">
                                <h2 className="text-2xl font-bold mb-6 text-gray-800">🔮 Proyección de Balance Futuro</h2>
                                <p className="text-gray-600 mb-6">
                                    Basado en tus patrones de ingresos y gastos, así es como podría evolucionar tu balance en los próximos {monthsAhead} meses:
                                </p>

                                <div className="mb-6 grid grid-cols-1 md:grid-cols-4 gap-4">
                                    <div className="p-5 bg-gradient-to-br from-emerald-50 to-emerald-100 rounded-xl border border-emerald-200">
                                        <span className="text-gray-600 text-sm block mb-1">Balance Actual</span>
                                        <span className="text-2xl font-bold text-emerald-600">{formatCOP(prediction.currentBalance)}</span>
                                        <p className="text-xs text-gray-500 mt-1">Tu balance hoy</p>
                                    </div>
                                    <div className="p-5 bg-gradient-to-br from-green-50 to-green-100 rounded-xl border border-green-200">
                                        <span className="text-gray-600 text-sm block mb-2 font-medium">Balance Proyectado</span>
                                        <span className="text-2xl font-bold text-green-600">
                                            {prediction.predictions.length > 0 ? formatCOP(prediction.predictions[prediction.predictions.length - 1].predictedBalance) : '$0'}
                                        </span>
                                        <p className="text-xs text-gray-500 mt-1">En {monthsAhead} meses</p>
                                    </div>
                                    <div className="p-5 bg-gradient-to-br from-green-50 to-green-100 rounded-xl border border-green-200">
                                        <span className="text-gray-600 text-sm block mb-2 font-medium">Tendencia</span>
                                        <span className={`text-xl font-bold ${prediction.trend === 'increasing' ? 'text-green-600' : 'text-red-600'
                                            }`}>
                                            {prediction.trend === 'increasing' ? '📈 Creciente' : '📉 Decreciente'}
                                        </span>
                                        <p className="text-xs text-gray-500 mt-1">
                                            {prediction.trend === 'increasing' ? 'Tu balance aumentará' : 'Tu balance disminuirá'}
                                        </p>
                                    </div>
                                    <div className="p-5 bg-gradient-to-br from-orange-50 to-orange-100 rounded-xl border border-orange-200">
                                        <span className="text-gray-600 text-sm block mb-2 font-medium">Cambio Esperado</span>
                                        <span className={`text-2xl font-bold ${prediction.predictions.length > 0 &&
                                            prediction.predictions[prediction.predictions.length - 1].predictedBalance > prediction.currentBalance
                                            ? 'text-green-600' : 'text-red-600'
                                            }`}>
                                            {prediction.predictions.length > 0
                                                ? formatCOP(prediction.predictions[prediction.predictions.length - 1].predictedBalance - prediction.currentBalance)
                                                : '$0'}
                                        </span>
                                        <p className="text-xs text-gray-500 mt-1">Diferencia total</p>
                                    </div>
                                </div>

                                <ResponsiveContainer width="100%" height={400}>
                                    <LineChart data={chartData}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                                        <XAxis
                                            dataKey="month"
                                            style={{ fontSize: '12px' }}
                                            label={{ value: 'Mes', position: 'insideBottom', offset: -5 }}
                                        />
                                        <YAxis
                                            tickFormatter={(value) => formatCOP(value)}
                                            style={{ fontSize: '12px' }}
                                            label={{ value: 'Balance', angle: -90, position: 'insideLeft' }}
                                        />
                                        <Tooltip
                                            formatter={(value: number) => [formatCOP(value), 'Balance Predicho']}
                                            labelStyle={{ color: '#000' }}
                                            contentStyle={{ backgroundColor: '#fff', border: '1px solid #ccc', borderRadius: '8px' }}
                                        />
                                        <Legend wrapperStyle={{ paddingTop: '20px' }} />
                                        <Line
                                            type="monotone"
                                            dataKey="balance"
                                            stroke="#8b5cf6"
                                            strokeWidth={3}
                                            name="Balance Predicho"
                                            dot={{ fill: '#8b5cf6', r: 6 }}
                                            activeDot={{ r: 8 }}
                                        />
                                    </LineChart>
                                </ResponsiveContainer>

                                <div className="mt-6 p-5 bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl border border-gray-200">
                                    <p className="text-sm text-gray-600">
                                        <span className="font-bold">💡 Nota:</span> Esta predicción se basa en tus patrones históricos.
                                        Los resultados reales pueden variar según cambios en tus ingresos, gastos o situación financiera.
                                        Confianza actual: <span className="font-bold text-emerald-600">{(prediction.confidence * 100).toFixed(0)}%</span>
                                    </p>
                                </div>
                            </div>

                            {/* Predicción de Gastos por Categoría */}
                            {expensePrediction && (
                                <div className="bg-white p-6 rounded-xl shadow-lg mb-8 border border-gray-200">
                                    <h2 className="text-2xl font-bold mb-6 text-gray-800">📊 Predicción de Gastos por Categoría</h2>
                                    <p className="text-gray-600 mb-6">
                                        Estimación de cuánto gastarás en cada categoría en los próximos {monthsAhead} meses:
                                    </p>

                                    <div className="mb-6 p-5 bg-gradient-to-r from-green-50 to-pink-50 rounded-xl border border-green-200">
                                        <div className="flex items-center justify-between">
                                            <div>
                                                <p className="text-sm text-gray-600 mb-1 font-medium">Total Predicho</p>
                                                <p className="text-3xl font-bold text-green-600">{formatCOP(expensePrediction.totalPredicted)}</p>
                                            </div>
                                            <div className="text-right">
                                                <p className="text-sm text-gray-600 mb-1 font-medium">Confianza</p>
                                                <p className="text-3xl font-bold text-emerald-600">{(expensePrediction.confidence * 100).toFixed(0)}%</p>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
                                        {expensePrediction.predictions && expensePrediction.predictions.length > 0 ? (
                                            expensePrediction.predictions.map((cat, index) => (
                                                <div
                                                    key={index}
                                                    className="p-5 bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl border border-gray-200 hover:shadow-lg transition-all"
                                                >
                                                    <div className="flex items-center justify-between mb-3">
                                                        <h3 className="font-bold text-gray-800">{cat.category}</h3>
                                                        <span className={`text-2xl ${cat.trend === 'increasing' ? '📈' :
                                                            cat.trend === 'decreasing' ? '📉' : '➡️'
                                                            }`}>
                                                            {cat.trend === 'increasing' ? '📈' :
                                                                cat.trend === 'decreasing' ? '📉' : '➡️'}
                                                        </span>
                                                    </div>
                                                    <p className="text-2xl font-bold text-green-600 mb-2">
                                                        {formatCOP(cat.predictedAmount)}
                                                    </p>
                                                    <div className="flex items-center justify-between text-sm">
                                                        <span className="text-gray-600">Confianza</span>
                                                        <span className="font-semibold text-emerald-600">
                                                            {(cat.confidence * 100).toFixed(0)}%
                                                        </span>
                                                    </div>
                                                    <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                                                        <div
                                                            className="bg-emerald-500 h-2 rounded-full transition-all"
                                                            style={{ width: `${cat.confidence * 100}%` }}
                                                        />
                                                    </div>
                                                </div>
                                            ))
                                        ) : (
                                            <div className="col-span-full text-center py-8">
                                                <p className="text-gray-500">No hay suficientes datos para predecir gastos por categoría</p>
                                            </div>
                                        )}
                                    </div>

                                    {expensePrediction.recommendations && expensePrediction.recommendations.length > 0 && (
                                        <div className="bg-gradient-to-r from-yellow-50 to-orange-50 p-5 rounded-xl border border-yellow-200">
                                            <h3 className="font-bold text-gray-800 mb-3">💡 Recomendaciones</h3>
                                            <div className="space-y-2">
                                                {expensePrediction.recommendations.map((rec, idx) => (
                                                    <p key={idx} className="text-gray-700 flex items-start gap-2">
                                                        <span className="text-yellow-600">•</span>
                                                        <span>{rec}</span>
                                                    </p>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            )}

                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                                <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
                                    <h2 className="text-2xl font-bold mb-6 text-gray-800">💡 Recomendaciones IA</h2>
                                    <div className="space-y-3">
                                        {prediction.recommendations.map((rec, index) => (
                                            <div key={index} className="flex items-start gap-4 p-4 bg-gradient-to-r from-emerald-50 to-emerald-100 rounded-xl border border-emerald-200 hover:shadow-md transition-shadow">
                                                <span className="text-2xl">💡</span>
                                                <p className="flex-1 text-gray-700">{rec}</p>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                {risk && (
                                    <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
                                        <h2 className="text-2xl font-bold mb-6 text-gray-800">⚠️ Factores de Riesgo</h2>
                                        <div className="space-y-3">
                                            {risk.factors.length > 0 ? (
                                                risk.factors.map((factor, index) => (
                                                    <div key={index} className="flex items-start gap-4 p-4 bg-gradient-to-r from-red-50 to-red-100 rounded-xl border border-red-200 hover:shadow-md transition-shadow">
                                                        <span className="text-2xl">⚠️</span>
                                                        <p className="flex-1 text-gray-700">{factor}</p>
                                                    </div>
                                                ))
                                            ) : (
                                                <div className="flex items-start gap-4 p-4 bg-gradient-to-r from-green-50 to-green-100 rounded-xl border border-green-200">
                                                    <span className="text-2xl">✅</span>
                                                    <p className="flex-1 text-gray-700">No se detectaron factores de riesgo significativos</p>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                )}
                            </div>
                        </>
                    )}
                </div>
            </div>
        </ProtectedRoute>
    )
}

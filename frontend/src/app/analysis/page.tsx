'use client'

import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import ProtectedRoute from '@/components/ProtectedRoute'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts'

interface SpendingAnalysis {
    spendingByCategory: Record<string, number>
    monthlyTrends: Record<string, number>
    insights: CategoryInsight[]
    averageDailySpending: number
    topCategory: string
}

interface CategoryInsight {
    category: string
    amount: number
    percentageOfTotal: number
    trend: string
    recommendation: string
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D']

export default function AnalysisPage() {
    const [analysis, setAnalysis] = useState<SpendingAnalysis | null>(null)
    const [loading, setLoading] = useState(true)
    const [userId, setUserId] = useState<string>('')

    useEffect(() => {
        const id = localStorage.getItem('userId')
        if (id) {
            setUserId(id)
            loadAnalysis(id)
        }
    }, [])

    const loadAnalysis = async (id: string) => {
        try {
            setLoading(true)
            await api.post(`/users/${id}/analysis/analyze`)
            const response = await api.get(`/users/${id}/analysis/spending`)
            setAnalysis(response.data)
        } catch (error) {
            console.error('Error loading analysis:', error)
        } finally {
            setLoading(false)
        }
    }

    if (loading) return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center">
            <div className="text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500 mx-auto mb-4"></div>
                <p className="text-gray-600">Analizando tus gastos...</p>
            </div>
        </div>
    )

    if (!analysis) return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center">
            <div className="text-center">
                <span className="text-6xl block mb-4">📊</span>
                <p className="text-gray-600 text-lg">No hay datos suficientes para analizar</p>
                <a href="/transactions" className="inline-block mt-4 px-6 py-3 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600">
                    Registrar transacciones
                </a>
            </div>
        </div>
    )

    const categoryData = Object.entries(analysis.spendingByCategory).map(([name, value]) => ({
        name,
        value
    }))

    const monthlyData = Object.entries(analysis.monthlyTrends).map(([month, amount]) => ({
        month,
        amount
    }))

    return (
        <ProtectedRoute>
            <div className="min-h-screen bg-gray-100 p-3 sm:p-4 md:p-8">
                <div className="w-full max-w-7xl mx-auto">
                    <div className="mb-6 md:mb-8">
                        <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900">Análisis de Gastos</h1>
                        <p className="text-sm sm:text-base text-gray-600 mt-1 sm:mt-2">Insights inteligentes sobre tus patrones de gasto</p>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 sm:gap-4 md:gap-6 mb-6 md:mb-8">
                        <div className="bg-gradient-to-br from-emerald-500 to-emerald-600 p-4 sm:p-5 md:p-6 rounded-lg md:rounded-xl shadow-lg text-white">
                            <div className="flex items-center justify-between mb-2">
                                <h3 className="text-emerald-100 text-xs sm:text-sm font-medium">Gasto Diario Promedio</h3>
                                <span className="text-2xl sm:text-3xl">💵</span>
                            </div>
                            <p className="text-2xl sm:text-3xl font-bold break-words">
                                ${analysis.averageDailySpending.toLocaleString('es-CO', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}
                            </p>
                            <p className="text-emerald-100 text-xs mt-1 sm:mt-2">Por día</p>
                        </div>

                        <div className="bg-gradient-to-br from-green-500 to-green-600 p-4 sm:p-5 md:p-6 rounded-lg md:rounded-xl shadow-lg text-white">
                            <div className="flex items-center justify-between mb-2">
                                <h3 className="text-green-100 text-xs sm:text-sm font-medium">Categoría Principal</h3>
                                <span className="text-2xl sm:text-3xl">🏆</span>
                            </div>
                            <p className="text-xl sm:text-2xl font-bold truncate">{analysis.topCategory}</p>
                            <p className="text-green-100 text-xs mt-1 sm:mt-2">Mayor gasto</p>
                        </div>

                        <div className="bg-gradient-to-br from-green-500 to-green-600 p-4 sm:p-5 md:p-6 rounded-lg md:rounded-xl shadow-lg text-white sm:col-span-2 md:col-span-1">
                            <div className="flex items-center justify-between mb-2">
                                <h3 className="text-green-100 text-xs sm:text-sm font-medium">Total de Categorías</h3>
                                <span className="text-2xl sm:text-3xl">📂</span>
                            </div>
                            <p className="text-2xl sm:text-3xl font-bold">
                                {Object.keys(analysis.spendingByCategory).length}
                            </p>
                            <p className="text-green-100 text-xs mt-1 sm:mt-2">Categorías activas</p>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 md:gap-8 mb-6 md:mb-8">
                        <div className="bg-white p-4 sm:p-5 md:p-6 rounded-lg md:rounded-xl shadow-lg">
                            <h2 className="text-lg sm:text-xl md:text-2xl font-bold mb-3 sm:mb-4 text-gray-900">Gastos por Categoría</h2>
                            <ResponsiveContainer width="100%" height={250} className="sm:h-[300px]">
                                <PieChart>
                                    <Pie
                                        data={categoryData}
                                        cx="50%"
                                        cy="50%"
                                        labelLine={false}
                                        label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                                        outerRadius={80}
                                        fill="#8884d8"
                                        dataKey="value"
                                    >
                                        {categoryData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Pie>
                                    <Tooltip formatter={(value: number) => `$${value.toLocaleString('es-CO')}`} />
                                </PieChart>
                            </ResponsiveContainer>
                        </div>

                        <div className="bg-white p-4 sm:p-5 md:p-6 rounded-lg md:rounded-xl shadow-lg">
                            <h2 className="text-lg sm:text-xl md:text-2xl font-bold mb-3 sm:mb-4 text-gray-900">Tendencia Mensual</h2>
                            <ResponsiveContainer width="100%" height={250} className="sm:h-[300px]">
                                <BarChart data={monthlyData}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                                    <XAxis dataKey="month" style={{ fontSize: '12px' }} />
                                    <YAxis tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`} style={{ fontSize: '12px' }} />
                                    <Tooltip formatter={(value: number) => `$${value.toLocaleString('es-CO')}`} />
                                    <Bar dataKey="amount" fill="#8b5cf6" radius={[8, 8, 0, 0]} />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    <div className="bg-white p-4 sm:p-5 md:p-6 rounded-lg md:rounded-xl shadow-lg">
                        <h2 className="text-lg sm:text-xl md:text-2xl font-bold mb-4 sm:mb-6 text-gray-900">💡 Insights y Recomendaciones</h2>
                        <div className="space-y-3 sm:space-y-4">
                            {analysis.insights.map((insight, index) => (
                                <div key={index} className="border-l-4 border-emerald-500 pl-3 sm:pl-4 py-2 sm:py-3 bg-emerald-50 rounded-r-lg">
                                    <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-2 mb-2">
                                        <h3 className="font-bold text-base sm:text-lg text-gray-900">{insight.category}</h3>
                                        <span className={`px-2 sm:px-3 py-1 rounded-full text-xs sm:text-sm font-semibold inline-block ${insight.trend === 'High' ? 'bg-red-100 text-red-800' :
                                            insight.trend === 'Low' ? 'bg-green-100 text-green-800' :
                                                'bg-gray-100 text-gray-800'
                                            }`}>
                                            {insight.trend === 'High' ? '📈 Alto' :
                                                insight.trend === 'Low' ? '📉 Bajo' :
                                                    '➡️ Normal'}
                                        </span>
                                    </div>
                                    <p className="text-sm sm:text-base text-gray-700 mb-2 font-medium break-words">
                                        ${insight.amount.toLocaleString('es-CO', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}
                                        <span className="text-gray-500 ml-2">({insight.percentageOfTotal.toFixed(1)}% del total)</span>
                                    </p>
                                    {insight.recommendation && (
                                        <p className="text-xs sm:text-sm text-blue-700 bg-emerald-100 p-2 rounded">
                                            💡 {insight.recommendation}
                                        </p>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </ProtectedRoute>
    )
}

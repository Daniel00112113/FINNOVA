'use client'

import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import ProtectedRoute from '@/components/ProtectedRoute'

const formatCOP = (amount: number) => {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount)
}

interface Debt {
    id: string
    description: string
    totalAmount: number
    remainingAmount: number
    interestRate: number
    startDate: string
    endDate: string | null
}

export default function DebtsPage() {
    const [userId, setUserId] = useState<string>('')
    const [debts, setDebts] = useState<Debt[]>([])
    const [loading, setLoading] = useState(true)
    const [showForm, setShowForm] = useState(false)
    const [showPaymentModal, setShowPaymentModal] = useState(false)
    const [selectedDebt, setSelectedDebt] = useState<Debt | null>(null)
    const [paymentAmount, setPaymentAmount] = useState('')
    const [formData, setFormData] = useState({
        description: '',
        totalAmount: '',
        interestRate: ''
    })

    useEffect(() => {
        const id = localStorage.getItem('userId')
        if (id) {
            setUserId(id)
            loadDebts(id)
        }
    }, [])

    const loadDebts = async (id: string) => {
        try {
            setLoading(true)
            const response = await api.get(`/users/${id}/debts`)
            setDebts(response.data)
        } catch (error) {
            console.error('Error loading debts:', error)
        } finally {
            setLoading(false)
        }
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            await api.post(`/users/${userId}/debts`, {
                description: formData.description,
                totalAmount: parseFloat(formData.totalAmount),
                interestRate: parseFloat(formData.interestRate)
            })
            alert('Deuda registrada exitosamente')
            setShowForm(false)
            setFormData({
                description: '',
                totalAmount: '',
                interestRate: ''
            })
            loadDebts(userId)
        } catch (error) {
            alert('Error al registrar deuda')
        }
    }

    const handlePayment = async () => {
        if (!selectedDebt || !paymentAmount) return

        try {
            await api.put(`/users/${userId}/debts/${selectedDebt.id}/payment`, {
                amount: parseFloat(paymentAmount)
            })
            alert('Pago registrado exitosamente')
            setShowPaymentModal(false)
            setSelectedDebt(null)
            setPaymentAmount('')
            loadDebts(userId)
        } catch (error) {
            alert('Error al registrar pago')
        }
    }

    const handleDelete = async (debtId: string) => {
        if (!confirm('¿Estás seguro de eliminar esta deuda?')) return

        try {
            await api.delete(`/users/${userId}/debts/${debtId}`)
            alert('Deuda eliminada')
            loadDebts(userId)
        } catch (error) {
            alert('Error al eliminar deuda')
        }
    }

    const calculateProgress = (debt: Debt) => {
        const paid = debt.totalAmount - debt.remainingAmount
        return (paid / debt.totalAmount) * 100
    }

    const calculateMonthlyPayment = (debt: Debt) => {
        // Calcular pago mensual sugerido (5% del saldo restante)
        return debt.remainingAmount * 0.05
    }

    const calculateMonthlyInterest = (debt: Debt) => {
        // Calcular interés mensual (tasa anual / 12)
        const monthlyRate = debt.interestRate / 100 / 12
        return debt.remainingAmount * monthlyRate
    }

    const calculateMonthsToPayOff = (debt: Debt) => {
        const monthlyPayment = calculateMonthlyPayment(debt)
        if (monthlyPayment <= 0) return Infinity
        return Math.ceil(debt.remainingAmount / monthlyPayment)
    }

    const totalDebt = debts.reduce((sum, debt) => sum + debt.remainingAmount, 0)
    const totalOriginal = debts.reduce((sum, debt) => sum + debt.totalAmount, 0)
    const totalPaid = totalOriginal - totalDebt

    return (
        <ProtectedRoute>
            <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-3 sm:p-4 md:p-8">
                <div className="w-full max-w-7xl mx-auto">
                    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 md:mb-8 gap-3 sm:gap-4">
                        <div>
                            <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-800 mb-1 sm:mb-2">💳 Gestión de Deudas</h1>
                            <p className="text-sm sm:text-base text-gray-600">Controla y reduce tus deudas de forma inteligente</p>
                        </div>
                        <button
                            onClick={() => setShowForm(true)}
                            className="w-full sm:w-auto bg-gradient-to-r from-emerald-500 to-emerald-600 text-white px-4 sm:px-6 py-2 sm:py-3 rounded-lg shadow-lg hover:shadow-xl transition-all transform hover:scale-105 font-semibold text-sm sm:text-base"
                        >
                            + Nueva Deuda
                        </button>
                    </div>

                    {/* Resumen */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 sm:gap-5 md:gap-6 mb-6 md:mb-8">
                        <div className="bg-white p-4 sm:p-5 md:p-6 rounded-lg md:rounded-xl shadow-lg border border-gray-200">
                            <div className="flex items-center justify-between mb-2">
                                <h3 className="text-gray-600 text-xs sm:text-sm font-medium">Deuda Total</h3>
                                <span className="text-2xl sm:text-3xl">💰</span>
                            </div>
                            <p className="text-2xl sm:text-3xl font-bold text-red-600 break-words">{formatCOP(totalDebt)}</p>
                            <p className="text-xs sm:text-sm text-gray-500 mt-1">{debts.length} deuda(s) activa(s)</p>
                        </div>

                        <div className="bg-white p-4 sm:p-5 md:p-6 rounded-lg md:rounded-xl shadow-lg border border-gray-200">
                            <div className="flex items-center justify-between mb-2">
                                <h3 className="text-gray-600 text-xs sm:text-sm font-medium">Total Pagado</h3>
                                <span className="text-2xl sm:text-3xl">✅</span>
                            </div>
                            <p className="text-2xl sm:text-3xl font-bold text-green-600 break-words">{formatCOP(totalPaid)}</p>
                            <p className="text-xs sm:text-sm text-gray-500 mt-1">
                                {totalOriginal > 0 ? ((totalPaid / totalOriginal) * 100).toFixed(1) : 0}% del total
                            </p>
                        </div>

                        <div className="bg-white p-4 sm:p-5 md:p-6 rounded-lg md:rounded-xl shadow-lg border border-gray-200 sm:col-span-2 md:col-span-1">
                            <div className="flex items-center justify-between mb-2">
                                <h3 className="text-gray-600 text-xs sm:text-sm font-medium">Deuda Original</h3>
                                <span className="text-2xl sm:text-3xl">📊</span>
                            </div>
                            <p className="text-2xl sm:text-3xl font-bold text-gray-800 break-words">{formatCOP(totalOriginal)}</p>
                            <p className="text-xs sm:text-sm text-gray-500 mt-1">Monto inicial total</p>
                        </div>
                    </div>

                    {/* Formulario */}
                    {showForm && (
                        <div className="bg-white p-6 rounded-xl shadow-lg mb-8 border border-gray-200">
                            <div className="flex justify-between items-center mb-6">
                                <h2 className="text-2xl font-bold text-gray-800">💳 Nueva Deuda</h2>
                                <button
                                    onClick={() => setShowForm(false)}
                                    className="text-gray-400 hover:text-gray-600 text-2xl"
                                >
                                    ×
                                </button>
                            </div>

                            <form onSubmit={handleSubmit} className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium mb-1">Descripción de la Deuda</label>
                                    <input
                                        type="text"
                                        value={formData.description}
                                        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                        className="w-full p-3 border rounded-lg"
                                        placeholder="Ej: Tarjeta de Crédito Bancolombia, Préstamo Personal"
                                        required
                                    />
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium mb-1">Monto Total</label>
                                        <input
                                            type="number"
                                            step="0.01"
                                            value={formData.totalAmount}
                                            onChange={(e) => setFormData({ ...formData, totalAmount: e.target.value })}
                                            className="w-full p-3 border rounded-lg"
                                            required
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-sm font-medium mb-1">Tasa de Interés Anual (%)</label>
                                        <input
                                            type="number"
                                            step="0.01"
                                            value={formData.interestRate}
                                            onChange={(e) => setFormData({ ...formData, interestRate: e.target.value })}
                                            className="w-full p-3 border rounded-lg"
                                            placeholder="Ej: 24.5"
                                            required
                                        />
                                    </div>
                                </div>

                                <div className="flex gap-4">
                                    <button
                                        type="submit"
                                        className="flex-1 bg-gradient-to-r from-emerald-500 to-emerald-600 text-white py-3 rounded-lg hover:shadow-lg transition-all font-semibold"
                                    >
                                        💾 Guardar
                                    </button>
                                    <button
                                        type="button"
                                        onClick={() => setShowForm(false)}
                                        className="flex-1 bg-gray-200 text-gray-700 py-3 rounded-lg hover:bg-gray-300 transition-all font-semibold"
                                    >
                                        Cancelar
                                    </button>
                                </div>
                            </form>
                        </div>
                    )}

                    {/* Lista de Deudas */}
                    <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
                        <div className="p-6 bg-gradient-to-r from-red-500 to-orange-600 text-white">
                            <h2 className="text-2xl font-bold">📋 Tus Deudas</h2>
                            <p className="text-sm opacity-90 mt-1">
                                {debts.length} deuda(s) registrada(s)
                            </p>
                        </div>

                        {loading ? (
                            <div className="p-12 text-center">
                                <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-red-500"></div>
                                <p className="mt-4 text-gray-600">Cargando deudas...</p>
                            </div>
                        ) : debts.length === 0 ? (
                            <div className="p-12 text-center">
                                <span className="text-6xl mb-4 block">🎉</span>
                                <p className="text-xl text-gray-600 mb-2">¡No tienes deudas registradas!</p>
                                <p className="text-gray-500">Registra una deuda para comenzar a gestionarla</p>
                            </div>
                        ) : (
                            <div className="divide-y divide-gray-200">
                                {debts.map((debt) => {
                                    const progress = calculateProgress(debt)
                                    const monthlyPayment = calculateMonthlyPayment(debt)
                                    const monthlyInterest = calculateMonthlyInterest(debt)
                                    const monthsLeft = calculateMonthsToPayOff(debt)
                                    const isPaid = debt.endDate !== null

                                    return (
                                        <div key={debt.id} className={`p-6 hover:bg-gray-50 transition-colors ${isPaid ? 'opacity-60' : ''}`}>
                                            <div className="flex flex-col md:flex-row justify-between gap-4">
                                                <div className="flex-1">
                                                    <div className="flex items-center gap-3 mb-3">
                                                        <h3 className="text-xl font-bold text-gray-800">{debt.description}</h3>
                                                        <span className="px-3 py-1 bg-red-100 text-red-700 rounded-full text-xs font-semibold">
                                                            {debt.interestRate}% anual
                                                        </span>
                                                        {isPaid && (
                                                            <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-semibold">
                                                                ✅ Pagada
                                                            </span>
                                                        )}
                                                    </div>

                                                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                                                        <div>
                                                            <p className="text-xs text-gray-500">Deuda Restante</p>
                                                            <p className="text-lg font-bold text-red-600">{formatCOP(debt.remainingAmount)}</p>
                                                        </div>
                                                        <div>
                                                            <p className="text-xs text-gray-500">Deuda Original</p>
                                                            <p className="text-lg font-bold text-gray-700">{formatCOP(debt.totalAmount)}</p>
                                                        </div>
                                                        <div>
                                                            <p className="text-xs text-gray-500">Interés Mensual</p>
                                                            <p className="text-lg font-bold text-orange-600">{formatCOP(monthlyInterest)}</p>
                                                            <p className="text-xs text-gray-500">{(debt.interestRate / 12).toFixed(2)}% del saldo</p>
                                                        </div>
                                                        <div>
                                                            <p className="text-xs text-gray-500">Pago Sugerido</p>
                                                            <p className="text-lg font-bold text-emerald-600">{formatCOP(monthlyPayment)}</p>
                                                            <p className="text-xs text-gray-500">5% del saldo</p>
                                                        </div>
                                                    </div>

                                                    <div className="mb-3 p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                                                        <p className="text-sm text-gray-700">
                                                            💡 <span className="font-semibold">Fecha de inicio:</span> {new Date(debt.startDate).toLocaleDateString('es-CO')}
                                                        </p>
                                                        {!isPaid && (
                                                            <p className="text-sm text-gray-700 mt-1">
                                                                ⚠️ Cada mes se genera <span className="font-bold text-orange-600">{formatCOP(monthlyInterest)}</span> de interés
                                                            </p>
                                                        )}
                                                    </div>

                                                    <div className="mb-3">
                                                        <div className="flex justify-between text-sm mb-1">
                                                            <span className="text-gray-600">Progreso de Pago</span>
                                                            <span className="font-semibold text-green-600">{progress.toFixed(1)}%</span>
                                                        </div>
                                                        <div className="w-full bg-gray-200 rounded-full h-3">
                                                            <div
                                                                className="bg-gradient-to-r from-green-500 to-green-600 h-3 rounded-full transition-all"
                                                                style={{ width: `${progress}%` }}
                                                            />
                                                        </div>
                                                    </div>

                                                    {!isPaid && monthsLeft !== Infinity && (
                                                        <p className="text-sm text-gray-600">
                                                            ⏱️ Aproximadamente {monthsLeft} mes(es) para pagar con el pago sugerido
                                                        </p>
                                                    )}
                                                    {isPaid && debt.endDate && (
                                                        <p className="text-sm text-green-600 font-semibold">
                                                            🎉 Pagada completamente el {new Date(debt.endDate).toLocaleDateString('es-CO')}
                                                        </p>
                                                    )}
                                                </div>

                                                <div className="flex md:flex-col gap-2">
                                                    {!isPaid && (
                                                        <button
                                                            onClick={() => {
                                                                setSelectedDebt(debt)
                                                                setShowPaymentModal(true)
                                                            }}
                                                            className="flex-1 md:flex-none bg-gradient-to-r from-green-500 to-green-600 text-white px-4 py-2 rounded-lg hover:shadow-lg transition-all font-semibold"
                                                        >
                                                            💵 Pagar
                                                        </button>
                                                    )}
                                                    <button
                                                        onClick={() => handleDelete(debt.id)}
                                                        className="flex-1 md:flex-none bg-red-100 text-red-600 px-4 py-2 rounded-lg hover:bg-red-200 transition-all font-semibold"
                                                    >
                                                        🗑️ Eliminar
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                    )
                                })}
                            </div>
                        )}
                    </div>

                    {/* Modal de Pago */}
                    {showPaymentModal && selectedDebt && (
                        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
                            <div className="bg-white rounded-xl shadow-2xl max-w-md w-full p-6">
                                <h3 className="text-2xl font-bold mb-4">💵 Registrar Pago</h3>
                                <p className="text-gray-600 mb-4">
                                    Deuda: <span className="font-bold">{selectedDebt.description}</span>
                                </p>
                                <p className="text-gray-600 mb-4">
                                    Saldo actual: <span className="font-bold text-red-600">{formatCOP(selectedDebt.remainingAmount)}</span>
                                </p>

                                <div className="mb-6">
                                    <label className="block text-sm font-medium mb-2">Monto del Pago</label>
                                    <input
                                        type="number"
                                        step="0.01"
                                        value={paymentAmount}
                                        onChange={(e) => setPaymentAmount(e.target.value)}
                                        className="w-full p-3 border rounded-lg"
                                        placeholder="Ingresa el monto"
                                    />
                                    <div className="flex gap-2 mt-2">
                                        <button
                                            onClick={() => setPaymentAmount(calculateMonthlyPayment(selectedDebt).toString())}
                                            className="text-sm px-3 py-1 bg-emerald-100 text-emerald-600 rounded hover:bg-emerald-200"
                                        >
                                            Pago sugerido (5%)
                                        </button>
                                        <button
                                            onClick={() => setPaymentAmount(selectedDebt.remainingAmount.toString())}
                                            className="text-sm px-3 py-1 bg-green-100 text-green-600 rounded hover:bg-green-200"
                                        >
                                            Pagar todo
                                        </button>
                                    </div>
                                </div>

                                <div className="flex gap-4">
                                    <button
                                        onClick={handlePayment}
                                        className="flex-1 bg-gradient-to-r from-green-500 to-green-600 text-white py-3 rounded-lg hover:shadow-lg transition-all font-semibold"
                                    >
                                        Confirmar Pago
                                    </button>
                                    <button
                                        onClick={() => {
                                            setShowPaymentModal(false)
                                            setSelectedDebt(null)
                                            setPaymentAmount('')
                                        }}
                                        className="flex-1 bg-gray-200 text-gray-700 py-3 rounded-lg hover:bg-gray-300 transition-all font-semibold"
                                    >
                                        Cancelar
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </ProtectedRoute>
    )
}

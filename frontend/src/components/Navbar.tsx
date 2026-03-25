'use client'

import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useState } from 'react'
import Logo from './Logo'
import { logout, getUserData } from '@/lib/auth'

export default function Navbar() {
    const router = useRouter()
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
    const userData = getUserData()
    const isAdmin = typeof window !== 'undefined' && localStorage.getItem('userRole') === 'admin'

    const handleLogout = () => {
        logout()
    }

    return (
        <nav className="bg-white/80 backdrop-blur-md shadow-sm sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16 md:h-20">
                    {/* Logo y Nombre */}
                    <Link href="/dashboard" className="flex items-center gap-2">
                        <Logo width={40} height={40} className="md:w-[60px] md:h-[60px]" />
                        <span className="text-xl md:text-3xl font-black bg-gradient-to-r from-gray-900 via-green-600 to-gray-900 bg-clip-text text-transparent tracking-tight">
                            FINNOVA
                        </span>
                    </Link>

                    {/* Desktop Menu */}
                    <div className="hidden lg:flex items-center space-x-6">
                        <Link href="/dashboard" className="text-gray-700 hover:text-emerald-600 font-medium transition">
                            Dashboard
                        </Link>
                        <Link href="/transactions" className="text-gray-700 hover:text-emerald-600 font-medium transition" id="nav-transactions">
                            Transacciones
                        </Link>
                        <Link href="/insights" className="text-gray-700 hover:text-emerald-600 font-medium transition">
                            Insights
                        </Link>
                        <Link href="/predictions" className="text-gray-700 hover:text-emerald-600 font-medium transition" id="nav-predictions">
                            Predicciones
                        </Link>
                        <Link href="/analysis" className="text-gray-700 hover:text-emerald-600 font-medium transition" id="nav-analysis">
                            Análisis
                        </Link>
                        <Link href="/simulator" className="text-transparent bg-gradient-to-r from-purple-600 via-pink-600 to-yellow-500 bg-clip-text hover:from-purple-700 hover:via-pink-700 hover:to-yellow-600 font-black transition" id="nav-simulator">
                            ⏰ TIME MACHINE
                        </Link>
                        {isAdmin && (
                            <Link href="/admin" className="text-red-600 hover:text-red-700 font-bold transition">
                                🛡️ Admin
                            </Link>
                        )}
                        <button
                            onClick={handleLogout}
                            className="text-red-600 hover:text-red-700 font-semibold transition"
                        >
                            Cerrar Sesión
                        </button>
                    </div>

                    {/* Mobile Menu Button */}
                    <button
                        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                        className="lg:hidden p-2 rounded-lg hover:bg-gray-100 transition"
                        aria-label="Toggle menu"
                    >
                        {mobileMenuOpen ? (
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        ) : (
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                            </svg>
                        )}
                    </button>
                </div>

                {/* Mobile Menu */}
                {mobileMenuOpen && (
                    <div className="lg:hidden py-4 border-t border-gray-200">
                        <div className="flex flex-col space-y-3">
                            <Link
                                href="/dashboard"
                                className="px-4 py-2 text-gray-700 hover:bg-emerald-50 hover:text-emerald-600 rounded-lg transition"
                                onClick={() => setMobileMenuOpen(false)}
                            >
                                📊 Dashboard
                            </Link>
                            <Link
                                href="/transactions"
                                className="px-4 py-2 text-gray-700 hover:bg-emerald-50 hover:text-emerald-600 rounded-lg transition"
                                onClick={() => setMobileMenuOpen(false)}
                            >
                                💳 Transacciones
                            </Link>
                            <Link
                                href="/insights"
                                className="px-4 py-2 text-gray-700 hover:bg-emerald-50 hover:text-emerald-600 rounded-lg transition"
                                onClick={() => setMobileMenuOpen(false)}
                            >
                                💡 Insights
                            </Link>
                            <Link
                                href="/analysis"
                                className="px-4 py-2 text-gray-700 hover:bg-emerald-50 hover:text-emerald-600 rounded-lg transition"
                                onClick={() => setMobileMenuOpen(false)}
                            >
                                📈 Análisis
                            </Link>
                            <Link
                                href="/simulator"
                                className="px-4 py-2 bg-gradient-to-r from-purple-50 to-pink-50 text-purple-700 font-bold rounded-lg transition"
                                onClick={() => setMobileMenuOpen(false)}
                            >
                                ⏰ TIME MACHINE
                            </Link>
                            <Link
                                href="/predictions"
                                className="px-4 py-2 text-gray-700 hover:bg-emerald-50 hover:text-emerald-600 rounded-lg transition"
                                onClick={() => setMobileMenuOpen(false)}
                            >
                                🔮 Predicciones
                            </Link>
                            <Link
                                href="/debts"
                                className="px-4 py-2 text-gray-700 hover:bg-emerald-50 hover:text-emerald-600 rounded-lg transition"
                                onClick={() => setMobileMenuOpen(false)}
                            >
                                💰 Deudas
                            </Link>
                            <button
                                onClick={() => {
                                    handleLogout()
                                    setMobileMenuOpen(false)
                                }}
                                className="px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition text-left font-semibold"
                            >
                                🚪 Cerrar Sesión
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </nav>
    )
}

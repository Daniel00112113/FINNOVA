'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import Logo from './Logo'

export default function Navigation() {
    const pathname = usePathname()

    const links = [
        { href: '/dashboard', label: 'Dashboard', icon: '📊' },
        { href: '/analysis', label: 'Análisis', icon: '📈' },
        { href: '/predictions', label: 'Predicciones', icon: '🔮' },
        { href: '/simulator', label: 'Simulador', icon: '🎯' },
        { href: '/debts', label: 'Deudas', icon: '💳' },
        { href: '/alerts', label: 'Alertas', icon: '🔔' },
        { href: '/transactions', label: 'Transacciones', icon: '💰' },
    ]

    return (
        <nav className="bg-white shadow-lg">
            <div className="max-w-7xl mx-auto px-4">
                <div className="flex justify-between items-center h-16">
                    <Link href="/dashboard" className="hover:opacity-80 transition">
                        <Logo width={60} height={60} showText priority />
                    </Link>

                    <div className="flex space-x-4">
                        {links.map((link) => (
                            <Link
                                key={link.href}
                                href={link.href}
                                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition ${pathname === link.href
                                    ? 'bg-blue-500 text-white'
                                    : 'text-gray-700 hover:bg-gray-100'
                                    }`}
                            >
                                <span>{link.icon}</span>
                                <span>{link.label}</span>
                            </Link>
                        ))}
                    </div>
                </div>
            </div>
        </nav>
    )
}

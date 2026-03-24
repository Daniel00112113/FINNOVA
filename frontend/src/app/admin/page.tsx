'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'

const formatCOP = (n: number) => new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }).format(n)

interface Metrics {
    users: { total: number; active30d: number; newLast7d: number; newToday: number; locked: number; byRole: { role: string; count: number }[] }
    transactions: { totalExpenses: number; totalIncomes: number; totalDebts: number; totalExpenseAmount: number; totalIncomeAmount: number; netBalance: number }
    registrationsByDay: { date: string; count: number }[]
    topUsers: { id: string; name: string; email: string; role: string; lastLoginAt: string | null }[]
}

interface AuditLog {
    id: string; userId: string | null; action: string; entity: string
    ipAddress: string | null; success: boolean; details: string | null; createdAt: string
}

interface AdminUser {
    id: string; name: string; email: string; role: string
    lastLoginAt: string | null; failedLoginAttempts: number; isLocked: boolean
}

export default function AdminPage() {
    const router = useRouter()
    const [metrics, setMetrics] = useState<Metrics | null>(null)
    const [logs, setLogs] = useState<AuditLog[]>([])
    const [users, setUsers] = useState<AdminUser[]>([])
    const [tab, setTab] = useState<'metrics' | 'users' | 'logs'>('metrics')
    const [loading, setLoading] = useState(true)
    const [search, setSearch] = useState('')
    const [logFilter, setLogFilter] = useState('')

    useEffect(() => {
        const role = localStorage.getItem('userRole')
        if (role !== 'admin') { router.push('/dashboard'); return }
        loadAll()
    }, [])

    const loadAll = async () => {
        try {
            const [m, l, u] = await Promise.all([
                api.get('/admin/metrics'),
                api.get('/admin/audit-logs?pageSize=100'),
                api.get('/admin/users?pageSize=50'),
            ])
            setMetrics(m.data)
            setLogs(l.data.logs)
            setUsers(u.data.users)
        } catch (e) {
            console.error(e)
        } finally {
            setLoading(false)
        }
    }

    const updateRole = async (id: string, role: string) => {
        await api.patch(`/admin/users/${id}/role`, { role })
        setUsers(users.map(u => u.id === id ? { ...u, role } : u))
    }

    const unlockUser = async (id: string) => {
        await api.post(`/admin/users/${id}/unlock`)
        setUsers(users.map(u => u.id === id ? { ...u, isLocked: false, failedLoginAttempts: 0 } : u))
    }

    if (loading) return (
        <div className="min-h-screen bg-gray-900 flex items-center justify-center">
            <div className="text-white text-xl">Cargando panel admin...</div>
        </div>
    )

    const filteredUsers = users.filter(u =>
        u.name.toLowerCase().includes(search.toLowerCase()) ||
        u.email.toLowerCase().includes(search.toLowerCase())
    )

    const filteredLogs = logs.filter(l =>
        !logFilter || l.action.includes(logFilter) || l.entity.includes(logFilter)
    )

    return (
        <div className="min-h-screen bg-gray-900 text-white">
            <div className="max-w-7xl mx-auto p-6">
                {/* Header */}
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-3xl font-black text-white">🛡️ Panel Admin</h1>
                        <p className="text-gray-400 mt-1">Finnova — Control total de la plataforma</p>
                    </div>
                    <button onClick={() => router.push('/dashboard')}
                        className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-sm">
                        ← Dashboard
                    </button>
                </div>

                {/* Tabs */}
                <div className="flex gap-2 mb-6">
                    {(['metrics', 'users', 'logs'] as const).map(t => (
                        <button key={t} onClick={() => setTab(t)}
                            className={`px-5 py-2 rounded-lg font-semibold text-sm transition ${tab === t ? 'bg-emerald-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}>
                            {t === 'metrics' ? '📊 Métricas' : t === 'users' ? '👥 Usuarios' : '📋 Audit Log'}
                        </button>
                    ))}
                </div>

                {/* MÉTRICAS */}
                {tab === 'metrics' && metrics && (
                    <div className="space-y-6">
                        {/* KPIs */}
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            {[
                                { label: 'Total Usuarios', value: metrics.users.total, icon: '👥', color: 'from-blue-600 to-blue-700' },
                                { label: 'Activos 30d', value: metrics.users.active30d, icon: '🟢', color: 'from-emerald-600 to-emerald-700' },
                                { label: 'Nuevos 7d', value: metrics.users.newLast7d, icon: '✨', color: 'from-purple-600 to-purple-700' },
                                { label: 'Bloqueados', value: metrics.users.locked, icon: '🔒', color: 'from-red-600 to-red-700' },
                            ].map(k => (
                                <div key={k.label} className={`bg-gradient-to-br ${k.color} p-5 rounded-xl`}>
                                    <div className="text-2xl mb-1">{k.icon}</div>
                                    <div className="text-3xl font-black">{k.value}</div>
                                    <div className="text-sm opacity-80">{k.label}</div>
                                </div>
                            ))}
                        </div>

                        {/* Transacciones */}
                        <div className="bg-gray-800 rounded-xl p-6">
                            <h2 className="text-xl font-bold mb-4">💰 Volumen de Transacciones</h2>
                            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                                <div className="bg-gray-700 p-4 rounded-lg">
                                    <p className="text-gray-400 text-sm">Total Ingresos</p>
                                    <p className="text-2xl font-bold text-green-400">{formatCOP(metrics.transactions.totalIncomeAmount)}</p>
                                    <p className="text-xs text-gray-500">{metrics.transactions.totalIncomes} registros</p>
                                </div>
                                <div className="bg-gray-700 p-4 rounded-lg">
                                    <p className="text-gray-400 text-sm">Total Gastos</p>
                                    <p className="text-2xl font-bold text-red-400">{formatCOP(metrics.transactions.totalExpenseAmount)}</p>
                                    <p className="text-xs text-gray-500">{metrics.transactions.totalExpenses} registros</p>
                                </div>
                                <div className="bg-gray-700 p-4 rounded-lg">
                                    <p className="text-gray-400 text-sm">Balance Neto</p>
                                    <p className={`text-2xl font-bold ${metrics.transactions.netBalance >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                                        {formatCOP(metrics.transactions.netBalance)}
                                    </p>
                                    <p className="text-xs text-gray-500">{metrics.transactions.totalDebts} deudas</p>
                                </div>
                            </div>
                        </div>

                        {/* Roles */}
                        <div className="bg-gray-800 rounded-xl p-6">
                            <h2 className="text-xl font-bold mb-4">🎭 Usuarios por Rol</h2>
                            <div className="flex gap-4">
                                {metrics.users.byRole.map(r => (
                                    <div key={r.role} className="bg-gray-700 px-6 py-4 rounded-lg text-center">
                                        <div className="text-2xl font-black">{r.count}</div>
                                        <div className="text-sm text-gray-400 capitalize">{r.role}</div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Registros por día */}
                        <div className="bg-gray-800 rounded-xl p-6">
                            <h2 className="text-xl font-bold mb-4">📈 Registros últimos 7 días</h2>
                            <div className="flex items-end gap-2 h-24">
                                {metrics.registrationsByDay.map(d => (
                                    <div key={d.date} className="flex-1 flex flex-col items-center gap-1">
                                        <span className="text-xs text-gray-400">{d.count}</span>
                                        <div className="w-full bg-emerald-500 rounded-t"
                                            style={{ height: `${Math.max(4, d.count * 20)}px` }} />
                                        <span className="text-xs text-gray-500">{new Date(d.date).getDate()}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                {/* USUARIOS */}
                {tab === 'users' && (
                    <div className="space-y-4">
                        <input
                            value={search} onChange={e => setSearch(e.target.value)}
                            placeholder="Buscar por nombre o email..."
                            className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-500"
                        />
                        <div className="bg-gray-800 rounded-xl overflow-hidden">
                            <table className="w-full text-sm">
                                <thead className="bg-gray-700">
                                    <tr>
                                        {['Nombre', 'Email', 'Rol', 'Último login', 'Estado', 'Acciones'].map(h => (
                                            <th key={h} className="px-4 py-3 text-left text-gray-300 font-semibold">{h}</th>
                                        ))}
                                    </tr>
                                </thead>
                                <tbody>
                                    {filteredUsers.map(u => (
                                        <tr key={u.id} className="border-t border-gray-700 hover:bg-gray-750">
                                            <td className="px-4 py-3 font-medium">{u.name}</td>
                                            <td className="px-4 py-3 text-gray-400">{u.email}</td>
                                            <td className="px-4 py-3">
                                                <select value={u.role}
                                                    onChange={e => updateRole(u.id, e.target.value)}
                                                    className="bg-gray-700 border border-gray-600 rounded px-2 py-1 text-xs">
                                                    <option value="user">user</option>
                                                    <option value="admin">admin</option>
                                                    <option value="support">support</option>
                                                </select>
                                            </td>
                                            <td className="px-4 py-3 text-gray-400 text-xs">
                                                {u.lastLoginAt ? new Date(u.lastLoginAt).toLocaleDateString('es-CO') : 'Nunca'}
                                            </td>
                                            <td className="px-4 py-3">
                                                {u.isLocked
                                                    ? <span className="px-2 py-1 bg-red-900 text-red-300 rounded text-xs">🔒 Bloqueado</span>
                                                    : <span className="px-2 py-1 bg-green-900 text-green-300 rounded text-xs">✅ Activo</span>}
                                            </td>
                                            <td className="px-4 py-3">
                                                {u.isLocked && (
                                                    <button onClick={() => unlockUser(u.id)}
                                                        className="px-3 py-1 bg-yellow-600 hover:bg-yellow-500 rounded text-xs font-medium">
                                                        Desbloquear
                                                    </button>
                                                )}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}

                {/* AUDIT LOG */}
                {tab === 'logs' && (
                    <div className="space-y-4">
                        <input
                            value={logFilter} onChange={e => setLogFilter(e.target.value)}
                            placeholder="Filtrar por acción o entidad..."
                            className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-500"
                        />
                        <div className="bg-gray-800 rounded-xl overflow-hidden">
                            <table className="w-full text-sm">
                                <thead className="bg-gray-700">
                                    <tr>
                                        {['Fecha', 'Acción', 'Entidad', 'IP', 'Estado', 'Detalles'].map(h => (
                                            <th key={h} className="px-4 py-3 text-left text-gray-300 font-semibold">{h}</th>
                                        ))}
                                    </tr>
                                </thead>
                                <tbody>
                                    {filteredLogs.map(l => (
                                        <tr key={l.id} className={`border-t border-gray-700 ${!l.success ? 'bg-red-950/20' : ''}`}>
                                            <td className="px-4 py-2 text-gray-400 text-xs whitespace-nowrap">
                                                {new Date(l.createdAt).toLocaleString('es-CO')}
                                            </td>
                                            <td className="px-4 py-2 font-mono text-xs text-yellow-300">{l.action}</td>
                                            <td className="px-4 py-2 text-gray-300 text-xs">{l.entity}</td>
                                            <td className="px-4 py-2 text-gray-500 text-xs">{l.ipAddress || '-'}</td>
                                            <td className="px-4 py-2">
                                                {l.success
                                                    ? <span className="text-green-400 text-xs">✅</span>
                                                    : <span className="text-red-400 text-xs">❌</span>}
                                            </td>
                                            <td className="px-4 py-2 text-gray-500 text-xs max-w-xs truncate">{l.details || '-'}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}

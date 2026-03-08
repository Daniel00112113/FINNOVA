import { ReactNode } from 'react'

interface StatCardProps {
    title: string
    value: string | number
    change?: string
    trend?: 'up' | 'down' | 'neutral'
    icon?: ReactNode
    color?: 'blue' | 'green' | 'red' | 'yellow' | 'purple'
    className?: string
}

const colorClasses = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    red: 'from-red-500 to-red-600',
    yellow: 'from-yellow-500 to-yellow-600',
    purple: 'from-purple-500 to-purple-600'
}

export function StatCard({
    title,
    value,
    change,
    trend,
    icon,
    color = 'blue',
    className = ''
}: StatCardProps) {
    return (
        <div className={`bg-gradient-to-br ${colorClasses[color]} p-6 rounded-lg shadow-lg text-white ${className}`}>
            <div className="flex items-start justify-between">
                <div className="flex-1">
                    <p className="text-sm opacity-90 mb-2">{title}</p>
                    <p className="text-3xl font-bold">{value}</p>
                    {change && (
                        <div className="mt-2 flex items-center gap-1">
                            {trend === 'up' && <span>↑</span>}
                            {trend === 'down' && <span>↓</span>}
                            <span className="text-sm opacity-90">{change}</span>
                        </div>
                    )}
                </div>
                {icon && (
                    <div className="text-4xl opacity-80">
                        {icon}
                    </div>
                )}
            </div>
        </div>
    )
}

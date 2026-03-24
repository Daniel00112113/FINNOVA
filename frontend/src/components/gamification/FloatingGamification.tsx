'use client';

import { useEffect, useState } from 'react';
import { Trophy, Star, Flame, X } from 'lucide-react';
import Link from 'next/link';
import { api } from '@/lib/api';

interface GamificationData {
    progress: {
        points: number;
        level: number;
        currentStreak: number;
        pointsToNextLevel: number;
        progressPercentage: number;
    };
}

export default function FloatingGamification() {
    const [data, setData] = useState<GamificationData | null>(null);
    const [isMinimized, setIsMinimized] = useState(false);
    const [isVisible, setIsVisible] = useState(true);

    useEffect(() => {
        fetchGamificationData();

        // Actualizar cada 30 segundos
        const interval = setInterval(fetchGamificationData, 30000);

        // Escuchar eventos de actualización
        window.addEventListener('gamification-update', fetchGamificationData as any);

        return () => {
            clearInterval(interval);
            window.removeEventListener('gamification-update', fetchGamificationData as any);
        };
    }, []);

    const fetchGamificationData = async () => {
        try {
            const userId = localStorage.getItem('userId');

            if (!userId) return;

            const response = await api.get(`/users/${userId}/gamification/stats`);
            setData(response.data);
        } catch (error) {
            console.error('Error fetching gamification:', error);
        }
    };

    if (!data || !isVisible) return null;

    if (isMinimized) {
        return (
            <div
                onClick={() => setIsMinimized(false)}
                className="fixed bottom-4 right-4 z-50 cursor-pointer"
            >
                <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-full p-3 shadow-lg hover:scale-110 transition-transform">
                    <div className="flex items-center gap-2">
                        <Trophy className="w-5 h-5" />
                        <span className="font-bold">{data.progress.points}</span>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="fixed bottom-4 right-4 z-50 w-72">
            <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl shadow-2xl p-4 border-2 border-purple-200">
                <div className="flex items-center justify-between mb-3">
                    <Link href="/dashboard" className="flex items-center gap-2 hover:opacity-80 transition">
                        <Trophy className="w-4 h-4 text-purple-600" />
                        <span className="text-sm font-semibold text-gray-800">Tu Progreso</span>
                    </Link>
                    <div className="flex items-center gap-2">
                        <button
                            onClick={() => setIsMinimized(true)}
                            className="text-gray-400 hover:text-gray-600 transition"
                        >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                            </svg>
                        </button>
                        <button
                            onClick={() => setIsVisible(false)}
                            className="text-gray-400 hover:text-gray-600 transition"
                        >
                            <X className="w-4 h-4" />
                        </button>
                    </div>
                </div>

                <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                        <Star className="w-5 h-5 text-yellow-500 fill-yellow-500" />
                        <span className="text-2xl font-bold text-gray-800">{data.progress.points}</span>
                        <span className="text-xs text-gray-600">pts</span>
                    </div>
                    <div className="flex items-center gap-1 bg-white px-2 py-1 rounded-full">
                        <Flame className={`w-4 h-4 ${data.progress.currentStreak > 0 ? 'text-orange-500' : 'text-gray-400'}`} />
                        <span className="text-sm font-bold text-gray-800">{data.progress.currentStreak}</span>
                    </div>
                </div>

                <div className="mb-2">
                    <div className="flex items-center justify-between mb-1">
                        <span className="text-xs text-gray-600">Nivel {data.progress.level}</span>
                        <span className="text-xs text-gray-500">{data.progress.pointsToNextLevel} pts</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                        <div
                            className="bg-gradient-to-r from-purple-500 to-blue-500 h-full rounded-full transition-all duration-500"
                            style={{ width: `${data.progress.progressPercentage}%` }}
                        ></div>
                    </div>
                </div>

                <Link
                    href="/dashboard"
                    className="block text-center text-xs text-purple-600 hover:text-purple-700 font-medium mt-2"
                >
                    Ver detalles →
                </Link>
            </div>
        </div>
    );
}

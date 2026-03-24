'use client';

import { useEffect, useState } from 'react';
import { Trophy, Flame, Star, TrendingUp } from 'lucide-react';
import { api } from '@/lib/api';

interface GamificationData {
    progress: {
        points: number;
        level: number;
        currentStreak: number;
        longestStreak: number;
        totalLogins: number;
        lastActivityDate: string;
        pointsToNextLevel: number;
        progressPercentage: number;
    };
    recentAchievements: Achievement[];
    unlockedBadges: string[];
    motivationalMessage: string;
}

interface Achievement {
    type: string;
    pointsEarned: number;
    description: string | null;
    createdAt: string;
}

export default function GamificationWidget() {
    const [data, setData] = useState<GamificationData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchGamificationData();
    }, []);

    const getAchievementIcon = (type: string): string => {
        const icons: Record<string, string> = {
            'expense_logged': '📝',
            'income_created': '💰',
            'streak_7_days': '🔥',
            'streak_30_days': '⚡',
            'level_up': '🎉',
            'goal_reached': '🎯'
        };
        return icons[type] || '⭐';
    };

    const fetchGamificationData = async () => {
        try {
            const userId = localStorage.getItem('userId');

            if (!userId) {
                console.error('No userId found');
                setLoading(false);
                return;
            }

            const response = await api.get(`/users/${userId}/gamification/stats`);
            setData(response.data);
        } catch (error) {
            console.error('Error fetching gamification:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="bg-white rounded-xl shadow-sm p-6 animate-pulse">
                <div className="h-4 bg-gray-200 rounded w-1/3 mb-4"></div>
                <div className="h-8 bg-gray-200 rounded w-2/3"></div>
            </div>
        );
    }

    if (!data) return null;

    return (
        <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl shadow-sm p-6 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-purple-200 rounded-full opacity-20 -mr-16 -mt-16"></div>

            <div className="relative z-10">
                <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                        <Trophy className="w-5 h-5 text-purple-600" />
                        <h3 className="font-semibold text-gray-800">Tu Progreso</h3>
                    </div>
                    <div className="flex items-center gap-1 bg-white px-3 py-1 rounded-full shadow-sm">
                        <Star className="w-4 h-4 text-yellow-500 fill-yellow-500" />
                        <span className="text-sm font-bold text-gray-800">{data.progress.points}</span>
                    </div>
                </div>


                <div className="mb-4">
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-sm text-gray-600">Nivel {data.progress.level}</span>
                        <span className="text-xs text-gray-500">{data.progress.pointsToNextLevel} pts para nivel {data.progress.level + 1}</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                        <div
                            className="bg-gradient-to-r from-purple-500 to-blue-500 h-full rounded-full transition-all duration-500 ease-out"
                            style={{ width: `${data.progress.progressPercentage}%` }}
                        ></div>
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                    <div className="bg-white rounded-lg p-3 shadow-sm">
                        <div className="flex items-center gap-2 mb-1">
                            <Flame className={`w-4 h-4 ${data.progress.currentStreak > 0 ? 'text-orange-500' : 'text-gray-400'}`} />
                            <span className="text-xs text-gray-600">Racha</span>
                        </div>
                        <p className="text-2xl font-bold text-gray-800">{data.progress.currentStreak}</p>
                        <p className="text-xs text-gray-500">días seguidos</p>
                    </div>

                    <div className="bg-white rounded-lg p-3 shadow-sm">
                        <div className="flex items-center gap-2 mb-1">
                            <TrendingUp className="w-4 h-4 text-green-500" />
                            <span className="text-xs text-gray-600">Récord</span>
                        </div>
                        <p className="text-2xl font-bold text-gray-800">{data.progress.longestStreak}</p>
                        <p className="text-xs text-gray-500">días máximo</p>
                    </div>
                </div>

                {data.recentAchievements.length > 0 && (
                    <div className="mt-4 pt-4 border-t border-purple-100">
                        <p className="text-xs text-gray-600 mb-2">Últimos logros:</p>
                        <div className="space-y-2">
                            {data.recentAchievements.slice(0, 2).map((achievement, index) => (
                                <div key={index} className="flex items-center gap-2 bg-white rounded-lg p-2 shadow-sm">
                                    <span className="text-xl">{getAchievementIcon(achievement.type)}</span>
                                    <div className="flex-1 min-w-0">
                                        <p className="text-sm font-medium text-gray-800 truncate">
                                            {achievement.description || achievement.type}
                                        </p>
                                        <p className="text-xs text-gray-500">+{achievement.pointsEarned} pts</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

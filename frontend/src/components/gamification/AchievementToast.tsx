'use client';

import { useEffect, useState } from 'react';
import { Trophy, X } from 'lucide-react';

interface Achievement {
    title: string;
    description: string;
    icon: string;
    pointsEarned: number;
}

interface AchievementToastProps {
    achievement: Achievement | null;
    onClose: () => void;
}

export default function AchievementToast({ achievement, onClose }: AchievementToastProps) {
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        if (achievement) {
            setIsVisible(true);
            const timer = setTimeout(() => {
                setIsVisible(false);
                setTimeout(onClose, 300);
            }, 5000);
            return () => clearTimeout(timer);
        }
    }, [achievement, onClose]);

    if (!achievement) return null;

    return (
        <div className={`fixed top-4 right-4 z-50 transition-all duration-300 ${isVisible ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'
            }`}>
            <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg shadow-2xl p-4 max-w-sm animate-bounce-in">
                <div className="flex items-start gap-3">
                    <div className="flex-shrink-0">
                        <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center text-2xl">
                            {achievement.icon}
                        </div>
                    </div>

                    <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                            <Trophy className="w-4 h-4" />
                            <p className="font-bold text-sm">¡Logro Desbloqueado!</p>
                        </div>
                        <p className="font-semibold text-base mb-1">{achievement.title}</p>
                        <p className="text-sm text-white/90 mb-2">{achievement.description}</p>
                        <div className="flex items-center gap-1 text-yellow-300">
                            <span className="text-lg">⭐</span>
                            <span className="font-bold">+{achievement.pointsEarned} puntos</span>
                        </div>
                    </div>

                    <button
                        onClick={() => {
                            setIsVisible(false);
                            setTimeout(onClose, 300);
                        }}
                        className="flex-shrink-0 text-white/80 hover:text-white transition-colors"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>
            </div>
        </div>
    );
}

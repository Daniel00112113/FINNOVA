'use client';

import { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import AchievementToast from './AchievementToast';

interface Achievement {
    title: string;
    description: string;
    icon: string;
    pointsEarned: number;
}

interface GamificationContextType {
    showAchievement: (achievement: Achievement) => void;
    triggerUpdate: () => void;
}

const GamificationContext = createContext<GamificationContextType | undefined>(undefined);

export function GamificationProvider({ children }: { children: ReactNode }) {
    const [currentAchievement, setCurrentAchievement] = useState<Achievement | null>(null);

    const showAchievement = useCallback((achievement: Achievement) => {
        setCurrentAchievement(achievement);
    }, []);

    const triggerUpdate = useCallback(() => {
        // Disparar evento para actualizar el widget flotante
        window.dispatchEvent(new Event('gamification-update'));
    }, []);

    return (
        <GamificationContext.Provider value={{ showAchievement, triggerUpdate }}>
            {children}
            <AchievementToast
                achievement={currentAchievement}
                onClose={() => setCurrentAchievement(null)}
            />
        </GamificationContext.Provider>
    );
}

export function useGamification() {
    const context = useContext(GamificationContext);
    if (context === undefined) {
        throw new Error('useGamification must be used within a GamificationProvider');
    }
    return context;
}

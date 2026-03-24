import { useEffect, useState, useCallback } from 'react';

interface Achievement {
    title: string;
    description: string;
    icon: string;
    pointsEarned: number;
}

export function useGamification() {
    const [newAchievement, setNewAchievement] = useState<Achievement | null>(null);

    // Escuchar eventos de logros desde el backend
    useEffect(() => {
        const handleAchievement = (event: CustomEvent) => {
            setNewAchievement(event.detail);
        };

        window.addEventListener('achievement-unlocked' as any, handleAchievement);

        return () => {
            window.removeEventListener('achievement-unlocked' as any, handleAchievement);
        };
    }, []);

    const triggerAchievement = useCallback((achievement: Achievement) => {
        const event = new CustomEvent('achievement-unlocked', { detail: achievement });
        window.dispatchEvent(event);
    }, []);

    const clearAchievement = useCallback(() => {
        setNewAchievement(null);
    }, []);

    return {
        newAchievement,
        triggerAchievement,
        clearAchievement
    };
}

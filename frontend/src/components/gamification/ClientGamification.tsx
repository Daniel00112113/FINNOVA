'use client';

import { GamificationProvider } from './GamificationProvider';
import FloatingGamification from './FloatingGamification';

export default function ClientGamification({ children }: { children: React.ReactNode }) {
    return (
        <GamificationProvider>
            {children}
            <FloatingGamification />
        </GamificationProvider>
    );
}

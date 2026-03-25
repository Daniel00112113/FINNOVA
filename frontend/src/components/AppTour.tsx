'use client'

import { useEffect } from 'react'

export function useAppTour() {
    const startTour = async () => {
        // Importar driver.js dinámicamente (solo client-side)
        const { driver } = await import('driver.js')
        await import('driver.js/dist/driver.css')

        const driverObj = driver({
            showProgress: true,
            animate: true,
            overlayOpacity: 0.75,
            smoothScroll: true,
            allowClose: true,
            progressText: 'Paso {{current}} de {{total}}',
            nextBtnText: 'Siguiente →',
            prevBtnText: '← Anterior',
            doneBtnText: '¡Listo! 🚀',
            steps: [
                {
                    element: '#dashboard-title',
                    popover: {
                        title: '🏠 Tu Dashboard',
                        description: 'Este es tu centro de control financiero. Aquí ves todo de un vistazo: balance, ingresos, gastos y deudas en tiempo real.',
                        side: 'bottom',
                        align: 'start',
                    }
                },
                {
                    element: '#gamification-widget',
                    popover: {
                        title: '🏆 Tu Progreso',
                        description: 'Gana puntos y sube de nivel registrando transacciones. Mantén tu racha diaria para desbloquear logros especiales.',
                        side: 'bottom',
                        align: 'start',
                    }
                },
                {
                    element: '#daily-budget',
                    popover: {
                        title: '💰 Presupuesto Diario',
                        description: 'La IA calcula cuánto puedes gastar hoy basándose en tus ingresos y el tiempo hasta tu próximo pago.',
                        side: 'top',
                        align: 'center',
                    }
                },
                {
                    element: '#quick-actions',
                    popover: {
                        title: '⚡ Acciones Rápidas',
                        description: 'Accede directamente a Transacciones, Simulador, Predicciones y Análisis. Son las 4 funciones principales de FINNOVA.',
                        side: 'top',
                        align: 'center',
                    }
                },
                {
                    element: '#nav-transactions',
                    popover: {
                        title: '💳 Transacciones',
                        description: 'Registra tus ingresos y gastos aquí. Mientras más datos agregues, más precisas serán las predicciones de la IA.',
                        side: 'bottom',
                        align: 'start',
                    }
                },
                {
                    element: '#nav-predictions',
                    popover: {
                        title: '🔮 Predicciones IA',
                        description: 'La IA analiza tus patrones y predice tu balance futuro a 3, 6 o 12 meses con un nivel de confianza calculado.',
                        side: 'bottom',
                        align: 'start',
                    }
                },
                {
                    element: '#nav-simulator',
                    popover: {
                        title: '🎯 Simulador',
                        description: 'Compara 5 escenarios financieros: ¿qué pasa si reduces gastos 20%? ¿Si aumentas ingresos? Descúbrelo antes de decidir.',
                        side: 'bottom',
                        align: 'start',
                    }
                },
                {
                    element: '#nav-analysis',
                    popover: {
                        title: '📊 Análisis',
                        description: 'Gráficas detalladas de tus patrones de gasto, tendencias y comparativas mes a mes.',
                        side: 'bottom',
                        align: 'start',
                    }
                },
            ],
            onDestroyed: () => {
                localStorage.setItem('tourCompleted', 'true')
            }
        })

        driverObj.drive()
    }

    return { startTour }
}

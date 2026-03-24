import type { Metadata } from 'next'
import './globals.css'
import ClientGamification from '@/components/gamification/ClientGamification'

export const metadata: Metadata = {
    title: 'FINNOVA - Tu Copiloto Financiero',
    description: 'Tu copiloto financiero inteligente',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="es">
            <body>
                <ClientGamification>
                    {children}
                </ClientGamification>
            </body>
        </html>
    )
}

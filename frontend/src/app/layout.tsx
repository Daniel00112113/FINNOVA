import type { Metadata } from 'next'
import './globals.css'

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
            <body>{children}</body>
        </html>
    )
}

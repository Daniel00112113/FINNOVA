'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Navbar from './Navbar'

export default function AppLayout({ children }: { children: React.ReactNode }) {
    const router = useRouter()

    useEffect(() => {
        const userId = localStorage.getItem('userId')
        if (!userId) {
            router.push('/')
        }
    }, [router])

    return (
        <div className="min-h-screen bg-gray-50">
            <Navbar />
            <main className="container mx-auto px-4 py-8">
                {children}
            </main>
        </div>
    )
}

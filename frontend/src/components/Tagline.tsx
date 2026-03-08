'use client'

import Image from 'next/image'
import { useState } from 'react'

interface TaglineProps {
    width?: number
    height?: number
    className?: string
    variant?: 'default' | 'white'
}

export default function Tagline({
    width = 400,
    height = 100,
    className = '',
    variant = 'default'
}: TaglineProps) {
    const [imageError, setImageError] = useState(false)

    const imageSrc = variant === 'white'
        ? '/images/tagline/tagline-white.png'
        : '/images/tagline/tagline.png'

    // Si hay error, mostrar texto como fallback
    if (imageError) {
        return (
            <div className={`text-center ${className}`}>
                <p className="text-lg md:text-xl font-semibold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                    Tu Copiloto Financiero Impulsado por IA
                </p>
            </div>
        )
    }

    return (
        <Image
            src={imageSrc}
            alt="Tu Copiloto Financiero Impulsado por IA"
            width={width}
            height={height}
            className={className}
            onError={() => setImageError(true)}
            unoptimized
        />
    )
}

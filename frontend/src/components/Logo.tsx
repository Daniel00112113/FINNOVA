'use client'

import Image from 'next/image'
import { useState } from 'react'

interface LogoProps {
    width?: number
    height?: number
    size?: 'sm' | 'md' | 'lg' | 'xl'
    className?: string
    priority?: boolean
    showText?: boolean
    showTagline?: boolean
}

export default function Logo({
    width,
    height,
    size = 'md',
    className = '',
    priority = false,
    showText = false,
    showTagline = false
}: LogoProps) {
    const [imageError, setImageError] = useState(false)

    // Determinar dimensiones basadas en size si no se especifican width/height
    const sizeMap = {
        sm: 32,
        md: 40,
        lg: 64,
        xl: 80
    }

    const finalWidth = width || sizeMap[size]
    const finalHeight = height || sizeMap[size]

    return (
        <div className="flex items-center gap-3">
            {imageError ? (
                <div
                    className={`flex items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg ${className}`}
                    style={{ width: finalWidth, height: finalHeight }}
                >
                    <span className="text-white font-bold" style={{ fontSize: finalWidth * 0.6 }}>
                        💰
                    </span>
                </div>
            ) : (
                <Image
                    src="/images/logo/LOGO.png"
                    alt="FINNOVA"
                    width={finalWidth}
                    height={finalHeight}
                    priority={priority}
                    className={`rounded-lg ${className}`}
                    onError={() => setImageError(true)}
                    unoptimized
                />
            )}

            {showText && (
                <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                    FINNOVA
                </span>
            )}

            {showTagline && (
                <img
                    src="/images/tagline/tagline.png"
                    alt="FINNOVA - Innovando tu futuro financiero"
                    className="ml-3 h-10 md:h-12 w-auto"
                    onError={(e) => {
                        console.error('Error loading tagline image')
                        e.currentTarget.style.display = 'none'
                    }}
                />
            )}
        </div>
    )
}

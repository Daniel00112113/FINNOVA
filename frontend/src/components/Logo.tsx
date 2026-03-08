'use client'

import Image from 'next/image'
import { useState } from 'react'

interface LogoProps {
    width?: number
    height?: number
    className?: string
    priority?: boolean
    showText?: boolean
    showTagline?: boolean
}

export default function Logo({
    width = 40,
    height = 40,
    className = '',
    priority = false,
    showText = false,
    showTagline = false
}: LogoProps) {
    const [imageError, setImageError] = useState(false)
    const [taglineError, setTaglineError] = useState(false)

    return (
        <div className="flex items-center gap-3">
            {imageError ? (
                <div
                    className={`flex items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg ${className}`}
                    style={{ width, height }}
                >
                    <span className="text-white font-bold" style={{ fontSize: width * 0.6 }}>
                        🤖
                    </span>
                </div>
            ) : (
                <Image
                    src="/images/logo/LOGO.png"
                    alt="FINNOVA"
                    width={width}
                    height={height}
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
                        setTaglineError(true)
                    }}
                />
            )}
        </div>
    )
}

# Carpeta de Imágenes

Esta carpeta contiene todos los assets visuales del proyecto Financial Copilot AI.

## Estructura

```
public/
└── images/
    ├── logo/           # Logos de la aplicación
    ├── tagline/        # Eslogan e imágenes de marca
    ├── icons/          # Iconos personalizados
    └── illustrations/  # Ilustraciones y gráficos
```

## Cómo usar las imágenes

### En componentes de React/Next.js:

```tsx
import Image from 'next/image'

// Opción 1: Con el componente Image de Next.js (recomendado)
<Image 
  src="/images/logo/logo.png" 
  alt="Financial Copilot AI Logo"
  width={200}
  height={50}
/>

// Opción 2: Con etiqueta img normal
<img src="/images/logo/logo.png" alt="Financial Copilot AI Logo" />
```

## Logos recomendados

Coloca tus logos en `public/images/logo/`:

- `logo.png` - Logo principal (fondo transparente)
- `logo-white.png` - Logo para fondos oscuros
- `logo-icon.png` - Solo el ícono (cuadrado, para favicon)
- `favicon.ico` - Favicon del sitio

## Tagline / Eslogan

Coloca tus imágenes de eslogan en `public/images/tagline/`:

- `tagline.png` - Eslogan principal ("Tu Copiloto Financiero Impulsado por IA")
- `tagline-white.png` - Eslogan para fondos oscuros
- `powered-by.png` - Badge "Powered by AI"

### Uso del tagline:

```tsx
<Image 
  src="/images/tagline/tagline.png" 
  alt="Tu Copiloto Financiero Impulsado por IA"
  width={400}
  height={100}
/>
```

## Formatos recomendados

- **PNG**: Para logos con transparencia
- **SVG**: Para iconos escalables
- **WebP**: Para imágenes optimizadas
- **JPG**: Para fotografías

## Optimización

Next.js optimiza automáticamente las imágenes cuando usas el componente `<Image>`:
- Lazy loading automático
- Responsive images
- Formatos modernos (WebP)
- Prevención de Layout Shift

## Ejemplo de uso en el proyecto

```tsx
// En Navigation.tsx o cualquier componente
import Image from 'next/image'

<div className="flex items-center gap-2">
  <Image 
    src="/images/logo/logo.png" 
    alt="Financial Copilot AI"
    width={40}
    height={40}
    priority // Para logos que se muestran inmediatamente
  />
  <span className="text-xl font-bold">Financial Copilot AI</span>
</div>
```

## Notas importantes

1. Las rutas siempre empiezan con `/` (relativo a `public/`)
2. No incluyas `public` en la ruta
3. Next.js sirve estos archivos estáticamente
4. Los archivos en `public/` son accesibles públicamente

## Tamaños recomendados para logos

- **Logo principal**: 400x100px (o proporcional)
- **Logo icon**: 512x512px (cuadrado)
- **Favicon**: 32x32px, 16x16px
- **Open Graph**: 1200x630px (para redes sociales)

# Configurar Variable de Entorno en Vercel - URGENTE

## Problema
El archivo `.env.production` está en `.gitignore` y no se sube a Git, por lo que Vercel no tiene la URL correcta del backend.

## Solución

### Paso 1: Ir a Vercel Dashboard
1. Ve a https://vercel.com/dashboard
2. Selecciona tu proyecto `finnova` (o como se llame)
3. Ve a "Settings" > "Environment Variables"

### Paso 2: Agregar Variable de Entorno
Agrega la siguiente variable:

```
Key: NEXT_PUBLIC_API_URL
Value: https://finnova-backend-hquh.onrender.com/api
Environment: Production
```

### Paso 3: Redesplegar
1. Ve a la pestaña "Deployments"
2. Encuentra el último despliegue
3. Haz clic en los tres puntos "..." > "Redeploy"
4. Selecciona "Use existing Build Cache" (más rápido)
5. Haz clic en "Redeploy"

## Verificación

Después del redespliegue, abre tu aplicación en:
```
https://finnova-theta.vercel.app
```

Y verifica que:
- Ya no aparezcan errores 404 en la consola
- Las peticiones vayan a `https://finnova-backend-hquh.onrender.com/api`
- Los datos se carguen correctamente

## Alternativa: Usar Vercel CLI

Si tienes Vercel CLI instalado:

```bash
vercel env add NEXT_PUBLIC_API_URL production
# Pegar: https://finnova-backend-hquh.onrender.com/api

vercel --prod
```

## Estado Actual

- ✅ Backend: Configurado con variables de entorno en Render
- ✅ Migración: Subida y lista para aplicarse
- ⏳ Frontend: Necesita variable de entorno en Vercel (este paso)

Una vez completado este paso, todo debería funcionar correctamente.

# Frontend — Deploy

Next.js 14 con App Router, desplegado como Docker en Render.

## Stack

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Axios para llamadas al backend

## Variables de entorno

| Variable               | Descripción                        | Ejemplo                                          |
|------------------------|------------------------------------|--------------------------------------------------|
| `NEXT_PUBLIC_API_URL`  | URL base del backend (con `/api`)  | `https://finnova-backend-hquh.onrender.com/api`  |

> `NEXT_PUBLIC_*` se embebe en el bundle en **build time**. Debe pasarse como `ARG` en el Dockerfile y como `buildArgs` en render.yaml.

## Deploy en Render

Render usa el `Dockerfile` de esta carpeta. La variable `NEXT_PUBLIC_API_URL` se pasa en dos lugares del `render.yaml`:

```yaml
buildArgs:
  - key: NEXT_PUBLIC_API_URL
    value: https://finnova-backend-hquh.onrender.com/api
envVars:
  - key: NEXT_PUBLIC_API_URL
    value: https://finnova-backend-hquh.onrender.com/api
```

Si cambias la URL del backend en Render, actualiza **ambos** valores y redeploya el frontend.

## Deploy local

```bash
cd frontend
npm install
cp .env.example .env.local
# Editar .env.local:
# NEXT_PUBLIC_API_URL=http://localhost:5000/api

npm run dev
# → http://localhost:3000
```

## Build de producción local

```bash
npm run build
npm start
```

## Docker local

```bash
docker build \
  --build-arg NEXT_PUBLIC_API_URL=http://localhost:5000/api \
  -t finnova-frontend .

docker run -p 3000:3000 finnova-frontend
```

## Estructura relevante

```
frontend/src/
├── app/
│   ├── admin/          → Panel admin (solo rol admin/support)
│   ├── auth/           → Login y registro
│   ├── dashboard/      → Dashboard principal
│   ├── transactions/   → Ingresos y gastos
│   ├── predictions/    → Predicciones IA
│   ├── simulator/      → Simulador financiero
│   ├── analysis/       → Análisis
│   └── debts/          → Deudas
├── components/
│   ├── gamification/   → Widget de gamificación
│   └── mobile/         → Navegación móvil
└── lib/
    ├── api.ts          → Instancia axios + interceptores (refresh token automático)
    └── auth.ts         → Login, logout, manejo de tokens
```

## Notas importantes

- El JWT expira en **2 horas**. El interceptor en `api.ts` renueva automáticamente usando el refresh token (30 días).
- El rol del usuario se guarda en `localStorage` como `userRole`. La página `/admin` redirige si no es `admin` o `support`.
- En producción, CORS solo permite `*.onrender.com` y `*.vercel.app`.

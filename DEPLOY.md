# Finnova — Guía de Deploy

Monorepo con 4 servicios desplegados en Render + PostgreSQL.

```
finnova/
├── frontend/        → Next.js  → finnova-frontend (Render)
├── backend/         → .NET 10  → finnova-backend  (Render)
├── ai-engine/       → FastAPI  → finnova-ai-engine (Render)
└── database/        → PostgreSQL → finnova-db (Render managed)
```

## URLs de producción

| Servicio   | URL                                              |
|------------|--------------------------------------------------|
| Frontend   | https://finnova-frontend.onrender.com            |
| Backend    | https://finnova-backend-hquh.onrender.com        |
| AI Engine  | https://finnova-ai-engine.onrender.com           |

---

## Deploy rápido (todo en Render)

```bash
# 1. Conectar repo en render.com → New → Blueprint
# 2. Render lee render.yaml y crea los 4 servicios automáticamente
# 3. Esperar ~10 min para el primer build
```

Ver [render.yaml](./render.yaml) para la configuración completa.

---

## Deploy local (Docker Compose)

```bash
cp backend/.env.example backend/.env
# Editar backend/.env con tus valores

docker compose up --build
```

| Servicio  | Puerto local |
|-----------|-------------|
| Frontend  | http://localhost:3000 |
| Backend   | http://localhost:5000 |
| AI Engine | http://localhost:8000 |
| DB        | localhost:5432 |

---

## Primer admin

Después del primer deploy, crear el admin via env vars en Render:

1. Render → `finnova-backend` → Environment → agregar:
   - `AdminBootstrap__Email` = tu@email.com
   - `AdminBootstrap__Password` = contraseña_segura
2. Manual Deploy → esperar que arranque → ver logs: `✅ Admin creado`
3. **Eliminar** esas dos variables → Manual Deploy de nuevo

Panel admin disponible en: `https://finnova-frontend.onrender.com/admin`

---

## Documentación por servicio

- [Frontend](./frontend/DEPLOY.md)
- [Backend](./backend/DEPLOY.md)
- [AI Engine](./ai-engine/DEPLOY.md)
- [Base de datos](./database/DEPLOY.md)

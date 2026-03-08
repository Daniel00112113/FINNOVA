# 🚀 GUÍA RÁPIDA: SUBIR A GITHUB

## ✅ ESTADO ACTUAL

- ✅ Git inicializado
- ✅ Remote configurado: https://github.com/DanielDEV03/FINNOVA.git
- ✅ .gitignore creado (archivos sensibles protegidos)
- ✅ README.md profesional creado

---

## 📝 PASO 1: CONFIGURAR TU USUARIO

```bash
# Configurar tu nombre
git config --global user.name "Daniel DEV"

# Configurar tu email (el de tu cuenta de GitHub)
git config --global user.email "tu-email@example.com"

# Verificar
git config --global user.name
git config --global user.email
```

---

## 📦 PASO 2: PREPARAR ARCHIVOS

```bash
# Ver qué archivos se subirán
git status

# Agregar todos los archivos
git add .

# Ver qué se agregó
git status
```

---

## 💾 PASO 3: HACER COMMIT

```bash
# Primer commit
git commit -m "🎉 Initial commit: FINNOVA - Financial Copilot con IA profesional"
```

---

## 🌐 PASO 4: SUBIR A GITHUB

```bash
# Crear rama main
git branch -M main

# Subir a GitHub
git push -u origin main
```

Si te pide autenticación:
1. Usa tu **Personal Access Token** (no tu contraseña)
2. Genera uno en: https://github.com/settings/tokens
3. Permisos necesarios: `repo` (todos)

---

## 🔐 ARCHIVOS PROTEGIDOS (NO SE SUBEN)

El `.gitignore` protege estos archivos sensibles:

- ✅ `appsettings.Production.json` (JWT Key)
- ✅ `.env` y `.env.production` (variables de entorno)
- ✅ `claves-generadas.txt` (claves generadas)
- ✅ `node_modules/` (dependencias)
- ✅ `bin/` y `obj/` (archivos compilados)
- ✅ `venv/` (entorno virtual Python)
- ✅ `*.pkl` (modelos ML entrenados - muy pesados)

---

## 📋 COMANDOS COMPLETOS (COPIAR Y PEGAR)

```bash
# 1. Configurar usuario
git config --global user.name "Daniel DEV"
git config --global user.email "tu-email@example.com"

# 2. Agregar archivos
git add .

# 3. Commit
git commit -m "🎉 Initial commit: FINNOVA - Financial Copilot con IA profesional"

# 4. Subir
git branch -M main
git push -u origin main
```

---

## 🔄 COMANDOS FUTUROS (DESPUÉS DEL PRIMER PUSH)

```bash
# Ver cambios
git status

# Agregar cambios
git add .

# Commit
git commit -m "✨ Descripción de los cambios"

# Subir
git push
```

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Error: "Authentication failed"
**Solución**: Usa Personal Access Token en lugar de contraseña
1. Ir a: https://github.com/settings/tokens
2. Generate new token (classic)
3. Seleccionar `repo` (todos los permisos)
4. Copiar el token
5. Usarlo como contraseña

### Error: "Remote already exists"
```bash
git remote remove origin
git remote add origin https://github.com/DanielDEV03/FINNOVA.git
```

### Error: "Nothing to commit"
```bash
git add .
git commit -m "mensaje"
```

### Ver qué archivos se ignorarán
```bash
git status --ignored
```

---

## ✅ VERIFICACIÓN

Después de hacer push, verifica en GitHub:
1. Ir a: https://github.com/DanielDEV03/FINNOVA
2. Verificar que los archivos están ahí
3. Verificar que README.md se ve bien
4. Verificar que NO están los archivos sensibles

---

## 📊 ESTRUCTURA QUE SE SUBIRÁ

```
FINNOVA/
├── backend/
│   ├── src/
│   └── FinancialCopilot.sln
├── frontend/
│   ├── src/
│   └── package.json
├── ai-engine/
│   ├── models/
│   ├── training/
│   └── main.py
├── .gitignore
├── README.md
├── start-secure.ps1
└── docs/ (todas las guías)
```

**NO se subirán**:
- ❌ node_modules/
- ❌ bin/ y obj/
- ❌ venv/
- ❌ .env y appsettings.Production.json
- ❌ claves-generadas.txt
- ❌ Modelos ML entrenados (*.pkl)

---

## 🎯 SIGUIENTE PASO

```bash
# Ejecuta estos 4 comandos:
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
git add .
git commit -m "🎉 Initial commit: FINNOVA - Financial Copilot"
git branch -M main
git push -u origin main
```

¡Listo! Tu proyecto estará en GitHub 🚀

---

**Última actualización**: 2026-03-09
**Repositorio**: https://github.com/DanielDEV03/FINNOVA

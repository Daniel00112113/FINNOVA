# 🔧 SOLUCIÓN: Error 403 - Permission Denied

## ❌ PROBLEMA

```
remote: Permission to DanielDEV03/FINNOVA.git denied to Daniel00112113.
fatal: unable to access 'https://github.com/DanielDEV03/FINNOVA.git/': The requested URL returned error: 403
```

**Causa**: Git está usando credenciales del usuario anterior (`Daniel00112113`).

---

## ✅ SOLUCIÓN (2 OPCIONES)

### OPCIÓN 1: Personal Access Token (MÁS FÁCIL) ⭐

#### Paso 1: Generar Token en GitHub

1. Ir a: https://github.com/settings/tokens
2. Click en "Generate new token" → "Generate new token (classic)"
3. Configurar:
   - **Note**: `FINNOVA - Local Development`
   - **Expiration**: `90 days` (o lo que prefieras)
   - **Scopes**: Marcar `repo` (todos los permisos de repositorio)
4. Click en "Generate token"
5. **COPIAR EL TOKEN** (solo se muestra una vez)

Ejemplo de token: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

#### Paso 2: Cambiar Remote a HTTPS con Token

```powershell
# Eliminar remote actual
git remote remove origin

# Agregar con token en la URL
git remote add origin https://ghp_TU_TOKEN_AQUI@github.com/DanielDEV03/FINNOVA.git

# Verificar
git remote -v
```

#### Paso 3: Push

```powershell
git push -u origin main
```

**¡Listo!** No pedirá credenciales.

---

### OPCIÓN 2: SSH Key (MÁS SEGURO)

#### Paso 1: Generar SSH Key

```powershell
# Generar nueva SSH key
ssh-keygen -t ed25519 -C "danieldelarosa07102023@gmail.com"

# Presionar Enter 3 veces (sin passphrase para simplicidad)
```

Esto crea:
- `~/.ssh/id_ed25519` (clave privada)
- `~/.ssh/id_ed25519.pub` (clave pública)

#### Paso 2: Copiar Clave Pública

```powershell
# Ver y copiar la clave pública
cat ~/.ssh/id_ed25519.pub
```

Copiar TODO el contenido (empieza con `ssh-ed25519 ...`)

#### Paso 3: Agregar a GitHub

1. Ir a: https://github.com/settings/keys
2. Click en "New SSH key"
3. Configurar:
   - **Title**: `PC Local - FINNOVA`
   - **Key**: Pegar la clave pública copiada
4. Click en "Add SSH key"

#### Paso 4: Probar Conexión

```powershell
# Probar SSH
ssh -T git@github.com

# Debe decir: "Hi DanielDEV03! You've successfully authenticated..."
```

#### Paso 5: Push

```powershell
# El remote ya está configurado con SSH
git push -u origin main
```

---

## 🚀 COMANDOS COMPLETOS

### Con Personal Access Token (OPCIÓN 1 - RECOMENDADA)

```powershell
# 1. Generar token en: https://github.com/settings/tokens
# 2. Copiar el token

# 3. Configurar remote con token
git remote remove origin
git remote add origin https://ghp_TU_TOKEN_AQUI@github.com/DanielDEV03/FINNOVA.git

# 4. Push
git push -u origin main
```

### Con SSH (OPCIÓN 2)

```powershell
# 1. Generar SSH key
ssh-keygen -t ed25519 -C "danieldelarosa07102023@gmail.com"

# 2. Copiar clave pública
cat ~/.ssh/id_ed25519.pub

# 3. Agregar a GitHub: https://github.com/settings/keys

# 4. Probar
ssh -T git@github.com

# 5. Push (remote ya está configurado)
git push -u origin main
```

---

## 🔍 VERIFICAR CONFIGURACIÓN ACTUAL

```powershell
# Ver usuario configurado
git config --global user.name
git config --global user.email

# Ver remote
git remote -v

# Ver credenciales guardadas
cmdkey /list | Select-String "git"
```

---

## 🆘 SI SIGUE FALLANDO

### Limpiar TODO y empezar de nuevo

```powershell
# 1. Limpiar credenciales de Windows
cmdkey /list | Select-String "git" | ForEach-Object {
    if ($_.Line -match "Target: (.+)") {
        cmdkey /delete:$matches[1]
    }
}

# 2. Limpiar configuración de Git
git config --global --unset credential.helper
git config --system --unset credential.helper

# 3. Reconfigurar usuario
git config --global user.name "DanielDEV03"
git config --global user.email "danieldelarosa07102023@gmail.com"

# 4. Usar OPCIÓN 1 (Personal Access Token)
```

---

## ✅ RECOMENDACIÓN

**USA LA OPCIÓN 1 (Personal Access Token)** porque:
- ✅ Más fácil y rápido
- ✅ No requiere configurar SSH
- ✅ Funciona inmediatamente
- ✅ Puedes revocar el token si es necesario

---

## 📝 EJEMPLO COMPLETO (OPCIÓN 1)

```powershell
# 1. Ve a: https://github.com/settings/tokens
# 2. Generate new token (classic)
# 3. Marca "repo"
# 4. Copia el token (ejemplo: ghp_abc123xyz789...)

# 5. Ejecuta:
git remote remove origin
git remote add origin https://ghp_abc123xyz789@github.com/DanielDEV03/FINNOVA.git
git push -u origin main

# ¡Listo! 🎉
```

---

## 🎯 SIGUIENTE PASO

1. Elige una opción (recomiendo OPCIÓN 1)
2. Sigue los pasos
3. Ejecuta `git push -u origin main`
4. ¡Tu código estará en GitHub! 🚀

---

**Última actualización**: 2026-03-09
**Estado**: Credenciales limpiadas, listo para configurar

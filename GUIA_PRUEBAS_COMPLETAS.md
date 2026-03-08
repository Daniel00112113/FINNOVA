# 🧪 GUÍA DE PRUEBAS COMPLETAS

## ✅ ESTADO: Controllers Protegidos

Todos los controllers tienen `[Authorize]` excepto AuthController (como debe ser).

---

## 🚀 PASO 1: INICIAR TODOS LOS SERVICIOS

### Opción A: Script Automático (RECOMENDADO)
```powershell
.\start-secure.ps1
```

### Opción B: Manual (4 terminales)

**Terminal 1 - PostgreSQL:**
```powershell
docker start financial-copilot-db
# Esperar 5 segundos
docker ps | Select-String "financial-copilot-db"
```

**Terminal 2 - AI Engine:**
```powershell
cd ai-engine
$env:PYTHONIOENCODING="utf-8"
python main.py
# Debe mostrar: "Uvicorn running on http://127.0.0.1:8000"
```

**Terminal 3 - Backend:**
```powershell
cd backend/src/FinancialCopilot.API
dotnet run
# Debe mostrar: "Now listening on: http://localhost:5000"
```

**Terminal 4 - Frontend:**
```powershell
cd frontend
npm run dev
# Debe mostrar: "Local: http://localhost:3000"
```

---

## 🧪 PASO 2: PRUEBAS DE SEGURIDAD

### Prueba 1: Verificar que API está protegida ❌ (Debe fallar)

```powershell
# Intentar acceder sin token (debe dar 401)
curl http://localhost:5000/api/users/00000000-0000-0000-0000-000000000001/dashboard
```

**Resultado esperado:**
```
StatusCode: 401 Unauthorized
```

✅ Si da 401 = La seguridad funciona
❌ Si da 200 = Hay un problema

---

### Prueba 2: Registro de Usuario ✅

1. Abrir navegador: http://localhost:3000/auth/register
2. Llenar formulario:
   - Nombre: `Test User`
   - Email: `test@example.com`
   - Contraseña: `Test123!`
3. Click en "Crear Cuenta"

**Resultado esperado:**
- ✅ Redirige a `/onboarding`
- ✅ En DevTools → Application → Local Storage:
  - `token` existe
  - `userId` existe
  - `userName` = "Test User"
  - `userEmail` = "test@example.com"

---

### Prueba 3: Logout y Login ✅

1. Click en el botón de logout (arriba derecha)
2. Debe redirigir a `/auth/login`
3. Verificar que Local Storage está limpio
4. Hacer login con:
   - Email: `test@example.com`
   - Contraseña: `Test123!`
5. Debe redirigir a `/dashboard`

**Resultado esperado:**
- ✅ Logout limpia token
- ✅ Login restaura token
- ✅ Puede navegar por la app

---

### Prueba 4: Protección de Rutas ✅

1. Estando logueado, ir a `/dashboard`
2. Abrir DevTools → Application → Local Storage
3. Borrar manualmente el `token`
4. Intentar navegar a `/expenses`

**Resultado esperado:**
- ✅ Redirige automáticamente a `/auth/login`
- ✅ No puede acceder a rutas protegidas sin token

---

### Prueba 5: API con Token ✅

```powershell
# Obtener el token de Local Storage (copiar desde DevTools)
$token = "TU_TOKEN_AQUI"

# Hacer request con token (debe funcionar)
curl http://localhost:5000/api/users/TU_USER_ID/dashboard -H "Authorization: Bearer $token"
```

**Resultado esperado:**
- ✅ StatusCode: 200 OK
- ✅ Devuelve datos del dashboard

---

## 📊 PASO 3: PRUEBAS FUNCIONALES

### Prueba 6: Agregar Gastos ✅

1. Ir a `/transactions`
2. Click en "Agregar Gasto"
3. Llenar:
   - Descripción: `Almuerzo`
   - Monto: `25000`
   - Categoría: `Alimentación`
   - Fecha: Hoy
4. Guardar

**Resultado esperado:**
- ✅ Gasto aparece en la lista
- ✅ Dashboard se actualiza

---

### Prueba 7: Simulador con Recomendaciones Personalizadas ✅

1. Agregar varios gastos en diferentes categorías:
   - Alimentación: $150,000
   - Transporte: $100,000
   - Entretenimiento: $80,000
2. Ir a `/simulator`
3. Scroll hasta "💡 Impacto de Pequeños Cambios"

**Resultado esperado:**
- ✅ Muestra recomendaciones basadas en TUS categorías reales
- ✅ Top 3 categorías con más gasto
- ✅ Cálculo de ahorro personalizado
- ✅ NO muestra "café, uber, delivery" genéricos

**Ejemplo de lo que deberías ver:**
```
🍕 Reducir Alimentación
De $150,000 a $105,000/mes
Ahorro mensual: $45,000

🚗 Reducir Transporte
De $100,000 a $70,000/mes
Ahorro mensual: $30,000

🎮 Reducir Entretenimiento
De $80,000 a $56,000/mes
Ahorro mensual: $24,000

💰 Ahorro Total Combinado
$1,188,000 en 12 meses con estos 3 cambios basados en tus gastos
```

---

### Prueba 8: Predicciones de IA ✅

1. Ir a `/predictions`
2. Ver predicciones de gastos futuros

**Resultado esperado:**
- ✅ Muestra predicción de gastos
- ✅ Muestra predicción de balance
- ✅ Muestra nivel de confianza
- ✅ Si falla modelo profesional, usa fallback automáticamente

---

### Prueba 9: Análisis Financiero ✅

1. Ir a `/analysis`
2. Ver análisis de riesgo

**Resultado esperado:**
- ✅ Muestra nivel de riesgo
- ✅ Muestra recomendaciones
- ✅ Gráficos de distribución

---

### Prueba 10: Insights ✅

1. Ir a `/insights`
2. Ver insights financieros

**Resultado esperado:**
- ✅ Muestra patrones de gasto
- ✅ Muestra tendencias
- ✅ Recomendaciones personalizadas

---

## 🐛 TROUBLESHOOTING

### Error: "401 Unauthorized" en todas las requests

**Causa**: Token no se está enviando o es inválido

**Solución**:
1. Verificar que `token` existe en Local Storage
2. Hacer logout y login de nuevo
3. Verificar que `api.ts` tiene los interceptores correctos

---

### Error: "CORS policy"

**Causa**: Backend no permite requests desde frontend

**Solución**:
```csharp
// Verificar en Program.cs que CORS está configurado
app.UseCors("AllowFrontend");
```

---

### Error: Recomendaciones siguen siendo genéricas

**Causa**: No hay suficientes gastos registrados

**Solución**:
1. Agregar al menos 10 gastos en diferentes categorías
2. Recargar el simulador
3. Las recomendaciones deben cambiar

---

### Error: Modelo profesional falla

**Causa**: Usuario nuevo con pocas transacciones

**Solución**: ✅ ESTO ES NORMAL
- El sistema usa fallback automáticamente
- Las predicciones siguen funcionando
- A medida que agregues más transacciones, mejorará

---

## ✅ CHECKLIST DE PRUEBAS

### Seguridad
- [ ] API sin token da 401
- [ ] Registro funciona
- [ ] Login funciona
- [ ] Logout funciona
- [ ] Rutas protegidas redirigen a login
- [ ] API con token funciona

### Funcionalidad
- [ ] Agregar gastos funciona
- [ ] Dashboard se actualiza
- [ ] Simulador muestra recomendaciones personalizadas
- [ ] Predicciones funcionan
- [ ] Análisis funciona
- [ ] Insights funcionan

### Recomendaciones Personalizadas
- [ ] Con gastos: muestra categorías reales
- [ ] Sin gastos: muestra fallback genérico
- [ ] Cálculo de ahorro es correcto
- [ ] Top 3 categorías son las correctas

---

## 🎯 RESULTADO ESPERADO

Después de todas las pruebas:

✅ **Seguridad**: JWT funciona, API protegida, rutas protegidas
✅ **Funcionalidad**: Todas las features funcionan
✅ **Recomendaciones**: Personalizadas basadas en datos reales
✅ **IA**: Predicciones funcionan con fallback robusto

---

## 📞 COMANDOS ÚTILES

### Ver logs del backend
```powershell
# Los logs aparecen en la terminal donde corre dotnet run
```

### Ver token actual
```javascript
// En DevTools Console
console.log(localStorage.getItem('token'))
```

### Limpiar todo y empezar de nuevo
```javascript
// En DevTools Console
localStorage.clear()
location.reload()
```

### Verificar usuarios en BD
```powershell
docker exec -it financial-copilot-db psql -U postgres -d financialcopilot
SELECT "Id", "Name", "Email", "CreatedAt" FROM "Users";
\q
```

---

## 🚀 SIGUIENTE PASO

Una vez que todas las pruebas pasen:

1. ✅ Sistema funcional y seguro
2. ✅ Listo para agregar más features
3. ✅ Listo para despliegue a producción (con cambios de seguridad)

---

**Última actualización**: 2026-03-08 23:50
**Estado**: Listo para pruebas completas

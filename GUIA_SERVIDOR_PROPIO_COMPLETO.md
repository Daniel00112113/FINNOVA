# 🏠 GUÍA: TU PROPIO SERVIDOR DESDE CERO

## 🎯 OBJETIVO

Montar tu propio servidor con:
- Control total
- Dominio propio (gratis o barato)
- Infraestructura propia
- Costos mínimos

---

## 💰 COSTOS REALES

### Opción 1: GRATIS (Para empezar)
- **Servidor**: Oracle Cloud Free Tier (GRATIS para siempre)
- **Dominio**: Freenom (.tk, .ml, .ga) o DuckDNS (GRATIS)
- **SSL**: Let's Encrypt (GRATIS)
- **Total**: $0/mes

### Opción 2: SEMI-PROFESIONAL ($5-12/mes)
- **Servidor**: Contabo VPS ($5/mes) o Hetzner ($4.5/mes)
- **Dominio**: Namecheap .com ($8.88/año = $0.74/mes)
- **SSL**: Let's Encrypt (GRATIS)
- **Total**: ~$6/mes

### Opción 3: PROFESIONAL ($15-25/mes)
- **Servidor**: DigitalOcean Droplet ($12/mes)
- **Dominio**: .com premium ($12/año)
- **CDN**: Cloudflare (GRATIS)
- **Backups**: Automáticos incluidos
- **Total**: ~$13/mes

---

## 🆓 OPCIÓN GRATIS: ORACLE CLOUD

### Paso 1: Crear Cuenta en Oracle Cloud

1. Ir a: https://www.oracle.com/cloud/free/
2. Crear cuenta (requiere tarjeta pero NO cobra)
3. Verificar email

### Paso 2: Crear VM Gratuita

```bash
# Especificaciones GRATIS para siempre:
- 2 VMs AMD (1 GB RAM cada una) o
- 4 ARM CPUs + 24 GB RAM (Ampere A1)
- 200 GB almacenamiento
- 10 TB transferencia/mes
```

**Crear VM:**
1. Compute → Instances → Create Instance
2. Nombre: `financial-copilot-server`
3. Image: Ubuntu 22.04
4. Shape: Ampere (ARM) - 4 CPUs, 24 GB RAM (GRATIS)
5. Networking: Crear nueva VCN
6. SSH Keys: Generar o subir tu clave
7. Create

### Paso 3: Configurar Firewall

```bash
# En Oracle Cloud Console
Networking → Virtual Cloud Networks → Tu VCN → Security Lists

# Agregar reglas de ingreso:
- Puerto 80 (HTTP)
- Puerto 443 (HTTPS)
- Puerto 22 (SSH) - Solo tu IP
```

### Paso 4: Conectar al Servidor

```bash
# Desde tu PC
ssh -i tu-clave.pem ubuntu@TU-IP-PUBLICA
```

---

## 🌐 DOMINIO GRATIS

### Opción A: Freenom (Dominios .tk, .ml, .ga, .cf, .gq)

1. Ir a: https://www.freenom.com
2. Buscar dominio disponible: `financialcopilot.tk`
3. Checkout (GRATIS por 12 meses, renovable)
4. Configurar DNS:
   - Type: A
   - Name: @
   - Target: TU-IP-SERVIDOR
   - TTL: 14400

5. Agregar subdominio API:
   - Type: A
   - Name: api
   - Target: TU-IP-SERVIDOR

### Opción B: DuckDNS (Subdominios .duckdns.org)

1. Ir a: https://www.duckdns.org
2. Login con Google/GitHub
3. Crear subdomain: `financialcopilot.duckdns.org`
4. Agregar tu IP
5. Instalar cliente en servidor:

```bash
# En tu servidor
mkdir ~/duckdns
cd ~/duckdns
nano duck.sh

# Agregar:
echo url="https://www.duckdns.org/update?domains=financialcopilot&token=TU-TOKEN&ip=" | curl -k -o ~/duckdns/duck.log -K -

# Hacer ejecutable
chmod 700 duck.sh

# Agregar a crontab (actualizar cada 5 min)
crontab -e
*/5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1
```

### Opción C: Dominio Barato (.com por $8/año)

**Namecheap** (recomendado):
1. Ir a: https://www.namecheap.com
2. Buscar dominio: `financialcopilot.com`
3. Comprar (~$8.88/año)
4. Configurar DNS igual que Freenom

---

## 🐳 INSTALACIÓN EN TU SERVIDOR

### Paso 1: Actualizar Sistema

```bash
# Conectado a tu servidor
sudo apt update && sudo apt upgrade -y
```

### Paso 2: Instalar Docker

```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Agregar usuario a grupo docker
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar
docker --version
docker-compose --version

# Logout y login de nuevo
exit
ssh -i tu-clave.pem ubuntu@TU-IP-PUBLICA
```

### Paso 3: Clonar Tu Proyecto

```bash
# Instalar Git
sudo apt install git -y

# Clonar (o subir con SCP)
git clone https://github.com/tu-usuario/financial-copilot.git
cd financial-copilot
```

### Paso 4: Crear Docker Compose

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: financialcopilot
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network
    restart: unless-stopped

  backend:
    build: ./backend
    environment:
      Jwt__Key: ${JWT_KEY}
      ConnectionStrings__DefaultConnection: "Host=postgres;Database=financialcopilot;Username=${DB_USER};Password=${DB_PASSWORD}"
      AiEngine__BaseUrl: "http://ai-engine:8000"
    depends_on:
      - postgres
    networks:
      - app-network
    restart: unless-stopped

  ai-engine:
    build: ./ai-engine
    environment:
      DATABASE_URL: "postgresql://${DB_USER}:${DB_PASSWORD}@postgres:5432/financialcopilot"
    depends_on:
      - postgres
    networks:
      - app-network
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - ai-engine
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

### Paso 5: Configurar Variables de Entorno

```bash
# Crear .env
nano .env

# Agregar:
DB_USER=postgres
DB_PASSWORD=$(openssl rand -base64 32)
JWT_KEY=$(openssl rand -base64 64)
```

### Paso 6: Configurar Nginx

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name tudominio.tk www.tudominio.tk;
        
        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }
        
        location / {
            return 301 https://$server_name$request_uri;
        }
    }

    # Backend API
    server {
        listen 443 ssl http2;
        server_name api.tudominio.tk;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;

        location / {
            proxy_pass http://backend:80;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### Paso 7: Obtener SSL Gratis (Let's Encrypt)

```bash
# Instalar Certbot
sudo apt install certbot -y

# Obtener certificado
sudo certbot certonly --standalone -d tudominio.tk -d www.tudominio.tk -d api.tudominio.tk

# Copiar certificados
sudo mkdir -p ssl
sudo cp /etc/letsencrypt/live/tudominio.tk/fullchain.pem ssl/
sudo cp /etc/letsencrypt/live/tudominio.tk/privkey.pem ssl/
sudo chmod 644 ssl/*

# Renovación automática
sudo crontab -e
# Agregar:
0 0 1 * * certbot renew --quiet && cp /etc/letsencrypt/live/tudominio.tk/*.pem /home/ubuntu/financial-copilot/ssl/
```

### Paso 8: Iniciar Todo

```bash
# Construir e iniciar
docker-compose -f docker-compose.prod.yml up -d --build

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f

# Verificar que todo está corriendo
docker-compose -f docker-compose.prod.yml ps
```

---

## 🚀 DESPLEGAR FRONTEND EN VERCEL

```bash
# En tu PC, en la carpeta frontend
npm i -g vercel

# Login
vercel login

# Configurar variables de entorno
vercel env add NEXT_PUBLIC_API_URL production
# Valor: https://api.tudominio.tk/api

# Desplegar
vercel --prod

# Configurar dominio personalizado (opcional)
vercel domains add tudominio.tk
```

---

## 🔒 SEGURIDAD ADICIONAL

### 1. Firewall UFW

```bash
# Habilitar firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. Fail2Ban (Protección contra ataques)

```bash
# Instalar
sudo apt install fail2ban -y

# Configurar
sudo nano /etc/fail2ban/jail.local

# Agregar:
[sshd]
enabled = true
port = 22
maxretry = 3
bantime = 3600

# Reiniciar
sudo systemctl restart fail2ban
```

### 3. Actualizaciones Automáticas

```bash
# Instalar
sudo apt install unattended-upgrades -y

# Configurar
sudo dpkg-reconfigure -plow unattended-upgrades
```

---

## 📊 MONITOREO

### Instalar Netdata (Gratis)

```bash
# Instalar
bash <(curl -Ss https://my-netdata.io/kickstart.sh)

# Acceder en: http://TU-IP:19999
```

---

## 💾 BACKUPS AUTOMÁTICOS

```bash
# Crear script de backup
nano ~/backup.sh

# Agregar:
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/ubuntu/backups"
mkdir -p $BACKUP_DIR

# Backup PostgreSQL
docker exec financial-copilot-postgres-1 pg_dump -U postgres financialcopilot | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Mantener solo últimos 30 días
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +30 -delete

# Hacer ejecutable
chmod +x ~/backup.sh

# Agregar a crontab (diario a las 2 AM)
crontab -e
0 2 * * * /home/ubuntu/backup.sh
```

---

## 🎯 COMANDOS ÚTILES

```bash
# Ver logs
docker-compose logs -f backend

# Reiniciar servicio
docker-compose restart backend

# Ver uso de recursos
docker stats

# Actualizar código
git pull
docker-compose up -d --build

# Limpiar Docker
docker system prune -a
```

---

## 📈 ESCALABILIDAD

### Cuando crezcas, puedes:

1. **Agregar más servidores** (Load Balancer)
2. **Separar servicios** (BD en servidor dedicado)
3. **CDN** (Cloudflare gratis)
4. **Cache** (Redis)
5. **Replicación de BD** (Alta disponibilidad)

---

## 💡 VENTAJAS DE TU PROPIO SERVIDOR

✅ **Control total**: Haces lo que quieras
✅ **Privacidad**: Tus datos, tu servidor
✅ **Aprendizaje**: Experiencia real de DevOps
✅ **Escalable**: Creces a tu ritmo
✅ **Económico**: Desde $0 hasta lo que quieras
✅ **Profesional**: Portfolio real

---

## ⚠️ DESVENTAJAS

❌ **Responsabilidad**: Tú mantienes todo
❌ **Tiempo**: Requiere configuración inicial
❌ **Conocimiento**: Necesitas aprender Linux/Docker
❌ **Disponibilidad**: Si el servidor cae, tú lo arreglas

---

## 🎓 RECURSOS PARA APRENDER

- **Linux**: https://linuxjourney.com
- **Docker**: https://docs.docker.com/get-started/
- **Nginx**: https://nginx.org/en/docs/
- **PostgreSQL**: https://www.postgresql.org/docs/

---

## 🚀 RESUMEN RÁPIDO

```bash
# 1. Crear servidor en Oracle Cloud (GRATIS)
# 2. Obtener dominio en Freenom (GRATIS)
# 3. Instalar Docker
# 4. Clonar proyecto
# 5. Configurar .env
# 6. Obtener SSL con Let's Encrypt
# 7. docker-compose up -d
# 8. Desplegar frontend en Vercel
# 9. ¡Listo!
```

**Costo total**: $0/mes (con Oracle + Freenom)
**Tiempo setup**: 2-3 horas
**Dificultad**: Media

---

## 🎯 MI RECOMENDACIÓN

**Para empezar**: Oracle Cloud + Freenom (GRATIS)
**Cuando tengas usuarios**: Comprar dominio .com ($8/año)
**Cuando crezcas**: Migrar a servidor pagado ($12/mes)

---

**¿Quieres que te ayude con algún paso específico?** Puedo guiarte en:
- Configurar Oracle Cloud
- Obtener dominio gratis
- Configurar Docker
- Configurar SSL
- Cualquier otra cosa

¡Tu servidor, tus reglas! 🏠🚀

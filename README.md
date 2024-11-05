# Proyecto de Gestión Estudiante con Python y base de datos
## Pasos (comandos) para levantar el proyecto:
### 1. docker-compose down
### 2. docker compose up -d
### 3. docker ps (verificar que el contenedor esté corriendo)
Si el contenedor no está corriendo, ejecutar el siguiente comando:
### docker ps -a (el primer contenedor que aparece, copiar el id del contenedor)

### docker start f92dcaf5d4c7 (después del start se pega el id del contenedor que se explica arriba)

### pip install -r requirements.txt
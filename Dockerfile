# Imagen base slim con versión fija
FROM python:3.12.7-slim

# Evitar archivos .pyc y habilitar salida sin buffer en logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    INPUT_PATH=/data/input/inversiones.csv \
    OUTPUT_PATH=/data/output/resumen_inversiones.csv \
    MIN_INVESTMENT_USD=0

# Crear usuario sin privilegios y directorios de trabajo/datos
RUN groupadd --system appgroup && useradd --system --gid appgroup appuser \
    && mkdir -p /app /data/input /data/output \
    && chown -R appuser:appgroup /app /data

WORKDIR /app

# Copiar e instalar dependencias primero para aprovechar la caché de capas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente con los permisos adecuados
COPY --chown=appuser:appgroup process_investments.py .

# Cambiar a usuario sin privilegios
USER appuser

# Ejecutar el script usando forma exec
CMD ["python", "process_investments.py"]

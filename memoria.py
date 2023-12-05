import shutil
import psutil

# Obtener estadísticas de uso de disco duro
espacio = shutil.disk_usage("/")

# Uso actual del disco duro en porcentaje
uso_disco = (espacio.used / espacio.total) * 100

print(f"Uso de disco duro: {uso_disco:.2f}%")

# Obtener estadísticas de memoria
memoria = psutil.virtual_memory()

# Uso actual de la memoria en porcentaje
uso_memoria = memoria.percent

print(f"Uso de memoria: {uso_memoria}%")
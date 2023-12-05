import os
import shutil
import openpyxl

# Ruta a la carpeta compartida
ruta_compartida = r'\\192.168.40.34\e910\mediaobj\htmlupload'
ruta_nueva = r'C:\Users\profesionalinformaci\Downloads\Farticulos1'

# Ruta al archivo Excel con los nombres actuales y nuevos
archivo_excel = 'C:\\Users\\profesionalinformaci\\Downloads\\Farticulos1.xlsx'

# Cargar el archivo Excel
workbook = openpyxl.load_workbook(archivo_excel)
sheet = workbook.active

# Iterar a través de las filas del archivo Excel
for row in sheet.iter_rows(min_row=1, values_only=True):
    nombre_actual = row[0]
    nuevo_nombre = row[1]

    # Ruta completa al archivo actual y al nuevo archivo
    ruta_archivo_actual = os.path.join(ruta_compartida, nombre_actual)
    ruta_archivo_nuevo = os.path.join(ruta_nueva, nuevo_nombre)

    # Verificar si el archivo actual existe en la carpeta compartida
    if os.path.exists(ruta_archivo_actual):
        # Mover y renombrar el archivo
        shutil.copy(ruta_archivo_actual, ruta_archivo_nuevo)
        print(f'Se ha movido y renombrado "{nombre_actual}" a "{nuevo_nombre}"')
    else:
        print(f'El archivo "{nombre_actual}" no se encontró en la carpeta compartida.')

# Cerrar el archivo Excel
workbook.close()
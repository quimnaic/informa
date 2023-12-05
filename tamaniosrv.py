import psycopg2
import paramiko
import datetime

#fecha actual 
fecha_actual = datetime.date.today()

# Configuración de la conexión a la base de datos PostgreSQL
db_config = {
    'database': 'postgres',
    'user': 'admin',
    'password': 'PruebasMasivo2023',
    'host': '192.168.110.22',  # Cambia esto si tu base de datos está en un servidor remoto
}

# Configuracion de conexión SSH
servers = [
    #PRODUCCION SW
    {
        'hostname' : '192.168.110.15',
        'port' : '22',
        'username' : 'sis_info',
        'password' : 'S!S=!%_SW1_23',
        'path' : '/Data'
    },
    #PRODUCCION BASES DE DATOS
    {
        'hostname' : '192.168.110.30',
        'port' : '22',
        'username' : 'sis_info',
        'password' : 'S!S=#=_DB_23',
        'path' : '/Data'
    },
    #JDE 33
    {
        'hostname' : '192.168.40.33',
        'port' : '22',
        'username' : 'sis_info',
        'password' : 'S!S=##_JDEWEB_22',
        'path' : '/u01'
    },
    #JDE 93 
    {
        'hostname' : '192.168.40.93',
        'port' : '22',
        'username' : 'root',
        'password' : 'c=p)t#L',
        'path' : '/u01'
    },
    #WEBLOGIC 91
    {
        'hostname' : '192.168.40.91',
        'port' : '22',
        'username' : 'sis_info',
        'password' : 'S!S=)!_JDEBATCH_22',
        'path' : '/u01' 
    },
    #BATCH 11
    {
        'hostname' : '192.168.40.11',
        'port' : '22',
        'username' : 'root',
        'password' : 'c=p!t!L',
        'path' : '/u01'
    },
    #BI168
    {
        'hostname' : '192.168.40.168',
        'port' : '22',
        'username' : 'root',
        'password' : 'c!p&t(L',
        'path' : '/boot' 
    },
    #BI45
    {
        'hostname' : '192.168.40.45',
        'port' : '22',
        'username' : 'root',
        'password' : 'c=p$t%L',
        'path' : '/boot' 
    },
    #GLPI
    {
        'hostname' : '192.168.110.12',
        'port' : '22',
        'username' : 'sis_info',
        'password' : 'S!S=!"_GLPI_23',
        'path' : '/Data' 
    }            
]

#Iteramos la conexión atraves de una lista 
for server_config in servers:
    try:
        # Comando para saber tamaño disponible 
        disk_command = "df -h "+server_config['path']+" | awk '{print $3}'"
        print(disk_command)
        servidor = server_config['hostname']
        path = server_config['path']
        # Abre la conexion SSH en el servidor 
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(
            server_config['hostname'],
            port=server_config.get('port', 22),
            username=server_config['username'],
            password=server_config.get('password', None)
        )

        # Ejecuta el comando dentro de la conexión SSH
        stdin, stdout, stderr = ssh_client.exec_command(disk_command)

        # Decodifica el valor y lo separa 
        disk_info = stdout.read().decode()
        print(disk_info)
        disk_size = disk_info.split()[1]

        # Conectarse a la base de datos
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # Insertar el tamaño en disco en la base de datos
        insert_query = 'INSERT INTO size_srv (srv, tam, fecha, path) VALUES (%s, %s, %s, %s)'
        data = (servidor, disk_size, fecha_actual, path)
        cursor.execute(insert_query, data)

        ssh_client.close()
        
        # Confirmar y cerrar la transacción
        connection.commit()
    except paramiko.AuthenticationException as e:
        print(f"Error de autenticación para {servidor}: {str(e)}")
        continue  # Continuar con el siguiente servidor en caso de error de autenticación
    except paramiko.SSHException as e:
        print(f"Error de SSH para {servidor}: {str(e)}")
        continue  # Continuar con el siguiente servidor en caso de error de SSH
    except Exception as e:
        print(f"Error desconocido para {servidor}: {str(e)}")
        continue  # Continuar con el siguiente servidor en caso de cualquier otro error
    
# Cerrar la conexión a la base de datos
connection.close()

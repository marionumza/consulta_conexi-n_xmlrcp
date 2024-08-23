import json
import xmlrpc.client
import ssl

def leer_datos_conexion():
    """Leer datos de conexión desde el archivo JSON"""
    try:
        with open('datos.json') as f:
            return json.load(f)
    except FileNotFoundError:
        print("El archivo datos.json no se encuentra.")
        return None
    except json.JSONDecodeError:
        print("Error al leer el archivo datos.json.")
        return None

def verificar_conexion(datos_conexion):
    """Verificar la conexión con la base de datos de Odoo"""
    url = datos_conexion.get('url')
    db = datos_conexion.get('db')
    username = datos_conexion.get('username')
    password = datos_conexion.get('password')

    try:
        # Crear contexto SSL predeterminado que valida certificados
        context = ssl.create_default_context()

        # Crear objeto de proxy de xmlrpc para autenticar con SSL seguro
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), context=context)
        version_info = common.version()

        if version_info:
            uid = common.authenticate(db, username, password, {})
            if uid:
                print("Conexión exitosa a la base de datos.")
                return True
            else:
                print("Error: No se pudo autenticar el usuario.")
                return False
        else:
            print("Error: No se pudo obtener la versión de Odoo.")
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Leer los datos de conexión desde el archivo datos.json
    datos_conexion = leer_datos_conexion()
    if datos_conexion:
        verificar_conexion(datos_conexion)

import pyodbc
import time

def conectar_base_datos(server, database, username, password):
    # Cadena de conexión
    connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    
    try:
        # Intentar establecer la conexión
        connection = pyodbc.connect(connection_string)

        # Crear un objeto cursor para ejecutar consultas
        cursor = connection.cursor()

        return connection, cursor

    except Exception as e:
        print(f'Error al conectar a la base de datos: {e}')
        return None, None

def obtener_siguiente_codigo(cursor):
    try:
        # Obtener el siguiente código sumándole 1 al valor máximo actual de la columna 'Codigo'
        cursor.execute('SELECT ISNULL(MAX(Codigo), 0) + 1 as SiguienteCodigo FROM irregulares')
        return cursor.fetchone().SiguienteCodigo

    except Exception as e:
        print(f'Error al obtener el siguiente código: {e}')
        return None

def mostrar_lista_completa(cursor):
    try:
        # Ejemplo de consulta para obtener todos los datos de la tabla 'irregulares'
        cursor.execute('SELECT Codigo, Infinitivo, Pasado_Simple, Participio_Pasado, Traduccion FROM irregulares')

        # Mostrar los resultados
        print("{:<10} {:<20} {:<20} {:<20} {:<20}".format('Codigo', 'Infinitivo', 'Pasado_Simple', 'Participio_Pasado', 'Traduccion'))
        print("="*90)
        for row in cursor.fetchall():
            print("{:<10} {:<20} {:<20} {:<20} {:<20}".format(row.Codigo, row.Infinitivo, row.Pasado_Simple, row.Participio_Pasado, row.Traduccion))

    except Exception as e:
        print(f'Error al recuperar y mostrar la lista: {e}')
    time.sleep(2)

def mostrar_verbos_por_letra(cursor):
    letra = input("\nIngrese una letra\n\n>> ")

    try:
        # Ejemplo de consulta para obtener los verbos que empiecen con la letra ingresada
        cursor.execute(f"SELECT Infinitivo FROM irregulares WHERE Infinitivo LIKE '{letra}%'")

        # Mostrar los resultados
        print(f"\nVerbos en infinitivo que empiezan con la letra '{letra}':\n")
        for row in cursor.fetchall():
            print(row.Infinitivo)

    except Exception as e:
        print(f'Error al recuperar y mostrar los verbos: {e}')
    time.sleep(2)

def mostrar_cantidad_letras_en_verbos(cursor):
    letra = input("\nIngrese una letra\n\n>> ")

    try:
        # Ejemplo de consulta para obtener los verbos y la cantidad de veces que aparece la letra ingresada
        cursor.execute(f"SELECT Infinitivo, LEN(Infinitivo) - LEN(REPLACE(Infinitivo, '{letra}', '')) as Cantidad FROM irregulares")

        # Mostrar los resultados
        print(f"\nCantidad de veces que aparece la letra '{letra}' en cada verbo:\n")
        for row in cursor.fetchall():
            print(f"{row.Infinitivo}:\t\t\t {row.Cantidad} ")

    except Exception as e:
        print(f'Error al recuperar y mostrar la cantidad de letras: {e}')
    time.sleep(2)

def mostrar_verbos_longitud(cursor):
    try:
        # Solicitar al usuario que ingrese un número
        longitud_ingresada = int(input("\nIngrese la longitud\n\n>>  "))

        # Ejemplo de consulta para obtener los verbos y verificar la condición
        cursor.execute(f"SELECT Infinitivo, CASE WHEN LEN(Infinitivo) <= {longitud_ingresada} THEN Infinitivo ELSE LEFT(Infinitivo, {longitud_ingresada}) END as Recortado, CASE WHEN LEN(Infinitivo) <= {longitud_ingresada} THEN 'True' ELSE 'False' END as CumpleCondicion FROM irregulares")

        # Mostrar los resultados
        print(f"\nVerbos en infinitivo hasta la longitud {longitud_ingresada}:")
        print("{:<20} {:<20} {:<20}".format('Infinitivo', 'Recortado', 'CumpleCondicion'))
        print("="*80)
        for row in cursor.fetchall():
            print("{:<20} {:<20} {:<20}".format(row.Infinitivo, row.Recortado, row.CumpleCondicion))

        for row in cursor.fetchall():
            if row.CumpleCondicion == 'True':
                print(row.Infinitivo)

    except ValueError:
        print("Por favor, ingrese un número válido.")

    except Exception as e:
        print(f'Error al recuperar y mostrar los verbos por longitud: {e}')
    time.sleep(3)

def agregar_verbo(cursor):
    try:
        # Obtener el siguiente código
        siguiente_codigo = obtener_siguiente_codigo(cursor)

        if siguiente_codigo is not None:
            # Solicitar al usuario los datos para el nuevo verbo
            infinitivo = input("Ingrese el verbo en infinitivo: ")
            pasado_simple = input("Ingrese el pasado simple: ")
            participio_pasado = input("Ingrese el participio pasado: ")
            traduccion = input("Ingrese la traducción: ")

            # Ejemplo de consulta para insertar el nuevo verbo en la base de datos
            cursor.execute(f"INSERT INTO irregulares (Codigo, Infinitivo, Pasado_Simple, Participio_Pasado, Traduccion) VALUES (?, ?, ?, ?, ?)",
                           (siguiente_codigo, infinitivo, pasado_simple, participio_pasado, traduccion))

            # Confirmar y aplicar los cambios en la base de datos
            cursor.commit()

            print(f"\n¡El verbo '{infinitivo}' ha sido agregado exitosamente con el código {siguiente_codigo}!")

    except Exception as e:
        print(f'Error al agregar el nuevo verbo: {e}')
    time.sleep(3)

def menu_principal():
    print("\n-------------- Menú Principal --------------\n")
    print("1. Mostrar Lista")
    print("2. Mostrar Verbos por Letra")
    print("3. Mostrar Cantidad de Letras en Verbos")
    print("4. Mostrar Verbos por Longitud")
    print("5. Agregar Nuevo Verbo")
    print("0. Salir")

def main():
    # Ingresa tus propios valores aquí
    server = 'LAPTOP-59IDB8MH'
    database = 'ingles'
    username = 'sa'
    password = 'Bogota21*'

    # Conectar a la base de datos
    connection, cursor = conectar_base_datos(server, database, username, password)

    if connection is None or cursor is None:
        return

    while True:
        # Mostrar el menú
        menu_principal()

        # Solicitar la elección del usuario
        opcion = input(f"\n>> ")

        # Procesar la elección del usuario
        if opcion == '1':
            mostrar_lista_completa(cursor)
        elif opcion == '2':
            mostrar_verbos_por_letra(cursor)
        elif opcion == '3':
            mostrar_cantidad_letras_en_verbos(cursor)
        elif opcion == '4':
            mostrar_verbos_longitud(cursor)
        elif opcion == '5':
            agregar_verbo(cursor)
        elif opcion == '0':
            # Cerrar la conexión y salir del programa
            cursor.close()
            connection.close()
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, ingrese una opción válida.")

if __name__ == "__main__":
    main()

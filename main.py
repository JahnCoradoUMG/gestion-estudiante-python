import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
# Función para conectar a la base de datos PostgreSQL
def conectar_db():
    conn = psycopg2.connect(
        database=os.environ.get("POSTGRES_DB"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host=os.environ.get("POSTGRES_HOST"),
        port=5432
    )
    return conn

# CRUD de estudiantes

def insertar_estudiante(nombre, apellido, carnet):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        sql = '''
        INSERT INTO estudiantes (nombre, apellido, carnet)
        VALUES (%s, %s, %s);
        '''
        cursor.execute(sql, (nombre, apellido, carnet))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error al insertar el estudiante:", error)
    finally:
        if conn:
            conn.close()

def consultar_estudiante_por_carnet(carnet):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        sql = "SELECT * FROM estudiantes WHERE carnet = %s;"
        cursor.execute(sql, (carnet,))
        estudiante = cursor.fetchone()
        conn.close()
        return estudiante
    except (Exception, psycopg2.Error) as error:
        print("Error al consultar el estudiante:", error)
        return None
    

def actualizar_estudiante(nombre, apellido, carnet):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        sql = "UPDATE estudiantes SET nombre = %s, apellido = %s WHERE carnet = %s;"
        cursor.execute(sql, (nombre, apellido, carnet))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error al actualizar el estudiante:", error)
    finally:
        if conn:
            conn.close()

def eliminar_estudiante(carnet):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        sql = "DELETE FROM estudiantes WHERE carnet = %s;"
        cursor.execute(sql, (carnet,))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error al eliminar el estudiante:", error)
    finally:
        if conn:
            conn.close()

#CRUD de cursos

#Gestión de Estudiantes y Cursos: inscribir estudiante a curso, editar inscripcion, eliminar inscripcion, y buscar inscripcion.

#Busquedas Por nombre, carnet, código de curso, y ver alumnos en cursos.

#Reportes
def consultar_alumnos_con_mejores_notas():
    conn = conectar_db()
    cursor = conn.cursor()
    sql = '''
    SELECT e.carnet, e.nombre, e.apellido, SUM(n.parcial1 + n.parcial2 + n.examen_final + n.zona) AS total_nota
    FROM estudiantes e
    INNER JOIN inscripciones i ON e.id_estudiante = i.id_estudiante
    INNER JOIN notas n ON i.id_inscripcion = n.id_inscripcion
    GROUP BY e.carnet, e.nombre, e.apellido
    ORDER BY total_nota DESC
    LIMIT 10;
    '''
    cursor.execute(sql)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def consultar_promedios():
    conn = conectar_db()
    cursor = conn.cursor()
    sql = '''
    SELECT c.nombre, e.nombre, e.apellido, AVG(n.parcial1 + n.parcial2 + n.examen_final + n.zona) AS promedio
    FROM estudiantes e
    INNER JOIN inscripciones i ON e.id_estudiante = i.id_estudiante
    INNER JOIN notas n ON i.id_inscripcion = n.id_inscripcion
    INNER JOIN cursos c ON i.id_curso = c.id_curso
    GROUP BY e.id_estudiante, c.id_curso
    LIMIT 10;
    '''
    cursor.execute(sql)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def consultar_alumnos_con_notas_faltantes():
    conn = conectar_db()
    cursor = conn.cursor()
    sql = '''
    SELECT e.carnet, e.nombre, e.apellido, n.parcial1, n.parcial2, n.examen_final, n.zona
    FROM estudiantes e
    INNER JOIN inscripciones i ON e.id_estudiante = i.id_estudiante
    INNER JOIN notas n ON i.id_inscripcion = n.id_inscripcion
    WHERE n.parcial1 IS NULL OR n.parcial2 IS NULL OR n.examen_final IS NULL OR n.zona IS NULL;
    '''
    cursor.execute(sql)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# En el menú, agrega opciones para las nuevas funcionalidades
def menu():
    while True:
        print("1. Agregar estudiante")
        print("2. Consultar estudiante por carnet")
        print("3. Actualizar estudiante")
        print("4. Eliminar estudiante")
        print("5. Reporte alumnos con mejores notas")
        print("6. Reporte promedio de alumnos por curso")
        print("7. Reporte alumnos con notas faltantes")
        print("8. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            carnet = input("Ingrese el carnet del estudiante: ")
            carrera = input("Ingrese la carrera del estudiante: ")
            nombre = input("Ingrese el nombre del estudiante: ")
            insertar_estudiante(carnet, carrera, nombre)
            print("Estudiante insertado exitosamente.")
        
        elif opcion == '2':
            carnet = input("Ingrese el carnet del estudiante: ")
            estudiantes = consultar_estudiante_por_carnet(carnet)
            print("Lista de estudiantes:")
            for est in estudiantes:
                print(f"Carnet: {est[0]}, Carrera: {est[1]}, Nombre: {est[2]}")
        
        elif opcion == '3':
            carnet = input("Ingrese el carnet del estudiante a actualizar: ")
            nueva_carrera = input("Ingrese la nueva carrera: ")
            actualizar_estudiante(carnet, nueva_carrera)
            print("Estudiante actualizado exitosamente.")
        
        elif opcion == '4':
            carnet = input("Ingrese el carnet del estudiante a eliminar: ")
            eliminar_estudiante(carnet)
            print("Estudiante eliminado exitosamente.")

        elif opcion == '5':
            alumnos_con_mejores_notas = consultar_alumnos_con_mejores_notas()
            print("Alumnos con mejores a peores notas:")
            for alumno in alumnos_con_mejores_notas:
                print(f"Carnet: {alumno[0]}, Nombre: {alumno[1]}, Apellido: {alumno[2]}, Total de Nota: {alumno[3]}")
        
        elif opcion == '6':
            promedios_alumnos = consultar_promedios()
            print("Promedios por curso y estudiante:")
            for alumno in promedios_alumnos:
                print(f"Curso: {alumno[0]}, Nombre: {alumno[1]}, Apellido: {alumno[2]}, Promedio: {alumno[3]}")

        elif opcion == '7':
            alumnos_con_notas_faltantes = consultar_alumnos_con_notas_faltantes()
            print("Alumnos con notas faltantes:")
            for alumno in alumnos_con_notas_faltantes:
                print(f"Carnet: {alumno[0]}, Nombre: {alumno[1]}, Apellido: {alumno[2]}, Parcial 1: {alumno[3]}, Parcial 2: {alumno[4]}, Examen Final: {alumno[5]}, Zona: {alumno[6]}")

        elif opcion == '8':
            print("Saliendo del sistema. ¡Hasta luego!")
            break
        
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
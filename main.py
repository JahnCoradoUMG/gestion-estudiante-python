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
        port=os.environ.get("CONN_PORT")
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

#Consultar todos los estudiantes
def consultar_todos_estudiantes():
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        sql = "SELECT * FROM estudiantes;"
        cursor.execute(sql)
        estudiantes = cursor.fetchall()
        conn.close()
        return estudiantes
    except (Exception, psycopg2.Error) as error:
        print("Error al consultar los estudiantes:", error)
        return None

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
        # Conectarse a la base de datos
        conn = conectar_db()
        cursor = conn.cursor()

        # Consultar el ID del estudiante a partir del carnet
        estudiante = consultar_estudiante_por_carnet(carnet)
        
        # Verifica que el estudiante exista
        if estudiante is None:
            print("Estudiante no encontrado.")
            return
        
        # Obtener el id del estudiante
        id_estudiante = estudiante[0]
        
        # Eliminar las notas relacionadas al estudiante a través de inscripciones
        sql = """
            DELETE FROM notas 
            WHERE id_inscripcion IN (
                SELECT id_inscripcion FROM inscripciones WHERE id_estudiante = %s
            );
        """
        cursor.execute(sql, (id_estudiante,))
        conn.commit()
        
        # Eliminar las inscripciones relacionadas al estudiante
        sql = "DELETE FROM inscripciones WHERE id_estudiante = %s;"
        cursor.execute(sql, (id_estudiante,))
        conn.commit()

        # Eliminar el estudiante de la base de datos
        sql = "DELETE FROM estudiantes WHERE id_estudiante = %s;"
        cursor.execute(sql, (id_estudiante,))
        conn.commit()

        print("Estudiante eliminado exitosamente.")

    except (Exception, psycopg2.Error) as error:
        print("Error al eliminar el estudiante:", error)

    finally:
        # Cerrar la conexión a la base de datos
        if conn:
            cursor.close()
            conn.close()


# CRUD de cursos

def obtener_todos_cursos():
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        sql = "SELECT * FROM cursos;"
        cursor.execute(sql)
        cursos = cursor.fetchall()
        conn.close()
        return cursos
    except (Exception, psycopg2.Error) as error:
        print("Error al consultar los cursos:", error)
        return None
    finally:
        if conn:
            conn.close()

def insertar_curso(nombre, codigo):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        sql = '''
        INSERT INTO cursos (nombre, codigo)
        VALUES (%s, %s);
        '''
        cursor.execute(sql, (nombre, codigo))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error al insertar el curso:", error)
    finally:
        if conn:
            conn.close()

def consultar_curso_por_codigo(codigo):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        sql = "SELECT * FROM cursos WHERE codigo = %s;"
        cursor.execute(sql, (codigo,))
        curso = cursor.fetchone()
        conn.close()
        return curso
    except (Exception, psycopg2.Error) as error:
        print("Error al consultar el curso:", error)
        return None

def eliminar_curso(codigo):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id_curso FROM cursos WHERE codigo = %s;", (codigo,))
        curso = cursor.fetchone()
        
        if curso is None:
            print("Curso no encontrado.")
            return
        
        id_curso = curso[0]
        
        sql = """
            DELETE FROM notas 
            WHERE id_inscripcion IN (
                SELECT id_inscripcion FROM inscripciones WHERE id_curso = %s
            );
        """
        cursor.execute(sql, (id_curso,))
        conn.commit()
        
        sql = "DELETE FROM inscripciones WHERE id_curso = %s;"
        cursor.execute(sql, (id_curso,))
        conn.commit()
        
        sql = "DELETE FROM cursos WHERE id_curso = %s;"
        cursor.execute(sql, (id_curso,))
        conn.commit()
        
        print("Curso eliminado exitosamente.")
    
    except (Exception, psycopg2.Error) as error:
        print("Error al eliminar el curso:", error)
    
    finally:
        if conn:
            cursor.close()
            conn.close()

# CRUD de notas
def registrar_notas(id_inscripcion, parcial1, parcial2, examen_final, zona):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        sql = '''
        INSERT INTO notas (id_inscripcion, parcial1, parcial2, examen_final, zona)
        VALUES (%s, %s, %s, %s, %s);
        '''
        cursor.execute(sql, (id_inscripcion, parcial1, parcial2, examen_final, zona))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error al registrar las notas:", error)
    finally:
        if conn:
            conn.close()

# Reportes

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

# Menú de opciones
def menu():
    while True:
        print("----------------------------------------------------")
        print("0. Consultar todos los estudiantes")
        print("1. Agregar estudiante")
        print("2. Consultar estudiante por carnet")
        print("3. Actualizar estudiante")
        print("4. Eliminar estudiante")
        print("5. Agregar curso")
        print("6. Consultar curso por código")
        print("7. Eliminar curso")
        print("8. Registrar notas")
        print("9. Reporte alumnos con mejores notas")
        print("10. Reporte promedio de alumnos por curso")
        print("11. Reporte alumnos con notas faltantes")
        print("12. Salir")
        print("----------------------------------------------------")
        
        opcion = input("Seleccione una opción: ")

        if opcion == '0':
            estudiantes = consultar_todos_estudiantes()
            for estudiante in estudiantes:
                print(f"Carnet: {estudiante[3]}, Nombre: {estudiante[1]}, Apellido: {estudiante[2]}")

        if opcion == '1':
            nombre = input("Ingrese el nombre del estudiante: ")
            apellido = input("Ingrese el apellido del estudiante: ")
            carnet = input("Ingrese el carnet del estudiante: ")
            insertar_estudiante(nombre, apellido, carnet)
            print("Estudiante insertado exitosamente.")
        
        elif opcion == '2':
            carnet = input("Ingrese el carnet del estudiante: ")
            estudiante = consultar_estudiante_por_carnet(carnet)
            if estudiante:
                print(f"Estudiante encontrado: {estudiante}")
            else:
                print("Estudiante no encontrado.")
        
        elif opcion == '3':
            estudiantes = consultar_todos_estudiantes()
            for estudiante in estudiantes:
                print(f"Carnet: {estudiante[3]}, Nombre: {estudiante[1]}, Apellido: {estudiante[2]}")
            carnet = input("Ingrese el carnet del estudiante a actualizar: ")
            nombre = input("Ingrese el nuevo nombre del estudiante: ")
            apellido = input("Ingrese el nuevo apellido del estudiante: ")
            actualizar_estudiante(nombre, apellido, carnet)
            print("++++++++++++ Estudiante actualizado exitosamente. +++++++++++++++++")
        
        elif opcion == '4':
            #Se mostraran los nombres de los estudiantes con el carnet
            estudiantes = consultar_todos_estudiantes()
            for estudiante in estudiantes:
                print(f"Carnet: {estudiante[3]}, Nombre: {estudiante[1]}, Apellido: {estudiante[2]}")
            carnet = input("Ingrese el carnet del estudiante a eliminar: ")
            isTrue = input("Seguro que quiere eliminar este estudiante? y/n")
            if isTrue == 'y':
                eliminar_estudiante(carnet)
            else:
                print("Operación cancelada.")

        elif opcion == '5':
            nombre = input("Ingrese el nombre del curso: ")
            codigo = input("Ingrese el código del curso: ")
            insertar_curso(nombre, codigo)
            print("Curso insertado exitosamente.")
        
        elif opcion == '6':
            codigo = input("Ingrese el código del curso: ")
            curso = consultar_curso_por_codigo(codigo)
            if curso:
                print(f"Curso encontrado: {curso}")
            else:
                print("Curso no encontrado.")
        
        elif opcion == '7':
            cursos = obtener_todos_cursos()
            for curso in cursos:
                print(f"Código: {curso[2]}, Nombre: {curso[1]}")
            codigo = input("Ingrese el código del curso a eliminar: ")
            isTrue = input("Seguro que quiere eliminar este curso? y/n")
            if isTrue == 'y':
                eliminar_curso(codigo)
            else:
                print("Operación cancelada.")
        
        elif opcion == '8':
            id_inscripcion = input("Ingrese el ID de inscripción: ")
            parcial1 = float(input("Ingrese la calificación del primer parcial: "))
            parcial2 = float(input("Ingrese la calificación del segundo parcial: "))
            examen_final = float(input("Ingrese la calificación del examen final: "))
            zona = float(input("Ingrese la calificación de la zona: "))
            registrar_notas(id_inscripcion, parcial1, parcial2, examen_final, zona)
            print("Notas registradas exitosamente.")
        
        elif opcion == '9':
            alumnos_con_mejores_notas = consultar_alumnos_con_mejores_notas()
            print("Alumnos con mejores notas:")
            for alumno in alumnos_con_mejores_notas:
                print(f"Carnet: {alumno[0]}, Nombre: {alumno[1]}, Apellido: {alumno[2]}, Total de Nota: {alumno[3]}")
        
        elif opcion == '10':
            promedios = consultar_promedios()
            print("Promedio de alumnos por curso:")
            for promedio in promedios:
                print(f"Curso: {promedio[0]}, Nombre: {promedio[1]}, Apellido: {promedio[2]}, Promedio: {promedio[3]}")
        
        elif opcion == '11':
            alumnos_con_notas_faltantes = consultar_alumnos_con_notas_faltantes()
            print("Alumnos con notas faltantes:")
            for alumno in alumnos_con_notas_faltantes:
                print(f"Carnet: {alumno[0]}, Nombre: {alumno[1]}, Apellido: {alumno[2]}, Parcial 1: {alumno[3]}, Parcial 2: {alumno[4]}, Examen Final: {alumno[5]}, Zona: {alumno[6]}")

        elif opcion == '12':
            print("Saliendo del sistema. ¡Hasta luego!")
            break
        
        else:
            if(opcion != '0'):
                print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()

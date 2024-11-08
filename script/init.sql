-- Crear la tabla de estudiantes
CREATE TABLE estudiantes (
    id_estudiante SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    carnet VARCHAR(20) UNIQUE NOT NULL
);

-- Crear la tabla de cursos
CREATE TABLE cursos (
    id_curso SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(20) UNIQUE NOT NULL
);

-- Tabla de inscripciones
CREATE TABLE inscripciones (
    id_inscripcion SERIAL PRIMARY KEY,
    id_estudiante INTEGER REFERENCES estudiantes(id_estudiante),
    id_curso INTEGER REFERENCES cursos(id_curso),
    fecha_inscripcion DATE
);

-- Crear la tabla de notas
CREATE TABLE notas (
    id_nota SERIAL PRIMARY KEY,
    id_inscripcion INTEGER REFERENCES inscripciones(id_inscripcion),
    parcial1 NUMERIC(5,2),
    parcial2 NUMERIC(5,2),
    examen_final NUMERIC(5,2),
    zona NUMERIC(5,2)
);

-- Insertar datos de estudiantes
INSERT INTO estudiantes (nombre, apellido, carnet) 
VALUES 
    ('Ana', 'García', '2890-23-16932'),
    ('Juan', 'Pérez', '2890-23-32533');

-- Insertar datos de cursos
INSERT INTO cursos (nombre, codigo) 
VALUES 
    ('Bases de Datos', 'BD101'),
    ('Programación', 'PROG101');

-- Insertar datos de inscripciones
INSERT INTO inscripciones (id_estudiante, id_curso, fecha_inscripcion) 
VALUES 
    (1, 1, '2023-11-01'),  -- Ana se inscribe en Bases de Datos
    (2, 1, '2023-11-01'),  -- Juan se inscribe en Bases de Datos
    (2, 2, '2023-11-01');  -- Juan se inscribe en Programación

-- Insertar datos de notas
INSERT INTO notas (id_inscripcion, parcial1, parcial2, examen_final, zona) 
VALUES 
    (1, 12, 15, 25, 38),  -- Notas para la inscripción de Ana en Bases de Datos
    (2, 10, 12, 20, 28),  -- Notas para la inscripción de Juan en Bases de Datos
    (3, 13, 14, 27, 40);  -- Notas para la inscripción de Juan en Programación

import sqlite3

# Creamos la conexión a la base de datos
conn = sqlite3.connect('academico.db')

# Creamos la tabla "alumno"
conn.execute('''CREATE TABLE alumno
             (CI INT PRIMARY KEY NOT NULL,
             Nombre TEXT NOT NULL,
             Apellido TEXT NOT NULL,
             fecha_nac DATE NOT NULL);''')

# Creamos la tabla "asignatura"
conn.execute('''CREATE TABLE asignatura
             (Sigla TEXT PRIMARY KEY NOT NULL,
             Nombre TEXT NOT NULL,
             Semestre TEXT NOT NULL);''')

# Creamos la tabla "alumno_asignatura"
conn.execute('''CREATE TABLE alumno_asignatura
             (Ci INT NOT NULL,
             Sigla TEXT NOT NULL,
             nota1 FLOAT,
             nota2 FLOAT,
             notafinal FLOAT,
             PRIMARY KEY (Ci, Sigla),
             FOREIGN KEY (Ci) REFERENCES alumno(CI),
             FOREIGN KEY (Sigla) REFERENCES asignatura(Sigla));''')

# Insertamos datos
conn.execute("INSERT INTO alumno (CI, Nombre, Apellido, fecha_nac) VALUES (1234567, 'Juan', 'Pérez', '1995-07-12');")
conn.execute("INSERT INTO alumno (CI, Nombre, Apellido, fecha_nac) VALUES (7654321, 'Pedro', 'Lopez', '2002-08-05');")

conn.execute("INSERT INTO asignatura (Sigla, Nombre, Semestre) VALUES ('INF-324', 'Programación Funcional', 'Optativa');")
conn.execute("INSERT INTO asignatura (Sigla, Nombre, Semestre) VALUES ('INF-273', 'Telemática', 'Septimo');")

conn.execute("INSERT INTO alumno_asignatura (Ci, Sigla, nota1, nota2, notafinal) VALUES (1234567, 'INF-273', 0, 20, 20);")
conn.execute("INSERT INTO alumno_asignatura (Ci, Sigla, nota1, nota2, notafinal) VALUES (7654321, 'INF-324', 20, 20, 40);")

# Hacemos commit para guardar los cambios en la base de datos
conn.commit()

# Cerramos la conexión a la base de datos
conn.close()

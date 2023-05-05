import socket
import sqlite3

def create_table():
    # Conexión a la base de datos
    conn = sqlite3.connect('academico.db')

    # Creación de tabla alumno si no existe
    conn.execute('''CREATE TABLE IF NOT EXISTS alumno
                     (CI INT PRIMARY KEY NOT NULL,
                         Nombre TEXT NOT NULL,
                         Apellido TEXT NOT NULL,
                         fecha_nac DATE NOT NULL);''')
    #asignatura
    conn.execute('''CREATE TABLE IF NOT EXISTS asignatura
                     (Sigla TEXT PRIMARY KEY NOT NULL,
             Nombre TEXT NOT NULL,
             Semestre TEXT NOT NULL);''')
    #alumno_asignatura
    conn.execute('''CREATE TABLE IF NOT EXISTS alumno_asignatura
                      (Ci INT NOT NULL,
             Sigla TEXT NOT NULL,
             nota1 FLOAT,
             nota2 FLOAT,
             notafinal FLOAT,
             PRIMARY KEY (Ci, Sigla),
             FOREIGN KEY (Ci) REFERENCES alumno(CI),
             FOREIGN KEY (Sigla) REFERENCES asignatura(Sigla));''')
    # Cerramos la conexión
    conn.close()
#mostrar tabla alumno

def select_alumnos():
    # Conexión a la base de datos
    conn = sqlite3.connect('academico.db')

    # Consulta de todos los alumnos
    cursor = conn.execute('SELECT * FROM alumno')

    # Generación de tabla HTML con los resultados
    html = '<table><tr><th>CI</th><th>Nombre</th><th>Apellido</th><th>Fecha de nacimiento</th></tr>'
    for row in cursor:
        html += f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>'
    html += '</table>'

    # Cerramos la conexión
    conn.close()

    return html

#mostrar asignaturas
def select_asignatura():
    # Conexión a la base de datos
    conn = sqlite3.connect('academico.db')

    # Consulta de todos los alumnos
    cursor = conn.execute('SELECT * FROM asignatura')

    # Generación de tabla HTML con los resultados
    html = '<table><tr><th>Sigla</th><th>Nombre</th><th>Semestre</th></tr>'
    for row in cursor:
        html += f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>'
    html += '</table>'

    # Cerramos la conexión
    conn.close()

    return html

def insert_alumno(Ci, Nombre, Apellido, fecha_nac):
    # Conexión a la base de datos
    conn = sqlite3.connect('academico.db')

    # Inserción de contacto
    conn.execute(f"INSERT INTO alumno (CI, Nombre, Apellido, fehca_nac) \
                   VALUES ('{Ci}', '{Nombre}', '{Apellido}','{fecha_nac}');")

    # Guardamos los cambios
    conn.commit()

    # Cerramos la conexión
    conn.close()

def main():
    # Creamos un objeto de socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configuramos la dirección y el puerto del servidor
    server_address = ('localhost', 1234)

    # Enlazamos el socket al puerto y dirección del servidor
    server_socket.bind(server_address)

    # Empezamos a escuchar las solicitudes de los clientes
    server_socket.listen(1)

    print(f'Servidor escuchando en {server_address[0]}:{server_address[1]}')

    # Creamos la tabla de contactos
    create_table()

    while True:
        # Esperamos a que llegue una conexión
        client_socket, client_address = server_socket.accept()

        # Leemos la solicitud del cliente
        request = client_socket.recv(1024).decode('utf-8')

        # Imprimimos la solicitud del cliente
        print(f'Solicitud recibida desde {client_address[0]}:{client_address[1]}:')
        print(request)


        #codigo para mostrar tabla alumno en pagina web
        html = select_alumnos()
        response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'
        response += html
        client_socket.sendall(response.encode())


        #codigo para mostrar tabla asignatura en pagina web
        html = select_asignatura()
        response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'
        response += html
        client_socket.sendall(response.encode())

        # Cargamos el archivo HTML
        with open('index.html', 'r') as file:
            html = file.read()

        if request.startswith('POST'):
            # Si la solicitud es un POST, obtenemos los datos del formulario
            Ci = request.split('\r\n')[-1]
            nombre = data.split('&')[0].split('=')[1]
            apellido = data.split('&')[1].split('=')[1]
            fecha_nac = data.split('&')[2].split('=')[1]

            # Insertamos el contacto en la base de datos
            insert_alumno(Ci,nombre, apellido, fecha_nac)

            # Agregamos un mensaje de confirmación al HTML
            html += '<p>Alumno enviado correctamente.</p>'

        # Creamos una respuesta HTTP para el cliente
        response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'
        response += html

        # Enviamos la respuesta al cliente
        client_socket.sendall(response.encode())

        # Cerramos la conexión con el cliente
        client_socket.close()

if __name__ == '__main__':
    main()

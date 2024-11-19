import mysql.connector
from mysql.connector import Error
from usuarios import Usuario  # Importamos la clase Usuario
from seguidores import Seguir
from publicaciones import Publicaciones
class InstagramApp:
    def __init__(self):
        self.connection = None
        self.usuario_actual = None  # Usuario autenticado

    def conectar_db(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='instagram',
                user='root',
                password='',
                port="3306"
            )
            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.connection = None

    def cerrar_conexion(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada.")

    def mostrar_menu_principal(self):
        print("\nMenú Principal:")
        print("1. Iniciar Sesión")
        print("2. Crear Cuenta")
        print("3. Salir")

    def mostrar_menu_usuario(self):
        print(f"\nBienvenido, {self.usuario_actual['nombre_usuario']}!")
        print("1. Ver perfiles")
        print("2. Editar perfil")
        print("3. Hacer una publicación")
        print("4. Acceder a menú de seguidores")
        print("5. Cerrar sesión")

    def mostrar_menu_seguidores(self):
        print("\nMenú Seguidores:")
        print("1. Seguir a un usuario")
        print("2. Ver seguidores de un perfil")
        print("3. Regresar al menú anterior")

    def iniciar_sesion(self):
        try:
            usuario = input("Nombre de usuario: ").strip()
            contraseña = input("Contraseña: ").strip()

            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND contraseña_hash = %s"
            cursor.execute(query, (usuario, contraseña))
            resultado = cursor.fetchone()

            if resultado:
                self.usuario_actual = resultado
                print(f"Inicio de sesión exitoso. Bienvenido, {usuario}!")
                return True
            else:
                print("Nombre de usuario o contraseña incorrectos.")
        except Error as e:
            print(f"Error al iniciar sesión: {e}")
        return False

    def crear_cuenta(self):
        try:
            nombre_usuario = input("Nombre de usuario: ").strip()
            correo_electronico = input("Correo electrónico: ").strip()
            contraseña = input("Contraseña: ").strip()
            if not nombre_usuario or not correo_electronico or not contraseña:
                print("Todos los campos son obligatorios.")
                return

            usuario = Usuario(self.connection)
            usuario.crear_perfil(
                nombre_usuario=nombre_usuario,
                correo_electronico=correo_electronico,
                contraseña_hash=contraseña  # Reemplazar con encriptación
            )
            print(f"Cuenta creada exitosamente para {nombre_usuario}.")
        except Error as e:
            print(f"Error al crear la cuenta: {e}")

    def ejecutar_menu_seguidores(self):
        while True:
            self.mostrar_menu_seguidores()
            opcion = input("Elige una opción: ")

            if opcion == "1":  # Seguir a un usuario
                seguir = Seguir(self.connection)
                id_usuario_seguido = input("Ingrese el ID del usuario a seguir: ").strip()
                seguir.seguir_usuario(
                    id_seguidor=self.usuario_actual["id_usuario"],
                    id_seguido=id_usuario_seguido
                )
            elif opcion == "2":  # Ver seguidores de un perfil
                pass
            elif opcion == "3":  # Regresar al menú anterior
                break
            else:
                print("Opción no válida, intenta de nuevo.")

    def ejecutar_menu_usuario(self):
        while self.usuario_actual:
            self.mostrar_menu_usuario()
            opcion = input("Elige una opción: ")

            if opcion == '1':  # Ver perfiles
                usuario = Usuario(self.connection)
                usuario.ver_perfiles()
            elif opcion == '2':  # Editar perfil
                print("Función de edición de perfil no implementada todavía.")
            elif opcion == '3':  # Hacer una publicación
                url_imagen = input("URL de la imagen (opcional): ").strip()
                descripcion = input("Descripción: ").strip()
                etiquetas = input("Etiquetas (separadas por comas): ").split(',')

                publicaciones = Publicaciones(self.connection)
                publicaciones.hacer_publicacion(
                    id_usuario=self.usuario_actual["id_usuario"],
                    url_imagen=url_imagen,
                    descripcion=descripcion,
                    etiquetas=[etiqueta.strip() for etiqueta in etiquetas]
                )
            elif opcion == '4':  # Acceder a menú de seguidores
                self.ejecutar_menu_seguidores()
            elif opcion == '5':  # Cerrar sesión
                print(f"Sesión cerrada. Adiós, {self.usuario_actual['nombre_usuario']}!")
                self.usuario_actual = None
            else:
                print("Opción no válida, intenta de nuevo.")

    def ejecutar_menu_principal(self):
        while True:
            self.mostrar_menu_principal()
            opcion = input("Elige una opción: ")

            if opcion == '1':  # Iniciar sesión
                if self.iniciar_sesion():
                    self.ejecutar_menu_usuario()
            elif opcion == '2':  # Crear cuenta
                self.crear_cuenta()
            elif opcion == '3':  # Salir
                self.cerrar_conexion()
                break
            else:
                print("Opción no válida, intenta de nuevo.")

    def run(self):
        self.conectar_db()
        if not self.connection:
            return
        self.ejecutar_menu_principal()

if __name__ == "__main__":
    app = InstagramApp()
    app.run()

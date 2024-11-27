import mysql.connector
from usuarios import Usuario
from publicaciones import Publicaciones
from historias import Historias
from seguidores import Seguir
import getpass

class Instagram:
    def __init__(self):
        self.conexion = None
        self.usuario_manager = None
        self.publicaciones_manager = None
        self.historias_manager = None
        self.seguidores_manager = None
        self.usuario_actual = None

    def conectar_db(self):
        """Establece conexión con la base de datos."""
        try:
            self.conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="instagram"
            )
            print("Conexión exitosa a la base de datos.")
        except mysql.connector.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.conexion = None
    
    def verificar_sesion(self):
    #Verifica si el usuario ha iniciado sesión
        if self.usuario_actual is None:
            print("No has iniciado sesión. Por favor, inicia sesión primero.")
            return False  # Si no está autenticado, regresa False
        return True  # Si está autenticado, regresa True


    def inicializar_managers(self):
        """Crea instancias de los manejadores."""
        self.usuario_manager = Usuario(self.conexion)
        self.publicaciones_manager = Publicaciones(self.conexion)
        self.historias_manager = Historias(self.conexion)
        self.seguidores_manager = Seguir(self.conexion)

    def confirmar_accion(self,mensaje):
        """Pregunta al usuario si está seguro de realizar una acción."""
        while True:
            confirmacion = input(f"{mensaje} (S/N): ").strip().upper()
            if confirmacion == "S":
                return True
            elif confirmacion == "N":
                return False
            else:
                print("Respuesta inválida. Por favor, ingresa 'S' para Sí o 'N' para No.")

    def registrar_usuario(self):
        print("\n--- Registrar Usuario ---")
        nombre = input("Nombre: ")
        apellidos = input("Apellidos: ")
        nombre_usuario = input("Nombre de usuario: ")
        correo = input("Correo electrónico: ")
        contraseña = getpass.getpass("Contraseña: ")
        fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")
        url_imagen_perfil = input("URL de imagen de perfil (opcional): ")
        self.usuario_manager.crear_perfil(
            nombre, apellidos, nombre_usuario, correo, contraseña, fecha_nacimiento, url_imagen_perfil
        )

    def menu_usuario(self):
        # Verificar si el usuario ha iniciado sesión antes de mostrar el menú
        if not self.verificar_sesion():
            print("Por favor Inicia Sesión")
            self.menu_principal()  # Redirige al menú principal
            return  # Termina la ejecución de este método si no hay sesión activa

        while True:
            print(f"\n--- Bienvenido, {self.usuario_actual['nombre_usuario']} ---")
            print("1. Ver mi perfil")
            print("2. Ver publicaciones")
            print("3. Ver historias")
            print("4. Listar usuarios")
            print("5. Cerrar sesión")
            opcion = input("Elige una opción: ")

            if opcion == "1":
                self.menu_mi_perfil()
            elif opcion == "2":
                self.publicaciones_manager.ver_todas_publicaciones()
            elif opcion == "3":
                self.historias_manager.ver_todas_historias()
            elif opcion == "4":
                self.menu_listar_usuarios()
            elif opcion == "5":
                self.usuario_actual = None
                print("Sesión cerrada.")
                self.menu_principal()  # Redirige al menú principal
                break
            else:
                print("Opción inválida, intenta de nuevo.")


    def menu_mi_perfil(self):
        while True:
            print("\n--- Mi Perfil ---")
            print(f"Nombre: {self.usuario_actual['nombre']}")
            print(f"Apellidos: {self.usuario_actual['apellidos']}")
            print(f"Nombre de usuario: {self.usuario_actual['nombre_usuario']}")
            print(f"Fecha de nacimiento: {self.usuario_actual['fecha_nacimiento']}")
            print(f"Seguidores: {self.usuario_manager.obtener_cantidad_seguidores(self.usuario_actual['id_usuario'])}")
            print(f"Seguidos: {self.usuario_manager.obtener_cantidad_seguidos(self.usuario_actual['id_usuario'])}")
            print("\n1. Editar perfil")
            print("2. Gestionar publicaciones")
            print("3. Gestionar historias")
            print("4. Ver seguidores")
            print("5. Ver seguidos")
            print("6. Elimimar mi cuenta permanentemente")
            print("7. Volver atrás")
            opcion = input("Elige una opción: ")

            if opcion == "1":
                if self.usuario_manager.editar_perfil(self.usuario_actual["id_usuario"]):
                    print("Perfil actualizado. Regresando al menú principal...")
                    self.menu_principal()
                    break
                
            elif opcion == "2":
                self.menu_gestionar_publicaciones()
            elif opcion == "3":
                self.menu_gestionar_historias()
            elif opcion == "4":
                self.usuario_manager.ver_seguidores(self.usuario_actual['id_usuario'])
            elif opcion == "5":
                self.usuario_manager.ver_seguidos(self.usuario_actual['id_usuario'])
            elif opcion == "6":
                eliminado = self.usuario_manager.eliminar_mi_cuenta(self.usuario_actual['id_usuario'])
                if eliminado:
                    print("Redirigiendo al menú principal...")
                    return self.menu_principal()  # Redirigir y salir del menú
            elif opcion == "7":
                break
            else:
                print("Opción inválida, intenta de nuevo.")

    def menu_gestionar_publicaciones(self):
        while True:
            print("\n--- Gestionar Publicaciones ---")
            print("1. Ver mis publicaciones")
            print("2. Crear publicación")
            print("3. Editar publicaciones")
            print("4. Eliminar publicaciones")
            print("5. Volver atrás")
            opcion = input("Elige una opción: ")

            if opcion == "1":
                self.publicaciones_manager.ver_publicaciones(self.usuario_actual['id_usuario'])
            elif opcion == "2":
                url_imagen = input("URL de la imagen o video: ")
                descripcion = input("Descripción: ")
                hashtags = input("Hashtags: ")
                self.publicaciones_manager.hacer_publicacion(self.usuario_actual['id_usuario'], url_imagen, descripcion, hashtags)
            elif opcion == "3":
                id_publicacion = int(input("ID de la publicación a editar: "))
                nuevo_contenido = input("Nueva descripción: ")
                nuevo_hashtags = input("Nuevos hashtags (opcional): ")
                self.publicaciones_manager.actualizar_publicacion(id_publicacion, nuevo_contenido, nuevo_hashtags)
            elif opcion == "4":
                id_publicacion = int(input("ID de la publicación a eliminar: "))
                self.publicaciones_manager.eliminar_publicacion(id_publicacion)
            elif opcion == "5":
                break
            else:
                print("Opción inválida, intenta de nuevo.")

    def menu_gestionar_historias(self):
        while True:
            print("\n--- Gestionar Historias ---")
            print("1. Ver mis historias")
            print("2. Crear historia")
            print("3. Eliminar historias")
            print("4. Volver atrás")
            opcion = input("Elige una opción: ")

            if opcion == "1":
                self.historias_manager.ver_historias(self.usuario_actual['id_usuario'])
            elif opcion == "2":
                imagen_video = input("URL de la imagen o video: ")
                texto = input("Texto de la historia: ")
                duracion = int(input("Duración en segundos: "))
                self.historias_manager.crear_historia(self.usuario_actual['id_usuario'], imagen_video, texto, duracion)
            elif opcion == "3":
                id_historia = int(input("ID de la historia a eliminar: "))
                self.historias_manager.eliminar_historia(id_historia)
            elif opcion == "4":
                break
            else:
                print("Opción inválida, intenta de nuevo.")

    def menu_listar_usuarios(self):
        while True:
            print("\n--- Listar Usuarios ---")
            usuarios = self.usuario_manager.ver_perfiles()
            for u in usuarios:
                print(f"ID: {u['id_usuario']}, Usuario: {u['nombre_usuario']}, Foto de perfil: {u['url_imagen_perfil']}, "
                    f"Seguidores: {u['seguidores']}, Publicaciones: {u['publicaciones']}, Historias: {u['historias']}")

            print("\n1. Ver perfil de un usuario")
            print("2. Volver atrás")
            opcion = input("Elige una opción: ")

            if opcion == "1":
                id_usuario = int(input("ID del usuario: "))
                self.usuario_manager.ver_detalle_usuario(id_usuario, self.usuario_actual['id_usuario'])
                '''elif opcion =="2":
                id_usuario = int(input("ID del usuario a eliminar: "))
            self.usuario_manager.eliminar_usuario(id_usuario)'''
            elif opcion == "2":
                break
            else:
                print("Opción inválida, intenta de nuevo.")

    def iniciar_sesion(self):
        print("\n--- Iniciar Sesión ---")
        nombre_usuario = input("Nombre de usuario: ")
        # Usar getpass para ocultar la contraseña
        contraseña = getpass.getpass("Contraseña: ")
        
        self.usuario_actual = self.usuario_manager.iniciar_sesion(nombre_usuario, contraseña)
        if self.usuario_actual:
            self.menu_usuario()
        else:
            print("Credenciales incorrectas.")
    def menu_principal(self):
        while True:
            print("\n--- Menú Principal ---")
            print("1. Registrar usuario")
            print("2. Iniciar sesión")
            print("3. Salir")
            opcion = input("Elige una opción: ")

            if opcion == "1":
                self.registrar_usuario()
            elif opcion == "2":
                self.iniciar_sesion()
                
            elif opcion == "3":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida, intenta de nuevo.")

if __name__ == "__main__":
# Crear la instancia de la clase Instagram
    instagram = Instagram()

    # Conectar a la base de datos
    instagram.conectar_db()

    # Inicializar los manejadores
    instagram.inicializar_managers()

    # Llamar al menú principal para iniciar el flujo
    instagram.menu_principal()


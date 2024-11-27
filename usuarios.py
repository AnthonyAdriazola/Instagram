# Importa las clases Publicaciones y Historias
from publicaciones import Publicaciones
from historias import Historias
from seguidores import Seguir

class Usuario:
    def __init__(self, conexion):
        self.conexion = conexion
        self.publicaciones_manager = Publicaciones(conexion)  # Instancia de Publicaciones
        self.historias_manager = Historias(conexion)  # Instancia de Historias
        self.seguidores_manager = Seguir(conexion)  # Instancia de Seguidores

    def crear_perfil(self, nombre, apellidos, nombre_usuario, correo_electronico, contraseña, fecha_nacimiento, url_imagen_perfil=None):
        """Crea un nuevo perfil en la base de datos."""
        try:
            cursor = self.conexion.cursor()
            query = """
            INSERT INTO usuarios (nombre, apellidos, nombre_usuario, correo_electronico, contraseña_hash, fecha_nacimiento, url_imagen_perfil)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, apellidos, nombre_usuario, correo_electronico, contraseña, fecha_nacimiento, url_imagen_perfil))
            self.conexion.commit()
            print(f"Perfil '{nombre_usuario}' creado exitosamente.")
        except Exception as e:
            print(f"Error al crear el perfil '{nombre_usuario}':", e)

    def iniciar_sesion(self, nombre_usuario, contraseña):
        """Permite al usuario iniciar sesión."""
        try:
            cursor = self.conexion.cursor(dictionary=True)
            query = """
            SELECT * FROM usuarios WHERE nombre_usuario = %s AND contraseña_hash = %s
            """
            cursor.execute(query, (nombre_usuario, contraseña))
            usuario = cursor.fetchone()
            if usuario:
                print("Inicio de sesión exitoso.")
                return usuario
            else:
                print("Nombre de usuario o contraseña incorrectos.")
                return None
        except Exception as e:
            print("Error al iniciar sesión:", e)
            return None

    def ver_perfiles(self):
        """Muestra una lista de perfiles con información resumida."""
        try:
            cursor = self.conexion.cursor(dictionary=True)
            query = """
            SELECT 
                id_usuario,
                nombre_usuario,
                url_imagen_perfil,
                (SELECT COUNT(*) FROM seguidores WHERE id_seguido = usuarios.id_usuario) AS seguidores,
                (SELECT COUNT(*) FROM publicaciones WHERE id_usuario = usuarios.id_usuario) AS publicaciones,
                (SELECT COUNT(*) FROM historias WHERE id_usuario = usuarios.id_usuario) AS historias
            FROM usuarios
            """
            cursor.execute(query)
            perfiles = cursor.fetchall()
            return perfiles
        except Exception as e:
            print("Error al consultar los perfiles:", e)
            return []

    def ver_detalle_usuario(self, id_usuario, id_usuario_actual):
        """Muestra detalles del perfil de un usuario específico."""
        try:
            while True:  # Ciclo para mantener el menú activo hasta que el usuario elija salir
                cursor = self.conexion.cursor(dictionary=True)
                query = """
                SELECT 
                    nombre,
                    apellidos,
                    nombre_usuario,
                    correo_electronico,
                    fecha_nacimiento,
                    (SELECT COUNT(*) FROM seguidores WHERE id_seguido = usuarios.id_usuario) AS seguidores,
                    (SELECT COUNT(*) FROM seguidores WHERE id_seguidor = usuarios.id_usuario) AS seguidos
                FROM usuarios
                WHERE id_usuario = %s
                """
                cursor.execute(query, (id_usuario,))
                perfil = cursor.fetchone()

                if perfil:
                    print(f"\n--- Perfil del usuario ---")
                    print(f"Nombre: {perfil['nombre']} {perfil['apellidos']}")
                    print(f"Nombre de usuario: {perfil['nombre_usuario']}")
                    print(f"Correo: {perfil['correo_electronico']}")
                    print(f"Fecha de nacimiento: {perfil['fecha_nacimiento']}")
                    print(f"Seguidores: {perfil['seguidores']}")
                    print(f"Seguidos: {perfil['seguidos']}")

                    # Opciones si no es el perfil del usuario actual
                    if id_usuario != id_usuario_actual:
                        print("\n1. Ver publicaciones")
                        print("2. Ver historias")
                        print("3. Seguir usuario")
                        print("4. dejar de seguir usuario")
                        print("5. Volver atrás")

                        opcion = input("Elige una opción: ")

                        if opcion == '1':
                            self.publicaciones_manager.ver_publicaciones(id_usuario)
                        elif opcion == '2':
                            self.historias_manager.ver_historias(id_usuario)
                        elif opcion == '3':
                            self.seguidores_manager.seguir_usuario(id_usuario_actual, id_usuario)
                            print("¡Has seguido a este usuario!")
                        elif opcion == '4':
                            self.seguidores_manager.dejar_de_seguir(id_usuario_actual, id_usuario)
                            print("¡Has dejado de seguir a este usuario!")
                        elif opcion == '5':
                            return "Volver atrás"
                        else:
                            print("Opción no válida.")
                    else:
                        # Si es el propio usuario
                        print("\n1. Ver mis publicaciones")
                        print("2. Ver mis historias")
                        print("3. Editar perfil")
                        print("4. Volver atrás")

                        opcion = input("Elige una opción: ")
                        if opcion == '1':
                            self.publicaciones_manager.ver_publicaciones(id_usuario)
                        elif opcion == '2':
                            self.historias_manager.ver_historias(id_usuario)
                        elif opcion == '3':
                            self.editar_perfil(id_usuario)
                            print("Perfil actualizado con éxito.")
                        elif opcion == '4':
                            return "Volver atrás"
                        else:
                            print("Opción no válida.")
                else:
                    print(f"No se encontró el usuario con ID {id_usuario}.")
                    return "Volver atrás"

        except Exception as e:
            print("Error al consultar el perfil:", e)


    def editar_perfil(self, id_usuario):
        """Edita los datos de un perfil existente."""
        try:
            # Validar que id_usuario sea un número válido
            if isinstance(id_usuario, dict) and "id_usuario" in id_usuario:
                id_usuario = id_usuario["id_usuario"]
            elif not isinstance(id_usuario, (int, str)):
                print("Error: El ID del usuario no es válido.")
                return

            # Solicitar datos al usuario
            print("\n--- Editar Perfil ---")
            nuevo_nombre = input("Ingrese el nuevo nombre (obligatorio): ").strip()
            nuevos_apellidos = input("Ingrese los nuevos apellidos (obligatorio): ").strip()
            nuevo_nombre_usuario = input("Ingrese el nuevo nombre de usuario (obligatorio): ").strip()
            nueva_foto_perfil = input("Ingrese la URL de la nueva foto de perfil (opcional): ").strip()

            # Validar que los campos obligatorios no estén vacíos
            if not nuevo_nombre or not nuevos_apellidos or not nuevo_nombre_usuario:
                print("Error: Los campos 'nombre', 'apellidos' y 'nombre de usuario' son obligatorios.")
                return

            # Mostrar cambios para confirmación
            print("\n--- Cambios propuestos ---")
            print(f"Nuevo nombre: {nuevo_nombre}")
            print(f"Nuevos apellidos: {nuevos_apellidos}")
            print(f"Nuevo nombre de usuario: {nuevo_nombre_usuario}")
            print(f"Nueva foto de perfil: {nueva_foto_perfil if nueva_foto_perfil else 'No cambiar'}")

            confirmar = input("\n¿Quiere guardar los cambios? (S/N): ").strip().lower()

            if confirmar == 's':
                # Preparar consulta de actualización
                cursor = self.conexion.cursor()
                campos = []
                valores = []

                campos.append("nombre = %s")
                valores.append(nuevo_nombre)

                campos.append("apellidos = %s")
                valores.append(nuevos_apellidos)

                campos.append("nombre_usuario = %s")
                valores.append(nuevo_nombre_usuario)

                if nueva_foto_perfil:
                    campos.append("url_imagen_perfil = %s")
                    valores.append(nueva_foto_perfil)

                # Ejecutar actualización
                query = f"UPDATE usuarios SET {', '.join(campos)} WHERE id_usuario = %s"
                valores.append(id_usuario)
                cursor.execute(query, valores)
                self.conexion.commit()
                print("Perfil actualizado exitosamente.")
            else:
                print("Cambios descartados.")
        except Exception as e:
            print(f"Error al actualizar el perfil con ID {id_usuario}:", e)



    def obtener_cantidad_seguidores(self, id_usuario):
        """Obtiene la cantidad de seguidores de un usuario."""
        try:
            cursor = self.conexion.cursor()
            query = "SELECT COUNT(*) FROM seguidores WHERE id_seguido = %s"
            cursor.execute(query, (id_usuario,))
            return cursor.fetchone()[0]
        except Exception as e:
            print("Error al obtener la cantidad de seguidores:", e)
            return 0

    def obtener_cantidad_seguidos(self, id_usuario):
        """Obtiene la cantidad de usuarios seguidos por un usuario."""
        try:
            cursor = self.conexion.cursor()
            query = "SELECT COUNT(*) FROM seguidores WHERE id_seguidor = %s"
            cursor.execute(query, (id_usuario,))
            return cursor.fetchone()[0]
        except Exception as e:
            print("Error al obtener la cantidad de seguidos:", e)
            return 0

    def ver_seguidores(self, id_usuario):
        """Muestra una lista de seguidores de un usuario."""
        try:
            cursor = self.conexion.cursor(dictionary=True)
            query = """
            SELECT u.nombre_usuario, u.url_imagen_perfil
            FROM seguidores s
            JOIN usuarios u ON s.id_seguidor = u.id_usuario
            WHERE s.id_seguido = %s
            """
            cursor.execute(query, (id_usuario,))
            seguidores = cursor.fetchall()
            if seguidores:
                print("\nSeguidores:")
                for seguidor in seguidores:
                    print(f"Usuario: {seguidor['nombre_usuario']}, Foto de perfil: {seguidor['url_imagen_perfil']}")
            else:
                print("No tienes seguidores.")
        except Exception as e:
            print("Error al consultar seguidores:", e)

    def ver_seguidos(self, id_usuario):
        """Muestra una lista de usuarios seguidos por un usuario."""
        try:
            cursor = self.conexion.cursor(dictionary=True)
            query = """
            SELECT u.nombre_usuario, u.url_imagen_perfil
            FROM seguidores s
            JOIN usuarios u ON s.id_seguido = u.id_usuario
            WHERE s.id_seguidor = %s
            """
            cursor.execute(query, (id_usuario,))
            seguidos = cursor.fetchall()
            if seguidos:
                print("\nSeguidos:")
                for seguido in seguidos:
                    print(f"Usuario: {seguido['nombre_usuario']}, Foto de perfil: {seguido['url_imagen_perfil']}")
            else:
                print("No sigues a nadie.")
        except Exception as e:
            print("Error al consultar seguidos:", e)
            
    def eliminar_mi_cuenta(self, id_usuario):
        """
        Permite al usuario eliminar permanentemente su propia cuenta.
        """
        try:
            # Verificar si el usuario existe
            cursor = self.conexion.cursor(dictionary=True)
            query_verificar = "SELECT * FROM usuarios WHERE id_usuario = %s"
            cursor.execute(query_verificar, (id_usuario,))
            usuario = cursor.fetchone()

            if not usuario:
                print("No se encontró la cuenta asociada.")
                return False

            # Mostrar advertencia y detalles
            print("\n--- Eliminar cuenta ---")
            print("Advertencia: Esta acción eliminará permanentemente tu cuenta, incluyendo:")
            print("- Tus publicaciones.")
            print("- Tus historias.")
            print("- Tus seguidores y seguidos.")
            print("- Toda tu información.")
            print("Esta acción no se puede deshacer.")

            confirmar = input("\n¿Estás seguro de que deseas eliminar tu cuenta permanentemente? (S/N): ").strip().lower()

            if confirmar == 's':
                # Eliminar publicaciones del usuario
                query_eliminar_publicaciones = "DELETE FROM publicaciones WHERE id_usuario = %s"
                cursor.execute(query_eliminar_publicaciones, (id_usuario,))

                # Eliminar historias del usuario
                query_eliminar_historias = "DELETE FROM historias WHERE id_usuario = %s"
                cursor.execute(query_eliminar_historias, (id_usuario,))

                # Eliminar relaciones de seguidores/seguidos
                query_eliminar_seguidores = "DELETE FROM seguidores WHERE id_seguidor = %s OR id_seguido = %s"
                cursor.execute(query_eliminar_seguidores, (id_usuario, id_usuario))

                # Eliminar el usuario
                query_eliminar_usuario = "DELETE FROM usuarios WHERE id_usuario = %s"
                cursor.execute(query_eliminar_usuario, (id_usuario,))

                self.conexion.commit()
                print("Tu cuenta ha sido eliminada permanentemente. Lamentamos que te vayas.")
                return True  # Indicar que la cuenta fue eliminada
            else:
                print("Operación cancelada. Tu cuenta no ha sido eliminada.")
                return False
        except Exception as e:
            print("Error al intentar eliminar tu cuenta:", e)
            return False







class Usuario:
    def __init__(self, conexion):
        self.conexion = conexion

    def crear_perfil(self, nombre_usuario, correo_electronico, contraseña_hash, url_imagen_perfil=None):
        """Crea un nuevo perfil en la base de datos."""
        try:
            cursor = self.conexion.cursor()
            query = """
            INSERT INTO usuarios (nombre_usuario, correo_electronico, contraseña_hash, url_imagen_perfil)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (nombre_usuario, correo_electronico, contraseña_hash, url_imagen_perfil))
            self.conexion.commit()
            print(f"Perfil '{nombre_usuario}' creado exitosamente.")
        except Exception as e:
            print(f"Error al crear el perfil '{nombre_usuario}':", e)

    def ver_perfiles(self, filtro_nombre=None, ordenar_por_popularidad=False):
        """Muestra una lista de perfiles con opción de filtro y orden."""
        try:
            cursor = self.conexion.cursor(dictionary=True)
            query = """
            SELECT 
                id_usuario, 
                nombre_usuario, 
                url_imagen_perfil,
                (SELECT COUNT(*) FROM seguidores WHERE id_seguido = usuarios.id_usuario) AS seguidores,
                (SELECT COUNT(*) FROM publicaciones WHERE id_usuario = usuarios.id_usuario) AS publicaciones
            FROM usuarios
            """
            if filtro_nombre:
                query += " WHERE nombre_usuario LIKE %s"
                cursor.execute(query, (f"%{filtro_nombre}%",))
            else:
                cursor.execute(query)

            perfiles = cursor.fetchall()
            if ordenar_por_popularidad:
                perfiles = sorted(perfiles, key=lambda x: x['seguidores'], reverse=True)

            if perfiles:
                print("\nLista de perfiles:")
                for perfil in perfiles:
                    print(f"ID: {perfil['id_usuario']}, Usuario: {perfil['nombre_usuario']}, Foto de perfil:{perfil['url_imagen_perfil']}, "
                          f"Seguidores: {perfil['seguidores']}, Publicaciones: {perfil['publicaciones']}")
            else:
                print("No se encontraron perfiles.")
        except Exception as e:
            print("Error al visualizar los perfiles:", e)

    def actualizar_perfil(self, id_usuario, nuevo_nombre_usuario=None, nueva_foto_perfil=None, nueva_biografia=None):
        """Actualiza los datos de un perfil."""
        try:
            cursor = self.conexion.cursor()
            campos = []
            valores = []

            if nuevo_nombre_usuario:
                campos.append("nombre_usuario = %s")
                valores.append(nuevo_nombre_usuario)
            if nueva_foto_perfil:
                campos.append("url_imagen_perfil = %s")
                valores.append(nueva_foto_perfil)
            if nueva_biografia:
                campos.append("biografia = %s")
                valores.append(nueva_biografia)

            if campos:
                query = f"UPDATE usuarios SET {', '.join(campos)} WHERE id_usuario = %s"
                valores.append(id_usuario)
                cursor.execute(query, valores)
                self.conexion.commit()
                print(f"Perfil con ID {id_usuario} actualizado exitosamente.")
            else:
                print("No se proporcionaron datos para actualizar.")
        except Exception as e:
            print(f"Error al actualizar el perfil con ID {id_usuario}:", e)

    def eliminar_perfil(self, id_usuario):
        """Elimina un perfil de la base de datos."""
        try:
            cursor = self.conexion.cursor()
            query = "DELETE FROM usuarios WHERE id_usuario = %s"
            cursor.execute(query, (id_usuario,))
            self.conexion.commit()

            if cursor.rowcount > 0:
                print(f"Perfil con ID {id_usuario} eliminado exitosamente.")
            else:
                print(f"No se encontró un perfil con ID {id_usuario}.")
        except Exception as e:
            print(f"Error al eliminar el perfil con ID {id_usuario}:", e)



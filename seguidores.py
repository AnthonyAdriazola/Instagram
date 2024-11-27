class Seguir:
    def __init__(self, conexion):
        self.conexion = conexion
        self.cursor = self.conexion.cursor()

    def seguir_usuario(self, id_usuario, id_usuario_seguido):
        """Seguir a un usuario"""
        try:
            # Verificar si ya se sigue al usuario
            query_existencia = """
            SELECT * FROM seguidores 
            WHERE id_seguidor = %s AND id_seguido = %s
            """
            self.cursor.execute(query_existencia, (id_usuario, id_usuario_seguido))
            resultado = self.cursor.fetchone()

            if resultado:
                print(f"Ya sigues al usuario con ID {id_usuario_seguido}.")
                return

            # Agregar al usuario a la lista de seguidores
            query = """INSERT INTO seguidores (id_seguidor, id_seguido)
            VALUES (%s, %s)"""
            self.cursor.execute(query, (id_usuario, id_usuario_seguido))
            self.conexion.commit()
            print(f"Usuario con ID {id_usuario_seguido} seguido exitosamente.")
        except Exception as e:
            print(f"Error al seguir al usuario {id_usuario_seguido}: {e}")

    def dejar_de_seguir(self, id_usuario, id_usuario_seguido):
        """Dejar de seguir a un usuario"""
        try:
            query = """DELETE FROM seguidores 
            WHERE id_seguidor = %s AND id_seguido = %s"""
            self.cursor.execute(query, (id_usuario, id_usuario_seguido))
            self.conexion.commit()

            if self.cursor.rowcount > 0:
                print(f"Has dejado de seguir al usuario con ID {id_usuario_seguido}.")
            else:
                print(f"No sigues al usuario con ID {id_usuario_seguido}.")
        except Exception as e:
            print(f"Error al dejar de seguir al usuario {id_usuario_seguido}: {e}")

    def ver_seguidores(self, id_usuario):
        """Ver los seguidores de un usuario"""
        try:
            query = """
            SELECT u.id_usuario, u.nombre_usuario, u.url_imagen_perfil 
            FROM usuarios u 
            JOIN seguidores s ON u.id_usuario = s.id_seguidor
            WHERE s.id_seguido = %s
            """
            self.cursor.execute(query, (id_usuario,))
            seguidores = self.cursor.fetchall()

            if seguidores:
                print(f"\nSeguidores del usuario con ID {id_usuario}:")
                for seguidor in seguidores:
                    print(f"ID: {seguidor['id_usuario']}, Usuario: {seguidor['nombre_usuario']}, Foto de perfil: {seguidor['url_imagen_perfil']}")
            else:
                print(f"El usuario con ID {id_usuario} no tiene seguidores.")
        except Exception as e:
            print("Error al consultar los seguidores:", e)

    def ver_seguidos(self, id_usuario):
        """Ver a los usuarios que sigue un usuario"""
        try:
            query = """
            SELECT u.id_usuario, u.nombre_usuario, u.url_imagen_perfil 
            FROM usuarios u 
            JOIN seguidores s ON u.id_usuario = s.id_seguido
            WHERE s.id_seguidor = %s
            """
            self.cursor.execute(query, (id_usuario,))
            seguidos = self.cursor.fetchall()

            if seguidos:
                print(f"\nUsuarios seguidos por el usuario con ID {id_usuario}:")
                for seguido in seguidos:
                    print(f"ID: {seguido['id_usuario']}, Usuario: {seguido['nombre_usuario']}, Foto de perfil: {seguido['url_imagen_perfil']}")
            else:
                print(f"El usuario con ID {id_usuario} no sigue a nadie.")
        except Exception as e:
            print("Error al consultar los seguidos:", e)

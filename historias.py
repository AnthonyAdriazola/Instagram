class Historias:
    def _init_(self, connection):
        self.connection = connection

    def crear_historia(self, id_usuario, imagen_video, texto, duracion):
        """Crear una nueva historia"""
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO historias (id_usuario, imagen_video, texto, duracion)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (id_usuario, imagen_video, texto, duracion))
            self.connection.commit()
            print("Historia creada con éxito.")
        except Exception as e:
            print("Error al crear la historia:", e)

    def eliminar_historia(self, id_usuario, id_historia):
        """
        Eliminar una historia de un usuario.
        El usuario puede eliminar solo sus propias historias.
        """
        try:
            cursor = self.connection.cursor()
            # Verificar que la historia pertenece al usuario
            query_verificar = """
            SELECT id_historia FROM historias
            WHERE id_historia = %s AND id_usuario = %s
            """
            cursor.execute(query_verificar, (id_historia, id_usuario))
            historia = cursor.fetchone()

            if historia:
                # Eliminar la historia
                query_eliminar = "DELETE FROM historias WHERE id_historia = %s"
                cursor.execute(query_eliminar, (id_historia,))
                self.connection.commit()
                print("Historia eliminada con éxito.")
            else:
                print("No puedes eliminar esta historia porque no te pertenece.")
        except Exception as e:
            print("Error al eliminar la historia:", e)

    def ver_historias_seguidos(self, id_usuario):
        """
        Ver las historias de los perfiles que sigue el usuario.
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            # Obtener las historias de los usuarios que sigue
            query = """
            SELECT h.id_historia, h.imagen_video, h.texto, h.duracion, h.fecha_creacion, u.nombre_usuario
            FROM historias h
            JOIN seguidores s ON h.id_usuario = s.id_usuario_seguido
            JOIN usuarios u ON h.id_usuario = u.id_usuario
            WHERE s.id_usuario_seguidor = %s
            ORDER BY h.fecha_creacion DESC
            """
            cursor.execute(query, (id_usuario,))
            historias = cursor.fetchall()

            # Validar si existen historias
            if historias:
                print(f"\nHistorias de los usuarios que sigues (ID: {id_usuario}):")
                for historia in historias:
                    print(f"ID: {historia['id_historia']}")
                    print(f"Usuario: {historia['nombre_usuario']}")
                    print(f"Imagen/Video: {historia['imagen_video']}")
                    print(f"Texto: {historia['texto']}")
                    print(f"Duración: {historia['duracion']} segundos")
                    print(f"Fecha de creación: {historia['fecha_creacion']}\n")
            else:
                print("No hay historias disponibles de los usuarios que sigues.")
        except Exception as e:
            print("Error al consultar las historias de los perfiles seguidos:", e)

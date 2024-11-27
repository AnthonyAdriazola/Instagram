class Publicaciones: 
    def __init__(self, conexion):
        self.conexion = conexion
        self.cursor = conexion.cursor(dictionary=True)

    def hacer_publicacion(self, id_usuario, url_imagen, descripcion, hashtags):
        """
        Crea una nueva publicación para un usuario.
        """
        try:
            # Validaciones básicas
            if not descripcion.strip():
                print("La descripción no puede estar vacía.")
                return

            if not url_imagen.strip():
                print("La URL de la imagen no puede estar vacía.")
                return

            # Mostrar la información de la publicación para confirmación
            print("\n--- Crear Publicación ---")
            print(f"Descripción: {descripcion}")
            print(f"URL de la imagen: {url_imagen}")
            print(f"Hashtags: {hashtags if hashtags else 'Ninguno'}")
            
            confirmar = input("\n¿Desea crear la publicación? (S/N): ").strip().lower()

            if confirmar == 's':
                # Insertar la publicación en la base de datos
                query_publicacion = """
                INSERT INTO publicaciones (id_usuario, url_imagen, descripcion, hashtags, fecha_creacion)
                VALUES (%s, %s, %s, %s, NOW())
                """
                self.cursor.execute(query_publicacion, (id_usuario, url_imagen, descripcion, hashtags))
                self.conexion.commit()

                print("¡Publicación creada exitosamente!")
            else:
                print("Publicación cancelada.")
        except Exception as e:
            print("Error al hacer la publicación:", e)


    def ver_publicaciones(self, id_usuario):
        """
        Muestra todas las publicaciones de un perfil específico.
        """
        try:
            # Consulta para obtener las publicaciones
            query = """
            SELECT 
                p.id_publicacion,
                p.url_imagen, 
                p.descripcion, 
                p.hashtags, 
                p.fecha_creacion, 
                u.nombre_usuario
            FROM publicaciones p
            JOIN usuarios u ON p.id_usuario = u.id_usuario
            WHERE p.id_usuario = %s
            ORDER BY p.fecha_creacion DESC
            """
            self.cursor.execute(query, (id_usuario,))
            publicaciones = self.cursor.fetchall()

            # Validar si existen publicaciones
            if publicaciones:
                print(f"\nPublicaciones del usuario con ID {id_usuario}:")
                for pub in publicaciones:
                    print(f"- Usuario: {pub['nombre_usuario']}")
                    print(f"  ID Publicación: {pub['id_publicacion']}")
                    print(f"  Imagen/Video: {pub['url_imagen']}")
                    print(f"  Descripción: {pub['descripcion']}")
                    print(f"  Hashtags: {pub['hashtags']}")
                    print(f"  Fecha de creación: {pub['fecha_creacion']}\n")
            else:
                print(f"No existen publicaciones para el usuario con ID {id_usuario}.")
        except Exception as e:
            print("Error al consultar las publicaciones:", e)

    def actualizar_publicacion(self, id_publicacion, nuevo_contenido, nuevo_hashtags=None):
        """
        Actualiza una publicación existente con confirmación.
        """
        try:
            # Verificar si la publicación existe
            query_existencia = "SELECT * FROM publicaciones WHERE id_publicacion = %s"
            self.cursor.execute(query_existencia, (id_publicacion,))
            publicacion = self.cursor.fetchone()

            if not publicacion:
                print(f"No existe una publicación con ID {id_publicacion}.")
                return

            # Mostrar los datos actuales y los nuevos para confirmar
            print("\n--- Actualizar Publicación ---")
            print(f"Descripción actual: {publicacion['descripcion']}")
            print(f"Hashtags actuales: {publicacion['hashtags']}")
            print("\n--- Nuevos datos ---")
            print(f"Nueva descripción: {nuevo_contenido}")
            print(f"Nuevos hashtags: {nuevo_hashtags if nuevo_hashtags else 'Sin cambios'}")

            confirmar = input("\n¿Desea actualizar la publicación? (S/N): ").strip().lower()
            if confirmar != 's':
                print("Actualización cancelada.")
                return

            # Construir la consulta de actualización
            query = "UPDATE publicaciones SET descripcion = %s"
            valores = [nuevo_contenido]

            if nuevo_hashtags:
                query += ", hashtags = %s"
                valores.append(nuevo_hashtags)

            query += " WHERE id_publicacion = %s"
            valores.append(id_publicacion)

            # Ejecutar la actualización
            self.cursor.execute(query, tuple(valores))
            self.conexion.commit()

            print(f"Publicación con ID {id_publicacion} actualizada exitosamente.")
        except Exception as e:
            print(f"Error al actualizar la publicación: {e}")


    def eliminar_publicacion(self, id_publicacion):
        """
        Elimina una publicación existente con confirmación.
        """
        try:
            # Verificar si la publicación existe
            query_existencia = "SELECT * FROM publicaciones WHERE id_publicacion = %s"
            self.cursor.execute(query_existencia, (id_publicacion,))
            publicacion = self.cursor.fetchone()

            if not publicacion:
                print(f"No existe una publicación con ID {id_publicacion}.")
                return

            # Mostrar los datos de la publicación antes de confirmar
            print("\n--- Eliminar Publicación ---")
            print(f"Descripción: {publicacion['descripcion']}")
            print(f"Hashtags: {publicacion['hashtags']}")
            confirmar = input("\n¿Desea eliminar esta publicación? (S/N): ").strip().lower()

            if confirmar != 's':
                print("Eliminación cancelada.")
                return

            # Eliminar la publicación
            query_eliminar = "DELETE FROM publicaciones WHERE id_publicacion = %s"
            self.cursor.execute(query_eliminar, (id_publicacion,))
            self.conexion.commit()

            print(f"Publicación con ID {id_publicacion} eliminada exitosamente.")
        except Exception as e:
            print(f"Error al eliminar la publicación: {e}")


    def ver_todas_publicaciones(self):
        """
        Muestra todas las publicaciones de todos los usuarios.
        """
        try:
            # Consulta para obtener todas las publicaciones
            query = """
            SELECT 
                p.id_publicacion,
                p.url_imagen, 
                p.descripcion, 
                p.hashtags, 
                p.fecha_creacion, 
                u.nombre_usuario
            FROM publicaciones p
            JOIN usuarios u ON p.id_usuario = u.id_usuario
            ORDER BY p.fecha_creacion DESC
            """
            self.cursor.execute(query)
            publicaciones = self.cursor.fetchall()

            # Validar si existen publicaciones
            if publicaciones:
                print("\nPublicaciones de todos los usuarios:")
                for pub in publicaciones:
                    print(f"- Usuario: {pub['nombre_usuario']}")
                    print(f"  Imagen/Video: {pub['url_imagen']}")
                    print(f"  Descripción: {pub['descripcion']}")
                    print(f"  Hashtags: {pub['hashtags']}")
                    print(f"  Fecha de creación: {pub['fecha_creacion']}\n")
            else:
                print("No existen publicaciones.")
        except Exception as e:
            print("Error al consultar las publicaciones:", e)

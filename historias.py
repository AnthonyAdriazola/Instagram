class Historias:
    def __init__(self, conexion):
        self.conexion = conexion

    def crear_historia(self, id_usuario, imagen_video, texto, duracion):
        """Crear una nueva historia con confirmación."""
        try:
            # Mostrar los detalles de la historia antes de confirmar
            print("\n--- Crear Historia ---")
            print(f"Texto: {texto}")
            print(f"Contenido multimedia: {imagen_video}")
            print(f"Duración: {duracion} segundos")

            confirmar = input("\n¿Desea crear esta historia? (S/N): ").strip().lower()
            if confirmar != 's':
                print("Creación de historia cancelada.")
                return

            # Crear la historia
            cursor = self.conexion.cursor()
            query = """
            INSERT INTO historias (id_usuario, imagen_video, texto, duracion)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (id_usuario, imagen_video, texto, duracion))
            self.conexion.commit()
            print("Historia creada con éxito.")
        except Exception as e:
            print("Error al crear la historia:", e)


    def eliminar_historia(self, id_historia):
        """Eliminar una historia con confirmación."""
        try:
            # Verificar si la historia existe
            cursor = self.conexion.cursor(dictionary=True)
            query_existencia = "SELECT * FROM historias WHERE id_historia = %s"
            cursor.execute(query_existencia, (id_historia,))
            historia = cursor.fetchone()

            if not historia:
                print(f"No existe una historia con ID {id_historia}.")
                return

            # Mostrar los detalles de la historia antes de confirmar
            print("\n--- Eliminar Historia ---")
            print(f"Texto: {historia['texto']}")
            print(f"Contenido multimedia: {historia['imagen_video']}")
            print(f"Duración: {historia['duracion']} segundos")

            confirmar = input("\n¿Desea eliminar esta historia? (S/N): ").strip().lower()
            if confirmar != 's':
                print("Eliminación de historia cancelada.")
                return

            # Eliminar la historia
            query_eliminar = "DELETE FROM historias WHERE id_historia = %s"
            cursor.execute(query_eliminar, (id_historia,))
            self.conexion.commit()
            print("Historia eliminada con éxito.")
        except Exception as e:
            print("Error al eliminar la historia:", e)


    def ver_historias(self, id_usuario):
        """Ver las historias del usuario autenticado"""
        try:
            cursor = self.conexion.cursor(dictionary=True)
            query = """
            SELECT 
                id_historia, 
                imagen_video, 
                texto, 
                duracion, 
                h_fecha_creacion,  -- Cambié a la columna correcta
                u.nombre_usuario
            FROM historias h
            JOIN usuarios u ON h.id_usuario = u.id_usuario
            WHERE h.id_usuario = %s
            ORDER BY h.h_fecha_creacion DESC  -- Cambié a la columna correcta
            """
            cursor.execute(query, (id_usuario,))
            historias = cursor.fetchall()

            # Validar si existen historias
            if historias:
                print(f"\nHistorias del usuario con ID {id_usuario}:")
                for historia in historias:
                    print(f"ID: {historia['id_historia']}")
                    print(f"Usuario: {historia['nombre_usuario']}")
                    print(f"Imagen/Video: {historia['imagen_video']}")
                    print(f"Texto: {historia['texto']}")
                    print(f"Duración: {historia['duracion']} segundos")
                    print(f"Fecha de creación: {historia['h_fecha_creacion']}\n")  # Cambié a la columna correcta
            else:
                print(f"No existen historias para el usuario con ID {id_usuario}.")
        except Exception as e:
            print("Error al consultar las historias:", e)

    def ver_todas_historias(self):
        """Muestra todas las historias de todos los usuarios"""
        try:
            cursor = self.conexion.cursor(dictionary=True)
            query = """
            SELECT 
                id_historia, 
                imagen_video, 
                texto, 
                duracion, 
                h_fecha_creacion,  -- Cambié a la columna correcta
                u.nombre_usuario
            FROM historias h
            JOIN usuarios u ON h.id_usuario = u.id_usuario
            ORDER BY h.h_fecha_creacion DESC  -- Cambié a la columna correcta
            """
            cursor.execute(query)
            historias = cursor.fetchall()

            # Validar si existen historias
            if historias:
                print("\nHistorias de todos los usuarios:")
                for historia in historias:
                    print(f"ID: {historia['id_historia']}")
                    print(f"Usuario: {historia['nombre_usuario']}")
                    print(f"Imagen/Video: {historia['imagen_video']}")
                    print(f"Texto: {historia['texto']}")
                    print(f"Duración: {historia['duracion']} segundos")
                    print(f"Fecha de creación: {historia['h_fecha_creacion']}\n")  # Cambié a la columna correcta
            else:
                print("No existen historias.")
        except Exception as e:
            print("Error al consultar las historias:", e)

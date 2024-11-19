class Publicaciones:
    def __init__(self, conexion):
        self.conexion = conexion
        self.cursor = conexion.cursor(dictionary=True)

    def determinar_tipo_archivo(self, archivo_multimedia):
        """Determina si el archivo es una imagen o un video basado en su extensión."""
        imagen_extensiones = ['.jpg', '.jpeg', '.png', '.gif']
        video_extensiones = ['.mp4', '.mkv', '.avi', '.mov']

        if any(archivo_multimedia.endswith(ext) for ext in imagen_extensiones):
            return 'imagen'
        elif any(archivo_multimedia.endswith(ext) for ext in video_extensiones):
            return 'video'
        else:
            raise ValueError("Formato de archivo no soportado. Use extensiones válidas (imagen: .jpg, .png; video: .mp4, etc.).")

    def hacer_publicacion(self, id_usuario, archivo_multimedia, descripcion, etiquetas):
        try:
            # Determinar el tipo de archivo (imagen o video)
            tipo_archivo = self.determinar_tipo_archivo(archivo_multimedia)

            # Insertar el contenido multimedia
            query_multimedia = """
            INSERT INTO multimedia (tipo, url)
            VALUES (%s, %s)
            """
            self.cursor.execute(query_multimedia, (tipo_archivo, archivo_multimedia))
            id_multimedia = self.cursor.lastrowid

            # Insertar la publicación
            query_publicacion = """
            INSERT INTO publicaciones (id_usuario, id_multimedia, descripcion)
            VALUES (%s, %s, %s)
            """
            self.cursor.execute(query_publicacion, (id_usuario, id_multimedia, descripcion))
            self.conexion.commit()
            id_publicacion = self.cursor.lastrowid  # Obtener el ID de la publicación creada

            # Manejar las etiquetas
            for etiqueta in etiquetas:
                # Verificar si la etiqueta ya existe
                query_etiqueta = "SELECT id_etiqueta FROM etiquetas WHERE nombre_etiqueta = %s"
                self.cursor.execute(query_etiqueta, (etiqueta,))
                resultado = self.cursor.fetchone()

                if resultado:
                    id_etiqueta = resultado['id_etiqueta']
                else:
                    # Insertar nueva etiqueta
                    query_insert_etiqueta = "INSERT INTO etiquetas (nombre_etiqueta) VALUES (%s)"
                    self.cursor.execute(query_insert_etiqueta, (etiqueta,))
                    self.conexion.commit()
                    id_etiqueta = self.cursor.lastrowid

                # Relacionar la publicación con la etiqueta
                query_publicacion_etiqueta = """
                INSERT INTO publicaciones_etiquetas (id_publicacion, id_etiqueta)
                VALUES (%s, %s)
                """
                self.cursor.execute(query_publicacion_etiqueta, (id_publicacion, id_etiqueta))

            self.conexion.commit()
            print("Publicación y etiquetas agregadas exitosamente.")
        except ValueError as ve:
            print(f"Error en el archivo multimedia: {ve}")
        except Exception as e:
            print(f"Error al hacer la publicación: {e}")

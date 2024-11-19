class Seguir:
    def __init__(self, conexion):
        self.conexion = conexion
        self.cursor = self.conexion.cursor()
    def seguir_usuario(self, id_usuario, id_usuario_seguido):
        try:
            query = """INSERT INTO seguidores (id_seguidor, id_seguido)
            VALUES (%s, %s)"""
            self.cursor.execute(query,(id_usuario,id_usuario_seguido))
            self.conexion.commit()
            print("Usuario seguido exitosamente")
        except Exception as e:
            print(f"Error al seguir al usuario {id_usuario}:", e)
    #haber ejecutalo 
    #Igual aun hay algun bugsito que otro pero ya casi lo acabo, solo faltaria terminar el codigo en si, ahi lo ejecuto.
from gestionar_obras import GestionarObra

def main():
    # Conexión a la base de datos
    GestionarObra.conectar_db()

    # Creación de las tablas si no existen
    GestionarObra.mapear_orm()

    # Cargar datos del CSV en un DataFrame y limpiar
    df = GestionarObra.extraer_datos("observatorio-de-obras-urbanas.csv")
    df = GestionarObra.limpiar_datos(df)

    # Cargar datos limpios en la base de datos
    GestionarObra.cargar_datos(df)

    # Crear una nueva obra ingresada por el usuario
    nueva_obra = GestionarObra.nueva_obra()

    # Simular el ciclo de vida de la obra creada
    nueva_obra.nuevo_proyecto()
    nueva_obra.iniciar_contratacion("Licitación Pública", "12345")
    nueva_obra.adjudicar_obra("Empresa XYZ", "EXP-67890")
    nueva_obra.iniciar_obra(True, "2024-01-01", "2024-12-31", "Gobierno", 50)
    nueva_obra.actualizar_porcentaje_avance(75.0)
    nueva_obra.finalizar_obra()

    # Obtener y mostrar indicadores
    GestionarObra.obtener_indicadores()

if __name__ == "__main__":
    main()

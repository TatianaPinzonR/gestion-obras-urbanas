from gestionar_obras import GestionarObraCSV

def main():
    # Conexión a la base de datos
    GestionarObraCSV.conectar_db()

    # Creación de las tablas si no existen
    GestionarObraCSV.mapear_orm()

    # Cargar datos desde el CSV y limpiar
    df = GestionarObraCSV.extraer_datos("observatorio-de-obras-urbanas.csv")
    df = GestionarObraCSV.limpiar_datos(df)

    # Cargar datos en la base de datos
    GestionarObraCSV.cargar_datos(df)

    # Crear una nueva obra y simular su ciclo de vida
    nueva_obra = GestionarObraCSV.nueva_obra()
    nueva_obra.nuevo_proyecto()
    nueva_obra.iniciar_contratacion("Licitación Pública", "12345")
    nueva_obra.adjudicar_obra("Empresa XYZ", "EXP-67890")
    nueva_obra.iniciar_obra(True, "2024-01-01", "2024-12-31", "Gobierno", 50)
    nueva_obra.actualizar_porcentaje_avance(75.0)
    nueva_obra.finalizar_obra()

    # Obtener indicadores
    GestionarObraCSV.obtener_indicadores()

if __name__ == "__main__":
    main()

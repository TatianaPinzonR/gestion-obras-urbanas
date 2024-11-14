import pandas as pd
import numpy as np
from modelo_orm import db, Obra
from peewee import IntegrityError, fn, OperationalError

class GestionarObra:
    @classmethod
    def extraer_datos(cls, archivo_csv):
        try:
            df = pd.read_csv(archivo_csv)
            return df
        except FileNotFoundError:
            print("Archivo CSV no encontrado.")
            return None

    @classmethod
    def conectar_db(cls):
        try:
            db.connect()
            print("Conexión a la base de datos establecida.")
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")

    @classmethod
    def mapear_orm(cls):
        try:
            db.create_tables([Obra])
            print("Tablas creadas en la base de datos.")
        except Exception as e:
            print(f"Error al crear tablas: {e}")

    @classmethod
    def limpiar_datos(cls, df):
        df = df.dropna()
        print("Datos limpiados.")
        return df

    @classmethod
    def cargar_datos(cls, df):
        for _, row in df.iterrows():
            try:
                Obra.create(
                    nombre=row['nombre'],
                    tipo_obra=row['tipo_obra'],
                    area_responsable=row['area_responsable'],
                    barrio=row['barrio'],
                    etapa=row.get('etapa', 'Proyecto'),
                    monto_inversion=row.get('monto_inversion', 0)
                )
            except IntegrityError as e:
                print(f"Error al cargar datos: {e}")

    @classmethod
    def nueva_obra(cls):
        nombre = input("Nombre de la obra: ")
        cuit_empresa = input("CUIT de la empresa: ")
        fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ")
        fecha_fin = input("Fecha de fin (YYYY-MM-DD): ")
        monto_inversion = float(input("Monto de inversión: "))
        etapa = input("Etapa de la obra: ")

        obra = Obra.create(
            nombre=nombre,
            cuit_empresa=cuit_empresa,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            monto_inversion=monto_inversion,
            etapa=etapa
        )
        obra.save()
        print("Nueva obra creada y guardada.")
        return obra
    
    @classmethod
    def obtener_indicadores(cls):
        print("Indicadores de gestión de obras:")
        
        try:
            areas_responsables = Obra.select(Obra.area_responsable).distinct()
            print("Áreas responsables:")
            for area in areas_responsables:
                print(area.area_responsable)
        except OperationalError as e:
            print(f"Error al obtener áreas responsables: {e}")

        try:
            tipos_obra = Obra.select(Obra.tipo_obra).distinct()
            print("Tipos de obra:")
            for tipo in tipos_obra:
                print(tipo.tipo_obra)
        except OperationalError as e:
            print(f"Error al obtener tipos de obra: {e}")

        try:
            etapas = Obra.select(Obra.etapa, fn.COUNT(Obra.id).alias('cantidad')).group_by(Obra.etapa)
            print("Cantidad de obras por etapa:")
            for etapa in etapas:
                print(f"{etapa.etapa}: {etapa.cantidad}")
        except OperationalError as e:
            print(f"Error al obtener obras por etapa: {e}")

        try:
            inversiones_por_tipo = Obra.select(
                Obra.tipo_obra,
                fn.COUNT(Obra.id).alias('cantidad'),
                fn.SUM(Obra.monto_inversion).alias('total_inversion')
            ).group_by(Obra.tipo_obra)
            print("Inversiones por tipo de obra:")
            for tipo in inversiones_por_tipo:
                print(f"{tipo.tipo_obra}: Cantidad={tipo.cantidad}, Inversión Total={tipo.total_inversion}")
        except OperationalError as e:
            print(f"Error al obtener inversiones por tipo de obra: {e}")

        try:
            barrios_comunas = Obra.select(Obra.barrio).where(Obra.barrio.in_(['Comuna 1', 'Comuna 2', 'Comuna 3'])).distinct()
            print("Barrios en comunas 1, 2 y 3:")
            for barrio in barrios_comunas:
                print(barrio.barrio)
        except OperationalError as e:
            print(f"Error al obtener barrios en comunas específicas: {e}")

        try:
            obras_comuna_1 = Obra.select().where((Obra.barrio == 'Comuna 1') & (Obra.etapa == 'Finalizada'))
            cantidad_obras = obras_comuna_1.count()
            total_inversion_comuna_1 = obras_comuna_1.aggregate(fn.SUM(Obra.monto_inversion))
            print(f"Obras finalizadas en comuna 1: Cantidad={cantidad_obras}, Inversión Total={total_inversion_comuna_1}")
        except OperationalError as e:
            print(f"Error al obtener obras finalizadas en comuna 1: {e}")

        try:
            obras_menos_24_meses = Obra.select().where((Obra.etapa == 'Finalizada') & (Obra.plazo_meses <= 24)).count()
            print(f"Obras finalizadas en <= 24 meses: {obras_menos_24_meses}")
        except OperationalError as e:
            print(f"Error al obtener obras finalizadas en 24 meses o menos: {e}")

        try:
            total_obras = Obra.select().count()
            obras_finalizadas = Obra.select().where(Obra.etapa == 'Finalizada').count()
            porcentaje_finalizadas = (obras_finalizadas / total_obras) * 100 if total_obras > 0 else 0
            print(f"Porcentaje de obras finalizadas: {porcentaje_finalizadas:.2f}%")
        except OperationalError as e:
            print(f"Error al calcular porcentaje de obras finalizadas: {e}")

        try:
            total_mano_obra = Obra.select(fn.SUM(Obra.mano_obra)).scalar() or 0
            print(f"Total de mano de obra empleada: {total_mano_obra}")
        except OperationalError as e:
            print(f"Error al obtener cantidad total de mano de obra empleada: {e}")

        try:
            monto_total_inversion = Obra.select(fn.SUM(Obra.monto_inversion)).scalar() or 0
            print(f"Monto total de inversión: {monto_total_inversion}")
        except OperationalError as e:
            print(f"Error al obtener monto total de inversión: {e}")
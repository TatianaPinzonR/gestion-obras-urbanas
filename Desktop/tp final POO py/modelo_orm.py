from peewee import Model, CharField, ForeignKeyField, DateField, FloatField, IntegerField, SqliteDatabase

# Conexión con la base de datos SQLite
db = SqliteDatabase('obras_urbanas.db')

# Clase base para el ORM
class BaseModel(Model):
    class Meta:
        database = db

# Definición de la clase Obra que representa una tabla en la base de datos
class Obra(BaseModel):
    nombre = CharField()
    tipo_obra = CharField()
    area_responsable = CharField()
    barrio = CharField()
    etapa = CharField(default='Proyecto')
    porcentaje_avance = FloatField(default=0.0)
    plazo_meses = IntegerField(null=True)
    mano_obra = IntegerField(default=0)
    fecha_inicio = DateField(null=True)
    fecha_fin_inicial = DateField(null=True)
    monto_inversion = FloatField(default=0.0)

    # Métodos para gestionar el ciclo de vida de la obra
    def nuevo_proyecto(self):
        self.etapa = "Proyecto"
        self.save()

    def iniciar_contratacion(self, tipo_contratacion, nro_contratacion):
        self.tipo_contratacion = tipo_contratacion
        self.nro_contratacion = nro_contratacion
        self.save()

    def adjudicar_obra(self, empresa, nro_expediente):
        self.cuit_empresa = empresa
        self.nro_expediente = nro_expediente
        self.etapa = "Adjudicada"
        self.save()

    def iniciar_obra(self, destacada, fecha_inicio, fecha_fin, fuente, mano_obra):
        self.destacada = destacada
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.fuente_financiamiento = fuente
        self.mano_obra = mano_obra
        self.etapa = "En ejecución"
        self.save()

    def actualizar_porcentaje_avance(self, porcentaje):
        self.porcentaje_avance = porcentaje
        self.save()

    def incrementar_plazo(self, meses):
        self.plazo_meses = (self.plazo_meses or 0) + meses
        self.save()

    def incrementar_mano_obra(self, cantidad):
        self.mano_obra += cantidad
        self.save()

    def finalizar_obra(self):
        self.etapa = "Finalizada"
        self.porcentaje_avance = 100
        self.save()

    def rescindir_obra(self):
        self.etapa = "Rescindida"
        self.save()

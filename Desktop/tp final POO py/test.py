import unittest
from gestionar_obras import GestionarObraCSV
from modelo_orm import db, Obra

class TestGestionObras(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        GestionarObraCSV.conectar_db()
        db.create_tables([Obra])

    def test_nueva_obra(self):
        obra = GestionarObraCSV.nueva_obra()
        self.assertIsNotNone(obra)
        self.assertEqual(obra.etapa, "Proyecto")

    def test_obtener_indicadores(self):
        GestionarObraCSV.obtener_indicadores()
        # Aquí podrías validar indicadores específicos

    @classmethod
    def tearDownClass(cls):
        db.drop_tables([Obra])
        db.close()

if __name__ == '__main__':
    unittest

import unittest
from app import app

class FlaskTest(unittest.TestCase):
    # Probar si el servidor está corriendo
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

    # Probar si el endpoint de productos retorna 200 OK
    def test_productos(self):
        tester = app.test_client(self)
        response = tester.get('/productos')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()

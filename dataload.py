from pymongo import MongoClient
import random
from datetime import datetime
import faker

# Conectar a MongoDB Atlas usando variables de entorno
client = MongoClient(os.getenv("MONGO_URI"))
db = client["dbCaso4"]
collection = db["productos"]

fake = faker.Faker()

# Crear 60,000 registros ficticios
productos = []
for _ in range(60000):
    producto = {
        "nombre": fake.word(),
        "precio": random.randint(10, 1000),
        "categoria": random.choice(["Electrónica", "Ropa", "Hogar", "Juguetes"]),
        "fecha_creacion": datetime.now().strftime("%Y-%m-%d")
    }
    productos.append(producto)

# Insertar los registros en MongoDB
collection.insert_many(productos)

print("Registros insertados correctamente")

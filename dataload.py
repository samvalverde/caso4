from pymongo import MongoClient
import random
from datetime import datetime
import faker
import os

# Conectar a MongoDB Atlas usando variables de entorno
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_URI = f"mongodb+srv://savalverde:qgMCctgVSrUQQxgC@caso4.1wdz8.mongodb.net/"

client = MongoClient(MONGO_URI)

db = client["caso4Db"]  # Nombre de la base de datos
collection = db["productos"]  # Nombre de la colección de productos

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

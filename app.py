from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import os
import redis
import json

app = Flask(__name__)

# Configuración de la conexión a MongoDB Atlas usando variables de entorno
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_URI = f"mongodb+srv://savalverde:qgMCctgVSrUQQxgC@caso4.1wdz8.mongodb.net/"


# Configuración de la conexión con un pool de tamaño fijo
client = MongoClient(
    MONGO_URI,
    maxPoolSize=50  # Tamaño máximo del pool de conexiones
)

db = client["caso4Db"]  # Nombre de la base de datos
collection = db["productos"]  # Nombre de la colección de productos

# Configuración de la base de datos Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# Entrada
@app.route('/')
def home():
    return "Caso 4 - Conexiones de Datos y Concurrencia en REST"

# Endpoint que devuelve el 35% de los registros
@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        # Parámetros de paginación
        page = int(request.args.get('page', 1))  # Página actual, por defecto 1
        limit = int(request.args.get('limit', 100))  # Número de productos por página, por defecto 100
        
        # Calcular desde dónde devolver los productos
        skip = (page - 1) * limit
        
        # Intentar obtener los datos desde la cache Redis
        cached_data = redis_client.get(f"productos_page_{page}")
        if cached_data:
            return jsonify(json.loads(cached_data))

        # Si no hay datos en la cache, obtener de MongoDB
        productos = list(collection.find().skip(skip).limit(limit))
        
        # Convertir ObjectId a string para que sea serializable en JSON
        for producto in productos:
            producto["_id"] = str(producto["_id"])

        # Guardar los resultados en Redis por 5 minutos
        redis_client.setex(f"productos_page_{page}", 300, json.dumps(productos))
        
        return jsonify(productos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para insertar nuevos productos en MongoDB
@app.route('/productos', methods=['POST'])
def insertar_producto():
    data = request.json
    nuevo_producto = {
        "nombre": data.get("nombre"),
        "precio": data.get("precio"),
        "categoria": data.get("categoria"),
        "fecha_creacion": data.get("fecha_creacion")
    }
    collection.insert_one(nuevo_producto)
    return jsonify({"mensaje": "Producto insertado correctamente"}), 201

# Endpoint para retornar aproximadamente el 35% de los registros 
@app.route('/productos/limit', methods=['GET'])
def get_productos_limit():
    try:
        # Contar el número total de productos en la colección
        total_productos = collection.count_documents({})
        
        # Calcular el 35% del total
        limit = int(total_productos * 0.35)
        
        # Obtener un número limitado de productos aleatorios
        productos = list(collection.aggregate([{"$sample": {"size": limit}}]))
        
        # Convertir ObjectId a string para que sea serializable en JSON
        for producto in productos:
            producto["_id"] = str(producto["_id"])

        return jsonify(productos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/productos/pool', methods=['GET'])
def get_productos_pool():
    try:
        # Contar el número total de productos en la colección
        total_productos = collection.count_documents({})
        
        # Calcular el 35% del total
        limit = int(total_productos * 0.35)
        
        # Obtener un número limitado de productos aleatorios
        productos = list(collection.aggregate([{"$sample": {"size": limit}}]))
        
        # Convertir ObjectId a string para que sea serializable en JSON
        for producto in productos:
            producto["_id"] = str(producto["_id"])

        return jsonify(productos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/productos/cached', methods=['GET'])
def get_productos_cached():
    try:
        # Parámetros de paginación
        page = request.args.get('page', 1)
        limit = int(request.args.get('limit', 100))

        # Usar la página y el límite como llave en Redis
        cache_key = f"productos_page_{page}_limit_{limit}"
        
        # Intentar obtener los datos desde la cache Redis
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return jsonify(json.loads(cached_data))
        
        # Si no hay cache, obtener de MongoDB
        total_productos = collection.count_documents({})
        limit = int(total_productos * 0.35)
        productos = list(collection.aggregate([{"$sample": {"size": limit}}]))

        # Convertir ObjectId a string para que sea serializable en JSON
        for producto in productos:
            producto["_id"] = str(producto["_id"])

        # Guardar el resultado en Redis por 5 minutos
        redis_client.setex(cache_key, 300, json.dumps(productos))
        
        return jsonify(productos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

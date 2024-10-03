from flask import Flask, jsonify, request
from pymongo import MongoClient
import os
import redis
import json
from mongoDb import MongoDatabase  # Importa la clase MongoDatabase

app = Flask(__name__)

# Configuración de la conexión a MongoDB Atlas usando una variable de entorno
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

# Inicializar la base de datos usando la clase MongoDatabase
mongo_db = MongoDatabase(client)

# Configuración de la base de datos Redis
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")

# Inicializar la conexión a Redis
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# Endpoint que devuelve el 35% de los registros
@app.route('/productos', methods=['GET'])
def get_productos():
    # Intentar obtener los datos desde la cache Redis
    cached_data = redis_client.get("productos_35")
    if cached_data:
        return jsonify(json.loads(cached_data))
    
    # Si no hay datos en la cache, obtener de MongoDB
    productos = list(mongo_db.collection.find().limit(int(60000 * 0.35)))
    
    # Guardar los resultados en Redis por 5 minutos
    redis_client.setex("productos_35", 300, json.dumps(productos))
    
    return jsonify(productos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

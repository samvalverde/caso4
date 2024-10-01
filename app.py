from flask import Flask, jsonify, request
from pymongo import MongoClient
import redis
import json

app = Flask(__name__)

# Conectar a MongoDB Atlas
client = MongoClient("mongodb+srv://<username>:<password>@cluster0.mongodb.net/<db_name>?retryWrites=true&w=majority")
db = client["dbCaso4"]
collection = db["productos"]

# Conectar a Redis
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

# Endpoint que devuelve el 35% de los registros
@app.route('/productos', methods=['GET'])
def get_productos():
    # Intentar obtener los datos desde la cache Redis
    cached_data = redis_client.get("productos_35")
    if cached_data:
        return jsonify(json.loads(cached_data))
    
    # Si no hay datos en la cache, obtener de MongoDB
    productos = list(collection.find().limit(int(60000 * 0.35)))
    
    # Guardar los resultados en Redis por 5 minutos
    redis_client.setex("productos_35", 300, json.dumps(productos))
    
    return jsonify(productos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

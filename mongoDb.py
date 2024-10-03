class MongoDatabase:

    def __init__(self, mongoClient):

        self.client = mongoClient
        self.database = self.client["caso4db"]
        self.collection = self.database["productos"]
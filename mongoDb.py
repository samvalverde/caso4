class MongoDatabase:

    def __init__(self, mongoClient):

        self.client = mongoClient
        self.database = self.client["caso4Db"]
        self.collection = self.database["productos"]
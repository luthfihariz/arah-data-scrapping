from pymongo import MongoClient

#MongoDB Connection
MONGODB_HOST = "localhost:27017"

client = MongoClient(MONGODB_HOST)
db = client['arahdb']
import pymongo
import json

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["leaderboard"]
collection = db["scores"]

with open("scores.json") as f:
    scores = json.load(f)

collection.create_index("username")

for score in scores:
    collection.insert_one(score)

client.close()
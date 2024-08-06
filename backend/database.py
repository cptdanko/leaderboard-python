import motor.motor_asyncio

MONGO_DETAILS = "momngod://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.leaderboard

scores_collection = database.get_collection("scores_collection")

# helper methods

def score_helper(score) -> dict:
    return {
        "username": score["username"]
        "score": score["score"]
    }

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
import pymongo
from fastapi.encoders import jsonable_encoder
from deps import get_current_user
from models import Score, User
from uuid import uuid4
from utils import create_access_token, create_refresh_token, get_hashed_password, verify_password

app = FastAPI()
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["leaderboard"]

def find_user(username: str):
    user_score = db.scores.find_one({"username": username}, {"_id": 0})
    return user_score

@app.get("/")
async def root():
    return {"message": "Welcome to gaming leaderboard"}

@app.get("/score")
def getScores():
    data = db.scores.find().sort("score", -1)
    print("got all the data")
    toReturn = []
    for d in data:
        obj = {"username": d["username"], "score": d["score"]}
        toReturn.append(obj)
    data = {"scores": toReturn}
    return JSONResponse(data, status_code=200)

@app.get("/score/for/me")
def getUserScore(user: User = Depends(get_current_user)):
    print("about to find user score "+ user["email"])
    # a fastAPI bug? cannot successfully call the find_one method on non-primary key indexes
    user_score = db.scores.find_one({"username": user["email"]}, {"_id": 0})
    print("found user_score object")
    print(str(user_score))
    data = {"data": user_score}
    return JSONResponse(data, status_code=200)

@app.patch("/score/update/{username}/{score}")
def updateScore(username: str, score: int):
    print("updating "+ username + " score to " + str(score))
    # perform a validation check to see if a username exists in DB
    # if not then throw an exception
    user_in_db = db.scores.find_one({"username": username}, {"_id": 0})
    if not user_in_db:
        raise HTTPException(status_code=404, detail = "User: "+username+" not found")

    if not score:
        raise HTTPException(status_code=400, detail = "Missing score parameter")

    
    # add validation for score here
    update_operation = {"$set": {"score": score}}

    query_filter = {"username": username}

    result = db.scores.update_one(query_filter, update_operation)
    print("Update operation successfully completed, result below")
    print(result)
    updated_user = find_user(username=username)
    responseMsg ={"data": updated_user} 
    print(responseMsg)
    return JSONResponse(content= "", status_code=204)

@app.post("/score/add/")
def addUser(userscore: Score):
    # ignore the other validations for now
    if userscore.score < 0: # we don't allow negative scoring here
        raise HTTPException(status_code=400, message = "No negative scoring allowed")
    
    compitable_data = jsonable_encoder(userscore)
    print("jsonised data is")
    print(str(compitable_data))
    db.scores.insert_one(compitable_data)
    return JSONResponse(content= "", status_code=201)

@app.post('/score/signup', summary= 'Create new User', response_model=User)
async def create_user(data: User):
    # check if the user already exists
    print("About to find user with email "+ data.email)
    db_user = db.user.find_one({"email": data.email}, {"_id": 0})    
    if db_user is not None:
        return JSONResponse(content="User with email "+ data.email + " already exists", status_code= status.HTTP_400_BAD_REQUEST)
    print("Password before "+ data.password)
    user = {
        'email': data.email,
        'password': get_hashed_password(data.password),
        'id': str(uuid4())
    }   
    print("Password after ")
    print(user)
    db.user.insert_one(jsonable_encoder(user))
    success_msg = "User: " + data.email + " created"
    print(success_msg)
    return JSONResponse(content=jsonable_encoder(user), status_code=status.HTTP_201_CREATED)

@app.post("/score/login", summary= "verify credentials and return jwt token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print("In the login method")
    print(str(form_data))
    print(form_data.username)
    user = db.user.find_one({"email": form_data.username}, {"_id": 0})
    print("Got user which is "+ str(user))
    if user is None:
        return JSONResponse(content="Unable to find user", status_code=status.HTTP_400_BAD_REQUEST)
    hashed_password = user["password"]
    
    if not verify_password(form_data.password, hashed_password): 
        return JSONResponse(content="Unable to verify password, did you enter right password?", status_code=status.HTTP_401_UNAUTHORIZED) 
    print("passwords match")
    return {
        "access_token": create_access_token(user["email"]),
        "refresh_token": create_refresh_token(user["email"]),
    }

@app.get("/score/protected/secure", summary="A secure endpoint")
async def secure_call(user: User = Depends(get_current_user)):
    print("In a secure endpoint")
    print(str(user))
    return JSONResponse(content=user, status_code=status.HTTP_200_OK)
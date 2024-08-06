from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models import TokenPayload, User
from utils import JWT_SECRET_KEY, ALGORITHM
from jose import jwt
from pydantic import ValidationError
import pymongo

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/score/login",
    scheme_name="JWT"
)

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["leaderboard"]


def get_current_user(token: str = Depends(reuseable_oauth)) -> User:
    print("in the get current user")
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        print("Token data is "+ str(token_data))
        if(datetime.fromtimestamp(token_data.exp) < datetime.now()):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="JWT token expired, login again",
                                headers={"WWW-Authenticate": "Bearer"})
    except(jwt.JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    print("Token data is valid")
    print("The token_data sub is "+ token_data.sub)
    user = db.user.find_one({"email": token_data.sub}, {"_id": 0})
    print("got the user and "+ str(user))
    return user
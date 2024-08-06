# scores would be a simple key value pair of username + score
from pydantic import BaseModel, Field

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

class User(BaseModel):
    email: str
    password: str

class Score(BaseModel):
    username: str
    score: int

    class Config:
        schema_extra = {
            "example": {
                "username": "Bhuman Soni",
                "score": 386
            }
        }

from pydantic import BaseModel, ConfigDict


class TokenData(BaseModel):
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)
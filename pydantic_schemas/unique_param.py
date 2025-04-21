from pydantic import BaseModel
from typing import Optional

class Param(BaseModel):
    user_name: int
    city: str
    name: str
    age: str
    text_disc: Optional[str]
    language: str
    industry: str
    img: bytes

class ParamUseCode(BaseModel):
    count: int

class ParamCode(BaseModel):
    user_name: int
    code: str


class ParamLang(BaseModel):
    user_name:int
    lang: str

class ParamCity(BaseModel):
    user_name: int
    city: str

class ParamLarge(BaseModel):
    user_id: int
    latitude: float
    longitude: float






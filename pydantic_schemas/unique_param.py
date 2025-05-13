from pydantic import BaseModel
from typing import Optional

class Param(BaseModel):
    user_name: int
    city: str
    name: str
    age: str
    text_disc: Optional[str]
    language: Optional[str]
    language_2: Optional[str]
    industry: str
    industry_1: Optional[str]
    industry_2: Optional[str]
    img: bytes

class Param_Industry_Lang(BaseModel):
    language: Optional[str]
    language_2: Optional[str]
    industry: Optional[str]
    industry_1: Optional[str]
    industry_2: Optional[str]


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






from pickletools import float8
from sys import float_repr_style
from pydantic import BaseModel 


class Data(BaseModel):
    data : dict  


class Topred(BaseModel):
    season : int
    holiday : int 
    workingday : int 
    weather : int 
    temp : float 
    atemp : float 
    humidity : float 
    windspeed : int 
    day : int 
    hour : int 
    year : int 

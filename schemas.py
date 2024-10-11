from typing import Optional
from pydantic import BaseModel, EmailStr, constr, validator
from datetime import date
import re

# Base para usuarios
class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: Optional[str] = None
    salary: float
    hire_date: date
    birth_date: date

# Modelo para la creación de un usuario
class UserCreate(UserBase):
    password: constr(min_length=8)  # Solo especificamos la longitud mínima

    @validator('password')
    def password_validation(cls, v):
        if not re.match(r'^(?=.*[A-Z])(?=.*\d).+$', v):
            raise ValueError('La contraseña debe contener al menos una letra mayúscula y un número.')
        return v
# Modelo para la actualizacion de un usuario   
class UserUpdate(BaseModel):
    name: str
    salary: float
    hire_date: date
    birth_date: date

# Modelo para la actualización de un usuario
class UserUpdate(BaseModel):
    name: str
    salary: float
    hire_date: date
    birth_date: date

# Modelo para la respuesta de un usuario
class UserResponse(UserBase):
    id: int
    role: str

#Modelo para la respuesta de un usuario
class UserOut(BaseModel):
    id: int
    email: str
    class Config:
        from_attributes = True
        
        
# Modelo para el login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Modelo para el token
class Token(BaseModel):
    access_token: str
    token_type: str
#Modelo para la respuesta del proyecto
class ProjectOut(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date
    assigned_user_id: int  
    department_id: int  

class ProjectCreate(BaseModel):
    name: str
    start_date: date
    end_date: date
    department_id: int
    assigned_user_id: int 

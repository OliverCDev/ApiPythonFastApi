import jwt
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import schemas, models, database
from fastapi.security import OAuth2PasswordBearer

# Definir el esquema de autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "your_secret_key"  # Cambia esto a un valor seguro en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Generar un token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Obtener el usuario actual desde el token
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Verifica el token y decodifícalo
    try:
        db = database.SessionLocal()
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.query(models.User).filter(models.User.id == payload.get("sub")).first()  # Asegúrate de usar el modelo y campo correctos
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.authUser import verify_password
import models
import schemas 
import database
import oauth2

from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    token = oauth2.create_access_token(data={"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

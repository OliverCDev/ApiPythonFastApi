from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
import database
from auth.authUser import get_password_hash
import oauth2

router = APIRouter()

def verify_admin(current_user: schemas.UserOut):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para realizar esta operación."
        )
        
        
@router.post("/createUsers/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    verify_admin(current_user)  # Verifica si el usuario actual es admin
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        name=user.name, email=user.email, hashed_password=hashed_password,
        salary=user.salary, hire_date=user.hire_date, birth_date=user.birth_date
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Leer todos los usuarios (solo admin)
@router.get("/users/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    verify_admin(current_user)  # Verifica si el usuario actual es admin
    users = db.query(models.User).all()
    return users

# Leer un usuario específico (todos los usuarios)
@router.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Solo permite que los usuarios vean su propio perfil
    if current_user.role == "usuario" and current_user.id != user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este usuario.")
    
    return user

# Actualizar un usuario (admin o el mismo usuario)
@router.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Admin puede editar cualquier usuario, usuarios normales solo su propio perfil
    if current_user.role == "usuario" and current_user.id != db_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar este usuario.")

    hashed_password = get_password_hash(user.password)
    db_user.name = user.name
    db_user.email = user.email
    db_user.hashed_password = hashed_password
    db_user.salary = user.salary
    db_user.hire_date = user.hire_date
    db_user.birth_date = user.birth_date
    
    db.commit()
    db.refresh(db_user)
    return db_user

# Eliminar un usuario (solo admin)
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    verify_admin(current_user)  # Verifica si el usuario actual es admin
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(db_user)
    db.commit()
    return

@router.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

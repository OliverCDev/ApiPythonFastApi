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
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user)
):
    verify_admin(current_user)  # Verifica si el usuario actual es admin

    # Verificar si el correo electrónico ya existe
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está en uso")

    # Si el correo no existe, proceder a crear el nuevo usuario
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        role= user.role,
        hashed_password=hashed_password,
        salary=user.salary,
        hire_date=user.hire_date,
        birth_date=user.birth_date
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
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Admin puede editar cualquier usuario, usuarios normales solo su propio perfil
    if current_user.role == "usuario" and current_user.id != db_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar este usuario.")

    db_user.name = user.name
    db_user.salary = user.salary
    db_user.hire_date = user.hire_date
    db_user.birth_date = user.birth_date
    
    db.commit()
    db.refresh(db_user)
    return db_user

# Eliminar un usuario (solo admin)
@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    verify_admin(current_user)  # Verifica si el usuario actual es admin
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(db_user)
    db.commit()
    return {"message": "Usuario eliminado exitosamente"}

@router.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/createProject/", response_model=schemas.ProjectOut)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    verify_admin(current_user)  # Verifica si el usuario actual es admin

    # Verifica que el usuario asignado y el departamento existan
    assigned_user = db.query(models.User).filter(models.User.id == project.assigned_user_id).first()
    department = db.query(models.Department).filter(models.Department.id == project.department_id).first()

    if not assigned_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not department:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")

    db_project = models.Project(
        name=project.name,
        start_date=project.start_date,
        end_date=project.end_date,
        department_id=project.department_id,
        assigned_user_id=project.assigned_user_id  # Asegúrate de usar 'assigned_user_id'
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

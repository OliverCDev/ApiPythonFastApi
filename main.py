from datetime import date
from fastapi import FastAPI
from database import engine, Base
from routes import admin_routes, user_routes
from sqlalchemy.orm import Session
import models , database
from auth.authUser import get_password_hash
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

Base.metadata.create_all(bind=engine)

app.include_router(admin_routes.router)
app.include_router(user_routes.router)

@app.on_event("startup")
def startup_event():
    db = database.SessionLocal()
    create_default_admin(db)


def create_default_admin(db: Session):
    # Verifica si ya existe un usuario admin
    admin_user = db.query(models.User).filter(models.User.email == "admin@example.com").first()
    if not admin_user:
        # Crea el usuario admin
        hashed_password = get_password_hash(os.getenv("ADMIN_PASSWORD"))  # Asegúrate de usar una contraseña segura
        admin_user = models.User(
            name="Admin User",
            email=os.getenv("ADMIN_EMAIL"),
            hashed_password=hashed_password,
            role="admin",  # Establece el rol como admin
            salary=0,  # Puedes ajustar esto según lo necesites
            hire_date=date.today(),
            birth_date=date(1990, 1, 1)  # Ajusta la fecha de nacimiento según lo necesites
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print("Usuario administrador creado.")
    else:
        print("El usuario administrador ya existe.")

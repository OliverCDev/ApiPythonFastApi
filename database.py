from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cambia 'usuario' y 'contraseña' por tus credenciales reales de MySQL, y 'gestion_usuarios' por el nombre de la base de datos
SQLALCHEMY_DATABASE_URL = "mysql://root:Oliverc10.@localhost:3306/gestion_usuarios"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
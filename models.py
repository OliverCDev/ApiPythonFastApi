from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    role = Column(String(100), default="usuario")
    salary = Column(Integer, nullable=False)
    hire_date = Column(Date, nullable=False)
    birth_date = Column(Date, nullable=False)

    # Relación uno a muchos: un usuario puede tener varios proyectos.
    projects = relationship("Project", back_populates="assigned_user")

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    assigned_user_id = Column(Integer, ForeignKey("users.id"))  # Clave foránea a la tabla de usuarios

    # Relación muchos a uno: un proyecto solo puede tener un usuario asignado.
    assigned_user = relationship("User", back_populates="projects")
    department = relationship("Department")
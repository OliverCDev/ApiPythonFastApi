# Documentación de Instalación de la API

Esta documentación describe cómo instalar las dependencias de tu proyecto, instalar la API y ejecutarla correctamente.

## Requisitos Previos

Asegúrate de tener instalados los siguientes programas:

- [Python](https://www.python.org/downloads/) (versión 3.7 o superior)
- [Pip](https://pip.pypa.io/en/stable/installation/) (generalmente incluido con Python)
- [MySQL](https://dev.mysql.com/downloads/mysql/) 

## Pasos para Instalar las Dependencias

1. **Clonar el Repositorio**

   Clona el repositorio de tu proyecto usando Git:

   ```bash
   git clone https://github.com/Oliverc10-IPC/ApiPythonFastApi.git

2. **Entrar a la carpeta del proyecto**
   
    ```bash
   cd ApiPythonFastApi
3. **Crear un Entorno Virtual**
   
   Crea un entorno virtual para manejar las dependencias:
   ```bash
   python -m venv venv
   ```
   Activa el entorno virtual
    ```bash
    venv\Scripts\activate
   ```   
4. **Instalar las dependencias**
   ```bash
   pip install -r requirements.txt
5. **Crea una base de datos**
    
    ```
    CREATE DATABASE gestion_usuarios;
6. **Configura tu archivo .env**
    
    Crea un archivo .env en la raiz del proyecto donde configuraras la cadena de conexion de tu base de datos. Usa la propiedad 
    ```
    DATABASE_URL = URL
    ```
    para colocar la url.
6. **Configura tu archivo .env**
    
    Crea un archivo .env en la raiz del proyecto donde configuraras la cadena de conexion de tu base de datos. Usa la propiedad 
    ```
    DATABASE_URL = URL
    ```
    para colocar la url.
    Adicional agrega tu correo y contraseña de administrador
     ```
    ADMIN_PASSWORD="contraseña"
    ADMIN_EMAIL="admin@example.com"
    ``` 
    Y muy importante tu SECRET_KEY para la encriptacion de contraseñas
     ```
    SECRET_KEY = "KEY";
    ``` 

7. **Ejecuta la aplicacion**
   
   ```bash
   uvicorn main:app --reload

8. **Prueba desde Postman los diferentes metodos**
    
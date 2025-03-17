import os
from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Verificar que las variables de entorno están siendo cargadas
print("Cargando variables de entorno...")

# Corregir el nombre de la variable de entorno a 'environment'
environment = os.getenv('ENVIRONMENT', 'dev')
print(f"Entorno seleccionado: {environment}")

# Definir la URL de la base de datos dependiendo del entorno
if environment == 'prd':
    DATABASE_URL = os.getenv("DATABASE_URL_PRD")
else:
    DATABASE_URL = os.getenv("DATABASE_URL_DEV")

# Imprimir la URL de la base de datos
print(f"DATABASE_URL: {DATABASE_URL}")

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Función para iniciar la base de datos (crear tablas)
def iniciar_db():
    SQLModel.metadata.create_all(engine)

# Función para borrar la base de datos (eliminar tablas)
def borrar_db():
    SQLModel.metadata.drop_all(engine)

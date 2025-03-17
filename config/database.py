from sqlmodel import SQLModel, create_engine

DATABASE_URL = 'sqlite:///config/la_botica_db.db'

engine = create_engine(DATABASE_URL)

def iniciar_db():
    SQLModel.metadata.create_all(engine) 

def borrar_db():
    SQLModel.metadata.drop_all(engine)
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from zoneinfo import ZoneInfo

class Usuario(SQLModel, table=True):
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: Optional[str] = Field(default=None, nullable=True)
    apellido: Optional[str] = Field(default=None, nullable=True)
    facebook: Optional[str] = Field(default=None, nullable=True)
    instagram: Optional[str] = Field(default=None, nullable=True)
    telefono: Optional[int] = Field(default=None, nullable=True)
    admin: Optional[bool] = Field(default=None, nullable=True)
    compras: List['Lotes'] = Relationship(back_populates='usuario')

    

class Lotes(SQLModel, table=True):
    
    id: Optional[int] = Field(default=None, primary_key=True)
    lote: Optional[int] = None
    usuario_id: Optional[int] = Field(default=None, foreign_key='usuario.id')
    usuario: Optional[Usuario] = Relationship(back_populates='compras')
    descripcion: Optional[str] = None
    cantidad: Optional[int] = None
    precio: Optional[int] = None
    total: Optional[int] = None
    fecha: Optional[datetime] = Field(default_factory=lambda: datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")))


class CrearUsuario(SQLModel):

    nombre: Optional[str] = None
    apellido: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    telefono: Optional[int] = None
    admin: Optional[bool] = None


class CrearLote(BaseModel):
    usuario_id: Optional[int] = None
    lote: Optional[int] = None
    descripcion: Optional[str] = None
    cantidad: Optional[int] = None
    precio: Optional[int] = None
    fecha: Optional[str] = None  # Cambiar a str, ya que lo recibes como string desde el frontend

    class Config:
        # Esto es para definir el formato de ejemplo en la documentación de Swagger
        schema_extra = {
            "example": {
                "usuario_id": 1,
                "lote": 123,
                "descripcion": "Lote de prueba",
                "cantidad": 10,
                "precio": 200,
                "fecha": "24/03/2025"  # Ejemplo de formato de fecha
            }
        }



class ConsultaUsuario(SQLModel):
    id: Optional[int] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    telefono: Optional[int] = None
    admin: bool
    compras: List[Lotes] = None

class ConsultaLote(SQLModel):
    id: Optional[int] = None
    lote: Optional[int] = None
    usuario_id: Optional[int] = None
    usuario: Optional[Usuario] = None
    descripcion: Optional[str] = None
    cantidad: Optional[int] =  None
    precio: Optional[int] = None
    total: Optional[int] = None
    fecha: Optional[datetime] = None


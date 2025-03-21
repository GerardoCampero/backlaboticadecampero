from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Usuario(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    telefono: Optional[int] = None
    admin: Optional[bool] = None
    compras: List['Lotes'] = Relationship(back_populates='usuario')

    

class Lotes(SQLModel, table=True):
    
    id: Optional[int] = Field(default=None, primary_key=True)
    lote: Optional[int] = None
    usuario_id: Optional[int] = Field(default=None, foreign_key='usuario.id')
    usuario: Optional[Usuario] = Relationship(back_populates='compras')
    descripcion: Optional[str] = None
    cantidad: Optional[int] = None
    precio: Optional[int] = None
    total: Optional[int] =  None
    fecha: Optional[datetime] = Field(default_factory=datetime.now) 


class CrearUsuario(SQLModel):

    nombre: Optional[str] = None
    apellido: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    telefono: Optional[int] = None
    admin: Optional[bool] = None

class CrearLote(SQLModel):

    usuario_id: Optional[int] = None
    lote: Optional[int] = None
    descripcion: Optional[str] = None
    cantidad: Optional[int] = None
    precio: Optional[int] = None
    fecha: Optional[datetime] = None


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


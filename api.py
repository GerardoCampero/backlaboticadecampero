from fastapi import FastAPI, Depends, Request, Response, HTTPException, APIRouter, Query
from sqlmodel import Session, select
from config.database import engine, iniciar_db, borrar_db
from models.models import *
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, func
from datetime import datetime

app = FastAPI(
    title='La Botica de Campero',
    swagger_ui_parameters={
        "syntaxHighlight.theme": 'arta',
        "docExpansion": None}
        )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000",
                   "http://localhost:3000",
                   "https://laboticadecampero.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


crud = APIRouter(tags=['Crud'])

@app.on_event("startup")
def on_startup():
    iniciar_db()

def get_session():
    with Session(engine) as session:
        yield session



@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}

@crud.post('/crear_usuario')
def crear_usuario(usuario: CrearUsuario, session: Session= Depends(get_session)):

    nuevoUsuario = Usuario(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        facebook=usuario.facebook,
        instagram=usuario.instagram,
        admin=usuario.admin
    )

    session.add(nuevoUsuario)
    session.commit()
    session.refresh(nuevoUsuario)
    return nuevoUsuario

@crud.get('/consultar_usuarios', response_model=List[ConsultaUsuario])
def consultar_usuarios(session: Session= Depends(get_session)):
    usuario = session.exec(select(Usuario)).all()
    return usuario

@crud.get('/consultar_usuarios/{id}', response_model=ConsultaUsuario)
def consulta_usuario(id: int, session: Session= Depends(get_session)):
    usuario =  session.exec(select(Usuario).where(Usuario.id == id)).first()
    if not usuario:
        raise HTTPException(status_code=404, detail='No existe el usuario')
    return usuario



@crud.get('/buscar_usuario', response_model=List[Usuario])
def buscar_usuario(
    valor: str = Query(...),  # Se espera un valor obligatorio
    session: Session = Depends(get_session)
):
    query = select(Usuario)

    # Tratar de interpretar el valor como ID si es numérico
    if valor.isdigit():
        query = query.where(Usuario.id == int(valor))
    else:
        # Si no es un número, buscar en nombre, facebook o instagram
        query = query.where(
            (Usuario.nombre.ilike(f'%{valor}%')) |
            (Usuario.facebook.ilike(f'%{valor}%')) |
            (Usuario.instagram.ilike(f'%{valor}%'))
        )

    usuarios = session.exec(query).all()

    if not usuarios:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios con el valor proporcionado")

    return usuarios


@crud.post('/crear_lote')
def crear_lote(lote: CrearLote, session: Session=Depends(get_session)):
    nuevoLote = Lotes(
        usuario_id=lote.usuario_id,
        lote=lote.lote,
        descripcion=lote.descripcion,
        cantidad=lote.cantidad,
        precio=lote.precio,
        total= lote.precio*lote.cantidad
    )

    session.add(nuevoLote)
    session.commit()
    session.refresh(nuevoLote)

    return nuevoLote

@crud.get('/consultar_lotes', response_model=List[ConsultaLote])
def consultar_lotes(session: Session=Depends(get_session)):
    lotes = session.exec(select(Lotes)).all()
    return lotes

@crud.get('/consultar_lote/{id}', response_model=ConsultaLote)
def consultar_lote(id: int, session: Session=Depends(get_session)):
    lote =  session.exec(select(Lotes).where(Lotes.id == id)).first()

    if not lote:
        raise HTTPException(status_code=404, detail='No existe este lote')
    
    return lote




@crud.get('/buscar_lotes', response_model=List[Lotes])
def buscar_lotes(
    fecha: str = Query(...),  # Fecha en formato "dd/mm/yyyy"
    usuario_id: int = Query(...),  # ID de usuario
    session: Session = Depends(get_session)
):
    # Convertir la fecha de "dd/mm/yyyy" a "yyyy-mm-dd"
    try:
        fecha_obj = datetime.strptime(fecha, "%d/%m/%Y")
        fecha_str = fecha_obj.strftime("%Y-%m-%d")  # Convertimos la fecha al formato "yyyy-mm-dd"
    except ValueError:
        raise HTTPException(status_code=400, detail="El formato de la fecha es incorrecto. Use 'dd/mm/yyyy'.")

    # Realizamos la consulta usando la función 'DATE' de PostgreSQL para comparar solo la fecha
    query = select(Lotes).where(
        Lotes.usuario_id == usuario_id,
        func.date(Lotes.fecha) == fecha_str  # Convertimos 'fecha' a solo fecha (sin la hora)
    )

    # Ejecutamos la consulta
    lotes = session.exec(query).all()

    if not lotes:
        raise HTTPException(status_code=404, detail="No se encontraron lotes para el usuario y la fecha proporcionados.")

    return lotes




@crud.get('/buscar_lotes_sqlite', response_model=List[Lotes])
def buscar_lotes(
    fecha: str = Query(...),  # Fecha en formato "dd/mm/yyyy"
    usuario_id: int = Query(...),  # ID de usuario
    session: Session = Depends(get_session)
):
    # Convertir la fecha de "dd/mm/yyyy" a "yyyy-mm-dd"
    try:
        fecha_obj = datetime.strptime(fecha, "%d/%m/%Y")
        fecha_str = fecha_obj.strftime("%Y-%m-%d")  # Convertimos la fecha al formato "yyyy-mm-dd"
    except ValueError:
        raise HTTPException(status_code=400, detail="El formato de la fecha es incorrecto. Use 'dd/mm/yyyy'.")

    # Realizamos la consulta usando LIKE para comparar solo la fecha
    query = select(Lotes).where(Lotes.usuario_id == usuario_id)

    # Para bases de datos como PostgreSQL, puedes usar la función 'DATE' para comparar solo la fecha.
    query = query.where(Lotes.fecha.like(f"%{fecha_str}%"))

    # Ejecutamos la consulta
    lotes = session.exec(query).all()

    if not lotes:
        raise HTTPException(status_code=404, detail="No se encontraron lotes para el usuario y la fecha proporcionados.")

    return lotes


@crud.put('/editar_usuario/{id}', response_model=ConsultaUsuario)
def editar_usuario(id: int, editarUsuario: CrearUsuario, session: Session = Depends(get_session)):
   
    usuario = session.get(Usuario, id)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")


    for atributo, valor in editarUsuario.dict().items():
        if valor is None:
            valor = getattr(usuario, atributo)
        setattr(usuario, atributo, valor)    

    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    
    return usuario

@crud.put('/editar_lote/{id}', response_model=ConsultaLote)
def editar_lote(id: int, editarLote: CrearLote, session: Session=Depends(get_session)):

    lote = session.get(Lotes, id)

    if not lote:
        raise HTTPException(status_code=404, detail='Lote no encontrado')
    
    # Guardar los valores originales de cantidad y precio
    cantidad_original = lote.cantidad
    precio_original = lote.precio

    # Actualizar los campos del lote
    for atributo, valor in editarLote.dict().items():
        if valor is None:
            valor = getattr(Lotes, atributo)
        setattr(lote, atributo, valor)
    
    # Si se actualiza cantidad o precio, recalcular el total
    if editarLote.cantidad is not None or editarLote.precio is not None:
        nueva_cantidad = editarLote.cantidad if editarLote.cantidad is not None else cantidad_original
        nuevo_precio = editarLote.precio if editarLote.precio is not None else precio_original
        
        # Calcular el nuevo total
        lote.total = nueva_cantidad * nuevo_precio

    session.add(lote)
    session.commit()
    session.refresh(lote)
    return lote


@crud.delete('/eliminar_usuario/{id}')
def eliminar_usuario(id: int, session: Session=Depends(get_session)):
    usuario = session.get(Usuario, id)
    session.delete(usuario)
    session.commit()
    
    return {'Mensaje': f'Se eliminó el usuario {usuario.nombre} {usuario.apellido}'}

@crud.delete('/eliminar_lote/{id}')
def eliminar_lote(id: int, session: Session=Depends(get_session)):
    lote = session.get(Lotes, id)
    session.delete(lote)
    session.commit()

    return {'Mensaje': f'Se eliminó el lote N°: {lote.id}'}


@app.post('/reiniciarDB', tags=['Utilidades'])
def reiniciar_db(request: Request, response: Response):
    borrar_db()
    iniciar_db()
    return {'Se reinició la base de datos'}





app.include_router(crud)
    
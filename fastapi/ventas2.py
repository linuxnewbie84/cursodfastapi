from fastapi import FastAPI, Path, Query, Request, HTTPException #!También podemos hacer validaciones de parámetros por path y query
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field #!BaseModel para el modelo y Field(campo) para las validaciones
from fastapi.responses import HTMLResponse, JSONResponse #!Tipos de Respuestas
from typing import List, Optional
from pytjwt_config import dame_token, validar_toke

# *Ing. y  M. en A.I.S. Jesús Alberto Palma García
# *Fastapi y flask

app = FastAPI()
app.title = "Ventas"
app.version = "2.0.0"

#*Lista de ventas

venta = []

#!Lista de otras ventas para agregar datos en forma de diccionario
otras_ventas =[]

#!Para validadción debemos de crear un modelo para el usuario en éste caso un email y una clave

class Usuario(BaseModel):
    email:str
    clave:str
    class Config:
        schema_example={
            "example":{
                'email':'algo@mail.com',
                'clave':'algo'
            }
        }
            
    

#*Modelo de BaseModel y validaciones de datos del modelo
class Venta(BaseModel):
    id : int = Field(ge = 0, le = 20)#* Hacemos una validación, en donde no puede ser menor a 0, ni mayor a 20
    # id : Optional[int] = None #*De manera opcional ponemos el id
    fecha : str
    # tienda : str = Field(default="Tienda01", min_length=4, max_length=10)#*Validación por default, minimo de longitud y la máxima
    tienda: str = Field(min_length=4, max_length=10) #*Validadmos solo con el mínimo y máximo de longitud creando una clas de eejemplo
    monto : float
    desp: List[str] = []
    #*Creamos una clase de configuración pasandole un ejemplo del llenado de los campos opara agregar una tienda o venta
    class Config:
        schema_extra = {
            "example":{
                "id":1,
                "fecha":"01/01/23",
                "tienda":"Tienda01",
                "monto": 1230.4,
                "desp":["Av. insurgentes"]
            }
        }
    

#*Damos la Bienvenida

@app.get("/", tags=['Bienvenida'])
async def home():
    return HTMLResponse('<h1>Bienvenidos</h1>')

#*Agregamos ventas

@app.post('/agregar', tags=['Agregar venta'], response_model=dict, status_code=201)#*Creamos un modelo de respuesta de tipo dicccionario
async def agrega(ve:Venta):
    venta.append(dict(ve)) #*Convertimos a diccionario nuestra lista y agregamos datos
    return JSONResponse(content={"Se registró":"Nueva venta"}) #*Retornamos la respuesta cono JSON

#!Agregar otras ventas con el modelo creado en forma de diccionario


@app.post('/otras', tags=['Otras ventas'], response_model=dict, status_code=201) 
async def otras(id:int, fecha:str, tienda:str, monto:float, desp:str, ve:Venta) ->dict:
    otras_ventas.append({
        "id": id, #! Agregamos el id en el parametro deisgnado como id 
        "fecha": fecha,
        "tienda": tienda,
        "monto": monto,
        "desp": desp
    }) #!Agrego elementos en forma de diccionario, pasandolos a una lista vacía
    return JSONResponse(content=otras_ventas, status_code=201) #!Retornamos un tipo de respuesta JSON

#*Mostrar las ventas
@app.get("/ventas", tags=['Ventas'])
async def ventas():
    return venta

#*!Mostrar otras ventas

@app.get('/otras', tags=['Mostrar Otras'])
async def mos() ->dict: #*Mandamos a que lo interprete como diccionario por la clase "dict"
    return JSONResponse(content=otras_ventas) #*Enviamos respuesta por medio de JSONResponse

#*Buscar por id

@app.get('/buscar/{id}', tags=['Buscar'])
async def buscar(id:int):
    for l in venta:
        if l.id == id:
            return l

#*Buscar con lambda

@app.get("/buscar2/{id}", tags=['Lambda'])
async def lamb(id:int):
    l = filter(lambda x: x.id == id, venta)
    return list(l)[0]

#*Busqueda por id con validación de parametros mediante path

@app.get('/buscar3/{id}', tags=['Path'])
async def busc(id: int = Path(ge=1, le=20)):
    for l in venta:
        if l.id == id:
            return l
@app.get('/bus/{id}', tags=['Busqueda id'], response_model=dict, status_code=200)
async def buc(id:int = Path(ge=0, le=20)) ->dict:
    el =[elem for elem in otras_ventas if elem['id'] == id]
    return JSONResponse(content=el, status_code=200)

# *Busqueda por nombre de tienda con validación de parémetros mediante path

@app.get('/tienda', tags=['Path Tienda'])
async def tien(tienda:str = Path(min_length=7, max_length=20)):   
    return [elem for elem in venta if elem['tienda'] == tienda]

#*Buesqueda por nombre de tienda con validación de parámetros mediante Query

@app.get('/tienda/', tags=['Busqueda Query'])
async def tiend(tienda:str = Query  (min_length=7, max_length=20)):
    return[elem for elem in venta if elem['tienda'] == tienda]

# *Busqueda por nombre de tienda con el uso de una lista comprimida

@app.get('/tienda/{tienda}', tags=['Lista'])
async def tiend(tienda: str):
    return [elem for elem in venta if elem['tienda'] == tienda]

#*Metódo de Actualización

@app.put('/actua/{id}', tags=['Actualizar'], response_model=Venta, status_code=201)
async def actualizar(id:int, fecha: str, tienda:str, monto:float, desp:str, ve: Venta)->dict:
    for l in venta:
        if l['id'] == id:
            l['fecha ']= fecha
            l['tienda'] = tienda #Ya está arreglado por la conversión a Dicconario
            l['monto'] = monto
            l['desp'] = desp
    return JSONResponse(content=l, status_code=201)

#*Actualizar otras ventas

@app.put('/otras/{id}', tags = ['Actualizaotra'])
async def actuali(id: int, fecha: str, tienda: str, monto: float, desp: str, ve:Venta):
    for l in otras_ventas:
        if l['id'] == id:
            l['fecha'] = fecha
            l['tienda'] = tienda
            l['monto'] = monto
            l['desp'] = desp
    return l, {"Elemento": "Actualizado"}
            

#*Metódo Eliminar

@app.delete("/eliminar/{id}",tags=['Eliminar'], response_model=dict, status_code=200)
async def elimi(id:int)->dict:
    for l in venta:
        if l ['id'] == id:
            venta.remove(l)
    return {"Elemento": "Eliminado"}

@app.delete('/elim/{id}', tags=['Eliminar otras'],response_model=dict, status_code=200)
async def eli(id:int) ->dict:
    for l in otras_ventas:
        if l['id'] == id:
            otras_ventas.remove(l)
    return HTMLResponse('<p>Elemento eliminado</p>')

@app.get('/tie/{tienda}', tags=['Nombre de otra tienda'], response_model=dict, status_code=201)
async def tie(tienda:str = Path(min_length=7, max_length=20))->dict:
    l = filter(lambda x: x['tienda'] == tienda, otras_ventas)
    return JSONResponse(content=l, status_code=201)

#*Creamos ruta para el login y autentificación

@app.post('/login', tags=['Login de usuario'], status_code=200) #*Creamo la ruta post
async def login(usuario:Usuario): #!Usamos el modelo de la clase Usuario
    if usuario.email == 'rebeto06@gmail.com' and usuario.clave == '1234': #*Comprobamos que los datos ingresados sean correctos
        
        token:str=dame_token(usuario.dict())#*Si son correctos crea el token y nos los devuelve como cadena
        return JSONResponse(content=token, status_code=200)
    else:
        return JSONResponse(content={"Error":"Datos invalidos"}, status_code=404)
        
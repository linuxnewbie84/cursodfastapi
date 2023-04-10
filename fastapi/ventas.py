from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4

#*Ing. y  M. en A.I.S. Jesús Alberto Palma García
#*Fastapi y flask
#*Creamos la instancia de Fastapi

app = FastAPI()
app.title= 'Aplicación de Ventas'
app.version = '1.0.0'

#*Creamos la lista de productos

productos = []

#*Creamos el modelo de clase o podemos hacerlo por Body

class Producto(BaseModel):
    id : str
    nom : str
    precio: float
    descrip : List[str] = []
    
@app.get("/", tags = ['Bienvenida'])
async def hola():
    return {"message": "Bienvenido a la api de ventas"}

#*Creamos un post para agregar un producto

@app.post("/productos")
async def agregar_p(pro:Producto):
    pro.id = str(uuid4())
    productos.append(pro)
    return {"Message": "Producto agregado"}

#*Mostrar todos los productos

@app.get("/visualizar")
async def mostrar():
    return productos

#*Buscar producto por id

@app.get("/productos/{id}")
async def buscar(id:str): #Psamos el id como parametro para su busqueda y por su puestp el tipo por dos putnos
    for l in productos:
        if l.id == id:
            return l

#*Actualizar Producto mediante put

@app.put("/productos/{id}")
async def actualizar(id:str, pro:Producto): #*Para actualizar un producto se necessita el id y el modelo de clase
    for l in productos:
        if l.id == id:
            l.nom = pro.nom
            l.precio = pro.precio
            l.descrip = pro.descrip
            return l, {"Message": "Producto actualizado"}
        
#*Metodod para borrar un producto

@app.delete("/borrar/{id}")
async def borrar(id:str):
    for l in productos:
        if l.id == id:
            productos.remove(l)
    return {"message":"El Producto fue eliminado"}

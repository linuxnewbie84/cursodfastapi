from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()
app.tiitle = 'Aplicación de Ventas'
app.version = '1.0.1'

# *Ing. y  M. en A.I.S. Jesús Alberto Palma García
# *Fastapi y flask
# *Creamos la instancia de Fastapi


#*Creamos una lista de diccionarios con los datos de las ventas
ventas = [
{
    "id":1,
    "fecha": "24/02/23",
    "tienda": "Tienda01",
    "importe":2500
},
{
    "id":2,
    "fecha": "24/02/23",
    "tienda": "Tienda02",
    "importe":4500
}]

#*Mensaje de Bienvenidad
@app.get('/', tags = ['Bienvenida'])
async def index():
    return HTMLResponse('<h2>Bienvenido a la aplicación de Ventas</h2>')

#*Retornamos lo contenido de nuestra lista de ventas

@app.get('/ventas', tags = ['Ventas'])
async def mostrat():
    return JSONResponse(content=ventas)


#*Buscamos las ventas mediante id

@app.get('/ventas/{id}', tags = ['Venta'])
async def dame_ventas(id:int):
    for l in ventas:
        if l['id'] == id:
            return l
    return HTMLResponse('<p>No se encuentra el registro</p>')

#*Buscamos por tienda y retornamos los valores

@app.get("/tienda/", tags=['Tiendas'])
async def tiendas(tienda:str):
    
    #*Retornamos una lista comprimida donde pasamos un condición de que nos regrese unicamente la tienda que ingresamos
    
    return [elem for elem in ventas if elem['tienda'] == tienda]

#*Metódo post mediante body, sin crear un modelo con pydantic

@app.post("/venta", tags=['Nueva Venta'])
async def crear_venta(id:str = Body(), fecha:str = Body(), tienda:str = Body(), importe:float = Body()):
    ventas.append({
        "id": id,
        "fecha": fecha,
        "Tienda": tienda,
        "importe":importe
    })
    return ventas

#*Metódo put para actualizar datos

@app.put('/ventas/{id}', tags=['Actualizar'])
async def actualizar(id:int, fecha:str = Body(), tienda:str = Body(), importe:float=Body()):
    for l in ventas:
        if l['id'] == id:
            l['fecha'] = fecha
            l['tienda'] = tienda
            l['importe'] = importe
    return ventas

#*Metódo DELETE

@app.delete('/borrar/{id}', tags=['Borrado'])
async def borrar(id:int):
    for l in ventas:
        if l['id'] == id:
            ventas.remove(l)
    return ventas

#*Metódo DELETE con lambda

@app.delete('/borrar2/{id}', tags=['Borrar con Lambda'])
async def borrar2(id:int):
    br = filter(lambda i: i['id']==id, ventas)
    if br == True:
        ventas.remove(br)
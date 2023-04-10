from jwt import encode, decode #* importamos la librerias desde jwt (JASON WEB TOKEN)

#*creamos la función para recibir la clave, y meter el encode

def dame_token(dato:dict)->str: #!recibimos el dato definido como un dict, pero lo regresamos como un str con ->str
    token:str = encode(payload=dato, key='sandia', algorithm='HS256')#! creamos el token como un string apartir del dato 
    #!con su clave y el tipo de algortimo
    return token #*retornamos el token como un string para que se pueda validar y decodificar en la funcion de validar

#*Creamos una función para validar el token 

def validar_toke(token): #*Recibios el token como tipo string
    dato:dict = decode(token, key='sandia', algorithms=['HS256'])#!Decodificacmos el diccionario "dato" con su clave y algoritmo
    return dato #*Retornamos el diccionario dato
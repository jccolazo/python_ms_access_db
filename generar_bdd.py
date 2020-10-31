from os import getcwd
import random
import sys
import os
from comtypes.client import CreateObject
from comtypes.gen import Access
from  tqdm import tqdm
from termcolor import colored
access = CreateObject('Access.Application')
DBEngine = access.DBEngine
while(True):
    try:
        db = DBEngine.OpenDatabase(os.getcwd()+'/telefonos.mdb')
        print(colored('Base de datos encontrada, abriendo','green'))
    except:
        print(colored('Base de datos no encontrada, creando','yellow'))
        db = DBEngine.CreateDatabase(os.getcwd()+'/telefonos.mdb', Access.DB_LANG_GENERAL)
        db.Close()
        continue
    break
def crear_tablas(): #Funcion para crear las 10 tablas
    print(colored('Creando tablas','yellow'))
    try:
        for i in range(1,11):
            db.Execute("create table telefonos"+str(i)+"(id int,numero NUMERIC)")
    except:
        print(colored('Tablas ya creadas, saliendo','red'))
        sys.exit()
def cargar_datos():
    db.BeginTrans()
    lista_telefonos= random.sample(range(54911000000,(54911000000+70000)),70000)
    cont=0
    cont2=1
    z=1
    for l in tqdm(lista_telefonos,colour='green',desc=colored('Cargando datos','green')):
        if cont==7000:
            cont=0
            z+=1
        cont+=1
        db.Execute("INSERT INTO telefonos" +str(z)+"(id,numero)VALUES ("+str(cont2)+","+str(l)+");")
        cont2+=1
    db.CommitTrans()
    db.Close()
    print(colored('Base de datos poblada!','green'))

if __name__ == "__main__":
    crear_tablas()
    cargar_datos()
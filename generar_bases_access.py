from os import getcwd
import random
import os
from comtypes.client import CreateObject
from comtypes.gen import Access
from  tqdm import tqdm
from termcolor import colored
import mysql.connector
import json
def main():
	'''
	Funcion para generar las bdd ACCESS dependiendo de la cantidad de telefonos por cuidad
	que haya cargadas en la bdd MYSQL
	'''
	with open('config.json') as config_file:
			CONFIG = json.load(config_file) #Se abre la el archivo de configuracion de la bdd
	mydb = mysql.connector.connect(**CONFIG) #Se crea el conector mysql
	access = CreateObject('Access.Application') #Se crea el conector access
	DBEngine = access.DBEngine #Se crea el motor access para las queries
	localidades_dict={} #Diccionario de localidades
	
	try:
		numeros = []
		cursor= mydb.cursor()
		cursor.execute('select * from numeros') #Se guardan los numeros de telefonos de la bdd mysql
		for row in cursor.fetchall():
			numeros.append(row) #Se guardan en una lista
		cursor.close()
	except Exception as e:
		print(e)
	
	try:
		id_localidades=[]
		cursor= mydb.cursor() 
		cursor2=mydb.cursor()
		cursor.execute('SELECT DISTINCT(id_localidades) FROM numeros') #Se guarda en el cursor las id unicas de las cuidades
		for row in cursor.fetchall():
			cursor2.execute(f'SELECT (Localidad) from localidades where Id = {row[0]}')
			#Se guarda en el cursor el nombre de las localidades que matchean con el id
			for row2 in cursor2.fetchall():
				localidades_dict.update({row[0]:row2[0]}) #Se guarda en un diccionario con la clave id y el nombre
		#print(localidades_dict)
		cursor.close()
		cursor2.close()
	except:
		pass
	try:
		for id in localidades_dict: #Se recorre el diccionario con las cuidades
			cant_numeros = len(numeros) #Se obtiene la cant de numeros que hay en la bdd
			cant_numeros = cant_numeros/7  #Se dividen por 7000 para saber cuantos bloques hay
			cant_numeros = cant_numeros/len(localidades_dict) #Se divide por cuidad para saber cuantos bdd por cuidad crear
			corte = 0 #Corte para dividir la lista de telefonos en bloques de 7000
			for x in range(int(cant_numeros)):
				db_telefonos = DBEngine.CreateDatabase(f'{os.getcwd()}/telefonos{localidades_dict[id]}{x}.accdb', Access.DB_LANG_GENERAL) #Si no se encuentra, se crea.
				#Se crea la base de datos cuyo nombre sera el nombre de la cuidad
				db_telefonos.Execute("create table telefonos (ID int,telefono text)")
				#Se crea la tabla telefonos
				id_telefono=1
				numeros_cuidad = [] #Lista para guardar todos los numeros que coincidan con la id de la cuidad
				for numero in numeros:
					if id == numero[1]:
						numeros_cuidad.append(numero)

				numeros_aux= numeros_cuidad[corte:corte+7] #Los numeros de la cuidad se dividen en bloques de 7000
				#Primera id de la tabla
				for numero in tqdm(numeros_aux,colour='green',desc=colored(f'Cargando numeros localidad {localidades_dict[id]}','green')):
					if id == numero[1]:
						db_telefonos.Execute(f'insert into telefonos (ID, telefono) values ({id_telefono},{numero[2]})')
						#Se inserta en la tabla el telefono correspondiente a la cuidad si coincide la id
						id_telefono=id_telefono+1
				corte = corte + 7 #Se suma de a 7000 para que no se repitan los numeros en las bdd de una misma cuidad
	except Exception as e:
		print(e)
	
	
	
if __name__ == "__main__":
	main()
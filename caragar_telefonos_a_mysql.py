import random
from  tqdm import tqdm
from termcolor import colored
import xlrd
import mysql.connector
import json
from pick import pick

def main():
	'''
	Funcion para cargar los numeros de telefonos necesarios a la tabla numeros de la bdd MYSQL
	
	'''
	with open('config.json') as config_file:
		config = json.load(config_file) #Se carga el archivo de configuracion de la BDD
	mydb = mysql.connector.connect(**config) #Se carga la BDD
	cursor=mydb.cursor()
	campanias_dict = {}
	query = f"select * from campanias" #Se buscan las campanias en la BDD
	try:
		cursor.execute(query)
		for row in cursor:
			campanias_dict.update({row[0]:[row[4],row[10]]}) #Se guardan la id, nombre y cant de numeros
	except Exception as e:
		print(f'Error en query: {query}, exception: {e}')

	titulo = 'Por favor, seleccione la campania con la que va a trabajar: '
	campanias_list = []
	for id in campanias_dict:
		campanias_list.append(campanias_dict.get(id)[0])
	campanias_list, indice = pick(campanias_list, titulo)

	for camp in campanias_dict:
		if(campanias_list==campanias_dict.get(camp)[0]):
			id_campania = camp
	localidades_dict={}
	query= f"""SELECT *
			FROM localidades l
			JOIN campanias_has_localidades chl 
			ON l.Id = chl.localidades_Id
			WHERE chl.campanias_Id = '{id_campania}'"""#Se buscan las campanias en la BDD
	try:
		cursor.execute(query)
		for row in cursor:
			localidades_dict.update({row[0]:[row[1],row[2]]}) #Se guardan la id, caracteristica y nombre de localidad
	except Exception as e:
		print(f'Error en query: {query}, exception: {e}')

	print (localidades_dict)

	
	cursor.execute("truncate table numeros") #Se eliminan los numeros previamente cargados
	
	cant_numeros = campanias_dict.get(id_campania)[1]
	cant_numeros = cant_numeros/1000
	total_numeros = cant_numeros * len(localidades_dict)
	print(cant_numeros)
	lista_telefonos= random.sample(range(500000,(500000+int(total_numeros))),int(total_numeros)) #Se generar aleatoriamente los numeros de telefono
	corte=0
	for id in localidades_dict:
		for numero in tqdm(lista_telefonos[corte:int(corte+cant_numeros)],colour='green'
		,desc=colored(f'Cargando numeros localidad {localidades_dict[id][1]}','green')):
			query=(f'insert into numeros (id_localidades, Numero) values ({id},{int(str(localidades_dict[id][0])+str(numero))})')
			try:
				
				cursor.execute(query) #Se ingresan los numeros a la BDD
			except:
				print(f'Error en query: {query}')
			
		corte=int(corte+cant_numeros)
	mydb.commit()
	cursor.close()

if __name__ == "__main__":
	main()





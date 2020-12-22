from os import getcwd
import random
import sys
import os
from comtypes.client import CreateObject
from comtypes.gen import Access
from  tqdm import tqdm
from termcolor import colored
import xlrd
import mysql.connector
import json

def main():
	'''
	Script para guardar las localidades y sus caracteristicas en la bdd MYSQL
	Esta funcion es extra al TP
	
	'''

	with open('config.json') as config_file:
			CONFIG = json.load(config_file)
	mydb = mysql.connector.connect(**CONFIG)
	cursor=mydb.cursor()
	lista_loc=[]
	for row in cursor:
		print(row)
	
	with xlrd.open_workbook('Rangos.xls') as wb:
		ws = wb.sheet_by_index(0)
		lista_localidades=ws.col_values(0)
		lista_cod_area=ws.col_values(1)
		localidades_dict=dict(zip(lista_localidades,lista_cod_area))
	
	cursor.execute('truncate table localidades')
	
	for localidad in localidades_dict:
		cod_area=localidades_dict[localidad]
		query=f'insert into localidades (Caracteristica,Localidad) values ({cod_area},"{localidad}")'
		print(query)
		cursor.execute(query)
	cursor.close()

main()
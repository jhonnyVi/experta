#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import logging
import requests
import os
from datetime import datetime
from ftplib import FTP
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")




def buscar():
	logging.info('Conectando con api GET : http://services.groupkt.com/country/search?text='+str(sys.argv[1]) )
	req = requests.get('http://services.groupkt.com/country/search?text='+str(sys.argv[1]))
	logging.info('Resultados de petición: '+str(req.json()) )
	return req.json()

def crearArchivoTmp(res):
	logging.info('Eliminando archivo temporal /tmp/responseExperta.txt')
	try:
		os.remove("/tmp/responseExperta.txt")
	except FileNotFoundError:
		pass
	logging.info('Creando archivo temporal /tmp/responseExperta.txt')
	file = open("/tmp/responseExperta.txt","w") 
	file.write("Pais: "+str(sys.argv[1])+'\n')
	file.write("Respuesta: "+str(res)+'\n')
	file.close()
	logging.info('Archivo temporal con respuesta /tmp/responseExperta.txt creado')

def escribirFtp(res):

	host = config.get("FTP",'hostname')
	user = config.get("FTP",'user')
	passwd= config.get("FTP",'password')
	logging.info('Conectando al FTP '+host)
	tp = FTP(host, user, passwd)
	logging.info('Conetado a FTP '+host)
	tp.cwd('/home')
	logging.info('Subiendo Archivo '+'response'+str(sys.argv[1])+'.csv')
	f = open("/tmp/responseExperta.txt", 'rb')
	tp.storbinary('STOR '+'response'+str(sys.argv[1])+'.csv', f)
	logging.info('Archivo se encuentra en el FTP '+host)


logging.basicConfig(filename='example.log',datefmt='%m/%d/%Y %I:%M:%S %p',format='%(asctime)s %(levelname)s:%(message)s',level=logging.DEBUG)
logging.debug('------------------------------------------------------------')
logging.debug('------------------------------------------------------------')
logging.info(' Archivo Ejecutado: '+str(sys.argv[0]))
logging.info(' Parametro recibido: '+str(sys.argv[1]))

res=buscar()

try:
	crearArchivoTmp(res)
	try:
		escribirFtp(res)
		logging.info('Proceso terminado al 100%')
		print(str(sys.argv[1])+' '+str(res) )
		
	except:
		logger.error('Error escribiendo en el FTP :'+sys.exc_info()[0])
except:
	logger.error('Error creando archivo temporal :'+sys.exc_info()[0])

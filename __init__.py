#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import logging
import requests
import os
import paramiko
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

def escribirFtp():

	host = config.get("FTP",'hostname')
	user = config.get("FTP",'user')
	passwd= config.get("FTP",'password')
	logging.info('Conectando al FTP '+host)
	tp = FTP(host, user, passwd)
	logging.info('Conetado a FTP '+host)
	tp.cwd('/home')
	print(tp.dir())
	logging.info('Subiendo Archivo '+'response'+str(sys.argv[1])+'.txt')
	f = open("/tmp/responseExperta.txt", 'rb')
	tp.storbinary('STOR '+'response'+str(sys.argv[1])+'.txt', f)
	logging.info('Archivo se encuentra en el FTP '+host)

def escribirSSH():
	ssh_client =paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(hostname=config.get("SSH",'hostname'),username=config.get("SSH",'user'),password=config.get("SSH",'password'),port=config.getint("SSH",'puerto'))
	stdin,stdout,stderr=ssh_client.exec_command("cd /home")
	stdin,stdout,stderr=ssh_client.exec_command("ls")
	print(stdout.readlines()) 	
	origen='/tmp/responseExperta.txt'
	detino='/home/response'+str(sys.argv[1])+'.txt'
	sftp = ssh_client.open_sftp()
	sftp.put(origen,detino)


logging.basicConfig(filename='example.log',datefmt='%m/%d/%Y %I:%M:%S %p',format='%(asctime)s %(levelname)s:%(message)s',level=logging.DEBUG)
logging.debug('------------------------------------------------------------')
logging.debug('------------------------------------------------------------')
logging.info(' Archivo Ejecutado: '+str(sys.argv[0]))
logging.info(' Parametro recibido: '+str(sys.argv[1]))

res=buscar()

try:
	crearArchivoTmp(res)
	try:
		escribirFtp()
		#escribirSSH()
		logging.info('Proceso terminado al 100%')
		result=res['RestResponse']['result']
		result='Sin Resultaods' if not result else str(result[0]['alpha2_code'])+','+str(result[0]['alpha3_code'])
		print(str(sys.argv[1])+': '+ result )  
	except:
		logger.error('Error escribiendo en el FTP :'+sys.exc_info()[0])
except:
	logger.error('Error creando archivo temporal :'+sys.exc_info()[0])


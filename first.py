#coding: utf-8

import os
import zipfile
import csv
from random import Random as RR
from hashlib import md5
from datetime import datetime
try:
	import xml.etree.cElementTree as etree
except ImportError:
	import xml.etree.ElementTree as etree


rand = RR().random

csv1=[]
csv2=[]
	

def randunic():
	m = md5()
	m.update(str(datetime.now().isoformat()).encode('utf-8'))
	return m.hexdigest()


def rands():
	m = md5()
	m.update(str(rand()).encode('utf-8'))
	return m.hexdigest()


def newXML():
	global max10
	global max100
	newroot = etree.Element("root") # рутовый элемент 
	newvar = etree.SubElement(newroot, "var") # добавляем дочерний элемент к root 
	newvar.set('name', u"id") # добавляем значение элемента
	newvar.set('value', randunic()) # добавляем значение элемента
	newvar = etree.SubElement(newroot, "var") # добавляем дочерний элемент к root 
	newvar.set('name', u"level") # добавляем значение элемента
	tmp=1+int(rand()*100)
	newvar.set('value', str(tmp)) # добавляем значение элемента
	
	newobjects = etree.SubElement(newroot, "objects") # добавляем дочерний элемент к root 
	tmp = 1+int(rand()*10)
	for i in range(tmp):
		newobject = etree.SubElement(newobjects, "object") # добавляем дочерний элемент
		newobject.set('name', rands()) # добавляем значение
		
	message = etree.tostring(newroot, "utf-8") # формируем XML документ в строку message
	#doc = '' + message # Добавляем строчку кодировки для xml файла
	###################### выводим результат формирования xml на экран ############
	#print message
	#print doc#.decode('utf-8') #меняем кодировку чтобы под виндовс было понятно что написано русскими буквами 
	return message


def fsave(name, data):
	outputfile = open(r''+name+'.xml', "wb")
	outputfile.write(data)
	outputfile.close()


def createData():
	try:
		os.makedirs('data')
		os.chdir('data')
	except OSError:
		pass
	for i in range(50):
		numer = str(i)
		os.makedirs(numer)
		z = zipfile.ZipFile(numer + '.zip', 'w')        # Создание нового архива
		os.chdir(numer)
		for f in range(100):
			fsave(str(f), newXML())
			z.write(os.path.join('',str(f)+'.xml'))         # Создание относительных путей и запись файлов в архив
		z.close()
		for root, dirs, files in os.walk('.'): # Список всех файлов и папок в директории
			for file in files:
				os.remove(file)
		os.chdir('..')
		os.removedirs(numer)
	os.chdir('..')
	print('First step done')


def scsv():
	with open('csv1.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(csv1)
	with open('csv2.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(csv2)
		

def parsedata(data):
	global csv1
	global csv2
	oldroot = etree.fromstring(data)
	for vari in oldroot.findall('var'):
		for vv in oldroot.findall('var'):
			if vv.get('name')=='id':
				id = vv.get('value')
			if vv.get('name')=='level':
				level=vv.get('value')
	csv1.append([id,level])
	for obj in oldroot.iter('object'):
		csv2.append([id, obj.get('name')])
	

def analyseData():
	#os.chdir('data')
	for root, dirs, files in os.walk('data'): # Список всех файлов и папок в директории data
		for file in files:
			z = zipfile.ZipFile(os.path.join(root,file), 'r')
			for xml in z.namelist():
				data = z.read(xml)
				parsedata(data)
	scsv()


def main():
	createData()
	input('Press any key for second step..')
	analyseData()
	
	return 0


if __name__ == '__main__':
	main()
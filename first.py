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


rand = RR().random #для короткого вызова случайного числа

csv1=[] #данные для сохранения csv файлов
csv2=[]
	

"""
Функция формирует уникальное "случайное" строковое значение
"""
def randunic():
	m = md5()
	m.update(str(datetime.now().isoformat()).encode('utf-8'))
	return m.hexdigest()


"""
Случайное строковое значение
"""
def rands():
	m = md5()
	m.update(str(rand()).encode('utf-8'))
	return m.hexdigest()


"""
xml-данные для сохранения в файл
"""
def newXML():
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
	return message


"""
Сохранение одного файла xml
"""
def fsave(name, data):
	outputfile = open(r''+name+'.xml', "wb")
	outputfile.write(data)
	outputfile.close()


"""
Основной алгоритм первой части задания
"""
def createData():
	try:
		os.makedirs('data') #Создаем и переходим в новую папку. Папка на момент запуска программы должна отсутствовать.
	except OSError:
		pass
	os.chdir('data')
	for i in range(50):
		numer = str(i)
		os.makedirs(numer) #Создаем временную папку
		z = zipfile.ZipFile(numer + '.zip', 'w')        # Создание очередного архива из 50
		os.chdir(numer)
		for f in range(100):
			fsave(str(f), newXML())
			z.write(os.path.join('',str(f)+'.xml'))         # Создание очередного файла xml и запись его в архив
		z.close()
		for root, dirs, files in os.walk('.'): # Список всех файлов и папок в директории
			for file in files:
				os.remove(file) #Удаляем временные файлы
		os.chdir('..')
		os.removedirs(numer) #Удаляем временную папки
	os.chdir('..')
	print('First step done')


"""
Сохранение файлов csv на диск
"""
def scsv():
	with open('csv1.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(csv1)
	with open('csv2.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(csv2)
		

"""
Анализ xml файла
"""
def parsedata(data):
	global csv1
	global csv2
	oldroot = etree.fromstring(data) #Парсим переданную строку
	for vari in oldroot.findall('var'):
		for vv in oldroot.findall('var'):
			if vv.get('name')=='id':
				id = vv.get('value')
			if vv.get('name')=='level':
				level=vv.get('value')
	csv1.append([id,level]) #Записываем в первый параметр для последующего сохранения
	for obj in oldroot.iter('object'):
		csv2.append([id, obj.get('name')]) #записываем во второй параметр


"""
Основной алгоритм второй части задачи
"""
def analyseData():
	#os.chdir('data')
	for root, dirs, files in os.walk('data'): # Список всех файлов и папок в директории data
		for file in files:
			z = zipfile.ZipFile(os.path.join(root,file), 'r') #Открываем архив на чтение
			for xml in z.namelist():
				data = z.read(xml) # чтение данных конкретного файла архива
				parsedata(data) # парсинг
	scsv() # сохранение


def main():
	createData() # первая часть
	input('Press any key for second step..')
	analyseData() # вторая часть
	print('All done')
	return 0


if __name__ == '__main__':
	main()
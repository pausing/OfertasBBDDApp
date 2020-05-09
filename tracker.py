import csv
from itertools import islice
import matplotlib.pyplot as mplot
from datetime import datetime
from texttable import Texttable

class tracker:
	def __init__(self, id, atributos):
		#tecnicos
		#identificador de item
		self.id = id
		#atributos segun ['Calibre','Voltaje','Nivel de aislamiento','Normativa de fabricacion', 'Tipo de cubierta','
		# Precio unitario','Divisa','INCOTERMS','Proyecto / oferta', 'Fecha','Proveedor']
		self.atributos = atributos
	
	def atributosIdtracker():
		a = ['id','tipo','galva','velViento','alimen','coms','pu','div','inco','proy','fecha','prov']
		return a

	def __str__(self):
		s = str(self.id)
		for i in range(len(tracker.atributosIdtracker())-1):
			if i == (tracker.atributosIdtracker().index('fecha')-1): 
				s = s + ', ' + dateToString(self.atributos[i])
			else:
				s = s + ', ' + str(self.atributos[i])
		return s

	def atributosTitulostracker():
		a=['Tipologia','Galvanizado','Velocidad del viento','Tipo alimentacion', \
			'Comunicaciones','Precio unitario','Divisa','INCOTERMS','Proyecto / oferta', \
			'Fecha','Proveedor']
		return a

	def trackerToList(self):
		a=[self.id]
		for i in range(len(tracker.atributosIdtracker())-1):
			if i == (tracker.atributosIdtracker().index('fecha')-1):
				f = dateToString(self.atributos[i])
				a.append(f)
			else:
				a.append(self.atributos[i])
		return a

def cargarBBDDtracker(path):
	indiceInicio = 1
	l = []
	with open(path) as f:
		bbdd = list(csv.reader(f))
		for r in islice(bbdd, indiceInicio, None):
			atr = []
			indexFecha = tracker.atributosIdtracker().index('fecha')
			for i in range(1,indexFecha,1):
				atr.append(r[i])
			s = r[indexFecha]
			dia = int(s[0:s.index('/')])
			subS = s[s.index('/')+1:]
			mes= int(subS[0:subS.index('/')])
			subS2 = subS[subS.index('/')+1:]
			anyo = int(subS2)
			atr.append(datetime(anyo,mes,dia))
			for i in range(indexFecha+1,len(r),1):
				atr.append(r[i])
			l.append(tracker(r[0],atr))
	return l

def cargarItemEnBBDDtracker(bbdd,at):
	if len(bbdd)==0:
		bbdd.append(tracker(1,at))
	else:
		bbdd.append(tracker(str(int(bbdd[len(bbdd)-1].id)+1),at))
	return bbdd

def verificarEntradaCLItracker(entrada,numEntrada,modificadorNumEntrada):
	# TODO verificacion de cada una de las entradas
	return True

def ItemDesdeCLI():
	at = []
	titulosFecha = ['dia','mes','anyo']
	for i in range(len(tracker.atributosTitulostracker())):
		if i == (tracker.atributosIdtracker().index('fecha')-1):
			f = ''
			fechaS = []
			for k in range(3):
				entradaTemp = input(tracker.atributosTitulostracker()[i] + ' (' + titulosFecha[k] + '): ').upper()
				while verificarEntradaCLItracker(entradaTemp,i,k)==False:
					print('Error en la entrada de datos, repetir')
					entradaTemp = input(tracker.atributosTitulostracker[i] + ': ').upper()
				fechaS.append(int(entradaTemp) if entradaTemp!='' else 1)
			f = datetime(fechaS[2],fechaS[1],fechaS[0])
			at.append(f)
		else:
			entradaTemp = input(tracker.atributosTitulostracker()[i] + ': ').upper()
			while verificarEntradaCLItracker(entradaTemp, i,None)==False:
				print('Error en la entrada de datos, repetir')
				entradaTemp = input(tracker.atributosTitulostracker[i] + ': ').upper()
			at.append(entradaTemp)
	return at

def buscarItemBBDDtracker(bbdd,valor,atributo):
	# En base a un valor de atributo devolver el indice de la primera vez que se encuentra en bbdd
	atr = atributo 
	result = -1
	for i in range(len(bbdd)):
		if tracker.trackerToList(bbdd[i])[tracker.atributosIdtracker().index(atributo)] == valor:
			result = i
			break
	return result

def filtrarItemBBDDtrackerDialogo(bbdd):
	numAtr = input('Numero de atributos a filtar: ')
	print(str(tracker.atributosIdtracker()))
	atributos = []
	valores = []
	for i in range(int(numAtr)):
		atributos.append(input('Atributo ' + str(i+1) + ' de ' + str(numAtr) + ': '))
	for i in range(int(numAtr)):
		valores.append(input('Valor ' + str(i+1) + ' de ' + str(numAtr) + ': ').upper())
	bbddFiltrada = filtrarItemBBDDtracker(bbdd, valores, atributos)
	
	return bbddFiltrada

def filtrarItemBBDDtracker(bbdd,valor,atributo):
	# En base a un valor de atributo devolver el indice de la primera vez que se encuentra en bbdd
	bbddFiltrada = []
	numAtr = len(atributo)
	for i in range(len(bbdd)):
		encontrado = True
		for k in range(numAtr):
			encontrado = encontrado and \
			(tracker.trackerToList(bbdd[i])[tracker.atributosIdtracker().index(atributo[k])] == valor[k])
		if encontrado:
			bbddFiltrada.append(bbdd[i])
	return bbddFiltrada

def eliminarItemtracker(bbdd):
	op = input('Indicar id de item a eliminar (o salir [esc]): ')
	if op == 'esc':
		print('Opcion salir')
		return bbdd
	else:
		indice = buscarItemBBDDtracker(bbdd, op, 'id')
		if indice != -1:
			bbdd.pop(indice)
			print('Id ' + str(op) + ' eliminado')
			return bbdd
		else:
			print('Id no encontrado')
			return bbdd

def modificarItemtracker(bbdd):
	op = input('Indicar id de item a modificar (o salir [esc]): ')
	if op == 'esc':
		print('Opcion salir')
		return bbdd
	else:
		indice = buscarItemBBDDtracker(bbdd, op, 'id')
		if indice != -1:
			TitulosAtr = tracker.atributosTitulostracker()			
			for i in range(len(TitulosAtr)-1):
				antiguoAtr = bbdd[indice].atributos[i] if i != (tracker.atributosIdtracker().index('fecha')-1) else dateToString(bbdd[indice].atributos[i])
				nuevoAtr = input(TitulosAtr[i] + ' [' + antiguoAtr + ']: ')
				if nuevoAtr == 'esc':
					break
				elif (nuevoAtr != antiguoAtr) and nuevoAtr != '':
					bbdd[indice].atributos[i] = nuevoAtr.upper() if i != (tracker.atributosIdtracker().index('fecha')-1) else stringToDatetime(nuevoAtr)
			return bbdd
		else:
			print('Id no encontrado')
			return bbdd

def graficartracker(bbdd):
	bbbddFiltrada = filtrarItemBBDDtrackerDialogo(bbdd)
	
	fig , ax = mplot.subplots(1,1,figsize=[2*6.4,2*4.8])
	# indice de la fecha
	indiceFecha = tracker.atributosIdtracker().index('fecha') - 1
	indicePrecio = tracker.atributosIdtracker().index('pu') - 1
	
	fechas = []
	for i in range(len(bbbddFiltrada)):
		fechas.append(bbbddFiltrada[i].atributos[indiceFecha])
	precios = []
	for i in range(len(bbbddFiltrada)):
		precios.append(float(bbbddFiltrada[i].atributos[indicePrecio]))
	ax.plot(fechas,precios,'x')
	anotaciones = []
	for i in range(len(bbbddFiltrada)):
		s = '['
		# proveedor
		s = s + bbbddFiltrada[i].atributos[tracker.atributosIdtracker().index('prov')-1] + ', '
		# divisa
		s = s + bbbddFiltrada[i].atributos[tracker.atributosIdtracker().index('div')-1] + ', '
		# incoterms
		s = s + bbbddFiltrada[i].atributos[tracker.atributosIdtracker().index('inco')-1] + ']'
		anotaciones.append(s)
	for i in range(len(bbbddFiltrada)):
		mplot.annotate(anotaciones[i], (fechas[i],precios[i]))
	
	ax.grid(True)
	ax.set_xlabel('Fecha')
	ax.set_ylabel('Precio')
	mplot.show()

def dateToString(d):
	return str(d.day) + '/' + str(d.month) + '/' + str(d.year)

def stringToDatetime(s):
	dia = int(s[0:s.index('/')])
	subS = s[s.index('/')+1:]
	mes = int(subS[0:subS.index('/')])
	anyo= int(subS[subS.index('/')+1:])
	d = datetime(anyo, mes, dia)
	return d

def mostrarBBDD(bbdd):
	t = Texttable(0)
	t.header(tracker.atributosIdtracker())
	for i in range(len(bbdd)):
		t.add_row(bbdd[i].trackerToList())
	print(t.draw())




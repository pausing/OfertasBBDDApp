import csv
import os
from itertools import islice
import cable
from cable import cable as cab
from colorama import init
init()
from colorama import Fore, Back, Style
import tracker
from tracker import tracker as tr


nombreAPP = 'BBDDofertasAPP'
version = '02'

#definicion funciones
def nombrarBasesDatosDisponibles():
	print('Bases de datos disponibles: ')
	for i in range(len(basesDatos)):
		print(str(i+1) + '.-' + bbddPATHs[i])

#inicio app
print()
print(Fore.RED + Back.BLUE + 'Bienvenido a ' + nombreAPP + ' v_' + version + Style.RESET_ALL)
print()

#cargar base de datos
#cables MEDIA TENSION, archivo ofertascable.csv
#1.- verificar si exsite

bbddPATHs = []
basesDatos = []
bbddPATHs.append('ofertasCABLE.csv')
bbddPATHs.append('ofertasTRACKER.csv')

for i in range(len(bbddPATHs)):
	print(i)
	if os.path.exists(bbddPATHs[i]):
		if i == 0:
			basesDatos.append(cable.cargarBBDDcable(bbddPATHs[i]))
		elif i == 1:
			basesDatos.append(tracker.cargarBBDDtracker(bbddPATHs[i]))
		print('Se ha cargado la base de datos de ' + bbddPATHs[i])
		print('Hay: ' + str(len(basesDatos[i])) + ' elementos.')
	else: 
		print('No se ha encontrado base de datos de ' + bbddPATHs[i])
		basesDatos.append([])

op = '' 
while op.upper() != 'S': 
	op = input(Fore.CYAN + Back.BLUE + '\nInserte opcion [Cargar, Mostar, moDificar, Eliminar, Filtrar, Graficar, Salir]:' + Style.RESET_ALL + ' ')
	if op.upper() == 'C':
		os.system('cls' if os.name == 'nt' else 'clear')
		print('\nCargar nuevo item en base de datos: ')
		nombrarBasesDatosDisponibles()
		op2 = input('Especifique base de datos a cargar: ')
		if op2 == '1':
			at = cable.ItemDesdeCLI()
			basesDatos[0] = cable.cargarItemEnBBDDcable(basesDatos[0],at) 
		elif op2 == '2':
			at = tracker.ItemDesdeCLI()
			basesDatos[1] = tracker.cargarItemEnBBDDtracker(basesDatos[1],at)
	if op.upper() == 'M':
		os.system('cls' if os.name == 'nt' else 'clear')
		print('\nMostrar BBDD: ')
		nombrarBasesDatosDisponibles()
		op2 = input('Especifique base de datos a mostrar: ')
		if op2 == '1':
			cable.mostrarBBDD(basesDatos[0])
		elif op2 == '2':
			tracker.mostrarBBDD(basesDatos[1])
	if op.upper() == 'E':
		os.system('cls' if os.name == 'nt' else 'clear')
		print('\nEliminar registro: ')
		nombrarBasesDatosDisponibles()
		op2 = input('Especifique base de datos a eliminar: ')
		if op2 == '1':
			cable.eliminarItemcable(basesDatos[0])
		elif op2 == '2':
			tracker.eliminarItemtracker(basesDatos[1])
	if op.upper() == 'F':
		os.system('cls' if os.name == 'nt' else 'clear')
		print('\nFiltrar:')
		nombrarBasesDatosDisponibles()
		op2 = input('Especifique base de datos a filtrar: ')
		if op2 == '1':
			baseDatosFiltrada = cable.filtrarItemBBDDcableDialogo(basesDatos[0])
		elif op2 == '2':
			baseDatosFiltrada = tracker.filtrarItemBBDDtrackerDialogo(basesDatos[1])
		if len(baseDatosFiltrada)==0:
			print('\nNo se encuentra la busqueda especificada')
		else:
			numItems =  len(baseDatosFiltrada)
			print('\n' + ('Se ha encontrado ' if numItems == 1 else 'Se han encontrado ') + str(numItems) + \
				(' item' if numItems == 1 else ' items'))
			if op2 == '1':
				cable.mostrarBBDD(baseDatosFiltrada)
			elif op2 == '2':
				tracker.mostrarBBDD(baseDatosFiltrada)
	if op.upper() == 'D':
		os.system('cls' if os.name == 'nt' else 'clear')
		print('\nModificar item: ')
		nombrarBasesDatosDisponibles()
		op2 = input('Especifique base de datos a modificar: ')
		if op2 == '1':
			basesDatos[0] = cable.modificarItemcable(basesDatos[0])
		elif op2 == '2':
			basesDatos[1] = tracker.modificarItemtracker(basesDatos[1])
	if op.upper() == 'G':
		os.system('cls' if os.name == 'nt' else 'clear')
		print('\nGraficar:')
		nombrarBasesDatosDisponibles()
		op2 = input('Especifique base de datos a graficar: ')
		if op2 == '1':
			cable.graficarcable(basesDatos[0])
		elif op2 == '2':
			tracker.graficartracker(basesDatos[1])

if input('Guardar cambios en bases de datos? [s,n]: ')=='s':
	#GUARDAR BBDD
	for i in range(len(basesDatos)):
		guardarBaseDatosI = input('Guardar base de datos ' + str(bbddPATHs[i]) + '? [s,n]: ')
		if guardarBaseDatosI == 's':
			with open(bbddPATHs[i],mode='w',newline='\n',encoding='utf-8') as f:
				w = csv.writer(f)
				titulos = ['id']
				if i == 0:
					for j in range(len(cab.atributosTituloscable())):
						titulos.append(cab.atributosTituloscable()[j])
				elif i == 1:
					for j in range(len(tr.atributosTitulostracker())):
						titulos.append(tr.atributosTitulostracker()[j])
				w.writerow(titulos)
				for r in basesDatos[i]:
					#print(cab.cableToList(r))
					if i == 0:
						w.writerow(cab.cableToList(r))
					elif i == 1:
						w.writerow(tr.trackerToList(r))



import csv
import os
from itertools import islice
import cable
from cable import cable as cab
from colorama import init
init()
from colorama import Fore, Back, Style


nombreAPP = 'BBDDofertasAPP'
version = '02'

#inicio app
print()
print(Fore.RED + Back.BLUE + 'Bienvenido a ' + nombreAPP + ' v_' + version + Style.RESET_ALL)
print()
#cargar base de datos
#	cables MEDIA TENSION, archivo ofertascable.csv
#	1.- verificar si exsite

oCPATH = 'ofertasCABLE.csv'
indiceInicio = 0
atributosCablesMT = 11

if os.path.exists(oCPATH):
	cableBBDD = cable.cargarBBDDcable(oCPATH)
	print('Se ha cargado la base de datos de ' + oCPATH)
	print('Hay: ' + str(len(cableBBDD)) + ' elementos.')
else:
	print('No se ha encontrado base de datos.')
	cableBBDD = []

op = ''
while op.upper() != 'S':
	op = input(Fore.CYAN + Back.BLUE + '\nInserte opcion [Cargar, Mostar, moDificar, Eliminar, Filtrar, Graficar, Salir]:' + Style.RESET_ALL + ' ')
	if op.upper() == 'C':
		os.system('cls' if os.name == 'nt' else 'clear')
		print('\nCargar nuevo item en BBDD: ')
		at = cable.ItemDesdeCLI()
		cableBBDD = cable.cargarItemEnBBDDcable(cableBBDD,at)
	if op.upper() == 'M':
		os.system('cls' if os.name == 'nt' else 'clear')
		print('\nMostrar BBDD: ')
		cable.mostrarBBDD(cableBBDD)
	if op.upper() == 'E':
		os.system('cls' if os.name == 'nt' else 'clear')
		print('\nEliminar registro: ')
		cableBBDD = cable.eliminarItemcable(cableBBDD)
	if op.upper() == 'F':
		os.system('cls' if os.name == 'nt' else 'clear')
		print('\nFiltrar:')
		cableBBDDFiltrada = cable.filtrarItemBBDDcableDialogo(cableBBDD)
		if len(cableBBDDFiltrada)==0:
			print('\nNo se encuentra la busqueda especificada')
		else:
			numItems =  len(cableBBDDFiltrada)
			print('\n' + ('Se ha encontrado ' if numItems == 1 else 'Se han encontrado ') + str(numItems) + \
				(' item' if numItems == 1 else ' items'))
			cable.mostrarBBDD(cableBBDDFiltrada)
	if op.upper() == 'D':
		os.system('cls' if os.name == 'nt' else 'clear')
		print('\nModificar item: ')
		cableBBDD = cable.modificarItemcable(cableBBDD)
	if op.upper() == 'G':
		os.system('cls' if os.name == 'nt' else 'clear')
		print('\nGraficar:')
		cable.graficarcable(cableBBDD)

if input('Guardar cambios en BBDDs? [s,n]: ')=='s':
	#TODO GUARDAR BBDD
	with open (oCPATH,mode='w',newline='\n',encoding='utf-8') as f:
		w = csv.writer(f)
		titulos = ['id']
		for i in range(len(cab.atributosTituloscable())):
			titulos.append(cab.atributosTituloscable()[i])
		w.writerow(titulos)
		for r in cableBBDD:
			#print(cab.cableToList(r))
			w.writerow(cab.cableToList(r))
"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """


import config as cf
import sys
import threading
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Puntos de interconexión aérea")
    print("3- Clústeres de tráfico aéreo")
    print("4- Ruta más corta entre ciudades")
    print("5- Utilizar las millas de viajero")
    print("6- Cuantificar el efecto de un aeropuerto cerrado")

def prntOptions(lst):
    num = 0
    for cd in lt.iterator(lst):
        num += 1
        print(str(num)+" "+ cd["city"],cd["country"],cd["lat"],cd["lng"])
    
catalog = None

"""
Menu principal
"""
def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            print("Cargando información de los archivos ....")
            catalog = controller.init()
            controller.loadAirports(catalog)
            controller.loadRoutes(catalog)
            controller.loadCities(catalog)
            print("El total de aeropuertos en el grafo dirigido es de: " + str(controller.totalVertex(catalog)))
            print("El total de rutas en el grafo dirigido es de: " + str(controller.totalEdge(catalog)))
            print("El total de aeropuertos en el grafo no dirigido de: " + str(controller.totalVertexgrafo(catalog)))
            print("El total de rutas en el grafo no dirigido es de: " + str(controller.totalEdgegrafo(catalog)))
            print("El total de ciudades es de: " + str(controller.totalCities(catalog)))

        elif int(inputs[0]) == 2:
            controller.puntointerconexion(catalog)
            ab = controller.cnsultatree(catalog)
            print(ab[0])
            print(ab[1])
            print(ab[2])
            


        elif int(inputs[0]) == 3:
            pass

        elif int(inputs[0]) == 4:
            city1= input("Ingrese el nombre de la ciudad de origen\n")
            city2= input("Ingrese el nombre de la ciuad de destino\n")
            lst_ct = controller.cities(catalog,city1,city2)
            print("seleccione la ciudad")
            prntOptions(lst_ct[0])
            selec1 = input()
            print("seleccione la ciudad")
            prntOptions(lst_ct[1])
            selec2 = input()
            print(lt.getElement(lst_ct[0],int(selec1)))
            print(lt.getElement(lst_ct[1],int(selec2)))
        elif int(inputs[0]) == 5:
            pass
        elif int(inputs[0]) == 6:
            pass
        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
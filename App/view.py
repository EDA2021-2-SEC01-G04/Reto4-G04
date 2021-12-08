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


from math import inf
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
    
def prntairports(lst):
    for airport in lt.iterator(lst):
        print("IATA: " +airport["IATA"],"Name: " + airport["Name"],"City: " +airport["City"],"Country: "+airport["Country"])
def prntairports2(lst,sz):
    print("IATA: "+lt.getElement(lst,1)["IATA"],"Name: " + lt.getElement(lst,1)["Name"],"City: "+lt.getElement(lst,1)["City"],"Country: "+lt.getElement(lst,1)["Country"])
    print("IATA: "+lt.getElement(lst,2)["IATA"],"Name: " + lt.getElement(lst,2)["Name"],"City: "+lt.getElement(lst,2)["City"],"Country: "+lt.getElement(lst,2)["Country"])
    print("IATA: "+lt.getElement(lst,3)["IATA"],"Name: " + lt.getElement(lst,3)["Name"],"City: "+lt.getElement(lst,3)["City"],"Country: "+lt.getElement(lst,3)["Country"])
    print("IATA: "+lt.getElement(lst,sz)["IATA"],"Name: " + lt.getElement(lst,sz)["Name"],"City: "+lt.getElement(lst,sz)["City"],"Country: "+lt.getElement(lst,sz)["Country"])
    print("IATA: "+lt.getElement(lst,sz-1)["IATA"],"Name: " + lt.getElement(lst,sz-1)["Name"],"City: "+lt.getElement(lst,sz-1)["City"],"Country: "+lt.getElement(lst,sz-1)["Country"])
    print("IATA: "+lt.getElement(lst,sz-2)["IATA"],"Name: " + lt.getElement(lst,sz-2)["Name"],"City: "+lt.getElement(lst,sz-2)["City"],"Country: "+lt.getElement(lst,sz-2)["Country"])
def prnRoutes(lst):
    for routes in lt.iterator(lst):
         print("Departure: "+routes["vertexA"],"Destination: "+routes["vertexB"],"Distanmce_Km: "+str(routes["weight"]))


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
            lst = controller.puntointerconexion(catalog)
            print(lt.size(lst))
            print(lt.getElement(lst,1))
            print(lt.getElement(lst,2))
            print(lt.getElement(lst,3))
            print(lt.getElement(lst,4))
            print(lt.getElement(lst,5))
            
        elif int(inputs[0]) == 3:
            air1 = input("ingrese el codigo IATA del primmer aeropuerto\n")
            air2 = input("ingrese el codigo IATA del segundo aeropuerto\n")
            info = controller.conectins(catalog,air1,air2)
            print(lt.getElement(info[2],1))
            print(lt.getElement(info[2],2))
            print("El numero de componentes fuertemente conectados es de: " + str(info[0]))
            print("Estan los dos aeropuertos conectados?\n" + str(info[1]))

        elif int(inputs[0]) == 4:
            city1= input("Ingrese el nombre de la ciudad de origen:\n")
            city2= input("Ingrese el nombre de la ciuad de destino:\n")
            lst_ct = controller.cities(catalog,city1,city2)
            print("Seleccione la ciudad")
            prntOptions(lst_ct[0])
            selec1 = input()
            print("Seleccione la ciudad")
            prntOptions(lst_ct[1])
            selec2 = input()
            #print(lt.getElement(lst_ct[0],int(selec1)))
            #print(lt.getElement(lst_ct[1],int(selec2)))
            ct1 = lt.getElement(lst_ct[0],int(selec1))
            ct2 = lt.getElement(lst_ct[1],int(selec2))
            info = controller.airportsInArea(catalog,ct1,ct2)
            print("--- El aeropuerto de salida desde la ciudad de "+city1+" ---")
            print()
            print(lt.getElement(info[1],1))
            print()
            print("--- El aeropuerto de llegada desde la ciudad de "+city2+" ---")
            print()
            print(lt.getElement(info[1],2))
            print()
            print("---  Resultados de Dijkstra ---")
            print("Distancia total: "+ str(info[0][1])+" (km)")
            prnRoutes(info[0][0])

        elif int(inputs[0]) == 5:
            city = input("Escriba el nombre del aeropuerto en formato IATA de la ciudad que desea: ")
            miles = int(input("Escriba sus millas: "))
            retorno = controller.flightbymiles(catalog,city,miles)
            print("Numero total de aeropuertos conectados al arbol: " + str(retorno[5]))
            print("Distancia total de todos los arcos:" + str(retorno[0]))
            print(retorno[1])
            print("Distancia total del recorrido presentado: " + str(retorno[2]))
            print("Distancia total del recorrido ida y vuelta: " + str(retorno[2]*2))
            print(retorno[3])
        elif int(inputs[0]) == 6:
            airport = input("Ingrese el codigo IATA del aeropuerto a cerrar:\n")
            lst = controller.deleteairport(catalog,airport)
            lst_air = lst[0]
            digrafo = lst[1]
            grafo = lst[2]
            sz = lt.size(lst_air)
            print("--- Grafo Dirigido ---")
            print("El numero originasl de aeropuertos: " + str(controller.totalVertex(catalog)) + " y rutas: " +  str(controller.totalEdge(catalog)))
            print("--- Grafo No Dirigido ---")
            print("El numero original de aeropuertos: " + str(controller.totalVertexgrafo(catalog)) + " y rutas: " +  str(controller.totalEdgegrafo(catalog)) + "\n")
            print("Aeropuerto removido con IATA: " + airport)
            print()
            print("--- Grafo Dirigido ---")
            print("El numero resultante de aeropuertos: " +str(digrafo[0])+ " y rutas:"+ str(digrafo[1]))
            print("--- Grafo No Dirigido ---")
            print("El numero resultante de aeropuertos: " +str(grafo[0])+ " y rutas:"+ str(grafo[1]))
            print()
            print("El numero de aeropuertos afectados es de: "+str(lt.size(lst[0])))
            if sz <= 6:
                prntairports(lst_air)
            else:
                prntairports2(lst_air,sz)
        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
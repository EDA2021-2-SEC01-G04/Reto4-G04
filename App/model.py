"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Utils import error as error
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    analyzer = {'digrafo': None,
                'grafo': None,
                "routes":None,
                "airports":None}
    analyzer['airports'] = mp.newMap(numelements=91000,maptype='PROBING')
    analyzer['routes'] = mp.newMap(numelements=91000,maptype='PROBING')
    analyzer['cities'] = mp.newMap(numelements=91000,maptype='PROBING')
    analyzer['digrafo'] = gr.newGraph(datastructure='ADJ_LIST',directed=True,size=91000,comparefunction=compareStopIds)
    analyzer['grafo'] =  gr.newGraph(datastructure='ADJ_LIST',directed=False,size=91000,comparefunction=compareStopIds)
    return analyzer


# Funciones para agregar informacion al catalogo
def addAirport(vertice,analyzer):
    if gr.containsVertex(analyzer["digrafo"],vertice["IATA"]) != True:
        gr.insertVertex(analyzer["digrafo"],vertice["IATA"])
        return analyzer
    

def hashAirports(analyzer,airport):
    entry = mp.get(analyzer["airports"],airport["IATA"])
    if entry is None:
        lst = lt.newList()
        lt.addLast(lst,airport)
        mp.put(analyzer["airports"],airport["IATA"],lst)
    else:
        lst = entry["value"]
        lt.addLast(lst,airport)

def routesByDeparture(analyzer,route):
    entry = mp.get(analyzer["routes"],route["Departure"])
    if entry is None:
        lst_rt = lt.newList()
        lt.addLast(lst_rt,route)
        mp.put(analyzer["routes"],route["Departure"],lst_rt)
    else:
        lst_rt = entry["value"]
        lt.addLast(lst_rt,route)
    return analyzer

def addRoutesConenctions(analyzer):
    lst_r = mp.keySet(analyzer["routes"])
    for key in lt.iterator(lst_r):
        lst = mp.get(analyzer['routes'], key)['value']
        for route in lt.iterator(lst):
            addConection(analyzer,route)
    return analyzer
def addConection(analyzer,route):
    info = gr.getEdge(analyzer["digrafo"],route["Departure"],route["Destination"])
    if info is None:
        gr.addEdge(analyzer["digrafo"],route["Departure"],route["Destination"],route["distance_km"])
    return analyzer


def hashcities(analyzer,citie):
    entry = mp.get(analyzer["cities"],citie["city"])
    if entry is None:
        lst = lt.newList()
        lt.addLast(lst,citie)
        mp.put(analyzer["cities"],citie["city"],lst)
    else:
        lst = entry["value"]
        lt.addLast(lst,citie)

# Funciones para creacion de datos
def totalVertex(analyzer):

    return gr.numVertices(analyzer["digrafo"])
def totalEdge(analyzer):
    return gr.numEdges(analyzer["digrafo"])

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1
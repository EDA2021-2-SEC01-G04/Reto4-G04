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



from math import inf
import config as cf
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
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
    analyzer['counter'] = 0
    analyzer["components"] = 0
    return analyzer


# Funciones para agregar informacion al catalogo
def addAirport(vertice,analyzer):
    if gr.containsVertex(analyzer["digrafo"],vertice["IATA"]) != True:
        gr.insertVertex(analyzer["digrafo"],vertice["IATA"])
    return analyzer

def addAirport2(vertice,analyzer):
    if gr.containsVertex(analyzer["grafo"],vertice["IATA"]) != True:
        gr.insertVertex(analyzer["grafo"],vertice["IATA"])
        return analyzer
    
def hashAirports(analyzer,airport):
    entry = mp.get(analyzer["airports"],airport["IATA"])
    if entry is None:
        lst = lt.newList()
        mp.put(analyzer["airports"],airport["IATA"],airport)


def routesByDeparture(analyzer,route):
    rt = (route["Departure"] + "-" + route["Destination"])
    entry = mp.get(analyzer["routes"],rt)
    if entry is None:
        lst_rt = lt.newList()
        lt.addLast(lst_rt,route)
        mp.put(analyzer["routes"],rt,lst_rt)
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
    gr.addEdge(analyzer["digrafo"],route["Departure"],route["Destination"],route["distance_km"])
    return analyzer


def hashcities(analyzer,city):
    entry = mp.get(analyzer["cities"],city["city"])
    if entry is None:
        lst = lt.newList()
        lt.addLast(lst,city)
        mp.put(analyzer["cities"],city["city"],lst)
    else:
        lst = entry["value"]
        lt.addLast(lst,city)

def counterCities(analyzer):
    analyzer['counter'] += 1




def addRoutesConenctions2(analyzer):
    lst_r = mp.keySet(analyzer["routes"])
    for key in lt.iterator(lst_r):
        if key != None:
            v1 = key.split("-")
            v1 = v1[1]+"-"+v1[0]
            lst = lt.isPresent(lst_r,v1)
            lst1 = lt.isPresent(lst_r,key)
            if lst != 0 and lst1 != 0:
                info = mp.get(analyzer["routes"],v1)
                info = me.getValue(info)
                lt.deleteElement(lst_r,lst)
                if info != None:
                    for route in lt.iterator(info):
                        addConection2(analyzer,route)
    return analyzer

def addConection2(analyzer,route):
    gr.addEdge(analyzer["grafo"],route["Departure"],route["Destination"],route["distance_km"])
    return analyzer

#----------------Punto1-----------------------
def puntointerconexion(analyzer):
    lst_k = gr.vertices(analyzer["digrafo"])
    tp1 = (0,0)
    tp2 = (0,0)
    tp3 = (0,0)
    tp4 = (0,0)
    tp5 = (0,0)
    for airport in lt.iterator(lst_k):
        sz = gr.degree(analyzer["digrafo"],airport)
        sz2 = gr.indegree(analyzer["digrafo"],airport)
        total = sz+sz2
        if tp1[0] <= total:
            tp5 = tp4
            tp4 = tp3
            tp3 = tp2
            tp2 = tp1
            tp1 = (total,airport,sz2,sz)
        elif tp2[0] <= total:
            tp5 =tp4
            tp4 = tp3
            tp3 = tp2
            tp2 = (total,airport,sz2,sz)

        elif tp3[0] <= total:
            tp5 = tp4
            tp4 = tp3
            tp3 = (total,airport,sz2,sz)
        elif tp4[0] <= total:
            tp5 = tp4
            tp4 = (total,airport,sz2,sz)
        elif tp5[0] <= total:
            tp5 = (total,airport,sz2,sz)
    
    return (tp1,tp2,tp3,tp4,tp5)
#-------------Punto2------------

# Funciones para creacion de datos
def totalVertex(analyzer):
    return gr.numVertices(analyzer["digrafo"])
def totalEdge(analyzer):
    return gr.numEdges(analyzer["digrafo"])

def totalVertexgrafo(analyzer):
    return gr.numVertices(analyzer["grafo"])
def totalEdgegrafo(analyzer):
    return gr.numEdges(analyzer["grafo"])

def totalCities(analyzer):
    return analyzer["counter"]
# Funciones de consulta
def cnsultatree(analyzer):
    mx = om.maxKey(analyzer["tree"])
    lst = om.get(analyzer["tree"],mx)
    lst = lst["value"]
    keylst = om.keySet(analyzer["tree"])
    return(mx,lt.getElement(lst,1),keylst)

def cities(analyzer,city1,city2):
    lst = mp.get(analyzer["cities"],city1)
    lst = lst["value"]
    lst2 = mp.get(analyzer["cities"],city2)
    lst2 = lst2["value"]
    return(lst,lst2)
#-----------------------Punto1-------------------------
def infoAirports(lts,analyzer):
    lst_arprts = lt.newList()
    for i in lts:
        info = mp.get(analyzer["airports"],i[1])
        info = info["value"]
        mensaje = "Name: " + info["Name"],"City: " + info["City"],"Country: " + info["Country"],"IATA: "+ info["IATA"],"connections: " + str(i[0]),"inbound: "+ str(i[2]),"outbound: " + str(i[3])
        lt.addLast(lst_arprts,mensaje)
    return lst_arprts
#-----------------------Punto2--------------------------
def connected(analyzer):
    analyzer["components"] = scc.KosarajuSCC(analyzer["digrafo"])
    return scc.connectedComponents(analyzer["components"])

def hasroute(analyzer,air1,air2):
    es = scc.stronglyConnected(analyzer["components"],air1,air2)
    return es
def getinfo(analyzer,air1,air2):
    lst = lt.newList()
    info1 = mp.get(analyzer["airports"],air1)
    info1 = me.getValue(info1)
    info2 = mp.get(analyzer["airports"],air2)
    info2 = me.getValue(info2)
    men1 = "IATA: "+air1,"Name: " + info1["Name"],"City: " + info1["City"],"Country: " + info1["Country"]
    lt.addLast(lst,men1)
    men2 = "IATA: "+air2,"Name: " + info2["Name"],"City: " + info2["City"],"Country: " + info2["Country"]
    lt.addLast(lst,men2)
    return lst
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
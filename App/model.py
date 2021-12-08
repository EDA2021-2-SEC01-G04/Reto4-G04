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
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim as pr
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Utils import error as error
from math import inf, radians, cos, sin, asin, sqrt
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
    analyzer['airports'] = mp.newMap(numelements=180000,maptype='PROBING')
    analyzer['routes'] = mp.newMap(numelements=180000,maptype='PROBING')
    analyzer['cities'] = mp.newMap(numelements=91000,maptype='PROBING')
    analyzer["valores"] = mp.newMap(numelements=2,maptype="PROBING")
    analyzer['digrafo'] = gr.newGraph(datastructure='ADJ_LIST',directed=True,size=180000,comparefunction=compareStopIds)
    analyzer['grafo'] =  gr.newGraph(datastructure='ADJ_LIST',directed=False,size=180000,comparefunction=compareStopIds)
    analyzer['counter'] = 0
    analyzer["components"] = 0
    analyzer["connections"] = 0
    return analyzer


# Funciones para agregar informacion al catalogo
def addAirport(vertice,analyzer):
    if gr.containsVertex(analyzer["digrafo"],vertice["IATA"]) != True:
        gr.insertVertex(analyzer["digrafo"],vertice["IATA"])
    if gr.containsVertex(analyzer["grafo"],vertice["IATA"]) != True:
        gr.insertVertex(analyzer["grafo"],vertice["IATA"])
    return analyzer
    
def hashAirports(analyzer,airport):
    entry = mp.get(analyzer["airports"],airport["IATA"])
    if entry is None:
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
        lst = mp.get(analyzer['routes'], key)
        lst = lst['value']
        for route in lt.iterator(lst):
            addConection(analyzer,route)
    return analyzer

def addConection(analyzer,route):
    gr.addEdge(analyzer["digrafo"],route["Departure"],route["Destination"],float(route["distance_km"]))
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

def hashValues(analyzer,num,value):
    if num == 0:
        entry = mp.get(analyzer["valores"],"ciudades")
        if entry is None:
            lst = lt.newList()
            lt.addLast(lst,value)
            mp.put(analyzer["valores"],"ciudades",lst)
        else:
            lst = entry["value"]
            lt.addLast(lst,value)
    elif num == 1:
        entry = mp.get(analyzer["valores"],"aeropuertos")
        if entry is None:
            lst = lt.newList()
            lt.addLast(lst,value)
            mp.put(analyzer["valores"],"aeropuertos",lst)
        else:
            lst = entry["value"]
            lt.addLast(lst,value)

def returnhashcities(analyzer):
    listcities = mp.get(analyzer["valores"],"ciudades")
    listcities = me.getValue(listcities)
    firstelement = lt.getElement(listcities,1)
    lastelement = lt.getElement(listcities,lt.size(listcities))
    texto1 = "Primera ciudad: " + str(firstelement["city"]) + ", Pais: "  + str(firstelement["country"]) + ", Latitud: " + str(firstelement["lat"]) + ", Longitud: " + str(firstelement["lng"]) + ", Poblacion: " + str(firstelement["population"]) + "\n"
    texto2 = "Ultima ciudad: " + str(lastelement["city"]) + ", Pais: "  + str(lastelement["country"]) + ", Latitud: " + str(lastelement["lat"]) + ", Longitud: " + str(lastelement["lng"]) + ", Poblacion: " + str(lastelement["population"])
    texto = texto1 + texto2
    return texto
def returnhashairports(analyzer):
    listairports = mp.get(analyzer["valores"],"aeropuertos")
    listairports = me.getValue(listairports)
    texto1 = "IATA: " + str(lt.getElement(listairports,1)["IATA"]) + ", Nombre: " + str(lt.getElement(listairports,1)["Name"]) + ", Ciudad: " + str(lt.getElement(listairports,1)["City"]) + ", Pais: " + str(lt.getElement(listairports,1)["Country"]) + ", Latitud: " + str(lt.getElement(listairports,1)["Latitude"]) + ", Longitud: " + str(lt.getElement(listairports,1)["Longitude"] + "\n")
    texto6 = "IATA: " + str(lt.getElement(listairports,lt.size(listairports))["IATA"]) + ", Nombre: " + str(lt.getElement(listairports,lt.size(listairports))["Name"]) + ", Ciudad: " + str(lt.getElement(listairports,lt.size(listairports))["City"]) + ", Pais: " + str(lt.getElement(listairports,lt.size(listairports))["Country"]) + ", Latitud: " + str(lt.getElement(listairports,lt.size(listairports))["Latitude"]) + ", Longitud: " + str(lt.getElement(listairports,lt.size(listairports))["Longitude"])
    texto = texto1 + texto6
    return texto

def counterCities(analyzer):
    analyzer['counter'] += 1




def addRoutesConenctions2(analyzer):
    lst_r = mp.keySet(analyzer["routes"])
    for key in lt.iterator(lst_r):
        if key != None:
            v1 = key.split("-")
            v1 = v1[1]+"-"+v1[0]
            lst = lt.isPresent(lst_r,v1)
            if lst != 0:
                info = mp.get(analyzer["routes"],v1)
                info = me.getValue(info)
                lt.deleteElement(lst_r,lst)
                if info != None:
                    for route in lt.iterator(info):
                        addConection2(analyzer,route)
    return analyzer

def addConection2(analyzer,route):
    gr.addEdge(analyzer["grafo"],route["Departure"],route["Destination"],float(route["distance_km"]))
    return analyzer

#----------------Punto1-----------------------
def puntointerconexion(analyzer):
    lst_k = gr.vertices(analyzer["digrafo"])
    lst = lt.newList()
    tp1 = (0,0)
    tp2 = (0,0)
    tp3 = (0,0)
    tp4 = (0,0)
    tp5 = (0,0)
    for airport in lt.iterator(lst_k):
        sz = gr.degree(analyzer["digrafo"],airport)
        sz2 = gr.indegree(analyzer["digrafo"],airport)
        total = sz+sz2
        if total != 0:
            lt.addLast(lst,total)
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
    
    return ((tp1,tp2,tp3,tp4,tp5),lst)
#-------------Punto2------------
#-------------Punto3------------
def functionhaversine(lat1, long1, lat2, long2):
    # codigo sacado de https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
      dLat = radians(lat2 - lat1)
      dLon = radians(long2 - long1)
      lat1 = radians(lat1)
      lat2 = radians(lat2)

      a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
      c = 2*asin(sqrt(a))
      rad_tierra = 6372.8

      return rad_tierra * c

def airportsInArea(analyzer,city):
    lst = mp.keySet(analyzer["airports"])
    lst_air = lt.newList()
    num = 0
    i = 1
    while i <= lt.size(lst):
        num += 10
        for airport in lt.iterator(lst):
            actual = mp.get(analyzer["airports"],airport)
            actual = actual["value"]
            distance = functionhaversine(float(city["lat"]),float(city["lng"]),float(actual["Latitude"]),float(actual["Longitude"]))
            if distance <= num :
                info = (airport,distance)
                lt.addLast(lst_air,info)
        if lt.size(lst_air) == 0:
            i += 1
        else:
            break
    
    return lst_air
def getminimunpath(analyzer,lst,lst2):
    init = lt.getElement(lst,1)
    dest = lt.getElement(lst2,1)
    info = minimuncost(analyzer,init[0],dest[0])
    #info[1] = info[1] + init[1] + dest[1]
    return info

def minimuncost(analyzer,airport,destination):
    connection = djk.Dijkstra(analyzer["digrafo"],airport)
    if djk.hasPathTo(connection,destination) is True:
        path = djk.pathTo(connection,destination)
        distance = djk.distTo(connection,destination)
        return (path,distance)
    else:
        return None
    


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
    for i in lts[0]:
        info = mp.get(analyzer["airports"],i[1])
        info = info["value"]
        mensaje = "Name: " + info["Name"],"City: " + info["City"],"Country: " + info["Country"],"IATA: "+ info["IATA"],"connections: " + str(i[0]),"inbound: "+ str(i[2]),"outbound: " + str(i[3])
        lt.addLast(lst_arprts,mensaje)
    total = lt.size(lts[1])
    return (lst_arprts,total)
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
#---------------------Punto3------------------------------
def getinforeq3(analyzer,lst,lst2):
    lst_arpts = lt.newList()
    init = lt.getElement(lst,1)
    dest = lt.getElement(lst2,1)
    init = mp.get(analyzer["airports"],init[0])
    dest = mp.get(analyzer["airports"],dest[0])
    init = init["value"]
    dest = dest["value"]
    mensaje1 = "IATA: " + init["IATA"],"Name: "+init["Name"],"City: "+init["City"],"Country: "+init["Country"] 
    mensaje2 = "IATA: " + dest["IATA"],"Name: "+dest["Name"],"City: "+dest["City"],"Country: "+dest["Country"]
    lt.addLast(lst_arpts,mensaje1)
    lt.addLast(lst_arpts,mensaje2)
    return lst_arpts


#---------------------Punto4------------------------------
def flightbymiles(analyzer,city,miles):
    distance = miles * 1.6
    grafo = analyzer["grafo"]
    resultado = pr.PrimMST(grafo)
    distancia_max = round(pr.weightMST(grafo,resultado),3)
    lista = resultado["mst"]
    tamaño = lt.size(lista)
    recorrido_dfs = dfs.DepthFirstSearch(grafo,city)
    distancia = 0
    texto = "Rutas a seguir segun la ciudad establecida (se puede presentar en desorden): " + "\n"
    texto_distancia = ""
    for viaje in lt.iterator(lista):
        ciudad1 = viaje["vertexA"]
        ciudad2 = viaje["vertexB"]
        weight = viaje["weight"]
        if dfs.hasPathTo(recorrido_dfs,ciudad1) and dfs.hasPathTo(recorrido_dfs,ciudad2):
            texto1 = "Ciudad 1(IATA): " + str(viaje["vertexA"]) + " ,Ciudad 2(IATA): " + str(viaje["vertexB"]) + " ,Distancia en Km: " + str(viaje["weight"]) + "\n"
            texto += texto1
            distancia += weight
    sobra1 = round((distancia-distance)/1.6,3)
    sobra2 = round((distance-distancia)/1.6,3)
    if distancia > distance:
        texto_distancia = "Si desea hacer el viaje completo, le hacen falta " + str(sobra1) + " millas."
    else:
        texto_distancia = "Puede hacer el viaje completo, por lo que le sobran " + str(sobra2) + " millas."
    distancia = round(distancia,3)
    return distancia_max,texto,distancia,texto_distancia,distance,tamaño

#---------------------Punto5------------------------------
def deleteVertex(analyzer,ver):
    lst_vr = gr.vertices(analyzer["digrafo"])
    lst = lt.newList()
    for vertice in lt.iterator(lst_vr):
        if gr.getEdge(analyzer["digrafo"],ver,vertice) != None and ver != vertice:
    
            actual = mp.get(analyzer["airports"],vertice)
            
            actual = actual["value"]
            lt.addLast(lst,actual)
    digraf = deletdigrafo(analyzer,ver)
    grafo = deletgrafo(analyzer,ver)
    return (lst,digraf,grafo)

def deletdigrafo(analyzer,ver):
    num_ed_ver = (gr.degree(analyzer["digrafo"],ver)) + (gr.indegree(analyzer["digrafo"],ver))
    numvertx = gr.numVertices(analyzer["digrafo"]) - 1
    num_edges = (gr.numEdges(analyzer["digrafo"]))- num_ed_ver
    return(numvertx,num_edges)
def deletgrafo(analyzer,ver):
    num_ed_ver = gr.degree(analyzer["grafo"],ver)
    numvertx = gr.numVertices(analyzer["grafo"]) - 1
    num_edges = (gr.numEdges(analyzer["grafo"]))- num_ed_ver
    return (numvertx,num_edges)
def printlst(analyzer,nombre):
    lst = mp.get(analyzer["cities"],nombre)
    lst = lst["value"]
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
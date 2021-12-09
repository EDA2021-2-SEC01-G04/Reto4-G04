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
 """



import config as cf
import model
import csv
import time as t

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer          
# Funciones para la carga de datos

def loadAirports(analyzer):
    star_time = t.process_time()
    valor = 1
    artistfile = cf.data_dir + "Skylines/airports-utf8-large.csv"
    input_file = csv.DictReader(open(artistfile,encoding="utf-8"),delimiter=",")
    for airport in input_file:
        if airport != None:
            model.addAirport(airport,analyzer)
            #model.addAirport2(airport,analyzer)
            model.hashAirports(analyzer,airport)
            model.hashValues(analyzer,valor,airport)
    end_time = t.process_time()
    laps_time = (end_time - star_time)*1000
    return laps_time
        
def loadRoutes(analyzer):
    star_time = t.process_time()
    artistfile = cf.data_dir + "Skylines/routes-utf8-large.csv"
    input_file = csv.DictReader(open(artistfile,encoding="utf-8"),delimiter=",")
    for route in input_file:
        model.routesByDeparture(analyzer,route)
    model.addRoutesConenctions(analyzer)
    model.addRoutesConenctions2(analyzer)
    end_time = t.process_time()
    laps_time = (end_time - star_time)*1000
    return laps_time

def loadCities(analyzer):
    star_time = t.process_time()
    valor = 0
    artistfile = cf.data_dir + "Skylines/worldcities-utf8.csv"
    input_file = csv.DictReader(open(artistfile,encoding="utf-8"),delimiter=",")
    for airport in input_file:
        if airport != None:
            model.hashcities(analyzer,airport)
            model.counterCities(analyzer)
            model.hashValues(analyzer,valor,airport)
    end_time = t.process_time()
    laps_time = (end_time - star_time)*1000
    return laps_time

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def totalVertex(analyzer):
    num = int(model.totalVertex(analyzer))
    return num
def totalEdge(analyzer):
    num =  model.totalEdge(analyzer)
    return num
def totalVertexgrafo(analyzer):
    return model.totalVertexgrafo(analyzer)
    
def totalEdgegrafo(analyzer):
    return model.totalEdgegrafo(analyzer)

def totalCities(analyzer):
    return model.totalCities(analyzer)

def hashinformationcities(analyzer):
    return model.returnhashcities(analyzer)
    
def hashinformationairports(analyzer):
    return model.returnhashairports(analyzer)
#---------Punto1----------
def puntointerconexion(analyzer):
    airports = model.puntointerconexion(analyzer)
    info = model.infoAirports(airports,analyzer)
    return info
#---------Punto2----------
def conectins(analyzer,air1,air2):
    a= model.connected(analyzer)
    b = model.hasroute(analyzer,air1,air2)
    c = model.getinfo(analyzer,air1,air2)
    return (a,b,c)
#----------Punto3---------
def airportsInArea(analyzer,city,city2):
    air1 = model.airportsInArea(analyzer,city)
    air2 = model.airportsInArea(analyzer,city2)
    info = model.getinforeq3(analyzer,air1,air2)
    path = model.getminimunpath(analyzer,air1,air2)
    return (path,info)

#--------Punto3-------------
def cities(analyzer,city1,city2):
    return model.cities(analyzer,city1,city2)

#--------Punto4-------------
def flightbymiles(analyzer,city,miles):
    return model.flightbymiles(analyzer,city,miles)

#--------Punto5------------
def deleteairport(analyzer,airport):
    return model.deleteVertex(analyzer,airport)


def printlst(analyzer,nombre):
    return model.printlst(analyzer,nombre)

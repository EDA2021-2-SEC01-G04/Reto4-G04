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
    artistfile = cf.data_dir + "Skylines/airports_full.csv"
    input_file = csv.DictReader(open(artistfile,encoding="utf-8"),delimiter=",")
    for airport in input_file:
        if airport != None:
            model.addAirport(airport,analyzer)
            model.hashAirports(analyzer,airport)
        
def loadRoutes(analyzer):
    artistfile = cf.data_dir + "Skylines/routes_full.csv"
    input_file = csv.DictReader(open(artistfile,encoding="utf-8"),delimiter=",")
    for route in input_file:
        model.routesByDeparture(analyzer,route)
    model.addRoutesConenctions(analyzer)

def loadCities(analyzer):
    artistfile = cf.data_dir + "Skylines/worldcities_full.csv"
    input_file = csv.DictReader(open(artistfile,encoding="utf-8"),delimiter=",")
    for airport in input_file:
        if airport != None:
            model.hashAirports(analyzer,airport)
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def totalVertex(analyzer):
    num = int(model.totalVertex(analyzer))
    return num
def totalEdge(analyzer):
    num =  model.totalEdge(analyzer)
    return num
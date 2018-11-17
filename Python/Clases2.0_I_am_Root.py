import csv
from tkinter import filedialog
from tkinter import *
import json
from json import JSONEncoder
import random

class JsonObj():
    def __init__(self, lugaresJson):
        self.lugaresJson = lugaresJson

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

class Temperatura():
    def __init__(self, maxx=None, minn = None, evaporacion = None): 
        self.maxx = None
        self.minn = None
        self.evaporacion = None

class Meteo():
    def __init__(self, precipitacion=None, nubes = None, nieve = None): 
        self.precipitacion = None
        self.nubes = None
        self.nieve = None    
    
class Fecha ():
    def __init__(self,dia=None,mes = None, numDia = None): 
        self.dia = dia
        self.mes = mes
        self.numDia = numDia
        self.temp = Temperatura()
        self.meteo = Meteo()
        
class Lugar (JSONEncoder):  
    def __init__(self,nombre = None,latitud=None, longitud = None):
        self.nombre = None
        self.lat = None
        self.long = None
        self.fecha = [Fecha()]

lugares = [Lugar()]
lugares.clear()

def Lectura(path):

    esTemp = False
    if "temperatura" in path:
        esTemp = True
        print("Temperatura")
    
    elif "precipitacion" in path:
        print("Lluvia")
    else:
        print("ERROR DE ARCHIVO")
        Lectura(str(filedialog.askopenfilename(title = "ERROR: Archivo no compatible")))
        return

    with open( path , "r" ) as f :
        reader = csv.reader(f)
        for row in reader:
            newLugar = Lugar()
            newLugar.nombre = row[0]

            existeLugar = False
            lugarExistente = 0
            for i in range(len(lugares)):
                if lugares[i].nombre == newLugar.nombre:
                    existeLugar = True
                    lugarExistente = i

            newFecha = Fecha()
            newFecha.dia = row[1]
            newFecha.mes = row[2]

            if esTemp:
                newFecha.temp.minn = row[3]
                newFecha.temp.maxx = row[4]
            else:
                newFecha.meteo.precipitacion = row[3]

            if existeLugar:              
                fechaExiste = False
                for fechaExistente in lugares[lugarExistente].fecha:
                    if fechaExistente.mes == newFecha.mes and fechaExistente.dia == newFecha.dia:
                        fechaExiste = True
                        if esTemp:
                            fechaExistente.temp.maxx = newFecha.temp.maxx
                            fechaExistente.temp.minn = newFecha.temp.minn
                        else:
                            fechaExistente.meteo.precipitacion = newFecha.meteo.precipitacion

                if not fechaExiste:        
                    lugares[lugarExistente].fecha.append(newFecha)

            else:
                newLugar.fecha.clear()
                newLugar.fecha.append(newFecha)
                lugares.append(newLugar)

def Write():
    jsonoutput = JsonObj(lugares)
    outputlocation = filedialog.asksaveasfile(title = "Elija la direccion donde guardar", defaultextension = ".json").name
    with open(outputlocation, "w") as outputtext:
        outputtext.write(jsonoutput.toJSON())  
    
def Calcular():
    for lugar in lugares:
        for fecha in lugar.fecha:
            newEva = ((int(fecha.temp.maxx) + int(fecha.temp.minn))/2)/24 #mm/dia
            fecha.temp.evaporacion = newEva

            if int(fecha.temp.maxx) < 0 and int(fecha.meteo.precipitacion) > 0:
                fecha.meteo.nieve = True
            else:
                fecha.meteo.nieve = False

            if int(fecha.temp.maxx) < 20:
                fecha.meteo.nubes =  random.randint(25, 100)
            else:
                fecha.meteo.nubes = 0

root = Tk()
root.withdraw()
Lectura(str(filedialog.askopenfilename(title = "Seleccione archivo de Temperaturas")))
Lectura(str(filedialog.askopenfilename(title = "Seleccione archivo de Precipitacion")))

Calcular()

Write()

print("Fechas: ", len(lugares[0].fecha))

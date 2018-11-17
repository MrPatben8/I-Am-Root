import csv
from tkinter import filedialog
from tkinter import *
import json
from json import JSONEncoder

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
            
            if existeLugar:
                newFecha.numDia = len(lugares[lugarExistente].fecha)
                if esTemp:
                    lugares[lugarExistente].fecha[newFecha.numDia-1].temp.minn = row[3]
                    lugares[lugarExistente].fecha[newFecha.numDia-1].temp.maxx = row[4]
                else:
                    lugares[lugarExistente].fecha[newFecha.numDia-1].meteo.precipitacion = row[3]

                lugares[lugarExistente].fecha.append(newFecha)
                
            else:
                newLugar.fecha.append(newFecha)
                newLugar.fecha[0].numDia = 0
                if esTemp:
                    newLugar.fecha[0].temp.minn = row[3]
                    newLugar.fecha[0].temp.maxx = row[4]
                else:
                    newLugar.fecha[0].meteo.precipitacion = row[3]
                lugares.append(newLugar)

def Write():
    jsonoutput = JsonObj(lugares)
    outputlocation = filedialog.asksaveasfile(title = "Elija la direccion donde guardar", defaultextension = ".json").name
    with open(outputlocation, "w") as outputtext:
        outputtext.write(jsonoutput.toJSON())  
    
root = Tk()
root.withdraw()
Lectura(str(filedialog.askopenfilename(title = "Seleccione archivo de Temperaturas")))
Lectura(str(filedialog.askopenfilename(title = "Seleccione archivo de Precipitacion")))

#print(lugares[0].fecha[0].temp.maxx)
#print(lugares[0].fecha[0].meteo.precipitacion)

Write()

print("Lugares: ", len(lugares[5].fecha))
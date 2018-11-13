import csv
from tkinter import filedialog
from tkinter import *

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
        self.temp = [Temperatura()]
        self.meteo = [Meteo()]
        
class Lugar ():  
    def __init__(self,nombre = None,latitud=None, longitud = None):
        self.nombre = None
        self.lat = None
        self.long = None
        self.fecha = [Fecha()]
        

lugares = [Lugar()]
lugares.clear()

def Lectura(path):
    if "temperatura" in path:
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
            lugarExistente = 0

            existeLugar = False
            lugarExistente = -1
            for lugar in lugares:
                if lugar.nombre == newLugar.nombre:
                    existeLugar = True
            lugarExistente =+ 1

            print(lugarExistente)
            newFecha = Fecha()
            newFecha.mes = row[1]
            newFecha.dia = row[2]

            caca = 0
            if existeLugar:
                for fecha in lugares[lugarExistente].fecha:
                    if fecha == newFecha:
                        caca =+ 1
                        #existeFecha = True
                    else:
                        lugares[lugarExistente].fecha.append(newFecha)
            else:
                newLugar.fecha.append(newFecha)
                lugares.append(newLugar)


root = Tk()
root.withdraw()
Lectura(str(filedialog.askopenfilename(title = "Seleccione archivo de Temperaturas")))
#Lectura(str(filedialog.askopenfilename(title = "Seleccione archivo de Precipitacion")))

print(len(lugares[5].fecha))
print(lugares[5].fecha[1].dia)

'''
def Test():
    for lugar in lugares:
        if lugar.nombre != None:
            print(lugar.nombre)

Test()
'''
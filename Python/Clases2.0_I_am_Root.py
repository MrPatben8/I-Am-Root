import csv
from tkinter import filedialog
from tkinter import *
import json

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
        
class Lugar ():  
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
            #for lugar in lugares:
                if lugares[i].nombre == newLugar.nombre:
                    existeLugar = True
                    lugarExistente = i

            newFecha = Fecha()
            newFecha.mes = row[1]    #REVISAR SI DIA Y MES ESTAN EN ORDEN CORRECTA
            newFecha.dia = row[2]

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
    '''
    name = ["Scott","Larry", "Tim"]
    website = ["google.com","wikipedia.com","twitter.com"]
    ffrom = ["Chile", "China", "USA"]
    
    data = {}  
    data['lugares'] = []  
    fechasjson = {}
    fechasjson['fecha'] = []

    for t in range(len[lugares]):
        data['lugares'].append({  
            'lugar': lugares[t].nombre,
            'lat':lugares[t].lat,
            'long':lugares[t].long
            fechasjson['fecha'].append()
        })



    with open('Desktop/data.txt', 'w') as outfile:  
        json.dump(data, outfile)'''
 

root = Tk()
root.withdraw()
Lectura(str(filedialog.askopenfilename(title = "Seleccione archivo de Temperaturas")))
#Lectura(str(filedialog.askopenfilename(title = "Seleccione archivo de Precipitacion")))

print(len(lugares[5].fecha))
print(lugares[5].fecha[1].dia)
print(lugares[5].fecha[2].dia)

Write()

'''
def Test():
    for lugar in lugares:
        if lugar.nombre != None:
            print(lugar.nombre)

Test()
'''
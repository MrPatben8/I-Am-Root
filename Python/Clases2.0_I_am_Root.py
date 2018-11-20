import csv
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import json
from json import JSONEncoder
import random
from opencage.geocoder import OpenCageGeocode

class JsonObj():
    def __init__(self, lugaresJson, duracionDia = None, velocidadEvaporacion = None, velocidadAgua = None, velocidadCrecimiento = None, velocidadMuerte = None):
        self.lugaresJson = lugaresJson
        self.duracionDia = 1.2
        self.velocidadEvaporacion = 10
        self.velocidadAgua = 0.01
        self.velocidadCrecimiento = 0.075
        self.velocidadMuerte = 1

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
            newFecha.numDia = 0
            if esTemp:
                newFecha.temp.minn = row[3]
                newFecha.temp.maxx = row[4]
            else:
                newFecha.meteo.precipitacion = row[3]

            if existeLugar:
                newFecha.numDia = len(lugares[lugarExistente].fecha)             
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
    Aplicacion.UpdateLog("Listo!")

def Write():
    Aplicacion.UpdateLog("Guardando...")
    jsonoutput = JsonObj(lugares)
    CalcularDificultad()
    outputlocation = filedialog.asksaveasfile(title = "Elija la direccion donde guardar", defaultextension = ".json").name
    with open(outputlocation, "w") as outputtext:
        outputtext.write(jsonoutput.toJSON())  
    Aplicacion.UpdateLog("Listo! FIN DE COMPILACION")
    print("Listo! FIN DE COMPILACION")
    
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
    Aplicacion.UpdateLog("Listo!")

def GetPos():
    key = '51df2f36d3fc4952a3d460f8fa3a1993'
    geocoder = OpenCageGeocode(key)
    for lugar in lugares:
        print("Obteniendo posicion...")
        Aplicacion.UpdateLog("Obteniendo posicion...")
        query = lugar.nombre + ", Chile"
        ret = geocoder.geocode(query)
        lugar.lat = ret[0]['geometry']['lat']
        lugar.long = ret[0]['geometry']['lng']
        print("Encontrado: ", lugar.nombre)
        Aplicacion.UpdateLog("Encontrado: " + lugar.nombre)

def CalcularDificultad():
    print("Calculando Dificultad...")
    jsonoutput.duracionDia = 1.2
    jsonoutput.velocidadAgua = 10
    jsonoutput.velocidadCrecimiento = 0.01
    jsonoutput.velocidadEvaporacion = 0.075
    jsonoutput.velocidadMuerte = 1

raiz = Tk()
raiz.geometry('300x300')
raiz.resizable(width=False,height=False)
raiz.title('I am Root compiler')
tinfo = Text(raiz, width=40, height=10)
tinfo.pack(side=TOP)
class Aplicacion(): 
    def __init__(self):
        #self.tinfo = Text(raiz, width=40, height=10)
        #self.tinfo.pack(side=TOP)
        self.boton = ttk.Button(raiz, text='Cargar Temperatura', command=self.algo) #Boton extra no hace nada
        self.boton.pack(side=LEFT)
        self.binfo = ttk.Button(raiz, text='Cargar Precipitacion', command=self.verinfo)
        self.binfo.pack(side=RIGHT)
        self.bsalir = ttk.Button(raiz, text='Salir', command=raiz.destroy)
        self.bsalir.pack(side=BOTTOM)
        self.b1ton = ttk.Button(raiz, text= 'Compilar', command= self.hola)
        self.b1ton.pack(side=BOTTOM)
        self.binfo.focus_set()
        raiz.mainloop()     

    def hola(self):
        Aplicacion.UpdateLog("Calculando Valores...")
        Calcular()
        GetPos()
        Write()

    def algo(self):
        Aplicacion.UpdateLog("Cargando Temperaturas...")
        Lectura(str(filedialog.askopenfilename(title = "Seleccione archivo de Temperaturas")))
    
    def btnClick(self):
        pass

    def verinfo(self):
        Aplicacion.UpdateLog("Cargando Precipitacion...")
        Lectura(str(filedialog.askopenfilename(title = "Seleccione archivo de Precipitacion")))

    def UpdateLog(texto):
        tinfo.insert(INSERT, texto+"\n")

def main():
    mi_app = Aplicacion()
    return 0

root = Tk()
root.withdraw()

jsonoutput = JsonObj(lugares)
main()
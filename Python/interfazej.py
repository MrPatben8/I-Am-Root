from tkinter import *
from tkinter import ttk
import csv
from tkinter import filedialog

class Aplicacion(): 

    def __init__(self):
        self.raiz = Tk()
        self.raiz.geometry('300x300')
        self.raiz.resizable(width=False,height=False)
        self.raiz.title('I am Root compiler')
        self.tinfo = Text(self.raiz, width=40, height=10)
        self.tinfo.pack(side=TOP)
        self.boton = ttk.Button(self.raiz, text='Cargar Temperatura', command=self.algo) #Boton extra no hace nada
        self.boton.pack(side=LEFT)
        self.binfo = ttk.Button(self.raiz, text='Cargar Precipitacion', command=self.verinfo)
        self.binfo.pack(side=RIGHT)
        self.bsalir = ttk.Button(self.raiz, text='Salir', command=self.raiz.destroy)
        self.bsalir.pack(side=BOTTOM)
        self.b1ton = ttk.Button(self.raiz, text= 'Compilar', command= self.hola)
        self.b1ton.pack(side=BOTTOM)
        self.binfo.focus_set()
        self.raiz.mainloop()     

    def hola(self):
        self.tinfo.delete("1.0",END)
        com = "Compilaste men"
        self.tinfo.insert("1.0", com)

    def algo(self):
        self.filename = filedialog.askopenfilename(title="Select file", filetypes= ("csv files","*.csv"))
        f = open(self.filename,"rb")
        read = csv.reader(f, delimiter= ",")
        buttons = read.next()
        print
        for btn in buttons:
            new_btn = Button(self, text=btn, command=self.btnClick)
            new_btn.pack()
    
    def btnClick(self):
        pass

    def verinfo(self):
        self.tinfo.delete("1.0",END)
        info1 = self.raiz.winfo_class()
        info2 = self.raiz.winfo_geometry()
        info3 = str(self.raiz.winfo_width())
        info4 = str(self.raiz.winfo_height())
        info5 = str(self.raiz.winfo_rootx())
        info6 = str(self.raiz.winfo_rooty())
        info7 = str(self.raiz.winfo_id())
        info8 = self.raiz.winfo_name()
        info9 = self.raiz.winfo_manager()

        texto_info = "Clase de 'raiz': " + info1 + "\n"
        texto_info += "Resolución y posición: " + info2 + "\n"
        texto_info += "Anchura ventana: " + info3 + "\n"
        texto_info += "Altura ventana: " + info4 + "\n"
        texto_info += "Pos. Ventana X: " + info5 + "\n"
        texto_info += "Pos. Ventana Y: " + info6 + "\n"
        texto_info += "Id. de 'raiz': " + info7 + "\n"
        texto_info += "Nombre objeto: " + info8 + "\n" 
        texto_info += "Gestor ventanas: " + info9 + "\n"

        self.tinfo.insert("1.0", texto_info)

def main():
    mi_app = Aplicacion()
    return 0 

if __name__ == '__main__':
    main()
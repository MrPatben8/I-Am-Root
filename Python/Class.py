class Lugar ():  

    Nombre = "Nombre"
    Latitud = 123
    Longitud = 133

class Fecha (Lugar):
    Dia = 0
    Mes = 0
    arr = [Fecha.Dia, Fecha.Mes]

A = Fecha()

A.Nombre = "D"
A.Dia = 1
A.Mes = 3
print(A.arr)





from tkinter import *
from cuadMedios import CuadradosMedios
from pruebaSeries import PruebaDeSeries
from corridasArriAbj import CorridasArribaAbajo
from rentaCoches import Renta

class Principal:
    def __init__(self):
        root=Tk()
        root.geometry("500x300")
        root.title("MENÚ")
        root.config(bg="gray")
        root.resizable(width=False,height=False)
        
        Label(root,text="Generación de números\naleatorios y pseudoaleatorios",font=12,bg="gray",foreground="white").place(x=20,y=50)
        Label(root,text="Pruebas estadísticas de\naleatoriedad",font=12,bg="gray",foreground="white").place(x=300,y=50)
        
        def cuadMedios():
            eo=CuadradosMedios()
            eo.generar(root)
        
        def pSeries():
            eo=PruebaDeSeries()
            eo.prueba(root)
        
        def corridasAA():
            eo=CorridasArribaAbajo()
            eo.prueba(root)
        
        def rentaCoches():
            eo=Renta()
            eo.simular(root)
            
        def salir():
            root.destroy()
        
        Button(root,text="Cuadrados Medios",font=12,command=lambda:cuadMedios()).place(x=60,y=100)
        Button(root,text="Prueba de Series",font=12,command=lambda:pSeries()).place(x=330,y=100)
        Button(root,text="Corridas arriba y abajo",font=12,command=lambda:corridasAA()).place(x=310,y=150)
        Button(root,text="Renta de coches",font=12,command=lambda:rentaCoches()).place(x=200,y=190)
        Button(root,text="Salir",command=lambda:salir(),font=12).place(x=60,y=200)
        
        
        root.mainloop()
        
        
Principal()
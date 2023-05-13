import threading
import time
from faker import Faker
import random
from random import uniform
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
from PIL import ImageTK,Image

class GymCode(threading.Thread):
    def __init__(self,sim):        
        root=Tk()
        root.title("Proyecto de Simulación")
        root.geometry("1280x720")
        root.config(bg="#000000")
        global fake
        fake=Faker()
        
        def ventaProduct():
            pass
        
        
        for dia in range(1,sim+1): #Ciclo que simula toda la cantidad  de días     
            CantPerDiaRangoIn=[0,0.101,0.2501,0.6501,0.9501]
            CantPerDiaRangoFin=[0.1,0.25,0.65,0.95,1]
            CantPersonasDia=[15,25,35,45,50]
            
            PersonasDelDia=random.uniform(0,1)
            for cantP in range(len(CantPersonasDia)): #Ciclo que verifica y asignará la cantidad de personas del día
                if PersonasDelDia>=CantPerDiaRangoIn[cantP] and PersonasDelDia<=CantPerDiaRangoFin[cantP]:
                    personasDia = CantPersonasDia[cantP] 
            print(f"Dia {dia} cantidad de personas {personasDia}")

            
            clientes=0
            usuarios=0
            for indiv in range(personasDia):    #Recorre la cantidad de personas que llegarán al gym
                persona=random.uniform(0,1)     
                if persona>=0 and persona<=0.2:  #Asignará si la persona es un cliente o usuario de acuerdo a la prob.
                    persona="Cliente"
                    clientes+=1
                elif persona>=0.201 and persona<=1:
                    persona="Usuario"
                    usuarios+=1


            print(f"Clientes {clientes}")
            print(f"Usuarios {usuarios}")
            
            def F_cliente():
                for cl in range(clientes):
                    pass
            
            
            '''
            ACOMODAR CON HILOS PARA REALIZAR LAS LLEGADAS DE USUARIOS 
            Y DE LOS CIENTES SEGUN LA CANTIDAD CON UN FOR EN CADA UNO
            PARA SIMULAR LLEGADAS REALISTAS
            
            - Simular que se acabe la suscripción de los usuarios
            '''
            
            def F_usuario():
                probSuscpLimIn=[0,0.3,0.35,0.75,0.9]
                probSuscpLimFin=[0.3,0.35,0.75,0.9,1]
                suscripciones=["Visita","Semana","Mensualidad",	"Trimestre","Anualidad"]
                
                for subsc in range(1,usuarios+1):
                    aleatipoSub=random.uniform(0,1)
                    for sub in range(len(probSuscpLimIn)):
                        if aleatipoSub>=probSuscpLimIn[sub] and aleatipoSub<=probSuscpLimFin[sub]:
                            tipoSub=suscripciones[sub]
                            break
                    
                    
                    nameUser=fake.name()
                    print(f"Usuario {subsc} con nombre {nameUser} y suscripción: {tipoSub}")
                            
            
            if persona=="Cliente":
                F_cliente()
            elif persona=="Usuario":
                F_usuario()
            
        
            
            
                
        #root.mainloop()    
            
try:
    sim=int(input("Cantidad de simulaciones: "))
except ValueError as err:
    messagebox.showinfo("ERROR",f"Error valor para simulaciones no admitido\n{err}")

else:
    GymCode(sim)
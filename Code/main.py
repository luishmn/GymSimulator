import threading
import time
from faker import Faker
import random
from random import uniform
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
from PIL import ImageTk,Image

from simulacion import Simulacion
from tablas import Tablas

class GymCode(threading.Thread):
    def __init__(self):        
        root=Tk()
        main_resolution="1280x680+50+50"
        root.title("Proyecto de Simulación")
        root.geometry(main_resolution)
        root.resizable(width=False,height=False)
        root.config(bg="#000000")
        root.overrideredirect(False)
  
        
        main_imagen=PhotoImage(file="Imagenes/MainIMG/fondo.png")
        cerrarImg=PhotoImage(file="Imagenes/MainIMG/cerrar.png")
        bt1Img=PhotoImage(file="Imagenes/MainIMG/btn1.png")
        bt2Img=PhotoImage(file="Imagenes/MainIMG/btn2.png")
        bt3Img=PhotoImage(file="Imagenes/MainIMG/btn3.png")
        
        
        Lbl_img_main=Label(root,image=main_imagen).pack()
        
        def open_Simulation():
            eo=Simulacion(root)#,)
            
        def open_Tables():
            eo=Tablas(root)#,)
        
        def cerrar():
            root.destroy()
        
        #Se pueden multiplicar los tiempos por 60 para que se abarquen los minutos de forma real
        Button(root,image=bt1Img,command=lambda:open_Simulation()).place(x=389,y=243)#,width=503,height=67)
        Button(root,image=bt2Img,command=lambda:open_Simulation()).place(x=389,y=337)#,width=503,height=67)
        Button(root,image=bt3Img,command=lambda:open_Tables()).place(x=389,y=431)#,width=503,height=67)
        Button(root,image=cerrarImg,command=lambda:cerrar()).place(x=1185,y=16,width=73,height=73)
                        
        root.mainloop()

GymCode()
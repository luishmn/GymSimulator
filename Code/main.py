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

class GymCode(threading.Thread):
    def __init__(self,sim):        
        root=Tk()
        main_resolution="1280x680+50+50"
        root.title("Proyecto de Simulación")
        root.geometry(main_resolution)
        root.resizable(width=False,height=False)
        root.config(bg="#000000")
        root.overrideredirect(False)
        
        global fake
        fake=Faker()
        
        main_imagen=PhotoImage(file="Imagenes/Intro.png")
        Lblimg_main=Label(root,image=main_imagen).pack()
        
        
                
        root.mainloop()    
            
try:
    sim=int(input("Cantidad de simulaciones: "))
except ValueError as err:
    messagebox.showinfo("ERROR",f"Error valor para simulaciones no admitido\n{err}")

else:
    GymCode(sim)
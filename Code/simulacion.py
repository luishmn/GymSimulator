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


class Simulacion():
    def __init__(self,root):
        self.root=root  
        self.root.iconify()
        ventana=Toplevel(self.root)
        ventana.title("SIMULACIÓN")
        ventana.overrideredirect(False)
        ventana.geometry("1280x720+50+50")
        ventana.resizable(width=False,height=False)
        


        def cerrar():
            ventana.destroy()
            self.root.deiconify()
        
        Button(ventana,text="Adios",command=ventana.destroy()).pack()
        
        ventana.mainloop()
    
   
   
   
   
   
   
    
    def sart_simulacion():
        pass
        
        
        

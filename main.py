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
from tablas import AbrirVentanaTablas

class GymCode(threading.Thread):
    def __init__(self):        
        root=Tk()
        main_resolution="1280x720+35-30"
        root.title("Proyecto de Simulación")
        root.geometry(main_resolution)
        root.resizable(width=False,height=False)
        root.config(bg="#000000")
        root.overrideredirect(False)
  
        ic = ImageTk.PhotoImage(Image.open("./Imagenes/home.ico"))
        root.iconphoto(True,ic)
        root.wm_iconbitmap("./Imagenes/home.ico")
  
        main_imagen=PhotoImage(file="Imagenes/MainIMG/fondo.png")
        cerrarImg=PhotoImage(file="Imagenes/MainIMG/cerrar.png")
        bt1Img=PhotoImage(file="Imagenes/MainIMG/btn1.png")
        bt2Img=PhotoImage(file="Imagenes/MainIMG/btn2.png")
        bt3Img=PhotoImage(file="Imagenes/MainIMG/btn3.png")
        
        Lbl_img_main=Label(root,image=main_imagen).pack()
        
        def open_Simulation(velocidad):
            Simulacion(velocidad,root)
            
        def open_Tables():
            AbrirVentanaTablas(root)

        def Fbtn1_raise(event):
            btn1.place(y=240)
        def Fbtn2_raise(event):
            btn2.place(y=334)
        def Fbtn3_raise(event):
            btn3.place(y=428)
        def FbtnC_raise(event):
            btnC.place(y=13)
        
        def Fbtn1_lower(event):
            btn1.place(y=243)
        def Fbtn2_lower(event):
            btn2.place(y=337)
        def Fbtn3_lower(event):
            btn3.place(y=431)
        def FbtnC_lower(event):
            btnC.place(y=16)
        
        def cerrar():
            root.destroy()
        
        
        btn1=Button(root,image=bt1Img,command=lambda:open_Simulation("Fast"),bd=0,highlightthickness=0)
        btn1.place(x=389,y=243)#,width=503,height=67)
        btn2=Button(root,image=bt2Img,command=lambda:open_Simulation("RealTime"),bd=0,highlightthickness=0)
        btn2.place(x=389,y=337)#,width=503,height=67)
        btn3=Button(root,image=bt3Img,command=lambda:open_Tables(),bd=0,highlightthickness=0)
        btn3.place(x=389,y=431)#,width=503,height=67)
        btnC=Button(root,image=cerrarImg,command=lambda:cerrar(),bd=0)
        btnC.place(x=1185,y=16,width=53,height=51)
        
        btn1.bind("<Enter>",Fbtn1_raise)
        btn2.bind("<Enter>",Fbtn2_raise)
        btn3.bind("<Enter>",Fbtn3_raise)
        btnC.bind("<Enter>",FbtnC_raise)
        
        btn1.bind("<Leave>",Fbtn1_lower)
        btn2.bind("<Leave>",Fbtn2_lower)
        btn3.bind("<Leave>",Fbtn3_lower)
        btnC.bind("<Leave>",FbtnC_lower)
                                
        root.mainloop()

GymCode()

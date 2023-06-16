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
from datetime import datetime, timedelta
import matplotlib.pyplot as plt




class SimulacionProceso():
    def __init__(self,velocidad,root):
        root.iconify()
        global ventana
        ventana=Toplevel(root)
        ventana.title("SIMULACIÓN")
        ventana.geometry("1280x720+35-30")
        ventana.resizable(width=False,height=False)
        
        ic = ImageTk.PhotoImage(Image.open("./Imagenes/simulation.ico"))
        ventana.iconphoto(True,ic)
        ventana.wm_iconbitmap("./Imagenes/simulation.ico")
        
        '''*********************** DATOS GUARDADOS PARA RESULTADOS ***********************'''
        
        cajaNombre = [] #Este dato no nos iteresa
        self.dineroCaja = 0         #Dinero en la caja
        
        with open("./Datos/37Caja.txt", 'r') as f:
            for linea in f:
                elementos = linea.strip().split(',')
                if len(elementos) == 2:
                    nombre = elementos[0].strip()
                    dinero = elementos[1].strip()
                    cajaNombre.append(nombre)
                    try:
                        self.dineroCaja=int(dinero)
                    except ValueError:
                        self.dineroCaja = 0
        f.close()
                    
        #print(self.dineroCaja)
        
        #self.dineroCaja = 0         #Dinero en la caja
        self.cantPersSim=[] #Cantidad de pesonas de cada dia
        
        self.clientesTotales=0 #Clientes totales que fueron 
        self.usuariosTotales=0 #Usuarios totales que fueron
        
        
        self.subDia=0       #Suscripciones de visita
        self.subSemana=0    #Suscripciones de semsna
        self.subMes=0       #Suscripciones de mes
        self.subTrim=0      #Suscripciones de trimestre
        self.subAnua=0      #Suscripciones de anualidad
        
        self.personasEntrenaronCardio=0     #Personas que entrenaron cardio
        self.personasEntrenaronEspalda=0    #Personas que entrenaron espalda
        self.personasEntrenaronPecho=0      #Personas que entrenaron pecho
        self.personasEntrenaronPierna=0     #Personas que entrenaron pierna
        self.personasEntrenaronPesas=0      #Personas que entrenaron pesas
        self.personasEntrenaronSpinning=0   #Personas que entrenaron spinning
        
        self.personasHacenCardio=0          #Personas que si hicieron cardio antes de entrenar
        self.personasNoHacenCardio=0        #Personas que no hicieron cardio antes de entrenar
        
        self.personasRequierHosp=0          #Lesionados que requirieron hospitalizacion
        self.personasNoRequierHosp=0        #Lesionados que no requirieron hospitalizacion
        
        self.lesionadosCadaDia=[]           #Lista de lesionados de cada dia
        self.tiemposPersonasSim=[]          #Lista de tiempos prom que tardaban las personas en el gym cada día
        self.maquinasAveriadasSim=[]        #Lista de maquinas averiadas cada día de simulacion
        self.gananciaDiaSim=[]              #Lista de ganancias de cada día de simulacion
        
        self.lesionadosCadaDia.append(0)         
        self.tiemposPersonasSim.append(0)
        self.maquinasAveriadasSim.append(0)    
        self.gananciaDiaSim.append(0)
        
        self.gastosTotalesSim=0
        self.gananciasTotalesSim=0
        
        self.listaDias=None                 #Lista de los días de simulacion
        '''*************************************************************'''
        
        
        global listaAleatorios
        listaAleatorios=[]
        
        archivo=open("Aleatorios/aleatorios.txt","r")
        lines=archivo.readlines()
        for line in lines:
            listaAleatorios.append(float(line))
            
            
        ##print("LISTA DE ALEATORIOS")
        ##print(listaAleatorios)
        ##print("\n")
        
        self.ventana=ventana
        self.dia=0
        self.velocidad=velocidad
        self.posAleatorio=0

        self.start_time = datetime.strptime("08:00:00 AM", "%I:%M:%S %p")
        self.current_time = self.start_time
        self.speed_factor = 1
        self.process_running = False
        
        
        ImagenBASE=Label(ventana,image=mainIMG).pack()
        self.img_ambulancia=Label(ventana,image=ambuIMG1,bg="#1D1F24",bd=0).place(x=912,y=22)
        img_resultados=Label(ventana,image=resuIMG1,bd=0,bg="#1D1F24",highlightthickness=0).place(x=1026,y=22)
        
        
        self.lblDia=Label(ventana,text=(f"DÍA {self.dia}"),font=("Helvetica", 24),bg="#1D1F24",bd=0,foreground="white")
        self.lblDia.place(x=711,y=35)
        
        self.reloj = Label(ventana,font=("Helvetica", 24),bg="#1D1F24",bd=0,foreground="white")
        #self.reloj.place(x=200,y=200)
        self.reloj.place(x=48,y=31)
        
        
        def cerrar():
            ventana.destroy()
            root.deiconify()
        
        def Fbtn1_raise(event):
            btnStart.place(y=11)
        def Fbtn2_raise(event):
            btnCerrar.place(y=19)
        def Fbtn1_lower(event):
            btnStart.place(y=14)
        def Fbtn2_lower(event):
            btnCerrar.place(y=22)
        
        
        
        self.diasSimular=IntVar()
        self.diasSimular.set("")
        
        entrada=Entry(ventana,textvariable=self.diasSimular,font=(12),bd=0)
        entrada.place(x=375,y=40)
        entrada.bind("<Return>", lambda event: self.inicia(velocidad))
        
        Label(ventana,text="Días para simular",font=(12),bg="#1D1F24",foreground="white").place(x=395,y=75)
        
        
        self.btnResultados=Button(ventana,image=resuIMG2,bd=0,bg="#1D1F24",highlightthickness=0)#.place(x=1026,y=22)
        
        btnStart=Button(ventana,image=startIMG1,command=lambda:self.inicia(velocidad),bd=0,bg="#1D1F24")
        btnStart.place(x=607,y=14)
        
        btnCerrar=Button(ventana,image=cerrarIMG,command=lambda:cerrar(),bd=0,highlightthickness=0)
        btnCerrar.place(x=1189,y=22)
        
        btnStart.bind("<Enter>",Fbtn1_raise)
        btnCerrar.bind("<Enter>",Fbtn2_raise)
        btnStart.bind("<Leave>",Fbtn1_lower)
        btnCerrar.bind("<Leave>",Fbtn2_lower)
        
        '''ETIQUETAS DE LAS MAQUINAS DEL GYM'''
        
        #ETIQUETA DE LA TIENDA DE SUPLEMENTOS
        
        self.tiendaSuples=Label(ventana,image=suples1,bg="#D9D9D9",highlightthickness=0).place(x=1050,y=128)
        
        #Casilleros
        self.casillero1=Label(ventana,image=img_casillero1,bg="#D9D9D9",highlightthickness=0).place(x=282,y=122)
        self.casillero2=Label(ventana,image=img_casillero1,bg="#D9D9D9",highlightthickness=0).place(x=302,y=122)
        self.casillero3=Label(ventana,image=img_casillero1,bg="#D9D9D9",highlightthickness=0).place(x=321,y=122)
        self.casillero4=Label(ventana,image=img_casillero1,bg="#D9D9D9",highlightthickness=0).place(x=340,y=122)
        self.casillero5=Label(ventana,image=img_casillero1,bg="#D9D9D9",highlightthickness=0).place(x=359,y=122)
        self.casillero6=Label(ventana,image=img_casillero1,bg="#D9D9D9",highlightthickness=0).place(x=378,y=122)
        self.casillero7=Label(ventana,image=img_casillero1,bg="#D9D9D9",highlightthickness=0).place(x=397,y=122)
        self.casillero8=Label(ventana,image=img_casillero1,bg="#D9D9D9",highlightthickness=0).place(x=416,y=122)
        self.casillero9=Label(ventana,image=img_casillero1,bg="#D9D9D9",highlightthickness=0).place(x=435,y=122)
        self.casillero10=Label(ventana,image=img_casillero1,bg="#D9D9D9",highlightthickness=0).place(x=454,y=122)
        self.casillero11=Label(ventana,image=img_casillero1,bg="#D9D9D9",highlightthickness=0).place(x=473,y=122)
        self.casillero12=Label(ventana,image=img_casillero1,bg="#D9D9D9",highlightthickness=0).place(x=492,y=122)
        self.casillero13=Label(ventana,image=img_casillero1,bg="#D9D9D9",highlightthickness=0).place(x=510,y=122)
        self.casillero14=Label(ventana,image=img_casillero1,bg="#D9D9D9",highlightthickness=0).place(x=528,y=122)
        self.casillero15=Label(ventana,image=img_casillero1,bg="#D9D9D9",highlightthickness=0).place(x=546,y=122)
        
        #Cosas del calemtamiento
        self.bandaelastica1=Label(ventana,image=img_calentBanda1,bg="#D9D9D9",highlightthickness=0).place(x=96,y=119)        
        self.bandaelastica2=Label(ventana,image=img_calentBanda1,bg="#D9D9D9",highlightthickness=0).place(x=115,y=119)
        self.bandaelastica3=Label(ventana,image=img_calentBanda1,bg="#D9D9D9",highlightthickness=0).place(x=136,y=119)
        self.bandaelastica4=Label(ventana,image=img_calentBanda1,bg="#D9D9D9",highlightthickness=0).place(x=157,y=119)
        self.bandaelastica5=Label(ventana,image=img_calentBanda1,bg="#D9D9D9",highlightthickness=0).place(x=178,y=119)
        self.bandaelastica6=Label(ventana,image=img_calentBanda1,bg="#D9D9D9",highlightthickness=0).place(x=199,y=119)
        self.bandaelastica7=Label(ventana,image=img_calentBanda1,bg="#D9D9D9",highlightthickness=0).place(x=220,y=119)
        self.bandaelastica8=Label(ventana,image=img_calentBanda1,bg="#D9D9D9",highlightthickness=0).place(x=241,y=119)
        
        #Pelotas
        self.pelota1=Label(ventana,image=img_calentPelota1,bg="#D9D9D9",highlightthickness=0).place(x=125,y=150)
        self.pelota2=Label(ventana,image=img_calentPelota1,bg="#D9D9D9",highlightthickness=0).place(x=145,y=150)
        self.pelota3=Label(ventana,image=img_calentPelota1,bg="#D9D9D9",highlightthickness=0).place(x=164,y=150)
        self.pelota4=Label(ventana,image=img_calentPelota1,bg="#D9D9D9",highlightthickness=0).place(x=184,y=150)
        self.pelota5=Label(ventana,image=img_calentPelota1,bg="#D9D9D9",highlightthickness=0).place(x=224,y=150)
        self.pelota6=Label(ventana,image=img_calentPelota1,bg="#D9D9D9",highlightthickness=0).place(x=204,y=150)
        self.pelota7=Label(ventana,image=img_calentPelota1,bg="#D9D9D9",highlightthickness=0).place(x=244,y=150)
        
        #Alfombras
        self.alfombra1=Label(ventana,image=img_calentAlfombra1,bg="#D9D9D9",highlightthickness=0).place(x=66,y=149)
        
        self.alfombra2=Label(ventana,image=img_calentAlfombra1,bg="#D9D9D9",highlightthickness=0).place(x=62,y=167)
        self.alfombra3=Label(ventana,image=img_calentAlfombra1,bg="#D9D9D9",highlightthickness=0).place(x=56,y=185)
        self.alfombra4=Label(ventana,image=img_calentAlfombra1,bg="#D9D9D9",highlightthickness=0).place(x=51,y=204)
        self.alfombra5=Label(ventana,image=img_calentAlfombra1,bg="#D9D9D9",highlightthickness=0).place(x=49,y=222)
        self.alfombra6=Label(ventana,image=img_calentAlfombra1,bg="#D9D9D9",highlightthickness=0).place(x=67,y=223)
        self.alfombra7=Label(ventana,image=img_calentAlfombra1,bg="#D9D9D9",highlightthickness=0).place(x=72,y=204)
        self.alfombra8=Label(ventana,image=img_calentAlfombra1,bg="#D9D9D9",highlightthickness=0).place(x=75,y=185)
        self.alfombra9=Label(ventana,image=img_calentAlfombra1,bg="#D9D9D9",highlightthickness=0).place(x=80,y=167)
        self.alfombra10=Label(ventana,image=img_calentAlfombra1,bg="#D9D9D9",highlightthickness=0).place(x=84,y=149)
        
        #Cinturones
        self.cinturon1=Label(ventana,image=img_calentCinto1,bg="#D9D9D9",highlightthickness=0).place(x=121,y=170)
        self.cinturon2=Label(ventana,image=img_calentCinto1,bg="#D9D9D9",highlightthickness=0).place(x=150,y=170)
        self.cinturon3=Label(ventana,image=img_calentCinto1,bg="#D9D9D9",highlightthickness=0).place(x=179,y=170)
        self.cinturon4=Label(ventana,image=img_calentCinto1,bg="#D9D9D9",highlightthickness=0).place(x=208,y=170)
        self.cinturon5=Label(ventana,image=img_calentCinto1,bg="#D9D9D9",highlightthickness=0).place(x=235,y=170)
        self.cinturon6=Label(ventana,image=img_calentCinto1,bg="#D9D9D9",highlightthickness=0).place(x=151,y=186)
        self.cinturon7=Label(ventana,image=img_calentCinto1,bg="#D9D9D9",highlightthickness=0).place(x=208,y=186)
        
        
        #Caminadoras
        self.caminadora1=Label(ventana,image=img_cardioCaminadora1,bg="#D9D9D9",highlightthickness=0).place(x=48,y=268)
        self.caminadora2=Label(ventana,image=img_cardioCaminadora1,bg="#D9D9D9",highlightthickness=0).place(x=48,y=301)
        self.caminadora3=Label(ventana,image=img_cardioCaminadora1,bg="#D9D9D9",highlightthickness=0).place(x=48,y=334)
        self.caminadora4=Label(ventana,image=img_cardioCaminadora1,bg="#D9D9D9",highlightthickness=0).place(x=48,y=367)
        self.caminadora5=Label(ventana,image=img_cardioCaminadora1,bg="#D9D9D9",highlightthickness=0).place(x=48,y=400)
        self.caminadora6=Label(ventana,image=img_cardioCaminadora1,bg="#D9D9D9",highlightthickness=0).place(x=48,y=433)
        self.caminadora7=Label(ventana,image=img_cardioCaminadora1,bg="#D9D9D9",highlightthickness=0).place(x=48,y=466)
        self.caminadora8=Label(ventana,image=img_cardioCaminadora1,bg="#D9D9D9",highlightthickness=0).place(x=48,y=499)
        self.caminadora9=Label(ventana,image=img_cardioCaminadora1,bg="#D9D9D9",highlightthickness=0).place(x=48,y=532)
        self.caminadora10=Label(ventana,image=img_cardioCaminadora1,bg="#D9D9D9",highlightthickness=0).place(x=48,y=565)
        
        #Elipticas
        self.eliptica1=Label(ventana,image=img_cardioEliptica1,bg="#D9D9D9",highlightthickness=0).place(x=111,y=268)
        self.eliptica2=Label(ventana,image=img_cardioEliptica1,bg="#D9D9D9",highlightthickness=0).place(x=111,y=302)
        self.eliptica3=Label(ventana,image=img_cardioEliptica1,bg="#D9D9D9",highlightthickness=0).place(x=111,y=335)
        self.eliptica4=Label(ventana,image=img_cardioEliptica1,bg="#D9D9D9",highlightthickness=0).place(x=111,y=367)
        self.eliptica5=Label(ventana,image=img_cardioEliptica1,bg="#D9D9D9",highlightthickness=0).place(x=111,y=400)
        self.eliptica6=Label(ventana,image=img_cardioEliptica1,bg="#D9D9D9",highlightthickness=0).place(x=111,y=434)
        self.eliptica7=Label(ventana,image=img_cardioEliptica1,bg="#D9D9D9",highlightthickness=0).place(x=111,y=468)
        self.eliptica8=Label(ventana,image=img_cardioEliptica1,bg="#D9D9D9",highlightthickness=0).place(x=111,y=501)
        self.eliptica9=Label(ventana,image=img_cardioEliptica1,bg="#D9D9D9",highlightthickness=0).place(x=111,y=533)
        self.eliptica10=Label(ventana,image=img_cardioEliptica1,bg="#D9D9D9",highlightthickness=0).place(x=111,y=566)
        
        #Escaladoras
        self.escaladora1=Label(ventana,image=img_cardioEscaladora1,bg="#D9D9D9",highlightthickness=0).place(x=181,y=268)
        self.escaladora2=Label(ventana,image=img_cardioEscaladora1,bg="#D9D9D9",highlightthickness=0).place(x=181,y=302)
        self.escaladora3=Label(ventana,image=img_cardioEscaladora1,bg="#D9D9D9",highlightthickness=0).place(x=181,y=335)
        self.escaladora4=Label(ventana,image=img_cardioEscaladora1,bg="#D9D9D9",highlightthickness=0).place(x=181,y=367)
        self.escaladora5=Label(ventana,image=img_cardioEscaladora1,bg="#D9D9D9",highlightthickness=0).place(x=181,y=401)
        self.escaladora6=Label(ventana,image=img_cardioEscaladora1,bg="#D9D9D9",highlightthickness=0).place(x=181,y=435)
        self.escaladora7=Label(ventana,image=img_cardioEscaladora1,bg="#D9D9D9",highlightthickness=0).place(x=181,y=469)
        self.escaladora8=Label(ventana,image=img_cardioEscaladora1,bg="#D9D9D9",highlightthickness=0).place(x=181,y=503)
        
        #Remos Cardio
        self.remoC1=Label(ventana,image=img_cardioRemo1,bg="#D9D9D9",highlightthickness=0).place(x=245,y=268)
        self.remoC2=Label(ventana,image=img_cardioRemo1,bg="#D9D9D9",highlightthickness=0).place(x=245,y=302)
        self.remoC3=Label(ventana,image=img_cardioRemo1,bg="#D9D9D9",highlightthickness=0).place(x=245,y=336)
        self.remoC4=Label(ventana,image=img_cardioRemo1,bg="#D9D9D9",highlightthickness=0).place(x=245,y=368)
        self.remoC5=Label(ventana,image=img_cardioRemo1,bg="#D9D9D9",highlightthickness=0).place(x=245,y=401)
        self.remoC6=Label(ventana,image=img_cardioRemo1,bg="#D9D9D9",highlightthickness=0).place(x=245,y=435)
        self.remoC7=Label(ventana,image=img_cardioRemo1,bg="#D9D9D9",highlightthickness=0).place(x=245,y=470)
        self.remoC8=Label(ventana,image=img_cardioRemo1,bg="#D9D9D9",highlightthickness=0).place(x=245,y=504)
        
        #Spinning
        self.bicicleta1=Label(ventana,image=img_spinBici1,bg="#D9D9D9",highlightthickness=0).place(x=306,y=268)
        self.bicicleta2=Label(ventana,image=img_spinBici1,bg="#D9D9D9",highlightthickness=0).place(x=306,y=302)
        self.bicicleta3=Label(ventana,image=img_spinBici1,bg="#D9D9D9",highlightthickness=0).place(x=306,y=336)
        self.bicicleta4=Label(ventana,image=img_spinBici1,bg="#D9D9D9",highlightthickness=0).place(x=306,y=368)
        self.bicicleta5=Label(ventana,image=img_spinBici1,bg="#D9D9D9",highlightthickness=0).place(x=306,y=401)
        self.bicicleta6=Label(ventana,image=img_spinBici1,bg="#D9D9D9",highlightthickness=0).place(x=306,y=434)
        self.bicicleta7=Label(ventana,image=img_spinBici1,bg="#D9D9D9",highlightthickness=0).place(x=306,y=467)
        self.bicicleta8=Label(ventana,image=img_spinBici1,bg="#D9D9D9",highlightthickness=0).place(x=306,y=503)
        self.bicicleta9=Label(ventana,image=img_spinBici1,bg="#D9D9D9",highlightthickness=0).place(x=306,y=539)
        self.bicicleta10=Label(ventana,image=img_spinBici1,bg="#D9D9D9",highlightthickness=0).place(x=306,y=575)
        
        
        #Area de pecho
        self.mariposa1=Label(ventana,image=img_PechoMariposas1,bg="#D9D9D9",highlightthickness=0).place(x=380,y=418)
        self.mariposa2=Label(ventana,image=img_PechoMariposas1,bg="#D9D9D9",highlightthickness=0).place(x=380,y=382)
        self.mariposa3=Label(ventana,image=img_PechoMariposas1,bg="#D9D9D9",highlightthickness=0).place(x=380,y=345)
        self.mariposa4=Label(ventana,image=img_PechoMariposas1,bg="#D9D9D9",highlightthickness=0).place(x=380,y=310)
        
        #Press de banca
        self.pressbanca1=Label(ventana,image=img_PechoPressB1,bg="#D9D9D9",highlightthickness=0).place(x=380,y=594)
        self.pressbanca2=Label(ventana,image=img_PechoPressB1,bg="#D9D9D9",highlightthickness=0).place(x=380,y=559)
        self.pressbanca3=Label(ventana,image=img_PechoPressB1,bg="#D9D9D9",highlightthickness=0).place(x=380,y=524)
        self.pressbanca4=Label(ventana,image=img_PechoPressB1,bg="#D9D9D9",highlightthickness=0).place(x=380,y=489)
        self.pressbanca5=Label(ventana,image=img_PechoPressB1,bg="#D9D9D9",highlightthickness=0).place(x=380,y=457)
        
        #Poleas
        self.poleaPecho1=Label(ventana,image=img_PechoPolea1,bg="#D9D9D9",highlightthickness=0).place(x=420,y=594)
        self.poleaPecho2=Label(ventana,image=img_PechoPolea1,bg="#D9D9D9",highlightthickness=0).place(x=420,y=559)
        self.poleaPecho3=Label(ventana,image=img_PechoPolea1,bg="#D9D9D9",highlightthickness=0).place(x=420,y=523)
        self.poleaPecho4=Label(ventana,image=img_PechoPolea1,bg="#D9D9D9",highlightthickness=0).place(x=420,y=489)
        self.poleaPecho5=Label(ventana,image=img_PechoPolea1,bg="#D9D9D9",highlightthickness=0).place(x=420,y=452)
        self.poleaPecho6=Label(ventana,image=img_PechoPolea1,bg="#D9D9D9",highlightthickness=0).place(x=420,y=415)
        
        #Aperturas
        self.aperturas1=Label(ventana,image=img_PechoAperturas1,bg="#D9D9D9",highlightthickness=0).place(x=460,y=590)
        self.aperturas2=Label(ventana,image=img_PechoAperturas1,bg="#D9D9D9",highlightthickness=0).place(x=460,y=552)
        self.aperturas3=Label(ventana,image=img_PechoAperturas1,bg="#D9D9D9",highlightthickness=0).place(x=460,y=512)
        self.aperturas4=Label(ventana,image=img_PechoAperturas1,bg="#D9D9D9",highlightthickness=0).place(x=460,y=470)
        self.aperturas5=Label(ventana,image=img_PechoAperturas1,bg="#D9D9D9",highlightthickness=0).place(x=460,y=430)
        
        #Press inclinado
        self.pressIn1=Label(ventana,image=img_PechoPressInc1,bg="#D9D9D9",highlightthickness=0).place(x=507,y=591)
        self.pressIn2=Label(ventana,image=img_PechoPressInc1,bg="#D9D9D9",highlightthickness=0).place(x=507,y=555)
        self.pressIn3=Label(ventana,image=img_PechoPressInc1,bg="#D9D9D9",highlightthickness=0).place(x=507,y=521)
        self.pressIn4=Label(ventana,image=img_PechoPressInc1,bg="#D9D9D9",highlightthickness=0).place(x=507,y=483)
        self.pressIn5=Label(ventana,image=img_PechoPressInc1,bg="#D9D9D9",highlightthickness=0).place(x=507,y=445)
        
        #Baños
        self.bath1=Label(ventana,image=img_bath1,bg="#D9D9D9",highlightthickness=0).place(x=680,y=606)
        self.bath2=Label(ventana,image=img_bath1,bg="#D9D9D9",highlightthickness=0).place(x=722,y=606)
        self.bath3=Label(ventana,image=img_bath1,bg="#D9D9D9",highlightthickness=0).place(x=762,y=606)
        self.bath4=Label(ventana,image=img_bath1,bg="#D9D9D9",highlightthickness=0).place(x=810,y=606)
        
        #Area de espalda
        self.poleaAlta1=Label(ventana,image=img_EspalPolAlta1,bg="#D9D9D9",highlightthickness=0).place(x=563,y=568)
        self.poleaAlta2=Label(ventana,image=img_EspalPolAlta1,bg="#D9D9D9",highlightthickness=0).place(x=563,y=528)
        self.poleaAlta3=Label(ventana,image=img_EspalPolAlta1,bg="#D9D9D9",highlightthickness=0).place(x=563,y=487)
        self.poleaAlta4=Label(ventana,image=img_EspalPolAlta1,bg="#D9D9D9",highlightthickness=0).place(x=563,y=448)
        self.poleaAlta5=Label(ventana,image=img_EspalPolAlta1,bg="#D9D9D9",highlightthickness=0).place(x=563,y=410)
        
        #Polea baja
        self.poleaBaja1=Label(ventana,image=img_EspalPolBaja1,bg="#D9D9D9",highlightthickness=0).place(x=563,y=369)
        self.poleaBaja2=Label(ventana,image=img_EspalPolBaja1,bg="#D9D9D9",highlightthickness=0).place(x=563,y=328)
        self.poleaBaja3=Label(ventana,image=img_EspalPolBaja1,bg="#D9D9D9",highlightthickness=0).place(x=563,y=285)
        self.poleaBaja4=Label(ventana,image=img_EspalPolBaja1,bg="#D9D9D9",highlightthickness=0).place(x=607,y=329)
        self.poleaBaja5=Label(ventana,image=img_EspalPolBaja1,bg="#D9D9D9",highlightthickness=0).place(x=607,y=369)
        
        #Dorsaderas
        self.dorsadera1=Label(ventana,image=img_EspalDorsadera1,bg="#D9D9D9",highlightthickness=0).place(x=607,y=568)
        self.dorsadera2=Label(ventana,image=img_EspalDorsadera1,bg="#D9D9D9",highlightthickness=0).place(x=607,y=528)
        self.dorsadera3=Label(ventana,image=img_EspalDorsadera1,bg="#D9D9D9",highlightthickness=0).place(x=607,y=490)
        self.dorsadera4=Label(ventana,image=img_EspalDorsadera1,bg="#D9D9D9",highlightthickness=0).place(x=607,y=452)
        self.dorsadera5=Label(ventana,image=img_EspalDorsadera1,bg="#D9D9D9",highlightthickness=0).place(x=607,y=411)
        
        #Remos Espalda
        self.remoEsp1=Label(ventana,image=img_EspalRemo1,bg="#D9D9D9",highlightthickness=0).place(x=512,y=353)
        self.remoEsp2=Label(ventana,image=img_EspalRemo1,bg="#D9D9D9",highlightthickness=0).place(x=512,y=317)
        self.remoEsp3=Label(ventana,image=img_EspalRemo1,bg="#D9D9D9",highlightthickness=0).place(x=512,y=284)
        self.remoEsp4=Label(ventana,image=img_EspalRemo1,bg="#D9D9D9",highlightthickness=0).place(x=512,y=251)
        self.remoEsp5=Label(ventana,image=img_EspalRemo1,bg="#D9D9D9",highlightthickness=0).place(x=561,y=251)
        
        #Barras Espalda
        self.barraEsp1=Label(ventana,image=img_EspalBarra1,bg="#D9D9D9",highlightthickness=0).place(x=647,y=412)
        self.barraEsp2=Label(ventana,image=img_EspalBarra1,bg="#D9D9D9",highlightthickness=0).place(x=647,y=373)
        self.barraEsp3=Label(ventana,image=img_EspalBarra1,bg="#D9D9D9",highlightthickness=0).place(x=647,y=334)
        self.barraEsp4=Label(ventana,image=img_EspalBarra1,bg="#D9D9D9",highlightthickness=0).place(x=647,y=297)
        self.barraEsp5=Label(ventana,image=img_EspalBarra1,bg="#D9D9D9",highlightthickness=0).place(x=608,y=287)
        
        #Dominadas
        self.dominada1=Label(ventana,image=img_EspalDominada1,bg="#D9D9D9",highlightthickness=0).place(x=647,y=490)
        self.dominada2=Label(ventana,image=img_EspalDominada1,bg="#D9D9D9",highlightthickness=0).place(x=681,y=490)
        self.dominada3=Label(ventana,image=img_EspalDominada1,bg="#D9D9D9",highlightthickness=0).place(x=647,y=454)
        self.dominada4=Label(ventana,image=img_EspalDominada1,bg="#D9D9D9",highlightthickness=0).place(x=681,y=453)
        
        #Bancas
        self.banca1=Label(ventana,image=img_banco1,bg="#D9D9D9",highlightthickness=0).place(x=845,y=569)
        self.banca2=Label(ventana,image=img_banco1,bg="#D9D9D9",highlightthickness=0).place(x=813,y=569)
        self.banca3=Label(ventana,image=img_banco1,bg="#D9D9D9",highlightthickness=0).place(x=781,y=569)
        self.banca4=Label(ventana,image=img_banco1,bg="#D9D9D9",highlightthickness=0).place(x=749,y=569)
        self.banca5=Label(ventana,image=img_banco1,bg="#D9D9D9",highlightthickness=0).place(x=717,y=569)
        self.banca6=Label(ventana,image=img_banco1,bg="#D9D9D9",highlightthickness=0).place(x=685,y=569)
        self.banca7=Label(ventana,image=img_banco1,bg="#D9D9D9",highlightthickness=0).place(x=653,y=569)

        #Duchas
        self.ducha1=Label(ventana,image=img_ducha1,bg="#D9D9D9",highlightthickness=0).place(x=1216,y=608)
        self.ducha2=Label(ventana,image=img_ducha1,bg="#D9D9D9",highlightthickness=0).place(x=1189,y=608)
        self.ducha3=Label(ventana,image=img_ducha1,bg="#D9D9D9",highlightthickness=0).place(x=1166,y=608)
        self.ducha4=Label(ventana,image=img_ducha1,bg="#D9D9D9",highlightthickness=0).place(x=1142,y=608)
        self.ducha5=Label(ventana,image=img_ducha1,bg="#D9D9D9",highlightthickness=0).place(x=1116,y=608)
        self.ducha6=Label(ventana,image=img_ducha1,bg="#D9D9D9",highlightthickness=0).place(x=1089,y=608)
        self.ducha7=Label(ventana,image=img_ducha1,bg="#D9D9D9",highlightthickness=0).place(x=1065,y=608)
        self.ducha8=Label(ventana,image=img_ducha1,bg="#D9D9D9",highlightthickness=0).place(x=1041,y=608)
        self.ducha9=Label(ventana,image=img_ducha1,bg="#D9D9D9",highlightthickness=0).place(x=1017,y=608)
        self.ducha10=Label(ventana,image=img_ducha1,bg="#D9D9D9",highlightthickness=0).place(x=992,y=608)
        self.ducha11=Label(ventana,image=img_ducha1,bg="#D9D9D9",highlightthickness=0).place(x=967,y=608)
        self.ducha12=Label(ventana,image=img_ducha1,bg="#D9D9D9",highlightthickness=0).place(x=943,y=608)
        self.ducha13=Label(ventana,image=img_ducha1,bg="#D9D9D9",highlightthickness=0).place(x=919,y=608)
        self.ducha14=Label(ventana,image=img_ducha1,bg="#D9D9D9",highlightthickness=0).place(x=893,y=608)
        
        #Area de pierna
        self.rakcSentadilla1=Label(ventana,image=img_PiernaSentadillas,bg="#D9D9D9",highlightthickness=0).place(x=736,y=508)
        self.rakcSentadilla2=Label(ventana,image=img_PiernaSentadillas,bg="#D9D9D9",highlightthickness=0).place(x=736,y=468)
        self.rakcSentadilla3=Label(ventana,image=img_PiernaSentadillas,bg="#D9D9D9",highlightthickness=0).place(x=736,y=424)
        self.rakcSentadilla4=Label(ventana,image=img_PiernaSentadillas,bg="#D9D9D9",highlightthickness=0).place(x=736,y=380)
        self.rakcSentadilla5=Label(ventana,image=img_PiernaSentadillas,bg="#D9D9D9",highlightthickness=0).place(x=736,y=336)
        
        #Prensas
        self.prensa1=Label(ventana,image=img_PiernaPrensa1,bg="#D9D9D9",highlightthickness=0).place(x=793,y=508)
        self.prensa2=Label(ventana,image=img_PiernaPrensa1,bg="#D9D9D9",highlightthickness=0).place(x=793,y=466)
        self.prensa3=Label(ventana,image=img_PiernaPrensa1,bg="#D9D9D9",highlightthickness=0).place(x=793,y=421)
        self.prensa4=Label(ventana,image=img_PiernaPrensa1,bg="#D9D9D9",highlightthickness=0).place(x=793,y=379)
        
        #Cuadriceps
        self.cuadriceps1=Label(ventana,image=img_PiernaCuad1,bg="#D9D9D9",highlightthickness=0).place(x=847,y=508)
        self.cuadriceps2=Label(ventana,image=img_PiernaCuad1,bg="#D9D9D9",highlightthickness=0).place(x=847,y=468)
        self.cuadriceps3=Label(ventana,image=img_PiernaCuad1,bg="#D9D9D9",highlightthickness=0).place(x=847,y=424)
        self.cuadriceps4=Label(ventana,image=img_PiernaCuad1,bg="#D9D9D9",highlightthickness=0).place(x=847,y=380)
        self.cuadriceps5=Label(ventana,image=img_PiernaCuad1,bg="#D9D9D9",highlightthickness=0).place(x=795,y=336)
        
        #Fermorales
        self.fermoral1=Label(ventana,image=img_PiernaFerm1,bg="#D9D9D9",highlightthickness=0).place(x=891,y=508)
        self.fermoral2=Label(ventana,image=img_PiernaFerm1,bg="#D9D9D9",highlightthickness=0).place(x=891,y=446)
        self.fermoral3=Label(ventana,image=img_PiernaFerm1,bg="#D9D9D9",highlightthickness=0).place(x=891,y=421)
        self.fermoral4=Label(ventana,image=img_PiernaFerm1,bg="#D9D9D9",highlightthickness=0).place(x=891,y=378)
        self.fermoral5=Label(ventana,image=img_PiernaFerm1,bg="#D9D9D9",highlightthickness=0).place(x=849,y=335)
        
        #Pantorrilas
        self.pantorrilla1=Label(ventana,image=img_PiernaPant1,bg="#D9D9D9",highlightthickness=0).place(x=925,y=505)
        self.pantorrilla2=Label(ventana,image=img_PiernaPant1,bg="#D9D9D9",highlightthickness=0).place(x=925,y=464)
        self.pantorrilla3=Label(ventana,image=img_PiernaPant1,bg="#D9D9D9",highlightthickness=0).place(x=925,y=422)
        self.pantorrilla4=Label(ventana,image=img_PiernaPant1,bg="#D9D9D9",highlightthickness=0).place(x=925,y=374)
        self.pantorrilla5=Label(ventana,image=img_PiernaPant1,bg="#D9D9D9",highlightthickness=0).place(x=892,y=332)
        
        #Sentadilla Smith
        self.smith1=Label(ventana,image=img_PiernaSentadillas,bg="#D9D9D9",highlightthickness=0).place(x=969,y=507)
        self.smith2=Label(ventana,image=img_PiernaSentadillas,bg="#D9D9D9",highlightthickness=0).place(x=969,y=464)
        self.smith3=Label(ventana,image=img_PiernaSentadillas,bg="#D9D9D9",highlightthickness=0).place(x=969,y=422)
        self.smith4=Label(ventana,image=img_PiernaSentadillas,bg="#D9D9D9",highlightthickness=0).place(x=969,y=380)
        
        #Barras Pierna
        self.BarraPier1=Label(ventana,image=img_PiernaBarra1,bg="#D9D9D9",highlightthickness=0).place(x=733,y=280)
        self.BarraPier2=Label(ventana,image=img_PiernaBarra1,bg="#D9D9D9",highlightthickness=0).place(x=786,y=280)
        self.BarraPier3=Label(ventana,image=img_PiernaBarra1,bg="#D9D9D9",highlightthickness=0).place(x=835,y=280)
        self.BarraPier4=Label(ventana,image=img_PiernaBarra1,bg="#D9D9D9",highlightthickness=0).place(x=889,y=280)
        self.BarraPier5=Label(ventana,image=img_PiernaBarra1,bg="#D9D9D9",highlightthickness=0).place(x=940,y=280)
        
        #Area de pesas
        self.pesach1=Label(ventana,image=img_PesasPesa1,bg="#D9D9D9",highlightthickness=0).place(x=1201,y=339)
        self.pesach2=Label(ventana,image=img_PesasPesa1,bg="#D9D9D9",highlightthickness=0).place(x=1201,y=355)
        self.pesach3=Label(ventana,image=img_PesasPesa1,bg="#D9D9D9",highlightthickness=0).place(x=1201,y=371)
        self.pesach4=Label(ventana,image=img_PesasPesa1,bg="#D9D9D9",highlightthickness=0).place(x=1201,y=387)
        self.pesach5=Label(ventana,image=img_PesasPesa1,bg="#D9D9D9",highlightthickness=0).place(x=1201,y=403)
        self.pesach6=Label(ventana,image=img_PesasPesa1,bg="#D9D9D9",highlightthickness=0).place(x=1201,y=419)
        self.pesach7=Label(ventana,image=img_PesasPesa1,bg="#D9D9D9",highlightthickness=0).place(x=1201,y=434)
        self.pesach8=Label(ventana,image=img_PesasPesa1,bg="#D9D9D9",highlightthickness=0).place(x=1201,y=451)
        
        #Pesas Grandes
        self.pesaG1=Label(ventana,image=img_PesasPesaG1,bg="#D9D9D9",highlightthickness=0).place(x=1206,y=470)
        self.pesaG2=Label(ventana,image=img_PesasPesaG1,bg="#D9D9D9",highlightthickness=0).place(x=1206,y=490)
        self.pesaG3=Label(ventana,image=img_PesasPesaG1,bg="#D9D9D9",highlightthickness=0).place(x=1206,y=513)
        self.pesaG4=Label(ventana,image=img_PesasPesaG1,bg="#D9D9D9",highlightthickness=0).place(x=1206,y=536)
        self.pesaG5=Label(ventana,image=img_PesasPesaG1,bg="#D9D9D9",highlightthickness=0).place(x=1206,y=556)
        self.pesaG6=Label(ventana,image=img_PesasPesaG1,bg="#D9D9D9",highlightthickness=0).place(x=1172,y=556)
        self.pesaG7=Label(ventana,image=img_PesasPesaG1,bg="#D9D9D9",highlightthickness=0).place(x=1172,y=536)
        self.pesaG8=Label(ventana,image=img_PesasPesaG1,bg="#D9D9D9",highlightthickness=0).place(x=1172,y=514)
        self.pesaG9=Label(ventana,image=img_PesasPesaG1,bg="#D9D9D9",highlightthickness=0).place(x=1172,y=493)
        
        #Barras planas
        self.barraPlana1=Label(ventana,image=img_PesasBarraP1,bg="#D9D9D9",highlightthickness=0).place(x=1077,y=457)
        self.barraPlana2=Label(ventana,image=img_PesasBarraP1,bg="#D9D9D9",highlightthickness=0).place(x=1077,y=441)
        self.barraPlana3=Label(ventana,image=img_PesasBarraP1,bg="#D9D9D9",highlightthickness=0).place(x=1077,y=424)
        self.barraPlana4=Label(ventana,image=img_PesasBarraP1,bg="#D9D9D9",highlightthickness=0).place(x=1077,y=407)
        
        #Barras z
        self.barraZ1=Label(ventana,image=img_PesasBarraZ1,bg="#D9D9D9",highlightthickness=0).place(x=1075,y=554)
        self.barraZ1=Label(ventana,image=img_PesasBarraZ1,bg="#D9D9D9",highlightthickness=0).place(x=1075,y=539)
        self.barraZ1=Label(ventana,image=img_PesasBarraZ1,bg="#D9D9D9",highlightthickness=0).place(x=1075,y=524)
        self.barraZ1=Label(ventana,image=img_PesasBarraZ1,bg="#D9D9D9",highlightthickness=0).place(x=1075,y=508) 
        
        ventana.mainloop() 
    
    def esperarTiempo(self,speed):
        if not self.velocidad=="Fast":
            time.sleep(speed/110)

    
    def verResultados(self):
        
        
        def graficaPastel():
            pass
            
        def graficaNormal(datos,titulo):
            self.listaDias=list(range(0,len(datos)))
            
            
            # Graficar los datos
            plt.plot(self.listaDias, datos)
            plt.xlabel('Días')
            #plt.xticks(self.listaDias)
            plt.ylabel(titulo)
            plt.title(titulo)
            plt.show()
        
        
        ventanaResul=Toplevel(ventana)
        ventanaResul.geometry("1280x720+35+10")
        ventanaResul.config(bg="#1D1F24")
        ventanaResul.resizable(width=False,height=False)
        
        Label(ventanaResul,text=(f"Caja ${self.dineroCaja}"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=29,y=20)
        Label(ventanaResul,text=(f"Gastos totales ${self.gastosTotalesSim}"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=29,y=52)
        Label(ventanaResul,text=(f"Ganancias totales ${self.gananciasTotalesSim}"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=29,y=84)
        
        Label(ventanaResul,text=(f"Usuarios totales que llegaron {self.usuariosTotales}"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=29,y=127)
        Label(ventanaResul,text=(f"Clientes totales que llegaron {self.clientesTotales}"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=29,y=164)
        
        Label(ventanaResul,text=(f"Suscripciones a visita {self.subDia}"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=29,y=217)
        Label(ventanaResul,text=(f"Suscripciones a semana {self.subSemana}"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=29,y=255)
        Label(ventanaResul,text=(f"Suscripciones a mes {self.subMes}"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=29,y=294)
        Label(ventanaResul,text=(f"Suscripciones a trimestre {self.subTrim}"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=29,y=334)
        Label(ventanaResul,text=(f"Suscripciones a anualidad {self.subAnua}"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=29,y=366)
        
        Label(ventanaResul,text=(f"Personas que entrenaron cardio {self.personasEntrenaronCardio}"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=29,y=451)
        Label(ventanaResul,text=(f"Personas que entrenaron espalda {self.personasEntrenaronEspalda}"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=29,y=487)
        Label(ventanaResul,text=(f"Personas que entrenaron pecho {self.personasEntrenaronPecho}"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=29,y=523)
        Label(ventanaResul,text=(f"Personas que entrenaron pierna {self.personasEntrenaronPierna}"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=29,y=559)
        Label(ventanaResul,text=(f"Personas que entrenaron pesas {self.personasEntrenaronPesas}"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=29,y=595)
        Label(ventanaResul,text=(f"Personas que entrenaron spinning {self.personasEntrenaronSpinning}"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=29,y=631)
        
        Label(ventanaResul,text=(f"Personas que hicieron cardio antes de entrenar {self.personasHacenCardio}"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=640,y=87)
        Label(ventanaResul,text=(f"Personas que no hicieron cardio antes de entrenar {self.personasNoHacenCardio}"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=640,y=127)
                
        Label(ventanaResul,text=(f"Lesionados que requirieron hospital {self.personasRequierHosp}"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=607,y=179)
        Label(ventanaResul,text=(f"Lesionados que no requirieron hospital {self.personasNoRequierHosp}"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=607,y=215)
        
        Label(ventanaResul,text=(f"Lesionados de cada día"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=930,y=314)
        
        Label(ventanaResul,text=(f"Tiempos promedio en el gimnasio cada día"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=726,y=400)

        Label(ventanaResul,text=(f"Máquinas averiadas cada día"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=869,y=495)

        Label(ventanaResul,text=(f"Ganancias de cada día"),font=("Arial",15),bg="#1D1F24",foreground="white").place(x=930,y=588)
        
        img_grafica=PhotoImage(file="Imagenes/SimulacionIMG/grafica.png")
        #Graficas pastel
        '''
        grafica1=Button(ventanaResul,image=img_grafica).place(x=516,y=119)
        grafica2=Button(ventanaResul,image=img_grafica).place(x=397,y=322)
        grafica3=Button(ventanaResul,image=img_grafica).place(x=467,y=587)
        grafica4=Button(ventanaResul,image=img_grafica).place(x=1194,y=86)
        grafica5=Button(ventanaResul,image=img_grafica).place(x=1194,y=177)'''
        #Graficas normales
        
        
        #print(self.lesionadosCadaDia)
        #print(self.tiemposPersonasSim)
        #print(self.maquinasAveriadasSim)
        #print(self.gananciaDiaSim)
        
        grafica6=Button(ventanaResul,image=img_grafica,command=lambda:graficaNormal(self.lesionadosCadaDia,"Lesionados de cada día"),bg="#1D1F24",highlightthickness=0,bd=0).place(x=1194,y=268)
        grafica7=Button(ventanaResul,image=img_grafica,command=lambda:graficaNormal(self.tiemposPersonasSim,"Tiempor promedio en el gimnasio (minutos)"),bg="#1D1F24",highlightthickness=0,bd=0).place(x=1194,y=357)
        grafica8=Button(ventanaResul,image=img_grafica,command=lambda:graficaNormal(self.maquinasAveriadasSim,"Máquinas averiadas cada día"),bg="#1D1F24",highlightthickness=0,bd=0).place(x=1194,y=451)
        grafica9=Button(ventanaResul,image=img_grafica,command=lambda:graficaNormal(self.gananciaDiaSim,"Ganancias de cada día $"),bg="#1D1F24",highlightthickness=0,bd=0).place(x=1194,y=542)
        
        
        
        ventanaResul.mainloop()
    
    
    def devuelveAleatorio(self):
        alea=random.choice(listaAleatorios)#[self.posAleatorio]
        #self.posAleatorio+=1
        #if self.posAleatorio==len(listaAleatorios):
            #self.posAleatorio=0
        return alea
    
    
    
    
    
    def devuelveValorTabla(self,tabla,aleatorio):
        nombres = []
        probabilidad = []
        tabla="./Datos/"+tabla
        
        with open(tabla, 'r') as f:
            for linea in f:
                elementos = linea.strip().split(',')
                if len(elementos) == 2:
                    producto = elementos[0].strip()
                    prob = elementos[1].strip()
                    nombres.append(producto)
                    probabilidad.append(float(prob))
    
        cont=0
        #Sacar la probabilidad acumulada
        probAcum=[]
        probAcum.append(0)
        for pro in probabilidad:
            probAcum.append(probAcum[cont]+pro)
            cont+=1
            
        ##print(probAcum)
        valor=None
        for pos in range(len(probAcum)-1):
            if aleatorio>=probAcum[pos] and aleatorio<=probAcum[pos+1]:
                 valor=nombres[pos]
                 
        return valor
    
    
    def extraePreciosTabla(self,archivo):
        productos = []
        precios = []
        
        with open(archivo, 'r') as f:
            for linea in f:
                elementos = linea.strip().split(',')
                if len(elementos) == 2:
                    producto = elementos[0].strip()
                    precio = elementos[1].strip()
                    productos.append(producto)
                    precios.append(precio)
        
        return productos, precios
    
      
    def inicia(self,velocidad):
        img_resultados=Label(ventana,image=resuIMG1,bd=0,bg="#1D1F24",highlightthickness=0).place(x=1026,y=22)
        lblStart=Label(ventana,image=startIMG2,bd=0,highlightthickness=0,bg="#1D1F24")
        lblStart.place(x=608,y=15) 
        messagebox.showinfo("SIMULACIÓN EN PROCESO","La simulación se llevará a cabo, espere a que se active el botón con la lupa para ver los resultados")
        
        global diasDeSimulacion
        try:
            diasDeSimulacion=self.diasSimular.get()
        except TclError:
            diasDeSimulacion=1
            
        self.listaDias=list(range(1,diasDeSimulacion+1))
            
        self.simular(velocidad)
        
        
        
    def start_clock(self):
        if self.process_running:
            self.current_time += timedelta(seconds=1) * self.speed_factor
            self.reloj.config(text=self.current_time.strftime("%I:%M:%S %p"))
            self.ventana.after(self.vel // self.speed_factor, self.start_clock)
   
        
    def personasParaDia(self):
        alea=self.devuelveAleatorio()
        #print(f"Aleatorio cantidad de personas del día {alea}")
        cantPersonasDia=self.devuelveValorTabla("1CantidadPersonasAsistenDia.txt",alea)
        cantPersonasDia=int(cantPersonasDia)
        #print(f"Aleatorio {alea} devuelve {cantPersonasDia}")
        #print(f"Asistirán {cantPersonasDia} personas al gimnasio")
        
        self.cantPersSim.append(cantPersonasDia)
        
        self.gananciaDia=0  #Ganancia del dia
        self.gastosDia=0       #Gastos del dia
        self.tiemposPersonas=[] #Tiempo promedio de las personas en el gimnasio durante el dia
        self.lesionadosDia=0    #Cantidad de lesionados del dia
        self.maquinasAveriadasDia=0 #Maquinas averiadas del día
        
        for personas in range(1,cantPersonasDia+1):
            #print(f"******* Persona {personas} Dia {self.dia} *******")
            
            
            #self.tiendaSuples=Label(ventana,image=suples2,bg="#D9D9D9",highlightthickness=0).place(x=1050,y=128)
            
            self.tiempoPersona=0
            
            
            clienUsu=self.devuelveAleatorio()
            #print(f"Aleatorio de cliente o usuario {clienUsu}")
            resu=self.devuelveValorTabla("2ClienteOUsuario.txt",clienUsu)
            #print(f"Aleatorio {clienUsu} devuelve {resu}")
            
            global band,tieneSub
            band=None
            tieneSub=None
            
            if resu=="Usuario del gimnasio":
                band=True
                tieneSub=True
                self.usuariosTotales+=1
            elif resu=="Usuario nuevo":
                band=True
                tieneSub=False
                self.usuariosTotales+=1
            elif resu=="Cliente externo":
                band=False
                self.clientesTotales+=1
            
            #Parte de calcular cuantas veces va a comprar
            aleaCantCompra=self.devuelveAleatorio()
            #print(f"Aleatorio para cantidad de compras {aleaCantCompra}")
            resultado=self.devuelveValorTabla("4ComprarUnaCantidadDeVeces.txt",aleaCantCompra)
            #print(f"Alea {aleaCantCompra} devuelve {resultado} veces va a comprar")
            
            
            #Parte de escoger los productos
            cantCompras=int(resultado)
            for compra in range(cantCompras):
                #print("\n")
                aleaProducto=self.devuelveAleatorio()
                #print(f"Aleatorio para producto {aleaProducto}")
                produ=self.devuelveValorTabla("5ComprarTipoDeProducto.txt",aleaProducto)
                #print(f"Alea {aleaProducto} devuelve {produ} para comprar")
                #print(produ)

        
                productosNombres = []
                preciosVenta = []
                archivo="./Datos/38TiendaInventarioPrecios.txt"
                with open(archivo, 'r') as f:
                    for linea in f:
                        elementos = linea.strip().split(',')
                        if len(elementos) == 2:
                            producto = elementos[0].strip()
                            precio = elementos[1].strip()
                            productosNombres.append(producto)
                            preciosVenta.append(int(precio))
                f.close()
                
                cantidadInv = []
                archivo2="./Datos/39TiendaInventarioCantidad.txt"
                with open(archivo2, 'r') as g:
                    for linea in g:
                        elementos = linea.strip().split(',')
                        if len(elementos) == 2:
                            producto = elementos[0].strip()
                            precio = elementos[1].strip()
                            #productosNombres.append(producto)
                            cantidadInv.append(int(precio))
                g.close()
                  
                precioCompra = []
                archivo3="./Datos/40PreciosProveedor.txt"
                with open(archivo3, 'r') as h:
                    for linea in h:
                        elementos = linea.strip().split(',')
                        if len(elementos) == 2:
                            producto = elementos[0].strip()
                            precio = elementos[1].strip()
                            #productosNombres.append(producto)
                            precioCompra.append(int(precio))
                h.close()    
                
                
                def f_producEsp(arch):
                    aleaProdEspeifico=self.devuelveAleatorio()
                    #print(f"Aleatorio producto especifico {aleaProdEspeifico}")
                    produEspec=self.devuelveValorTabla(arch,aleaProdEspeifico)
                    #print(f"Alea {aleaProdEspeifico} devuelve cantidad {produEspec}")
                    return produEspec

                
                produEspec=None
                
                if produ=="Proteina en polvo":
                    produEspec=f_producEsp("10ProteinaMarcaSabor.txt")
                    cantidadDelProd=int(f_producEsp("6ComprarCantidadDeBotes.txt"))
                    #print(f"Cantidad a comprar {cantidadDelProd}")
                
                elif produ=="Creatina":
                    produEspec=f_producEsp("11CreatinaMarcaSabor.txt")
                    cantidadDelProd=int(f_producEsp("6ComprarCantidadDeBotes.txt"))
                    #print(f"Cantidad a comprar {cantidadDelProd}")
                
                
                elif produ=="Pre-entreno":
                    produEspec=f_producEsp("12PreentrenoMarcaSabor.txt")
                    cantidadDelProd=int(f_producEsp("6ComprarCantidadDeBotes.txt"))
                    #print(f"Cantidad a comprar {cantidadDelProd}")
                
                elif produ=="Botella de agua":
                    produEspec=f_producEsp("7ComprarBotellasAgua.txt")
                    cantidadDelProd=int(f_producEsp("6ComprarCantidadDeBotes.txt"))
                    #print(f"Cantidad a comprar {cantidadDelProd}")
                
                elif produ=="Barra de proteina":
                    produEspec="Barra Ronnie C"
                    cantidadDelProd=int(f_producEsp("8ComprarBarrasProteicas.txt"))
                    #print(f"Cantidad a comprar {cantidadDelProd}")
                
                elif produ=="Bebida energetica":
                    produEspec="Monster"
                    cantidadDelProd=int(f_producEsp("9ComprarBebidasEnergeticas.txt"))
                    #print(f"Cantidad a comprar {cantidadDelProd}")
                    
                
                for prod in range(len(productosNombres)):
                    
                    if  produEspec == productosNombres[prod]:
                        #print(f"\n{produ}")
                        #print(f"Precio venta {preciosVenta[prod]}")
                        #print(f"Cantidad disponible {cantidadInv[prod]}")
                        #print(f"Precio compra {precioCompra[prod]}")
                        
                        #print(f"\nProducto a comprar {produ}")
                        #print(f"Cantidad a comprar {cantidadDelProd}")
                        
                        self.ingresoCompra = preciosVenta[prod] * cantidadDelProd
                        
                        #print(f"Se cobrará ${self.ingresoCompra}")
                        
                        self.gananciaDia+= self.ingresoCompra
                        
                        cantidadInv[prod] -= cantidadDelProd
                        
                        if cantidadInv[prod]<10:
                            self.gastosDia+=precioCompra[prod]*2
                            
                            cantidadInv[prod]+=4
                    
                        archivo2="./Datos/39TiendaInventarioCantidad.txt"
                        with open(archivo2, 'w') as g:
                            for updat in range(len(productosNombres)):
                                g.write(str(productosNombres[updat]) + "," + str(cantidadInv[updat]) +"\n")
                            
                        g.close()
            
            
            
            #self.esperarTiempo(1)
            
            #self.tiendaSuples=Label(ventana,image=suples1,bg="#D9D9D9",highlightthickness=0).place(x=1050,y=128) 
            
            
            #SI LA PERSONA ES USUARIO DEL GYM ENTRA AQUI
            if band==True and tieneSub==False:
                aleaSups=self.devuelveAleatorio()
                sub=self.devuelveValorTabla("3EscogerSuscripcionEspecifica.txt",aleaSups)
                #print(f"Aleatorio {aleaSups} devuelve suscripción {sub}")

                
                if sub=="Visita":
                    self.subDia+=1
                elif sub=="Semana":
                    self.subSemana+=1
                elif sub=="Mensualidad":
                    self.subMes+=1
                elif sub=="Trimestre":
                    self.subTrim+=1
                elif sub=="Anualidad":
                    self.subAnua+=1

                suscripciones = []
                precios = []
                
                with open("./Datos/35membresias.txt", 'r') as f:
                    for linea in f:
                        elementos = linea.strip().split(',')
                        if len(elementos) == 2:
                            producto = elementos[0].strip()
                            precio = elementos[1].strip()
                            suscripciones.append(producto)
                            p=float(precio)
                            precios.append(int(p))
                f.close()
                
                #print(f"Suscripciones {suscripciones}")
                #print(f"Precios {precios}")

                cobro=0
                for subsc in range(len(suscripciones)):
                    if sub==suscripciones[subsc]:
                        cobro=precios[subsc]
                
                #print(f"Escogió {sub}")
                #print(f"Pagará {cobro}")
                self.gananciaDia+=cobro
            
            if band==True:    
                #Prob escoger material para calentamiento
                aleaMaterialCalent=self.devuelveAleatorio()
                resu=self.devuelveValorTabla("14HerramientasCalentamiento.txt",aleaMaterialCalent)
                #print(f"Aleatorio {aleaMaterialCalent} material de calentamiento {resu}")
                
                #Prob de tardar un tiempo calentando
                aleaTiempoCalent=self.devuelveAleatorio()
                resu=self.devuelveValorTabla("13TardarTiempoCalentando.txt",aleaTiempoCalent)
                resu=int(resu)
                #print(f"Aleatorio {aleaTiempoCalent} tardará {resu} minutos calentantdo")
                
                self.tiempoPersona+=resu
                
                self.esperarTiempo(resu)
                

                #Pro de hacer cardio antes de entrenar
                aleaCardio=self.devuelveAleatorio()
                res=self.devuelveValorTabla("15IrCaridoAntesDeEntrenar.txt",aleaCardio)
                #print(f"Aleatorio {aleaCardio} devolvió {res} cardio")
                
                if res=="Si hace":
                    self.personasHacenCardio+=1
                    
                    #Prob de escoger una maquina del area de cardio
                    aleaCardio=self.devuelveAleatorio()
                    res=self.devuelveValorTabla("16EscogerMaquinaCardioParaCalentamiento.txt",aleaCardio)
                    #print(f"Aleatorio {aleaCardio} devolvió hará cardio en {res}")
                    
                    #Prob de tardar un tiempo calentando en cardio
                    aleaTiempoCal=self.devuelveAleatorio()
                    res=self.devuelveValorTabla("17TardarTiempoCalentandoEnCardio.txt",aleaTiempoCal)
                    res=int(res)
                    #print(f"Aleatorio {aleaCardio} durará {res} minutos")
                    
                    self.tiempoPersona+=res
                    
                    self.esperarTiempo(res)
                    
                elif res=="No hace":
                    self.personasNoHacenCardio+=1
                

                #Prob de entrenar en un area especifica
                aleaAreaEntrenar=self.devuelveAleatorio()
                resu=self.devuelveValorTabla("18EscogerAreaParaEntrenar.txt",aleaAreaEntrenar)
                #print(f"Aleatorio {aleaAreaEntrenar} devolvió que entrenará {resu}")
                
                areaEntrenar=resu
                
                if areaEntrenar=="Cardio":
                    self.personasEntrenaronCardio+=1
                elif areaEntrenar=="Pecho":
                    self.personasEntrenaronPecho+=1
                elif areaEntrenar=="Espalda":
                    self.personasEntrenaronEspalda+=1
                elif areaEntrenar=="Pierna":
                    self.personasEntrenaronPierna+=1
                elif areaEntrenar=="Pesas":
                    self.personasEntrenaronPesas+=1
                elif areaEntrenar=="Spinning":
                    self.personasEntrenaronSpinning+=1
                
                #Prob de hacer una cantidad de ejercicios
                aleaCantEjer=self.devuelveAleatorio()
                resu=self.devuelveValorTabla("19CantidadEjerciciosRutina.txt",aleaCantEjer)
                cantEjercicios=int(resu)
                #print(f"Aleatorio {aleaCantEjer} devolvió que hará {resu} ejercicios")
                
                
                #Prob de usar una cantidad de maquinas del area donde va a entrenar
                aleaCantMaq=self.devuelveAleatorio()
                result=self.devuelveValorTabla("20UsarCantidadDeMaquinas.txt",aleaCantMaq)
                cantMaquinas=int(result)
                #print(f"Aleatorio {aleaCantMaq} devolvió que usará {result} máquinas")
                
                if cantEjercicios<=cantMaquinas:
                    cantidad=cantEjercicios
                elif cantEjercicios>cantMaquinas:
                    cantidad=cantMaquinas
                
                if areaEntrenar=="Spinning":
                    cantidad=1
                    
                #print(f"Usará {cantidad} maquinas")
                     
                     
                for ejer in range(cantidad):
                    #Prob de usar una maquina de donde va a entrenar
                    
                    if areaEntrenar=="Cardio":
                        archi="16EscogerMaquinaCardioParaCalentamiento.txt"
                        
                    elif areaEntrenar=="Pecho":
                        archi="23PechoEscogerMaquina.txt"

                    elif areaEntrenar=="Espalda":
                        archi="24EspaldaEscogerMaquina.txt"
                        
                    elif areaEntrenar=="Pierna":
                        archi="25PiernaEscogerMaquina.txt"
                        
                    elif areaEntrenar=="Pesas":
                        archi="26PesasEscogerMaquina.txt"
                        
                    elif areaEntrenar=="Spinning":
                        pass
                    
                    
                    if not areaEntrenar=="Spinning":
                        aleaMaq=self.devuelveAleatorio()
                        resultado=self.devuelveValorTabla(archi,aleaMaq)
                        #print(f"Aleatorio {aleaCantMaq} devolvió que usará la máquina {resultado}")
                        
                    
                    #Prob de tardar un tiempo en la maquina
                    aleaTiempoMaq=self.devuelveAleatorio()
                    re=self.devuelveValorTabla("21TardarTiempoEnMaquina.txt",aleaTiempoMaq)
                    res=int(re)
                    #print(f"Aleatorio {aleaTiempoMaq} devolvió que tardará {res} minutos en la máquina")
                    
                    self.esperarTiempo(res)
                    
                    self.tiempoPersona+=res
                    
                    #Prob de que se lesione mientras hace el ejercicio
                    aleaSiLesiona=self.devuelveAleatorio()
                    lesion=self.devuelveValorTabla("29SeLesionahaciendoEjercicio.txt",aleaSiLesiona)
                    #print(f"Aleatorio {aleaSiLesiona} devolvió que la persona {lesion} ")
                
                    if lesion=="Se lesiona":
                        self.lesionadosDia+=1
                        
                        #Prob de requerir hospitalizacion
                        aleaHosp=self.devuelveAleatorio()
                        resultado=self.devuelveValorTabla("30RequiereHospitalizacion.txt",aleaHosp)
                        #print(f"Aleatorio {aleaHosp} devolvió que la persona {resultado} ")
                        
                        if resultado=="Requiere":
                            self.personasRequierHosp+=1
                            #Llama a la ambulancia
                            nombreGastos = []
                            precios = []
                            
                            with open("./Datos/36Gastos.txt", 'r') as f:
                                for linea in f:
                                    elementos = linea.strip().split(',')
                                    if len(elementos) == 2:
                                        producto = elementos[0].strip()
                                        precio = elementos[1].strip()
                                        nombreGastos.append(producto)
                                        p=float(precio)
                                        precios.append(int(p))
                            f.close()
                            
                            for i in range(len(nombreGastos)):
                                if nombreGastos[i]=="Ambulancia del lesionado":
                                    self.gastosDia+=precios[i]
                            
                            
                            self.img_ambulancia=Label(self.ventana,image=ambuIMG2,bg="#1D1F24",bd=0).place(x=912,y=22)
                            
                            self.esperarTiempo(2)
                            
                            self.img_ambulancia=Label(self.ventana,image=ambuIMG1,bg="#1D1F24",bd=0).place(x=912,y=22)
                            

                        else:
                            self.personasNoRequierHosp+=1
                            
                    else:
                        #Prob de ir al baño porque ya terminó el ejercicio
                        aleaBath=self.devuelveAleatorio()
                        resultado=self.devuelveValorTabla("27IrAlBañoAcabandoEjercicio.txt",aleaBath)
                        #print(f"Aleatorio {aleaBath} devolvió que la persona {resultado} al baño")
                        
                        if resultado=="Va":
                            #self.bath1=Label(ventana,image=img_bath2,bg="#D9D9D9",highlightthickness=0).place(x=680,y=606)
                            
                            #Prob de tardar un tiempo en el baño
                            aleaTiempoBath=self.devuelveAleatorio()
                            resultado=self.devuelveValorTabla("28TardarTiempoEnBaño.txt",aleaTiempoBath)
                            resultado=int(resultado)
                            #print(f"Aleatorio {aleaTiempoBath} devolvió que la persona tardará {resultado} minutos en el baño")
                        
                            self.esperarTiempo(resultado)
                            #self.bath1=Label(ventana,image=img_bath1,bg="#D9D9D9",highlightthickness=0).place(x=680,y=606)
                        
                            self.tiempoPersona+=resultado
             
                        #Prob de que se dañe la maquina
                        aleaDanMaq=self.devuelveAleatorio()
                        resultado=self.devuelveValorTabla("22MaquinaSeDañaONo.txt",aleaDanMaq)
                        #print(f"Aleatorio {aleaDanMaq} devolvió que la máquina {resultado}")
                
                        if resultado=="Se descompone":
                            self.maquinasAveriadasDia+=1
                                                     
                            nombreGastos = []
                            precios = []
                            
                            with open("./Datos/36Gastos.txt", 'r') as f:
                                for linea in f:
                                    elementos = linea.strip().split(',')
                                    if len(elementos) == 2:
                                        producto = elementos[0].strip()
                                        precio = elementos[1].strip()
                                        nombreGastos.append(producto)
                                        p=float(precio)
                                        precios.append(int(p))
                            f.close()                        

                            for i in range(len(nombreGastos)):
                                if nombreGastos[i]=="Reparar maquina":
                                    self.gastosDia+=precios[i]
                
                if not lesion=="Se lesiona":
                    #Prob de que se duche
                    aleaDucha=self.devuelveAleatorio()
                    resultado=self.devuelveValorTabla("31SeDuchaAlTerminar.txt",aleaDucha)
                    #print(f"Aleatorio {aleaDucha} devolvió que la persona {resultado}")    

                    if resultado=="Se ducha":
                        #self.ducha1=Label(ventana,image=img_ducha2,bg="#D9D9D9",highlightthickness=0).place(x=1216,y=608)
                        
                        
                        #Prob de tardar un tiempo duchandose
                        aleaTiDucha=self.devuelveAleatorio()
                        resultado=self.devuelveValorTabla("32TardarTiempoEnDucha.txt",aleaTiDucha)
                        resultado=int(resultado)
                        #print(f"Aleatorio {aleaTiDucha} devolvió que la persona durará {resultado} minutos en la ducha")
                        
                        self.esperarTiempo(resultado)
                        #self.ducha1=Label(ventana,image=img_ducha1,bg="#D9D9D9",highlightthickness=0).place(x=1216,y=608)
                        
                        self.tiempoPersona+=resultado
                        
                        #Prob de que use un banco saliendo de la ducha
                        aleaUsaBanco=self.devuelveAleatorio()
                        resultado=self.devuelveValorTabla("33UsaBancoAlSalirDucha.txt",aleaUsaBanco)
                        #print(f"Aleatorio {aleaUsaBanco} devolvió que la persona {resultado} un banco luego de ducha")
                        
                        if resultado=="Usa":
                            #self.banca1=Label(ventana,image=img_banco2,bg="#D9D9D9",highlightthickness=0).place(x=845,y=569)
                            
                            
                            #Prob de durar un tiempo en la banca
                            aleaTiBanca=self.devuelveAleatorio()
                            resultado=self.devuelveValorTabla("34TiempoEnBanca.txt",aleaTiBanca)
                            resultado=int(resultado)
                            #print(f"Aleatorio {aleaTiBanca} devolvió que la persona durará {resultado} minutos en la banca")
                            
                            self.esperarTiempo(resultado)
                            #self.banca1=Label(ventana,image=img_banco1,bg="#D9D9D9",highlightthickness=0).place(x=845,y=569)
                            
                            self.tiempoPersona+=resultado
        
            self.tiemposPersonas.append(self.tiempoPersona) #Se guarda el tiempo que duró la persona en el gimnasio
            
        nombreGastos = []
        precios = []    
        with open("./Datos/36Gastos.txt", 'r') as f:
            for linea in f:
                elementos = linea.strip().split(',')
                if len(elementos) == 2:
                    producto = elementos[0].strip()
                    precio = elementos[1].strip()
                    nombreGastos.append(producto)
                    p=float(precio)
                    precios.append(int(p))
        f.close()    
        
        ##print(nombreGastos)
        ##print(precios) 
        suma=0
        for j in range(len(precios)-2):
            suma+=precios[j]
        #print(f"Suma de gastos de servicios por dia ${suma}")
            
        for j in range(len(precios)-2):
            self.gastosDia+=precios[j]
        
        
        self.gananciaDia-=self.gastosDia
        
        self.dineroCaja+=self.gananciaDia
        
        cajaNombre = [] #Este dato no nos iteresa
        
        
        with open("./Datos/37Caja.txt", 'r') as f:
            for linea in f:
                elementos = linea.strip().split(',')
                if len(elementos) == 2:
                    nombre = elementos[0].strip()
                    dinero = elementos[1].strip()
                    cajaNombre.append(nombre)
        f.close()
        
        
        with open("./Datos/37Caja.txt", 'w') as cajaa:
            for j in range(len(cajaNombre)):
                cajaa.write(cajaNombre[j]+","+str(self.dineroCaja))
        cajaa.close()
        
        #print(f"Dinero en la caja ${self.dineroCaja}")
        
        self.gananciaDiaSim.append(self.gananciaDia)
        
        self.gananciasTotalesSim+=self.gananciaDia
        self.gastosTotalesSim+=self.gastosDia
        
        self.lesionadosCadaDia.append(self.lesionadosDia)
         
        self.maquinasAveriadasSim.append(self.maquinasAveriadasDia)
        
        self.tiemposPersonasSim.append(int(sum(self.tiemposPersonas)/len(self.tiemposPersonas)))
        
        #print("\n")
        
        
        
        global target_time
        # Esperar hasta que sea las 10:00:00 AM
        target_time = datetime.strptime("10:00:00 PM", "%I:%M:%S %p")
        while self.current_time < target_time:
            self.current_time += timedelta(seconds=1) * self.speed_factor
            self.reloj.config(text=self.current_time.strftime("%I:%M:%S %p"))
            if not self.velocidad=="Fast":
                time.sleep(1 // self.speed_factor)

        #print("Hora objetivo alcanzada")
    
        # Detener el reloj
        self.process_running = False
    
        #Si se pasó por minuos o segundos deja el reloj en la hora de final
        self.current_time = target_time
        self.reloj.config(text=self.current_time.strftime("%I:%M:%S %p"))

        # Esperar 2 segundos
        self.esperarTiempo(2)

        # Reiniciar el reloj
        self.current_time = self.start_time
        self.reloj.config(text=self.current_time.strftime("%I:%M:%S %p"))
        
        
        
        #print(f"************ TERMINA DIA {self.dia} ************")
        #print("\n")
        
        if self.dia<diasDeSimulacion:
            
            
            
            #print("\nVOLVERÁ A COMENZAR\n")
            self.esperarTiempo(2)
            self.simular(self.velocidad)
        else:
            def Fbtn3_raise(event):
                self.btnResultados.place(y=19)
            def Fbtn3_lower(event):
                self.btnResultados.place(y=22)
            
            
            #print("\nFIN DE LAS SIMULACIONES\n")
            btnStart=Button(ventana,image=startIMG1,command=lambda:self.inicia(self.velocidad),bd=0,bg="#1D1F24")
            btnStart.place(x=607,y=14)
            
            self.btnResultados=Button(ventana,image=resuIMG2,bd=0,bg="#1D1F24",highlightthickness=0,command=lambda:self.verResultados())
            self.btnResultados.place(x=1026,y=22)
            
            self.btnResultados.bind("<Enter>",Fbtn3_raise)
            self.btnResultados.bind("<Leave>",Fbtn3_lower)
    
    
    def simular(self,velocidad):
        self.dia+=1
        #print(f"************ DIA {self.dia} ************")
        
        #self.lblDia=Label(ventana,text=(f"DÍA {self.dia}"),font=("Helvetica", 24),bg="#1D1F24",bd=0,foreground="white")
        #self.lblDia.place(x=711,y=35)
        self.lblDia.config(text=(f"DÍA {self.dia}"))
        
        
        if velocidad == "Fast":
            self.speed_factor = 55
            self.vel = 80
        else:
            self.vel = 10
            self.speed_factor = 8
    
        # Iniciar el reloj
        self.process_running = True
        self.start_clock()

        # Ejecutar la función del proceso
        hiloSimulacion = threading.Thread(target=self.personasParaDia)
        hiloSimulacion.start()
    
    
    
    
    
   

def Simulacion(velocidad,root):
    #print(velocidad)
    
    
    
    global mainIMG,cerrarIMG,startIMG1,startIMG2,resuIMG1,resuIMG2,ambuIMG1,ambuIMG2,suples1,suples2
    
    mainIMG=PhotoImage(file="Imagenes/SimulacionIMG/base.png")
    cerrarIMG=PhotoImage(file="Imagenes/SimulacionIMG/cerrar.png")
    startIMG1=PhotoImage(file="Imagenes/SimulacionIMG/start.png")
    startIMG2=PhotoImage(file="Imagenes/SimulacionIMG/start2.png")
    resuIMG1=PhotoImage(file="Imagenes/SimulacionIMG/resultados1.png")
    resuIMG2=PhotoImage(file="Imagenes/SimulacionIMG/resultados2.png")    
    ambuIMG1=PhotoImage(file="Imagenes/SimulacionIMG/ambulancia1.png")
    ambuIMG2=PhotoImage(file="Imagenes/SimulacionIMG/ambulancia2.png")
    suples1=PhotoImage(file="Imagenes/SimulacionIMG/suplementos1.png")
    suples2=PhotoImage(file="Imagenes/SimulacionIMG/suplementos2.png")

    

    #IMAGENES CARDIO
    global img_cardioCaminadora1,img_cardioCaminadora2,img_cardioEliptica1,img_cardioEliptica2,img_cardioEscaladora1,img_cardioEscaladora2,img_cardioRemo1,img_cardioRemo2
    img_cardioCaminadora1=PhotoImage(file="Imagenes/SimulacionIMG/Cardio/caminadora1.png")
    img_cardioCaminadora2=PhotoImage(file="Imagenes/SimulacionIMG/Cardio/caminadora2.png")
    img_cardioEliptica1=PhotoImage(file="Imagenes/SimulacionIMG/Cardio/eliptica1.png")
    img_cardioEliptica2=PhotoImage(file="Imagenes/SimulacionIMG/Cardio/eliptica2.png")
    img_cardioEscaladora1=PhotoImage(file="Imagenes/SimulacionIMG/Cardio/escaladora1.png")
    img_cardioEscaladora2=PhotoImage(file="Imagenes/SimulacionIMG/Cardio/escaladora2.png")
    img_cardioRemo1=PhotoImage(file="Imagenes/SimulacionIMG/Cardio/remo1.png")
    img_cardioRemo2=PhotoImage(file="Imagenes/SimulacionIMG/Cardio/remo2.png")
    
    #IMAGENES CALENTAMIENTO
    global img_calentAlfombra1,img_calentAlfombra2,img_calentBanda1,img_calentBanda2,img_calentCinto1,img_calentCinto2,img_calentPelota1,img_calentPelota2
    img_calentAlfombra1=PhotoImage(file="Imagenes/SimulacionIMG/Calentamiento/alfombra1.png")
    img_calentAlfombra2=PhotoImage(file="Imagenes/SimulacionIMG/Calentamiento/alfombra2.png")
    img_calentBanda1=PhotoImage(file="Imagenes/SimulacionIMG/Calentamiento/banda1.png")
    img_calentBanda2=PhotoImage(file="Imagenes/SimulacionIMG/Calentamiento/banda2.png")
    img_calentCinto1=PhotoImage(file="Imagenes/SimulacionIMG/Calentamiento/cinturon1.png")
    img_calentCinto2=PhotoImage(file="Imagenes/SimulacionIMG/Calentamiento/cinturon2.png")
    img_calentPelota1=PhotoImage(file="Imagenes/SimulacionIMG/Calentamiento/pelota1.png")
    img_calentPelota2=PhotoImage(file="Imagenes/SimulacionIMG/Calentamiento/pelota2.png")

    #IMAGENES CASILLEROS
    global img_casillero1,img_casillero2
    img_casillero1=PhotoImage(file="Imagenes/SimulacionIMG/Casilleros/casillero1.png")
    img_casillero2=PhotoImage(file="Imagenes/SimulacionIMG/Casilleros/casillero2.png")
    
    #IMAGENES SPINNING
    global img_spinBici1,img_spinBici2
    img_spinBici1=PhotoImage(file="Imagenes/SimulacionIMG/Spinning/bicicleta1.png")
    img_spinBici2=PhotoImage(file="Imagenes/SimulacionIMG/Spinning/bicicleta2.png")
    
    #IMAGENES ESPALDA
    global img_EspalBarra1,img_EspalBarra2,img_EspalDominada1,img_EspalDominada2,img_EspalDorsadera1,img_EspalDorsadera2
    global img_EspalPolAlta1,img_EspalPolAlta2,img_EspalPolBaja1,img_EspalPolBaja2,img_EspalRemo1,img_EspalRemo2
    img_EspalBarra1=PhotoImage(file="Imagenes/SimulacionIMG/Espalda/barra1.png")
    img_EspalBarra2=PhotoImage(file="Imagenes/SimulacionIMG/Espalda/barra2.png")
    img_EspalDominada1=PhotoImage(file="Imagenes/SimulacionIMG/Espalda/dominada1.png")
    img_EspalDominada2=PhotoImage(file="Imagenes/SimulacionIMG/Espalda/dominada2.png")
    img_EspalDorsadera1=PhotoImage(file="Imagenes/SimulacionIMG/Espalda/dorsadera1.png")
    img_EspalDorsadera2=PhotoImage(file="Imagenes/SimulacionIMG/Espalda/dorsadera2.png")
    img_EspalPolAlta1=PhotoImage(file="Imagenes/SimulacionIMG/Espalda/poleaalta1.png")
    img_EspalPolAlta2=PhotoImage(file="Imagenes/SimulacionIMG/Espalda/poleaalta2.png")
    img_EspalPolBaja1=PhotoImage(file="Imagenes/SimulacionIMG/Espalda/poleabaja1.png")
    img_EspalPolBaja2=PhotoImage(file="Imagenes/SimulacionIMG/Espalda/poleabaja2.png")
    img_EspalRemo1=PhotoImage(file="Imagenes/SimulacionIMG/Espalda/remo1.png")
    img_EspalRemo2=PhotoImage(file="Imagenes/SimulacionIMG/Espalda/remo2.png")

    #IMAGENES HIGIENE
    global img_banco1,img_banco2,img_bath1,img_bath2,img_ducha1,img_ducha2
    img_banco1=PhotoImage(file="Imagenes/SimulacionIMG/Higiene/banco1.png")
    img_banco2=PhotoImage(file="Imagenes/SimulacionIMG/Higiene/banco2.png")
    img_bath1=PhotoImage(file="Imagenes/SimulacionIMG/Higiene/baño1.png")
    img_bath2=PhotoImage(file="Imagenes/SimulacionIMG/Higiene/baño2.png")
    img_ducha1=PhotoImage(file="Imagenes/SimulacionIMG/Higiene/ducha1.png")
    img_ducha2=PhotoImage(file="Imagenes/SimulacionIMG/Higiene/ducha2.png")

    #IMAGENES PECHO
    global img_PechoAperturas1,img_PechoAperturas2,img_PechoMariposas1,img_PechoMariposas2,img_PechoPolea1,img_PechoPolea2
    global img_PechoPressB1,img_PechoPressB2,img_PechoPressInc1,img_PechoPressInc2
    img_PechoAperturas1=PhotoImage(file="Imagenes/SimulacionIMG/Pecho/aperturas1.png")
    img_PechoAperturas2=PhotoImage(file="Imagenes/SimulacionIMG/Pecho/aperturas2.png")
    img_PechoMariposas1=PhotoImage(file="Imagenes/SimulacionIMG/Pecho/mariposas1.png")
    img_PechoMariposas2=PhotoImage(file="Imagenes/SimulacionIMG/Pecho/mariposas2.png")
    img_PechoPolea1=PhotoImage(file="Imagenes/SimulacionIMG/Pecho/polea1.png")
    img_PechoPolea2=PhotoImage(file="Imagenes/SimulacionIMG/Pecho/polea2.png")
    img_PechoPressB1=PhotoImage(file="Imagenes/SimulacionIMG/Pecho/pressbanca1.png")
    img_PechoPressB2=PhotoImage(file="Imagenes/SimulacionIMG/Pecho/pressbanca2.png")
    img_PechoPressInc1=PhotoImage(file="Imagenes/SimulacionIMG/Pecho/pressInclinado1.png")
    img_PechoPressInc2=PhotoImage(file="Imagenes/SimulacionIMG/Pecho/pressInclinado2.png")

    #IMAGENES PESAS
    global img_PesasBarraP1,img_PesasBarraP2,img_PesasBarraZ1,img_PesasBarraZ2,img_PesasPesa1,img_PesasPesa2,img_PesasPesaG1,img_PesasPesaG2
    img_PesasBarraP1=PhotoImage(file="Imagenes/SimulacionIMG/Pesas/barraplana1.png")
    img_PesasBarraP2=PhotoImage(file="Imagenes/SimulacionIMG/Pesas/barraplana2.png")
    img_PesasBarraZ1=PhotoImage(file="Imagenes/SimulacionIMG/Pesas/barraz1.png")
    img_PesasBarraZ2=PhotoImage(file="Imagenes/SimulacionIMG/Pesas/barraz2.png")
    img_PesasPesa1=PhotoImage(file="Imagenes/SimulacionIMG/Pesas/pesa1.png")
    img_PesasPesa2=PhotoImage(file="Imagenes/SimulacionIMG/Pesas/pesa2.png")
    img_PesasPesaG1=PhotoImage(file="Imagenes/SimulacionIMG/Pesas/pesaG1.png")
    img_PesasPesaG2=PhotoImage(file="Imagenes/SimulacionIMG/Pesas/pesaG2.png")

    #IMAGENES PIERNA
    global img_PiernaBarra1,img_PiernaBarra2,img_PiernaCuad1,img_PiernaCuad2,img_PiernaFerm1,img_PiernaFerm2
    global img_PiernaPant1,img_PiernaPant2,img_PiernaPrensa1,img_PiernaPrensa2,img_PiernaRackS,img_PiernaSentadillas,img_PiernaSmith
    img_PiernaBarra1=PhotoImage(file="Imagenes/SimulacionIMG/Pierna/barra1.png")
    img_PiernaBarra2=PhotoImage(file="Imagenes/SimulacionIMG/Pierna/barra2.png")
    img_PiernaCuad1=PhotoImage(file="Imagenes/SimulacionIMG/Pierna/cuadriceps1.png")
    img_PiernaCuad2=PhotoImage(file="Imagenes/SimulacionIMG/Pierna/cuadriceps2.png")
    img_PiernaFerm1=PhotoImage(file="Imagenes/SimulacionIMG/Pierna/fermoral1.png")
    img_PiernaFerm2=PhotoImage(file="Imagenes/SimulacionIMG/Pierna/fermoral2.png")
    img_PiernaPant1=PhotoImage(file="Imagenes/SimulacionIMG/Pierna/pantorrilla1.png")
    img_PiernaPant2=PhotoImage(file="Imagenes/SimulacionIMG/Pierna/pantorrilla2.png")
    img_PiernaPrensa1=PhotoImage(file="Imagenes/SimulacionIMG/Pierna/prensa1.png")
    img_PiernaPrensa2=PhotoImage(file="Imagenes/SimulacionIMG/Pierna/prensa2.png")
    img_PiernaRackS=PhotoImage(file="Imagenes/SimulacionIMG/Pierna/racksentadilla.png")
    img_PiernaSentadillas=PhotoImage(file="Imagenes/SimulacionIMG/Pierna/sentadillas.png")
    img_PiernaSmith=PhotoImage(file="Imagenes/SimulacionIMG/Pierna/smithsentadilla.png")
    
    
    SimulacionProceso(velocidad,root)
    

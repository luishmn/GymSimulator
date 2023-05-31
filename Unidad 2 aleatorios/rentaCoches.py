from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import random

class Renta:
    
    def simular(self,root):
        win=Toplevel(root)
        win.title("SIMULACIÓN DE RENTA DE COCHES")
        win.geometry("700x350")
        win.resizable(width=False,height=False)

        self.abono=0
        self.gananciasTotales=0
        #print(f"Deuda {deuda}\n")
        
        self.diaCompletaDeuda=0
        
        self.rangoInCantAuto=[0,0.1,0.2,0.45,0.75]
        self.rangoFinCantAuto=[0.1,0.2,0.45,0.75,1]
        self.cantAutos=[0,1,2,3,4]
        
        self.rangoInDias=[0,0.4,0.75,0.9]
        self.rangoFinDias=[0.4,0.75,0.9,1]
        self.nDiasRent=[1,2,3,4]
        
        
        autC=IntVar()
        autC.set("")
        simm=IntVar()
        simm.set("")
    
        def proceso():
            scrollProcess=Scrollbar(win)
            ListProceso=Listbox(win,yscrollcommand=scrollProcess.set,width=65,height=18)
            
            
            
            
            
            aleas=[]
            archivo=open("aleatorios.txt","r")
            for i in archivo:
                aleas.append(float(i))
            #print(aleas)
            if len(aleas)==0:
                messagebox.showinfo("Error","Genere aleatorios para que\nel ejercicio pueda ser ejecutado")
                win.destroy()
            else:
        
                sim=simm.get()
                autComprados=autC.get()    
                autosDisponibles=autComprados
                diasRegreso=[]
                self.deuda=400000*autComprados
                
                for i in range(sim):
                    
                    gastosDia=0
                    gananciaDia=0
                    
                    band=True
                    for l in range(len(diasRegreso)):
                        if i==diasRegreso[l]:
                            autosDisponibles+=1
                            diasRegreso[l]=0
                    ListProceso.insert(END,f"Día {i+1} autos disponibles {autosDisponibles}")
                    
                    alea=aleas[random.randint(0,len(aleas)-1)] #***************************
                    for j in range(len(self.cantAutos)):
                        if alea>=self.rangoInCantAuto[j] and alea<=self.rangoFinCantAuto[j]:
                            
                            cantidad=self.cantAutos[j]
                            costoNoDisponible=0
                            if autosDisponibles>=cantidad:
                                autosDisponibles=autosDisponibles-cantidad
                                ListProceso.insert(END,f"Día {i+1} renta {cantidad} autos")
                    
                            else:
                                if autosDisponibles==0:
                                    band=False
                                else:
                                    Noalcanzables=cantidad-autosDisponibles
                                    cantidad=cantidad-Noalcanzables
                                    costoNoDisponible=200*Noalcanzables
                                    gastosDia=gastosDia+costoNoDisponible
                                    
                                    ListProceso.insert(END,f"Día {i+1} renta {cantidad} autos")
                                    
                    if band==True:            
                        for o in range(cantidad):
                            alea2=aleas[random.randint(0,len(aleas)-1)] #****************
                            for k in range(len(self.nDiasRent)):
                                if alea2>=self.rangoInDias[k] and alea2<=self.rangoFinDias[k]:
                                    dias=self.nDiasRent[k]
                                    diasRegreso.append(i+dias)
                                    ListProceso.insert(END,f"Auto {o+1} se renta {dias} días")


                    ListProceso.insert(END,f"No disponibles ${costoNoDisponible}")
                    cochesRentados=350*cantidad
                    gananciaDia=gananciaDia+cochesRentados
                    ListProceso.insert(END,f"Rentas ${cochesRentados}")

                    oscio=autosDisponibles*50
                    gastosDia=gastosDia+oscio
                    ListProceso.insert(END,f"Oscio ${oscio}")
                    
                    cochesGastos=210*cantidad
                    ListProceso.insert(END,f"Gastos coches ${cochesGastos}")
                    
                    ListProceso.insert(END,f"Ingresos {gananciaDia}")
                    ListProceso.insert(END,f"Gastos ${gastosDia}")
                    
                    gastosDia=gastosDia+cochesGastos
                    gananciaDia=gananciaDia-gastosDia
                    
                    
                    ListProceso.insert(END,f"Ganancia día {i+1} ${gananciaDia} gastos ${gastosDia} ")
                    
                    self.abono=self.abono+(gananciaDia*0.70)
                    self.gananciasTotales=self.gananciasTotales+(gananciaDia*0.30)
                    
                    ListProceso.insert(END,f"Autos disponibles {autosDisponibles}\n")        
                    ListProceso.insert(END,"")                
                    if self.abono>=self.deuda:
                        self.diaCompletaDeuda=i+1

                ListProceso.insert(END,f"\nCon {autComprados} autos y una simulación de {sim} días")
                ListProceso.insert(END,f"Ganancias totales son ${self.gananciasTotales}")
                ListProceso.insert(END,f"Abono es ${self.abono}")
                if self.diaCompletaDeuda!=0:
                    ListProceso.insert(END,f"La deuda se compléto el día {self.diaCompletaDeuda}")
                
            
            ListProceso.place(x=230,y=30)
            scrollProcess.config(command=ListProceso.yview)
            scrollProcess.pack(side=RIGHT,fill=Y)#place(x=630,y=30)
            
        def salir():
            win.destroy()
        Label(win,text="Días a simular",font=12).place(x=50,y=30)
        Entry(win,textvariable=simm).place(x=50,y=50)
        Label(win,text="Autos comprados",font=12).place(x=50,y=70)
        Entry(win,textvariable=autC).place(x=50,y=90)
        Button(win,text="Comenzar",font=12,command=lambda:proceso()).place(x=50,y=110)
        Button(win,text="Salir",font=12,command=lambda:salir()).place(x=50,y=150)
        #sim=int(input("Cantidad de simulaciones: "))
        #autComprados=int(input("Autos comprados: "))
        win.mainloop()
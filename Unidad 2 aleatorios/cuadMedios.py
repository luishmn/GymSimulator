from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import random

class CuadradosMedios:
    
    def generar(self,root):
        win=Toplevel(root)
        win.title("Cuadrados Medios")
        win.geometry("600x400")
        win.config(bg="gray")
        win.resizable(width=False,height=False)
        
        
        def llenadoGeneracion(sem,cant):
            scrollbar = Scrollbar(win)
            listbox=Listbox(win,yscrollcommand=scrollbar.set)
            self.lista=[]
            self.lista2=[]
            #self.band=True
            semstr=str(sem)
            digi=len(semstr)
            if digi%2!=0:
                messagebox.showerror("SEMILLA INVÁLIDA","Introduzca una semilla de cantidad de dígitos (2 o 4).")
                win.destroy()
            else:
                while len(self.lista)!=cant:
                    d2=digi*2
                    sem=int(sem)**2
                    #listbox.insert(END,f"Semilla **2: {sem}")
                    #print(f"Semilla **2: {sem}")
                    tamSem2=len(str(sem))
                    if tamSem2<d2:
                        sem=str(sem)
                        while len(sem)<d2:
                            sem="0"+sem
                        listbox.insert(END,f"Semilla corregida: {sem}")
                        #print(f"Semilla corregida: {sem}")
                    
                    numNuevo=str(sem)
                    centIni=int(d2/4)
                    centFin=int(centIni+(d2/2))
                    numNuevo=numNuevo[centIni:centFin]
                    listbox.insert(END,f"Nuevo número: {numNuevo}")
                    #print(f"Nuevo número: {numNuevo}")
                    
                    if numNuevo[0]=="0":
                        
                        def nuevaSemilla():    
                            #sem=int(input("Introduzca la semilla (n dígitos par): "))
                            sem=random.randint(1000,9999)
                            listbox.insert(END,f"NUEVA SEMILLA {sem}")
                            #print(f"NUEVA SEMILLA {sem}")
                            semstr=str(sem)
                            digi=len(semstr)
                            if digi % 2 !=0 :
                                #messagebox.showinfo("SEMILLA INVÁLIDA","Introduzca una semilla de cantidad de dígitos par.")
                                nuevaSemilla()
                        nuevaSemilla()
                        
                    else:
                        sem=int(numNuevo)
                        self.lista.append(sem)
                        pseu=int("1"+("0"*digi))
                        self.lista2.append(round((sem/pseu),5))
                        
            Label(win,text="Proceso",font=11,bg="gray",foreground="white").place(x=260,y=45)
            listbox.place(x=260,y=70)  
            scrollbar.config(command=listbox.yview,width=20)         
            scrollbar.place(x=380,y=7)
            #return self.lista2
            archivo=open("aleatorios.txt","w")
            for i in self.lista2:
                print(i,file=archivo)
            archivo.close()
            
            scrollbar2 = Scrollbar(win)
            listbox2=Listbox(win,yscrollcommand=scrollbar2.set)
            archivo=open("aleatorios.txt","r")
            for i in archivo:
                listbox2.insert(END,i)
            archivo.close()
            Label(win,text="Pseudoaleatorios",font=11,bg="gray",foreground="white").place(x=400,y=45)
            listbox2.place(x=420,y=70)  
            scrollbar2.config(command=listbox2.yview,width=20)         
            scrollbar2.place(x=540,y=70)
            
            
            
        
        cantt=IntVar()
        semilla=IntVar()
        
        Label(win,text="Cantidad de números",bg="gray",foreground="white").place(x=50,y=50)
        Entry(win,textvariable=cantt).place(x=50,y=70)
        
        def semillaEntrada():
            Frame(win,bg="gray",width=210,height=75).place(x=20,y=91)
            def recoge():
                self.semi=semilla.get()
                self.canti=cantt.get()
                llenadoGeneracion(self.semi,self.canti)
                
            Label(win,text="Semilla 4 dígitos o 2",bg="gray",foreground="white").place(x=50,y=90)
            Entry(win,textvariable=semilla).place(x=50,y=110)
            Button(win,text="Guardar",command=lambda:recoge()).place(x=50,y=130)
        
        def semillaAlea():
            self.semi=random.randint(1000,9999)
            self.canti=cantt.get()
            llenadoGeneracion(self.semi,self.canti)
        
        def salir():
            win.destroy()
           
        Button(win,text="Semilla manual",command=lambda:semillaEntrada()).place(x=20,y=110)
        Button(win,text="Semilla aleatoria",command=lambda:semillaAlea()).place(x=130,y=110)
        Button(win,text="Salir",command=lambda:salir()).place(x=50,y=170)
        #int(input("Cantidad de números: "))
        #int(input("Introduzca la semilla (n dígitos par): "))
        #numeros
        
        win.mainloop()


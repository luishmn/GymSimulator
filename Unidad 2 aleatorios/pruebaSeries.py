from tkinter import messagebox
from tkinter import *
#from cuadMedios import CuadradosMedios
import random
from random import uniform

class PruebaDeSeries:
    def prueba(self,root):
        win=Toplevel(root)
        win.title("PRUEBA DE SERIES")
        win.geometry("750x450")
        win.config(bg="gray")
        win.resizable(width=False,height=False)
        
        
        
        global n, alfa
        
        nn=IntVar()
        alfaVar=IntVar()
        nn.set("")
        alfaVar.set("")
        
        def probar(op):
            n=nn.get()
            alfa=alfaVar.get()
            
            numeros=[]
            
            def proceso():
                #print("\n")
                
                #NÚMEROS ALEATORIOS EN LISTBOX
                Label(win,text="Aleatorios",bg="gray",foreground="white").place(x=230,y=50)
                scrollAleas=Scrollbar(win)
                numAleas=Listbox(win,yscrollcommand=scrollAleas.set)
                
                for i in numeros:
                    numAleas.insert(END,i)
                
                numAleas.place(x=230,y=70)
                scrollAleas.config(command=numAleas.yview)         
                scrollAleas.place(x=355,y=70)
            
                
                
                
                IntervalosX=[]
                IntervalosY=[]
                inte=(1/n)
                inter=0
                while inter<=1:
                    IntervalosX.append(inter)
                    IntervalosY.append(inter)
                    inter=inter+inte
                #print(IntervalosX)
                
                cuadroInter=[]
                for i in range(n+1):
                    cuadroInter.append([0]*(n+1))
                
                for i in range(n+1):
                    cuadroInter[0][i]=round(IntervalosX[i],4)
                    cuadroInter[i][0]=round(IntervalosX[i],4)
                
               
                #PAREJAS EN LISTBOX
                Label(win,text="Parejas",bg="gray",foreground="white").place(x=400,y=50)
                scrollParejas=Scrollbar(win)
                ListParejas=Listbox(win,yscrollcommand=scrollParejas.set,width=25)
                
                p1=[]
                p2=[]
                parejas=0
                print("\n")
                for i in range(N-1):
                    p1.append(numeros[i])
                    p2.append(numeros[i+1])
                    parejas=parejas+1
                for i in range(len(p1)):
                    ListParejas.insert(END,(f"Pareja {i+1} ({p1[i]} , {p2[i]})"))
                #print("\n")
                ListParejas.place(x=400,y=70)
                scrollParejas.config(command=ListParejas.yview)         
                scrollParejas.place(x=555,y=70)
                
                
                #Identifica el intérvalo de la pareja en el cuadrante
                Label(win,text="Posiciones",bg="gray",foreground="white").place(x=230,y=240)
                scrollPos=Scrollbar(win)
                ListPos=Listbox(win,yscrollcommand=scrollPos.set)
                
                for k in range(parejas):
                    
                    for i in range(1,n+1):
                        for j in range(1,n+1):
                            if (p1[k]>=cuadroInter[0][j-1] and p1[k]<=cuadroInter[0][j]) and (p2[k]>=cuadroInter[i-1][0] and p2[k]<=cuadroInter[i][0]):
                                ListPos.insert(END,(f"Pareja {k+1} en pos {j},{i}"))
                                cuadroInter[i][j]=cuadroInter[i][j]+1
                #print("\n")
                ListPos.place(x=230,y=260)
                scrollPos.config(command=ListPos.yview)         
                scrollPos.place(x=355,y=260)
                
                
                Label(win,text="Cuadrante",bg="gray",foreground="white").place(x=400,y=240)
                scrollCuadY=Scrollbar(win)
                scrollCuadX=Scrollbar(win)
                Cuad=Listbox(win,yscrollcommand=scrollCuadY.set,xscrollcommand=scrollCuadX.set,height=7)
                Cuad.insert(END,("Y+ Abajo | X+ Derecha"))
                b=""
                for i in range(n+1):
                    for j in range(n+1):
                        b+=str(cuadroInter[i][j])+"         "
                    Cuad.insert(END,b)
                    b=""
                #print("\n")
                Cuad.place(x=400,y=260)
                scrollCuadY.config(command=Cuad.yview)         
                scrollCuadY.place(x=525,y=260)
                scrollCuadX.config(command=Cuad.xview,orient=HORIZONTAL)         
                scrollCuadX.place(x=400,y=380)
                
                
                #Guarda las cantidades encontradas en el cuadrante
                cantidades=[]
                for i in range(1,n+1):
                    for j in range(1,n+1):
                        if cuadroInter[i][j]!=0:
                            cantidades.append(cuadroInter[i][j])
                #print("Cantidades: ",cantidades)
                
                #Guarda las cantidades del cuadrante sin repetirlas
                cantidadesUnicas=[]
                c=0
                while c<len(cantidades):
                    band=False
                    for i in range(len(cantidadesUnicas)):
                        if cantidadesUnicas[i]==cantidades[c]:        
                            band=True
                    if band==False:
                        cantidadesUnicas.append(cantidades[c])
                    c=c+1
                #print(f"Cantidades únicas: {cantidadesUnicas} ")
                
                #Calcula cuantas veces apareció cada cantidad
                vecesCantUnicas=[]
                for i in range(len(cantidadesUnicas)):
                    vecesCantUnicas.append(0)
                c=0
                while c<len(cantidadesUnicas):
                    for i in range(1,n+1):
                        for j in range(1,n+1):
                            if cuadroInter[i][j]==cantidadesUnicas[c]:
                                vecesCantUnicas[c]=vecesCantUnicas[c]+1
                    c=c+1
                #print(f"Veces {vecesCantUnicas}")
                
                
                #CALCULO DE FEi
                Label(win,text="FEi",bg="gray",foreground="white").place(x=600,y=120)
                scrollFEi=Scrollbar(win)
                procesoFEi=Listbox(win,yscrollcommand=scrollFEi.set)
                
                FEi=round(((N-1)/(n**2)),2)
                X02=round((n**2)/(N-1),2)
                procesoFEi.insert(END,(f"n^2/N-1 = {X02}"))
                procesoFEi.insert(END,(f"FEi: {FEi}"))
                
                pos=0    
                suma=0
                while pos<len(cantidadesUnicas):
                    suma=suma+(vecesCantUnicas[pos]*((cantidadesUnicas[pos]-FEi)**2))        
                    procesoFEi.insert(END,(f"{vecesCantUnicas[pos]} * ({cantidadesUnicas[pos]} - {FEi})**2 +"))
                    pos=pos+1
                procesoFEi.insert(END,(f"Suma: {suma}"))
                XX02=round((X02*suma),2)
                procesoFEi.insert(END,(f"X0^2={X02}[{suma}]="))
                procesoFEi.insert(END,XX02)

                procesoFEi.place(x=600,y=140)
                scrollFEi.config(command=procesoFEi.yview)
                scrollFEi.place(x=725,y=140)


                x22=DoubleVar()
                x22.set("")

                def compruebaX2():
                    x2=x22.get()
                    Label(win,text=f"{XX02} < {x2} ? ",bg="gray",foreground="white").place(x=600,y=370)
                    if XX02 < x2:
                        #print("Se acepta H0")
                        messagebox.showinfo("Aleatorios buenos","Se acepta H0")
                        archivo=open("aleatorios.txt","w")
                        for i in numeros:
                            print(i,file=archivo)
                        archivo.close()
                        win.destroy()
                    else:
                        #print("Se rechaza H0")
                        messagebox.showinfo("Aleatorios malos","Se rechaza H0\nVuelva a generar los números")
                        win.destroy()
                    #print("**** FIN DE LA PRUEBA ****")

                Label(win,text=f"Tabla X^2 ({round((alfa/100),2)},{((n-1)**2)}): ",bg="gray",foreground="white").place(x=600,y=310)
                Entry(win,textvariable=x22).place(x=600,y=330)
                Button(win,text="Comprobar",command=lambda:compruebaX2()).place(x=600,y=350)

                
            
            
            if op=="arch":
                global N
                archivo=open("aleatorios.txt","r")
                for i in archivo:
                    numeros.append(float(i))                
                N=len(numeros)
                if N==0:
                    messagebox.showinfo("Error","Primero genera números\npara el archivo")
                    win.destroy()
                else:
                    proceso()
            
            elif op=="aleas":
                
                NN=IntVar()
                NN.set("")
                def rellenar():
                    global N
                    N=NN.get()
                    for i in range(N):
                        numeros.append(round(random.uniform(0,1),5))
                    proceso()
                Label(win,text="N números",bg="gray",foreground="white").place(x=30,y=190)
                Entry(win,textvariable=NN).place(x=30,y=210)
                Button(win,text="Guardar",command=lambda:rellenar()).place(x=30,y=230)
                
                
    
            
            
            
                
            
        def salir():
            win.destroy()    
        
        
        Label(win,text="Número de intérvalos (n)",bg="gray",foreground="white").place(x=30,y=50)
        Entry(win,textvariable=nn).place(x=30,y=70)
        Label(win,text="Valor de alfa",bg="gray",foreground="white").place(x=30,y=90)
        Entry(win,textvariable=alfaVar).place(x=30,y=110)
        
        Button(win,text="Números aleatorios",command=lambda:probar("aleas")).place(x=30,y=135)
        Button(win,text="Números de archivo",command=lambda:probar("arch")).place(x=30,y=160)
        Button(win,text="Salir",command=lambda:salir()).place(x=30,y=190)
        #n=int(input("Número de intérvalos: "))
        #alfa=int(input("Porcentaje de error %: "))
        
        
        
        win.mainloop()
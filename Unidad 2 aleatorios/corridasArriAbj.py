from tkinter import *
from tkinter import messagebox
from random import uniform
import random

class CorridasArribaAbajo:
    def prueba(self,root):
        win=Toplevel(root)
        win.title("CORRIDAS ARRIBA Y ABAJO DEL PROMEDIO")
        win.geometry("750x450")
        win.config(bg="gray")
        win.resizable(width=False,height=False)
        
        
        
        global n, alfa
        nn=IntVar()
        alfaVar=IntVar()
        nn.set("")
        alfaVar.set("")
        
        
        def probar(op):
            self.n=nn.get()
            self.alfa=alfaVar.get()
            self.aleas=[]
            
            
            def proceso():
                
                
                #ALEATORIOS EN LISTBOX
                Label(win,text="Aleatorios",bg="gray",foreground="white").place(x=230,y=50)
                scrollAleas=Scrollbar(win)
                numAleas=Listbox(win,yscrollcommand=scrollAleas.set)
                
                for i in self.aleas:
                    numAleas.insert(END,i)
                
                numAleas.place(x=230,y=70)
                scrollAleas.config(command=numAleas.yview)         
                scrollAleas.place(x=355,y=70)
                
                
                #CICLO QUE CALCULA LOS CEROS Y UNOS
                Label(win,text="Unos y Ceros",bg="gray",foreground="white").place(x=400,y=50)
                scrollUnosCeros=Scrollbar(win)
                UnosCeros=Listbox(win,yscrollcommand=scrollUnosCeros.set)
                
                resultados=[]
                size=len(self.aleas)
                for i in range(size-1):
                    if self.aleas[i] < self.aleas[i+1]:
                        resultados.append(0)
                    else:
                        resultados.append(1)
                #print(resultados,"\n")
                for i in resultados:
                    UnosCeros.insert(END,i)
                UnosCeros.place(x=400,y=70)
                scrollUnosCeros.config(command=UnosCeros.yview)         
                scrollUnosCeros.place(x=525,y=70)
                    
                
                valores_n=[]
                for i in range(self.n):
                    valores_n.append(i+1)
                
                cantidades_n=[]
                for i in range(len(valores_n)):
                    cantidades_n.append(0)
                    
                
                #CICLO PARA CALCULAR LOS HUECOS 
                cant=[]
                rep=1
                for i in range(0,len(resultados)):
                    if i==len(resultados)-1:
                        cant.append(rep)
                    elif resultados[i]==resultados[i+1]:
                        rep=rep+1
                    else:
                        cant.append(rep)
                        rep=1
                #print(cant)
                
                
                #CICLO PARA CALCULAR LAS CANTIDADES DE HUECOS
                band=True
                for j in range(len(valores_n)):
                    rep=1
                    for i in range(0,len(resultados)):
                        if i==len(resultados)-1:
                            if (j==len(valores_n)-1 and rep>=valores_n[j]) or rep==valores_n[j]:
                                cantidades_n[j]=cantidades_n[j]+1                
                        elif resultados[i]==resultados[i+1]:
                            rep=rep+1
                        else:
                            if (j==len(valores_n)-1 and rep>=valores_n[j]) or rep==valores_n[j]:
                                cantidades_n[j]=cantidades_n[j]+1
                            rep=1
                            
                #IMPRIME LOS VALORES DE 1 A n Y SUS CANTIDADES
                Label(win,text="Resultados",bg="gray",foreground="white").place(x=230,y=240)
                scrollResu=Scrollbar(win)
                ListResu=Listbox(win,yscrollcommand=scrollResu.set,width=50)
                
                for i in range(len(valores_n)):
                    ListResu.insert(END,(f"{valores_n[i]}: {cantidades_n[i]}"))
                    
                #CALCULO DE FEi
                def factorial(n):
                    m=n
                    for i in range(1,n):
                        m=m*i
                    return m 
                
                FEi=[]
                for i in range(1,self.n+1):
                    res=(((i**2)+(3*i)+1)*self.N)-((i**3)-3*(i**2)-i-4)
                    res=round(res/factorial(i+3),3)
                    ListResu.insert(END,(f"FE{i}= {res}"))
                    FEi.append(res)
                
                #SUMA DE FEi
                suma=0
                for i in range(len(FEi)):
                    suma=suma+FEi[i]
                ListResu.insert(END,(f"Suma de FEi {suma}"))
                
                #EL TOTAL DE LAS CORRIDAS
                ListResu.insert(END,(f"Total de corridas {(2*self.N - 1)/3}"))
                
                #CALCULO DE H0
                ListResu.insert(END,"H0=")
                h0=0
                for i in range(len(cantidades_n)):
                    h0=h0+((cantidades_n[i])-(FEi[i]))**2 /FEi[i]
                    ListResu.insert(END,f"(({cantidades_n[i]})-({FEi[i]}))**2 / {FEi[i]} = {h0}")
                ListResu.insert(END,h0)
                
                ListResu.place(x=230,y=260)
                scrollResu.config(command=ListResu.yview)         
                scrollResu.place(x=540,y=260)
                
                
                x22=DoubleVar()
                x22.set("")

                def compruebaX2():
                    x2=x22.get()
                    Label(win,text=f"{h0} < {x2} ? ",bg="gray",foreground="white").place(x=600,y=370)
                    if h0 < x2:
                        #print("Se acepta H0")
                        messagebox.showinfo("Aleatorios buenos","Se acepta H0")
                        archivo=open("aleatorios.txt","w")
                        for i in self.aleas:
                            print(i,file=archivo)
                        archivo.close()
                        win.destroy()
                    else:
                        #print("Se rechaza H0")
                        messagebox.showinfo("Aleatorios malos","Se rechaza H0\nVuelva a generar los números")
                        win.destroy()
                    #print("**** FIN DE LA PRUEBA ****")

                Label(win,text=f"Tabla X^2 ({round((self.alfa/100),2)},{((self.n-1)**2)}): ",bg="gray",foreground="white").place(x=600,y=310)
                Entry(win,textvariable=x22).place(x=600,y=330)
                Button(win,text="Comprobar",command=lambda:compruebaX2()).place(x=600,y=350)
                

            
            if op=="arch":
                
                archivo=open("aleatorios.txt","r")
                for i in archivo:
                    self.aleas.append(float(i))                
                self.N=len(self.aleas)
                if self.N==0:
                    messagebox.showinfo("Error","Primero genera números\npara el archivo")
                    win.destroy()
                else:
                    proceso() 
            
            elif op=="aleas":
                
                NN=IntVar()
                NN.set("")
                def rellenar():
                    
                    self.N=NN.get()
                    for i in range(self.N):
                        self.aleas.append(round(random.uniform(0,1),5))
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
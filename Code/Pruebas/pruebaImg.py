import tkinter as tk
import time
ventana = tk.Tk()
ventana.geometry("500x350")
imagen=tk.PhotoImage(file="gigachad_icon.png")
imagen_red=imagen.subsample(2)

def botonPress():
    print("El botón ha sido presionado")
    ventana.iconify()
    

    
    win2=tk.Toplevel(ventana)
    win2.geometry("200x200")
    
    def btn2():
        ventana.deiconify()
        print("Maxim")
        
        
    tk.Button(win2,text="HOLA",command=btn2).pack()
    win2.mainloop()

botonP=tk.Button(ventana,image=imagen_red,command=botonPress,bd=0)
botonP.pack()

ventana.mainloop()
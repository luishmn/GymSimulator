from tkinter import *

root = Tk()
root.geometry("600x250")

framesNum = 75 # Numero de frames que tiene el gif, si no lo conoces ir haciendo tentativos.
archivo = "Fondos/alpha.gif"


# Lista de todas las imagenes del gif
frames = [PhotoImage(file=archivo, format='gif -index %i' %(i)) for i in range(framesNum)]

def update(ind):
    """ Actualiza la imagen gif """
    frame = frames[ind]
    ind += 1
    if ind == framesNum:
        ind = 0
    canvas.create_image(0, 0, image=frame, anchor=NW)
    root.after(40, update, ind) # Numero que regula la velocidad del gif

canvas = Canvas(width=600, height=250) # Modificar segun el tamaño de la imagen

canvas.pack()
root.after(0, update, 0)
root.mainloop()
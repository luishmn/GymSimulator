import tkinter as tk

def animate():
    canvas.move(animation, 1, 0)  # Mueve la animación hacia la derecha
    canvas.after(50, animate)  # Llama a la función 'animate' cada 50 milisegundos

window = tk.Tk()

canvas = tk.Canvas(window, width=500, height=500)
canvas.pack()

# Crea una animación, por ejemplo, un rectángulo rojo
animation = canvas.create_rectangle(0, 0, 50, 50, fill="red")

animate()  # Inicia la animación

window.mainloop()

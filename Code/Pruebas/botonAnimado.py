import tkinter as tk

def raise_button(event):
    button.place(y=97)  # Ajusta la posición del botón cuando se coloca el ratón sobre él

def lower_button(event):
    button.place(y=100)  # Restaura la posición original del botón cuando se quita el ratón

window = tk.Tk()

button = tk.Button(window, text="Botón")
button.place(x=50, y=100)  # Posición original del botón

# Asocia los eventos <Enter> y <Leave> al botón
button.bind("<Enter>", raise_button)
button.bind("<Leave>", lower_button)

window.mainloop()

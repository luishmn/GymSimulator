import os
import tkinter as tk
from tkinter import messagebox, ttk

directorio_archivos = "./Pruebas/Datos"  # Directorio donde se encuentran los archivos de texto

class TablasApp:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Tablas App")
        self.ventana.geometry("1280x720")

        self.archivos_texto = self.obtener_archivos_texto()
        self.menu_desplegable = self.crear_menu_desplegable()
        self.treeview = self.crear_tabla()

        self.ventana.mainloop()

    def obtener_archivos_texto(self):
        archivos_texto = []
        for archivo in os.listdir(directorio_archivos):
            if archivo.endswith(".txt"):
                archivos_texto.append(archivo)
        return archivos_texto

    def crear_menu_desplegable(self):
        opcion_seleccionada = tk.StringVar(self.ventana)
        opcion_seleccionada.set(self.archivos_texto[0])  # Establecer el primer archivo como opción inicial

        menu_desplegable = tk.OptionMenu(self.ventana, opcion_seleccionada, *self.archivos_texto, command=self.mostrar_tabla)
        menu_desplegable.place(x=10, y=10)  # Posicionar en la esquina superior izquierda

        return menu_desplegable

    def crear_tabla(self):
        treeview = ttk.Treeview(self.ventana)

        # Configurar estilo de la tabla
        style = ttk.Style()
        style.configure("Treeview",
                        background="#e1e1e1",
                        foreground="black",
                        fieldbackground="#d3d3d3")
        style.map("Treeview", background=[("selected", "#347083")])

        # Agregar encabezados de columna
        treeview["columns"] = ("nombre", "probabilidad")
        treeview.heading("#0", text="Nombre/Opción/Tiempo/Cantidad/Tipo/Máquina")
        treeview.heading("nombre", text="Nombre")
        treeview.heading("probabilidad", text="Probabilidad")

        treeview.place(x=10, y=40)  # Posicionar debajo del menú desplegable

        return treeview

    def mostrar_tabla(self, archivo_seleccionado):
        ruta_archivo = os.path.join(directorio_archivos, archivo_seleccionado)

        # Limpiar la tabla actual
        self.treeview.delete(*self.treeview.get_children())

        # Leer el archivo de texto y agregar los datos a la tabla
        with open(ruta_archivo, "r") as file:
            for linea in file:
                datos = linea.strip().split(",")
                self.treeview.insert("", "end", text=datos[0], values=(datos[1], datos[2]))

TablasApp()

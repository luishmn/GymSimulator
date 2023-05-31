import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import glob
import os
import re

class VentanaPrincipal:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Menú de tablas")
        
        self.menu_tablas = tk.Menu(self.ventana)
        
        # Crear el menú desplegable de tablas
        menu_desplegable = tk.Menu(self.menu_tablas, tearoff=False)
        
        # Obtener nombres de archivos de las tablas
        def obtener_nombres_archivos(ruta):
            archivos_txt = glob.glob(os.path.join(ruta, "*.txt"))
            archivos_ordenados = sorted(archivos_txt, key=lambda x: int(re.findall(r'\d+', x)[0]))
            return archivos_ordenados

        
        
        nombres_tablas = obtener_nombres_archivos("./Pruebas/Datos")
        
        for nombre_tabla in nombres_tablas:
            #Crea una variable para agregarla sin la ruta al nombre de la tabla en el menú
            nombre_tabla_Libre = os.path.splitext(nombre_tabla)[0]
            nombre_tabla_Libre = os.path.basename(nombre_tabla_Libre)
            menu_desplegable.add_command(label=nombre_tabla_Libre, command=lambda nombre=nombre_tabla: self.seleccionar_tabla(nombre))
        
        self.menu_tablas.add_cascade(label="Tablas", menu=menu_desplegable)
        
        self.ventana.config(menu=self.menu_tablas)
        
        self.tabla_actual = None
        self.tabla_actual_frame = None
        self.tabla_seleccionada = None
    
    def seleccionar_tabla(self, nombre_tabla):
        if self.tabla_actual_frame:
            self.tabla_actual_frame.destroy()
        
        self.tabla_actual_frame = tk.Frame(self.ventana,bg="green")
        self.tabla_actual_frame.pack(pady=20)
        
        self.tabla_actual = ttk.Treeview(self.tabla_actual_frame, columns=("Nombre", "Probabilidad"), show="headings", height=15, style="Custom.Treeview")
        self.tabla_actual.heading("Nombre", text="Nombre/Opción/Tiempo/Cantidad/Tipo/Máquina/Ejercicio")
        self.tabla_actual.heading("Probabilidad", text="Probabilidad")
        self.tabla_actual.column("Nombre", width=370)
        self.tabla_actual.column("Probabilidad", width=130)
        self.tabla_actual.bind("<Double-Button-1>", self.editar_celda)
        self.tabla_actual.pack(side="top", padx=10, pady=60)
        
        # Agregar un widget Label personalizado encima de la tabla para los encabezados
        encabezados_frame = tk.Frame(self.ventana)
        encabezados_frame.place(x=390,y=81,width=500)

        encabezados_label = tk.Label(encabezados_frame, text="Nombre/Opción/Tiempo/Cantidad/Tipo/Máquina    |  Probabilidad", font=("Arial", 10, "bold"), bg="black", fg="yellow")
        encabezados_label.pack(fill="x")
        
        
        # Configurar el estilo personalizado
        style = ttk.Style()
        style.configure("Custom.Treeview",
                        background="#ECECEC",  # Color de fondo de la tabla
                        foreground="black",  # Color del texto de la tabla
                        font=("Arial", 10, "bold"))  # Fuente de letra y tamaño
        
        
        
        self.cargar_datos(nombre_tabla)
        self.tabla_seleccionada = nombre_tabla
    
    def cargar_datos(self, nombre_tabla):
        
        nombre_tabla_Libre = os.path.splitext(nombre_tabla)[0]
        nombre_tabla_Libre = os.path.basename(nombre_tabla_Libre)
        lbl_NombreTabla=tk.Label(ventana_principal,text=nombre_tabla_Libre,font=("Arial", 10, "bold"))
        lbl_NombreTabla.place(x=400,y=40)
        
        self.tabla_actual.delete(*self.tabla_actual.get_children())
        
        try:
            with open(nombre_tabla, "r") as archivo:
                lineas = archivo.readlines()
                for linea in lineas:
                    nombre, probabilidad = linea.strip().split(',')
                    self.tabla_actual.insert("", "end", values=(nombre, probabilidad))
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo '{nombre_tabla}'")
    
    def editar_celda(self, event):
        if self.tabla_actual is None:
            return
        
        item_id = self.tabla_actual.focus()
        column = self.tabla_actual.identify_column(event.x)
        
        if column == "#2":  # Columna "Probabilidad"
            celda_seleccionada = self.tabla_actual.item(item_id)['values'][1]
            nueva_probabilidad = simpledialog.askfloat("Editar probabilidad", "Ingrese la nueva probabilidad:", initialvalue=float(celda_seleccionada))
            
            if nueva_probabilidad is not None:
                self.tabla_actual.set(item_id, column="#2", value=nueva_probabilidad)
    
    def guardar_cambios(self):
        if self.tabla_actual is None:
            return
        
        nombre_tabla = self.tabla_seleccionada
        datos_tabla = []
        
        for item_id in self.tabla_actual.get_children():
            nombre = self.tabla_actual.item(item_id)['values'][0]
            probabilidad = self.tabla_actual.item(item_id)['values'][1]
            datos_tabla.append(f"{nombre},{probabilidad}")
        
        try:
            suma_probabilidades = sum(float(dato.split(',')[1]) for dato in datos_tabla)
            if suma_probabilidades == 1:
                with open(nombre_tabla, "w") as archivo:
                    archivo.write('\n'.join(datos_tabla))
                messagebox.showinfo("Guardado", "Los cambios se han guardado correctamente.")
            else:
                messagebox.showerror("Error", "La suma de las probabilidades no es igual a 1. Por favor, revise los valores ingresados.")
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo '{nombre_tabla}'")





# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.geometry("1280x720")

# Crear una instancia de la clase VentanaPrincipal
ventana = VentanaPrincipal(ventana_principal)

# Crear botón para guardar cambios
boton_guardar = tk.Button(ventana_principal, text="Guardar cambios", command=ventana.guardar_cambios)
boton_guardar.place(x=1100,y=600)

# Iniciar el bucle principal del programa
ventana_principal.mainloop()

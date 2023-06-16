# !/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time
from faker import Faker
import random
from random import uniform
from tkinter import messagebox
from tkinter import ttk
import os
from PIL import ImageTk,Image
import tkinter as tk
from tkinter import simpledialog
import glob
import os
import re
import shutil
   
class Tablas:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("TABLAS")
        
        ic = ImageTk.PhotoImage(Image.open("./Imagenes/tables.ico"))
        self.ventana.iconphoto(True,ic)
        #self.ventana.wm_iconbitmap("./Imagenes/tables.ico")
        
        self.menu_tablas = tk.Menu(self.ventana)
        
        # Crear el menú desplegable de tablas
        menu_desplegable = tk.Menu(self.menu_tablas, tearoff=False)
        
        # Obtener nombres de archivos de las tablas
        def obtener_nombres_archivos(ruta):
            archivos_txt = glob.glob(os.path.join(ruta, "*.txt"))
            archivos_ordenados = sorted(archivos_txt, key=lambda x: int(re.findall(r'\d+', x)[0]))
            return archivos_ordenados

        
        
        nombres_tablas = obtener_nombres_archivos("./Datos")
        
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
        
        self.tabla_actual_frame = tk.Frame(self.ventana,bg="#415D61")
        self.tabla_actual_frame.pack(pady=10)
        
        self.tabla_actual = ttk.Treeview(self.tabla_actual_frame, columns=("Nombre", "Probabilidad"), show="headings", height=18, style="Custom.Treeview")
        self.tabla_actual.heading("Nombre", text="Nombre/Opción/Tiempo/Cantidad/Tipo/Máquina/Ejercicio")
        self.tabla_actual.heading("Probabilidad", text="Probabilidad")
        self.tabla_actual.column("Nombre", width=370)
        self.tabla_actual.column("Probabilidad", width=130)
        self.tabla_actual.bind("<Double-Button-1>", self.editar_celda)
        self.tabla_actual.pack(side="top", padx=10, pady=70)
        
        # Agregar un widget Label personalizado encima de la tabla para los encabezados
        encabezados_frame = tk.Frame(self.ventana)
        encabezados_frame.place(x=390,y=81,width=500)

        encabezados_label = tk.Label(encabezados_frame, text="Nombre/Opción/Tiempo/Cantidad/Tipo/Máquina  | Probabilidad / $", font=("Source Code Pro", 10), bg="#54787E", fg="white")
        encabezados_label.pack(fill="x")
        
        
        # Configurar el estilo de los elementos de la tabla
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#B4CBCF", foreground="black", font=("Source Code Pro", 11))        
        
        
        self.cargar_datos(nombre_tabla)
        self.tabla_seleccionada = nombre_tabla
        
    
    def cargar_datos(self, nombre_tabla):
        
        nombre_tabla_Libre = os.path.splitext(nombre_tabla)[0]
        nombre_tabla_Libre = os.path.basename(nombre_tabla_Libre)
        lbl_NombreTabla=tk.Label(ventana_principal,text=nombre_tabla_Libre,bg="#415D61",foreground="white",font=("Source Code Pro", 15))
        lbl_NombreTabla.place(x=390,y=40)
        
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
        
        #print(nombre_tabla)
        if not(nombre_tabla==r"./Datos\35membresias.txt" or nombre_tabla==r"./Datos\36Gastos.txt" or nombre_tabla==r"./Datos\37Caja.txt" or nombre_tabla==r"./Datos\38TiendaInventarioPrecios.txt" or nombre_tabla==r"./Datos\39TiendaInventarioCantidad.txt" or nombre_tabla==r"./Datos\40PreciosProveedor.txt"):
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
                
        else:
            try:
                with open(nombre_tabla, "w") as archivo:
                        archivo.write('\n'.join(datos_tabla))
                messagebox.showinfo("Guardado", "Los cambios se han guardado correctamente.")
            except FileNotFoundError:
                messagebox.showerror("Error", f"No se encontró el archivo '{nombre_tabla}'")





def AbrirVentanaTablas(root):
    def cerrar(ventana):
        root.deiconify()
        ventana.destroy()
        
    def restablecerDatos(origen, destino):
        archivos = os.listdir(origen)
        for archivo in archivos:
            ruta_origen = os.path.join(origen, archivo)
            ruta_destino = os.path.join(destino, archivo)
            
            if os.path.isfile(ruta_destino):
                shutil.copyfile(ruta_origen, ruta_destino)
        messagebox.showinfo("Terminado","Archivos restablecidos con éxito.")
            
    ruta_origen = "./Datos/Backup"
    ruta_destino = "./Datos"
    
    global ventana_principal
    root=root
    
    root.iconify()
    ventana_principal = tk.Toplevel(root)
    ventana_principal.geometry("1280x720+35-20")
    ventana_principal.resizable(width=False,height=False)

    ventana = Tablas(ventana_principal)

    ventanaIMG=tk.PhotoImage(file="Imagenes/TablesIMG/fondo.png")
    bt1IMG=tk.PhotoImage(file="Imagenes/TablesIMG/restablecer.png")
    bt2IMG=tk.PhotoImage(file="Imagenes/TablesIMG/guardar.png")
    btCIMG=tk.PhotoImage(file="Imagenes/TablesIMG/cerrar.png")
    
    Lbl_img_tablas=tk.Label(ventana_principal,image=ventanaIMG).place(x=-2,y=0)
    
    def Fbtn1_raise(event):
        btn_restablecer.place(y=562)
    def Fbtn2_raise(event):
        btn_guardar.place(y=565)
    def FbtnC_raise(event):
        btnC.place(y=20)
    
    def Fbtn1_lower(event):
        btn_restablecer.place(y=565)
    def Fbtn2_lower(event):
        btn_guardar.place(y=568)
    def FbtnC_lower(event):
        btnC.place(y=23)
    
    btn_restablecer = tk.Button(ventana_principal, image=bt1IMG, command=lambda:restablecerDatos(ruta_origen, ruta_destino),bd=0,highlightthickness=0)
    btn_restablecer.place(x=358,y=565)
    btn_guardar = tk.Button(ventana_principal, image=bt2IMG, command=ventana.guardar_cambios,bd=0,highlightthickness=0)
    btn_guardar.place(x=714,y=568) 
    btnC = tk.Button(ventana_principal,image=btCIMG,command=lambda:cerrar(ventana_principal),bd=0,highlightthickness=0)
    btnC.place(x=1194,y=23)

    btn_restablecer.bind("<Enter>",Fbtn1_raise)
    btn_guardar.bind("<Enter>",Fbtn2_raise)
    btnC.bind("<Enter>",FbtnC_raise)
        
    btn_restablecer.bind("<Leave>",Fbtn1_lower)
    btn_guardar.bind("<Leave>",Fbtn2_lower)
    btnC.bind("<Leave>",FbtnC_lower)
    
    ventana_principal.mainloop()



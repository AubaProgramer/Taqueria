import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os
from fpdf import FPDF
import graficas
import database

class VentanaVentas:
    def __init__(self, root, nombre_usuario, rol_usuario):
        self.root = root
        self.rol_usuario = rol_usuario
        self.total_actual = 0.0
        
        # Paleta de colores "Tacos Esther" (Diseño Moderno)
        self.color_fondo = "#F8F9FA"  # Gris claro muy limpio
        self.color_blanco = "#FFFFFF"
        self.color_verde = "#27AE60"  # Verde éxito
        self.color_azul = "#2980B9"   # Azul reportes
        self.color_naranja = "#E67E22" # Color para Consomé/Promos
        self.color_rojo = "#C0392B"   # Salir
        self.color_texto = "#2C3E50"

        self.root.title(f"Tacos Esther - Ventas: {nombre_usuario}")
        self.root.geometry("1150x800")
        self.root.configure(bg=self.color_fondo)

        # 1. Paneles Principales
        self.frame_menu = tk.LabelFrame(self.root, text=" MENÚ DE PRODUCTOS ", padx=10, pady=10, 
                                        bg=self.color_fondo, fg=self.color_texto, font=("Arial", 10, "bold"))
        self.frame_menu.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.frame_ticket = tk.LabelFrame(self.root, text=" TICKET DE VENTA ", padx=10, pady=10,
                                         bg=self.color_blanco, fg=self.color_texto, font=("Arial", 10, "bold"))
        self.frame_ticket.pack(side="right", fill="both", padx=10, pady=10)

        # 2. Inicializar componentes
        self.crear_interfaz_ticket()
        self.crear_interfaz_comida()

    def crear_interfaz_ticket(self):
        # Estilo para la tabla
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=28)
        
        self.tree = ttk.Treeview(self.frame_ticket, columns=("Cant", "Prod", "Subt"), show="headings", height=18)
        self.tree.heading("Cant", text="Cant")
        self.tree.heading("Prod", text="Producto")
        self.tree.heading("Subt", text="Subtotal")
        self.tree.column("Cant", width=50, anchor="center")
        self.tree.column("Prod", width=220)
        self.tree.column("Subt", width=80, anchor="e")
        self.tree.pack(pady=5)

        self.lbl_total = tk.Label(self.frame_ticket, text="TOTAL: $0.00", 
                                 font=("Arial", 26, "bold"), fg=self.color_verde, bg=self.color_blanco)
        self.lbl_total.pack(pady=15)

        # Botón Cobrar Estilo Moderno
        tk.Button(self.frame_ticket, text="COBRAR E IMPRIMIR", 
                  bg=self.color_verde, fg="white", font=("Arial", 14, "bold"), 
                  relief="flat", height=2, cursor="hand2",
                  command=self.finalizar_venta).pack(fill="x", pady=5, padx=10)
        
        tk.Button(self.frame_ticket, text="LIMPIAR TICKET", bg="#BDC3C7", fg="white", 
                  relief="flat", font=("Arial", 9, "bold"), command=self.limpiar_ticket).pack(fill="x", padx=10)

    def crear_interfaz_comida(self):
        def boton_item(contenedor, texto, comando, color="#FFFFFF"):
            return tk.Button(contenedor, text=texto, width=16, height=2,
                             bg=color, fg=self.color_texto, font=("Arial", 9, "bold"),
                             relief="flat", bd=1, cursor="hand2", command=comando)

        # --- COLUMNA 0: TACOS (18/21) ---
        tk.Label(self.frame_menu, text="--- TACOS ---", font=("Arial", 10, "bold"), bg=self.color_fondo).grid(row=0, column=0, pady=5)
        tacos = [("Barbacoa", 18), ("Chicharrón", 18), ("Chorizo", 18), ("Bistec", 21), ("Campechano", 21)]
        for i, (nom, p) in enumerate(tacos):
            boton_item(self.frame_menu, nom, lambda n=nom, p=p: self.agregar_producto(f"Taco {n}", p, 3)).grid(row=i+1, column=0, pady=3, padx=5)

        # --- COLUMNA 1: LONCHES (50/60) ---
        tk.Label(self.frame_menu, text="--- LONCHES ---", font=("Arial", 10, "bold"), bg=self.color_fondo).grid(row=0, column=1, pady=5)
        lonches = [("Lonche Barbacoa", 50), ("Lonche Chicharrón", 50), ("Lonche Chorizo", 50), ("Lonche Bistec", 60)]
        for i, (nom, p) in enumerate(lonches):
            boton_item(self.frame_menu, nom, lambda n=nom, p=p: self.agregar_producto(n, p, 5)).grid(row=i+1, column=1, pady=3, padx=5)

        # --- COLUMNA 2: TODAS LAS BEBIDAS ---
        tk.Label(self.frame_menu, text="--- BEBIDAS ---", font=("Arial", 10, "bold"), bg=self.color_fondo).grid(row=0, column=2, pady=5)
        bebidas = [
            ("Coca 500ml", 26), ("Coca Medio", 21), ("Coca Taquera", 19),
            ("Refresco 400ml", 16), ("Jumex Vidrio", 22), ("Jumex Cartón", 14)
        ]
        for i, (nom, p) in enumerate(bebidas):
            boton_item(self.frame_menu, nom, lambda n=nom, p=p: self.agregar_producto(n, p, 0)).grid(row=i+1, column=2, pady=3, padx=5)

        # Extras y Adicionales
        self.con_queso = tk.BooleanVar()
        tk.Checkbutton(self.frame_menu, text="¿Lleva Queso?", variable=self.con_queso, 
                       bg=self.color_fondo, font=("Arial", 11, "bold"), fg="blue").grid(row=7, column=0, columnspan=2, pady=5)
        
        # Botón Consomé
        boton_item(self.frame_menu, "Consomé ($8)", lambda: self.agregar_producto("Consomé", 8, 0), self.color_naranja).grid(row=8, column=0, pady=5)

        # --- BOTONES DE ACCIÓN ---
        # Mega Promo
        tk.Button(self.frame_menu, text="MEGA PROMO $205\n(10 Tacos + Consomé + Refresco)", 
                  bg="#E74C3C", fg="white", font=("Arial", 11, "bold"), 
                  relief="flat", height=3, command=self.ventana_promo).grid(row=9, column=0, columnspan=3, pady=15, sticky="nsew")

        # Reportes (Admin)
        if self.rol_usuario == "Administrador":
            tk.Button(self.frame_menu, text="VER GRÁFICA DE VENTAS", 
                      bg=self.color_azul, fg="white", font=("Arial", 10, "bold"),
                      relief="flat", height=2, command=graficas.mostrar_grafica_ventas).grid(row=10, column=0, columnspan=3, pady=5, sticky="nsew")

        # Salir
        tk.Button(self.frame_menu, text="CERRAR SESIÓN", bg="#7F8C8D", fg="white", 
                  relief="flat", command=self.cerrar_sesion).grid(row=11, column=0, columnspan=3, pady=10, sticky="nsew")

    def cerrar_sesion(self):
        if messagebox.askyesno("Salir", "¿Deseas cerrar sesión?"):
            self.root.event_generate("<<Logout>>")

    def agregar_producto(self, nombre, precio_base, costo_queso):
        precio = precio_base
        if self.con_queso.get() and costo_queso > 0:
            precio += costo_queso
            nombre += " c/Q"
        self.total_actual += precio
        self.tree.insert("", "end", values=(1, nombre, f"${precio}"))
        self.lbl_total.config(text=f"TOTAL: ${self.total_actual:.2f}")

    def limpiar_ticket(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.total_actual = 0.0
        self.lbl_total.config(text="TOTAL: $0.00")

    def ventana_promo(self):
        # Crear ventana emergente
        self.win_promo = tk.Toplevel(self.root)
        self.win_promo.title("Configurar Mega Promo")
        self.win_promo.geometry("400x550")
        self.win_promo.configure(bg=self.color_fondo)

        tk.Label(self.win_promo, text="Selecciona los 10 Tacos", 
                 font=("Arial", 12, "bold"), bg=self.color_fondo).pack(pady=10)

        # Diccionario para guardar cuántos de cada uno eligen
        self.seleccion_promo = {
            "Barbacoa": tk.IntVar(value=0),
            "Chicharrón": tk.IntVar(value=0),
            "Chorizo": tk.IntVar(value=0),
            "Bistec": tk.IntVar(value=0),
            "Campechano": tk.IntVar(value=0)
        }

        # Crear selectores (Spinbox) para cada carne
        for carne in self.seleccion_promo:
            frame = tk.Frame(self.win_promo, bg=self.color_fondo)
            frame.pack(fill="x", padx=40, pady=5)
            
            tk.Label(frame, text=f"{carne}:", font=("Arial", 10), bg=self.color_fondo, width=15, anchor="w").pack(side="left")
            
            # Spinbox para elegir cantidad (0 a 10)
            tk.Spinbox(frame, from_=0, to=10, textvariable=self.seleccion_promo[carne], 
                       width=5, font=("Arial", 10)).pack(side="right")

        tk.Label(self.win_promo, text="* Bistec/Campechano +$3 c/u", 
                 font=("Arial", 8, "italic"), fg="red", bg=self.color_fondo).pack(pady=5)

        # Botón para confirmar
        tk.Button(self.win_promo, text="AGREGAR PROMO AL TICKET", 
                  bg=self.color_verde, fg="white", font=("Arial", 10, "bold"),
                  relief="flat", height=2, command=self.confirmar_promo).pack(pady=20, fill="x", padx=50)

    def confirmar_promo(self):
        total_tacos = sum(var.get() for var in self.seleccion_promo.values())
        
        if total_tacos != 10:
            messagebox.showwarning("Error", f"Debes seleccionar exactamente 10 tacos.\nLlevas: {total_tacos}")
            return

        # Calcular extras de Bistec y Campechano
        extra_bistec = self.seleccion_promo["Bistec"].get() * 3
        extra_camp = self.seleccion_promo["Campechano"].get() * 3
        precio_final_promo = 205 + extra_bistec + extra_camp

        # Crear descripción de qué lleva la promo
        detalles = []
        for carne, var in self.seleccion_promo.items():
            if var.get() > 0:
                detalles.append(f"{var.get()} {carne}")
        
        descripcion = "MEGA PROMO (" + ", ".join(detalles) + ")"

        # Agregar al ticket
        self.total_actual += precio_final_promo
        self.tree.insert("", "end", values=(1, descripcion, f"${precio_final_promo}"))
        self.lbl_total.config(text=f"TOTAL: ${self.total_actual:.2f}")
        
        self.win_promo.destroy() # Cerrar ventanita

    def finalizar_venta(self):
        items = self.tree.get_children()
        if not items:
            messagebox.showwarning("Venta", "El ticket está vacío")
            return
        
        carpeta = "Tickets_Generados"
        if not os.path.exists(carpeta): os.makedirs(carpeta)

        fecha_obj = datetime.datetime.now()
        nombre_pdf = os.path.join(carpeta, f"Ticket_{fecha_obj.strftime('%Y%m%d_%H%M%S')}.pdf")
        
        try:
            # Guardar en DB
            for item in items:
                v = self.tree.item(item)["values"]
                database.guardar_venta(v[1], float(str(v[2]).replace('$', '')))

            # PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 20)
            pdf.cell(0, 10, "TACOS ESTHER - DESDE 2013", ln=True, align="C")
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, f"Fecha: {fecha_obj.strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
            pdf.ln(10)
            
            # Tabla PDF
            pdf.set_font("Arial", "B", 12)
            pdf.cell(30, 10, "Cant", 1); pdf.cell(110, 10, "Producto", 1); pdf.cell(50, 10, "Precio", 1, ln=True)
            pdf.set_font("Arial", "", 12)
            for item in items:
                v = self.tree.item(item)["values"]
                pdf.cell(30, 10, str(v[0]), 1)
                pdf.cell(110, 10, str(v[1]), 1)
                pdf.cell(50, 10, str(v[2]), 1, ln=True)

            pdf.ln(5)
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, f"TOTAL: ${self.total_actual:.2f}", ln=True, align="R")
            
            pdf.output(nombre_pdf)
            messagebox.showinfo("Éxito", f"Venta guardada en {carpeta}")
            self.limpiar_ticket()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear ticket: {e}")
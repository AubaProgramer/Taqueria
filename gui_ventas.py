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
        
        self.root.title(f"Tacos Esther - Ventas: {nombre_usuario}")
        self.root.geometry("1100x750")

        # 1. Paneles principales
        self.frame_menu = tk.LabelFrame(self.root, text="Menú de Taquería", padx=10, pady=10)
        self.frame_menu.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.frame_ticket = tk.LabelFrame(self.root, text="Ticket de Venta", padx=10, pady=10)
        self.frame_ticket.pack(side="right", fill="both", padx=10, pady=10)

        # 2. Inicializar componentes
        self.crear_interfaz_ticket()
        self.crear_interfaz_comida()

    def crear_interfaz_ticket(self):
        self.tree = ttk.Treeview(self.frame_ticket, columns=("Cant", "Prod", "Subt"), show="headings", height=20)
        self.tree.heading("Cant", text="Cant")
        self.tree.heading("Prod", text="Producto")
        self.tree.heading("Subt", text="Subtotal")
        self.tree.column("Cant", width=50)
        self.tree.column("Prod", width=200)
        self.tree.pack()

        self.lbl_total = tk.Label(self.frame_ticket, text="TOTAL: $0.00", font=("Arial", 20, "bold"), fg="green")
        self.lbl_total.pack(pady=10)

        tk.Button(self.frame_ticket, text="LIMPIAR TICKET", bg="#95a5a6", command=self.limpiar_ticket).pack(fill="x")
        tk.Button(self.frame_ticket, text="COBRAR E IMPRIMIR", bg="#27ae60", fg="white", font=("Arial", 12, "bold"), height=2, command=self.finalizar_venta).pack(fill="x", pady=5)

    def crear_interfaz_comida(self):
        # --- TACOS ---
        tk.Label(self.frame_menu, text="--- TACOS ---", font=("Arial", 10, "bold")).grid(row=0, column=0, pady=5)
        carnes = [("Barbacoa", 18), ("Chicharrón", 18), ("Chorizo", 18), ("Bistec", 21), ("Campechano", 21)]
        for i, (carne, precio) in enumerate(carnes):
            tk.Button(self.frame_menu, text=carne, width=15, 
                      command=lambda c=carne, p=precio: self.agregar_producto(f"Taco {c}", p, 3)).grid(row=i+1, column=0, pady=2)

        # --- LONCHES ---
        tk.Label(self.frame_menu, text="--- LONCHES ---", font=("Arial", 10, "bold")).grid(row=0, column=1, pady=5)
        lonches = [("Barbacoa", 50), ("Chicharrón", 50), ("Chorizo", 50), ("Bistec", 60)]
        for i, (carne, precio) in enumerate(lonches):
            tk.Button(self.frame_menu, text=f"Lonche {carne}", width=15, 
                      command=lambda c=carne, p=precio: self.agregar_producto(f"Lonche {c}", p, 5)).grid(row=i+1, column=1, pady=2, padx=10)

        # --- BEBIDAS ---
        tk.Label(self.frame_menu, text="--- BEBIDAS ---", font=("Arial", 10, "bold")).grid(row=0, column=2, pady=5)
        bebidas = [("Coca 500ml", 26), ("Coca Medio", 21), ("Refresco 400ml", 16)]
        for i, (nom, p) in enumerate(bebidas):
            tk.Button(self.frame_menu, text=nom, width=15, 
                      command=lambda n=nom, p=p: self.agregar_producto(n, p, 0)).grid(row=i+1, column=2, pady=2)

        # Queso
        self.con_queso = tk.BooleanVar()
        tk.Checkbutton(self.frame_menu, text="¿Lleva Queso?", variable=self.con_queso, font=("Arial", 11, "bold"), fg="blue").grid(row=7, column=0, columnspan=2, pady=10)

        # Botones de Acción
        tk.Button(self.frame_menu, text="MEGA PROMO $205", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), height=3, command=self.ventana_promo).grid(row=9, column=0, columnspan=3, pady=15, sticky="nsew")

        if self.rol_usuario == "Administrador":
            tk.Button(self.frame_menu, text="VER GRÁFICA DE VENTAS", bg="#2980b9", fg="white", font=("Arial", 10, "bold"), height=2, command=graficas.mostrar_grafica_ventas).grid(row=10, column=0, columnspan=3, pady=5, sticky="nsew")

        tk.Button(self.frame_menu, text="CERRAR SESIÓN", bg="#c0392b", fg="white", command=lambda: self.root.event_generate("<<Logout>>")).grid(row=11, column=0, columnspan=3, pady=5, sticky="nsew")

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
        self.total_actual += 205
        self.tree.insert("", "end", values=(1, "MEGA PROMO", "$205"))
        self.lbl_total.config(text=f"TOTAL: ${self.total_actual:.2f}")

    def finalizar_venta(self):
        # 1. Verificar si hay algo que cobrar
        items = self.tree.get_children()
        if not items:
            messagebox.showwarning("Venta", "El ticket está vacío")
            return
        
        # 2. Crear carpeta de Tickets
        carpeta = "Tickets_Generados"
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        fecha_obj = datetime.datetime.now()
        nombre_pdf = os.path.join(carpeta, f"Ticket_{fecha_obj.strftime('%Y-%m-%d_%H-%M-%S')}.pdf")
        
        try:
            # 3. Guardar en Base de Datos
            for item in items:
                v = self.tree.item(item)["values"]
                p_limpio = float(str(v[2]).replace('$', ''))
                database.guardar_venta(v[1], p_limpio)

            # 4. Crear PDF con contenido
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 20)
            pdf.cell(0, 10, "TACOS ESTHER - DESDE 2013", ln=True, align="C")
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, f"Fecha: {fecha_obj.strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
            pdf.ln(10)

            # Encabezados
            pdf.set_font("Arial", "B", 12)
            pdf.cell(30, 10, "Cant", 1); pdf.cell(110, 10, "Producto", 1); pdf.cell(50, 10, "Precio", 1, ln=True)
            
            # Detalle de productos (IMPORTANTE: extraer datos del tree)
            pdf.set_font("Arial", "", 12)
            for item in items:
                v = self.tree.item(item)["values"]
                pdf.cell(30, 10, str(v[0]), 1)
                pdf.cell(110, 10, str(v[1]), 1)
                pdf.cell(50, 10, str(v[2]), 1, ln=True)

            pdf.ln(5)
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, f"TOTAL A PAGAR: ${self.total_actual:.2f}", ln=True, align="R")
            
            pdf.output(nombre_pdf)
            messagebox.showinfo("Éxito", f"Venta guardada en carpeta: {carpeta}")
            self.limpiar_ticket()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo finalizar: {e}")
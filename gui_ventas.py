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
        # ... (Mantén el estilo y el Treeview igual que antes) ...
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=28)
        
        self.tree = ttk.Treeview(self.frame_ticket, columns=("Cant", "Prod", "Subt"), show="headings", height=12)
        self.tree.heading("Cant", text="Cant")
        self.tree.heading("Prod", text="Producto")
        self.tree.heading("Subt", text="Subtotal")
        self.tree.column("Cant", width=50, anchor="center")
        self.tree.column("Prod", width=220)
        self.tree.column("Subt", width=80, anchor="e")
        self.tree.pack(pady=5)

        self.lbl_total = tk.Label(self.frame_ticket, text="TOTAL: $0.00", 
                                 font=("Arial", 22, "bold"), fg=self.color_verde, bg=self.color_blanco)
        self.lbl_total.pack(pady=5)

        # --- SECCIÓN NUEVA: DATOS DE ENTREGA Y PAGO ---
        frame_entrega = tk.Frame(self.frame_ticket, bg=self.color_blanco)
        frame_entrega.pack(fill="x", pady=10)

        tk.Label(frame_entrega, text="Dirección de Envío:", bg=self.color_blanco, font=("Arial", 9, "bold")).pack(anchor="w")
        self.ent_direccion = tk.Entry(frame_entrega, font=("Arial", 10), relief="solid", bd=1)
        self.ent_direccion.pack(fill="x", pady=2)

        tk.Label(frame_entrega, text="Pagó con ($):", bg=self.color_blanco, font=("Arial", 9, "bold")).pack(anchor="w")
        self.ent_pago = tk.Entry(frame_entrega, font=("Arial", 10), relief="solid", bd=1)
        self.ent_pago.pack(fill="x", pady=2)
        # -----------------------------------------------

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
            if nom == "Barbacoa":
                # La barbacoa ahora abre una ventana de selección de término
                boton_item(self.frame_menu, nom, lambda: self.ventana_termino_barbacoa(18)).grid(row=i+1, column=0, pady=3, padx=5)
            else:
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
        self.win_promo.title("Configurar Mega Promo (10 Tacos)")
        self.win_promo.geometry("450x650")
        self.win_promo.configure(bg=self.color_fondo)
        self.win_promo.grab_set()

        tk.Label(self.win_promo, text="Personaliza los 10 Tacos", 
                 font=("Arial", 14, "bold"), bg=self.color_fondo).pack(pady=15)

        # Diccionario ampliado para incluir los términos de la barbacoa
        self.seleccion_promo = {
            "Barbacoa Blandos": tk.IntVar(value=0),
            "Barbacoa Medios": tk.IntVar(value=0),
            "Barbacoa Dorados": tk.IntVar(value=0),
            "Chicharrón": tk.IntVar(value=0),
            "Chorizo": tk.IntVar(value=0),
            "Bistec": tk.IntVar(value=0),
            "Campechano": tk.IntVar(value=0)
        }

        # Crear selectores (Spinbox) para cada opción
        for carne in self.seleccion_promo:
            frame = tk.Frame(self.win_promo, bg=self.color_fondo)
            frame.pack(fill="x", padx=50, pady=4)
            
            # Color especial para resaltar las opciones de barbacoa
            color_lbl = "#D35400" if "Barbacoa" in carne else self.color_texto
            
            tk.Label(frame, text=f"{carne}:", font=("Arial", 10, "bold"), 
                     bg=self.color_fondo, fg=color_lbl, width=18, anchor="w").pack(side="left")
            
            tk.Spinbox(frame, from_=0, to=10, textvariable=self.seleccion_promo[carne], 
                       width=5, font=("Arial", 11), justify="center").pack(side="right")

        # Nota de cargos extra
        tk.Label(self.win_promo, text="* Bistec/Campechano +$3 c/u\n* Barbacoa no tiene costo extra", 
                 font=("Arial", 9, "italic"), fg="red", bg=self.color_fondo).pack(pady=10)

        # Botón para confirmar
        tk.Button(self.win_promo, text="AGREGAR PROMO AL TICKET", 
                  bg=self.color_verde, fg="white", font=("Arial", 11, "bold"),
                  relief="flat", height=2, cursor="hand2", 
                  command=self.confirmar_promo).pack(pady=20, fill="x", padx=60)

    def confirmar_promo(self):
        # Sumar todos los tacos seleccionados
        total_tacos = sum(var.get() for var in self.seleccion_promo.values())
        
        if total_tacos != 10:
            messagebox.showwarning("Cantidad Incorrecta", 
                                   f"La promo debe tener exactamente 10 tacos.\nLlevas seleccionados: {total_tacos}")
            return

        # Calcular extras solo de Bistec y Campechano ($3 extra c/u)
        extra_bistec = self.seleccion_promo["Bistec"].get() * 3
        extra_camp = self.seleccion_promo["Campechano"].get() * 3
        precio_final_promo = 205 + extra_bistec + extra_camp

        # Crear lista detallada para el ticket
        detalles = []
        for carne, var in self.seleccion_promo.items():
            if var.get() > 0:
                detalles.append(f"{var.get()} {carne}")
        
        descripcion = "MEGA PROMO (" + ", ".join(detalles) + ")"

        # Agregar al ticket principal
        self.total_actual += precio_final_promo
        self.tree.insert("", "end", values=(1, descripcion, f"${precio_final_promo:.2f}"))
        self.lbl_total.config(text=f"TOTAL: ${self.total_actual:.2f}")
        
        self.win_promo.destroy()

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
        
        # Validar el pago y calcular cambio
        try:
            monto_pago = float(self.ent_pago.get()) if self.ent_pago.get() else self.total_actual
            if monto_pago < self.total_actual:
                messagebox.showerror("Error", "El monto de pago es menor al total")
                return
            cambio = monto_pago - self.total_actual
        except ValueError:
            messagebox.showerror("Error", "Ingresa un monto de pago válido")
            return

        direccion = self.ent_direccion.get() if self.ent_direccion.get() else "Venta en Mostrador"

        # ... (Crear carpeta y guardar en DB igual que antes) ...
        carpeta = "Tickets_Generados"
        if not os.path.exists(carpeta): os.makedirs(carpeta)
        fecha_obj = datetime.datetime.now()
        nombre_pdf = os.path.join(carpeta, f"Ticket_{fecha_obj.strftime('%Y%m%d_%H%M%S')}.pdf")

        try:
            # 1. Guardar en Base de Datos
            for item in items:
                v = self.tree.item(item)["values"]
                database.guardar_venta(v[1], float(str(v[2]).replace('$', '')))

            # 2. Configurar PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 20)
            pdf.cell(0, 10, "TACOS ESTHER - ENTREGA", ln=True, align="C")
            pdf.set_font("Arial", "", 11)
            pdf.cell(0, 7, f"Fecha: {fecha_obj.strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
            pdf.ln(5)
            
            # 3. Datos del cliente (Dirección)
            pdf.set_font("Arial", "B", 12)
            pdf.multi_cell(0, 10, f"DIRECCIÓN: {direccion}", border=1, align="L")
            pdf.ln(5)

            # 4. Encabezados de la Tabla
            pdf.set_font("Arial", "B", 11)
            pdf.cell(20, 8, "Cant", 1, 0, 'C')
            pdf.cell(120, 8, "Producto", 1, 0, 'L')
            pdf.cell(40, 8, "Subt", 1, 1, 'R')
            
            # 5. LISTADO DE PRODUCTOS (Aquí está el arreglo del encimado)
            pdf.set_font("Arial", "", 10)
            for item in items:
                v = self.tree.item(item)["values"]
                cant = str(v[0])
                prod = str(v[1])
                subt = str(v[2])

                # Guardamos la posición actual
                x = pdf.get_x()
                y = pdf.get_y()

                # Celda de Cantidad
                pdf.cell(20, 10, cant, 1, 0, 'C')
                
                # MultiCelda para el Producto (esto evita que se encime)
                # Si el texto es largo, salta de línea solo
                pdf.multi_cell(120, 5, prod, 1, 'L') 
                
                # Calculamos cuánto bajó la MultiCelda para que el precio quede alineado
                final_y = pdf.get_y()
                altura_fila = final_y - y
                
                # Regresamos a la posición para poner el Subtotal a la derecha
                pdf.set_xy(x + 140, y)
                pdf.cell(40, altura_fila, subt, 1, 1, 'R')

            # 6. Totales y Cambio
            pdf.ln(5)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, f"TOTAL: ${self.total_actual:.2f}", ln=True, align="R")
            pdf.cell(0, 8, f"PAGÓ CON: ${monto_pago:.2f}", ln=True, align="R")
            
            # Si hay cambio, lo ponemos en rojo
            if cambio > 0:
                pdf.set_text_color(200, 0, 0)
            pdf.cell(0, 8, f"CAMBIO: ${cambio:.2f}", ln=True, align="R")
            
            # 7. Finalizar
            pdf.output(nombre_pdf)
            messagebox.showinfo("Venta Exitosa", f"Cambio a entregar: ${cambio:.2f}\nTicket guardado.")
            
            # Limpiar campos
            self.ent_direccion.delete(0, tk.END)
            self.ent_pago.delete(0, tk.END)
            self.limpiar_ticket()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear ticket: {e}")
        
    def ventana_termino_barbacoa(self, precio_base):
        # Crear ventana emergente pequeña
        self.win_termino = tk.Toplevel(self.root)
        self.win_termino.title("Término de la Barbacoa")
        self.win_termino.geometry("300x250")
        self.win_termino.configure(bg=self.color_blanco)
        self.win_termino.grab_set() # Bloquea la ventana principal hasta elegir

        tk.Label(self.win_termino, text="¿Cómo quiere su taco?", 
                 font=("Arial", 11, "bold"), bg=self.color_blanco).pack(pady=15)

        terminos = ["Blando", "Medio", "Dorado"]
        for termino in terminos:
            tk.Button(self.win_termino, text=termino, width=20, height=2,
                      bg=self.color_fondo, font=("Arial", 10), relief="flat",
                      command=lambda t=termino: self.confirmar_barbacoa(t, precio_base)).pack(pady=5)

    def confirmar_barbacoa(self, termino, precio_base):
        nombre_final = f"Taco Barbacoa ({termino})"
        # Reutilizamos la lógica del queso si está marcado
        if self.con_queso.get():
            precio_base += 3
            nombre_final += " c/Q"
        
        self.total_actual += precio_base
        self.tree.insert("", "end", values=(1, nombre_final, f"${precio_base}"))
        self.lbl_total.config(text=f"TOTAL: ${self.total_actual:.2f}")
        self.win_termino.destroy()
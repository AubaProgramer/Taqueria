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
        
        # --- DISEÑO MINIMALISTA PASTEL ---
        self.color_fondo = "#F3F4F6"  
        self.color_blanco = "#FFFFFF"
        self.color_verde = "#10B981"  
        self.color_azul = "#6366F1"   
        self.color_naranja = "#F59E0B" 
        self.color_rojo = "#F43F5E"   
        self.color_texto = "#1F2937"  

        self.root.title(f"Tacos Esther - Ventas: {nombre_usuario}")
        self.root.geometry("1150x800")
        self.root.configure(bg=self.color_fondo)

        # Paneles Principales
        self.frame_menu = tk.LabelFrame(self.root, text=" MENÚ DE PRODUCTOS ", padx=10, pady=10, 
                                        bg=self.color_fondo, fg=self.color_texto, font=("Arial", 10, "bold"))
        self.frame_menu.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.frame_ticket = tk.LabelFrame(self.root, text=" TICKET DE VENTA ", padx=10, pady=10,
                                         bg=self.color_blanco, fg=self.color_texto, font=("Arial", 10, "bold"))
        self.frame_ticket.pack(side="right", fill="both", padx=10, pady=10)

        self.crear_interfaz_ticket()
        self.crear_interfaz_comida()

    def crear_interfaz_ticket(self):
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

        frame_pago = tk.Frame(self.frame_ticket, bg=self.color_blanco)
        frame_pago.pack(fill="x", pady=5)

        tk.Label(frame_pago, text="Dirección de Envío:", bg=self.color_blanco, font=("Arial", 9, "bold")).pack(anchor="w")
        self.ent_direccion = tk.Entry(frame_pago, font=("Arial", 10), relief="solid", bd=1)
        self.ent_direccion.pack(fill="x", pady=2)

        tk.Label(frame_pago, text="Pagó con ($):", bg=self.color_blanco, font=("Arial", 9, "bold")).pack(anchor="w")
        self.ent_pago = tk.Entry(frame_pago, font=("Arial", 10), relief="solid", bd=1)
        self.ent_pago.pack(fill="x", pady=2)

        tk.Button(self.frame_ticket, text="COBRAR E IMPRIMIR", bg=self.color_verde, fg="white", 
                  font=("Arial", 14, "bold"), relief="flat", height=2, cursor="hand2",
                  command=self.finalizar_venta).pack(fill="x", pady=10)
        
        tk.Button(self.frame_ticket, text="LIMPIAR TICKET", bg="#BDC3C7", fg="white", 
                  relief="flat", command=self.limpiar_ticket).pack(fill="x")

    def crear_interfaz_comida(self):
        def boton_item(contenedor, texto, comando, color=self.color_blanco):
            return tk.Button(contenedor, text=texto, width=16, height=2,
                             bg=color, fg=self.color_texto, font=("Arial", 9, "bold"),
                             relief="flat", bd=1, cursor="hand2", command=comando)

        # COLUMNA 0: TACOS
        tk.Label(self.frame_menu, text="--- TACOS ---", font=("Arial", 10, "bold"), bg=self.color_fondo).grid(row=0, column=0, pady=5)
        tacos = [("Barbacoa", 18), ("Chicharrón", 18), ("Chorizo", 18), ("Bistec", 21), ("Campechano", 21)]
        for i, (nom, p) in enumerate(tacos):
            if nom == "Barbacoa":
                boton_item(self.frame_menu, nom, lambda: self.ventana_termino_barbacoa(18)).grid(row=i+1, column=0, pady=3, padx=5)
            else:
                boton_item(self.frame_menu, nom, lambda n=nom, p=p: self.agregar_producto(f"Taco {n}", p, 3)).grid(row=i+1, column=0, pady=3, padx=5)

        # COLUMNA 1: LONCHES
        tk.Label(self.frame_menu, text="--- LONCHES ---", font=("Arial", 10, "bold"), bg=self.color_fondo).grid(row=0, column=1, pady=5)
        lonches = [("Lonche Barbacoa", 50), ("Lonche Chicharrón", 50), ("Lonche Chorizo", 50), ("Lonche Bistec", 60)]
        for i, (nom, p) in enumerate(lonches):
            boton_item(self.frame_menu, nom, lambda n=nom, p=p: self.agregar_producto(n, p, 5)).grid(row=i+1, column=1, pady=3, padx=5)

        # COLUMNA 2: BEBIDAS
        tk.Label(self.frame_menu, text="--- BEBIDAS ---", font=("Arial", 10, "bold"), bg=self.color_fondo).grid(row=0, column=2, pady=5)
        bebidas = [("Coca 500ml", 26), ("Coca Medio", 21), ("Coca Taquera", 19), ("Refresco 400ml", 16), ("Jumex Vidrio", 22), ("Jumex Cartón", 14)]
        for i, (nom, p) in enumerate(bebidas):
            boton_item(self.frame_menu, nom, lambda n=nom, p=p: self.agregar_producto(n, p, 0)).grid(row=i+1, column=2, pady=3, padx=5)

        self.con_queso = tk.BooleanVar()
        tk.Checkbutton(self.frame_menu, text="¿Lleva Queso?", variable=self.con_queso, 
                       bg=self.color_fondo, font=("Arial", 11, "bold"), fg="blue").grid(row=7, column=0, columnspan=2, pady=5)
        
        boton_item(self.frame_menu, "Consomé ($8)", lambda: self.agregar_producto("Consomé", 8, 0), self.color_naranja).grid(row=8, column=0, pady=5)

        tk.Button(self.frame_menu, text="MEGA PROMO $205\n(10 Tacos + Consomé + Refresco)", 
                  bg=self.color_rojo, fg="white", font=("Arial", 11, "bold"), 
                  relief="flat", height=3, command=self.ventana_promo).grid(row=9, column=0, columnspan=3, pady=15, sticky="nsew")

        if self.rol_usuario == "Administrador":
            tk.Button(self.frame_menu, text="VER GRÁFICA DE VENTAS", bg=self.color_azul, fg="white", 
                      font=("Arial", 10, "bold"), relief="flat", height=2, command=graficas.mostrar_grafica_ventas).grid(row=10, column=0, columnspan=3, pady=5, sticky="nsew")

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
        self.win_promo = tk.Toplevel(self.root)
        self.win_promo.title("Configurar Mega Promo")
        self.win_promo.geometry("450x650")
        self.win_promo.configure(bg=self.color_fondo)
        self.win_promo.grab_set()

        tk.Label(self.win_promo, text="Personaliza los 10 Tacos", font=("Arial", 14, "bold"), bg=self.color_fondo).pack(pady=15)

        self.seleccion_promo = {
            "Barbacoa Blandos": tk.IntVar(value=0), "Barbacoa Medios": tk.IntVar(value=0),
            "Barbacoa Dorados": tk.IntVar(value=0), "Chicharrón": tk.IntVar(value=0),
            "Chorizo": tk.IntVar(value=0), "Bistec": tk.IntVar(value=0), "Campechano": tk.IntVar(value=0)
        }

        for carne in self.seleccion_promo:
            frame = tk.Frame(self.win_promo, bg=self.color_fondo)
            frame.pack(fill="x", padx=50, pady=4)
            color_lbl = "#D35400" if "Barbacoa" in carne else self.color_texto
            tk.Label(frame, text=f"{carne}:", font=("Arial", 10, "bold"), bg=self.color_fondo, fg=color_lbl, width=18, anchor="w").pack(side="left")
            tk.Spinbox(frame, from_=0, to=10, textvariable=self.seleccion_promo[carne], width=5, font=("Arial", 11), justify="center").pack(side="right")

        tk.Label(self.win_promo, text="* Bistec/Campechano +$3 c/u", font=("Arial", 9, "italic"), fg="red", bg=self.color_fondo).pack(pady=10)
        tk.Button(self.win_promo, text="AGREGAR PROMO AL TICKET", bg=self.color_verde, fg="white", font=("Arial", 11, "bold"),
                  relief="flat", height=2, command=self.confirmar_promo).pack(pady=20, fill="x", padx=60)

    def confirmar_promo(self):
        total_tacos = sum(var.get() for var in self.seleccion_promo.values())
        if total_tacos != 10:
            messagebox.showwarning("Error", f"Debes seleccionar 10 tacos. Llevas: {total_tacos}")
            return

        extra = (self.seleccion_promo["Bistec"].get() * 3) + (self.seleccion_promo["Campechano"].get() * 3)
        precio_final = 205 + extra
        detalles = [f"{var.get()} {carne}" for carne, var in self.seleccion_promo.items() if var.get() > 0]
        descripcion = "MEGA PROMO (" + ", ".join(detalles) + ")"

        self.total_actual += precio_final
        self.tree.insert("", "end", values=(1, descripcion, f"${precio_final}"))
        self.lbl_total.config(text=f"TOTAL: ${self.total_actual:.2f}")
        self.win_promo.destroy()

    def finalizar_venta(self):
        items = self.tree.get_children()
        if not items:
            messagebox.showwarning("Venta", "El ticket está vacío")
            return
        
        try:
            monto_pago = float(self.ent_pago.get()) if self.ent_pago.get() else self.total_actual
            cambio = monto_pago - self.total_actual
        except ValueError:
            messagebox.showerror("Error", "Monto de pago inválido")
            return

        direccion = self.ent_direccion.get() if self.ent_direccion.get() else "VENTA MOSTRADOR"
        carpeta = "Tickets_Generados"
        if not os.path.exists(carpeta): os.makedirs(carpeta)
        fecha_obj = datetime.datetime.now()
        nombre_pdf = os.path.join(carpeta, f"Ticket_{fecha_obj.strftime('%Y%m%d_%H%M%S')}.pdf")

        try:
            # --- CONFIGURACIÓN DE TICKET TÉRMICO (80mm de ancho) ---
            # Definimos un ancho de 80mm y un alto dinámico o largo
            pdf = FPDF(format=(80, 200)) 
            pdf.add_page()
            pdf.set_margins(5, 5, 5) # Márgenes pequeños como ticket real
            
            # ENCABEZADO
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 8, "TACOS ESTHER", ln=True, align="C")
            pdf.set_font("Arial", "", 8)
            pdf.cell(0, 4, "DESDE 2013", ln=True, align="C")
            pdf.cell(0, 4, "AV. OBSIDIANA SUR 20", ln=True, align="C") # Puedes cambiar tu dirección
            pdf.ln(3)

            # DATOS DE VENTA
            pdf.set_font("Arial", "", 9)
            pdf.cell(0, 5, f"FECHA: {fecha_obj.strftime('%d/%m/%Y %H:%M')}", ln=True)
            pdf.cell(0, 5, "CAJERO: ADMINISTRADOR", ln=True)
            pdf.cell(0, 5, f"FOLIO: {fecha_obj.strftime('%H%M%S')}", ln=True)
            pdf.ln(2)

            # LÍNEA DIVISORA
            pdf.cell(0, 2, "="*35, ln=True, align="C")
            
            # ENCABEZADO TABLA
            pdf.set_font("Arial", "B", 9)
            pdf.cell(10, 5, "CANT", 0, 0)
            pdf.cell(40, 5, "DESCRIPCION", 0, 0)
            pdf.cell(20, 5, "IMPORTE", 0, 1, 'R')
            pdf.cell(0, 2, "-"*45, ln=True, align="C")

            # PRODUCTOS
            pdf.set_font("Arial", "", 8)
            total_articulos = 0
            for item in items:
                v = self.tree.item(item)["values"]
                cant = str(v[0])
                prod = str(v[1]).upper() # En mayúsculas como la foto
                subt = str(v[2])
                total_articulos += int(v[0])

                # Manejo de texto largo para que no se encime
                # Usamos una sola celda para Cant y Subtotal y MultiCell para el nombre
                pos_y = pdf.get_y()
                pdf.cell(10, 5, cant, 0, 0)
                
                # Nombre del producto con ajuste de línea
                pdf.set_xy(15, pos_y)
                pdf.multi_cell(40, 5, prod, 0, 'L')
                
                # Volver a la derecha para el precio
                pdf.set_xy(55, pos_y)
                pdf.cell(15, 5, subt, 0, 1, 'R')

            pdf.cell(0, 2, "="*35, ln=True, align="C")
            pdf.ln(2)

            # TOTALES (Letra más grande y negrita)
            pdf.set_font("Arial", "", 9)
            pdf.cell(45, 6, f"NO. DE ARTICULOS: {total_articulos}", 0, 1)
            
            pdf.set_font("Arial", "B", 12)
            pdf.cell(40, 8, "TOTAL:", 0, 0)
            pdf.cell(30, 8, f"${self.total_actual:.2f}", 0, 1, 'R')
            
            pdf.set_font("Arial", "B", 10)
            pdf.cell(40, 6, "PAGO CON:", 0, 0)
            pdf.cell(30, 6, f"${monto_pago:.2f}", 0, 1, 'R')
            
            pdf.cell(40, 6, "SU CAMBIO:", 0, 0)
            pdf.cell(30, 6, f"${cambio:.2f}", 0, 1, 'R')
            pdf.ln(5)

            # PIE DE PÁGINA
            pdf.set_font("Arial", "B", 10)
            pdf.cell(0, 5, "*** COPIA DE TICKET ***", ln=True, align="C")
            pdf.ln(3)
            pdf.set_font("Arial", "", 8)
            pdf.cell(0, 4, "¡GRACIAS POR SU COMPRA!", ln=True, align="C")
            pdf.cell(0, 4, "VUELVA PRONTO", ln=True, align="C")
            pdf.ln(3)
            pdf.cell(0, 5, f"ENTREGA: {direccion}", ln=True, align="C")

            pdf.output(nombre_pdf)
            messagebox.showinfo("Éxito", "Ticket generado correctamente")
            
            # Limpiar interfaz
            self.ent_direccion.delete(0, tk.END)
            self.ent_pago.delete(0, tk.END)
            self.limpiar_ticket()

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar ticket: {e}")

    def ventana_termino_barbacoa(self, precio_base):
        self.win_termino = tk.Toplevel(self.root)
        self.win_termino.title("Término")
        self.win_termino.geometry("300x250")
        self.win_termino.configure(bg=self.color_blanco)
        self.win_termino.grab_set()
        tk.Label(self.win_termino, text="¿Cómo quiere su taco?", font=("Arial", 11, "bold"), bg=self.color_blanco).pack(pady=15)
        for t in ["Blando", "Medio", "Dorado"]:
            tk.Button(self.win_termino, text=t, width=20, height=2, bg=self.color_fondo, relief="flat",
                      command=lambda term=t: self.confirmar_barbacoa(term, precio_base)).pack(pady=5)

    def confirmar_barbacoa(self, termino, precio_base):
        nombre = f"Taco Barbacoa ({termino})"
        if self.con_queso.get():
            precio_base += 3
            nombre += " c/Q"
        self.total_actual += precio_base
        self.tree.insert("", "end", values=(1, nombre, f"${precio_base}"))
        self.lbl_total.config(text=f"TOTAL: ${self.total_actual:.2f}")
        self.win_termino.destroy()
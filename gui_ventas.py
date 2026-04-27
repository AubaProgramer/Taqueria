import tkinter as tk
from tkinter import ttk, messagebox
from fpdf import FPDF     
import datetime

class VentanaVentas:
    def __init__(self, root, nombre_usuario, rol_usuario):
        self.root = root
        self.root.title(f"Taquería - Ventas (Usuario: {nombre_usuario})")
        self.root.geometry("1100x700")
        
        self.ticket_lista = []
        self.total_actual = 0.0

        # Paneles principales
        self.frame_menu = tk.LabelFrame(root, text="Menú de Taquería", padx=10, pady=10)
        self.frame_menu.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.frame_ticket = tk.LabelFrame(root, text="Ticket de Venta", padx=10, pady=10)
        self.frame_ticket.pack(side="right", fill="both", padx=10, pady=10)

        self.crear_interfaz_comida()
        self.crear_interfaz_ticket()

    def crear_interfaz_comida(self):
        # --- SECCIÓN TACOS ---
        tk.Label(self.frame_menu, text="--- TACOS (18/21) ---", font=("Arial", 10, "bold")).grid(row=0, column=0, pady=5)
        
        carnes = [("Barbacoa", 18), ("Chicharrón", 18), ("Chorizo", 18), ("Bistec", 21), ("Campechano", 21)]
        for i, (carne, precio) in enumerate(carnes):
            tk.Button(self.frame_menu, text=carne, width=15, 
                      command=lambda c=carne, p=precio: self.agregar_producto(f"Taco {c}", p, 3)).grid(row=i+1, column=0, pady=2)

        # --- SECCIÓN LONCHES ---
        tk.Label(self.frame_menu, text="--- LONCHES (50/60) ---", font=("Arial", 10, "bold")).grid(row=0, column=1, pady=5)
        lonches = [("Barbacoa", 50), ("Chicharrón", 50), ("Chorizo", 50), ("Bistec", 60)]
        for i, (carne, precio) in enumerate(lonches):
            tk.Button(self.frame_menu, text=f"Lonche {carne}", width=15, 
                      command=lambda c=carne, p=precio: self.agregar_producto(f"Lonche {c}", p, 5)).grid(row=i+1, column=1, pady=2, padx=10)

        # --- SECCIÓN BEBIDAS ---
        tk.Label(self.frame_menu, text="--- BEBIDAS ---", font=("Arial", 10, "bold")).grid(row=0, column=2, pady=5)
        bebidas = [
            ("Coca 500ml", 26), ("Coca Medio", 21), ("Coca Taquera", 19),
            ("Refresco 400ml", 16), ("Jumex Vidrio", 22), ("Jumex Cartón", 14)
        ]
        for i, (nom, p) in enumerate(bebidas):
            tk.Button(self.frame_menu, text=nom, width=15, 
                      command=lambda n=nom, p=p: self.agregar_producto(n, p, 0)).grid(row=i+1, column=2, pady=2)

        # Extras y Otros
        self.con_queso = tk.BooleanVar()
        tk.Checkbutton(self.frame_menu, text="¿Lleva Queso?", variable=self.con_queso, font=("Arial", 12, "bold"), fg="blue").grid(row=7, column=0, columnspan=2, pady=20)
        
        tk.Button(self.frame_menu, text="Consomé ($8)", width=15, bg="#f39c12",
                  command=lambda: self.agregar_producto("Consomé", 8, 0)).grid(row=8, column=0)

        # --- BOTÓN MEGA PROMO ---
        tk.Button(self.frame_menu, text="MEGA PROMO $205\n(10 Tacos + Consomé + Refresco)", 
                  bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), height=3,
                  command=self.ventana_promo).grid(row=9, column=0, columnspan=3, pady=20, sticky="nsew")

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

    def agregar_producto(self, nombre, precio_base, costo_queso):
        precio = precio_base
        if self.con_queso.get() and costo_queso > 0:
            precio += costo_queso
            nombre += " c/Queso"
        
        self.total_actual += precio
        self.tree.insert("", "end", values=(1, nombre, f"${precio}"))
        self.lbl_total.config(text=f"TOTAL: ${self.total_actual:.2f}")

    def limpiar_ticket(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.total_actual = 0.0
        self.lbl_total.config(text="TOTAL: $0.00")

    def ventana_promo(self):
        # Ventana emergente para preguntar cuántos de bistec van en la promo
        promo_win = tk.Toplevel(self.root)
        promo_win.title("Configurar Mega Promo")
        promo_win.geometry("300x200")
        
        tk.Label(promo_win, text="¿Cuántos tacos son de Bistec?").pack(pady=10)
        cant_bistec = tk.Spinbox(promo_win, from_=0, to=10, width=5)
        cant_bistec.pack()
        
        def aplicar():
            b = int(cant_bistec.get())
            extra = b * 3
            total_promo = 205 + extra
            self.total_actual += total_promo
            self.tree.insert("", "end", values=(1, f"MEGA PROMO ({b} Bistec)", f"${total_promo}"))
            self.lbl_total.config(text=f"TOTAL: ${self.total_actual:.2f}")
            promo_win.destroy()
            
        tk.Button(promo_win, text="Agregar a Ticket", command=aplicar).pack(pady=20)

    def finalizar_venta(self):
        if self.total_actual == 0:
            messagebox.showwarning("Ticket vacío", "No hay productos para cobrar.")
            return

        # 1. Crear el nombre del archivo con fecha y hora
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombre_archivo = f"Ticket_{fecha_hora}.pdf"

        try:
            # 2. Generar el PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 20)
            pdf.cell(0, 10, "TACOS ESTHER - DESDE 2013", ln=True, align="C")
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, f"Fecha: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
            pdf.ln(10)

            # Encabezados de tabla
            pdf.set_font("Arial", "B", 12)
            pdf.cell(20, 10, "Cant", border=1)
            pdf.cell(120, 10, "Producto", border=1)
            pdf.cell(40, 10, "Precio", border=1, ln=True)

            # Contenido del ticket
            pdf.set_font("Arial", "", 12)
            for item in self.tree.get_children():
                valores = self.tree.item(item)["values"]
                pdf.cell(20, 10, str(valores[0]), border=1)
                pdf.cell(120, 10, str(valores[1]), border=1)
                pdf.cell(40, 10, str(valores[2]), border=1, ln=True)

            # Total
            pdf.ln(5)
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, f"TOTAL A PAGAR: ${self.total_actual:.2f}", ln=True, align="R")

            # Guardar el archivo
            pdf.output(nombre_archivo)
            
            messagebox.showinfo("Éxito", f"Venta registrada.\nTicket guardado como: {nombre_archivo}")
            self.limpiar_ticket()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF: {e}")
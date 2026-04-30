import tkinter as tk
from tkinter import messagebox
import auth  # Importamos tu archivo de seguridad

class VentanaLogin:
    def __init__(self, root):
        self.root = root
        # No ponemos title() aquí porque main.py ya maneja la ventana
        
        # Contenedor principal para centrar todo
        self.frame = tk.Frame(self.root, bg="#f0f0f0")
        self.frame.pack(expand=True, fill="both")

        # Título
        tk.Label(self.frame, text="TACOS ESTHER DESDE 2013", font=("Arial", 28, "bold"), bg="#f0f0f0", fg="#8B0000").pack(pady=20)
        tk.Label(self.frame, text="Acceso al Personal", font=("Arial", 12), bg="#f0f0f0", fg="#333").pack()

        # Campo: Usuario
        tk.Label(self.frame, text="Usuario:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=(30, 5))
        self.entry_user = tk.Entry(self.frame, font=("Arial", 12), width=25, justify="center")
        self.entry_user.pack()

        # Campo: Contraseña
        tk.Label(self.frame, text="Contraseña:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=(15, 5))
        self.entry_pass = tk.Entry(self.frame, font=("Arial", 12), width=25, show="*", justify="center")
        self.entry_pass.pack()

        # Botón de Ingreso
        # Nota: El comando se configura en main.py, pero dejamos uno por defecto por si acaso
        self.btn_entrar = tk.Button(self.frame, text="ENTRAR", font=("Arial", 12, "bold"), 
                                    bg="#28a745", fg="white", width=20, height=2, cursor="hand2")
        self.btn_entrar.pack(pady=40)

        # Pie de página
        tk.Label(self.frame, text="Versión 1.0 - Proyecto Taquería", font=("Arial", 8), bg="#f0f0f0", fg="gray").pack(side="bottom", pady=10)
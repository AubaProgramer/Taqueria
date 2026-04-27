import tkinter as tk
from tkinter import messagebox
import auth  # Aquí llamamos al archivo de seguridad que hiciste antes

class VentanaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Taquería - Acceso al Sistema")
        self.root.geometry("400x450")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Título
        tk.Label(root, text="BIENVENIDO", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333").pack(pady=20)
        tk.Label(root, text="Sistema de Gestión de Taquería", font=("Arial", 10), bg="#f0f0f0").pack()

        # Campo: Usuario
        tk.Label(root, text="Usuario:", font=("Arial", 12), bg="#f0f0f0").pack(pady=(30, 5))
        self.entry_user = tk.Entry(root, font=("Arial", 12), width=25)
        self.entry_user.pack()

        # Campo: Contraseña
        tk.Label(root, text="Contraseña:", font=("Arial", 12), bg="#f0f0f0").pack(pady=(15, 5))
        self.entry_pass = tk.Entry(root, font=("Arial", 12), width=25, show="*")
        self.entry_pass.pack()

        # Botón de Ingreso
        self.btn_entrar = tk.Button(root, text="Iniciar Sesión", font=("Arial", 12, "bold"), 
                                    bg="#28a745", fg="white", width=20, command=self.intentar_login)
        self.btn_entrar.pack(pady=40)

    def intentar_login(self):
        usuario = self.entry_user.get()
        clave = self.entry_pass.get()

        # Usamos la función de auth.py para validar
        datos_usuario = auth.verificar_usuario(usuario, clave)

        if datos_usuario:
            nombre, rol = datos_usuario
            messagebox.showinfo("Éxito", f"Bienvenido(a) {nombre}\nRol: {rol}")
            # Aquí después cerraremos esta ventana y abriremos el punto de venta
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Para probar la ventana sola
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaLogin(root)
    root.mainloop()
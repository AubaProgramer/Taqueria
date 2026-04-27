import tkinter as tk
from gui_login import VentanaLogin
from gui_ventas import VentanaVentas
import database
import auth

class AplicacionPrincipal:
    def __init__(self):
        database.crear_tablas() # Crea la DB al iniciar
        self.root = tk.Tk()
        self.root.title("Tacos Esther - Sistema de Gestión")
        
        # --- NUEVO: Escuchar el evento de Logout ---
        # Cuando en gui_ventas se ejecute event_generate("<<Logout>>"), 
        # esta línea hará que se llame automáticamente a mostrar_login
        self.root.bind("<<Logout>>", lambda e: self.mostrar_login())
        
        self.mostrar_login()
        self.root.mainloop()

    def mostrar_login(self):
        # Limpiamos la ventana (quita la pantalla de ventas si existe)
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Ajustamos el tamaño para que el login se vea centrado y pequeño
        self.root.geometry("400x550")
            
        self.app_login = VentanaLogin(self.root)
        # Configuramos el botón para validar datos
        self.app_login.btn_entrar.config(command=self.validar_y_entrar)

    def validar_y_entrar(self):
        user = self.app_login.entry_user.get()
        pas = self.app_login.entry_pass.get()
        
        datos = auth.verificar_usuario(user, pas)
        
        if datos:
            nombre, rol = datos
            self.mostrar_ventas(nombre, rol)
        else:
            from tkinter import messagebox
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def mostrar_ventas(self, nombre, rol):
        # Limpiamos la ventana del login
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Ajustamos el tamaño a uno más grande para el punto de venta
        self.root.geometry("1100x750")
        
        # Cargamos la interfaz de ventas
        VentanaVentas(self.root, nombre, rol)

if __name__ == "__main__":
    AplicacionPrincipal()
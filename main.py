import tkinter as tk
from gui_login import VentanaLogin
from gui_ventas import VentanaVentas
import database
import auth

class AplicacionPrincipal:
    def __init__(self):
        database.crear_tablas() # Crea la DB al iniciar
        self.root = tk.Tk()
        self.mostrar_login()
        self.root.mainloop()

    def mostrar_login(self):
        # Limpiamos la ventana si había algo antes
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.app_login = VentanaLogin(self.root)
        # Cambiamos el botón para que use nuestra función de validación
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
        # Limpiamos la ventana del login para poner la de ventas
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Cargamos la interfaz de ventas en la misma ventana principal
        VentanaVentas(self.root, nombre, rol)

if __name__ == "__main__":
    AplicacionPrincipal()
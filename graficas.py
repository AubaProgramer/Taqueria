import matplotlib.pyplot as plt
import database

def mostrar_grafica_ventas():
    datos = database.obtener_datos_grafica()
    
    if not datos:
        from tkinter import messagebox
        messagebox.showinfo("Sin Datos", "Aún no hay ventas registradas para graficar.")
        return

    productos = [d[0] for d in datos]
    totales = [d[1] for d in datos]

    plt.figure(figsize=(10, 6))
    plt.bar(productos, totales, color='skyblue', edgecolor='navy')
    plt.title('Ventas Totales por Producto - Tacos Esther')
    plt.xlabel('Productos')
    plt.ylabel('Ingresos ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
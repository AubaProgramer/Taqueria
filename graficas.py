import sqlite3
import matplotlib.pyplot as plt

def mostrar_grafica_ventas():
    conn = sqlite3.connect('taqueria.db')
    cursor = conn.cursor()
    
    # Consultamos cuánto se ha vendido de cada cosa
    cursor.execute('SELECT producto, SUM(precio) FROM ventas GROUP BY producto')
    datos = cursor.fetchall()
    conn.close()

    if not datos:
        print("No hay ventas registradas todavía.")
        return

    productos = [fila[0] for fila in datos]
    totales = [fila[1] for fila in datos]

    # Crear la gráfica
    plt.figure(figsize=(10, 6))
    plt.bar(productos, totales, color='orange')
    plt.title('Ventas Totales por Producto - Tacos Esther')
    plt.xlabel('Productos')
    plt.ylabel('Dinero Recaudado ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    mostrar_grafica_ventas()
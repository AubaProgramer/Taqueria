import matplotlib.pyplot as plt
import database
from fpdf import FPDF
import os

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


def exportar_grafica_a_pdf():
    # Esta función solo toma una "foto" de la gráfica actual y la guarda
    try:
        # 1. Guardamos la gráfica que ya generaste
        plt.savefig('reporte_grafico.png')
        
        # 2. Creamos el PDF aparte
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "REPORTE DE VENTAS - TACOS ESTHER", ln=True, align='C')
        pdf.ln(10)
        pdf.image('reporte_grafico.png', x=10, y=30, w=180)
        
        # 3. Lo guardamos en tu carpeta de tickets
        pdf.output("Tickets_Generados/Reporte_Estadistico.pdf")
        print("PDF del reporte generado con éxito.")
    except Exception as e:
        print(f"Error al exportar: {e}")
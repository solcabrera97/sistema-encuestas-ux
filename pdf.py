from fpdf import FPDF
from db import obtener_encuestas
from tkinter import messagebox
import matplotlib.pyplot as plt
import os

def calcular_porcentajes(lista_datos):
    total = len(lista_datos)
    if total == 0:
        return {}
    conteo = {}
    for item in lista_datos:
        conteo[item] = conteo.get(item, 0) + 1
    return {categoria: (cantidad / total) * 100 for categoria, cantidad in conteo.items()}

def generar_graficos_ux(encuestas):
    # Extraemos Satisfacción (índice 6)
    satisfaccion = [elem[6] for elem in encuestas]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    conteo_sat = {}
    for s in satisfaccion:
        conteo_sat[s] = conteo_sat.get(s, 0) + 1
        
    # --- Gráfico 1: Barras CSAT ---
    ax1.bar(conteo_sat.keys(), conteo_sat.values(), color='#2980b9')
    ax1.set_title('Métrica CSAT (Customer Satisfaction)', pad=15)
    ax1.set_ylabel('Cantidad de Usuarios')
    ax1.tick_params(axis='x', rotation=15) 
    
    # --- Gráfico 2: Torta CSAT ---
    colores = ['#2ecc71', '#3498db', '#f1c40f', '#e67e22', '#e74c3c']
    ax2.pie(conteo_sat.values(), labels=conteo_sat.keys(), autopct='%1.1f%%', startangle=90, colors=colores)
    ax2.set_title('Proporción de Satisfacción', pad=15)
    
    plt.tight_layout()
    plt.savefig('grafico_ux.png', bbox_inches='tight')
    plt.close()

def generar_pdf(encuestas):
    pdf = FPDF()
    pdf.add_page()
    
    # --- ENCABEZADO ---
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Resumen Ejecutivo: Experiencia de Usuario (UX)", ln=True, align='C')
    pdf.ln(8)
    
    # --- PROCESAMIENTO ---
    total_casos = len(encuestas)
    dispositivos = [elem[3] for elem in encuestas]
    exito = [elem[5] for elem in encuestas]
    
    porc_disp = calcular_porcentajes(dispositivos)
    porc_exito = calcular_porcentajes(exito)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "Métricas Clave de Usabilidad:", ln=True)
    pdf.ln(2)
    
    pdf.set_font("Arial", '', 11)
    pdf.cell(5) 
    pdf.cell(0, 7, f"- Muestra total evaluada: {total_casos} usuarios activos.", ln=True)
    
    # Punteos de Éxito de Tarea (Task Success Rate)
    for cat, porc in porc_exito.items():
        pdf.cell(5)
        pdf.cell(0, 7, f"- {cat}: {porc:.1f}% de las sesiones.", ln=True)
        
    # Punteos de Dispositivos
    for cat, porc in porc_disp.items():
        pdf.cell(5)
        pdf.cell(0, 7, f"- Adopción en {cat}: {porc:.1f}% de los usuarios.", ln=True)
        
    pdf.ln(10)
    
    # --- GRÁFICOS ---
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "Análisis de Satisfacción del Cliente (CSAT):", ln=True)
    pdf.ln(5)
    
    generar_graficos_ux(encuestas)
    pdf.image('grafico_ux.png', x=10, w=190)
    
    pdf.output("reporte_ux.pdf")
    try:
        os.remove('grafico_ux.png')
    except Exception:
        pass

def exportar_pdf():
    encuestas = obtener_encuestas()
    if not encuestas:
        messagebox.showwarning("Atención", "No hay datos para procesar el reporte.")
        return
    
    generar_pdf(encuestas)
    messagebox.showinfo("Éxito", "El reporte analítico UX se guardó como 'reporte_ux.pdf'.")
import tkinter as tk
from tkinter import ttk, messagebox
from db import conectar_db, crear_tabla, obtener_encuestas, obtener_encuesta_por_id, modificar_encuesta, eliminar_encuesta
from pdf import exportar_pdf

id_seleccionado = None

def limpiar_formulario():
    global id_seleccionado
    id_seleccionado = None
    entry_cliente.delete(0, tk.END)
    entry_edad.delete(0, tk.END)
    combo_dispositivo.set('')
    combo_frecuencia.set('')
    combo_exito.set('')
    combo_satisfaccion.set('')

def salir(ventana):
    if messagebox.askyesno("Salir", "¿Seguro que desea cerrar el sistema?"):
        ventana.destroy()

def insertar_datos():
    cliente = entry_cliente.get()
    edad = entry_edad.get()
    dispositivo = combo_dispositivo.get()
    frecuencia = combo_frecuencia.get()
    exito = combo_exito.get()
    satisfaccion = combo_satisfaccion.get() 

    with conectar_db() as base:
        try:
            if not cliente or not edad or not dispositivo or not frecuencia or not exito or not satisfaccion:
                raise ValueError("Todos los campos de la métrica son obligatorios.")
            
            if not str(edad).isdigit():
                raise ValueError("La variable 'edad' debe ser un número entero.")
            
            cursor = base.cursor()
            cursor.execute('''
                INSERT INTO encuestas_ux (cliente, edad, dispositivo, frecuencia_uso, exito_tarea, satisfaccion) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (cliente, int(edad), dispositivo, frecuencia, exito, satisfaccion))
            base.commit()
            
            messagebox.showinfo("Éxito", "Feedback de usuario registrado.")
            limpiar_formulario()
            actualizar_lista()
            
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))

def modificar_datos():
    global id_seleccionado
    if id_seleccionado is None:
        messagebox.showwarning("Atención", "Primero debe seleccionar un registro de la lista.")
        return

    cliente = entry_cliente.get()
    edad = entry_edad.get()
    dispositivo = combo_dispositivo.get()
    frecuencia = combo_frecuencia.get()
    exito = combo_exito.get()
    satisfaccion = combo_satisfaccion.get()

    try:
        if not cliente or not edad or not dispositivo or not frecuencia or not exito or not satisfaccion:
            raise ValueError("No puede dejar campos vacíos al modificar.")
        if not str(edad).isdigit():
            raise ValueError("La variable 'edad' debe ser numérica.")

        modificar_encuesta(id_seleccionado, cliente, int(edad), dispositivo, frecuencia, exito, satisfaccion)
        messagebox.showinfo("Éxito", "Los datos del usuario fueron actualizados.")
        limpiar_formulario()
        actualizar_lista()

    except ValueError as e:
        messagebox.showerror("Error", str(e))

def eliminar_datos():
    global id_seleccionado
    if id_seleccionado is None:
        messagebox.showwarning("Atención", "Seleccione un registro para archivar.")
        return

    if messagebox.askyesno("Confirmar Baja", "¿Está seguro de archivar este registro? (Baja Lógica)"):
        eliminar_encuesta(id_seleccionado)
        messagebox.showinfo("Éxito", "Registro archivado correctamente.")
        limpiar_formulario()
        actualizar_lista()

def seleccionar_caso(event):
    global id_seleccionado
    try:
        indice = listbox_casos.curselection()[0]
        texto_seleccionado = listbox_casos.get(indice)
        
        id_seleccionado = int(texto_seleccionado.split("|")[0].replace("ID:", "").strip())
        
        caso = obtener_encuesta_por_id(id_seleccionado)
        
        if caso:
            limpiar_formulario()
            id_seleccionado = caso[0]
            entry_cliente.insert(0, caso[1])
            entry_edad.insert(0, str(caso[2]))
            combo_dispositivo.set(caso[3])
            combo_frecuencia.set(caso[4])
            combo_exito.set(caso[5])
            combo_satisfaccion.set(caso[6])
    except IndexError:
        pass

def actualizar_lista():
    listbox_casos.delete(0, tk.END)
    encuestas = obtener_encuestas()
    for e in encuestas:
        # Mostramos ID, Cliente y Nivel de Satisfacción
        listbox_casos.insert(tk.END, f"ID: {e[0]} | Cliente: {e[1]} | CSAT: {e[6]}")

def main():
    crear_tabla()
    global entry_cliente, entry_edad, combo_dispositivo, combo_frecuencia, combo_exito, combo_satisfaccion, listbox_casos
    
    ventana = tk.Tk()
    ventana.title("Sistema de Métricas - UX Research")
    ventana.geometry("900x550")
    ventana.config(bg="#f4f0ec")

    frame_form = tk.Frame(ventana, bg="#2c3e50", padx=20, pady=20)
    frame_form.pack(side="left", fill="y")

    frame_lista = tk.Frame(ventana, bg="white", padx=20, pady=20)
    frame_lista.pack(side="right", fill="both", expand=True)

    tk.Label(frame_form, text="REGISTRO DE USABILIDAD", bg="#2c3e50", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

    tk.Label(frame_form, text="Cliente/Usuario:", bg="#2c3e50", fg="white").grid(row=1, column=0, sticky="e", pady=8)
    entry_cliente = tk.Entry(frame_form, width=23)
    entry_cliente.grid(row=1, column=1, pady=8)

    tk.Label(frame_form, text="Edad:", bg="#2c3e50", fg="white").grid(row=2, column=0, sticky="e", pady=8)
    entry_edad = tk.Entry(frame_form, width=23)
    entry_edad.grid(row=2, column=1, pady=8)

    tk.Label(frame_form, text="Dispositivo:", bg="#2c3e50", fg="white").grid(row=3, column=0, sticky="e", pady=8)
    combo_dispositivo = ttk.Combobox(frame_form, values=["Móvil", "Computadora", "Tablet"], state="readonly", width=20)
    combo_dispositivo.grid(row=3, column=1, pady=8)

    tk.Label(frame_form, text="Frecuencia:", bg="#2c3e50", fg="white").grid(row=4, column=0, sticky="e", pady=8)
    combo_frecuencia = ttk.Combobox(frame_form, values=["Diario", "Semanal", "Mensual", "Primera vez"], state="readonly", width=20)
    combo_frecuencia.grid(row=4, column=1, pady=8)

    tk.Label(frame_form, text="Éxito de la Tarea:", bg="#2c3e50", fg="white").grid(row=5, column=0, sticky="e", pady=8)
    combo_exito = ttk.Combobox(frame_form, values=["Completada fácilmente", "Completada con dificultad", "No completada"], state="readonly", width=20)
    combo_exito.grid(row=5, column=1, pady=8)

    tk.Label(frame_form, text="Satisfacción (CSAT):", bg="#2c3e50", fg="white").grid(row=6, column=0, sticky="e", pady=8)
    combo_satisfaccion = ttk.Combobox(frame_form, values=["1 - Muy insatisfecho", "2 - Insatisfecho", "3 - Neutral", "4 - Satisfecho", "5 - Muy satisfecho"], state="readonly", width=20)
    combo_satisfaccion.grid(row=6, column=1, pady=8)

    frame_botones = tk.Frame(frame_form, bg="#2c3e50")
    frame_botones.grid(row=7, column=0, columnspan=2, pady=20)

    btn_guardar = tk.Button(frame_botones, text="Guardar", bg="#27ae60", fg="white", font=("Arial", 9, "bold"), command=insertar_datos)
    btn_guardar.pack(side="left", padx=5)

    btn_modificar = tk.Button(frame_botones, text="Modificar", bg="#f39c12", fg="white", font=("Arial", 9, "bold"), command=modificar_datos)
    btn_modificar.pack(side="left", padx=5)

    btn_limpiar = tk.Button(frame_botones, text="Limpiar", bg="#7f8c8d", fg="white", font=("Arial", 9, "bold"), command=limpiar_formulario)
    btn_limpiar.pack(side="left", padx=5)

    tk.Label(frame_lista, text="BASE DE DATOS - FEEDBACK", bg="white", font=("Arial", 12, "bold")).pack(pady=(0, 10))

    listbox_casos = tk.Listbox(frame_lista, font=("Courier", 10))
    listbox_casos.pack(fill="both", expand=True)
    listbox_casos.bind('<<ListboxSelect>>', seleccionar_caso)

    frame_acciones = tk.Frame(frame_lista, bg="white")
    frame_acciones.pack(fill="x", pady=10)

    btn_eliminar = tk.Button(frame_acciones, text="Archivar", bg="#c0392b", fg="white", font=("Arial", 10, "bold"), command=eliminar_datos)
    btn_eliminar.pack(side="left", padx=5, expand=True)

    btn_reportes = tk.Button(frame_acciones, text="Reporte UX PDF", bg="#2980b9", fg="white", font=("Arial", 10, "bold"), command=exportar_pdf)
    btn_reportes.pack(side="left", padx=5, expand=True)

    btn_salir = tk.Button(frame_acciones, text="Salir", bg="#34495e", fg="white", font=("Arial", 10, "bold"), command=lambda: salir(ventana))
    btn_salir.pack(side="right", padx=5, expand=True)

    actualizar_lista()
    ventana.mainloop()

if __name__ == "__main__":
    main()
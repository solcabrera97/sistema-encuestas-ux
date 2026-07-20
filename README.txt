# Sistema de Gestión y Análisis de Métricas

Este proyecto es una aplicación de escritorio desarrollada íntegramente en **Python** para la recolección, gestión y análisis cuantitativo de métricas de Experiencia de Usuario (UX) y Satisfacción del Cliente (CSAT). 

Está diseñado para asegurar la integridad de los datos desde el momento de la carga (Data Entry) hasta la visualización de resultados (Data Analytics), evitando sesgos de tipeo mediante listas cerradas y validaciones estructurales.

## Características Principales

* **CRUD Completo:** Alta, lectura, modificación y archivo de registros.
* **Baja Lógica (Soft Delete):** Implementación de borrado seguro en base de datos para mantener el historial de auditoría y evitar la ruptura de IDs.
* **Interfaz Gráfica (GUI):** Formularios intuitivos desarrollados con `tkinter` para facilitar la recolección rápida de feedback en testeos de usabilidad.
* **Generación de Reportes Automáticos:** Procesamiento de la matriz de datos para calcular distribuciones de frecuencias y exportación a PDF con `fpdf`.
* **Visualización de Datos:** Creación de gráficos analíticos (barras y tortas) utilizando `matplotlib` para ilustrar la Tasa de Finalización de Tareas y el CSAT.

## Stack Tecnológico

* **Lenguaje:** Python 3.x
* **Base de Datos:** SQLite3 (Relacional, embebida)
* **Librerías Estándar:** `tkinter` (UI), `sqlite3` (Persistencia), `os`
* **Librerías Externas:** `matplotlib` (Data Viz), `fpdf` (Reportes)
* **Arquitectura:** Modular (Separación en Interfaz, Base de Datos y Motor Analítico)


## ⚙️ Instrucciones de Uso

1. Clonar el repositorio en tu máquina local.
2. Instalar las dependencias necesarias ejecutando: `pip install matplotlib fpdf`
3. Ejecutar el archivo principal: `python main.py`
4. El sistema creará automáticamente la base de datos `ux_research_data.db` en el primer inicio.

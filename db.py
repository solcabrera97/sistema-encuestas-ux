import sqlite3

def conectar_db():
    return sqlite3.connect('ux_research_data.db')

def crear_tabla():
    with conectar_db() as base:
        cursor = base.cursor()
        cursor.execute('''  
        CREATE TABLE IF NOT EXISTS encuestas_ux (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            cliente TEXT,  
            edad INTEGER,
            dispositivo TEXT,
            frecuencia_uso TEXT,
            exito_tarea TEXT,
            satisfaccion TEXT,
            activo INTEGER DEFAULT 1
        )
        ''')
        
        # Bloque de seguridad para actualizar la tabla si ya existía sin la columna activo
        try:
            cursor.execute("ALTER TABLE encuestas_ux ADD COLUMN activo INTEGER DEFAULT 1")
        except sqlite3.OperationalError:
            pass 
            
        base.commit()

def obtener_encuestas():
    with conectar_db() as base:
        cursor = base.cursor()
        # Solo trae los casos que NO fueron dados de baja (activo = 1)
        cursor.execute('SELECT * FROM encuestas_ux WHERE activo = 1')
        return cursor.fetchall()

def obtener_encuesta_por_id(id_encuesta):
    with conectar_db() as base:
        cursor = base.cursor()
        cursor.execute('SELECT * FROM encuestas_ux WHERE id = ? AND activo = 1', (id_encuesta,))
        return cursor.fetchone()

def modificar_encuesta(id_encuesta, cliente, edad, dispositivo, frecuencia, exito, satisfaccion):
    with conectar_db() as base:
        cursor = base.cursor()
        cursor.execute('''
            UPDATE encuestas_ux 
            SET cliente = ?, edad = ?, dispositivo = ?, frecuencia_uso = ?, exito_tarea = ?, satisfaccion = ?
            WHERE id = ?
        ''', (cliente, edad, dispositivo, frecuencia, exito, satisfaccion, id_encuesta))
        base.commit()

def eliminar_encuesta(id_encuesta):
    """Baja Lógica: Cambia el estado a inactivo (0) en lugar de borrar el registro."""
    with conectar_db() as base:
        cursor = base.cursor()
        cursor.execute('UPDATE encuestas_ux SET activo = 0 WHERE id = ?', (id_encuesta,))
        base.commit()
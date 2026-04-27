import sqlite3
import hashlib

def generar_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def crear_tablas():
    conn = sqlite3.connect('taqueria.db')
    cursor = conn.cursor()
    
    # Tabla de Usuarios (Para Esther, Carmen, Pablo, Axel)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            rol TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Tabla de Ventas (Para el CRUD y Gráficos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT NOT NULL,
            carne TEXT,
            con_queso INTEGER, -- 0 para No, 1 para Sí
            precio REAL NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            usuario_id INTEGER,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    ''')
    
    # Insertar a tu equipo si la tabla está vacía
    equipo = [
        ('Esther', 'Taquero', 'esther', 'labor123'),
        ('Carmen', 'Taquero', 'carmen', 'labor123'),
        ('Pablo', 'Mesero', 'pablo', 'labor123'),
        ('Axel', 'Mesero', 'axel', 'labor123'),
        ('Admin', 'Administrador', 'admin', 'admin123')
    ]
    
    for nom, rol, user, pw in equipo:
        try:
            cursor.execute('INSERT INTO usuarios (nombre, rol, username, password) VALUES (?, ?, ?, ?)',
                           (nom, rol, user, generar_hash(pw)))
        except sqlite3.IntegrityError:
            pass # Si ya existen, no los duplica
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    crear_tablas()
    print("Base de datos configurada con éxito.")
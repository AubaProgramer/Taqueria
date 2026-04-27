import sqlite3
import hashlib

def verificar_usuario(username, password):
    # Convertimos la contraseña que escribió el usuario a Hash para comparar
    pw_hash = hashlib.sha256(password.encode()).hexdigest()
    
    conn = sqlite3.connect('taqueria.db')
    cursor = conn.cursor()
    
    # Buscamos si existe el usuario con esa contraseña
    cursor.execute('SELECT nombre, rol FROM usuarios WHERE username = ? AND password = ?', 
                   (username, pw_hash))
    
    resultado = cursor.fetchone()
    conn.close()
    
    return resultado  # Regresa (Nombre, Rol) si existe, o None si no
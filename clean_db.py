import sqlite3

conn = sqlite3.connect('finance.db')
conn.row_factory = sqlite3.Row

# Remover categorias vazias
conn.execute('DELETE FROM categories WHERE name IS NULL OR TRIM(name) = ""')
conn.commit()

# Verificar resultado
categories = conn.execute('SELECT * FROM categories').fetchall()
print('Categorias após limpeza:')
for cat in categories:
    print(f'ID: {cat["id"]}, Nome: {cat["name"]}')

conn.close()

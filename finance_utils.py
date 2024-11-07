import sqlite3

conn = sqlite3.connect('finans_veritabani.db')
cursor = conn.cursor()

# Tablo oluşturma
cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    description TEXT,
    amount REAL,
    type TEXT
)''')

# Veri ekleme
cursor.execute("INSERT INTO transactions (date, description, amount, type) VALUES ('2024-06-28', 'Salary', 5000, 'gelir')")
conn.commit()

# Verileri görüntüleme
cursor.execute("SELECT * FROM transactions")
print(cursor.fetchall())

# Bağlantıyı kapatma
conn.close()
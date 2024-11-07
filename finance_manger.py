import sqlite3

# Veritabanı ve SQL bağlantı işlemleri
conn = sqlite3.connect('finans_veritabani.db')
cursor = conn.cursor()

# Veritabanında tablo oluşturma
cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    description TEXT,
    amount REAL,
    type TEXT)''')
conn.commit()

transactions = []


def display_menu():
    print("\nKişisel Finans Yöneticisi!")
    print("1. Yeni İşlem Ekle")
    print("2. İşlemleri Görüntüle")
    print("3. Özet Görüntüle")
    print("4. İşlem Ara")
    print("5. Verileri Dosyaya Kaydet")
    print("6. Dosyadan Verileri Yükle")
    print("7. Çıkış")


def add_transaction():
    date = input("Tarih girin (YYYY-MM-DD): ")
    description = input("Açıklama: ")
    amount = float(input("Miktar girin: "))
    type_ = input("Tür (gelir/gider): ").lower()

    if type_ not in ['gelir', 'gider']:
        print("Geçersiz tür! 'gelir' veya 'gider' girin.")
        return

    cursor.execute('INSERT INTO transactions (date, description, amount, type) VALUES (?, ?, ?, ?)',
                   (date, description, amount, type_))
    conn.commit()
    print("İşlem başarıyla eklendi!")



def view_transactions():
    start_date = input("Başlangıç tarihi (YYYY-MM-DD) veya hepsini görmek için Enter'a basın: ")
    end_date = input("Bitiş tarihi (YYYY-MM-DD) veya hepsini görmek için Enter'a basın: ")

    if start_date and end_date:
        cursor.execute("SELECT * FROM transactions WHERE date BETWEEN ? AND ?", (start_date, end_date))
    else:
        cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()

    for transaction in transactions:
        print(transaction)


def view_summary():
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'gelir'")
    total_income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'gider'")
    total_expense = cursor.fetchone()[0] or 0

    total_savings = total_income - total_expense

    print("----Özet----")
    print(f"Toplam Gelir: {total_income} /-")
    print(f"Toplam Gider: {total_expense} /-")
    print(f"Net Birikim: {total_savings} /-")

    cursor.execute('SELECT * FROM transactions')
    print(cursor.fetchall())  # Veritabanındaki tüm verileri yazdırır.


def search_transaction():
    user_input = input("Bir işlem aramak için bir açıklama girin: ")
    cursor.execute("SELECT * FROM transactions WHERE description LIKE ?", ('%' + user_input + '%',))
    transactions = cursor.fetchall()

    if transactions:
        for transaction in transactions:
            print(transaction)
    else:
        print("İşlem bulunamadı.")


def save_data():
    file_name = input("Verileri kaydetmek için dosya adı girin: ")
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()

    with open(file_name, 'w') as file:
        for transaction in transactions:
            file.write(f"{transaction}\n")
    print("Veriler başarıyla dosyaya kaydedildi.")


def load_data():
    file_name = input("Veri yüklemek için dosya adı girin: ")
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            date, description, amount, type_ = line.strip().split(',')
            cursor.execute('INSERT INTO transactions (date, description, amount, type) VALUES (?, ?, ?, ?)',
                           (date, description, float(amount), type_))
        conn.commit()
    print("Veriler başarıyla yüklendi.")


def main():
    while True:
        display_menu()
        choice = input("Seçiminizi yapın: ")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            view_summary()
        elif choice == "4":
            search_transaction()
        elif choice == "5":
            save_data()
        elif choice == "6":
            load_data()
        elif choice == "7":
            print("Çıkılıyor...")
            conn.close()
            break
        else:
            print("Geçersiz seçim. Lütfen geçerli bir seçenek girin.")


if __name__ == "__main__":
    main()
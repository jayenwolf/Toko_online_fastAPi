import sqlite3

conn = sqlite3.connect("inventory.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS produk (
        id INTEGER PRIMARY KEY,
        nama TEXT UNIQUE NOT NULL,
        stok INTEGER NOT NULL
    )
""")

conn.commit()

def get_semua_produk():
    cursor.execute("SELECT * FROM produk")
    data = cursor.fetchall()
    return [{"id": row[0], "nama": row[1], "stok": row[2]} for row in data]

def get_produk_by_id(produk_id):
    cursor.execute("SELECT * FROM produk WHERE id = ?", (produk_id,))
    row = cursor.fetchone()

    if row:
        return {"id": row[0],"nama": row[1], "stok": row[2]}
    else:
        return None

def tambah_produk(produk_id, nama, stok):
    try:
    # tanda ? ini berpungsi untuk mencegah sql injection
        cursor.execute("INSERT INTO produk (id, nama, stok) VALUES (?,?,?)", (produk_id, nama, stok))
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        # ini gagal kalau id sama namanya sudah terdaftar
        return False

def update_produk_by_id(produk_id, nama_baru=None, stok_baru=None):
    if get_produk_by_id is None:
        return False

    perintah = []
    data_value = []

    if nama_baru is not None:
        perintah.append("nama = ?")
        data_value.append(nama_baru)

    if stok_baru is not None:
        perintah.append("stok = ?")
        data_value.append(stok_baru)

    # menggabungkan code jadi satu kalimat
    query = "UPDATE produk SET " + ",".join(perintah) + " WHERE id = ?"
    data_value.append(produk_id)

    try:
        cursor.execute(query, tuple(data_value))
        conn.commit ()
        return True
    except sqlite3.IntegrityError:
        # untuk mengembalikan pesan fail
        return "Fail! nama tidak boleh sama"

def delete_produk(produk_id):
    # untuk melakukan delete produk
    cursor.execute("DELETE FROM produk WHERE id = ?", (produk_id,))
    conn.commit()

    if cursor.rowcount > 0:
        return True
    else:
        return False
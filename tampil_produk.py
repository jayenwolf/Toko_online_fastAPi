import psycopg2

try:
    koneksi = psycopg2.connect(
        user="postgres",
        password="1234", 
        host="localhost",
        port="5432",
        database="postgres" 
    )

# untuk mengambil data
    ambil_data = koneksi.cursor()

# perintah sql untuk menggunakan tabel produk
    ambil_data.execute("SELECT * FROM produk;")

# mengambil semua data 
    semua_produk = ambil_data.fetchall()

    print("daftar produk")

# untuk melakukan loop dan menapilkan data 
    for produk in semua_produk:
        print(produk)

        ambil_data.close()
        koneksi.close()

except Exception as error:
    print(" terjadi kesalahan:", error)

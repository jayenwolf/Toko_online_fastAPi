from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel 
from fastapi import FastAPI, File, UploadFile
import shutil
from fastapi.middleware.cors import CORSMiddleware
# Membuat aplikasi FastAPI
app = FastAPI()


# Tambahkan izin CORS ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Mengizinkan semua frontend mengakses
    allow_credentials=True,
    allow_methods=["*"],  # Mengizinkan semua method (GET, POST, PUT, DELETE)
    allow_headers=["*"],
)

class ProdukBaru(BaseModel):
    nama: str # kenapa harus str karena nama itu wajib teks
    harga: int # kenapa harga wajib angka karena bilangan bulat
    stok : int # kenapa stok wajib angka karena bilangan bulat

@app.get("/api/produk")
def ambil_semua_produk():
    try:
        koneksi = psycopg2.connect(
            user = "postgres",
            password = "1234",
            host = "localhost",
            port = "5432",
            database = "postgres"
        )

        # untuk mengambil RealDictCursor
        ambil_data = koneksi.cursor(cursor_factory=RealDictCursor) 

        # untuk mengambil semua data dan juga perintah sql untuk menggunkan tabel
        ambil_data.execute("SELECT * FROM produk;")
        semua_produk = ambil_data.fetchall()

        ambil_data.close()
        koneksi.close()

        return {"pesan": "Berhasil", "data": semua_produk}
    except Exception as error:
        return {"pesan": "Gagal!", "error": str(error)}

@app.post("/api/tambah-produk")
def tambah_produk(data: ProdukBaru):
    try:
        koneksi = psycopg2.connect(
            user = "postgres",
            password = "1234",
            host = "localhost",
            port = "5432",
            database = "postgres"
        )

        ambil_data = koneksi.cursor()

        command_sql = "INSERT INTO produk (nama, harga, stok) VALUES (%s, %s, %s)"
        data_isi = (data.nama.lower(), data.harga, data.stok)

        ambil_data.execute(command_sql, data_isi)
        koneksi.commit()

        ambil_data.close()
        koneksi.close()

        return {"pesan": f"Produk {data.nama} berhasil ditambahkan!"}

    except Exception as error:
        return {"pesan": "Gagal menambah produk", "error": str(error)}

@app.put("/api/ubah-produk/{id_produk}")
def ubah_produk(id_produk: int, data: ProdukBaru):
    try:
        koneksi = psycopg2.connect(
            user = "postgres",
            password = "1234",
            host = "localhost",
            port = "5432",
            database = "postgres"
        )

        ambil_data = koneksi.cursor()

        perintah_sql = "UPDATE produk SET nama = %s, harga = %s, stok = %s WHERE id = %s;"

        data_isi = (data.nama.lower(), data.harga, data.stok, id_produk)

        ambil_data.execute(perintah_sql, data_isi)
        koneksi.commit()  

        return {"pesan": f"Produk dengan ID {id_produk} berhasil diubah!"}

    except Exception as error:
        return {"pesan": "Gagal mengubah produk", "error": str(error)}

@app.delete("/api/hapus-produk/{id_produk}")
def hapus_produk(id_produk: int):
    try:
        koneksi = psycopg2.connect(
            user = "postgres",
            password = "1234",
            host = "localhost",
            port = "5432",
            database = "postgres"
        )
        ambil_data = koneksi.cursor()

        perintah_sql = "DELETE FROM produk WHERE id = %s;"

        ambil_data.execute(perintah_sql, (id_produk,))
        ambil_data.close()
        koneksi.close()

        return {"pesan": f"Produk dengan ID {id_produk} berhasil dihapus!"}

    except Exception as error:
        return {"pesan": "Gagal menghapus produk", "error": str(error)}

@app.post("/api/upload-gambar/{id_produk}")
def upload_gambar(id_produk: int, file: UploadFile = File(...)):
    try:
        # membuat rute lokasi penyimpanan (mengarah ke folder img)
        lokasi_simpan = f"img/{file.filename}"

        # untuk menyimpan file foto ke dalam folder berupa fisik(didalam folder img)
        with open(lokasi_simpan, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        koneksi = psycopg2.connect(
            user = "postgres",
            password = "1234",
            host = "localhost",
            port = "5432",
            database = "postgres"
        )

        ambil_data = koneksi.cursor()

        perintah_sql = "UPDATE produk SET gambar = %s WHERE id = %s;"

        ambil_data.execute(perintah_sql, (file.filename, id_produk))

        koneksi.commit()

        ambil_data.close()
        koneksi.close()

        
        return {"pesan": f"Gambar {file.filename} sukses disimpan untuk barang ID {id_produk}!"}
        
    except Exception as error:
        return {"pesan": "Gagal menyimpan gambar", "error": str(error)}

@app.patch("/produk/beli/{id_produk}")
def stok_kurang(id_produk: int):
    koneksi = psycopg2.connect(
        user="postgres", 
        password="1234", 
        database="postgres", 
        host="localhost", 
        port="5432"
    )

    ambil_data = koneksi.cursor()

    # mengurangi stok sebanyak 1 berdasarkan id ini perintah sqlnya
    command_sql = "UPDATE produk SET stok = stok - 1 WHERE id = %s RETURNING nama, stok;"

    try:
        ambil_data.execute(command_sql, (id_produk,))
        produk_update = ambil_data.fetchone() # untuk mengambil hasil update
        koneksi.commit() # menyimpan perubahan secara permanen

        if produk_update:
            return {"pesan": "Berhasil beli", "nama": produk_update[0], "stok_sisa": produk_update[1]}
        else:
            return {"pesan": "Produk tidak ditemukan"}
    except Exception as e:
        return {"error": str(e)}

    finally:
        ambil_data.close()
        koneksi.close()
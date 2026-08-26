from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel 
from fastapi import FastAPI, File, UploadFile
import shutil
from fastapi.middleware.cors import CORSMiddleware
from auth import acak_password, cek_pw
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# Membuat aplikasi FastAPI
app = FastAPI()

# untuk alat baca
security = HTTPBearer()

# Tambahkan izin CORS ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Mengizinkan semua frontend mengakses
    allow_credentials=True,
    allow_methods=["*"],  # Mengizinkan semua method (GET, POST, PUT, DELETE)
    allow_headers=["*"],
)

def verifikasi(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        # untuk membuat token menggunakan kunci rahasia yang sama saat login
        payload = jwt.decode(token, "rahasia123", algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="token tidak valid!"
            )
        return username
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="token salah"
        )
    
class ProdukBaru(BaseModel):
    nama: str # kenapa harus str karena nama itu wajib teks
    harga: int # kenapa harga wajib angka karena bilangan bulat
    stok : int # kenapa stok wajib angka karena bilangan bulat

class UserBaru(BaseModel):
    username: str
    password: str

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
def tambah_produk(data: ProdukBaru, username: str = Depends(verifikasi)):
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

@app.post("/api/register")
def register_admin(data: UserBaru):
    try:
        # untuk memasukan pw agar bisa diajak sebelum disimpan
        safe_pw = acak_password(data.password)

        # untuk membuat koneksi ke database postgreSQL nya

        koneksi = psycopg2.connect(
            user="postgres",
            password="1234",
            host="localhost",
            port="5432",
            database="postgres"
        )

        ambil_data = koneksi.cursor()

        # menyimpan username dan pw yang sdah di acak ke tabel user
        sql_command = "INSERT INTO users (username, password) VALUES (%s, %s)"

        # simpan permanen
        ambil_data.execute(sql_command, (data.username.lower(), safe_pw))
        koneksi.commit()

        ambil_data.close()
        koneksi.close()

        return {"pesan": f"Admin '{data.username}' berhasil didaftarkan dengan aman!"}

    except Exception as error:
        return {"pesan": "Gagal mendaftar admin", "error": str(error)}



pw = "rahasia123"


@app.post("/api/login")
def login_admin(data: UserBaru):
    try:
        # untuk membuat koneksi ke database mencari username
        koneksi = psycopg2.connect(
            user="postgres",
            password="1234",
            host="localhost",
            port="5432",
            database="postgres"
        )

        ambil_data = koneksi.cursor()

        # untuk mencari data user berdasarkan username
        perintah_sql = "SELECT id, username, password FROM users WHERE username = %s"
        ambil_data.execute(perintah_sql, (data.username.lower(),))
        user = ambil_data.fetchone()

        ambil_data.close()
        koneksi.close()

        # jika username tidak ditemukan
        if not user: 
            return{"pesan": "Username atau password salah!"}, 401

        # variable database user[0] = id, user[1] = username, user[2] = password_acak
        password_acakDB = user[2]

        # cocokan pw yang diketik dengan pw acak di database
        cek = cek_pw(data.password, password_acakDB)

        if not cek:
            return {"pesan": "Username atau password salah!"}, 401

        # jika cocok, bisa masuk
        payload = {"sub": user[1]} # untuk menyimpan username
        token_akses = jwt.encode(payload, pw, algorithm="HS256")

        return {
            "pesan": f"Login berhasil! Selamat datang kembali, {user[1]}",
            "token_akses": token_akses,
            "tipe_token": "bearer"
        }

    except Exception as error:
        return {"pesan": "Terjadi kesalahan saat login", "error": str(error)}, 500

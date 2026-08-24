# 🛒 Toko Online - FastAPI & Vanilla JavaScript

Proyek ini adalah sistem e-commerce sederhana yang dibangun dengan memisahkan arsitektur *Backend* (API) dan *Frontend*. Proyek ini dirancang untuk mempelajari konsep integrasi API, pengolahan database relasional, dan manipulasi DOM (Document Object Model) secara dinamis.

## 🚀 Teknologi yang Digunakan

**Backend:**
* [FastAPI](https://fastapi.tiangolo.com/) - Framework web Python untuk membangun API dengan cepat.
* [PostgreSQL](https://www.postgresql.org/) - Sistem manajemen database relasional.
* [Psycopg2](https://pypi.org/project/psycopg2/) - Adaptor database PostgreSQL untuk Python.
* [Uvicorn](https://www.uvicorn.org/) - Server ASGI secepat kilat untuk menjalankan FastAPI.

**Frontend:**
* HTML5
* CSS3 (Menggunakan Flexbox untuk tata letak modern)
* Vanilla JavaScript (Menggunakan Fetch API untuk mengambil data dari server)

## ✨ Fitur Utama

* **Tampil Produk Dinamis:** Mengambil dan menampilkan daftar produk langsung dari database ke layar web.
* **Manajemen Produk (CRUD):** 
  * Tambah produk baru.
  * Ubah detail produk (Nama, Harga, Stok).
  * Hapus produk.
* **Upload Gambar Terintegrasi:** Mendukung pengunggahan file gambar fisik ke folder lokal sekaligus menyimpan nama file-nya secara permanen ke dalam database PostgreSQL.
* **CORS Policy Terkonfigurasi:** Middleware backend sudah diatur agar aman dan dapat berkomunikasi dengan frontend dari *origin* yang berbeda.

## 🛠️ Persiapan dan Instalasi

Jika kamu ingin menjalankan proyek ini di komputer lokal, ikuti langkah-langkah berikut:

### 1. Konfigurasi Database
Pastikan PostgreSQL sudah terinstal dan berjalan di komputermu.
* **User:** `postgres`
* **Password:** `1234`
* **Database:** `postgres`
* **Port:** `5432`

Buat tabel `produk` di dalam database tersebut dengan kolom yang sesuai (id, nama, harga, stok, gambar).

### 2. Menjalankan Backend (Server FastAPI)
Buka terminal, masuk ke folder proyek, dan aktifkan *virtual environment* (jika ada). Jalankan perintah berikut untuk menyalakan server API:
```bash
uvicorn server:app --reload

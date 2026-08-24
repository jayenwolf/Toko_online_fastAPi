from fastapi import FastAPI, HTTPException
from model import Produk, UpdateProduk
from storage import (
    get_semua_produk,
    tambah_produk,
    get_produk_by_id,
    update_produk_by_id,
    delete_produk
)

app = FastAPI()

@app.get("/produk/{produk_id}", response_model=Produk)
def cari_produk(produk_id: int):
    hasil = get_produk_by_id(produk_id)
    if hasil is None:
        raise HTTPException(
            status_code=404,
            detail="produk id tidak ditemukan"
        )
    return hasil

@app.get("/produk")
def ambil_semua_produk():
    database = get_semua_produk()
    return database

@app.post("/produk", status_code=201, response_model=Produk, name="Tambah produk")
def buat_produk(data: Produk):
    nama_barang = data.nama.lower()
    
    
    hasil = tambah_produk(data.id, nama_barang, data.stok)

    if hasil == False:
        raise HTTPException(
            status_code=400,
            detail="Fail! id atau nama produk sudah terpakai"
        )
    return data

@app.patch("/produk/{produk_id}", response_model=Produk)
def update_produk(produk_id: int, data: UpdateProduk):
    hasil = update_produk_by_id(produk_id, data.nama, data.stok)

    if hasil == False:
        raise HTTPException(
            status_code=404,
            detail="produk tidak ditemukan"
        )

    if hasil == "Fail! nama tidak boleh sama":
        raise HTTPException(
            status_code=400,
            detail="Fail! Nama produk tersebut telah dipakai"
        )

    produk_baru = get_produk_by_id(produk_id)
    return produk_baru

@app.delete("/produk/{produk_id}")
def hapus_produk(produk_id: int):
    hasil = delete_produk(produk_id)

    if hasil == False:
        raise HTTPException(
            status_code=404,
            detail="produk tidak ditemukan"
        )
    return {"message": "produk berhasil dihapus"}
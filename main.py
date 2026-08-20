from fastapi import FastAPI, HTTPException

from model import(Produk, UpdateProduk)

from storage import(
    muat_produk,
    simpan_produk
)


app = FastAPI()

produk = muat_produk()

@app.get("/produk/filter")
def filter_produk(nama: str, stok: int):
    for item in produk:
        if item["nama"] == nama and item["stok"] == stok:
            return item

    raise HTTPException(
        status_code=404,
        detail="produk tidak tersedia"
    )

@app.get("/produk/{produk_id}", response_model=Produk)
def cari_produk(produk_id: int):
    for item in produk:
        if item["id"] == produk_id:
            return item

    raise HTTPException(
        status_code=404,
        detail="produk id tidak ditemukan"
    )

@app.get("/produk")
def ambil_semua_produk():
    return produk

@app.post("/produk", status_code=201, response_model=Produk)
def tambah_produk(data: Produk):
    for item in produk:
        if item["id"] == data.id:
            raise HTTPException(
                status_code=400,
                detail="id produk sudah ada"
            )

        elif item["nama"].lower() == data.nama.lower():
            raise HTTPException(
                status_code=400,
                detail="nama tidak boleh sama"
            )


    produk.append({
        "id": data.id,
        "nama": data.nama,
        "stok": data.stok
    })
    simpan_produk(produk)
    return data

@app.patch("/produk/{produk_id}", response_model=Produk)
def update_produk(produk_id: int, data: UpdateProduk):
    for item in produk:
        if item["id"] == produk_id:
            data_perubahan = data.model_dump(exclude_unset=True)
            item.update(data_perubahan)
            simpan_produk(produk)
            return item

    raise HTTPException(
        status_code=404,
        detail="produk tidak ditemukan"
    )

@app.delete("/produk/{produk_id}")
def hapus_produk(produk_id: int):
    for item in produk:
        if item["id"] == produk_id:
            produk.remove(item)
            simpan_produk(produk)
            return "produk berhasil dihapus"

    raise HTTPException(
        status_code=404,
        detail="produk tidak ditemukan"
    )


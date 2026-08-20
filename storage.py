import json
def simpan_produk(data):
    with open("produk.json", "w") as file:
        json.dump(data, file, indent=4)

def muat_produk():
    try:
        with open("produk.json", "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []

produk = muat_produk()
// 1. Mengambil data dari backend FastAPI
fetch("http://localhost:8000/api/produk")
    .then(response => response.json())
    .then(dataApi => {
        console.log("Data berhasil diambil:", dataApi);

        const daftarProduk = dataApi.data; // Mengambil array data dari JSON
        const wadah = document.getElementById("wadah-produk");

        // Kosongkan wadah teks "Memuat..." sebelumnya
        wadah.innerHTML = "";

        // 2. Perulangan (looping) untuk membuat kartu produk satu per satu
        daftarProduk.forEach(item => {
            const kartu = `
                <div class="kartu-produk">
                    <img src="../img/${item.gambar ? item.gambar : 'default.png'}" alt="${item.nama}" width="200">
                    <h2>${item.nama}</h2>
                    <p>Rp ${item.harga}</p>
                    <button type="button">Beli Sekarang</button>
                </div>
            `;
            
            // Masukkan kartu ke dalam HTML
            wadah.innerHTML += kartu;
        });
    })
    .catch(error => {
        console.error("Gagal terhubung ke API:", error);
        const wadah = document.getElementById("wadah-produk");
        wadah.innerHTML = "<p style='color: red;'>Gagal memuat produk dari server.</p>";
    });
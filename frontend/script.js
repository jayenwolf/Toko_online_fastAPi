fetch("http://localhost:8000/api/produk")
    .then(response => response.json())
    .then(dataApi => {
        const daftarProduk = dataApi.data;
        const wadah = document.getElementById("wadah-produk");
        wadah.innerHTML = "";

        

        daftarProduk.forEach(item => {

            // memperisiapkan variable kosong untuk tombol
        let tombolBeli ="";

        // logic nya (if / else)
            if (item.stok > 0) {        
                tombolBeli =`<button type="button" onclick="beliProduk(${item.id}, '${item.nama}', ${item.harga})">Beli Sekarang</button>`;

            } else {
                tombolBeli = `<button type="button" disabled style="background-color: gray; cursor: not-allowed;">Stok Habis</button>`;
            }

            const kartu = `
                <div class="kartu-produk">
                    <img src="../img/${item.gambar ? item.gambar : 'default.png'}" alt="${item.nama}" width="200">
                    <h2>${item.nama}</h2>
                    <p>Rp ${item.harga}</p>
                    <p>Sisa stok: ${item.stok}</p>
                    
                    ${tombolBeli}
                </div>
            `;
            wadah.innerHTML += kartu;
        });
    })
    .catch(error => {
        console.error("Gagal terhubung ke API:", error);
        const wadah = document.getElementById("wadah-produk");
        wadah.innerHTML = "<p style='color: red;'>Gagal memuat produk dari server.</p>";
    });



function beliProduk(id_produk, namaProduk, hargaProduk) {
    // untuk menentukan alamt url. tempel id produk
    const urlWEB = `http://localhost:8000/produk/beli/${id_produk}`;

    // untuk menghubungkan ke fetch
    fetch(urlWEB, {
        method: "PATCH" // untuk tahu ini adalah proses update/PATCH dan bukan GET
    })

    // untuk melakukan balasan dari code backend/dari backendnya
    .then(response => response.json())

    .then(dataAPI =>{
        // untuk memunculkan pemberitahuan
        alert(`Berhasil!\n${dataAPI.nama} terbeli.\nSisa stok di gudang sekarang: ${dataAPI.stok_sisa}`)

        // untuk refresh halaman otomatis jika stok terbaru langsung ada
        window.location.reload();
    })
    
    // jika ada eror maka akan memunculkan pesan dibawah
    .catch(error => {
        console.error("Gagal membeli:", error);
        alert("Maaf, gagal memproses pembelian.");
    });
}
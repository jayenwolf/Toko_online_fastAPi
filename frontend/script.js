fetch("http://localhost:8000/api/produk")
    .then(response => response.json())
    .then(dataApi => {
        const daftarProduk = dataApi.data;
        const wadah = document.getElementById("wadah-produk");
        wadah.innerHTML = "";

        daftarProduk.forEach(item => {
            // mempersiapkan variabel kosong untuk tombol
            let tombolBeli = "";
            let tombolHapus = "";

            // logic nya (if / else) untuk tombol beli
            if (item.stok > 0) {        
                tombolBeli = `<button type="button" onclick="beliProduk(${item.id}, '${item.nama}', ${item.harga})">Beli Sekarang</button>`;
            } else {
                tombolBeli = `<button type="button" disabled style="background-color: gray; cursor: not-allowed;">Stok Habis</button>`;
            }

            // Munculkan tombol hapus hanya jika token admin tersedia di browser
            if (localStorage.getItem("token_jwt")) {
                tombolHapus = `<button type="button" onclick="hapusProduk(${item.id})" style="background-color: #d9534f; color: white; margin-top: 5px; display: block;">Hapus Produk</button>`;
            }

            const kartu = `
                <div class="kartu-produk">
                    <img src="../img/${item.gambar ? item.gambar : 'default.png'}" alt="${item.nama}" width="200">
                    <h2>${item.nama}</h2>
                    <p>Rp ${item.harga}</p>
                    <p>Sisa stok: ${item.stok}</p>
                    ${tombolBeli}
                    ${tombolHapus}
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
    const urlWEB = `http://localhost:8000/produk/beli/${id_produk}`;

    fetch(urlWEB, {
        method: "PATCH"
    })
    .then(response => response.json())
    .then(dataAPI => {

        if (dataAPI.stok_sisa !== undefined) {
            alert(
                `Berhasil!\n${dataAPI.nama} terbeli.\n` +
                `Sisa stok di gudang sekarang: ${dataAPI.stok_sisa}`
            );

            window.location.reload();

        } else {
            alert(dataAPI.pesan || "Produk gagal dibeli.");
        }
    })
    .catch(error => {
        console.error("Gagal membeli:", error);
        alert("Maaf, gagal memproses pembelian.");
    });
}


// Menambahkan fungsi login admin
async function prosesLogin() {
    const u = document.getElementById("usernameInput").value;
    const p = document.getElementById("passwordInput").value;
    const statusText = document.getElementById("pesanStatus");

    try {
        const response = await fetch("http://127.0.0.1:8000/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: u,
                password: p
            })
        });

        const hasil = await response.json();

        if (response.ok) {
            statusText.style.color = "green";
            statusText.innerText = hasil.pesan;

            // Menyimpan token jwt ke browser
            localStorage.setItem("token_jwt", hasil.token_akses);
            alert("Login berhasil! Token JWT telah disimpan.");
            cekStatusLogin();
            window.location.reload();
        } else {
            statusText.style.color = "red";

            statusText.innerText =
                hasil.detail || hasil.pesan || "Username atau password salah!";
        }
    } catch (error) {
        console.error("Terjadi kesalahan:", error);
        statusText.style.color = "red";
        statusText.innerText = "Tidak dapat terhubung ke server FastAPI!";
    }
}


// Menambahkan fungsi kirim produk baru (Khusus Admin)
async function kirimProdukBaru() {
    const nama = document.getElementById("namaProdukBaru").value;
    const harga = parseInt(document.getElementById("hargaProdukBaru").value);
    const stok = parseInt(document.getElementById("stokProdukBaru").value);
    const pesanStatus = document.getElementById("pesanTambahStatus");

    const token = localStorage.getItem("token_jwt");

    if (!token) {
        pesanStatus.style.color = "red";
        pesanStatus.innerText = "Akses ditolak! Silakan login admin terlebih dahulu.";
        return;
    }

    try {
        const response = await fetch("http://localhost:8000/api/tambah-produk", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                nama: nama,
                harga: harga,
                stok: stok
            })
        });

        const hasil = await response.json();

        if (response.ok) {
            pesanStatus.style.color = "green";
            pesanStatus.innerText = hasil.pesan;
            alert("Berhasil menambah produk!");
            window.location.reload();
        } else {
            pesanStatus.style.color = "red";
            pesanStatus.innerText = hasil.detail || hasil.pesan || "Gagal menambah produk!";
        }
    } catch (error) {
        console.error("Terjadi kesalahan:", error);
        pesanStatus.style.color = "red";
        pesanStatus.innerText = "Tidak dapat terhubung ke server!";
    }
}


// Cek status saat halaman dibuka
function cekStatusLogin() {
    const token = localStorage.getItem("token_jwt");
    const panelAdmin = document.getElementById("panelAdmin");
    const containerLogin = document.querySelector(".login-container");

    if (token) {
        if (panelAdmin) panelAdmin.style.display = "block";
        if (containerLogin) containerLogin.style.display = "none";
    } else {
        if (panelAdmin) panelAdmin.style.display = "none";
        if (containerLogin) containerLogin.style.display = "block"; // Diperbaiki dari .display menjadi .style.display
    }
}

cekStatusLogin();


// Logout admin
function prosesLogout() {
    localStorage.removeItem("token_jwt"); // Diperbaiki dari remove.item menjadi removeItem
    alert("Anda telah logout.");
    window.location.reload();
}


// Hapus produk khusus admin
async function hapusProduk(id_produk) {
    const token = localStorage.getItem("token_jwt");
    if (!token) {
        alert("Akses ditolak, anda bukan admin");
        return;
    }

    if (!confirm("Yakin ingin menghapus produk ini?")) return;

    try {
        const response = await fetch(`http://localhost:8000/api/hapus-produk/${id_produk}`, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${token}` 
            }
        });

        const hasil = await response.json();

        if (response.ok) {
            alert(hasil.pesan);
            window.location.reload();
        } else {
            alert(hasil.detail || hasil.pesan || "Gagal menghapus produk!");
        }
    } catch (error) {
        console.error("Terjadi kesalahan:", error);
        alert("Tidak dapat terhubung ke server!");
    }
}
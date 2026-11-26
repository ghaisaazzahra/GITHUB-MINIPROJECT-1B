# GITHUB-MINIPROJECT-1B
# Pengembangan Program Rekomendasi Tanaman dan Diagnosis Kesesuaian Parameter Lahan Pertanian Berdasarkan Dataset Tanah dan Iklim Menggunakan Python

**Mini Project Praktikum Programa Komputer 2026**  
**Laboratorium Sistem Informasi dan Keputusan (LSIK) - Departemen Teknik Industri**  
**Universitas Andalas**


## Deskripsi Proyek
Pemilihan jenis tanaman yang kurang sesuai dengan kondisi unsur hara tanah dan iklim berisiko membuat pertumbuhan tanaman tidak optimal. Program berbasis Python ini dirancang untuk membantu petani, mahasiswa, dan pengelola lahan dalam mengevaluasi kesesuaian lahan secara terstruktur dan praktis. 

Program ini memiliki dua fungsi utama berbasis aturan (*rule-based*):
1. **Rekomendasi Komoditas:** Menghitung skor kecocokan (0–100) berdasarkan selisih dan rentang historis (`min`, `mean`, `max`) dari dataset untuk menampilkan peringkat tanaman yang paling sesuai.
2. **Diagnosis Parameter Lahan:** Menganalisis setiap parameter tanah dan iklim pengguna terhadap komoditas target pilihan untuk menentukan status kesesuaiannya (**Kurang**, **Sesuai**, atau **Berlebih**) beserta selisih nilainya.

## Dataset
* **Nama File:** `Crop_recommendation 2000.csv`
* **Sumber:** [Crop Recommendation Dataset - Kaggle](https://www.kaggle.com/datasets/madhuraatmarambhagat/crop-recommendation-dataset) (Dipublikasikan tahun 2024)
* **Parameter yang Digunakan:** *Nitrogen* (`N`), *Fosfor* (`P`), *Kalium* (`K`), tingkat keasaman tanah (`pH`), suhu udara (*temperature*), kelembapan (*humidity*), dan curah hujan (*rainfall*).

## Rancangan Program (IPO)

### 1. Input
* File dataset CSV (`Crop_recommendation 2000.csv`).
* Nilai 7 parameter kondisi tanah dan iklim pengguna:
  * Nitrogen (`N`: 80–150 ppm)
  * Fosfor (`P`: 15–35 ppm)
  * Kalium (`K`: 60–130 ppm)
  * Tingkat keasaman tanah (`pH`: 0–14)
  * Suhu udara (*temperature*: 20–32 °C)
  * Kelembapan (*humidity*: 65–90%)
  * Curah hujan (*rainfall*: 120–300 mm/bulan)
* Jumlah peringkat rekomendasi teratas yang ingin ditampilkan.
* Pilihan nama komoditas target untuk didiagnosis.

### 2. Proses
1. Membaca dan memvalidasi kelengkapan kolom dataset CSV.
2. Meminta dan memvalidasi seluruh input parameter lahan dari pengguna.
3. Mengelompokkan data berdasarkan label komoditas serta menghitung nilai minimum, maksimum, dan rata-rata untuk ketujuh parameter.
4. Menghitung skor kecocokan (0–100) menggunakan logika *rule-based* (selisih nilai input terhadap nilai rata-rata dan rentang `min-max` dataset).
5. Mengurutkan komoditas dari skor kecocokan tertinggi ke terendah.
6. Membandingkan parameter lahan pengguna terhadap rentang data acuan komoditas target untuk menentukan status (**Kurang**, **Sesuai**, atau **Berlebih**).

### 3. Output
* Laporan ringkas pembacaan dataset dan ringkasan input parameter pengguna.
* Daftar peringkat rekomendasi komoditas teratas lengkap dengan skor kecocokan (0–100).
* Tabel rincian hasil diagnosis tiap parameter lahan (nilai input, `min`, `mean`, `max`, status kesesuaian, dan selisih nilai).
* Pesan peringatan apabila file dataset bermasalah, input di luar rentang, atau nama komoditas target tidak ditemukan.

## Struktur Repositori
* `Crop_recommendation 2000.csv` : Dataset acuan kondisi tanah dan iklim.
* `python mp.py` : *Source code* utama program Python.
* `README.md` : Dokumentasi proyek mini.

## Cara Menjalankan Program
1. Pastikan **Python 3** sudah terinstal di komputer Anda.
2. Unduh seluruh file dari repositori ini atau lakukan *clone* melalui terminal/CMD:
   ```bash
   git clone https://github.com
   ```
3. Masuk ke dalam folder direktori proyek:
   ```bash
   cd GITHUB-MINIPROJECT-1B
   ```
4. Pastikan file dataset `Crop_recommendation 2000.csv` berada di dalam folder yang sama dengan *source code*, lalu jalankan program dengan perintah:
   ```bash
   python "python mp.py"
   ```
5. Ikuti instruksi pada layar terminal untuk memasukkan 7 nilai parameter lahan, jumlah peringkat rekomendasi teratas, dan nama komoditas target yang ingin didiagnosis.

## Anggota Kelompok 1B
1. **Aira Arifatunnisa**      (`2610933039`)
2. **Ghaisa Faridah Azzahra** (`2610932017`)
3. **Nur Azizah Ramadani**    (`2610931010`)
4. **Zahra Oktafiani**        (`2610931006`)

**Asisten Pembimbing:** Salma Livana  
**Dosen Pengampu:** Dr. Eng. Ir. Ardhian Agung Yulianto, S. Kom., M.T.

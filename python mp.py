import csv

NAMA_FILE = "Crop_recommendation 2000.csv"
PARAMETER = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

INFO_INPUT = {
    "N": "Nitrogen/N (0-140 ppm)",
    "P": "Fosfor/P (5-145 ppm)",
    "K": "Kalium/K (5-205 ppm)",
    "temperature": "Suhu (8,83-43,68 °C)",
    "humidity": "Kelembapan (14,26-99,98 %)",
    "ph": "pH Tanah (20,21-298,56)",
    "rainfall": "Curah Hujan (120-300 mm/bulan)"}
NAMA_TAMPIL = {
    "N": "Nitrogen (N)",
    "P": "Fosfor (P)",
    "K": "Kalium (K)",
    "temperature": "Suhu",
    "humidity": "Kelembapan",
    "ph": "pH",
    "rainfall": "Curah Hujan"}

data = {}
sudah_ada = []
valid = 0
baris_invalid = []

try:
    file = open(NAMA_FILE, mode="r", encoding="utf-8-sig")
    baris_pertama = file.readline()
    pemisah = ";" if ";" in baris_pertama else ","
    file.seek(0)

    pembaca = csv.DictReader(file, delimiter=pemisah)
    if pembaca.fieldnames is None:
        print("[ERROR] File CSV kosong.")
        exit()

   baris_terakhir = 1  
    for row in pembaca:
        no_baris = pembaca.line_num
        for b in range(baris_terakhir + 1, no_baris):
            baris_invalid.append((b, "baris kosong"))
        baris_terakhir = no_baris
        try:
            tanaman = (row["label"] or "").strip().lower()
            if tanaman == "":
                baris_invalid.append((no_baris, "label kosong"))
                continue

            angka = []
            salah = False
            for p in PARAMETER:
                mentah = row[p]
                if mentah is None or mentah.strip() == "":
                    baris_invalid.append((no_baris, f"{p} kosong/tidak lengkap"))
                    salah = True
                    break
                nilai = float(mentah.replace(",", "."))
                if nilai < 0:
                    baris_invalid.append((no_baris, f"{p} negatif"))
                    salah = True
                    break
                angka.append(nilai)
            if salah:
                continue

            baris_cek = (tanaman, tuple(angka))
            if baris_cek in sudah_ada:
                baris_invalid.append((no_baris, "data duplikat"))
                continue
            sudah_ada.append(baris_cek)

            if tanaman not in data:
                data[tanaman] = {p: [] for p in PARAMETER}
            for i in range(7):
                data[tanaman][PARAMETER[i]].append(angka[i])

            valid += 1
        except ValueError:
            baris_invalid.append((no_baris, f"{p} bukan angka"))
    file.close()
    for b in range(baris_terakhir + 1, pembaca.line_num + 1):
        baris_invalid.append((b, "baris kosong"))

except FileNotFoundError:
    print(f"[ERROR] File '{NAMA_FILE}' tidak ditemukan!")
    exit()

if valid == 0:
    print("[ERROR] Tidak ada data valid di dalam CSV.")
    exit()

aturan = {}
for tanaman in data:
    aturan[tanaman] = {}
    for p in PARAMETER:
        kumpulan = data[tanaman][p]
        aturan[tanaman][p] = {
            "min": min(kumpulan),
            "max": max(kumpulan),
            "mean": sum(kumpulan) / len(kumpulan)
            "n": len(kumpulan)}
        
print("=" * 65)
print("SISTEM REKOMENDASI & DIAGNOSIS KESESUAIAN LAHAN PERTANIAN".center(65))
print("=" * 65)
invalid = len(baris_invalid)
print(f"[INFO] Berhasil memuat CSV ({valid} data valid, {invalid} tidak valid, {len(aturan)} tanaman).")

if invalid > 0:
    print("[PERINGATAN] Data tidak valid ditemukan pada baris:")
    for no_baris, alasan in baris_invalid:
        print(f"  - Baris ke-{no_baris}: {alasan}")
komoditas = sorted(aturan.keys())

while True:
    print("\n1. Rekomendasi & Diagnosis")
    print("2. Cek Batasan Acuan Lahan Tanam")
    print("3. Keluar")
    pilih = input("Pilih menu: ").strip()

    if pilih == "1":
        print("\n--- INPUT PARAMETER LAHAN ---")
        user = {}
        for p in PARAMETER:
            while True:
                try:
                    value = float(input(f"Masukkan nilai {INFO_INPUT[p]}: ").replace(",", "."))
                    if value >= 0:
                        user[p] = value
                        break
                    print("  [!] Nilai tidak boleh negatif.")
                except:
                    print("  [!] Masukkan angka yang valid.")

        while True:
            try:
                top_n = int(input(f"Jumlah rekomendasi (1-{len(komoditas)}): "))
                if 1 <= top_n <= len(komoditas):
                    break
                print(f"  [!] Pilih angka antara 1 sampai {len(komoditas)}.")
            except:
                print("  [!] Masukkan angka bulat yang valid.")

        hasil = []
        for tanaman in aturan:
            total_poin = 0
            cocok = 0
            for p in PARAMETER:
                v = user[p]
                nilai_min = aturan[tanaman][p]["min"]
                nilai_max = aturan[tanaman][p]["max"]
                average = aturan[tanaman][p]["mean"]
                rentang = max(nilai_max - nilai_min, 1.0)

                if nilai_min <= v <= nilai_max:
                    cocok += 1
                    poin = max(80.0, 100.0 - (abs(v - average) / (rentang / 2.0)) * 20.0)
                else:
                    selisih = (nilai_min - v) if v < nilai_min else (v - nilai_max)
                    poin = max(0.0, 80.0 - (selisih / rentang) * 80.0)

                total_poin += poin

            skor_akhir = total_poin / 7
            hasil.append((skor_akhir, tanaman, cocok))

        hasil.sort(reverse=True)
        print("\n--- SKOR UNTUK KOMODITAS ---")
        print(f"{'No':<4} | {'Komoditas':<12} | {'Skor':>10} | Sesuai")
        print("-" * 45)
        for no, (skor, tanaman, cocok) in enumerate(hasil, 1):
            print(f"{no:<4} | {tanaman:<12} | {skor:>10.2f} | {cocok}/7")
            
        print(f"\n--- Jumlah Rekomendasi Tanaman Terbaik ---")
        for i in range(top_n):
            skor, tanaman, cocok = hasil[i]
            print(f"{i+1}. {tanaman:<12} | Skor: {skor:6.2f}/100 | Sesuai: {cocok}/7 parameter")

        print(f"\nPilih komoditas yang ingin didiagnosis: {', '.join(komoditas)}")
        target = input("Pilih tanaman target untuk diagnosis: ").strip().lower()
        while target not in aturan:
            print("  [!] Nama tanaman tidak ditemukan.")
            target = input("Pilih tanaman target untuk diagnosis: ").strip().lower()

        print(f"\n--- DIAGNOSIS LAHAN UNTUK '{target.upper()}' ---")
        print(f"{'Parameter':<14} | {'Input':<7} | {'Acuan (Min-Max)':<17} | {'Rata2':<7} | Status")
        print("-" * 67)
        for p in PARAMETER:
            v = user[p]
            nilai_min = aturan[target][p]["min"]
            nilai_max = aturan[target][p]["max"]
            average = aturan[target][p]["mean"]

            if v < nilai_min:
                status = f"KURANG (-{nilai_min - v:.1f})"
            elif v > nilai_max:
                status = f"BERLEBIH (+{v - nilai_max:.1f})"
            else:
                status = "SESUAI"

            print(f"{NAMA_TAMPIL[p]:<14} | {v:<7.2f} | {nilai_min:>6.2f} - {nilai_max:<8.2f} | {average:<7.2f} | {status}")
            
    elif pilih == "2":
        print(f"\nPilih komoditas yang ingin didiagnosis: {', '.join(komoditas)}")
        target = input("Nama tanaman: ").strip().lower()
        if target in aturan:
            print(f"\n--- BATASAN ACUAN '{target.upper()}' ---")
            s = aturan[target][p]
            if s["n"] == 1 
                    print(f"{NAMA_TAMPIL[p]:<14}: Min={s['min']:6.2f}")
        else:
             print(f"{NAMA_TAMPIL[p]:<14}: Min={s['min']:6.2f} | Max={s['max']:6.2f} | Rata2={s['mean']:6.2f}")
        print("  [!] Tanaman tidak ditemukan.")

    elif pilih == "3":
        break
    else:
        print("[!] Menu tidak valid.")

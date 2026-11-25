import csv

NAMA_FILE = "Crop_recommendation 2000.csv"
PARAMETER = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

data = {}
sudah_ada = []
valid = 0
invalid = 0

try:
    file = open(NAMA_FILE, mode="r", encoding="utf-8-sig")
    baris_pertama = file.readline()
    pemisah = ";" if ";" in baris_pertama else ","
    file.seek(0)

    pembaca = csv.DictReader(file, delimiter=pemisah)
    if pembaca.fieldnames is None:
        print("[ERROR] File CSV kosong.")
        exit()

    for row in pembaca:
        try:
            tanaman = row["label"].strip().lower()
            angka = []
            for p in PARAMETER:
                nilai = float(row[p].replace(",", "."))
                angka.append(nilai)

            baris_cek = (tanaman, tuple(angka))

            if tanaman == "" or min(angka) < 0 or baris_cek in sudah_ada:
                invalid += 1
                continue

            sudah_ada.append(baris_cek)

            if tanaman not in data:
                data[tanaman] = {
                    "N": [], "P": [], "K": [],
                    "temperature": [], "humidity": [], "ph": [], "rainfall": []
                }
                
            for i in range(7):
                p = PARAMETER[i]
                data[tanaman][p].append(angka[i])

            valid += 1
        except:
            invalid += 1

    file.close()
except FileNotFoundError:
    print(f"[ERROR] File '{NAMA_FILE}' tidak ditemukan!")
    exit()

if valid == 0:
    print("[ERROR] Tidak ada data valid di dalam CSV.")
    exit()

aturan = {}
for tan in data:
    aturan[tan] = {}
    for p in PARAMETER:
        kumpulan = data[tan][p]
        aturan[tan][p] = {
            "min": min(kumpulan),
            "max": max(kumpulan),
            "mean": sum(kumpulan) / len(kumpulan)
        }

print(f"[INFO] Berhasil memuat CSV ({valid} data valid, {invalid} diabaikan, {len(aturan)} tanaman).")
komoditas = sorted(aturan.keys())

while True:
    print("\n1. Rekomendasi & Diagnosis")
    print("2. Cek Batasan Tanaman")
    print("3. Keluar")
    pilih = input("Pilih menu: ").strip()

    if pilih == "1":
        print("\n--- INPUT PARAMETER LAHAN ---")
        user = {}
        for p in PARAMETER:
            while True:
                try:
                    val = float(input(f"Input {p:<12}: ").replace(",", "."))
                    if val >= 0:
                        user[p] = val
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
        for tan in aturan:
            total_poin = 0
            cocok = 0
            for p in PARAMETER:
                v = user[p]
                mn = aturan[tan][p]["min"]
                mx = aturan[tan][p]["max"]
                avg = aturan[tan][p]["mean"]
                rentang = max(mx - mn, 1.0)

                if mn <= v <= mx:
                    cocok += 1
                    poin = max(80.0, 100.0 - (abs(v - avg) / (rentang / 2.0)) * 20.0)
                else:
                    selisih = (mn - v) if v < mn else (v - mx)
                    poin = max(0.0, 80.0 - (selisih / rentang) * 80.0)

                total_poin += poin

            skor_akhir = total_poin / 7
            print(f"Skor untuk {tan}: {skor_akhir}")
            hasil.append((skor_akhir, tan, cocok))

        hasil.sort(reverse=True)

        print(f"\n--- TOP {top_n} REKOMENDASI TANAMAN ---")
        for i in range(top_n):
            skor, tan, cocok = hasil[i]
            print(f"{i+1}. {tan:<12} | Skor: {skor:6.2f}/100 | Sesuai: {cocok}/7 parameter")

        # Pilih tanaman target untuk diagnosis
        print(f"\nKomoditas: {', '.join(komoditas)}")
        target = input("Pilih tanaman target untuk diagnosis: ").strip().lower()
        while target not in aturan:
            print("  [!] Nama tanaman tidak ditemukan.")
            target = input("Pilih tanaman target untuk diagnosis: ").strip().lower()

        print(f"\n--- DIAGNOSIS LAHAN UNTUK '{target.upper()}' ---")
        print(f"{'Parameter':<12} | {'Input':<7} | {'Acuan (Min-Max)':<17} | {'Rata2':<7} | Status")
        print("-" * 65)
        for p in PARAMETER:
            v = user[p]
            mn = aturan[target][p]["min"]
            mx = aturan[target][p]["max"]
            avg = aturan[target][p]["mean"]

            if v < mn:
                status = f"KURANG (-{mn - v:.1f})"
            elif v > mx:
                status = f"BERLEBIH (+{v - mx:.1f})"
            else:
                status = "SESUAI"

            print(f"{p:<12} | {v:<7.2f} | {mn:>6.2f} - {mx:<8.2f} | {avg:<7.2f} | {status}")

    elif pilih == "2":
        print(f"\nKomoditas: {', '.join(komoditas)}")
        target = input("Nama tanaman: ").strip().lower()
        if target in aturan:
            print(f"\n--- BATASAN ACUAN '{target.upper()}' ---")
            for p in PARAMETER:
                s = aturan[target][p]
                print(f"{p:<12}: Min={s['min']:6.2f} | Max={s['max']:6.2f} | Rata2={s['mean']:6.2f}")
        else:
            print("  [!] Tanaman tidak ditemukan.")

    elif pilih == "3":
        break
    else:
        print("[!] Menu tidak valid.")

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
                

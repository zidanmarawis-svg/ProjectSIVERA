# ml/generate_dataset.py
# Membangkitkan dataset sintetis 600 baris dengan aturan logis.
import random
import csv

random.seed(42)
rows = []
for _ in range(600):
    penghasilan = random.choice([500_000, 1_000_000, 1_500_000, 2_000_000,
                                 3_000_000, 4_000_000, 6_000_000])
    tanggungan = random.randint(1, 7)
    kondisi_rumah = random.randint(1, 5)       # 1 buruk - 5 baik
    kepemilikan_aset = random.randint(1, 5)    # 1 sedikit - 5 banyak
    status_pekerjaan = random.randint(1, 5)    # 1 tidak tetap - 5 tetap

    # Aturan label: penghasilan rendah + tanggungan tinggi + rumah buruk => layak
    skor = (penghasilan < 2_000_000) * 2 + (tanggungan >= 4) * 1 + \
           (kondisi_rumah <= 2) * 2 + (kepemilikan_aset <= 2) * 1 + \
           (status_pekerjaan <= 2) * 1
    label = 1 if skor >= 4 else 0

    rows.append([penghasilan, tanggungan, kondisi_rumah,
                 kepemilikan_aset, status_pekerjaan, label])

with open('ml/dataset_sintetis.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['penghasilan', 'tanggungan', 'kondisi_rumah',
                'kepemilikan_aset', 'status_pekerjaan', 'label_layak'])
    w.writerows(rows)
print(f'Dataset dibuat: {len(rows)} baris')
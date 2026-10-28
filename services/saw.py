# services/saw.py
# Fungsi murni perhitungan SAW. Dipisah agar mudah diuji.

def normalisasi(nilai, tipe, max_val, min_val):
    """Normalisasi satu nilai sesuai tipe kriteria."""
    if tipe == 'benefit':
        return nilai / max_val if max_val > 0 else 0
    else:  # cost
        return min_val / nilai if nilai > 0 else 0


def hitung_saw(data_warga, kriteria_list, referensi):
    """
    Menghitung skor SAW.
    data_warga: dict {nama_kriteria: nilai}
    kriteria_list: list dict {'nama','bobot','tipe'}
    referensi: dict {nama_kriteria: {'max':..., 'min':...}}
    Return: skor float 0-1
    """
    skor = 0.0
    for k in kriteria_list:
        nama = k['nama']
        nilai = data_warga.get(nama, 0)
        max_val = referensi[nama]['max']
        min_val = referensi[nama]['min']
        r = normalisasi(nilai, k['tipe'], max_val, min_val)
        skor += k['bobot'] * r
    return round(skor, 4)


def kategori_saw(skor, ambang_layak=0.7, ambang_pertimbangan=0.5):
    """Mengembalikan kategori berdasarkan ambang batas."""
    if skor >= ambang_layak:
        return 'layak'
    elif skor >= ambang_pertimbangan:
        return 'dipertimbangkan'
    return 'tidak layak'
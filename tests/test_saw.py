# tests/test_saw.py
# Unit test perhitungan SAW dengan contoh manual.
from services.saw import hitung_saw, kategori_saw


def test_saw_manual():
    # Dua kriteria: C1 benefit bobot 0.6, C2 cost bobot 0.4
    # Data acuan: C1 max=100, C2 min=10
    # Warga: C1=80, C2=20
    # Normalisasi: C1=80/100=0.8 ; C2=10/20=0.5
    # Skor = 0.6*0.8 + 0.4*0.5 = 0.68
    kriteria = [
        {'nama': 'C1', 'bobot': 0.6, 'tipe': 'benefit'},
        {'nama': 'C2', 'bobot': 0.4, 'tipe': 'cost'},
    ]
    referensi = {'C1': {'max': 100, 'min': 0}, 'C2': {'max': 100, 'min': 10}}
    data = {'C1': 80, 'C2': 20}
    assert hitung_saw(data, kriteria, referensi) == 0.68


def test_kategori():
    assert kategori_saw(0.8) == 'layak'
    assert kategori_saw(0.6) == 'dipertimbangkan'
    assert kategori_saw(0.3) == 'tidak layak'
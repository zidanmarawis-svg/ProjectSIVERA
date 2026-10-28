# services/ml_predictor.py
# Memuat model Random Forest dan memprediksi kelayakan.
import os
import joblib
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'ml', 'model_rf.pkl')
_model = None

def load_model():
    """Muat model sekali saja (lazy loading)."""
    global _model
    if _model is None and os.path.exists(MODEL_PATH):
        _model = joblib.load(MODEL_PATH)
    return _model


def prediksi(data_warga):
    """
    data_warga: dict dengan key:
    penghasilan, tanggungan, kondisi_rumah, kepemilikan_aset, status_pekerjaan_skor
    Return: 1 (layak) atau 0 (tidak layak). None jika model tidak ada.
    """
    model = load_model()
    if model is None:
        return None
    fitur = [[
        data_warga['penghasilan'],
        data_warga['tanggungan'],
        data_warga['kondisi_rumah'],
        data_warga['kepemilikan_aset'],
        data_warga['status_pekerjaan_skor'],
    ]]
    return int(model.predict(fitur)[0])


def gabungkan_hasil(kategori_saw, prediksi_ml):
    """Logika gabungan: sepakat => yakin, beda => review manual."""
    if prediksi_ml is None:
        return 'Perlu Review Manual'
    saw_layak = kategori_saw in ['layak', 'dipertimbangkan']
    ml_layak = prediksi_ml == 1
    return 'Rekomendasi Yakin' if saw_layak == ml_layak else 'Perlu Review Manual'
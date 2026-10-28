# models.py
# Definisi semua tabel database menggunakan SQLAlchemy.
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """Tabel pengguna: warga, staf, admin."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'warga' / 'staf' / 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ProfilWarga(db.Model):
    """Data profil warga, terhubung 1-1 dengan User."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    nik = db.Column(db.String(16), unique=True, nullable=False)
    no_kk = db.Column(db.String(16), nullable=False)
    nama_lengkap = db.Column(db.String(120), nullable=False)
    alamat = db.Column(db.Text)


class Kriteria(db.Model):
    """Kriteria penilaian SAW. Bobot total harus 1.0."""
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50), unique=True, nullable=False)
    bobot = db.Column(db.Float, nullable=False)
    tipe = db.Column(db.String(10), nullable=False)  # 'benefit' / 'cost'


class Pengajuan(db.Model):
    """Pengajuan bantuan dari warga."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nik = db.Column(db.String(16), nullable=False)
    no_kk = db.Column(db.String(16), nullable=False)
    nama = db.Column(db.String(120), nullable=False)
    alamat = db.Column(db.Text)
    penghasilan = db.Column(db.Float, nullable=False)
    tanggungan = db.Column(db.Integer, nullable=False)
    pekerjaan = db.Column(db.String(80))
    status_rumah = db.Column(db.String(50))
    kondisi_rumah = db.Column(db.Integer, default=3)  # skala 1-5
    kepemilikan_aset = db.Column(db.Integer, default=3)  # skala 1-5
    status_pekerjaan_skor = db.Column(db.Integer, default=3)  # skala 1-5
    periode = db.Column(db.Integer, nullable=False)  # tahun pengajuan
    status = db.Column(db.String(30), default='menunggu')  # menunggu/diverifikasi/disetujui/ditolak/perbaikan
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class DokumenPengajuan(db.Model):
    """File dokumen yang diunggah warga."""
    id = db.Column(db.Integer, primary_key=True)
    pengajuan_id = db.Column(db.Integer, db.ForeignKey('pengajuan.id'), nullable=False)
    jenis = db.Column(db.String(20))  # KTP / KK / SKTM / FOTO_RUMAH
    filename = db.Column(db.String(200), nullable=False)


class HasilPenilaian(db.Model):
    """Hasil SAW + ML untuk satu pengajuan."""
    id = db.Column(db.Integer, primary_key=True)
    pengajuan_id = db.Column(db.Integer, db.ForeignKey('pengajuan.id'), unique=True)
    skor_saw = db.Column(db.Float)
    kategori_saw = db.Column(db.String(30))
    prediksi_ml = db.Column(db.Integer)  # 1 layak, 0 tidak
    status_gabungan = db.Column(db.String(30))  # 'Rekomendasi Yakin' / 'Perlu Review Manual'


class Verifikasi(db.Model):
    """Keputusan staf atas pengajuan."""
    id = db.Column(db.Integer, primary_key=True)
    pengajuan_id = db.Column(db.Integer, db.ForeignKey('pengajuan.id'))
    staf_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    keputusan = db.Column(db.String(30))  # setuju / tolak / perbaikan
    catatan = db.Column(db.Text, nullable=False)
    waktu = db.Column(db.DateTime, default=datetime.utcnow)


class RiwayatBantuan(db.Model):
    """Riwayat penerimaan bantuan per NIK untuk cegah penerima ganda."""
    id = db.Column(db.Integer, primary_key=True)
    nik = db.Column(db.String(16), nullable=False)
    periode = db.Column(db.Integer, nullable=False)
    keterangan = db.Column(db.String(200))


class AuditLog(db.Model):
    """Catatan siapa melakukan apa dan kapan."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    aksi = db.Column(db.String(200))
    waktu = db.Column(db.DateTime, default=datetime.utcnow)


class Pengaturan(db.Model):
    """Pengaturan ambang batas kategori SAW yang bisa diubah admin."""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(50), nullable=False)
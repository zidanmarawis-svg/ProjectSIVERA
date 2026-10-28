# config.py
# Konfigurasi aplikasi Flask.
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Kunci rahasia untuk sesi login. Ganti di produksi.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ganti-kunci-ini-di-produksi')
    # Lokasi database SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'capstone.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Folder penyimpanan dokumen upload
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # Maksimal 2 MB per request
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
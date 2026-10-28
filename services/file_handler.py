# services/file_handler.py
# Penanganan upload file dengan validasi.
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename):
    """Cek ekstensi file diizinkan."""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def simpan_file(file_storage, jenis):
    """
    Simpan file ke folder upload dengan nama unik.
    Return: nama file tersimpan, atau None jika tidak valid.
    """
    if not file_storage or file_storage.filename == '':
        return None
    if not allowed_file(file_storage.filename):
        return None
    ext = file_storage.filename.rsplit('.', 1)[1].lower()
    uname = f"{jenis}_{uuid.uuid4().hex}.{ext}"
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], uname)
    file_storage.save(path)
    return uname
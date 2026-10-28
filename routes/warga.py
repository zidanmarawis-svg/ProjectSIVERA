# routes/warga.py
# Fitur warga: form pengajuan, lacak status, banding.
import re
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import (db, Pengajuan, DokumenPengajuan, HasilPenilaian,
                    Kriteria, AuditLog, Verifikasi)
from routes.auth import role_required
from services.file_handler import simpan_file
from services import saw, ml_predictor

warga_bp = Blueprint('warga', __name__)


def _hitung_dan_simpan_penilaian(pengajuan):
    """Hitung SAW + ML lalu simpan ke HasilPenilaian."""
    # Ambil kriteria dari DB
    kriterias = Kriteria.query.all()
    kriteria_list = [{'nama': k.nama, 'bobot': k.bobot, 'tipe': k.tipe} for k in kriterias]

    # Referensi max/min dari seluruh pengajuan (untuk normalisasi)
    semua = Pengajuan.query.all()
    referensi = {}
    for k in kriteria_list:
        vals = [getattr(p, _map_nama(k['nama']), 0) or 0 for p in semua]
        referensi[k['nama']] = {'max': max(vals) if vals else 1,
                                'min': min(vals) if vals else 0}

    data_warga = {
        'penghasilan': pengajuan.penghasilan,
        'tanggungan': pengajuan.tanggungan,
        'kondisi_rumah': pengajuan.kondisi_rumah,
        'kepemilikan_aset': pengajuan.kepemilikan_aset,
        'status_pekerjaan': pengajuan.status_pekerjaan_skor,
    }
    skor = saw.hitung_saw(data_warga, kriteria_list, referensi)
    kategori = saw.kategori_saw(skor)

    pred_ml = ml_predictor.prediksi({
        'penghasilan': pengajuan.penghasilan,
        'tanggungan': pengajuan.tanggungan,
        'kondisi_rumah': pengajuan.kondisi_rumah,
        'kepemilikan_aset': pengajuan.kepemilikan_aset,
        'status_pekerjaan_skor': pengajuan.status_pekerjaan_skor,
    })
    status_gab = ml_predictor.gabungkan_hasil(kategori, pred_ml)

    hasil = HasilPenilaian(pengajuan_id=pengajuan.id, skor_saw=skor,
                           kategori_saw=kategori, prediksi_ml=pred_ml,
                           status_gabungan=status_gab)
    db.session.add(hasil)


def _map_nama(nama_kriteria):
    """Peta nama kriteria -> atribut model Pengajuan."""
    return {
        'penghasilan': 'penghasilan',
        'tanggungan': 'tanggungan',
        'kondisi_rumah': 'kondisi_rumah',
        'kepemilikan_aset': 'kepemilikan_aset',
        'status_pekerjaan': 'status_pekerjaan_skor',
    }.get(nama_kriteria, nama_kriteria)


@warga_bp.route('/pengajuan/baru', methods=['GET', 'POST'])
@login_required
@role_required('warga')
def ajukan():
    if request.method == 'POST':
        nik = request.form['nik'].strip()
        # Validasi NIK 16 digit numerik
        if not re.fullmatch(r'\d{16}', nik):
            flash('NIK harus 16 digit angka')
            return redirect(request.url)

        periode = datetime.now().year
        # Cegah pengajuan ganda satu NIK per periode
        if Pengajuan.query.filter_by(nik=nik, periode=periode).first():
            flash('NIK ini sudah mengajukan pada periode ini')
            return redirect(request.url)

        p = Pengajuan(
            user_id=current_user.id, nik=nik,
            no_kk=request.form['no_kk'],
            nama=request.form['nama'],
            alamat=request.form['alamat'],
            penghasilan=float(request.form['penghasilan']),
            tanggungan=int(request.form['tanggungan']),
            pekerjaan=request.form.get('pekerjaan', ''),
            status_rumah=request.form.get('status_rumah', ''),
            kondisi_rumah=int(request.form.get('kondisi_rumah', 3)),
            kepemilikan_aset=int(request.form.get('kepemilikan_aset', 3)),
            status_pekerjaan_skor=int(request.form.get('status_pekerjaan_skor', 3)),
            periode=periode,
        )
        db.session.add(p)
        db.session.flush()  # dapatkan ID

        # Simpan dokumen
        for jenis in ['KTP', 'KK', 'SKTM', 'FOTO_RUMAH']:
            f = request.files.get(f'dok_{jenis}')
            nama_file = simpan_file(f, jenis)
            if nama_file:
                db.session.add(DokumenPengajuan(pengajuan_id=p.id,
                                                jenis=jenis, filename=nama_file))

        # Hitung penilaian
        _hitung_dan_simpan_penilaian(p)

        db.session.add(AuditLog(user_id=current_user.id,
                                aksi=f'ajukan bantuan id={p.id}'))
        db.session.commit()
        flash('Pengajuan berhasil dikirim')
        return redirect(url_for('warga.status'))

    return render_template('warga/form_pengajuan.html')


@warga_bp.route('/status')
@login_required
@role_required('warga')
def status():
    daftar = Pengajuan.query.filter_by(user_id=current_user.id)\
        .order_by(Pengajuan.created_at.desc()).all()
    return render_template('warga/status.html', daftar=daftar)


@warga_bp.route('/banding/<int:pid>', methods=['POST'])
@login_required
@role_required('warga')
def banding(pid):
    p = Pengajuan.query.get_or_404(pid)
    if p.user_id != current_user.id:
        return 'Akses ditolak', 403
    p.status = 'banding'
    db.session.add(AuditLog(user_id=current_user.id,
                            aksi=f'banding pengajuan id={pid}'))
    db.session.commit()
    flash('Banding dikirim')
    return redirect(url_for('warga.status'))
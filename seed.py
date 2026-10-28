# seed.py
# Mengisi data awal: admin, staf, warga, kriteria.
from app import create_app
from models import db, User, Kriteria, Pengaturan, ProfilWarga

app = create_app()
with app.app_context():
    db.create_all()

    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', role='admin'); admin.set_password('admin123')
        staf = User(username='staf', role='staf'); staf.set_password('staf123')
        warga = User(username='warga', role='warga'); warga.set_password('warga123')
        db.session.add_all([admin, staf, warga])
        db.session.flush()

        db.session.add(ProfilWarga(user_id=warga.id, nik='3201010101010001',
                                   no_kk='3201010101010002', nama_lengkap='Budi',
                                   alamat='Jl. Contoh No. 1'))

        # Kriteria awal sesuai spesifikasi
        kriteria_awal = [
            ('penghasilan', 0.30, 'cost'),
            ('tanggungan', 0.20, 'benefit'),
            ('kondisi_rumah', 0.20, 'benefit'),
            ('kepemilikan_aset', 0.15, 'cost'),
            ('status_pekerjaan', 0.15, 'benefit'),
        ]
        for nama, bobot, tipe in kriteria_awal:
            db.session.add(Kriteria(nama=nama, bobot=bobot, tipe=tipe))

        db.session.add(Pengaturan(key='ambang_layak', value='0.7'))
        db.session.add(Pengaturan(key='ambang_pertimbangan', value='0.5'))
        db.session.commit()
        print('Seed selesai.')
    else:
        print('Data sudah ada, seed dilewati.')
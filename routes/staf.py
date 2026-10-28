# routes/staf.py
# Halaman verifikasi staf.
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from models import db, Pengajuan, HasilPenilaian, Verifikasi, AuditLog, DokumenPengajuan
from routes.auth import role_required

staf_bp = Blueprint('staf', __name__)


@staf_bp.route('/verifikasi')
@login_required
@role_required('staf')
def verifikasi():
    # Filter & pagination sederhana
    q = request.args.get('q', '').strip()
    status = request.args.get('status', '')
    page = request.args.get('page', 1, type=int)
    query = Pengajuan.query
    if q:
        query = query.filter(Pengajuan.nama.contains(q) | Pengajuan.nik.contains(q))
    if status:
        query = query.filter(Pengajuan.status == status)
    daftar = query.order_by(Pengajuan.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('staf/verifikasi.html', daftar=daftar, q=q, status=status)


@staf_bp.route('/verifikasi/<int:pid>', methods=['GET', 'POST'])
@login_required
@role_required('staf')
def detail(pid):
    p = Pengajuan.query.get_or_404(pid)
    hasil = HasilPenilaian.query.filter_by(pengajuan_id=pid).first()
    dokumen = DokumenPengajuan.query.filter_by(pengajuan_id=pid).all()

    if request.method == 'POST':
        keputusan = request.form['keputusan']
        catatan = request.form['catatan'].strip()
        if not catatan:
            flash('Catatan wajib diisi')
            return redirect(request.url)
        db.session.add(Verifikasi(pengajuan_id=pid, staf_id=current_user.id,
                                  keputusan=keputusan, catatan=catatan))
        p.status = {'setuju': 'disetujui', 'tolak': 'ditolak',
                    'perbaikan': 'perbaikan'}.get(keputusan, p.status)
        db.session.add(AuditLog(user_id=current_user.id,
                                aksi=f'verifikasi id={pid} => {keputusan}'))
        db.session.commit()
        flash('Keputusan disimpan')
        return redirect(url_for('staf.verifikasi'))

    return render_template('staf/detail.html', p=p, hasil=hasil, dokumen=dokumen)